import re # module for regular expressions
from collections import Counter
#from moviepy.editor import *
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate, concatenate_audioclips, TextClip, CompositeVideoClip
import os, sys

from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
import scipy.io.wavfile as wav

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

#from pylab import*
import pylab as pl

import numpy 

import wave
import contextlib

from random import randint

#from __future__ import unicode_literals
import youtube_dl

import my_mfcc as cus_mfcc



def convert_time(timestring):
    """ Converts a string into seconds """
    nums = map(float, re.findall(r'\d+', timestring))
    return 3600*nums[0] + 60*nums[1] + nums[2] + nums[3]/1000

def orig_code():
    with open("state.en.srt") as f:
        lines = f.readlines()


    times_texts = []
    current_times , current_text = None, ""
    for line in lines:
        times = re.findall("[0-9]*:[0-9]*:[0-9]*.[0-9]*", line)
        if times != []:
            current_times = map(convert_time, times)
        elif line == '\n':
            times_texts.append((current_times, current_text))
            current_times, current_text = None, ""
        elif current_times is not None:
            current_text = current_text + line.replace("\n"," ")

def get_times_texts(subtitle_str):

    with open(subtitle_str) as s:
        my_lines = s.readlines()
    my_times_texts = []

    my_current_times , my_current_text = None, ""
    for line in my_lines:
        my_times = re.findall("[0-9]*:[0-9]*:[0-9]*.[0-9]*", line)
        if my_times != []:
            my_current_times = map(convert_time, my_times)
        elif line == '\n':
            my_times_texts.append((my_current_times, my_current_text))
            my_current_times, my_current_text = None, ""
        elif my_current_times is not None:
            my_current_text = my_current_text + line.replace("\n"," ")
    return my_times_texts

#print (times_texts)

#whole_text = " ".join([text for (time, text) in times_texts])
#all_words = re.findall("\w+", whole_text)
#counter = Counter([w.lower() for w in all_words if len(w)>5])
#print (counter.most_common(10))

#cuts = [times for (times,text) in times_texts if (re.findall("Americans",text) != [])]

#print cuts
#video = VideoFileClip("state.mp4")
#audio = AudioFileClip("state.mp4")

def assemble_cuts(video_str, cuts, outputfile):
    """ Concatenate cuts and generate a video file. """
    video = VideoFileClip(video_str)
    #print cuts
    final = concatenate([video.subclip(start, end) for (start,end) in cuts])
    final.to_videofile(outputfile, codec='libx264', audio_codec='aac', temp_audiofile=outputfile+".m4a", remove_temp=True)

def assemble_audio_cuts(audio_str, cuts, outputfile):
    """ Concatenate cuts and generate a audio file. """
    audio = AudioFileClip(audio_str)

    final = concatenate_audioclips([audio.subclip(start, end) for (start,end) in cuts])
    final.to_audiofile(outputfile)

def make_audio_cuts(audio_str, cuts, outputfile):
    """ create single instance of audio file for every occurance"""

    #create new folder if not exists
    if not os.path.exists(outputfile):
        os.makedirs(outputfile, 0777)
        number_files = 0
    else:
        list = os.listdir(outputfile) # dir is your directory path
        number_files = len(list)

    audio = AudioFileClip(audio_str)
    #create every single audio file inside outputfile folder
    for index, (start,end) in enumerate(cuts):
        final = audio.subclip(start, end)
        final.to_audiofile(outputfile + "/" + str(index + number_files) + ".wav")


def make_video_cuts(video_str, cuts, outputfile):
    """ create single instance of video file for every occurance"""

    #create new folder if not exists
    if not os.path.exists(outputfile):
        os.makedirs(outputfile, 0777)
        number_files = 0
    else:
        list = os.listdir(outputfile) # dir is your directory path
        number_files = len(list)

    video = VideoFileClip(video_str)
    colors = TextClip.list('color')
    #create every single video file inside outputfile folder
    for index, (start,end) in enumerate(cuts):
        clip = video.subclip(start, end)
        randColor = randint(0,len(colors)-1)
        #text = TextClip(outputfile[outputfile.index("/")+1:outputfile.index("OnlyFolder")],  fontsize=70, color = colors[randColor]).set_pos("bottom").set_duration(end-start)
        #final = CompositeVideoClip([clip, text])
        final = clip
        final.write_videofile(outputfile + "/" + str(index + number_files) + ".mp4")


