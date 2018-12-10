#import make_music
import xml.etree.ElementTree as ET
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips,  TextClip, CompositeVideoClip, ColorClip, CompositeAudioClip
from moviepy.audio.fx.volumex import volumex
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx

from make_music import find_longest, search_for_best_silent


from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence

import numpy
import os
import re

from audiotsm import phasevocoder
from audiotsm.io.wav import WavReader, WavWriter



def convert_time(timestring):
    """ Converts a string into seconds """
    nums = timestring.split(":")
    hours = int(nums[0])
    minutes = int(nums[1])
    seconds = int(nums[2].split(",")[0])
    millis = float(nums[2].split(",")[1])
    #print 3600*hours + 60*minutes + seconds + millis/1000
    return 3600*hours + 60*minutes + seconds + millis/1000
def convert_time_to_millis(timestring):
    """ Converts a string into seconds """
    nums = timestring.split(":")
    hours = int(nums[0])
    minutes = int(nums[1])
    seconds = int(nums[2].split(",")[0])
    millis = float(nums[2].split(",")[1])
    #print 3600*hours + 60*minutes + seconds + millis/1000
    return 3600*hours*1000 + 60*minutes*1000 + seconds*1000 + millis


def xml_timing(xml_path, lyrics_len):
	tree = ET.parse(xml_path)
	root = tree.getroot()
	word_dur_time = []
	karaoke = root.find("karaoke")
	for pg in karaoke.findall("page"):
		if int(pg.get("id")) < lyrics_len:
			for ln in pg.findall("line"):
				for word in ln.findall("word"):
					text = ""
					start = ""
					end = ""
					count = 0
					syls = word.findall("syllabe")
					for syl in syls:
						count += 1
						text += syl.find("text").text
						if count == 1:
							start = syl.find("start").text
						if count == len(syls):
							end = syl.find("end").text
					
					#print text, start
					#print convert_time(start)
					if convert_time(start) >= 0:
						word_dur_time.append([text, start, end])
	return word_dur_time

#print xml_timing("hacks/karaoke-versions/sub_times/shape_of_you.xml",7)

def xml_line_timing(xml_path, lyrics_len):
	tree = ET.parse(xml_path)
	root = tree.getroot()
	word_dur_time = []
	karaoke = root.find("karaoke")
	for pg in karaoke.findall("page"):
		if int(pg.get("id")) < lyrics_len:
			for ln in pg.findall("line"):
				start = ""
				text = ""
				end = ""
				count = 0
				words = ln.findall("word")
				for word in words:
					count += 1
					syl_count = 0
					syls = word.findall("syllabe")
					for syl in syls:
						syl_count += 1
						text += syl.find("text").text
						if count == 1:
							start = syl.find("start").text
						if count == len(words):
							end = syl.find("end").text
						if syl_count ==len(syls):
							text += " "
					
					#print text, start
					#print convert_time(start)
				if convert_time(start) >= 0:
					word_dur_time.append([text, start, end])
	return word_dur_time


