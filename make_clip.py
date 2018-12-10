#!/usr/bin/env python
# -*- coding: utf-8 -*-

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips, concatenate_audioclips, TextClip, CompositeVideoClip, ColorClip, CompositeAudioClip
from moviepy.audio.fx.volumex import volumex

import os
import re # module for regular expressions


s_dir = "clips"
sen_dir = "video_sentences"

def word_filter(word):
	if word.endswith(","):
		word = word[:-1]
	if "’" in word:
		word = word.replace("’", "'")
	if word.endswith("'"):
		word = word[:-1]
	while word.endswith("."):
		word = word.replace(".", "")
	if word.endswith("?"):
		word = word[:-1]
	return word
def text_filter(text):
	if "I'm" in text:
		text = text.replace("I'm", "I am")
	if "I've" in text:
		text = text.replace("I've", "I have")
	return text

def convert_time(timestring):
    """ Converts a string into seconds """
    nums = map(float, re.findall(r'\d+', timestring))
    return (3600*nums[0] + 60*nums[1] + nums[2] + nums[3]/1000)

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
	return my_times_texts
#print get_times_texts_srt("songs/Eminem-Lose-Yourself.srt")

def character_cuts(subtitle_str, video_str):
	times_texts = get_times_texts_srt(s_dir+"/"+subtitle_str)
	video = VideoFileClip(s_dir + "/"+video_str)
	video_cuts = []
	blank_start = 0
	for [t1, t2], text in times_texts:
		if blank_start != t1:
			non_part = video.subclip(blank_start, t1)
			video_cuts.append(([non_part, False], [blank_start, t1], None))
		part = video.subclip(t1, t2)
		video_cuts.append(([part, True], [t1, t2], text))
		blank_start = t2
	return video_cuts
def make_clips(subtitle_str, video_str, line_num):
	cuts = character_cuts(subtitle_str, video_str)
	line_count = 0
	clips_cuts = []
	sound_cuts = []
	for [video, isPart], [t1, t2], text in cuts:
		if isPart:
			line_count += 1
			#text = text_filter(text)
			#print "|"+text +"|"
			my_words = text.lower().split(" ")
			list_dir = os.listdir(sen_dir)
			sentences = sorted(list_dir)
			cuts_dirs = []
			found = []
			not_found = []
			for my_word in my_words:
				#print "Word = "+my_word
				my_word = word_filter(my_word) 
				count = 0
				flag = 0
				for sen in sentences:
					#print "Searhing sentence #"+ str(count)
					words = os.listdir(sen_dir+"/"+sen+"/words")
					words_dir = sen_dir + "/"+sen+"/words"
					for word in words:
						if my_word == word and (my_word in sen):
							cut_single = words_dir+"/"+my_word+"/0.wav"
							cuts_dirs.append(cut_single)
							found.append(my_word)
							flag = 1
							break
					count += 1
					if flag == 1:
						break
				if flag == 0:
					#cuts_dirs.append("Not found")
					not_found.append(my_word)
			print "line_count: ", line_count
			print "text:",text
			print "found:", found
			print "not_found:",not_found

			# Now making audio
			audio_cuts = []
			for file in cuts_dirs:
				print file
				audio = AudioFileClip(file)
				audio_cuts.append(audio)

			final = concatenate_audioclips(audio_cuts)
			#final.write_audiofile(s_dir + "/Obama version of "+text + ".wav")
			# silent the video add the obama audio
			video = video.set_audio(final).set_duration(video.duration)
			word_text = TextClip(text, fontsize = 35, color = "white", bg_color = "black").set_pos("bottom").set_duration(video.duration)
			video_text = CompositeVideoClip([video, word_text])
			clips_cuts.append(video_text)
			#sound_cuts.append(final)
			print "##############################################################"
			if line_count == line_num:
				break
		else:
			clips_cuts.append(video)
	print clips_cuts
	#print audio_cuts
	final_video = concatenate_videoclips(clips_cuts)
	final_video.write_videofile(s_dir + "/Obama version of "+video_str + ".mp4", codec='libx264', audio_codec='aac', temp_audiofile=s_dir+"/Obama version of "+video_str +".m4a")
make_clips("now you see me.srt", "Now You See Me - Daniel Atlas Opening Scene-ZAiXJFe7us8.mp4", 100)
def convert_wav(video_str):
	video = AudioFileClip(video_str)
	video.write_audiofile(video_str + ".wav")