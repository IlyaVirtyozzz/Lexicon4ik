import random
from constants import sessionStorage, dialogues_info, data, logging
from rooms import Antonyms, Buzzwords, Paronyms, Phraseologisms, Stupid_Dictionary, Vocabulary_words, Menu


class Main_class():
    def __init__(self, res, req):
        self.mains_passage = [self.main_menu, self.buzzwords_menu, self.vocabulary_words_menu, self.phraseologisms_menu,
                              self.antonyms_menu, self.paronyms_menu, self.stupid_dictionary_menu]
        self.words_id = {"1": "buzzwords", "2": "vocabulary_words", "3": "phraseologisms", "4": "antonyms",
                         "5": "paronyms", "6": "stupid_dictionary", }
        self.classes_list = [Buzzwords, Vocabulary_words, Phraseologisms, Antonyms, Paronyms, Stupid_Dictionary]
        self.res = res
        self.req = req
        self.user_id = req['session']['user_id']
        self.user = sessionStorage.get(self.user_id)

    def if_new_session(self):
        if not self.user:
            self.user = sessionStorage[self.user_id] = {"passage_num": 0, "room_num": 0, "previous_buttons": [],
                                                        "phraseologisms": {"phraseologisms_step_num": 0, 'list': []},
                                                        "paronyms": {"paronyms_step_num": 0,
                                                                     "paronyms_test_step_num": 0, 'list': [],
                                                                     "test_list": [], 'previous_test_list': []},
                                                        "antonyms": {"antonyms_test_step_num": 0,
                                                                     "antonyms_step_num": 0, 'list': [],
                                                                     "test_list": [], 'previous_test_list': []},
                                                        "buzzwords": {"buzzword_step_num": 0, 'list': []},
                                                        "stupid_dictionary": {"stupid_dictionary_step_num": 0,
                                                                              'list': []},
                                                        "vocabulary_words": {"vocabulary_words_step_num": 0,
                                                                             "vocabulary_words_test_step_num": 0,
                                                                             'list': [], "test_list": [],
                                                                             'previous_test_list': []}}
        self.user["passage_num"] = 0
        self.user["room_num"] = 0

    def start(self):
        if self.req['session']['new']:
            self.if_new_session()
            menu = Menu(self.res, self.req, self.user_id, True)
            self.res = menu.get_res()
        else:
            self.check_answer()

    def check_can(self):
        if 'умеешь' in list(map(lambda x: x.lower(), self.req['request']['nlu']["tokens"])):
            return True
        return False

    def check_answer(self):
        command = self.req['request']["original_utterance"].strip().lower()
        tokens = self.req['request']['nlu']['tokens']
        if self.check_can():
            self.res['response']['text'], self.res['response']['tts'] = dialogues_info["ican"]
            self.res['response']['buttons'] = self.user["previous_buttons"]
            return
        elif any(word in tokens for word in ["алиса", "alice", "алис"]):
            self.res['response']['text'], self.res['response']['tts'] = ["Ой. Я не Алиса. Можно сказать, я её друг.",
                                                                         "Ой. Я не Ал+иса. Можно сказ+ать, я её др+уг."]
            self.res['response']['buttons'] = self.user["previous_buttons"]
            return
        elif any(word in tokens for word in dialogues_info['is_hello']):
            self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info['hello'])
            self.res['response']['buttons'] = self.user["previous_buttons"]
            return

        elif any(word in tokens for word in dialogues_info['is_bye']):
            self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info['bye'])
            self.res['response']['buttons'] = self.user["previous_buttons"]
            return

        elif any(word in command.split() for word in dialogues_info['fuck_words']):
            self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info["fuck_answer"])
            self.res['response']['buttons'] = self.user["previous_buttons"]
            return
        elif all(word in tokens for word in ["как", "тебя", "зовут"]):
            self.res['response']['text'], self.res['response']['tts'] = ["Сам прихожу. А так, имени у меня нет)",
                                                                         "Сам прихож+у. А т+ак, +имени у мен+я н+ет)"]
            self.res['response']['buttons'] = self.user["previous_buttons"]
            return
        elif any(word in tokens for word in ["ясно", "понятно"]):
            self.res['response']['text'], self.res['response']['tts'] = ["Хе-хе",
                                                                         "Хе-хе"]
            self.res['response']['buttons'] = self.user["previous_buttons"]
            return
        elif self.user["passage_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["main"]
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return

            elif any(word in tokens for word in ["поехали", "давай", "начать", "начинаем", "старт", "стартуем", "да"]):
                self.res['response']['text'], self.res['response']['tts'] = ["Поехали! Ой, выбери сначала категорию.",
                                                                             "По+ехали! Ой,sil <[200]> в+ыбери снач+ала катег+орию."]
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return

            elif command in dialogues_info["structure"]["main_menu"]:

                if any(word in tokens for word in ["интересные", "крутые"]):
                    self.user["passage_num"] = 1
                if any(word in tokens for word in ["словарные", "сс", "словарь"]):
                    self.user["passage_num"] = 2
                if any(word in tokens for word in ["фразеологизмы", "фразиология", "фраз"]):
                    self.user["passage_num"] = 3
                if any(word in tokens for word in ["антоним", "антонимы", "антон"]):
                    self.user["passage_num"] = 4
                if any(word in tokens for word in ["пароним", "парон", "парные", "паронимы"]):
                    self.user["passage_num"] = 5
                if any(word in tokens for word in ["глупые", "бестолковые"]):
                    self.user["passage_num"] = 6
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                self.res = a.get_menu()

            else:
                self.res['response']['text'], self.res['response']['tts'] = random.choice(
                    dialogues_info["incomprehension"])
                self.user["previous_buttons"] = self.res['response']['buttons'] = dialogues_info['buttons']["main"]
        else:
            self.mains_passage[self.user["passage_num"]]()

    def main_menu(self):
        pass

    def buzzwords_menu(self):

        buzzwordsmenu = Buzzwords(self.res, self.req, self.user_id)
        self.res = buzzwordsmenu.sequence()

    def antonyms_menu(self):
        antonymsmenu = Antonyms(self.res, self.req, self.user_id)
        self.res = antonymsmenu.sequence()

    def phraseologisms_menu(self):
        phraseologismsmenu = Phraseologisms(self.res, self.req, self.user_id)
        self.res = phraseologismsmenu.sequence()

    def paronyms_menu(self):
        paronymsmenu = Paronyms(self.res, self.req, self.user_id)
        self.res = paronymsmenu.sequence()

    def stupid_dictionary_menu(self):
        stupidmenu = Stupid_Dictionary(self.res, self.req, self.user_id)
        self.res = stupidmenu.sequence()

    def vocabulary_words_menu(self):
        vocabularymenu = Vocabulary_words(self.res, self.req, self.user_id)
        self.res = vocabularymenu.sequence()

    def get_response(self):
        if self.req['request']["original_utterance"] != "ping":
            logging.info(self.res['session']["user_id"][:5] + " : " + self.res['response']['text'])
        return self.res
