import os
import random
import string

def get_path(directory, file_name="."):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), directory, file_name))


def read_file(path):
    try:
        file = open(path, "r", encoding='utf-8')
    except:
        print("ERROR while tring to read file:", path)
        return None
    else:
        text = file.read().splitlines()
        file.close()
        return text


def remove_punctuation(text : string):
    return text.translate(str.maketrans('', '', string.punctuation))


def is_in_language(language: dict, text: string, min_matches: int = 1):
    matches = 0
    for word in text.split():
        if language.get(remove_punctuation(word), False):
            matches +=1
    return True if matches >= min_matches else False


def list_to_dict(l: list, value : bool = True):
    dictionary = {key: value for key in l}
    return dictionary


def pick_random_key_from_dict(d: dict):
    """Grab a random key from a dictionary."""
    keys = list(d.keys())
    random_key = random.choice(keys)
    return random_key


def pick_random_item_from_dict(d: dict):
    """Grab a random item from a dictionary."""
    random_key = pick_random_key_from_dict(d)
    random_item = random_key, d[random_key]
    return random_item


def pick_random_value_from_dict(d: dict):
    """Grab a random value from a dictionary."""
    _, random_value = pick_random_item_from_dict(d)
    return random_value