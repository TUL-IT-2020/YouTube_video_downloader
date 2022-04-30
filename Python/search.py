from youtubesearchpython import *
DEBUG = True

def get_videos(search, n=100):
    i = 0
    end = False
    new_batch = True
    while not end:
        for video in search.result()['result']:
            new_batch = False
            i += 1
            if i > n:
                end = True
                if DEBUG:
                    print("Max iter hit.")
                break
            yield video
        
        if new_batch:
            if DEBUG:
                print("Search does not have more videos.")
            break

        if DEBUG:
            print("Searching more videos.")
        if not end and not search.next():
            end = True
            new_batch = True
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

if __name__ == '__main__':
    iterations = 2
    query = "Aleš Brichta (s textem)"
    search = VideosSearch(query, language="cs")
    lenght = list(get_videos(search, iterations))
    print(len(lenght), iterations)