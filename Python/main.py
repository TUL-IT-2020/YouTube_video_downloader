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


def download(video, transcript):
    try:
        if VERBOSE:
            print("Downloading video...")
        video.save(video.id)
        if VERBOSE:
            print("Downloading transcript...")
        transcript.save(video.id, plain_text=True)
        if VERBOSE:
            print("Downloading is finished.")
        add_video_to_downloaded(downloaded, video, transcript)
    except Exception as e:
        print("ERROR:", e)
        return False
    return True

def process_video(video_json, language_dictionary, downloaded, index=None):
    video = Video(video_json)
    if VERBOSE:
        print(str(index) + ' - ' + str(video))

    # allready downloaded
    if downloaded.get(video.id) is not None:
        if VERBOSE:
            print("Allready downloaded.")
        return False
    
    # not valid language title
    if not is_in_language(language_dictionary, video.title):
        if VERBOSE:
            print("Title not in my language.")
        return False

    try:
        transcript = Subtitles(video.id, language["code"])
    except Exception as e:
        print("Warning:", "Subtitles are disabled for this video")
        return False

    if len(list(transcript.get_languages())) != 0:
        if DEBUG:
            print(transcript)

    # does not have valid language trancritpion
    if not transcript.has_language(language["code"]):
        return False
    
    if DEBUG:
        print("Got: ", language['title'])
    return download(video, transcript)


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
all_words = read_file(path)
language_dictionary = list_to_dict(all_words)

old_settings = termios.tcgetattr(sys.stdin)
downloaded = {}
try:
    tty.setcbreak(sys.stdin.fileno())
    exit = False
    while not exit:
        words = get_n_random(number_of_words, all_words)
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

            process_video(video_json, language_dictionary, downloaded, index)

            # check pressed key
            if isData():
                c = sys.stdin.read(1)
                if c == "q":
                    exit = True

finally:
    print("Exiting...")
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    print("Done")
