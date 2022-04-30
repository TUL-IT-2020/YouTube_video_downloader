import random
from youtubesearchpython import *

from tools import *
from video import *
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
string = "Živě cz"
#string = "Česky s titulky"
#string = "Aleš Brichta (s textem)"
print(string)
query = string
#search= CustomSearch(string, VideoSortOrder.uploadDate, language = 'cs', region = 'CZ')
search = VideosSearch(query, language=language["code"])



index = 0
for video_json in get_videos(search, 1000):
    video = Video(video_json)
    print(str(index) + ' - ' + video.title + " - " + video.id)
    index += 1

    try:
        transcript = Subtitles(video.id, language["code"])
    except Exception:
        continue

    if len(list(transcript.get_languages())) != 0:
        print(transcript)

    if transcript.has_language(language["code"]):
        print("Mám: ",language['title'])
        print("Stahuji...")
        try:
            video.save(video.id)
            transcript.save(video.id)
        except DownloadError as e:
            print(e)
        #break
    


