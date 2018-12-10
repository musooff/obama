from pocketsphinx import AudioFile
import speech_recognition as sr
import os

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips,  TextClip, CompositeVideoClip,CompositeAudioClip
from moviepy.audio.fx.volumex import volumex
import moviepy.video.fx.all as vfx

#from vid_utils import Video, concatenate_videos

r = sr.Recognizer()

def make_timestamp(audio_str):
	# use the audio file as the audio source
	with sr.AudioFile(audio_str) as source:
		audio_en = r.record(source) # read the entire audio file
	try:
		decoder = r.recognize_sphinx(audio_en, show_all=False)
		#print ([(seg.word, seg.start_frame, seg.end_frame)for seg in decoder.seg()])
		print("Sphinx thinks you said: " + r.recognize_sphinx(audio_en))
	except sr.UnknownValueError:
	    print("Sphinx could not understand audio")
	except sr.RequestError as e:
		print("Sphinx error; {0}".format(e))

#make_timestamp("chorus 2 shape of you.wav")

def cut_part(start, end, name):
	shape = AudioFileClip("shape of you instrumental.mp4")
	final = shape.subclip(start, end)
	final.write_audiofile(name + "shape of you.wav")
#cut_part(51,60.906, "chorus instrumental ")

def convert_wav(video_str):
	video = AudioFileClip(video_str)
	video.write_audiofile(video_str + ".wav")
#convert_wav("songs/Lose Yourself (Karaoke)-UGbejyDDGPc.mkv")

def some():
	part1 = "I'm in love with the shape of you/I'm in love with the shape of you.mp4"
	part2 = "we push and pull like a magnet do/we push and pull like a magnet do.mp4"
	part3 = "although my heart is falling too/although my heart is falling too.mp4"
	part4 = "I'm in love with your body/I'm in love with your body.mp4"


	p1 = "Let it go/Let it go.mp4"
	p2 = "Let it go/Let it go.mp4"
	p3 = "can't hold it back anymore/can't hold it back anymore.mp4"
	p4 = "Let it go/Let it go.mp4"
	p5 = "Let it go/Let it go.mp4"
	p6 = "turn away and slam the door/turn away and slam the door.mp4"

	ts = [[0.314, 1.950], [1.950, 3.613], [3.813, 7.112], [7.304, 8.909], [8.909, 10.603], [10.805, 14.804]]

	audio_background = AudioFileClip("chorus instrumental shape of you.wav")
	audio_background = audio_background.fx(volumex, 0.03)
	print audio_background.duration
	parts = [part1, part2, part3, part4]
	ps =  [p1, p2, p3, p4,p5, p6]
	times = [[0.314,2.413], [2.615, 4.814], [5.006, 7.305], [7.507, 9.906]]
	# diff = 2.099           2.199            2.299          2.399
	# sile =           0.202           1.039            0.202
	print "\n"
	cuts = []
	for x in xrange(0,4):
		part = VideoFileClip(parts[x])
		print "video durations"
		print part.duration
		#part = part.speedx(part.duration/(times[x][1]-times[x][0]))
		#part = part.fx(vfx.speedx, (times[x][1]-times[x][0])/part.duration)
		print part.duration
		cuts.append(part)
		#part.write_videofile(str(x)+".mp4")

		# add silent video in between
		if x<3:
			silent = VideoFileClip("silent_video.mp4")
			print "silent"
			print silent.duration
			silent = silent.speedx(silent.duration/(times[x+1][0]-times[x][1]))
			print silent.duration
			cuts.append(silent)
	final = concatenate_videoclips(cuts)
	#final.set_audio(audio)

	final.audio = CompositeAudioClip([final.audio, audio_background]).set_duration(final.duration)
	print final.duration
	final.write_videofile("shape chorus obama normal speed with audio.mp4")
#some()

def some_2():
	part1 = "I'm in love with the shape of you/I'm in love with the shape of you.mp4"
	part2 = "we push and pull like a magnet do/we push and pull like a magnet do.mp4"
	part3 = "although my heart is falling too/although my heart is falling too.mp4"
	part4 = "I'm in love with your body/I'm in love with your body.mp4"

	audio_background = AudioFileClip("chorus instrumental shape of you.wav")
	audio_background = audio_background.fx(volumex, 0.3)
	print audio_background.duration
	parts = [part1, part2, part3, part4]
	times = [(0.314,2.413), (2.615, 4.814), (5.006, 7.305), (7.507, 8.906)]

	print "\n"
	cuts = []
	for x in xrange(0,4):
		part = Video(speed = 2.0, path = parts[x])
		#print part.duration
		#part = part.speedx((times[x][1]-times[x][0])/part.duration)
		#print part.duration
		cuts.append(part)
		#part.write_videofile(str(x)+".mp4")
	final = concatenate_videos(videos=cuts, output_file = "test speed.mp4")
	#final.set_audio(audio)

	#final.audio = CompositeAudioClip([final.audio, audio_background]).set_duration(final.duration)
	#print final.duration
	#final.write_videofile("shape chorus obama.mp4")
#some_2()

def body():
	videofile =VideoFileClip( "body/bodySentenceFolder/police use body cameras and collect data on the .mp4")
	colors = TextClip.list('color')
	text = TextClip("body",  fontsize=70, color = colors[100]).set_pos("bottom").set_duration(0.25)
	final = CompositeVideoClip([videofile.subclip(1.05, 1.3),text])
	final.write_videofile("test.mp4")

def speed_test():
	part1 = "I'm in love with the shape of you/I'm in love with the shape of you.mp4"
	audio = AudioFileClip(part1)

	#video = video.speedx(factor = 2)
	audio.write_audiofile("speed_test.mp3", ffmpeg_params=["-filter:a", "atempo=2.0"])

	#song = AudioFileClip("shape of you instrumental.mp4")
	#print song.duration

	video = VideoFileClip(part1)
	video = video.speedx(factor = 2.0)
	video.write_videofile("speed_test.mp4")

#speed_test()

def silent_video():
	part1 = "I know everything is done by now/byOnlyFolder/0.mp4"
	video = VideoFileClip(part1, audio = False)
	video.write_videofile("silent_video.mp4")
#silent_video()

def video_speed_test():
	video = VideoFileClip("shape chorus obama.mp4")
	print video.duration
	video = video.speedx(factor = 2)
	print video.duration
#video_speed_test()