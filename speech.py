from pocketsphinx import AudioFile

import speech_recognition as sr
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate

import os

r = sr.Recognizer()

from pydub import AudioSegment
from pydub.silence import split_on_silence

import obama as obama
framerate = 100

def orig_code():
	# use the audio file as the audio source
	with sr.AudioFile("obama.wav") as source:
		audio_en = r.record(source) # read the entire audio file


	try:
		decoder = r.recognize_sphinx(audio_en, show_all=False)
		print ([(seg.word, seg.start_frame/framerate)for seg in decoder.seg()])
		print("Sphinx thinks you said: " + r.recognize_sphinx(audio_en))
	except sr.UnknownValueError:
	    print("Sphinx could not understand audio")
	except sr.RequestError as e:
		print("Sphinx error; {0}".format(e))

def check_dir(word, dir):

	list = os.listdir(dir + "/" + word + "SentenceFolder") # dir is your directory path
	number_files = len(list)

	for index, file in enumerate(list):
		print "Splitting keyword from sentence "+str(index) +"/"+str(number_files)
		with sr.AudioFile(dir + "/" + word+"SentenceFolder/"+file) as source:
			audio = r.record(source)
		try:

			#decoder = r.recognize_sphinx(audio, show_all=False)
			#print [(seg.word, seg.start_frame/framerate) for seg in decoder.seg()]
			print file+": 			" + r.recognize_sphinx(audio, show_all = False)
			decoder = r.recognize_sphinx(audio, show_all = True)
			#print "###############New File#############"
			for seg in decoder.seg():
				print (seg.word, seg.start_frame, seg.end_frame)
				found_word = seg.word
				if found_word.endswith(")"):
					index = found_word.index("(")
					found_word = found_word[:index]
				if found_word == word.lower():
					print file
					times = mill_to_sec(seg.start_frame), mill_to_sec(seg.end_frame)
					print seg.word, times
					obama.make_audio_cuts(dir + "/" + word + "SentenceFolder/" + file, [times], dir + "/" + word+"OnlyFolder")
		except sr.UnknownValueError:
			print("Sphinx could not understand audio")
		except sr.RequestError as e:
			print("Sphinx error; {0}".format(e))
def mill_to_sec(mill):
	return (mill * 10)/1000.0

#obama.sentence_with_word("speculations")
#check_dir("know")


def custom_speech():
    text = raw_input('Please, enter a text of your choice: ')
    words = text.split(' ')

    #words = [single.lower() for single in words]

    if not obama.is_there(text)[0]:
    	print "No occurences found for the word \"" + word + '\"'
    	return
    os.makedirs(text)

    print "Making Sentences"
    for word in words:
    	wrote = obama.sentence_with_word(word, text)
    	if wrote == 0:
    		print "No occurences found for the word \"" + word + '\"'
    		return
    print "Making Words"
    for word in words:
    	print "Word: " + word
    	check_dir(word, text)

    random_words(words, text)

def random_words(words, text):
    print "Randomly selecting words"
    nums = []
    for word in words:
		list = os.listdir(text + "/" + word + "OnlyFolder") # dir is your directory path
		number_files = len(list)
		rand = obama.randint(0,number_files-1)
		print word + ": " + str(rand)
		nums.append(rand)
    print "Concatinating words"
    final = obama.concatenate_audioclips([obama.AudioFileClip(text + "/" + word+ "OnlyFolder/" + str(nums[i]) + ".wav") for i, word in enumerate(words)])
    final.to_audiofile(text + "/" + text + ".wav")

custom_speech()
#random_words(['We', 'will', 'make', 'this', 'project', 'work'], "We will make this project work")
#random_words(['this','is', 'just' ,'test'], "this is just test")