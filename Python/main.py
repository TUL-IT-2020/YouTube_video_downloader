import random
from youtubesearchpython import *

from tools import *
#from video import *
from subtitles import *


def get_n_random(n, array):
    entrys = []
    for i in range(n):
        entrys.append(random.choice(array))
    return entrys


def get_videos(search, n=100):
    i = 0
    end = False
    while not end:
        for video in search.result()['result']:
            yield video
            i += 1
            if i > n:
                end = True
                break
        search.next()
        

"""
"title" : ,
"code" : ,
"file_name" :
"""
languages = {
    "CS": {
        "title": "Czech",
        "code": "cs",
        "file_name": "czech.txt"
    },
    "EN": {
        "title": "English",
        "code": "en",
        "file_name": "engmix.txt"
    }
}


lang_folder = "../dict"
language = languages["CS"]

N = 3
path = get_path(lang_folder, language["file_name"])
dictionary = read_file(path)
words = get_n_random(N, dictionary)
string = " ".join(words)
string = "Karel Čapek"
#string = "Česky s titulky"
string = "Aleš Brichta (s textem)"
print(string)
# + "&" + "sp=EgIoAQ%253D%253D"
query = string
#search= CustomSearch(string, VideoSortOrder.uploadDate, language = 'cs', region = 'CZ')
search = VideosSearch(query, language=language["code"])
#search = VideosSearch(query, limit=100, language=language["code"])
# mode = ResultMode.dict


index = 0
for video_json in get_videos(search, 1000):
    video = Video(video_json)
    url = Video.url+video.id
    transcripts = Transcript.get(url)

    print(str(index) + ' - ' + video.title + " - " + video.id)
    if len(transcripts["languages"]) != 0:
        
        print(transcript_get_languages(transcripts["languages"]))

    if transcript_has_language(transcripts["languages"], language):
        print("Mám: ",language['title'])
        print("Stahuji...")
        video.save("empty")
        break
    
    index += 1

"""
import urllib.request
link = "https://www.youtube.com/watch?v="
video = "fbjFofNGHks"
url = link+video
print(url)


opener = urllib.request.FancyURLopener({})
f = opener.open(url)
content = f.read()

print(content)
"""