#dur = start, time = end
def make_song_xml(song_name,lyr_len):

	xml_path = "hacks/karaoke-versions/sub_times/"+song_name.replace(" ","_").lower()+".xml"
	m4a_path = "karaoke/kml_audio/"+song_name.replace(" ","_").lower()+".m4a"
	lyr_start = 0

	word_dur_time = xml_timing(xml_path, lyr_len)
	line_start_end = xml_line_timing(xml_path, lyr_len)

	print word_dur_time
	audio = AudioFileClip(m4a_path)
	audio = audio.fx(volumex, 0.1)
	cuts_dirs = []
	found = []
	not_found = []
	db_values = []
	skip = 0

	total_skip = 0

	
	for word, dur, time in word_dur_time:

		if (skip > 0):

			print "SKIPPED"
			skip -=1
			continue

		pair_index = word_dur_time.index([word, dur, time])
		word = word.replace(" ", "")
		print "Word = "+word
		
		cuts_words = find_longest(word.lower(), pair_index, word_dur_time)
		

		if len(cuts_words[0]) == 0:
			cuts_dirs.append(("Not Found", dur, time))
			not_found.append(word)
			print "\""+word+"\" not found"
		else:
			cut_singles = cuts_words[0]
			word_found = cuts_words[1]
			#print len(cut_singles)

			skip = len(cut_singles) - 1
			total_skip += skip
			for cut_single, d, t in cut_singles:
				found_ind = cut_singles.index((cut_single, d, t))
				#print cut_single, d, t
				#print word_found[found_ind]

				cuts_dirs.append((cut_single, d, t))
				#get db of the file

				song_file = AudioSegment.from_wav(cut_single.replace(".mp4",".wav"))
			#print "db", song_file.dBFS
				db_values.append(song_file.dBFS)

				found.append(word_found[found_ind])

	print found
	print cuts_dirs

	av = numpy.mean(db_values)
	print "av", av

	blank_start = 0
	final_song_cuts = []
	if not os.path.exists("karaoke/temp_videos"):
		os.makedirs("karaoke/temp_videos",0777)
	
	line_num = 1
	word_in_line = 0
	first_word = True
	#			  dur    time
	for i, ( cut, start, end) in enumerate(cuts_dirs):

		start = convert_time(start)
		end = convert_time(end)

		dur = end - start

		#blank = ColorClip((1280,720),(255,255,255), duration = time - blank_start)
		#final_song_cuts.append(blank)
		
		# instead of blank, put silent obama videos

		blank_dur = start - blank_start
		if not (blank_dur == 0):
			blank = search_for_best_silent(blank_dur)
			final_song_cuts.append(blank)

		if cut != "Not Found":
			video = VideoFileClip(cut, audio = False)
			#print dur
			#print "dur",video.duration
			#ratio = video.duration / dur

			


			print cut
			video = video.resize((1280,720))


			video_audio = AudioFileClip(cut.replace(".mp4",".wav"))
			

			# change sound level to average
			db_video_audio = AudioSegment.from_wav(cut.replace(".mp4",".wav"))
			db_level = db_video_audio.dBFS
			coef = pow(10, ((av-db_level)/20))

			if not (cut[cut.index("words/")+6:cut.index("/0.mp4")][0] == 't' or cut[cut.index("words/")+6:cut.index("/0.mp4")][-1] == 't'):
				video_audio = video_audio.volumex(coef)

			#if video_audio.duration > 0.2:
			#	new_audio = video_audio.fx(afx.audio_fadein, 0.1).fx(afx.audio_fadeout, 0.1);
			#else:
			#	new_audio = video_audio.fx(afx.audio_fadein, 0.05).fx(afx.audio_fadeout, 0.05);


			video_audio.write_audiofile("karaoke/temp_videos/before_test.wav")

			tempo =  video_audio.duration / dur
			print "tempo = ", tempo

			with WavReader("karaoke/temp_videos/before_test.wav") as reader:
   		 		with WavWriter("karaoke/temp_videos/test.wav", reader.channels, reader.samplerate) as writer:
   		 			tsm = phasevocoder(reader.channels, speed=tempo)
   		 			tsm.run(reader, writer)
   		 			print "Speed has been changed"
		
			video = video.fx(vfx.speedx, video.duration / dur)
			#add audio to video file
			audio_of_video = AudioFileClip("karaoke/temp_videos/test.wav")
			#audio_of_video = (audio_of_video.fadein(0.1).fadeout(0.1))
			video = video.set_audio(audio_of_video)


			if video.duration > 0.2:
				video = video.audio_fadein(0.01).audio_fadeout(0.01)
			else:
				video = video.audio_fadein(0.001).audio_fadeout(0.001)
			
			#video.write_videofile("karaoke/temp_videos"+str(i)+".mp4", ffmpeg_params=["-atempo","2.0"], codec = 'libx264', audio_codec = 'acc', temp_audiofile = "karaoke/temp_videos"+str(i)+".m4a", remove_temp = True)
			#print "dur", video.duration

		else:
			video = ColorClip((1280,720),(0,0,0), duration = dur)


		#lyr_of_word = find_lyr_of_word(start, text_dur_time)


		#word_text = TextClip(lyr_of_word[0], fontsize = 50, color = "white", bg_color = "black").set_pos(("center", 600)).set_duration(dur)
		#video = CompositeVideoClip([video, word_text])
		final_song_cuts.append(video)


		#print time, dur, time+dur
		blank_start = start + dur
	final_song = concatenate_videoclips(final_song_cuts)

	#for text, dur, time in text_dur_time:
	#	word_text = TextClip(text, fontsize = 50, color = "white", bg_color = "black").set_pos((100,500)).set_start(time).set_duration(dur)
	#	final_song = CompositeVideoClip([final_song, word_text])
	#final_song.audio = CompositeAudioClip([final_song.audio, audio]).set_duration(final_song.duration)
	final_song = final_song.fx(volumex, 1.5)
	final_song.write_videofile("karaoke/"+song_name+"_karaoke_version.mp4", codec='libx264', audio_codec='aac', temp_audiofile="karaoke/"+song_name+".m4a", remove_temp = True)
	#final_song.audio.write_audiofile("karaoke/for_audio_prof/"+song_name+".wav")
