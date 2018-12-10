from bs4 import BeautifulSoup
import requests
import json
import urllib
import os

def get_video(url):

	song_name = ""
	singer = ""
	r  = requests.get(url)
	data = r.text
	#print data
	soup = BeautifulSoup(data)
	for h1 in soup.find_all("h1"):
		if h1.get("itemprop") == "name":
			song_name = h1.string
	print song_name
	if not os.path.exists(song_name):
		os.makedirs(song_name, 0777)
	for link in soup.find_all('video'):
		if link.get("id") == "karaoke-video2":
			print link.find("source").get("src")
			url = str(link.find("source").get("src"))
			testfile = urllib.URLopener()
			testfile.retrieve (url, song_name + "/" + song_name + ".mp4")
get_video("http://www.karaoke-version.com/karaoke/ed-sheeran/shape-of-you.html")