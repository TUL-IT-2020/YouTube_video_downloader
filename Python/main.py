import sys
import time
import argparse
import threading

from search import *
from video import *
from subtitles import *
from non_blocking_input import *
import tools
import colors


def add_video_to_downloaded(downloaded, video, transcript):
    key, data = video.to_json()
    data['transcript_languages'] = list(transcript.get_languages())
    downloaded[key] = data


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

    ret = [args.language, args.words, args.iterations, args.debug, args.verbose]
    return ret


def download(video, transcript, downloaded):
    try:
        if VERBOSE:
            print("Downloading video...")
        video.save(video.id + "_" + video.title)
        # video.save(video.id)
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


def process_video(video_json, language, downloaded, index=None):
    match = 0.3
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
    if not is_in_language(language_code, video.title, match):
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
    return download(video, transcript, downloaded)


def check_end():
    endLock.acquire()
    value = end
    endLock.release()
    return value


class WorkerThread(threading.Thread):
    lang_folder = "../dict"

    def __init__(self, language, iterations, number_of_words):
        threading.Thread.__init__(self)
        self.language = language
        self.iterations = iterations
        self.number_of_words = number_of_words
        self.language_code = language["code"]
        path = get_path(self.lang_folder, self.language["file_name"])
        self.all_words = read_file(path)
        self.downloaded = {}

    def run(self):
        while not check_end():
            words = get_n_random(self.number_of_words, self.all_words)
            query = " ".join(words)
            if VERBOSE:
                print("Searched words:")
                print(query)
            search = VideosSearch(query, language=self.language_code)
            if DEBUG:
                print("Quering initial search.")

            index = 0
            for video_json in get_videos(search, self.iterations):
                index += 1
                process_video(video_json, self.language,
                              self.downloaded, index)
                if check_end():
                    break

        # TODO
        # store downloaded


# config
DEBUG = False
VERBOSE = False
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
    "SK": {
        "title": "Slovak",
        "code": "sk",
        "file_name": "slovak.txt"
    },
    "EN": {
        "title": "English",
        "code": "en",
        "file_name": "engmix.txt"
    },
    "NO": {
        "title": "Norsk",
        "code": "no",
        "file_name": "norsk.txt"
    }
}

if __name__ == '__main__':
    selected_language, number_of_words, iterations, DEBUG, VERBOSE = parse_args(
        sys.argv[1:])
    if DEBUG:
        tools.DEBUG = True
    language = languages[selected_language]
    endLock = threading.Lock()
    worker_thread = WorkerThread(language, iterations, number_of_words)

    end = False
    old_settings = termios.tcgetattr(sys.stdin)
    worker_thread.start()
    try:
        tty.setcbreak(sys.stdin.fileno())
        while True:
            if isData():
                c = sys.stdin.read(1)
                print("You presed:", c)
                if c == "q":
                    endLock.acquire()
                    print("Exiting proces started...")
                    end = True
                    endLock.release()
                    break
    finally:
        worker_thread.join()
        print("Exiting...")
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        print("Done")

"""
Ukladat navrhovaná slová
Ukládat log

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
