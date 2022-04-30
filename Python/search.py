from youtubesearchpython import *

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
        if not search.next():
            end = True
            if DEBUG:
                print("Search does not have more videos.")

def get_videos_list(search, n=100):
    i = 0
    videos = []
    for video in search.result()['result']:
        i += 1
        videos.append(video)
        if i > n:
            break
    return videos

def compare_video(video1, video2):
    return video1['title'] == video2['title']

def print_videos(search):
    for video in search.result()['result']:
        print(video['title'])
        