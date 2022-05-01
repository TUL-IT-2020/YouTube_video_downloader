from tools import *


language = ["kůň", "ódy", "o", "a", "ďáblů", "péče"]
texts_valid = [False, True, True, True]
texts = [
    "The quick brown fox jumps over a lazy dog.",
    "Příliš žluťoučký kůň úpěl ďábelské ódy.",
    "Nechť již hříšné saxofony ďáblů rozezvučí síň úděsnými tóny waltzu, tanga a quickstepu.",
    "Inkoust Tattoo .  PÉČE O TETOVÁNÍ . Suprasorb F"
]
# Inside Star Citizen: Budoucnost vesmírného boje

punctuation = "!hi. wh?at is the weat[h]er lik?e."
removed_punctuation = "hi what is the weather like"

def test_remove_punctuation():
    for generated, striped in zip(remove_punctuation(punctuation).split(), removed_punctuation.split()):
        assert generated == striped

def test_list_to_dict_len():
    dictionary = list_to_dict(language)
    assert len(list(dictionary)) == len(language)

def test_list_to_dict_words():
    dictionary = list_to_dict(language)
    for word in language:
        assert is_in_language(dictionary, word)

def test_is_in_language():
    dictionary = list_to_dict(language)
    for text, text_valid in zip(texts, texts_valid):
        assert text_valid == is_in_language(dictionary, text, 2)