#!/usr/bin/env python
# -*- coding: utf-8 -*-

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips,  TextClip, CompositeVideoClip, ColorClip, CompositeAudioClip
from moviepy.audio.fx.volumex import volumex
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx
import pronouncing

import os
import re # module for regular expressions
from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence

import numpy
import pyaudio

import xml.etree.ElementTree as ET

import ast
from audiotsm import phasevocoder
from audiotsm.io.wav import WavReader, WavWriter




s_dir = "songs"
sen_dir = "video_sentences"
sen_dir_new = "video_sentence"
music_sub_dir = "music_sub_dir"
blank_dir = "obama_silent_videos"

def convert_time(timestring):
    """ Converts a string into seconds """
    nums = map(float, re.findall(r'\d+', timestring))
    return 3600*nums[0] + 60*nums[1] + nums[2] + nums[3]/1000 - 1
def get_times_texts_lrc(subtitle_str):

    with open(subtitle_str) as s:
        my_lines = s.readlines()
    my_times_texts = []

    for i, line in enumerate(my_lines):
    	if i%2 == 0:
        	start_time = line[line.index("[")+1: line.index("]")]
        	text = line[line.index("]")+1:line.index("\r\n")]
        	next_line = my_lines[i+1]
        	end_time = my_lines[i+1][next_line.index("[")+1: next_line.index("]")]
        	if text != "By RentAnAdviser.com":
        		my_times_texts.append(([start_time, end_time], text))
    return my_times_texts
def get_times_texts_srt(subtitle_str):
	with open(subtitle_str) as s:
		my_lines = s.readlines()
	my_times_texts = []
	for i, line in enumerate(my_lines):
		times = re.findall("[0-9]*:[0-9]*:[0-9]*.[0-9]*", line)
		if times != []:
			current_times = map(convert_time, times)
			text = my_lines[i+1][:my_lines[i+1].index("\r\n")]
			if len(my_lines) > i+2 and my_lines[i+1] != "\n":
				text = text + " " + my_lines[i+2][:my_lines[i+2].index("\r\n")]
			if text != "By RentAnAdviser.com":
				my_times_texts.append((current_times, text))
	print my_times_texts
	return my_times_texts
#print get_times_texts_srt("songs/Eminem-Lose-Yourself.srt")


#print get_times_texts_lrc(s_dir+"/Eminem-Lose-Yourself.lrc")


def convert_wav(video_str):
	video = AudioFileClip(video_str)
	video.write_audiofile(video_str + ".wav")
#convert_wav("silent_test.mp4")

def word_filter(word):
	if word.endswith(","):
		word = word[:-1]
	if "’" in word:
		word = word.replace("’", "'")
	if word.endswith("?"):
		word = word[:-1]
	if word.endswith("!"):
		word = word[:-1]
	if word.endswith("in'"):
		word = word.replace("'","g")
	if word == "coz":
		word = "because"
	while word.endswith("."):
		word = word.replace(".", "")
	return word
def text_filter(text):
	if "I'm" in text:
		text = text.replace("I'm", "I am")
	if "I've" in text:
		text = text.replace("I've", "I have")
	return text
def word_dir(word):
	my_word = word_filter(word)
	list_dir = os.listdir(sen_dir)
	sentences = sorted(list_dir) 
	count = 0
	flag = 0
	for sen in sentences:
		#print "Searhing sentence #"+ str(count)
		if os.path.exists(sen_dir+"/"+sen+"/words"):
			pass
			words = os.listdir(sen_dir+"/"+sen+"/words")
			words_dir = sen_dir + "/"+sen+"/words"
			for word in words:
				if my_word == word and (my_word in sen.lower()):
					cut_single = words_dir+"/"+my_word+"/0.mp4"
					return cut_single
		count += 1
	return None
