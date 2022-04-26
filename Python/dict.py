import random


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