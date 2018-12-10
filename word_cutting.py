
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips,  TextClip, CompositeVideoClip
import os
import ast
import numpy as np
import shutil

s_dir = "video_sentences_obama_new"
def mill_to_sec(mill):
	return (mill * 10)/1000.0
def cut_words():
	list_dir = os.listdir(s_dir) # dir is your directory path
	sentences = sorted(list_dir)
	wrote = 0
	count = 0
	for sen in sentences:
		print "Cutting sentence #" + str(count)
		if not os.path.exists(s_dir + "/" + sen + "/" + "words"):
			#print sen+"\n" + r.recognize_sphinx(audio, show_all = False)
			os.makedirs(s_dir + "/" + sen + "/" + "words")
			w_dir = s_dir + "/" + sen + "/" + "words"
			words_str = ""
			with open(s_dir + "/" + sen + "/" + "keywords", "r") as k:
				words_str = k.read()
			#print words_str
			words =  ast.literal_eval(words_str)

			audio = AudioFileClip(s_dir + "/" + sen + "/" + sen + ".wav")
			video = VideoFileClip(s_dir + "/" + sen + "/" + sen + ".mp4")
			for word in words:
				if (not (word[0] == '<s>')) and (not (word[0] == '<sil>')) and (not (word[0] == '</s>')):
					if word[0].endswith(")"):
						index = word[0].index("(")
						word[0] = word[0][:index]
					w_audio = audio.subclip(mill_to_sec(word[1]), mill_to_sec(word[2]))
					w_video = video.subclip(mill_to_sec(word[1]), mill_to_sec(word[2]))

					if not os.path.exists(w_dir + "/" + word[0]):
						os.makedirs(w_dir+ "/"+word[0], 0777)
						number_files = 0
					number_files = len(os.listdir(w_dir+"/"+word[0]))
					w_audio.write_audiofile(w_dir + "/" + word[0] + "/" + str(number_files) + ".wav")
					w_video.write_videofile(w_dir + "/" + word[0] + "/" + str(number_files) + ".mp4", codec='libx264', audio_codec='aac', temp_audiofile=w_dir+"/" +word[0]+".m4a", remove_temp=True)
		count += 1
#cut_words()
def cut_silent():
	list_dir = os.listdir(s_dir) # dir is your directory path
	sentences = sorted(list_dir)
	wrote = 0
	count = 0
	for sen in sentences:
		print "Cutting sentence #" + str(count)
		if not os.path.exists(s_dir + "/" + sen + "/" + "words"):
			#print sen+"\n" + r.recognize_sphinx(audio, show_all = False)
			os.makedirs(s_dir + "/" + sen + "/" + "words")
			w_dir = s_dir + "/" + sen + "/" + "words"
			words_str = ""
			with open(s_dir + "/" + sen + "/" + "keywords", "r") as k:
				words_str = k.read()
			#print words_str
			words =  ast.literal_eval(words_str)

			audio = AudioFileClip(s_dir + "/" + sen + "/" + sen + ".wav")
			video = VideoFileClip(s_dir + "/" + sen + "/" + sen + ".mp4")
			for word in words:
				if (not (word[0] == '<s>')) and (not (word[0] == '<sil>')) and (not (word[0] == '</s>')):
					if word[0].endswith(")"):
						index = word[0].index("(")
						word[0] = word[0][:index]
					w_audio = audio.subclip(mill_to_sec(word[1]), mill_to_sec(word[2]))
					w_video = video.subclip(mill_to_sec(word[1]), mill_to_sec(word[2]))

					if not os.path.exists(w_dir + "/" + word[0]):
						os.makedirs(w_dir+ "/"+word[0], 0777)
						number_files = 0
						number_files = len(os.listdir(w_dir+"/"+word[0]))
					w_audio.write_audiofile(w_dir + "/" + word[0] + "/" + str(number_files) + ".wav")
					w_video.write_videofile(w_dir + "/" + word[0] + "/" + str(number_files) + ".mp4", codec='libx264', audio_codec='aac', temp_audiofile=w_dir+"/" +word[0]+".m4a", remove_temp=True)
		count += 1
#cut_silent()
# there was error at 122 video_sentences/$7.25 an hour. /words/hour/0.mp4 128 379 629 880 #1173 #1191
def test_exist():
	list_dir = os.listdir(s_dir)
	sentences = sorted(list_dir)
	wrote = 0
	count = 0
	non_list = []
	for sen in sentences:
		print "Testing sentence #"+ str(count)
		words_dir = os.listdir(s_dir+"/"+sen+"/words")
		for word in words_dir:
			if os.path.isfile(s_dir+"/"+sen+"/words/"+word):
				non_list.append(sen)
				break
			items = os.listdir(s_dir+"/"+sen+"/words/"+word)
			if (len(items) < 2) or (len(items)%2 == 1):
				non_list.append(sen)
				break
		count +=1
	for found in non_list:
			#shutil.rmtree(s_dir+"/"+found+"/words")
			print found
	print len(non_list)
#test_exist()

def make_silent_words():
	list_dir = os.listdir(s_dir) # dir is your directory path
	sentences = sorted(list_dir)
	wrote = 0
	count = 0
	for sen in sentences:
		print "Cutting sentence #" + str(count)

		with open(s_dir + "/" + sen + "/" + "keywords", "r") as k:
			words_str = k.read()
		#print words_str
		words =  ast.literal_eval(words_str)

		audio = AudioFileClip(s_dir + "/" + sen + "/" + sen + ".wav")
		video = VideoFileClip(s_dir + "/" + sen + "/" + sen + ".mp4")
		for word in words:
			if (word[0] == '<sil>'):
				w_audio = audio.subclip(mill_to_sec(word[1]), mill_to_sec(word[2]))
				w_video = video.subclip(mill_to_sec(word[1]), mill_to_sec(word[2]))

				w_audio.write_audiofile("obama_silent_videos/" + str(wrote) + ".wav")
				w_video.write_videofile("obama_silent_videos/" + str(wrote) + ".mp4", codec='libx264', audio_codec='aac', temp_audiofile="obama_silent_videos/" + str(wrote) + ".m4a", remove_temp=True)
				wrote += 1
		count += 1
make_silent_words()