def make_song(who_is_singing, subtitle_srt, music_str, line_num, error_time = 0, audio_volume = 0.1):
	times_texts = get_times_texts_srt(music_sub_dir+"/"+ subtitle_srt)
	audio = AudioFileClip(music_sub_dir+"/"+ music_str)
	audio = audio.subclip(error_time)
	
	audio = audio.fx(volumex, audio_volume)
	line_count = 0

	songs_cuts = []

	for [t1, t2], text in times_texts:
		line_count += 1
		text = text_filter(text)
		#print "|"+text +"|"
		my_words = text.lower().split(" ")
		
		cuts_dirs = []
		found = []
		not_found = []
		for my_word in my_words:
			my_word = word_filter(my_word)
			print "Word = "+my_word
			cut_single = word_dir(my_word)
			if cut_single != None:
				cuts_dirs.append(cut_single)
				found.append(my_word)
			else:
				flag = 0
				if my_word != '' and my_word != ' ':
					rhymes_list = rhymes(my_word)
					for r in rhymes_list:
						print "Rhyme = "+ r
						cut_single = word_dir(r)
						if cut_single != None:
							cuts_dirs.append(cut_single)
							found.append(r)
							flag = 1
							break
				if my_word != '' and my_word != ' ' and flag == 0:
					cuts_dirs.append("Not found")
					not_found.append(my_word)
		print "line_count: ", line_count
		print "text:",text
		print "found:", found
		print "not_found:",not_found
		

		# Now making video
		# Silent video
		silent = VideoFileClip("silent_video.mp4")
		empty_video = ColorClip((1280,720), (0,0,0), duration = 0.1)
		video_cuts = []
		dbs = check_db(cuts_dirs)
		print dbs
		for i, file in enumerate(cuts_dirs):
			print file
			if file == "Not found":
				#video_cuts.append(silent)
				video_cuts.append(empty_video)
			else:
				video = VideoFileClip(file)
				#video = video.fx(volumex, 1/dbs[i])
				video = video.resize((1280,720))
				video_cuts.append(video)

		final = concatenate_videoclips(video_cuts)
		#word_text = TextClip(text, fontsize = 40, color = "white", bg_color = "black").set_pos((100,500)).set_duration(final.duration)
		#final = CompositeVideoClip([final, word_text])

		songs_cuts.append((final, [t1, t2]))
		print "##############################################################"
		if line_count == line_num:
			break
	blank_start = 0
	final_song_cuts = []
	print songs_cuts
	for cut, [t1, t2] in songs_cuts:
		blank = ColorClip((1280,720), (0,0,0), duration= t1 - blank_start)
		print "vid_dur:", cut.duration
		print t1, t2
		print "sub_dur:", t2 - t1
		final_song_cuts.append(blank)
		final_song_cuts.append(cut)
		if cut.duration < t2 - t1:
			blank_start = t1 + cut.duration
		else:
			blank_start = t2
	final_song = concatenate_videoclips(final_song_cuts)

	final_song.audio = CompositeAudioClip([final_song.audio, audio]).set_duration(final_song.duration)
	final_song.write_videofile(s_dir+"/"+ who_is_singing+" singing "+music_str + ".mp4", codec='libx264', audio_codec='aac', temp_audiofile=s_dir+"/" +who_is_singing +" Singing"+music_str +".m4a", remove_temp=True)
def rhymes(word):
	pronunciation_list = pronouncing.phones_for_word(word)
	if len(pronunciation_list) == 0:
		return []
	wor_syl = pronouncing.syllable_count(pronunciation_list[0])

	res = []
	for w in pronouncing.rhymes(word):
		p_list = pronouncing.phones_for_word(w.encode("utf-8"))
		w_syl = pronouncing.syllable_count(p_list[0])
		if w_syl == wor_syl:
			res.append(w.encode("utf-8"))
	return res
def check_db(lst):
	act_dbs = []
	dbs = []
	for file in lst:
		if file != "Not found":
			sound_file = AudioSegment.from_wav(file.replace(".mp4",".wav"))
			dbs.append(sound_file.dBFS)
			act_dbs.append(sound_file.dBFS)
		else:
			act_dbs.append(None)

	print act_dbs
	av = numpy.mean(dbs)
	print av
	vols = []
	for i,file in enumerate(lst):
		if file != "Not found":
			vols.append(1-av/act_dbs[i])
		else:
			vols.append(None)
	return vols

#make_song("Obama","Eminem-Lose-Yourself.srt", "Lose Yourself (Karaoke)-UGbejyDDGPc.mkv.wav", 3, 10)
#make_song("Trump","Disney's-Frozen-Let-It-Go-Sequence-Performed-by-Idina-Menzel.srt","Karaoke   'Let it Go'   Frozen-uCyLO3rsCMA.mkv.wav", 20, 3)
#make_song("Obama","Ed-Sheeran-Shape-Of-You-(Official-Video)(1).srt", "shape of you instrumental.mp4.wav", 20)
#make_song("Obama","Luis-Fonsi,-Daddy-Yankee-Despacito-(Audio)-ft.-Justin-Bieber.srt","Luis Fonsi, Daddy Yankee ft. Justin Bieber - Despacito (Karaoke Version)-jRpDuEgqQQQ.mkv.wav", 11, 10)
#make_song("Trump", "Wiz Khalifa -See You Again- ft. Charlie Puth.srt","Wiz Khalifa ft. Charlie Puth - See You Again (Karaoke Version)-ecd4MmrUKrw.mkv.wav",20, 10)
#make_song("Trump","Maroon-5-Sugar.srt", "Maroon 5 - Sugar (Karaoke Version)-PqX8aA6w4bM.mkv.wav", 20, 10)
#make_song("Trump","OneRepublic-Counting-Stars.srt", "OneRepublic - Counting Stars (Karaoke Version)-3EG3CfTv4lQ.webm.wav", 2, 10, 0.03)
#make_song("Passenger-Let-Her-Go-(Official-Video).srt", "Let Her Go (Piano Karaoke Version) Passenger-BAPhZMg9gnk.mkv.wav", 20)
#make_song("Obama", "Adele-Hello.srt", "Adele-Hello Karaoke Version(BY -SING KING KARAOKE)-q2UVTPlKZtQ.mp4", 2, 10, )
#make_song("Obama", "John-Legend-All-of-Me.srt", "John Legend - All of Me (Karaoke Version)-kr8wPkdHFA0.mp4", 10, 10, 0.03)
def cut_professional_songs(subtitle_srt, music_str, line_start, line_num):
	times_texts = get_times_texts_srt(music_sub_dir + "/"+subtitle_srt)
	line_count = line_start
	audio = AudioFileClip(music_str)
	texts_2 =[]
	lines_2 = []
	texts_3 =[]
	lines_3 = []
	texts_4 =[]
	lines_4 = []
	texts_5 =[]
	lines_5 = []
	thresh = 0;


	sound_file = AudioSegment.from_wav(music_str)
	audio_chunks = split_on_silence(sound_file, silence_thresh=sound_file.dBFS-1, min_silence_len=1000)

	print audio_chunks
	for i, chunk in enumerate(audio_chunks):
		chunk.export("songs/Professional Shape Of You Lines/lines 1/"+times_texts[line_start+i][1], format="wav")
