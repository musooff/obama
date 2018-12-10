from pocketsphinx import AudioFile
import speech_recognition as sr

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips,  TextClip, CompositeVideoClip
from moviepy.video.fx.all import even_size

from pocketsphinx import Pocketsphinx, get_model_path, get_data_path, Decoder

import os

r = sr.Recognizer()
import obama as obama

s_dir = "video_sentences_obama_new"
def listen():
	list_dir = os.listdir(s_dir) # dir is your directory path
	sentences = sorted(list_dir)
	wrote = 0
	count = 0
	for sen in sentences:
		print "Listening to sentence #" + str(count)
		with sr.AudioFile(s_dir + "/" + sen + "/" + sen+".wav") as source:
			audio = r.record(source)
		try:

			if not os.path.exists(s_dir + "/" + sen + "/" + "keywords"):
				#print sen+"\n" + r.recognize_sphinx(audio, show_all = False)
				decoder = r.recognize_sphinx(audio, show_all = True)

				keywords = []
				for seg in decoder.seg():
					print [seg.word, seg.start_frame, seg.end_frame]
					keywords.append([seg.word, seg.start_frame, seg.end_frame])
				f = open(s_dir + "/" + sen +"/keywords", 'w')
				f.write(str(keywords))
				f.close()
		except sr.UnknownValueError:
			print("Sphinx could not understand audio")
		except sr.RequestError as e:
			print("Sphinx error; {0}".format(e))
		count += 1
listen()
def pocket():

	ps = Pocketsphinx()


	language_directory = os.path.dirname(os.path.realpath(__file__))
	
	print language_directory

	acoustic_parameters_directory = os.path.join(language_directory, "acoustic-model")
	language_model_file = os.path.join(language_directory, "language-model.lm.bin")
	phoneme_dictionary_file = os.path.join(language_directory, "pronounciation-dictionary.dict")
    
	config = Decoder.default_config()
	config.set_string("-hmm", acoustic_parameters_directory)  # set the path of the hidden Markov model (HMM) parameter files
	config.set_string("-lm", language_model_file)
	config.set_string("-dict", phoneme_dictionary_file)

	decoder = Decoder(config)

	with sr.AudioFile(s_dir + "/a bad situation could become dramatically worse. /a bad situation could become dramatically worse. .wav") as source:
		audio_data = r.record(source)
	decoder.start_utt()
	decoder.process_raw(audio_data, False, True)
	decoder.end_utt()

	print decoder.hyp()

	ps.decode(
	    audio_file=os.path.join(s_dir, 'a bad situation could become dramatically worse. /a bad situation could become dramatically worse. .wav'),
	    buffer_size=2048,
	    no_search=False,
	    full_utt=False)
	print(ps.hypothesis()) # => ['<s>', '<sil>', 'go', 'forward', 'ten', 'meters', '</s>']
#pocket()