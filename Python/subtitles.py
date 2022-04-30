from youtube_transcript_api import YouTubeTranscriptApi as YTTA

class InvalidInput(Exception):
    """
    Invalid input exception.
    """

def transcript_has_language(transcripts, language):
    for transcript in transcripts:
        if transcript['title'] == language['title']:
            return True
    return False

def transcript_get_languages(transcripts):
    languages = []
    for transcript in transcripts:
        languages.append(transcript['title'])
    return languages

class Subtitles():
    def __init__(self, id, language=None):
        self.id = id
        if language==None:
            self.languages = YTTA.list_transcripts(id)
        else:
            self.text = YTTA.get_transcript(id, languages=[language])

    def save(self, file):
        if self.text is not None:
            

    def __str__(self):
        return ("# Subitles: \tLanguage: " + self.title)

if __name__ == '__main__':
    id = "bRUtDtMAVKQ"
    transcript_list = YTTA.list_transcripts(id)
    print(transcript_list)
    srt = YTTA.get_transcript(id, languages=['cs'])
    print(srt)
    srt = YTTA.get_transcript(id, languages=['en'])
    print(srt)