"""
	for ind, ([t1, t2], text) in enumerate(times_texts):
		if ind < line_start:
			thresh = t2
			continue
		line_count += 1
		final = audio.subclip(t1-thresh, t2-thresh)
		text = text_filter(text)

		lines_2.append(final)
		texts_2.append(text)
		if len(lines_2) == 2:
			cur_line_2 = concatenate_audioclips(lines_2)
			#cur_line_2.write_videofile("songs/Obama Shape Of You Lines/lines 2/"+" ".join(texts_2)+".mp4", temp_audiofile = "songs/Obama Shape Of You Lines/lines 2/"+" ".join(texts_2)+".wav", remove_temp = False)
			cur_line_2.write_audiofile("songs/Professional Shape Of You Lines/lines 2/" +" ".join(texts_2)+".wav")
			lines_2 = lines_2[1:]
			texts_2 = texts_2[1:]

		lines_3.append(final)
		texts_3.append(text)
		if len(lines_3) == 3:
			cur_line_3 = concatenate_audioclips(lines_3)
			#cur_line_3.write_videofile("songs/Obama Shape Of You Lines/lines 3/"+" ".join(texts_3)+".mp4", temp_audiofile = "songs/Obama Shape Of You Lines/lines 3/"+" ".join(texts_3)+".wav", remove_temp = False)
			cur_line_3.write_audiofile("songs/Professional Shape Of You Lines/lines 3/" +" ".join(texts_3)+".wav")
			lines_3 = lines_3[1:]
			texts_3 = texts_3[1:]
		lines_4.append(final)
		texts_4.append(text)
		if len(lines_4) == 4:
			cur_line_4 = concatenate_audioclips(lines_4)
			#cur_line_4.write_videofile("songs/Obama Shape Of You Lines/lines 4/"+" ".join(texts_4)+".mp4", temp_audiofile = "songs/Obama Shape Of You Lines/lines 4/"+" ".join(texts_4)+".wav", remove_temp = False)
			cur_line_4.write_audiofile("songs/Professional Shape Of You Lines/lines 4/" +" ".join(texts_4)+".wav")
			lines_4 = lines_4[1:]
			texts_4 = texts_4[1:]
		#final.write_videofile("songs/Obama Shape Of You Lines/lines 1/" +text+".mp4", temp_audiofile = "songs/Obama Shape Of You Lines/lines 1/" +text+".wav", remove_temp = False)
		final.write_audiofile("songs/Professional Shape Of You Lines/lines 1/" +text+".wav")
		print "##############################################################"
		if line_count == line_num:
			break
"""
#cut_professional_songs("Ed-Sheeran-Shape-Of-You-(Official-Video)(1).srt", "prof_musics/Shape of You by Ed Sheeran/Lead Vocal_modified.wav", 75, 80)

