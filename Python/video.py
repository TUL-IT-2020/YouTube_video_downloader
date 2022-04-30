from __future__ import unicode_literals
import youtube_dl

from tools import *

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192'
    }],
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'prefer_ffmpeg': True,
    'keepvideo': True,
    'progress_hooks': [my_hook],
}

folder = "../download"
path = get_path(folder)

ydl_opts = {
    'outtmpl': path+'/%(title)s.%(ext)s',
    'extractaudio': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}


class Video:
    url = "http://www.youtube.com/watch?v="
    
    def __init__(self, result):
        self.id = result['id']
        self.title = result['title']
        #self.keywords = result['keywords']
        #self.channel

    def __str__(self):
        return "# Video: \tTitle:" + self.title + "\tID:" + self.id

    def save(self, file=None):
        if file is not None:
            ydl_opts[outtmpl] = path+"/"+file+'s.%(ext)s',
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url + self.id])

if __name__ == '__main__':
    id = "bRUtDtMAVKQ"
    result = {
        'id': id,
        'title': "Aleš Brichta (s textem)"
    }
    print("Path:", path)
    video = Video(result)
    video.save()
