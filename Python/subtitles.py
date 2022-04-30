from youtube_transcript_api import YouTubeTranscriptApi as YTTA

from tools import *

class InvalidLanguage(Exception):
    pass

folder = "../download"
path = get_path(folder)

class Subtitles():
    def __init__(self, id, language=None):
        self.id = id
        self.language = language
        self.transcripts = YTTA.list_transcripts(id)
        self.fetch_language(language)

    def get_languages(self):
        for transcript in self.transcripts:
            yield transcript.language_code

    def has_language(self, language):
        for transcript in self.transcripts:
            if transcript.language_code == language:
                return True
        return False

    def fetch_language(self, language):
        if language is not None and self.has_language(language):
            self.text = YTTA.get_transcript(self.id, languages=[language])
            #transcript.fetch()

    def save(self, file_name=None, plain_text=False):
        if self.text is None:
            raise InvalidLanguage
        
        if file_name is None:
            file = path + "/" + self.id + "_" + self.language + ".txt"
        else:
            file = path + "/" + file_name + ".txt"
        
        with open(file, "w") as f:
            for line in self.text:
                if plain_text:
                    f.write(line["text"]+"\n")
                else:
                    f.write("{}\n".format(line))

    def __str__(self):
        string = "id: \t\t Language: \t Code: \t Generated:\n"
        for transcript in self.transcripts:
            string += (""+
                transcript.video_id + "\t " +
                transcript.language + "\t " +
                transcript.language_code + "\t " +
                str(transcript.is_generated) + "\n"
            )
        return string

if __name__ == '__main__':
    id = "bRUtDtMAVKQ"
    language = "cs"

    transcript_list = YTTA.list_transcripts(id)
    sub = Subtitles(id)
    print(sub)
    sub = Subtitles(id, language)
    sub.save()
    sub.save(id + "_" + language + "_plain", plain_text=True)
    
    #srt = YTTA.get_transcript(id, languages=['en'])
    #print(srt)