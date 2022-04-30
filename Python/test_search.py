from search import *


def test_generator_lenght():
    iterations = 20
    query = "Aleš Brichta (s textem)"
    search = VideosSearch(query, language="cs")
    assert len(list(get_videos(search, iterations))) == iterations

def test_generator_and_list():
    iterations = 20
    query = "Aleš Brichta (s textem)"
    search = VideosSearch(query, language="cs")
    for video1, video2 in zip(get_videos_list(search, iterations), get_videos(search, iterations)):
        assert compare_video(video1, video2)