# Obama singing any song
## 1st stage: Downloading Videos
First we need to download obama videos that that are available. All videos can be found in white house YouTube channel. For better visual looks we just listed Weekly Address of Obama and all the links of the videos can be found within videos.txt file. Additionally one can download all the videos of obama from their YouTube channel directly. Downloading videos can be done with youtube-dl library which has python extansion as well. The code to download videos is available within obama.py python file.
``` python
def download_videos():
    ydl_opts = {'write-sub':'srt'}
    video_urls = []
    with open("videos.txt") as v:
        video_urls = v.readlines()
        for x in xrange(0,1):
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_urls[x]])
```
The given code download videos with their subtitles as srt file. We need subtitles for the next stage of our work. An example video and subtitle is *"Weekly Address - Extending and Expanding..."* within directory. 
## 2nd stage: Cutting videos by sentences
Now since we have videos and subtitles of those videos we can cut these videos according to sentences timings. To cut videos into sentence will be helpful for us to run speech recognition faster for the next stage. The codes to cut the sentences is given within listen.py python file.
``` python
def cut_videos(limit):
    list = os.listdir(v_dir) # dir is your directory path
    subs_videos = sorted(list)
    wrote = 0
    count = 0
    for sub in subs_videos:
        if (count%2) == 0 and count > 490:
            print "Cutting sentences for video #"+str(count/2)
            times_texts = obama.get_times_texts(v_dir+'/'+sub)
            if times_texts == None:
                count +=1
                continue
            video = VideoFileClip(v_dir + '/' + subs_videos[count+1])
            audio = AudioFileClip(v_dir + '/' + subs_videos[count+1])
            for times, text in times_texts:
                ...
```
This way we cut every Weekly Address into sentence and we name each sentence according to it's text. The code will generate two file: one video file and one audio file. Audio file is there just to make our audio processing faster. An example of sentences is *actually help working families get ahead*. Within that folder we have one video and one audio file of correspoding speech. We cut this sentences with MoviePy library of Python. Although moviepy library is great for video editing, it is not the best for audio editing. Therefore, resulting audio may have some glitches in the beginning or the end of the file. A better audio library is PyDub of Python which is both great and fast while working with audios. We didn't use PyDub at this stage, because we already had generated 20Gb of data with MoviePy and didn't want to regenerate with PyDub. If you want better audio quality results, its better to edit the code and cut audios with PyDub. For video cutting, one can use MoviePy and then add generated of audio of the file through PyDub to it.
## 3rd stage: Speech Recognition
After generating all the sentences we will use speech recognition to listen each sentence and generate timings of the each keyword. Here we use CMU Sphinx Speech Recognition. One can use Google or IBM speech recognition at this stage. The reason we use CMU Sphinx Speech Recognition is because its free and can be used offline. To listen we use the code inside cmu_listen.py.
``` python
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
                ...
```
These codes will generate a text file of timings of the each keyword within the sentence. We write those timings inside *keywords* file within the folder of the sentence. In this case we have *actually help working families get ahead/keywords*. The *keywords* is filled with the following structure
```
[['<s>', 0, 2], ['actually(2)', 3, 28], ['help', 29, 63], ['<sil>', 64, 78], ['working', 79, 111], ['families(2)', 112, 151], ['the', 152, 168], ['head', 169, 195], ['</s>', 196, 198]]
```
Each element of the list is a data structure for each keyword with first element is word itself, second element is starting time in milliseconds and the third is ending time in milliseconds. 
## 4th stage: Cutting words according to timestamp
At this stage we cut the sentences according to the word timings. We used again MoviePy to do so. This stage could have been omitted because we can simple use PyDub and since its really fast we don't need already generated words. But happens you use MoviePy for later stages we better cut the sentences accoding to the timings in the beginning. To do so we use codes within word_cutting.py file.
``` python
def cut_words():
	list_dir = os.listdir(s_dir) # dir is your directory path
	sentences = sorted(list_dir)
	wrote = 0
	count = 0
	for sen in sentences:
		print "Cutting sentence #" + str(count)
		if not os.path.exists(s_dir + "/" + sen + "/" + "words"):
			#print sen+"\n" + r.recognize_sphinx(audio, show_all = False)
			os.makedirs(s_dir + "/" + sen + "/" + "words")
			w_dir = s_dir + "/" + sen + "/" + "words"
			words_str = ""
			with open(s_dir + "/" + sen + "/" + "keywords", "r") as k:
				words_str = k.read()
				...
```
This function will cut the sentence according to the times within *keywords* file. It writes all video and audio files of the each word within *words* folder within the sentence folder. An example for the word in our case is *actually help working families get ahead. /words/actually/0.mp4* for the word \*actually\*. Within *actually* folder we will have audio and video files with chronological order if there are more than one appeareance of the word within that sentences.
## 5th stage: Downloading Lyrics and professional singer
Now we need to download lyrics and professional singer's singing. By lyrics we mean word-by-word lyrics of the song. It will be karaoke style in which we know staring time and end time of the each word. For this we will use karaoke-version.org. In fact karaoke-version.org is paid service and one should buy their singings and lyrics. What we do is track down how the system collects data from their server and download what we need from their server. For downloading lyrics its a bit tricky. For now I am downloading lyrics manually. One can write script on python to scrawl the website and download automatically. Automatisization can be done analogously. To download manually follow, these steps:
- Go to karafun.com (It's subsidery of karaoke-version.com)
- Open "Inspect Element" of your browser (works clearner on Firefox)
- Navigate to "Network" of Insect Element
- Search for the song you want at karafun.com
- There will be now new request at Network and that should have request url
- Go to that url and bam, you have lyrics of the song according to the word. (Note that url will be available for couple of minutes, after a while it will not be accessable)
- Save the lyrics to some xml file.
Following above steps we have *shape_of_you.xml* file that includes word by word lyrics of the Shape Of You by Ed Sheeran. The timing will look like
``` xml
<line id="3">
	<position x="128.50" width="383" y="120.90" height="52"/>
		<word id="1">
			<syllabe>
				<start>00:00:00,660</start>
				<end>00:00:00,820</end>
				<text>Come</text>
			</syllabe>
		</word>
		<word id="2">
			<syllabe>
				<start>00:00:00,820</start>
				<end>00:00:01,130</end>
				<text>on</text>
			</syllabe>
		</word>
		<word id="3">
			<syllabe>
				<start>00:00:01,130</start>
				<end>00:00:01,440</end>
				<text>be</text>
			</syllabe>
		</word>
		<word id="4">
			<syllabe>
				<start>00:00:01,440</start>
				<end>00:00:01,600</end>
				<text>my</text>
			</syllabe>
		</word>
		<word id="5">
			<syllabe>
				<start>00:00:01,600</start>
				<end>00:00:01,960</end>
				<text>ba</text>
			</syllabe>
			<syllabe>
				<start>00:00:01,960</start>
				<end>00:00:02,250</end>
				<text>by</text>
			</syllabe>
		</word>
</line>
```
In fact, the optained lyrics is syllabul by syllabul. So one can improve the system to make it syllabul by sullabul instead of current word by word singing. Syllabul by syllabul timing is actually our future work. It is actually required because, some of the words are not available at Obama Speeches so one should be able to generate any word from existing syllabul.
Downloading professional singer's singing is quite easy. Actually one should follow similar steps for lyrics, but I already wrote script to download it automatically. The code is given inside music_downloader.py
``` python
def get_music(url):
	song_name = ""
	singer = ""
	r  = requests.get(url)
	data = r.text
	soup = BeautifulSoup(data)
	for meta in soup.find_all('meta'):
		if meta.get("property") == "og:audio:title":
			...
```
Given url of the video we can download lead vocal singer and an example for the song of Shape Of You is *Lead Vocal.wav*
## 6th stage: Making lyric lines with Obama words
For making lyrics we will you PyDub library and the code is given inside song_maker.py
``` python
def split_obama_by_line_pydub(song_name, xml_path, lyr_len):

	line_start_end = xml_line_timing(xml_path, lyr_len)
	word_start_end = xml_timing(xml_path, lyr_len)

	cuts_dirs = []
	found = []
	not_found = []

	db_values = []
	skip = 0

	total_skip = 0

	
	for word, dur, time in word_start_end:

		if (skip > 0):

			print "SKIPPED"
			skip -=1
			continue
			...
```
Above code will concatenate each word of the lyrics according to the timings and also stretch up and down word so that it fits perfectly in whe lyrics. Actually there are two versions of doing this. One is without streting any word: Just add words and then add silence if there is some time remaining. The second is strech each word according to the lyrics.
All stretching and concatenation will be done by PyDub library. There is also dB changing step as well. That one is used to make all the dBs of the words same.
``` python
	...
	if end == line_end:
		line_videos.export("karaoke/split_parts/"+song_name+"/obama/"+str(line_count) + ".wav", format = "wav")
	...
```
At this stage we generate each line of the song "said" by obama. Example lines can be seen at *obama* folder.
## 7th stage: Cutting Professional singer by line
Since we have professsional singer's singing in one folder we should cut it according to the lyrics. Cutting will be done within song_maker.py file
``` python
def split_prof_by_line_pydub(song_name, xml_path, audio_src, lyr_len):
	line_start_end = xml_line_timing(xml_path, lyr_len)
	audio = AudioSegment.from_mp3(audio_src)

	os.makedirs("karaoke/split_parts/"+song_name + "/prof", 0777)
	line_count = 1;
	for line, start, end in line_start_end:
		start = convert_time(start)
		end = convert_time(end)
		print line, start, end
		part = audio[start*1000:end*1000]
		part.export("karaoke/split_parts/" +song_name + "/prof/"+str(line_count)+".wav", format = "wav")
		line_count += 1
```
Above code will generate each line of the professional singer within *prof* folder. Note that each number of generated file in 7th stage corresponds to that number of generated file in this stage.
## 8th stage: Running matlab code to make two lines synched
## 9th stage: Concatenating all lines generated from matlab
