from __future__ import unicode_literals
import yt_dlp
import json

from tools import *

class MyLogger(object):
    def debug(self, msg):
        #print(msg)
        pass

    def warning(self, msg):
        print(msg)
        pass

    def error(self, msg):
        print(msg)

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

folder = "../download"
path = get_path(folder)

ydl_opts = {
    'outtmpl': path+'/%(title)s.%(ext)s',
    'format': 'bestaudio/best',
    'extractaudio': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192'
    }],
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'prefer_ffmpeg': True,
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}


class Video:
    url = "http://www.youtube.com/watch?v="
    
    def __init__(self, result, language=None):
        self.id = result['id']
        self.language = language
        self.title = result['title']
        self.duration = result['duration']
        #self.keywords = result['keywords']
        self.channel_id = result['channel']['id']
        self.channel_name = result['channel']['name']

    def __str__(self):
        return (
            colors.Green + "Video: " + colors.NC +
            "\n - Title: " + colors.Blue + self.title + colors.NC +
            "\n - Duration: " + colors.Blue + self.duration + colors.NC +
            "\n - ID: " + colors.Blue + self.id + colors.NC
        )

    def to_json(self):
        return [
            self.id,
            {
                'title' : self.title,
                'duration' : self.duration,
                'channel_id' : self.channel_id,
                'channel_name' : self.channel_name,
            }
        ]

    def save(self, file_name=None):
        if file_name is not None:
            file = path + "/" + self.language + "/" + file_name+'.%(ext)s'
            ydl_opts["outtmpl"] = file
            #print(file)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url + self.id])

if __name__ == '__main__':
    id = "bRUtDtMAVKQ"
    result = {
        'id': id,
        'title': "Aleš Brichta (s textem)",
        "duration": "4:17",
        "channel": {
            "name": "JohnyZumongar",
            "id": "UCzA_PM8EwCPAxK8DWN_2_1Q",
        }
    }
    print("Path:", path)
    video = Video(result)
    print(video)
    print(video.to_json())
    #video.save()
    #video.save(id)

"""
ydl_opts = {
    'outtmpl': path+'/%(title)s.%(ext)s',
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
"""