def make_song_lines(who_is_singing, subtitle_srt, music_str, line_start, line_num, error_time = 0, audio_volume = 0.1):
	times_texts = get_times_texts_srt(music_sub_dir+"/"+ subtitle_srt)
	audio = AudioFileClip(music_sub_dir+"/"+ music_str)
	audio = audio.subclip(error_time)
	
	audio = audio.fx(volumex, audio_volume)
	line_count = line_start

	songs_cuts = []
	texts_2 =[]
	lines_2 = []
	texts_3 =[]
	lines_3 = []
	texts_4 =[]
	lines_4 = []
	texts_5 =[]
	lines_5 = []

	wrote = 1

	for ind, ([t1, t2], text) in enumerate(times_texts):
		if ind < line_start:
			continue
		line_count += 1
		text = text_filter(text)
		#print "|"+text +"|"
		my_words = text.lower().split(" ")
		
		cuts_dirs = []
		found = []
		not_found = []
		for my_word in my_words:
			my_word = word_filter(my_word)
			print "Word = "+my_word
			cut_single = word_dir(my_word)
			if cut_single != None:
				cuts_dirs.append(cut_single)
				found.append(my_word)
			else:
				cuts_dirs.append("Not found")
				not_found.append(my_word)
		print "line_count: ", line_count
		print "text:",text
		print "found:", found
		print "not_found:",not_found
		

		# Now making video
		# Silent video
		silent = VideoFileClip("silent_video.mp4")
		empty_video = ColorClip((1280,720), (0,0,0), duration = 0.1)
		video_cuts = []
		dbs = check_db(cuts_dirs)
		print dbs
		for i, file in enumerate(cuts_dirs):
			print file
			if file == "Not found":
				#video_cuts.append(silent)
				video_cuts.append(empty_video)
			else:
				video = VideoFileClip(file)
				#video = video.fx(volumex, 1/dbs[i])
				video = video.resize((1280,720))
				video_cuts.append(video)

		final = concatenate_videoclips(video_cuts)
		"""
		lines_2.append(final)
		texts_2.append(text)
		if len(lines_2) == 2:
			cur_line_2 = concatenate_videoclips(lines_2)
			#cur_line_2.write_videofile("songs/Obama Shape Of You Lines/lines 2/"+" ".join(texts_2)+".mp4", temp_audiofile = "songs/Obama Shape Of You Lines/lines 2/"+" ".join(texts_2)+".wav", remove_temp = False)
			cur_line_2.audio.write_audiofile("songs/Obama Shape Of You Lines/lines 2/" +" ".join(texts_2)+".wav")
			lines_2 = lines_2[1:]
			texts_2 = texts_2[1:]

		lines_3.append(final)
		texts_3.append(text)
		if len(lines_3) == 3:
			cur_line_3 = concatenate_videoclips(lines_3)
			#cur_line_3.write_videofile("songs/Obama Shape Of You Lines/lines 3/"+" ".join(texts_3)+".mp4", temp_audiofile = "songs/Obama Shape Of You Lines/lines 3/"+" ".join(texts_3)+".wav", remove_temp = False)
			cur_line_3.audio.write_audiofile("songs/Obama Shape Of You Lines/lines 3/" +" ".join(texts_3)+".wav")
			lines_3 = lines_3[1:]
			texts_3 = texts_3[1:]
		lines_4.append(final)
		texts_4.append(text)
		if len(lines_4) == 4:
			cur_line_4 = concatenate_videoclips(lines_4)
			#cur_line_4.write_videofile("songs/Obama Shape Of You Lines/lines 4/"+" ".join(texts_4)+".mp4", temp_audiofile = "songs/Obama Shape Of You Lines/lines 4/"+" ".join(texts_4)+".wav", remove_temp = False)
			cur_line_4.audio.write_audiofile("songs/Obama Shape Of You Lines/lines 4/" +" ".join(texts_4)+".wav")
			lines_4 = lines_4[1:]
			texts_4 = texts_4[1:]
		#final.write_videofile("songs/Obama Shape Of You Lines/lines 1/" +text+".mp4", temp_audiofile = "songs/Obama Shape Of You Lines/lines 1/" +text+".wav", remove_temp = False)
		"""
		final.audio.write_audiofile("songs/Obama Am I Wrong/lines 1/" +str(wrote)+".wav")
		wrote += 1
		print "##############################################################"
		if line_count == line_num:
			break
	
#make_song_lines("Obama", "Nico-and-Vinz-Am-I-Wrong.srt","shape of you instrumental.mp4.wav", 9, 17)
def parser1(klm_path, lyrics_len):
	tree = ET.parse(klm_path)
	root = tree.getroot()
	word_dur_time = []
	for pg in root.findall("pg"):
		#print int(pg.get("id")[8:])
		if pg.get("id").startswith("lyrics") and int(pg.get("id")[7:]) < lyrics_len:
			for ln in pg.findall("ln"):
				lyrs = ln.findall("lyr")
				count = 0
				while count < len(lyrs):
					word = lyrs[count].get("s")
					dur = float(lyrs[count].get("d"))
					st = float(lyrs[count].get("t"))
					count += 1
					while not word.endswith(" "):
						word += lyrs[count].get("s")
						dur += float(lyrs[count].get("d"))
						count += 1
					word_dur_time.append((word, dur, st))
	return word_dur_time
