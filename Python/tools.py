import os

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