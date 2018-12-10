from pocketsphinx import AudioFile
import speech_recognition as sr

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips,  TextClip, CompositeVideoClip
from moviepy.video.fx.all import even_size

import os
import shutil
r = sr.Recognizer()
import obama as obama

old_dir = "video_sentences"
old_sens = os.listdir(old_dir)

v_dir = "wh_obama"
s_dir = "video_sentences"

def cut_videos(limit):
    list = os.listdir(v_dir) # dir is your directory path
    subs_videos = sorted(list)
    wrote = 0
    count = 0
    for sub in subs_videos:
        if (count%2) == 0 and count > 490:
            print "Cutting sentences for video #"+str(count/2)
            print sub
            #make_audio_cuts("video_files/" + subs_videos[count + 1], my_find_word(word, "video_files/" + sub), word + "Folder")
            times_texts = obama.get_times_texts(v_dir+'/'+sub)
            if times_texts == None:
                count +=1
                continue
            video = VideoFileClip(v_dir + '/' + subs_videos[count+1])
            audio = AudioFileClip(v_dir + '/' + subs_videos[count+1])
            for times, text in times_texts:
            	#print times, text
            	if times is not None:
            		if '/' in text:
            			text = text.replace('/', ',')
            		if ':' in text:
            			text = text.replace(':', ' , ')
            		while text.startswith('-'):
            			text = text[1:]
                    # if it exists in olds continue
                    	if text in old_sens:
                        	wrote +=1
                        	print "Sentence exists"
                       		continue
            		#create new folder if not exists
            		if not os.path.exists(s_dir + '/' + text):
            			os.makedirs(s_dir + '/' + text, 0777)
            		if not os.path.exists(s_dir + "/" +text + "/" + text + ".mp4"):
            			sen_video = video.subclip(times[0], times[1])
            			sen_video.write_videofile(s_dir + "/" + text + "/" + text + ".mp4")
            		if not os.path.exists(s_dir + "/" +text + "/" + text + ".wav"):
            			sen_audio = audio.subclip(times[0], times[1])
            			sen_audio.write_audiofile(s_dir + "/" + text + "/" + text + ".wav")
            		wrote +=1
            		print "wrote",wrote
            		print "count", count
        count += 1
#cut_videos(651)
def test_auto(limit):
    list = os.listdir(v_dir) # dir is your directory path
    subs_videos = sorted(list)
    wrote = 0
    count = 0
    for sub in subs_videos:
        if (count%2) == 0:
            print "Cutting sentences for video #"+str(count/2)
            #print sub
            #make_audio_cuts("video_files/" + subs_videos[count + 1], my_find_word(word, "video_files/" + sub), word + "Folder")
            times_texts = obama.get_times_texts(v_dir+'/'+sub)
            if times_texts == None:
                wrote+=1
                print sub
        count += 1
    print wrote
#test_auto(10)

def sub_converter(subtitle_str):
    lst = []
    with open(subtitle_str) as f:
        lst = f.readlines()
    str_subs = "".join(lst)
    while "-->" in str_subs:
        str_subs = str_subs.replace("-->","namedonam")
    while '<' in str_subs:
        substr = str_subs[str_subs.index("<"):str_subs.index(">")+1]
        print substr
        str_subs = str_subs.replace(substr, "")
    print str_subs
    while "namedonam" in str_subs:
        str_subs = str_subs.replace("namedonam","-->")
    while " align:start position:19%" in str_subs:
        str_subs = str_subs.replace(" align:start position:19%", "")
    str_subs = str_subs.replace("Style:\n::cue(c.colorCCCCCC) { color: rgb(204,204,204);\n }\n::cue(c.colorE5E5E5) { color: rgb(229,229,229);\n }\n##", "")
    with open("temp_sub.en.vtt",'w') as w:
        w.write(str_subs)
#sub_converter("wh_obama/Weekly Address - The Honor of Serving You as President-lbwlVwNWLzU.en.vtt")
#sub_converter("wh_obama/Weekly Address - This Labor Day, Lets Talk About the Minimum Wage-lflHi1N-PPU.en.vtt")
def remove_unwanted():
    list = os.listdir(v_dir) # dir is your directory path
    subs_videos = sorted(list)
    wrote = 0
    count = 0
    for sub in subs_videos:
        if (count %2) == 0:
            #print "Cutting sentences for video #"+str(count/2)
            if "It's mind-boggling" in sub:
                print sub
            #make_audio_cuts("video_files/" + subs_videos[count + 1], my_find_word(word, "video_files/" + sub), word + "Folder")
            times_texts = obama.get_times_texts(v_dir+'/'+sub)
            for times, text in times_texts:
                #print times, text
                if times is not None:
                    if '/' in text:
                        text = text.replace('/', ',')
                    if ':' in text:
                        text = text.replace(':', ' , ')
                    while text.startswith('-'):
                        text = text[1:]
                    #create new folder if not exists
                    if os.path.exists(s_dir + '/' + text):
                        #print s_dir+"/"+text
                        #shutil.rmtree(s_dir+"/"+text)
                        wrote +=1
        count += 1
    print wrote
#remove_unwanted()