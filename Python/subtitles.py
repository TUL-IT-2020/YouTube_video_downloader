from youtube_transcript_api import YouTubeTranscriptApi as YTTA

class InvalidLanguage(Exception):
    pass


class Subtitles():
    def __init__(self, id, language=None):
        self.id = id
        self.language = language
        self.transcripts = YTTA.list_transcripts(id)
        self.get_language(language)

    def has_language(self, language):
        for transcript in self.transcripts:
            if transcript.language_code == language:
                return True
        return False

    def get_language(self, language):
        if language is not None and self.has_language(language):
            self.text = YTTA.get_transcript(self.id, languages=[language])
            #transcript.fetch()

    def save(self, file=None, plain_text=False):
        if self.text is None:
            raise InvalidLanguage
        if file is None:
            file = self.id + "_" + self.language + ".txt"
        
        with open(file, "w") as f:
            for line in self.text:
                if plain_text:
                    f.write(line[text]+"\n")
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
    languages = "cs"
    transcript_list = YTTA.list_transcripts(id)
    sub = Subtitles(id)
    print(sub)
    sub = Subtitles(id, languages)
    sub.save()
    #srt = YTTA.get_transcript(id, languages=['en'])
    #print(srt)
