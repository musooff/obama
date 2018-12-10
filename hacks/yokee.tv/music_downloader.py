from bs4 import BeautifulSoup
import requests
import json
import urllib
import os

music_dir = "prof_musics/"

def get_music(url):

	song_name = ""
	singer = ""
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)
	for meta in soup.find_all('meta'):
		if meta.get("property") == "og:audio:title":
			song_name = meta.get("content")
		if meta.get("property") == "og:audio:artist":
			singer = meta.get("content")
	if not os.path.exists(music_dir + song_name + " by " + singer):
		os.makedirs(music_dir + song_name + " by " + singer, 0777)
	for link in soup.find_all('script'):
		str_link = str(link)
		if "mixer.init" in str_link:
			#print "#########################################"
			found = str_link[str_link.index("mixer.init"):]
			web_data = requests.get("http://www.karaoke-version.com"+found[found.index("(\'")+2:found.index( "\',")])
			j_data = json.loads(web_data.text)
			for track in j_data["tracks"]:
				print track["url"]
				print music_dir + song_name + " by " + singer + "/" + track["description"] + ".wav"
				testfile = urllib.URLopener()
				testfile.retrieve (track["url"], music_dir + song_name + " by " + singer + "/" + track["description"] + ".wav")
def download_kml(name, id):
	testfile = urllib.URLopener()
	testfile.retrieve("http://assets.yokee.cms.yokee.tv/KML/"+id+".kml",name+".kml")
	testfile.retrieve("http://assets.yokee.cms.yokee.tv/M4A/"+id+".m4a",name+".m4a")
#get_music("http://www.karaoke-version.com/custombackingtrack/ed-sheeran/shape-of-you.html")
download_kml("wake_me_up", "TEN44385")