def parser(klm_path, lyrics_start, lyrics_len):
	tree = ET.parse(klm_path)
	root = tree.getroot()
	word_dur_time = []
	for pg in root.findall("pg"):
		#print int(pg.get("id")[8:])
		if pg.get("id").startswith("lyrics") and int(pg.get("id")[7:]) >= lyrics_start and int(pg.get("id")[7:]) < lyrics_len :
			for ln in pg.findall("ln"):
				lyrs = ln.findall("lyr")
				count = 0
				while count < len(lyrs):
					word = lyrs[count].get("s")
					dur = float(lyrs[count].get("t")[lyrs[count].get("t").index(",")+1:])
					st = float(lyrs[count].get("t")[:lyrs[count].get("t").index(",")])
					count += 1
					while not word.endswith(" "):
						word += lyrs[count].get("s")
						dur += float(lyrs[count].get("t")[lyrs[count].get("t").index(",")+1:])
						count += 1
					word_dur_time.append((word, dur, st))
	return word_dur_time



def parser_for_sub(klm_path, lyrics_len):
	tree = ET.parse(klm_path)
	root = tree.getroot()
	text_dur_time = []
	for pg in root.findall("pg"):
		#print int(pg.get("id")[8:])
		if pg.get("id").startswith("lyrics") and int(pg.get("id")[7:]) < lyrics_len:

			

			for ln in pg.findall("ln"):
				lyrs = ln.findall("lyr")

				text = ""
				start_time = 0;
				end_time = 0;

				lyr_len = len(lyrs)


				count = 0
				while count < len(lyrs):
					word = lyrs[count].get("s")
					dur = float(lyrs[count].get("d"))
					st = float(lyrs[count].get("t"))

					if count == 0:
						start_time = st
					count += 1

					if count == lyr_len:
						end_time = st+dur
					text += word

				text_dur_time.append((text, start_time, end_time))

	return text_dur_time

def search_for_best_silent(blank_dur):

	list_dir = os.listdir(blank_dir)
	silents = sorted(list_dir) 
	count = 0
	flag = 0
	best_silent = ""
	cur_delta = 1000000
	for silent in silents:
		if silent.endswith("mp4"):
			delta_dur = abs(blank_dur - float(silent.replace(".mp4", "")))
			if cur_delta > delta_dur:
				cur_delta = delta_dur
				best_silent = silent
	video = VideoFileClip(blank_dir +"/"+best_silent, audio = False)
	print video.duration
	print blank_dur

	# if blank/vid.duration < 3 speed up, else add consequetively
	while not (blank_dur/video.duration < 3):
		video = concatenate_videoclips([video, video])
	video = video.fx(vfx.speedx,  video.duration/blank_dur)

	print "Video Dur", video.duration
	return video

def make_song_kml(song_name, kml_path, m4a_path, lyr_len):
	word_dur_time = parser1(kml_path, lyr_len)
	audio = AudioFileClip(m4a_path)
	audio = audio.fx(volumex, 0.1)
	cuts_dirs = []
	found = []
	not_found = []
	db_values = []
	for word, dur, time in word_dur_time:
		word = word.replace(" ", "")
		print "Word = "+word
		cut_single = word_dir(word.lower())
		if cut_single != None:
			cuts_dirs.append((cut_single, dur, time))
			# get db of the file

			song_file = AudioSegment.from_wav(cut_single.replace(".mp4",".wav"))
			#print "db", song_file.dBFS
			db_values.append(song_file.dBFS)

			found.append(word)
		else:
			cuts_dirs.append(("Not Found", dur, time))
			not_found.append(word)
			print "\""+word+"\" not found"
	print found
	print cuts_dirs

	av = numpy.mean(db_values)
	print "av", av

	blank_start = 0
	final_song_cuts = []
	if not os.path.exists("karaoke/temp_videos"):
		os.makedirs("karaoke/temp_videos",0777)
	for i, (cut, dur, time) in enumerate(cuts_dirs):
		blank = ColorClip((1280,720),(0,0,0), duration = time - blank_start)
		final_song_cuts.append(blank)
		if cut != "Not Found":
			video = VideoFileClip(cut, audio = False)
			#print dur
			#print "dur",video.duration
			#ratio = video.duration / dur
			print cut
			video = video.resize((1280,720))
			video_audio = AudioFileClip(cut.replace(".mp4",".wav"))
			tempo =  video_audio.duration / dur
			print "tempo = ", tempo
			if tempo > 2:
				tempo = 2
			elif tempo < 0.5:
				tempo = 0.5

			# change sound level to average
			db_video_audio = AudioSegment.from_wav(cut.replace(".mp4",".wav"))
			db_level = db_video_audio.dBFS
			coef = pow(10, ((av-db_level)/20))
			video_audio = video_audio.volumex(coef)
			print "atempo = ", tempo
			video_audio.write_audiofile("karaoke/temp_videos/test.wav", codec='pcm_s16le',ffmpeg_params=["-filter:a", "atempo=" +str(tempo)])
			after_audio = AudioSegment.from_wav("karaoke/temp_videos/test.wav")
			print "wrote"
			video = video.fx(vfx.speedx, video.duration / dur)
			
			#add audio to video file
			video = video.set_audio(AudioFileClip("karaoke/temp_videos/test.wav")) 
			
			#video.write_videofile("karaoke/temp_videos"+str(i)+".mp4", ffmpeg_params=["-atempo","2.0"], codec = 'libx264', audio_codec = 'acc', temp_audiofile = "karaoke/temp_videos"+str(i)+".m4a", remove_temp = True)
			#print "dur", video.duration
		else:
			video = ColorClip((1280,720),(0,0,0), duration = dur)
		final_song_cuts.append(video)
		#print time, dur, time+dur
		blank_start = time + dur
	final_song = concatenate_videoclips(final_song_cuts)
	final_song.audio = CompositeAudioClip([final_song.audio, audio]).set_duration(final_song.duration)
	final_song = final_song.fx(volumex, 1.5)
	final_song.write_videofile("karaoke/"+song_name+".mp4", codec='libx264', audio_codec='aac', temp_audiofile="karaoke/"+song_name+".m4a", remove_temp = True)

