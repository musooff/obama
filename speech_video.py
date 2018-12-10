from pocketsphinx import AudioFile

import speech_recognition as sr
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips,  TextClip, CompositeVideoClip
from moviepy.video.fx.all import even_size

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
		if file.endswith(".wav"):
			pass
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
						obama.make_video_cuts(dir + "/" + word + "SentenceFolder/" + file.replace(".wav",".mp4"), [times], dir + "/" + word+"OnlyFolder")
			except sr.UnknownValueError:
				print("Sphinx could not understand audio")
			except sr.RequestError as e:
				print("Sphinx error; {0}".format(e))
def mill_to_sec(mill):
	return (mill * 10)/1000.0

#obama.sentence_with_word("speculations")
#check_dir("know")


def custom_speech(text):
    #text = raw_input('Please, enter a text of your choice: ')
    #text = text.lower()
    words = text.split(' ')

    #words = [single.lower() for single in words]

    search = obama.is_there(text)
    if not search[0]:
    	print "No occurences found for the word \"" + search[1] + '\"'
    	return
    os.makedirs(text)

    print "Making Sentences"
    for word in words:
    	wrote = obama.sentence_with_word_video(word, text)
    	wrote = obama.sentence_with_word(word, text)
    print "Making Words"
    for word in words:
    	print "Word: " + word
    	check_dir(word, text)

    text_overlay( text)

def random_words(words, text):
    print "Randomly selecting words"
    nums = []
    available_words = []
    for word in words:
	    if os.path.exists(text + "/" + word+"OnlyFolder"):
			list = os.listdir(text + "/" + word + "OnlyFolder") # dir is your directory path
			number_files = len(list)
			rand = obama.randint(0,number_files-1)
			print word + ": " + str(rand)
			nums.append(rand)
			available_words.append(word)
	    else:
			print "Coul'd not find word \"" + word + '\"'
    print "Concatinating words"
    video_files = [VideoFileClip(text + "/" + word+ "OnlyFolder/" + str(nums[i]) + ".mp4") for i, word in enumerate(available_words)]
    final = concatenate_videoclips([video_file.resize((1280,720)) for video_file in video_files])
    #final = even_size(final)
    #final.resize(1280,720)
    final.write_videofile(text + "/" + text + ".mp4")

#custom_speech()
#random_words(['can' ,'you', 'add', 'on', 'top' ,'of', 'the' ,'video', 'either' ,'just' ,'the' ,'current' ,'word', 'or', 'the', 'full' ,'sentences', 'with' ,'the' ,'current' ,'word', 'in', 'a' ,'different' ,'color','and', 'try', 'longer', 'sentences' ], "can you add on top of the video either just the current word or the full sentences with the current word in a different color and try longer sentences")
#random_words(['it', 'should', 'work'], "it should work")

#random_words(['I', 'am', 'trying', 'different', 'approach'],"I am trying different approach")
def add_sub():
	print "hh"

#print TextClip.list('color')
#random_words(['final' ,'last' ,'test','for' ,'the', 'color'], "final last test for the color")
#random_words(['I', 'know', 'everything' ,'is', 'done', 'by' ,'now'], "I know everything is done by now")

#random_words(['I\'m', 'in', 'love', 'with', 'your', 'body'], "I'm in love with your body")

def text_overlay(text):
    words = text.split(' ')
    nums = []
    available_words = []

    textclips = []
    back_texts = []
    videoclips = []

    written_text = ""
    duration = 0

    for word in words:
	    if os.path.exists(text + "/" + word+"OnlyFolder"):
			list = os.listdir(text + "/" + word + "OnlyFolder") # dir is your directory path
			number_files = len(list)
			rand = obama.randint(0,number_files-1)
			print word + ": " + str(rand)
			nums.append(rand)
			available_words.append(word)

			video = VideoFileClip(text + "/" + word+ "OnlyFolder/" + str(rand) + ".mp4")
			videoclips.append(video)
			written_text += (word + " ")
			word_text = TextClip(written_text, fontsize = 50, color = "purple", bg_color = "black").set_pos((100,500)).set_duration(video.duration)
			textclips.append(word_text)
			back_texts.append(TextClip(text, fontsize = 50, color = "white", bg_color = "black").set_pos((100,500)).set_duration(video.duration))
			duration += video.duration
	    else:
			print "Coul'd not find word \"" + word + '\"'


	#main_text = TextClip(text, fontsize = 70, color = "white", bg_color = "black").set_pos("left").set_duration(duration)
    print "Concatinating words"
    videos_texts = []
    for i, v in enumerate(videoclips):
    	print i
    	video_text = CompositeVideoClip([v.resize((1280, 720)), back_texts[i], textclips[i]])
    	videos_texts.append(video_text)

    final = concatenate_videoclips(videos_texts)
    #final = concatenate_videoclips([video_file.resize((1280,720)) for video_file in video_files])
    #final = even_size(final)
    #final.resize(1280,720)
    final.write_videofile(text + "/" + text + ".mp4")
#text_overlay(['I\'m', 'in', 'love', 'with', 'the' ,'shape', 'of', 'you'], "I\'m in love with the shape of you")
#text_overlay(['we', 'push' ,'and' ,'pull' ,'like' ,'a', 'magnet', 'do'],"we push and pull like a magnet do")
#text_overlay(['although' ,'my', 'heart', 'is', 'falling', 'too'], "although my heart is falling too")
#custom_speech("let")
custom_speech("We are done for current bad performance")