from moviepy.editor import VideoFileClip,AudioFileClip, concatenate_videoclips
import moviepy.audio.fx.all as afx

def fade(wav_url):
	audio = AudioFileClip(wav_url)

	new_audio = audio.fx(afx.audio_fadein,0.1).fx(afx.audio_fadeout,0.1)
	new_audio.write_audiofile(wav_url+"_faded_0.1.wav")

def custom_conc(video_urls):
	final = concatenate_videoclips([VideoFileClip(url) for url in video_urls])
	final.write_videofile("conc.mp4");

custom_conc(["../video_sentences/If we make America the best place to do business, /words/best/0.mp4", "../video_sentences/If we make America the best place to do business, /words/place/0.mp4", "../video_sentences/If we make America the best place to do business, /words/to/0.mp4"])