def find_longest(word, ind, word_lst):

	#print word
	#print ind
	#print word_lst
	cur_len = 0

	word_lst = [(word_filter(x).lower().replace(" ", ""), d, t) for x, d, t in word_lst]
	myword_index = ind

	orig_w_i = ind


	#word_lst = [word_filter(x).lower() for x in word_lst]

	my_word = word_filter(word)
	list_dir = os.listdir(sen_dir)
	sentences = sorted(list_dir) 
	count = 0
	flag = 0
	found_words = []
	final_cuts = []
	final_found_words = []
	cuts = []
	for sen in sentences:
		#rint "Searhing sentence #"+ str(count)
		if os.path.exists(sen_dir+"/"+sen+"/words"):
			words = os.listdir(sen_dir+"/"+sen+"/words")
			words_dir = sen_dir + "/"+sen+"/words"
			for word in words:
				if my_word == word and (my_word in sen.lower()):

					key_file = open(sen_dir+"/"+sen+"/keywords",'r')
					keywords = key_file.read()

					#print sen
					lst_keywords = ast.literal_eval(keywords)
					for el in lst_keywords:
						if '(' in el[0]:
							el[0] = el[0][:el[0].index('(')]
					for i, word_time in enumerate(lst_keywords):
						#print word_time[0]
						if my_word == word_time[0]:
							word_index = i
							cur_len += 1
							w,d,t  = word_lst[myword_index]
							cuts.append((words_dir+"/"+my_word+"/0.mp4",d,t))
							found_words.append(my_word)
							break
					
					orig_f_i = word_index
					while ((myword_index + 1) < len(word_lst)) and ((word_index + 1) < len(lst_keywords)) and word_lst[myword_index+1][0] == lst_keywords[word_index+1][0]:
						w,d,t  = word_lst[myword_index+1]
						cuts.append((words_dir+"/"+word_lst[myword_index+1][0]+"/0.mp4",d,t))
						found_words.append(word_lst[myword_index+1][0])
						cur_len += 1
						myword_index += 1
						word_index += 1

					"""
					word_index = orig_f_i
					myword_index = orig_w_i
					while ((myword_index - 1) >= 0) and ((word_index - 1) >= 0) and word_lst[myword_index-1] == lst_keywords[word_index-1][0]:
						cur_len += 1
						cuts = [words_dir+"/"+word_lst[myword_index-1]+"/0.mp4"] + cuts
						found_words = [word_lst[myword_index-1]] + found_words
						myword_index -= 1
						word_index -= 1
					"""
					#print cuts
					#print found_words
					
					if len(final_cuts) < len(cuts):
						final_cuts = cuts
						final_found_words = found_words
					cuts = []
					found_words = []
		count += 1
	#print final_cuts
	#print final_found_words

	#video = concatenate_videoclips([VideoFileClip(x) for x in final_cuts])
	#video.write_videofile("i love.mp4")
	return  (final_cuts, final_found_words)