#make_song_xml("Shape Of You", 20)
def split_obama_by_line(song_name, xml_path, lyr_len):

	line_start_end = xml_line_timing(xml_path, lyr_len)
	word_start_end = xml_timing(xml_path, lyr_len)

	cuts_dirs = []
	found = []
	not_found = []

	db_values = []
	skip = 0

	total_skip = 0

	
	for word, dur, time in word_start_end:

		if (skip > 0):

			print "SKIPPED"
			skip -=1
			continue

		pair_index = word_start_end.index([word, dur, time])
		word = word.replace(" ", "")
		print "Word = "+word
		
		cuts_words = find_longest(word.lower(), pair_index, word_start_end)

		if len(cuts_words[0]) == 0:
			cuts_dirs.append(("Not Found", dur, time))
			not_found.append(word)
			print "\""+word+"\" not found"
		else:
			cut_singles = cuts_words[0]
			word_found = cuts_words[1]
			#print len(cut_singles)

			skip = len(cut_singles) - 1
			total_skip += skip
			for cut_single, d, t in cut_singles:
				found_ind = cut_singles.index((cut_single, d, t))
				#print cut_single, d, t
				#print word_found[found_ind]

				cuts_dirs.append((cut_single, d, t))
				#get db of the file

				song_file = AudioSegment.from_wav(cut_single.replace(".mp4",".wav"))
			#print "db", song_file.dBFS
				db_values.append(song_file.dBFS)

				found.append(word_found[found_ind])

	print found
	print cuts_dirs

	av = numpy.mean(db_values)


	line_videos = []
	line_start = convert_time(line_start_end[0][1])
	line_end = convert_time(line_start_end[0][2])

	line_count = 1;

	os.makedirs("karaoke/split_parts/"+song_name + "/obama", 0777)

	blank_start = 0
	for cut, start, end in cuts_dirs:

		start = convert_time(start)
		end = convert_time(end)

		dur = end - start

		blank_dur = start - blank_start
		if not (blank_dur == 0):
			blank = search_for_best_silent(blank_dur)
			#line_videos.append(blank)

		if cut != "Not Found":
			video = VideoFileClip(cut, audio = False)


			print cut
			video = video.resize((1280,720))


			video_audio = AudioFileClip(cut.replace(".mp4",".wav"))
			

			# change sound level to average
			db_video_audio = AudioSegment.from_wav(cut.replace(".mp4",".wav"))
			db_level = db_video_audio.dBFS
			coef = pow(10, ((av-db_level)/20))

			if not (cut[cut.index("words/")+6:cut.index("/0.mp4")][0] == 't' or cut[cut.index("words/")+6:cut.index("/0.mp4")][-1] == 't'):
				video_audio = video_audio.volumex(coef)

			#if video_audio.duration > 0.2:
			#	new_audio = video_audio.fx(afx.audio_fadein, 0.1).fx(afx.audio_fadeout, 0.1);
			#else:
			#	new_audio = video_audio.fx(afx.audio_fadein, 0.05).fx(afx.audio_fadeout, 0.05);


			video_audio.write_audiofile("karaoke/temp_videos/before_test.wav")

			tempo =  video_audio.duration / dur
			print "tempo = ", tempo

			with WavReader("karaoke/temp_videos/before_test.wav") as reader:
   		 		with WavWriter("karaoke/temp_videos/test.wav", reader.channels, reader.samplerate) as writer:
   		 			tsm = phasevocoder(reader.channels, speed=tempo)
   		 			tsm.run(reader, writer)
   		 			print "Speed has been changed"
		
			video = video.fx(vfx.speedx, video.duration / dur)
			#add audio to video file
			audio_of_video = AudioFileClip("karaoke/temp_videos/test.wav")
			#audio_of_video = (audio_of_video.fadein(0.1).fadeout(0.1))
			video = video.set_audio(audio_of_video)


			if video.duration > 0.2:
				video = video.audio_fadein(0.01).audio_fadeout(0.01)
			else:
				video = video.audio_fadein(0.001).audio_fadeout(0.001)
			
			#video.write_videofile("karaoke/temp_videos"+str(i)+".mp4", ffmpeg_params=["-atempo","2.0"], codec = 'libx264', audio_codec = 'acc', temp_audiofile = "karaoke/temp_videos"+str(i)+".m4a", remove_temp = True)
			#print "dur", video.duration

		else:
			video = ColorClip((1280,720),(0,0,0), duration = dur)


		if start >= line_start and end <= line_end:
			line_videos.append(video)
		print end, line_end
		if end == line_end:
			fin_line = concatenate_videoclips(line_videos)
			fin_line.audio.write_audiofile("karaoke/split_parts/"+song_name+"/obama/"+str(line_count) + ".wav")

			if not (line_count == len(line_start_end)):
				line_start = convert_time(line_start_end[line_count][1])
				line_end = convert_time(line_start_end[line_count][2])
				line_count += 1
				line_videos = []


		#print time, dur, time+dur
		blank_start = start + dur

