import librosa
import librosa.display
import matplotlib.pyplot as plt
from dtw import dtw
from numpy.linalg import norm
import numpy as np

from sklearn.cluster import KMeans
import os
from random import randint
from collections import Counter


def single_audio(number, folderName):
	y_base, sr_base = librosa.load(folderName + '/'+str(number)+'.wav')

	list = os.listdir(folderName) # dir is your directory path
	number_files = len(list)

	result = []
	mfcc_base = librosa.feature.mfcc(y_base, sr_base)
	for x in xrange(0,number_files):
		if x != number:
			y_x, sr_x = librosa.load(folderName + '/'+str(x)+'.wav')
			mfcc_x = librosa.feature.mfcc(y_x,sr_x)
			dist, cost, path, idk= dtw(mfcc_base.T, mfcc_x.T, dist = lambda x, y: norm(x - y, ord=1))
			result.append([x, dist])
	return result

def show_points_for(number, folderName):
	data = single_audio(number, folderName)

	plt.title("Audios close to: " + str(number))
	for z in data:
		plt.plot(z[0],z[1], "o")
		plt.text(z[0],z[1],str(z[0]))
	plt.show()

#single_audio(0, 'americansFolder')

#show_points_for(3, 'americansFolder')

def all_pairs(folderName):
	result = []
	only_results = []
	count = 0

	list = os.listdir(folderName) # dir is your directory path
	number_files = len(list)

	print "Calculating MFCCs. Please wait..."
	for i in xrange(0,number_files):
		for j in xrange(i+1,number_files):
			if i != j:
				y_i, sr_i = librosa.load(folderName + '/'+str(i)+'.wav')
				y_j, sr_j = librosa.load(folderName + '/'+str(j)+'.wav')

				mfcc_i = librosa.feature.mfcc(y_i, sr_i)
				mfcc_j = librosa.feature.mfcc(y_j, sr_j)

				dist, cost, path, idk= dtw(mfcc_i.T, mfcc_j.T, dist = lambda x, y: norm(x - y, ord=1))

				only_results.append(dist)
				result.append([count, [i,j], dist])
				#result.append([count, dist])
				count += 1
				print "Distance between %d and %d is %f" % (i, j, dist)
	return result
	#return only_results



#all_pairs()

def show_all(folderName):
	data = all_pairs(folderName);
	plt.title("Audio distances")
	for z in data:
		#if z[2] < 150:
		plt.plot(z[0], z[2], "o")
		#plt.plot(z[0], z[2], str(z[0]))
		#print z
	plt.show()

#show_all('helpFolder')

def selectRandom(folderName):
	data = all_pairs(folderName)

	pos_results = []
	for z in data:
		if z[2] < 150:
			pos_results.append(z)

	number = randint(0,len(pos_results)-1)
	one_or_two = randint(0,1)

	# return random possible position that have distance less then 150
	return pos_results[number][1][one_or_two] 

#print selectRandom('peopleFolder')

def clustering():
	data = all_pairs()
	for i, x in enumerate(data):
		plt.plot(i, x, "o")
		print i, x
	plt.show()

#clustering()

def k_means(folderName):
	data = all_pairs(folderName)

	result = [[z[2], z[2]] for z in data]
	result = np.array(result)
	kmeans = KMeans(n_clusters = 8).fit(result)
	print kmeans.cluster_centers_
	print kmeans.labels_
	print Counter(kmeans.labels_)
	for x in result:
		plt.plot(x[0],x[1], "o")
	plt.show()

#string = raw_input("Enter a word for mfcc check out: ")
#k_means(string+"Folder")

def orig_code():


	#Loading audio files
	y1, sr1 = librosa.load('peopleFolder/0.wav') 
	y2, sr2 = librosa.load('peopleFolder/1.wav') 
	#Showing multiple plots using subplot
	plt.subplot(1, 2, 1) 
	mfcc1 = librosa.feature.mfcc(y1,sr1)   #Computing MFCC values
	librosa.display.specshow(mfcc1)

	plt.subplot(1, 2, 2)
	mfcc2 = librosa.feature.mfcc(y2, sr2)
	librosa.display.specshow(mfcc2)


	dist, cost, path, idk= dtw(mfcc1.T, mfcc2.T, dist = lambda x, y: norm(x - y, ord=1))
	print "The normalized distance between the two : " + str(dist)   # 0 for similar audios 


	plt.imshow(cost.T, origin='lower', cmap=plt.get_cmap('gray'), interpolation='nearest')
	plt.plot(path[0], path[1], 'w')   #creating plot for DTW

	#plt.show()  #To display the plots graphically

	#youtube-dl --write-srt --sub-lang en https://www.youtube.com/watch?v=2AFpAATHXtc

def is_silent(audio_file):
	y_silent, sr_silent = librosa.load('silent_almost.wav')
	y_a, sr_a = librosa.load(audio_file) 

	mfcc_silent = librosa.feature.mfcc(y_silent, sr_silent)
	mfcc_a = librosa.feature.mfcc(y_a, sr_a)
	dist, cost, path, idk= dtw(mfcc_silent.T, mfcc_a.T, dist = lambda x, y: norm(x - y, ord=1))
	if dist < 150:
		return True
	return False

def show_mfcc(folderName):
	list = os.listdir(folderName) # dir is your directory path
	number_files = len(list)

	mfccs = []

	print "Calculating MFCCs. Please wait..."
	for i in xrange(0,number_files):
		y_i, sr_i = librosa.load(folderName+"/"+str(i)+".wav")
		mfcc_i = librosa.feature.mfcc(y_i, sr_i)
		#print str(len(mfcc_i)) +","+ str(len(mfcc_i[0]))
		mfccs.append(mfcc_i)
		print mfcc_i

	return mfccs

#mfccs = show_mfcc("helpFolder") 

