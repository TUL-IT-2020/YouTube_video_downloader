import pytest
from tools import *

language = ["kůň", "ódy", "o", "a", "ďáblů", "péče"]
texts_valid = [False, True, True, True]
texts = [
    "The quick brown fox jumps over a lazy dog.",
    "Příliš žluťoučký kůň úpěl ďábelské ódy.",
    "Nechť již hříšné saxofony ďáblů rozezvučí síň úděsnými tóny waltzu, tanga a quickstepu.",
    "Inkoust Tattoo .  PÉČE O TETOVÁNÍ . Suprasorb F"
]

@pytest.mark.parametrize('punctuation, removed_punctuation', [
    (
        "!hi. wh?at is the weat[h]er lik?e.",
        "hi what is the weather like"
    )
])
def test_remove_punctuation(punctuation, removed_punctuation):
    generated = remove_punctuation(punctuation).split()
    striped = removed_punctuation.split()
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

@pytest.mark.parametrize('text_valid, text', [
    [True, "Inside Star Citizen: Budoucnost vesmírného boje"],
    [True, "včelařství S receptem zesnulého Muhsina Dogaroğlua."],
    [False, "Our Miss Brooks: Connie the Work Horse / Babysitting for Three / Model School Teacher"],
    [False, "Angolan Civil War Documentary Film"],
    [True, "Modern Horizons 2: neuvěřitelné rozšíření Magic The Gathering v 30 krabicích"],
    [True, "Pétanque - křest koulí/baptême de boules/baptism of balls CZ/FR/EN"],
    [True, "Vražedná přísaha(2021)Thiller CZdabing"],
    [True, "Simpsonovi - Vířivka"]
])
def test_is_in_language(text_valid, text):
    min_matches = 2
    path = get_path("../dict", "czech.txt")
    dictionary = list_to_dict(read_file(path))
    matches = words_matches(dictionary, text)
    print(matches)
    assert text_valid == (True if matches >= min_matches else False)