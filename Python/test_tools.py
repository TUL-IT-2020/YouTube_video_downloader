import pytest
from tools import *

DEBUG = True

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
        assert is_in_language_old(dictionary, word)

def test_is_in_language():
    dictionary = list_to_dict(language)
    for text, text_valid in zip(texts, texts_valid):
        assert text_valid == is_in_language_old(dictionary, text, 2)

@pytest.mark.parametrize('text_valid, text', [
    [True, "Test čekoho jazyka."],
    [False, "This is written in English."]
])
def test_is_in_language_old(text_valid, text):
    min_matches = 2
    path = get_path("../dict", "czech.txt")
    dictionary = list_to_dict(read_file(path))
    matches = words_matches(dictionary, text)
    print(matches)
    assert text_valid == is_in_language_old(dictionary, text, min_matches)


@pytest.mark.parametrize('text_valid, text', [
    [True, "Inside Star Citizen: Budoucnost vesmírného boje"],
    [True, "včelařství S receptem zesnulého Muhsina Dogaroğlua."],
    [True, "Modern Horizons 2: neuvěřitelné rozšíření Magic The Gathering v 30 krabicích"],
    [True, "Vražedná přísaha(2021)Thiller CZdabing"],
    [True, "Simpsonovi - Vířivka"],
    [True, "Wot cz - Operace Overlord + trochu času navíc / Novinky a Speciály"],
    [False, "Our Miss Brooks: Connie the Work Horse / Babysitting for Three / Model School Teacher"],
    [False, "Angolan Civil War Documentary Film"],
    [False, "ԽՈՒՏՈՒՏ SHOW ԺԱՌԱՆԳՈՐԴԸ:"],
    [False, "ዘማሪ ኤፍሬም አለሙና አገልጋይ ዮናታን አክሊሉ ድንቅ አምልኮ ሁላችሁም ተባረኩበት OCT 7,2019 MARSIL TV WORLDWIDE"]
])
def test_is_in_language(text_valid, text):
    language_code = "cs"
    assert text_valid == is_in_language(language_code, text, 0.3)


"""

    [True, "MUSITE ZKUSIT!! Trenink na nohy - Martin Mester IFBB PRO"],
    [False, "ODESSA MARKET as PRIVACE CEN. Takovou jahodu jsem ještě neviděla!"]
"""

@pytest.mark.parametrize('text_valid, text, language_code', [
    [True, "8 fermentovaných potravin pro podporu trávení a zdraví", "sk"],
    [True, "Ukládejte e-maily z Hotmailu na pevný disk počítače", "sk"],
    [True, "Kde voda chutná jako víno Kapitola 1 Maine, Vermont a Massachusetts Žádný komentář", "sk"]
])
def test_is_in_language_with_code(text_valid, text, language_code):
    assert text_valid == is_in_language(language_code, text, 0.3)
