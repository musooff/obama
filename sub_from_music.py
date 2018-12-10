from pocketsphinx import AudioFile
import speech_recognition as sr

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips,  TextClip, CompositeVideoClip
from moviepy.video.fx.all import even_size

from pocketsphinx import Pocketsphinx, get_model_path, get_data_path, Decoder

import os

r = sr.Recognizer()
import obama as obama

s_dir = "prof_musics"
def listen(song):
	with sr.AudioFile(s_dir + "/" + song + "/Lead Vocal.wav") as source:
		audio = r.record(source)
	try:
		decoder = r.recognize_sphinx(audio, show_all = True)

		keywords = []
		for seg in decoder.seg():
			print [seg.word, seg.start_frame, seg.end_frame]
			keywords.append([seg.word, seg.start_frame, seg.end_frame])
	except sr.UnknownValueError:
		print("Sphinx could not understand audio")
	except sr.RequestError as e:
		print("Sphinx error; {0}".format(e))
listen("All Of Me by John Legend")

def wav_converter(song_dir):
	audio = AudioFileClip(song_dir)
	audio.write_audiofile(song_dir)
#wav_converter("prof_musics/All Of Me by John Legend/Lead Vocal.wav")