def make_song_same_videos(song_name, kml_path, m4a_path, lyr_len):
	word_dur_time = parser1(kml_path, lyr_len)
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

		pair_index = word_dur_time.index((word, dur, time))
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
			print len(cut_singles)

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
	for i, (cut, dur, time) in enumerate(cuts_dirs):
		blank = ColorClip((1280,720),(0,0,0), duration = time - blank_start)
		final_song_cuts.append(blank)
		if cut != "Not Found":
			video = VideoFileClip(cut, audio = False)
			#print dur
			#print "dur",video.duration
			#ratio = video.duration / dur
			print cut
			video = video.resize((1280,720))
			video_audio = AudioFileClip(cut.replace(".mp4",".wav"))
			tempo =  video_audio.duration / dur
			print "tempo = ", tempo
			if tempo > 2:
				tempo = 2
			elif tempo < 0.5:
				tempo = 0.5

			# change sound level to average
			db_video_audio = AudioSegment.from_wav(cut.replace(".mp4",".wav"))
			db_level = db_video_audio.dBFS
			coef = pow(10, ((av-db_level)/20))
			video_audio = video_audio.volumex(coef)
			print "atempo = ", tempo
			video_audio.write_audiofile("karaoke/temp_videos/test.wav", codec='pcm_s16le',ffmpeg_params=["-filter:a", "atempo=" +str(tempo)])
			after_audio = AudioSegment.from_wav("karaoke/temp_videos/test.wav")
			print "wrote"
			video = video.fx(vfx.speedx, video.duration / dur)
			
			#add audio to video file
			video = video.set_audio(AudioFileClip("karaoke/temp_videos/test.wav")) 
			
			#video.write_videofile("karaoke/temp_videos"+str(i)+".mp4", ffmpeg_params=["-atempo","2.0"], codec = 'libx264', audio_codec = 'acc', temp_audiofile = "karaoke/temp_videos"+str(i)+".m4a", remove_temp = True)
			#print "dur", video.duration
		else:
			video = ColorClip((1280,720),(0,0,0), duration = dur)
		final_song_cuts.append(video)
		#print time, dur, time+dur
		blank_start = time + dur
	final_song = concatenate_videoclips(final_song_cuts)
	final_song.audio = CompositeAudioClip([final_song.audio, audio]).set_duration(final_song.duration)
	final_song = final_song.fx(volumex, 1.5)
	final_song.write_videofile("karaoke/"+song_name+".mp4", codec='libx264', audio_codec='aac', temp_audiofile="karaoke/"+song_name+".m4a", remove_temp = True)

	print "Number of words", len(word_dur_time)
	print "Total skips", total_skip

def find_lyr_of_word(time, text_sta_end):
	tdt_len = len(text_sta_end)
	for i, (text, st, en) in enumerate(text_sta_end):
		if st <= time and time <= en:
			if tdt_len == i +1:
				return text, ""
			else:
				return text, text_sta_end[i+1][0]

def make_song_kml_multiple_speed(song_name,lyr_len):

	kml_path = "karaoke/kml_audio/"+song_name.replace(" ","_").lower()+".kml"
	m4a_path = "karaoke/kml_audio/"+song_name.replace(" ","_").lower()+".m4a"
	lyr_start = 0

	word_dur_time = parser1(kml_path, lyr_len)
	text_dur_time = parser_for_sub(kml_path, lyr_len)

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

		pair_index = word_dur_time.index((word, dur, time))
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
	
	for i, ( cut, dur, time) in enumerate(cuts_dirs):



		#blank = ColorClip((1280,720),(255,255,255), duration = time - blank_start)
		#final_song_cuts.append(blank)
		
		# instead of blank, put silent obama videos

		blank_dur = time - blank_start
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
			video_audio = video_audio.volumex(coef)
			print "audurarion",video_audio.duration

			if video_audio.duration > 0.2:
				newaudio = video_audio.fx(afx.audio_fadein, 0.1).fx(afx.audio_fadeout, 0.1);
			else:				
				newaudio = video_audio.fx(afx.audio_fadein, 0.01).fx(afx.audio_fadeout, 0.01);

			tempo =  newaudio.duration / dur
			print "tempo = ", tempo

			if tempo > 2 or tempo < 0.5:
				print "making irregular speeding for tempo ", tempo
				speed_updown_irregular(newaudio, "karaoke/temp_videos/test.wav", tempo)
			else:
				newaudio.write_audiofile("karaoke/temp_videos/test.wav", codec='pcm_s16le',ffmpeg_params=["-filter:a", "atempo=" +str(tempo)])

			if tempo:
							pass			
			video = video.fx(vfx.speedx, video.duration / dur)
			#add audio to video file
			audio_of_video = AudioFileClip("karaoke/temp_videos/test.wav")
			#audio_of_video = (audio_of_video.fadein(0.1).fadeout(0.1))
			video = video.set_audio(audio_of_video)


			
			#video.write_videofile("karaoke/temp_videos"+str(i)+".mp4", ffmpeg_params=["-atempo","2.0"], codec = 'libx264', audio_codec = 'acc', temp_audiofile = "karaoke/temp_videos"+str(i)+".m4a", remove_temp = True)
			#print "dur", video.duration

		else:
			video = ColorClip((1280,720),(0,0,0), duration = dur)


		lyr_of_word = find_lyr_of_word(time, text_dur_time)

		word_text = TextClip(lyr_of_word[0], fontsize = 50, color = "white", bg_color = "black").set_pos(("center", 600)).set_duration(dur)
		video = CompositeVideoClip([video, word_text])
		final_song_cuts.append(video)


		#print time, dur, time+dur
		blank_start = time + dur
	final_song = concatenate_videoclips(final_song_cuts)

	#for text, dur, time in text_dur_time:
	#	word_text = TextClip(text, fontsize = 50, color = "white", bg_color = "black").set_pos((100,500)).set_start(time).set_duration(dur)
	#	final_song = CompositeVideoClip([final_song, word_text])
	#final_song.audio = CompositeAudioClip([final_song.audio, audio]).set_duration(final_song.duration)
	final_song = final_song.fx(volumex, 1.5)
	final_song.write_videofile("karaoke/"+song_name+"_No_Music.mp4", codec='libx264', audio_codec='aac', temp_audiofile="karaoke/"+song_name+".m4a", remove_temp = True)
	#final_song.audio.write_audiofile("karaoke/for_audio_prof/"+song_name+".wav")
