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
                                                                             'list': [], "test_list": [],'previous_test_list': []}}
        self.user["passage_num"] = 0
        self.user["room_num"] = 0

    def start(self):
        if self.req['session']['new']:
            self.if_new_session()
            menu = Menu(self.res, self.req, self.user_id)
            self.res = menu.get_res()
        else:
            self.check_answer()

    def check_help(self):
        if 'умеешь' in list(map(lambda x: x.lower(), self.req['request']['nlu']["tokens"])):
            return True
        return False

    def check_phrase(self):
        if self.req['request']["command"].strip().lower() in dialogues_info['is_hello']:
            return [random.choice(dialogues_info['hello']), 0]
        elif self.req['request']["command"].strip().lower() in dialogues_info['is_bye']:
            return [random.choice(dialogues_info['bye']), 1]
        elif self.req['request']["command"].strip().lower() == "ping":
            return ["Кто(Who) я ping???", 0]
        elif self.req['request']["command"].strip().lower() == "ок":
            return ["Хоккей)", 0]
        return False

    def check_answer(self):
        result = self.check_phrase()
        if self.check_help():
            self.res['response']['text'] = dialogues_info["ican"]
            self.res['response']['buttons'] = self.user["previous_buttons"]
            return
        elif result:
            if result[1] == 1:
                self.res['response']['text'] = result[0]
                self.res['response']["end_session"] = True
            else:
                self.res['response']['text'] = result[0]
                self.res['response']['buttons'] = self.user["previous_buttons"]
        elif self.user["passage_num"] == 0:
            if self.req['request']["command"].strip().lower() == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["main"]
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return

            elif self.req['request']["command"].strip().lower() in dialogues_info["structure"]["main_menu"]:
                self.user["passage_num"] = dialogues_info["structure"]["main_menu"].index(
                    self.req['request']["command"].strip().lower()) + 1

                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                self.res = a.get_menu()
                return 0
            else:
                self.res['response']['text'] = random.choice(dialogues_info["incomprehension"])
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
        return self.res
