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

def add_video_to_downloaded(downloaded, video, transcript):
    key, data = video.to_json()
    data['transcript_languages'] = list(transcript.get_languages())
    downloaded[key] = data

def process_video(video_json, downloaded, index=None):
    video = Video(video_json)
    if VERBOSE:
        print(str(index) + ' - ' + str(video))
    
    try:
        transcript = Subtitles(video.id, language["code"])
    except Exception as e:
        print("Warning:", "Subtitles are disabled for this video")
        return False

    if len(list(transcript.get_languages())) != 0:
        if DEBUG:
            print(transcript)

    if transcript.has_language(language["code"]):
        if DEBUG:
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
            add_video_to_downloaded(downloaded, video, transcript)
        except Exception as e:
            print("ERROR:", e)
            return False
    return True
        
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
downloaded_file = "downloaded.data"
lang_folder = "../dict"
language = languages["CS"]

iterations = 1000
number_of_words = 3
path = get_path(lang_folder, language["file_name"])
dictionary = read_file(path)

old_settings = termios.tcgetattr(sys.stdin)
downloaded = {}
try:
    tty.setcbreak(sys.stdin.fileno())
    exit = False
    while not exit:
        words = get_n_random(number_of_words, dictionary)
        query = " ".join(words)
        if VERBOSE:
            print("Searched words:")
            print(query)
        time.sleep(2)
        search = VideosSearch(query, language=language["code"])
        if DEBUG:
            print("Quering initial search.")
        
        index = 0
        for video_json in get_videos(search, iterations):
            index += 1

            # yet not downloaded
            if downloaded.get(video_json['id']) is None:
                process_video(video_json, downloaded, index)
            
            # check pressed key
            if isData():
                c = sys.stdin.read(1)
                if c == "q":
                    exit = True

finally:
    print("Exiting...")
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    print("Done")
