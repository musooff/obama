import librosa
import librosa.display
import matplotlib.pyplot as plt
from dtw import dtw
from numpy.linalg import norm



def test():
    video_urls = []
    with open("videos.txt") as v:
        video_urls = v.readlines()
    
    videos_str = "array = ("
    for url in video_urls:
    	videos_str += '\"' + url.replace('\n', '') + '\" '
    videos_str += ")"
    print videos_str
test()