def speed_updown_irregular(audio_file_clip, output_audio, tempo):

	audio = audio_file_clip
	n_count = 1
	min_temp = 0.5
	max_temp = 2

	if min_temp > tempo:
		cur_temp = tempo/min_temp
		print cur_temp, tempo
		audio.write_audiofile(output_audio, codec='pcm_s16le',ffmpeg_params=["-filter:a", "atempo=0.5"])
		audio = AudioFileClip(output_audio)
		while not cur_temp >= min_temp:
			n_count += 1
			cur_temp /= min_temp

			audio.write_audiofile(output_audio, codec='pcm_s16le',ffmpeg_params=["-filter:a", "atempo=0.5"])
			audio = AudioFileClip(output_audio)
			print (cur_temp, tempo)

		audio.write_audiofile(output_audio, codec='pcm_s16le',ffmpeg_params=["-filter:a", "atempo="+str(cur_temp)])
		audio = AudioFileClip(output_audio)
	elif max_temp < tempo:
		cur_temp = tempo/max_temp
		print cur_temp, max_temp

		audio.write_audiofile(output_audio, codec='pcm_s16le',ffmpeg_params=["-filter:a", "atempo=2"])
		#print cur_temp, max_temp

		audio = AudioFileClip(output_audio)
		#print cur_temp, max_temp
		while not cur_temp <= max_temp:
			n_count += 1
			cur_temp /= max_temp

			audio.write_audiofile(output_audio, codec='pcm_s16le',ffmpeg_params=["-filter:a", "atempo=2"])
			audio = AudioFileClip(output_audio)
			print (cur_temp, tempo)

		audio.write_audiofile(output_audio, codec='pcm_s16le',ffmpeg_params=["-filter:a", "atempo="+str(cur_temp)])


#print find_longest("i",1, [("where",1, 1),('i', 1, 1),( 'go', 1, 1)])
#make_song_kml_multiple_speed("Shape Of You", 5)
#print TextClip.list('font')


def make_song_tsm(song_name,lyr_len):

	kml_path = "karaoke/kml_audio/"+song_name.replace(" ","_").lower()+".kml"
	m4a_path = "karaoke/kml_audio/"+song_name.replace(" ","_").lower()+".m4a"
	lyr_start = 0

	word_dur_time = parser1(kml_path, lyr_len)
	text_dur_time = parser_for_sub(kml_path, lyr_len)

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

		pair_index = word_dur_time.index((word, dur, time))
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
	
	for i, ( cut, dur, time) in enumerate(cuts_dirs):



		#blank = ColorClip((1280,720),(255,255,255), duration = time - blank_start)
		#final_song_cuts.append(blank)
		
		# instead of blank, put silent obama videos

		blank_dur = time - blank_start
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

			if video_audio.duration > 0.2:
				new_audio = video_audio.fx(afx.audio_fadein, 0.1).fx(afx.audio_fadeout, 0.1);
			else:
				new_audio = video_audio.fx(afx.audio_fadein, 0.05).fx(afx.audio_fadeout, 0.05);


			new_audio.write_audiofile("karaoke/temp_videos/before_test.wav")

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


		lyr_of_word = find_lyr_of_word(time, text_dur_time)

		word_text = TextClip(lyr_of_word[0], fontsize = 50, color = "white", bg_color = "black").set_pos(("center", 600)).set_duration(dur)
		video = CompositeVideoClip([video, word_text])
		final_song_cuts.append(video)


		#print time, dur, time+dur
		blank_start = time + dur
	final_song = concatenate_videoclips(final_song_cuts)

	#for text, dur, time in text_dur_time:
	#	word_text = TextClip(text, fontsize = 50, color = "white", bg_color = "black").set_pos((100,500)).set_start(time).set_duration(dur)
	#	final_song = CompositeVideoClip([final_song, word_text])
	#final_song.audio = CompositeAudioClip([final_song.audio, audio]).set_duration(final_song.duration)
	final_song = final_song.fx(volumex, 1.5)
	final_song.write_videofile("karaoke/"+song_name+"_TSM.mp4", codec='libx264', audio_codec='aac', temp_audiofile="karaoke/"+song_name+".m4a", remove_temp = True)
	#final_song.audio.write_audiofile("karaoke/for_audio_prof/"+song_name+".wav")

#make_song_tsm("Shape Of You", 5)