def find_word(word, padding=.05):
    """ Finds all 'exact' (t_start, t_end) for a word """
    matches = [re.search(word, text)
               for (t,text) in times_texts]
    return [(t1 + m.start()*(t2-t1)/len(text) - padding	,
             t1 + m.end()*(t2-t1)/len(text) + padding)
             for m,((t1,t2),text) in zip(matches, times_texts)
             if (m is not None)]

def my_find_word(word, subtitle_str, padding = 0.05):

    """ Finds all 'exact' (t_start, t_end) for a word """

    # except word
    word = " "+word+" "

    times_texts = get_times_texts(subtitle_str)
    matches = [re.search(word, text)
               for (t,text) in times_texts]


    maches_times_texts = []
    for index, (j_times, j_text) in enumerate(times_texts):
    	if matches[index] is not None:
	    	maches_times_texts.append((matches[index], j_times, j_text))
    
    return [(t1 + m.start()*(t2-t1)/len(text) - padding	,
             t1 + m.end()*(t2-t1)/len(text) + padding)
             for m,(t1,t2),text in maches_times_texts]

def my_find_sentence(word, subtitle_str):

    """ Finds all 'exact' (t_start, t_end) for a word """

    # except word
    word = " "+word+" "

    times_texts = get_times_texts(subtitle_str)
    matches = [re.search(word, text)
               for (t,text) in times_texts]


    maches_times_texts = []
    for index, (j_times, j_text) in enumerate(times_texts):
        if matches[index] is not None:
            maches_times_texts.append((matches[index], j_times, j_text))
    return maches_times_texts


#assemble_cuts("state.mp4", cuts, "people.mp4")

#print my_find_word("Americans")

#assemble_cuts("state.mp4",  my_find_word("people"), "people.mp4")

#assemble_audio_cuts(my_find_word("Americans"),"americans_audio.wav")

#make_audio_cuts("state.mp4", my_find_word("help", "state.en.srt"), "helpFolder")

def custom_mfcc(ind, fileinput):

    with contextlib.closing(wave.open(fileinput,'r')) as f: 
        frames = f.getnframes()
        rate = f.getframerate()
        length = frames / float(rate)    
        print "Length is " + str(length)

    	(rate,sig) = wav.read(fileinput)
    	mfcc_feat = mfcc(sig[:,0],rate, winlen = length)
    	plt.subplot(4,5,ind+1)
    	plt.plot(mfcc_feat[0])
        #plt.show()


def show_all_mfcc(folder_name):
	for index, file in enumerate(os.listdir(folder_name)):
		custom_mfcc(index, folder_name+"/"+file)
	plt.show()

#show_all_mfcc("americansFolder")

def mfcc_to_pca(ind, fileinput):
    
    print ind

    # length of fileinput
    with contextlib.closing(wave.open(fileinput,'r')) as f: 
        frames = f.getnframes()
        rate = f.getframerate()
        length = frames / float(rate)    
        print "Length is " + str(length)

        (rate,sig) = wav.read(fileinput)

        print numpy.shape(sig)

        mfcc_feat = mfcc(sig[:,0],rate, winlen = length, numcep = 50)
        #plt.subplot(4,5,ind+1)
        #plt.plot(mfcc_feat[0])

        #print(fbank_feat[1:3,:])
        print "Size of mfcc_feat equals to: " + str(numpy.shape(mfcc_feat))
        print "mfcc[0] " + str(mfcc_feat[0])
        return mfcc_feat[0]

        #return pairs
        result_list = []
        for x in xrange(0,13):
        	result_list.append([x,mfcc_feat[0][x]])
        print result_list
        #return result_list


def pca_all(folder_name):
    data_matrix = [ mfcc_to_pca(index, folder_name+"/"+file).tolist() for index, file in enumerate(os.listdir(folder_name))]
        
    print data_matrix
    #print "data_matrix : " + str(numpy.shape(data_matrix))
    myPCA = PCA(n_components=2)
    result_list = []

    transform = myPCA.fit_transform(numpy.array(data_matrix))
    
    data = numpy.array(transform)
    x,y = data.T
    #plt.scatter(x,y)
    #plt.show()
    return transform
#print pca_all("americansFolder")

def k_means(folder_name):
    data = pca_all(folder_name)
    print data
    X = numpy.array(data)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
    print kmeans.cluster_centers_

#k_means("americansFolder")

def plot_points(folder_name):
    data = pca_all(folder_name)

    for i, z in enumerate(data):
        pl.plot(z[0],z[1], "o")
        pl.text(z[0],z[1],str(i))
    pl.show()

#plot_points("americansFolder")

