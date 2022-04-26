import os
import random
from youtubesearchpython import *


def get_path(directory, file_name):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), directory, file_name))


def read_file(path):
    try:
        file = open(path, "r", encoding='utf-8')
    except:
        print("ERROR while tring to read file:", path)
        return None
    else:
        text = file.read().splitlines()
        file.close()
        return text


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
        

def transcript_has_language(transcripts, language):
    for transcript in transcripts:
        if transcript['title'] == language['title']:
            return True
    return False

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
"""
"title" : ,
"code" : ,
"file_name" :

"""



lang_folder = "../dict"
language = languages["CS"]

N = 3
path = get_path(lang_folder, language["file_name"])
dictionary = read_file(path)
words = get_n_random(N, dictionary)
string = " ".join(words)
string = "Karel Čapek"
print(string)
# + "&" + "sp=EgIoAQ%253D%253D"
query = string
#search= CustomSearch(string, VideoSortOrder.uploadDate, language = 'cs', region = 'CZ')
search = VideosSearch(query, language=language["code"])
#search = VideosSearch(query, limit=100, language=language["code"])
# mode = ResultMode.dict
index = 0

"""
while len(search.result()['result']) != 0:
    for video in search.result()['result']:
        
        url = "https://www.youtube.com/watch?v="+video['id']
        transcript = Transcript.get(url)

        print(str(index) + ' - ' + video['title'] + " - " + video['id'])
        if len(transcript["languages"]) != 0:
            
            print(transcript["languages"])
        index += 1
    search.next()
"""

for video in get_videos(search, 200):
    url = "https://www.youtube.com/watch?v="+video['id']
    transcripts = Transcript.get(url)

    print(str(index) + ' - ' + video['title'] + " - " + video['id'])
    if len(transcripts["languages"]) != 0:
        
        print(transcripts["languages"])

    if transcript_has_language(transcripts["languages"], language):
        print("Mám: ",language['title'])
    
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
