import time
import random

from search import *
from tools import *
from video import *
from subtitles import *
from non_blocking_input import *


def get_n_random(n, array):
    entrys = []
    for i in range(n):
        entrys.append(random.choice(array))
    return entrys


def process_video(video_json, index=None):
    video = Video(video_json)
    if VERBOSE:
        print(str(index) + ' - ' + video.title + " - " + video.id)
    
    try:
        transcript = Subtitles(video.id, language["code"])
    except Exception as e:
        print("ERROR:", e)
        return False

    if len(list(transcript.get_languages())) != 0:
        if DEBUG:
            print(transcript)

    if transcript.has_language(language["code"]):
        if DEUBG:
            print("Got: ",language['title'])
        try:
            if VERBOSE:
                print("Downloading video...")
            video.save(video.id)
            if VERBOSE:
                print("Downloading transcript...")
            transcript.save(video.id)
            if VERBOSE:
                print("Downloading is finished.")
        except Exception as e:
            print("ERROR:", e)
        
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

DEBUG = True
VERBOSE = True
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
        print(string)
        time.sleep(2)
        query = string
        #search= CustomSearch(string, VideoSortOrder.uploadDate, language = 'cs', region = 'CZ')
        search = VideosSearch(query, language=language["code"])
        index = 0
        for video_json in get_videos(search, iterations):
            index += 1
            process_video(video_json, index)
            if isData():
                c = sys.stdin.read(1)
                if c == "q":
                    exit = True

finally:
    print("Exiting...")
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