def speech(words, title):
    numbers = []
    time_cuts = []
    for x in xrange(0,len(words)):
        word_times = my_find_word(words[x])
        if len(word_times) == 0:
            print "No speech found for the word \"" + words[x]+"\""
            return
        time_cuts.append(word_times)
        #randomly select a cut
        numbers.append(randint(0,len(word_times)-1))
    #print time_cuts
    print numbers

    cuts = [time_cuts[i][numbers[i]] for i in xrange(0,len(words))]
    print cuts
    #cuts = [my_find_word(word)[n] for (word,n) in zip(words, numbers)]
    assemble_cuts("state.mp4",cuts, title + ".mp4")
#speech(["Americans", "are", "good","people"])
def any_speech():
    text = raw_input('Please, enter a text of your choice: ')
    words = text.split(' ')
    speech(words, text)

#any_speech()
        


def download_videos():
    ydl_opts = {'write-sub':'srt'}
    video_urls = []
    with open("videos.txt") as v:
        video_urls = v.readlines()
        for x in xrange(0,1):
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_urls[x]])
#download_videos()


def audio_cuts(word):
    list = os.listdir("video_files") # dir is your directory path
    subs_videos = sorted(list)

    count = 0
    for sub in subs_videos:
        if (count%2) == 0:
            print "Making cuts for video #"+str(count/2)
            make_audio_cuts("video_files/" + subs_videos[count + 1], my_find_word(word, "video_files/" + sub), word + "Folder")
        count += 1
#audio_cuts("some")

def sentence_with_word(word, dir):
    list = os.listdir("video_files") # dir is your directory path

    #create new folder if not exists
    if not os.path.exists(dir + "/" + word+"SentenceFolder"):
        os.makedirs(dir + "/" + word+"SentenceFolder", 0777)


    subs_videos = sorted(list)
    wrote = 0
    count = 0
    for sub in subs_videos:
        if (count%2) == 0:
            print "Searching cuts for video #"+str(count/2)
            #make_audio_cuts("video_files/" + subs_videos[count + 1], my_find_word(word, "video_files/" + sub), word + "Folder")
            for m, time, text in my_find_sentence(word, "video_files/" + sub):
                #print m.start(), m.end(), time, text
                if wrote < 5:
                    wrote += 1
                    assemble_audio_cuts("video_files/" + subs_videos[count + 1], [tuple(time)], dir + "/" + word + "SentenceFolder/" + text + ".wav")
        count += 1
    if wrote == 0:
        print "No occurences found for the word \"" + word + '\"'
        return wrote
#sentence_with_word("some")

def is_there_word(word):
    list = os.listdir("video_files") # dir is your directory path


    subs_videos = sorted(list)
    wrote = 0
    count = 0
    for sub in subs_videos:
        if (count%2) == 0:
            print "Searching cuts for video #"+str(count/2)
            #make_audio_cuts("video_files/" + subs_videos[count + 1], my_find_word(word, "video_files/" + sub), word + "Folder")
            for m, time, text in my_find_sentence(word, "video_files/" + sub):
                print m.start(), m.end(), time, text
                wrote += 1
        count += 1
    if wrote == 0:
        print "No occurences found for the word \"" + word + '\"'
        return wrote


def sentence_with_word_video(word, dir):
    list = os.listdir("video_files") # dir is your directory path

    #create new folder if not exists
    if not os.path.exists(dir + "/" + word+"SentenceFolder"):
        os.makedirs(dir + "/" + word+"SentenceFolder", 0777)


    subs_videos = sorted(list)
    wrote = 0
    count = 0
    for sub in subs_videos:
        if (count%2) == 0:
            print "Searching cuts for video #"+str(count/2)
            #make_audio_cuts("video_files/" + subs_videos[count + 1], my_find_word(word, "video_files/" + sub), word + "Folder")
            for m, time, text in my_find_sentence(word, "video_files/" + sub):
                #print m.start(), m.end(), time, text
                if wrote < 5:
                    wrote += 1
                    assemble_cuts("video_files/" + subs_videos[count + 1], [tuple(time)], dir + "/" + word + "SentenceFolder/" + text + ".mp4")
        count += 1
    if wrote == 0:
        print "No occurences found for the word \"" + word + '\"'
        return wrote
def is_there(text):
    words = text.split(' ')
    list = os.listdir("video_files") # dir is your directory path


    subs_videos = sorted(list)
    for word in words:
        wrote = is_there_word(word)
        if wrote == 0:
            print "No occurences found for the word \"" + word + '\"'
            return [False, word]
    return [True, "None"]
#print is_there("can you add text on top of the video either just the current word or the full sentences with the current word in a different color and try longer sentences")
#is_there("can")