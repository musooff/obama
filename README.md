# Obama singing any song
## 1st stage: Downloading Videos
\t First we need to download obama videos that that are available. All videos can be found in white house YouTube channel. For better visual looks we just listed Weekly Address of Obama and all the links of the videos can be found within videos.txt file. Additionally one can download all the videos of obama from their YouTube channel directly. Downloading videos can be done with youtube-dl library which has python extansion as well. The code to download videos is available within obama.py python file.
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
The given code download videos with their subtitles as srt file. We need subtitles for the next stage of our work. An example video and subtitle is "Weekly Address - Extending and Expanding..." within directory. 
## 2nd stage: Cutting videos by sentences

## 3rd stage: Speech Recognition
## 4th stage: Cutting words according to timestamp
## 5th stage: Downloading Lyrics and professional singer
## 6th stage: Making lyric lines with Obama words
## 7th stage: Cutting Professional singer by line
## 8th stage: Running matlab code to make two lines synched
## 9th stage: Concatenating all lines generated from matlab
