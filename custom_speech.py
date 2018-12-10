from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips,  TextClip, CompositeVideoClip
import os

s_dir = "video_sentences"

def make_sentence(sayer, text):
	word_list = text.lower().split(" ")

	list_dir = os.listdir(s_dir)
	sentences = sorted(list_dir)
	wrote = 0
	cuts_dirs = []
	cuts = []
	not_found = []
	for single in word_list:
		print "Word = "+single
		count = 0
		flag = 0
		for sen in sentences:
			print "Searhing sentence #"+ str(count)
			words = os.listdir(s_dir+"/"+sen+"/words")
			words_dir = s_dir+"/"+sen+"/words"
			for word in words:
				if single == word and (single in sen.lower()):
					cut_single = words_dir+"/"+single+"/0.mp4"
					cuts_dirs.append(cut_single)
					flag = 1
					break
			count += 1
			if flag == 1:
				break

		if flag == 0:
			not_found.append(single)
	if not  len(not_found) == 0 :
		print "Keywords that are not found are: "+str(not_found)
		return
	video_cuts = []
	for file in cuts_dirs:
		print file
		video = VideoFileClip(file)
		video = video.resize((1280,720))
		video_cuts.append(video)
	final = concatenate_videoclips(video_cuts)

	word_text = TextClip(text, fontsize = 40, color = "white", bg_color = "black").set_pos( "bottom").set_duration(final.duration)
	final = CompositeVideoClip([final, word_text])
	if not os.path.exists(sayer + "* "+ text):
		os.makedirs(sayer + "* "+ text, 0777)
	final.write_videofile(sayer + "* "+ text+"/"+text + ".mp4", codec='libx264', audio_codec='aac', temp_audiofile=sayer + "* "+ text+"/"+text+".m4a", remove_temp=True)
	
#make_sentence("Look If you had One shot Or one opportunity To seize everything you ever wanted In one moment Would you do it Or just let it go")
make_sentence("Sorry Trump", "Stay with us and we will make it better and better")