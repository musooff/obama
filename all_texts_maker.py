import os
import obama
from hyphen import Hyphenator, dict_info
from hyphen.dictools import *
def make_text():
	subs = os.listdir("video_files")
	sorted_subs = sorted(subs)
	count = 0
	all_texts = open("all_texts_obama.txt","a")
	for sub in sorted_subs:
		if (count %2 == 0):
			print "Listening to the sub #" + str(count/2)
			times_texts = obama.get_times_texts("video_files"+'/'+sub)
			for time, text in times_texts:
				all_texts.write("<s> " + text + " </s>\n")
		count +=1
def syllables(word):
	u_word = word.decode('utf-8')
	h_en = Hyphenator('en_US')
	return [syl.encode('utf-8') for syl in h_en.syllables(u_word)]
#print syllables("random")
def word_filter(word):
	if word.endswith(","):
		word = word[:-1]
	if word.endswith("'"):
		word = word[:-1]
	while word.endswith("."):
		word = word.replace(".", "")
	return word
def make_syllables():
	subs = os.listdir("video_files")
	sorted_subs = sorted(subs)
	count = 0
	all_texts = open("all_syllables_obama.txt","a")
	for sub in sorted_subs:
		if (count %2 == 0):
			print "Listening to the sub #" + str(count/2)
			#print sub
			times_texts = obama.get_times_texts("video_files"+'/'+sub)
			for time, text in times_texts:
				#print text
				new_text = ""
				for word in text.split(' '):
					if len(word) < 4:
						if new_text == "":
							new_text += word
						else:
							new_text += " " + word
					else:
						sylls = syllables(word_filter(word))
						if len(sylls) > 0:
							#print sylls
							for syll in sylls:
								if new_text == "":
									new_text += syll
								else:
									new_text += " "+syll
				#print "****************"
				#print new_text
				all_texts.write("<s> " + new_text + " </s>\n")
		count +=1
def make_syll():
	with open("all_syllables_obama.txt","r") as r:
		sens = r.readlines()
	all_syls1 = open("just_syll_30000.txt","a")
	all_syls2 = open("just_syll_60000.txt","a")
	all_syls3 = open("just_syll_90000.txt","a")
	all_syls4 = open("just_syll_120000.txt","a")
	all_syls5 = open("just_syll_150000.txt","a")
	all_syls6 = open("just_syll_180000.txt","a")
	all_syls7 = open("just_syll_210000.txt","a")
	all_syls8 = open("just_syll_240000.txt","a")
	all_syls9 = open("just_syll_270000.txt","a")
	all_syls10 = open("just_syll_300000.txt","a")
	all_syls11 = open("just_syll_330000.txt","a")
	all_syls12 = open("just_syll_360000.txt","a")
	all_syls13 = open("just_syll_390000.txt","a")
	all_syls14 = open("just_syll_420000.txt","a")
	all_syls15 = open("just_syll_450000.txt","a")
	all_syls16 = open("just_syll_480000.txt","a")
	all_syls17 = open("just_syll_510000.txt","a")
	all_syls18 = open("just_syll_540000.txt","a")
	all_syls = [all_syls1,all_syls2,all_syls3,all_syls4,all_syls5,all_syls6,all_syls7,all_syls8,all_syls9, all_syls10, all_syls12, all_syls13, all_syls14 , all_syls15, all_syls16 , all_syls17, all_syls18]
	count = 0
	f_count = 0
	for sen in sens:
		sen = sen[4:sen.index("</s>")]
		syls = sen.split(" ")
		for syl in syls:
			if count % 30000 == 0 :
				print count, f_count
				f_count += 1
			if syl != "":
				all_syls[f_count].write(syl+"\n")
			count += 1
def rem():
	with open("dict.txt", "r") as d:
		trans = f.readlines()
	removed = list(set(trans))
	print len(trans)
	print len(removed)
rem()
#make_syll()

#make_syllables()
#print syllables("dramatically")
#print len(syllables("we"))