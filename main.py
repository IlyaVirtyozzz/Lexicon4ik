import random
from constants import sessionStorage, dialogues_info


class Main_class():
    def __init__(self, req):
        self.mains_passage = [self.main_menu, self.buzzwords_menu, self.vocabulary_words_menu, self.phraseologisms_menu,
                              self.antonyms_menu, self.paronyms_menu, self.stupid_dictionary_menu, self.brainstorm_menu]
        self.words_id = {"1": "buzzwords", "2": "vocabulary_words", "3": "phraseologisms", "4": "antonyms",
                         "5": "paronyms", "6": "stupid_dictionary", "7": "brainstorm"}
        self.res = {}
        self.req = req
        self.user_id = req['session']['user_id']
        self.user = sessionStorage.get("user_id")

    def if_new_session(self):
        if not self.user:
            self.user = sessionStorage["user_id"] = {"passage_num": 0, "room_num": 0,
                                                     "phraseologisms": {"phraseologisms_step_num": 0},
                                                     "paronyms": {"paronyms_step_num": 0, "paronyms_test_step_num": 0},
                                                     "antonyms": {"antonyms_test_step_num": 0, "antonyms_step_num": 0},
                                                     "buzzword": {"buzzword_step_num": 0},
                                                     "stupid_dictionary": {"stupid_dictionary_step_num": 0},
                                                     "vocabulary_words": {"vocabulary_words_step_num": 0,
                                                                          "vocabulary_words_test_step_num": 0},
                                                     "brainstorm": {"brainstorm_step_num": 0}}
        self.user["passage_num"] = 0
        self.user["room_num"] = 0

    def start(self):
        if self.req['session']['new']:
            self.if_new_session()
            self.res['response']['text'] = "ПРивет. ЭТо меню"
            self.res['response']['buttons'] = dialogues_info['buttons']["main_menu"]
        else:
            self.check_answer()
            self.mains_passage[self.user["passage_num"]]()

    def check_help(self):
        if 'помощь' in list(map(lambda x: x.lower(), self.req['request']['nlu']["tokens"])) or 'умеешь' in list(
                map(lambda x: x.lower(), self.req['request']['nlu']["tokens"])):
            return True
        return False

    def check_answer(self):
        if self.check_help():
            self.res['response']['text'] = dialogues_info["helps"]
            return
        elif self.user["passage_num"] == 0:
            if self.req['request']["command"].strip().lower() in dialogues_info["structure"]["main_menu"]:
                self.user["passage_num"] = dialogues_info["structure"]["main_menu"].index(
                    self.req['request']["command"].strip().lower()) + 1
            else:
                self.res['text'] = random.choice(dialogues_info["incomprehension"])
        else:
            command = self.req['request']["command"].strip().lower()
            struct_room = dialogues_info["structure"][self.words_id[str(self.user["room_num"])]]
            if command in struct_room:
                i = struct_room.index(command)
                if i + 1 == len(struct_room):
                    self.user["passage_num"] = 0
                    self.user["room_num"] = 0
                    return
                else:
                    self.user["room_num"] = i
            else:
                self.res['text'] = random.choice(dialogues_info["incomprehension"])

    def main_menu(self):
        pass

    def antonyms_menu(self):
        pass

    def phraseologisms_menu(self):
        pass

    def paronyms_menu(self):
        pass

    def buzzwords_menu(self):
        pass

    def stupid_dictionary_menu(self):
        pass

    def vocabulary_words_menu(self):
        pass

    def brainstorm_menu(self):
        pass

    def get_response(self):
        return self.res