def split_obama_by_line_pydub(song_name, xml_path, lyr_len):

	line_start_end = xml_line_timing(xml_path, lyr_len)
	word_start_end = xml_timing(xml_path, lyr_len)

	cuts_dirs = []
	found = []
	not_found = []

	db_values = []
	skip = 0

	total_skip = 0

	
	for word, dur, time in word_start_end:

		if (skip > 0):

			print "SKIPPED"
			skip -=1
			continue

		pair_index = word_start_end.index([word, dur, time])
		word = word.replace(" ", "")
		print "Word = "+word
		
		cuts_words = find_longest(word.lower(), pair_index, word_start_end)

		if len(cuts_words[0]) == 0:
			cuts_dirs.append(("Not Found", dur, time))
			not_found.append(word)
			print "\""+word+"\" not found"
		else:
			cut_singles = cuts_words[0]
			word_found = cuts_words[1]
			#print len(cut_singles)

			skip = len(cut_singles) - 1
			total_skip += skip
			for cut_single, d, t in cut_singles:
				found_ind = cut_singles.index((cut_single, d, t))
				#print cut_single, d, t
				#print word_found[found_ind]

				cuts_dirs.append((cut_single, d, t))
				#get db of the file

				song_file = AudioSegment.from_wav(cut_single.replace(".mp4",".wav"))
			#print "db", song_file.dBFS
				db_values.append(song_file.dBFS)

				found.append(word_found[found_ind])

	print found
	print cuts_dirs

	av = numpy.mean(db_values)


	line_videos = AudioSegment.silent(duration = 0);
	line_start = convert_time(line_start_end[0][1])
	line_end = convert_time(line_start_end[0][2])

	line_count = 1;

	os.makedirs("karaoke/split_parts/"+song_name + "/obama", 0777)

	blank_start = 0
	for cut, start, end in cuts_dirs:

		start = convert_time(start)
		end = convert_time(end)

		dur = end - start

		blank_dur = start - blank_start
		if not (blank_dur == 0):
			blank = search_for_best_silent(blank_dur)
			#line_videos.append(blank)

		if cut != "Not Found":
			#video = VideoFileClip(cut, audio = False)


			print cut
			#video = video.resize((1280,720))


			#video_audio = AudioSegment(cut.replace(".mp4",".wav"))
			

			# change sound level to average
			db_video_audio = AudioSegment.from_wav(cut.replace(".mp4",".wav"))
			db_level = db_video_audio.dBFS
			coef = pow(10, ((av-db_level)/20))

			#if not (cut[cut.index("words/")+6:cut.index("/0.mp4")][0] == 't' or cut[cut.index("words/")+6:cut.index("/0.mp4")][-1] == 't'):
			#	video_audio = video_audio.volumex(coef)

			#if video_audio.duration > 0.2:
			#	new_audio = video_audio.fx(afx.audio_fadein, 0.1).fx(afx.audio_fadeout, 0.1);
			#else:
			#	new_audio = video_audio.fx(afx.audio_fadein, 0.05).fx(afx.audio_fadeout, 0.05);


			video_audio = db_video_audio + (av - db_level)
			#video_audio.write_audiofile("karaoke/temp_videos/before_test.wav")

			audio_faded = video_audio.fade_in(10).fade_out(10)
			

		else:
			#video = ColorClip((1280,720),(0,0,0), duration = dur)
			audio_faded = AudioSegment.silent(duration = dur);


		if start >= line_start and end <= line_end:
			line_videos = line_videos + audio_faded
		print end, line_end
		if end == line_end:
			line_videos.export("karaoke/split_parts/"+song_name+"/obama/"+str(line_count) + ".wav", format = "wav")
			#fin_line = concatenate_videoclips(line_videos)
			#fin_line.audio.write_audiofile("karaoke/split_parts/"+song_name+"/obama/"+str(line_count) + ".wav")

			if not (line_count == len(line_start_end)):
				line_start = convert_time(line_start_end[line_count][1])
				line_end = convert_time(line_start_end[line_count][2])
				line_count += 1
				line_videos = AudioSegment.silent(duration = 0);


		#print time, dur, time+dur
		blank_start = start + dur


