import os
from enum import Enum
from datetime import datetime


class Topics(Enum):
    F1 = 'f1'
    FOOTBALL = 'football'
    NBA = 'nba'
    TENNIS = "tennis"


class Models(Enum):
    LLAMA2 = 'llama-2-70b-chat'
    GPT = 'gpt-3.5-turbo'


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


def current_date():
    return datetime.now().strftime("%d-%B-%Y")


def create_document(topic: Topics, title: str, content: str):
    dir = os.path.join(DOCUMENTS_PATH, topic.value, "pending")
    if not os.path.exists(dir):
        os.makedirs(dir)
    path = os.path.join(dir, title)
    with open(path, 'w') as archivo:
        archivo.write(current_date() + "\n" + content)


def clean_title(title):
    cleaned_string = title.strip()
    trans_table = str.maketrans({"'": None, '"': None, '“': None, '”': None, '‘': None, '’': None, '/': None})
    cleaned_string = cleaned_string.translate(trans_table)
    return cleaned_string
