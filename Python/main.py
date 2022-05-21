import sys
import time
import random
import argparse

from search import *
from tools import *
from video import *
from subtitles import *
from non_blocking_input import *
import colors


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
        print(colors.Red + "ERROR:" + colors.NC, e)
        return False
    return True


def process_video(video_json, language, language_dictionary, downloaded, index=None):
    language_code = language["code"]
    video = Video(video_json, language_code)
    if VERBOSE:
        print(str(index) + '. ' + str(video))

    # allready downloaded
    if downloaded.get(video.id) is not None:
        if VERBOSE:
            print("Allready downloaded.")
        return False

    # not valid language title
    if not is_in_language(language_dictionary, video.title, DICT_MATCH):
        if VERBOSE:
            print("Title not in my language.")
        return False

    try:
        transcript = Subtitles(video.id, language_code)
    except Exception as e:
        print(colors.Yellow + "Warning:" + colors.NC,
              "Subtitles are disabled for this video")
        return False

    if len(list(transcript.get_languages())) != 0:
        if DEBUG:
            print(transcript)

    # does not have valid language trancritpion
    if not transcript.has_language(language_code):
        return False

    if DEBUG:
        print("Got: ", colors.Blue + language['title'], colors.NC)
    return download(video, transcript)


def parse_args(args):
    """parse arguments"""
    parser = argparse.ArgumentParser(
        description='Youtube video & subtitles downloader.')
    parser.add_argument(
        "-l", "--language", help="select language")
    parser.add_argument(
        "-w", "--words", help="Set number of generated words.",
        default=3, type=int)
    parser.add_argument(
        "-i", "--iterations", help="Number of tested iterations for query",
        default=1000, type=int)
    parser.add_argument(
        "-v", "--verbose", help="Increase verbosity.",
        action="store_true", default=False)
    parser.add_argument(
        "-d", "--debug", help="Run debug options.",
        action="store_true", default=False)
    args = parser.parse_args(args)
    if args.language is None:
        parser.error("Language must be selected!")

    # TODO
    DEBUG = args.debug
    VERBOSE = args.verbose
    ret = [args.language, args.words, args.iterations]
    return ret


# config
DEBUG = True
VERBOSE = True
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
    },
    "NO": {
        "title": "Norsk",
        "code": "no",
        "file_name": None
    }
}

if __name__ == '__main__':
    selected_language, number_of_words, iterations = parse_args(sys.argv[1:])

    language = languages[selected_language]
    language_code = language["code"]
    downloaded_file = "downloaded.data"
    lang_folder = "../dict"

    path = get_path(lang_folder, language["file_name"])
    all_words = read_file(path)
    language_dictionary = list_to_dict(all_words)
    DICT_MATCH = 2

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
            search = VideosSearch(query, language=language_code)
            if DEBUG:
                print("Quering initial search.")

            index = 0
            for video_json in get_videos(search, iterations):
                index += 1

                process_video(video_json, language,
                              language_dictionary, downloaded, index)

                # check pressed key
                if isData():
                    c = sys.stdin.read(1)
                    if c == "q":
                        exit = True

    finally:
        print("Exiting...")
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        print("Done")

"""
Ukladat navrhovaná slová
Lepší detekce jazyka z názvu videa
Ukládat log
fasttext

cca 30-100 souborů
Jazyky k analíze:
Projít ručo/algoritmicky
Češtině, Slověnština, Němčina, Angličtina
Bez analízy:
Noršitna Švédština


analýza funkčnosti
tabulka
česke, české video
neni česke, česke video
české vide, titulky nejsou česke .....
jazyk v češtině, titulky v češtině, nesouhlasí
ǔspšnost na češtině taková a taková

15-20
Titulní strana
Zadání
Cíl projektu
Složitost 

Způsob řešení
Nástroje
Uvažovaná řešení
Co nikam nevdlo

Odevzdávané řešení
Uživatelksý manuál

Analýza výsledků
Rychlost a úspěšnost
Tabulka 
Závěr
Vyhlídky do budoucna

"""
