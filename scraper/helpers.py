import os
from enum import Enum


class Topics(Enum):
    F1 = 'f1'
    FOOTBALL = 'football'
    NBA = 'nba'
    TENNIS = "tennis"


my_path = os.path.abspath(os.path.dirname(__file__))
DOCUMENTS_PATH = os.path.join(my_path, "..", "scraper", "documents")
documents = []


def get_all_documents(topic: Topics):
    try:
        dir = os.path.join(DOCUMENTS_PATH, topic.value)
        return os.listdir(dir)
    except FileNotFoundError:
        # Directory will be created in the create_document call
        return []


def create_document(topic: Topics, title: str, content: str):
    dir = os.path.join(DOCUMENTS_PATH, topic.value)
    if not os.path.exists(dir):
        os.makedirs(dir)
    path = os.path.join(dir, title)
    print(title)
    with open(path, 'w') as archivo:
        archivo.write(content)


def clean_title(title):
    cleaned_string = title.strip()
    trans_table = str.maketrans({"'": None, '"': None, '“': None, '”': None})
    cleaned_string = cleaned_string.translate(trans_table)
    return cleaned_string
