from __future__ import unicode_literals
import youtube_dl

ydl_opts = {
	'format': 'bestaudio/best',
	'writesubtitles': True

}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/channel/UCWSZJ4r3s5xk8zICXEveFpg'])
dr = "wh_obama"

