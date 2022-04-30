import random
from youtubesearchpython import *

from tools import *
from video import *
from subtitles import *
from non_blocking_input import *


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


def process_video(video_json, index=None):
    video = Video(video_json)
    print(str(index) + ' - ' + video.title + " - " + video.id)
    
    try:
        transcript = Subtitles(video.id, language["code"])
    except Exception:
        return False

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
        
# config
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

iterations = 1000
number_of_words = 3
path = get_path(lang_folder, language["file_name"])
dictionary = read_file(path)

old_settings = termios.tcgetattr(sys.stdin)
try:
    tty.setcbreak(sys.stdin.fileno())
    exit = False
    while not exit:
        words = get_n_random(number_of_words, dictionary)
        string = " ".join(words)
        #string = "Česky s titulky"
        string = "Aleš Brichta (s textem)"
        print(string)
        query = string
        #search= CustomSearch(string, VideoSortOrder.uploadDate, language = 'cs', region = 'CZ')
        search = VideosSearch(query, language=language["code"])
        index = 0
        for video_json in get_videos(search, number_of_words):
            index += 1
            process_video(video_json, index)
            
            if isData():
                c = sys.stdin.read(1)
                if c == "q":
                    exit = True

finally:
    print("Exiting...")
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