#split_obama_by_line_pydub("Shape Of You", "hacks/karaoke-versions/sub_times/shape_of_you.xml", 20)
def split_prof_by_line(song_name, xml_path, audio_src, lyr_len):
	line_start_end = xml_line_timing(xml_path, lyr_len)
	audio = AudioFileClip(audio_src)

	os.makedirs("karaoke/split_parts/"+song_name + "/prof", 0777)
	line_count = 1;
	for line, start, end in line_start_end:
		start = convert_time(start)
		end = convert_time(end)
		print line, start, end
		part = audio.subclip(start, end)
		part.write_audiofile("karaoke/split_parts/" +song_name + "/prof/"+str(line_count)+".wav")
		line_count += 1
def split_prof_by_line_pydub(song_name, xml_path, audio_src, lyr_len):
	line_start_end = xml_line_timing(xml_path, lyr_len)
	audio = AudioSegment.from_mp3(audio_src)

	os.makedirs("karaoke/split_parts/"+song_name + "/prof", 0777)
	line_count = 1;
	for line, start, end in line_start_end:
		start = convert_time(start)
		end = convert_time(end)
		print line, start, end
		part = audio[start*1000:end*1000]
		part.export("karaoke/split_parts/" +song_name + "/prof/"+str(line_count)+".wav", format = "wav")
		line_count += 1
#print xml_line_timing("hacks/karaoke-versions/sub_times/shape_of_you.xml",7)

#split_prof_by_line_pydub("Shape Of You", "hacks/karaoke-versions/sub_times/shape_of_you.xml", "karaoke/for_audio_prof/Shape Of You/Professional Singer.wav", 20)

def final_song(song_dir, xml_path, lyr_len):
	line_start_end = xml_line_timing(xml_path, lyr_len)
	line_count = 1
	audio = AudioSegment.empty()
	last_start = 0
	for line, start, end in line_start_end:
		start = convert_time(start)
		end = convert_time(end)
		if last_start < start:
			audio =audio + AudioSegment.silent(duration = (start*1000 - last_start*1000))
		audio = audio + AudioSegment.from_wav(song_dir+str(line_count)+'.wav')
		line_count += 1
		last_start = end
	audio.export("karaoke/split_parts/Shape Of You/result 2.wav", format = "wav")

