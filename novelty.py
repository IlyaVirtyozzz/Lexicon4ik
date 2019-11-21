from helper import read_json
from constants import db, data
from database import add_new_vocline, Line_Vocabulary_words
import random


class Antonym():
    def __init__(self):
        self.words = None

    def random_words(self):
        self.words = random.choice(data['antonyms'])

    def edit_the_view(self, words):
        letter = ""
        head = list(words.keys())[0]
        values = words[list(words.keys())[0]]


class Paronym():
    def __init__(self):
        self.words = None

    def random_words(self):
        self.words = random.choice(data['paronyms'])

    def edit_the_view(self, words):
        letter = ""
        head = list(words.keys())[0]
        values = words[list(words.keys())[0]]


class Phraseologism():
    def __init__(self):
        self.words = None

    def random_words(self):
        self.words = random.choice(data['phraseologisms'])

    def edit_the_view(self, words):
        letter = ""
        head = list(words.keys())[0]
        values = words[list(words.keys())[0]]


class Buzzword():
    def __init__(self):
        self.words = None

    def random_words(self):
        self.words = random.choice(data['buzzword'])

    def edit_the_view(self, words):
        letter = ""
        head = list(words.keys())[0]
        values = words[list(words.keys())[0]]


class Stupid_Dictionary():
    def __init__(self):
        self.words = None

    def random_words(self):
        self.words = random.choice(data['stupid_dictionary'])

    def edit_the_view(self, words):
        letter = ""
        head = list(words.keys())[0]
        values = words[list(words.keys())[0]]


class Vocabulary_words():
    def __init__(self, req):
        self.words = []
        self.user_id = req['session']['user_id']

    def if_first_time(self):
        self.line = db.session.query(Line_Vocabulary_words).filter_by(user_id=self.user_id).first()
        if not self.line:
            add_new_vocline(self.user_id)
            self.line = db.session.query(Line_Vocabulary_words).filter_by(user_id=self.user_id).first()

    def create(self):
        self.if_first_time()


    def edit_the_view(self, words):
        letter = ""
        head = list(words.keys())[0]
        values = words[list(words.keys())[0]]

    def get_letter(self):
        pass