final_song("karaoke/split_parts/Shape Of You/obama_res_2/","hacks/karaoke-versions/sub_times/shape_of_you.xml",20 )
def make_song_xml_pydub(song_name, lyr_len):
	xml_path = "hacks/karaoke-versions/sub_times/"+song_name.replace(" ","_").lower()+".xml"
	m4a_path = "karaoke/kml_audio/"+song_name.replace(" ","_").lower()+".m4a"
	lyr_start = 0

	word_dur_time = xml_timing(xml_path, lyr_len)
	line_start_end = xml_line_timing(xml_path, lyr_len)

	print word_dur_time
	cuts_dirs = []
	found = []
	not_found = []
	db_values = []
	skip = 0

	total_skip = 0
	for word, dur, time in word_dur_time:

		if (skip > 0):

			print "SKIPPED"
			skip -=1
			continue

		pair_index = word_dur_time.index([word, dur, time])
		word = word.replace(" ", "")
		print "Word = "+word
		
		cuts_words = find_longest(word.lower(), pair_index, word_dur_time)
		

		if len(cuts_words[0]) == 0:
			cuts_dirs.append(("Not Found", dur, time))
			not_found.append(word)
			print "\""+word+"\" not found"
		else:
			cut_singles = cuts_words[0]
			word_found = cuts_words[1]
			#print len(cut_singles)

			skip = len(cut_singles) - 1
			total_skip += skip
			for cut_single, d, t in cut_singles:
				found_ind = cut_singles.index((cut_single, d, t))
				#print cut_single, d, t
				#print word_found[found_ind]

				cuts_dirs.append((cut_single, d, t))
				#get db of the file

				song_file = AudioSegment.from_wav(cut_single.replace(".mp4",".wav"))
			#print "db", song_file.dBFS
				db_values.append(song_file.dBFS)

				found.append(word_found[found_ind])

	print found
	print cuts_dirs

	blank_start = 0
	final_song_cuts = AudioSegment.silent(duration = 0)
	if not os.path.exists("temp_videos"):
		os.makedirs("temp_videos",0777)
	
	av = numpy.mean(db_values)
	print "av", av

	line_num = 1
	word_in_line = 0
	first_word = True
	#			  dur    time
	for i, ( cut, start, end) in enumerate(cuts_dirs):

		start = convert_time_to_millis(start)
		end = convert_time_to_millis(end)

		dur = end - start

		#blank = ColorClip((1280,720),(255,255,255), duration = time - blank_start)
		#final_song_cuts.append(blank)
		
		# instead of blank, put silent obama videos

		blank_dur = start - blank_start
		if not (blank_dur == 0):
			blank = AudioSegment.silent(duration = blank_dur)
			final_song_cuts = final_song_cuts+blank

		if cut != "Not Found":
			#video = VideoFileClip(cut, audio = False)
			#print dur
			#print "dur",video.duration
			#ratio = video.duration / dur

			


			print cut
			#video = video.resize((1280,720))


			video_audio = AudioSegment.from_wav(cut.replace(".mp4",".wav"))
			

			# change sound level to average
			#db_video_audio = AudioSegment.from_wav(cut.replace(".mp4",".wav"))
			db_level = video_audio.dBFS
			coef = pow(10, ((av-db_level)/20))

			print db_level, "db level"
			print av, "av db"
			video_audio = video_audio + (av - db_level)
			print video_audio.dBFS, "then"

			#if not (cut[cut.index("words/")+6:cut.index("/0.mp4")][0] == 't' or cut[cut.index("words/")+6:cut.index("/0.mp4")][-1] == 't'):
			#video_audio = video_audio.volumex(coef)

			#if video_audio.duration > 0.2:
			#	new_audio = video_audio.fx(afx.audio_fadein, 0.1).fx(afx.audio_fadeout, 0.1);
			#else:
			#	new_audio = video_audio.fx(afx.audio_fadein, 0.05).fx(afx.audio_fadeout, 0.05);


			audio_faded = video_audio.fade_in(10).fade_out(10)
			audio_faded.export("temp_videos/before_test.wav", format = "wav")

			tempo =  (audio_faded.duration_seconds*1000) / dur
			print "tempo = ", tempo
			print "to be dur in millis= ", dur
			print "actual duration in millis=", audio_faded.duration_seconds*1000

			with WavReader("temp_videos/before_test.wav") as reader:
   		 		with WavWriter("temp_videos/test.wav", reader.channels, reader.samplerate) as writer:
   		 			tsm = phasevocoder(reader.channels, speed=tempo)
   		 			tsm.run(reader, writer)
   		 			#print "Speed has been changed"
		
			#video = video.fx(vfx.speedx, video.duration / dur)
			#add audio to video file
			audio_of_video = AudioSegment.from_wav("temp_videos/test.wav")
			print "new duration", audio_of_video.duration_seconds*1000

			fin_audio = audio_of_video.fade_in(10).fade_out(10)
			print "if"
			print fin_audio.duration_seconds

			#audio_of_video = (audio_of_video.fadein(0.1).fadeout(0.1))
			#video = video.set_audio(audio_of_video)

			
			#video.write_videofile("karaoke/temp_videos"+str(i)+".mp4", ffmpeg_params=["-atempo","2.0"], codec = 'libx264', audio_codec = 'acc', temp_audiofile = "karaoke/temp_videos"+str(i)+".m4a", remove_temp = True)
			#print "dur", video.duration

		else:

			fin_audio = AudioSegment.silent(duration = dur)
			print "else"
			print fin_audio.duration_seconds


		#lyr_of_word = find_lyr_of_word(start, text_dur_time)


		#word_text = TextClip(lyr_of_word[0], fontsize = 50, color = "white", bg_color = "black").set_pos(("center", 600)).set_duration(dur)
		#video = CompositeVideoClip([video, word_text])
		final_song_cuts = final_song_cuts + fin_audio


		#print time, dur, time+dur
		blank_start = start + dur
	#final_song = concatenate_videoclips(final_song_cuts)

	final_song_cuts.export("karaoke/"+song_name +" Pydub.wav", format = "wav")

#make_song_xml_pydub("Shape Of You", 20)

