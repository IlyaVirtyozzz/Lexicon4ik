from helper import read_json
from constants import data, sessionStorage, dialogues_info, logging
import random


class Antonyms():
    def __init__(self, res, req, user_id):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.buttons = dialogues_info['buttons']["antonyms"][:]

    def sequence(self):
        command = self.req['request']["command"].strip().lower()
        if self.user["room_num"] == 0:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["antonyms"]['menu']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command in dialogues_info['structure']["antonyms"]:
                ind = dialogues_info['structure']["antonyms"].index(command)
                if ind + 1 == len(dialogues_info['structure']["antonyms"]):
                    self.user["passage_num"] = 0
                    self.user["room_num"] = 0
                    self.user['antonyms']['antonyms_step_num'] = 0
                    menu = Menu(self.res, self.req, self.user_id)
                    return menu.get_res()
                else:
                    self.user["room_num"] = ind + 1
                    if self.user['room_num'] == 1:
                        return self.get_res()
                    else:
                        return self.get_test_res(0)
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 1:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["antonyms"]['learn']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "далее":
                return self.get_res()
            elif command == 'в меню':
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_step_num'] = 0
                return self.get_menu()
            elif command == "в главное меню":
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 2:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["antonyms"]['test']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "в главное меню":
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_test_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif command == 'в меню':
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_test_step_num'] = 0
                return self.get_menu()
            elif command == "не могу отгадать":
                return self.get_test_res(1)
            elif command in self.user["antonyms"]['previous_test_list']:
                return self.get_test_res(2)
            else:
                return self.get_test_res(3)

    def get_incomprehension(self):
        self.res['response']['text'] = random.choice(dialogues_info["incomprehension"])
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res

    def get_res(self):
        if len(self.user["antonyms"]['list']) == 0:
            words = data["antonyms"][:]
            random.shuffle(words)
            self.user["antonyms"]['list'] = words
        self.user['antonyms']['antonyms_step_num'] += 1
        element = self.user["antonyms"]['list'].pop(0)

        if len(element[list(element.keys())[0]]) > 1:
            text = ""
            for i in element[list(element.keys())[0]]:
                text += "•" + i.capitalize() + "\n"
            text = random.choice(dialogues_info["аntonyms_learn"]["many"]).format(list(element.keys())[0], text)
        else:
            text = random.choice(dialogues_info["аntonyms_learn"]["one"]).format(list(element.keys())[0],
                                                                                 element[list(element.keys())[0]][0])
        self.res['response']['text'] = text
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[1]
        return self.res

    def get_test_res(self, answer=0):
        def func(dont_know=False):
            if len(self.user["antonyms"]['test_list']) == 0:
                words = data["antonyms"][:]
                random.shuffle(words)
                self.user["antonyms"]['test_list'] = words
            self.user['antonyms']['antonyms_test_step_num'] += 1
            element = self.user["antonyms"]['test_list'].pop(0)
            variants = element[list(element.keys())[0]]
            text = random.choice(dialogues_info["antonyms_test"]).format(list(element.keys())[0])
            if dont_know:
                previous = 'Правильные варианты ответов:\n'
                for i in self.user["antonyms"]['previous_test_list']:
                    previous += "•" + i.capitalize() + '\n'
                text = previous + "\n" + text

            self.user["antonyms"]['previous_test_list'] = list(map(lambda x: x.lower(), variants))
            return text

        if answer == 0:
            text = func()
            self.res['response']['text'] = text
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        elif answer == 1:
            text = func(True)
            self.res['response']['text'] = text
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        elif answer == 2:
            text = func()
            self.res['response']['text'] = random.choice(dialogues_info['its_true']) + "\n\n" + text
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        else:
            self.res['response']['text'] = random.choice(dialogues_info["more_options"])
            self.user["previous_buttons"] = self.res['response']['buttons'] = [{"title": "Не могу отгадать",
                                                                                "hide": True}, {
                                                                                   "title": "В главное меню",
                                                                                   "hide": True
                                                                               }]

        return self.res

    def get_menu(self):
        self.res['response'][
            'text'] = dialogues_info['info_for_menu']['antonyms']
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res


class Paronyms():
    def __init__(self, res, req, user_id):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.buttons = dialogues_info['buttons']["paronyms"][:]

    def sequence(self):
        command = self.req['request']["command"].strip().lower()
        if self.user["room_num"] == 0:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["paronyms"]['menu']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command in dialogues_info['structure']["paronyms"]:
                ind = dialogues_info['structure']["paronyms"].index(command)
                if ind + 1 == len(dialogues_info['structure']["paronyms"]):
                    self.user["passage_num"] = 0
                    self.user["room_num"] = 0
                    self.user['paronyms']['paronyms_step_num'] = 0
                    menu = Menu(self.res, self.req, self.user_id)
                    return menu.get_res()
                else:
                    self.user["room_num"] = ind + 1
                    if self.user['room_num'] == 1:
                        return self.get_res()
                    else:
                        return self.get_test_res(0)
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 1:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["paronyms"]['learn']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "далее":
                return self.get_res()
            elif command == 'в меню':
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_step_num'] = 0
                return self.get_menu()
            elif command == "в главное меню":
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 2:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["paronyms"]['test']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "в главное меню":
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_test_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif command == 'в меню':
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_test_step_num'] = 0
                return self.get_menu()
            elif command == "не могу отгадать":
                return self.get_test_res(1)
            elif command in self.user["paronyms"]['previous_test_list']:
                return self.get_test_res(2)
            else:
                return self.get_test_res(3)

    def get_incomprehension(self):
        self.res['response']['text'] = random.choice(dialogues_info["incomprehension"])
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res

    def get_res(self):
        if len(self.user["paronyms"]['list']) == 0:
            words = data["paronyms"][:]
            random.shuffle(words)
            self.user["paronyms"]['list'] = words
        self.user['paronyms']['paronyms_step_num'] += 1
        element = self.user["paronyms"]['list'].pop(0)
        text = random.choice(dialogues_info["paronyms_learn"][:]) + "\n\n"
        for i in list(element.keys()):
            text += "•" + i + " — " + element[i] + "\n\n"

        self.res['response']['text'] = text
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[1]
        return self.res

    def get_test_res(self, answer=0):
        def func(dont_know=False):
            if len(self.user["paronyms"]['test_list']) == 0:
                words = data["paronyms"][:]
                random.shuffle(words)
                self.user["paronyms"]['test_list'] = words
            self.user['paronyms']['paronyms_test_step_num'] += 1
            element = self.user["paronyms"]['test_list'].pop(0)
            variants = list(element.keys())
            random.shuffle(variants)
            text = random.choice(dialogues_info["paronyms_test"]).format(variants.pop(0))
            if dont_know:
                previous = 'Правильные варианты ответов:\n'
                for i in self.user["paronyms"]['previous_test_list']:
                    previous += "•" + i.capitalize() + '\n'
                text = previous + "\n" + text
            self.user["paronyms"]['previous_test_list'] = list(map(lambda x: x.lower(), variants))
            return text

        if answer == 0:
            text = func()
            self.res['response']['text'] = text
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        elif answer == 1:
            text = func(True)
            self.res['response']['text'] = text
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        elif answer == 2:
            text = func()
            self.res['response']['text'] = random.choice(dialogues_info['its_true']) + "\n\n" + text
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        else:
            self.res['response']['text'] = random.choice(dialogues_info["more_options"])
            self.user["previous_buttons"] = self.res['response']['buttons'] = [{"title": "Не могу отгадать",
                                                                                "hide": True}, {
                                                                                   "title": "В главное меню",
                                                                                   "hide": True
                                                                               }]

        return self.res

    def get_menu(self):
        self.res['response']['text'] = dialogues_info['info_for_menu']['paronyms']
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res


class Phraseologisms():
    def __init__(self, res, req, user_id):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.buttons = dialogues_info['buttons']["phraseologisms"][:]

    def sequence(self):
        command = self.req['request']["command"].strip().lower()
        if self.user["room_num"] == 0:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["phraseologisms"]['menu']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command in dialogues_info['structure']["phraseologisms"]:
                ind = dialogues_info['structure']["phraseologisms"].index(command)
                if ind + 1 == len(dialogues_info['structure']["phraseologisms"]):
                    self.user["passage_num"] = 0
                    self.user["room_num"] = 0
                    self.user['phraseologisms']['phraseologisms_step_num'] = 0
                    menu = Menu(self.res, self.req, self.user_id)
                    return menu.get_res()
                else:
                    self.user["room_num"] = ind + 1
                    return self.get_res()
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 1:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["phraseologisms"]['learn']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "далее":
                return self.get_res()
            elif command == 'в меню':
                self.user["room_num"] = 0
                self.user['phraseologisms']['phraseologisms_step_num'] = 0
                return self.get_menu()
            elif command == "в главное меню":
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['phraseologisms']['phraseologisms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            else:
                return self.get_incomprehension()

    def get_incomprehension(self):
        self.res['response']['text'] = random.choice(dialogues_info["incomprehension"])
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res

    def get_res(self):
        if len(self.user["phraseologisms"]['list']) == 0:
            words = data["phraseologisms"][:]
            random.shuffle(words)
            self.user["phraseologisms"]['list'] = words
        self.user['phraseologisms']['phraseologisms_step_num'] += 1
        card = self.user["phraseologisms"]['list'].pop(0)
        self.res['response']["card"] = {"type": "BigImage",
                                        "image_id": card["id"],
                                        "title": list(card.keys())[0],
                                        "description": card[list(card.keys())[0]],
                                        }
        self.res['response']['text'] = "*Вывожу карточку*"
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[1]

        return self.res

    def get_menu(self):
        self.res['response'][
            'text'] = dialogues_info['info_for_menu']['phraseologisms']
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[0]
        return self.res


class Buzzwords():
    def __init__(self, res, req, user_id):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.buttons = dialogues_info['buttons']["buzzwords"][:]

    def sequence(self):
        command = self.req['request']["command"].strip().lower()
        if self.user["room_num"] == 0:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["buzzwords"]['menu']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command in dialogues_info['structure']["buzzwords"]:
                ind = dialogues_info['structure']["buzzwords"].index(command)
                if ind + 1 == len(dialogues_info['structure']["buzzwords"]):
                    self.user["passage_num"] = 0
                    self.user["room_num"] = 0
                    self.user['buzzwords']['buzzword_step_num'] = 0
                    menu = Menu(self.res, self.req, self.user_id)
                    return menu.get_res()
                else:
                    self.user["room_num"] = ind + 1
                    return self.get_res()
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 1:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["buzzwords"]['learn']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "далее":
                return self.get_res()
            elif command == 'в меню':
                self.user["room_num"] = 0
                self.user['buzzwords']['buzzword_step_num'] = 0
                return self.get_menu()
            elif command == "в главное меню":
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['buzzwords']['buzzword_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            else:
                return self.get_incomprehension()

    def get_incomprehension(self):
        self.res['response']['text'] = random.choice(dialogues_info["incomprehension"])
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res

    def get_res(self):
        if len(self.user["buzzwords"]['list']) == 0:
            words = data["buzzwords"][:]
            random.shuffle(words)
            self.user["buzzwords"]['list'] = words
        self.user['buzzwords']['buzzword_step_num'] += 1
        card = self.user["buzzwords"]['list'].pop(0)
        self.res['response']["card"] = {"type": "BigImage",
                                        "image_id": card["id"],
                                        "title": list(card.keys())[0],
                                        "description": card[list(card.keys())[0]],
                                        }
        self.res['response']['text'] = "*Вывожу карточку*"
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[1]
        return self.res

    def get_menu(self):
        self.res['response']['text'] = dialogues_info['info_for_menu']['buzzwords']
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[0]
        return self.res


class Stupid_Dictionary():
    def __init__(self, res, req, user_id):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.buttons = dialogues_info['buttons']["stupid_dictionary"][:]

    def sequence(self):
        command = self.req['request']["command"].strip().lower()
        if self.user["room_num"] == 0:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["stupid_dictionary"]['menu']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command in dialogues_info['structure']["stupid_dictionary"]:
                ind = dialogues_info['structure']["stupid_dictionary"].index(command)
                if ind + 1 == len(dialogues_info['structure']["stupid_dictionary"]):

                    self.user["passage_num"] = 0
                    self.user["room_num"] = 0
                    self.user['stupid_dictionary']['stupid_dictionary_step_num'] = 0
                    menu = Menu(self.res, self.req, self.user_id)
                    return menu.get_res()
                else:
                    logging.info('pa1')
                    self.user["room_num"] = ind + 1
                    return self.get_res()
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 1:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["stupid_dictionary"]['learn']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "далее":
                return self.get_res()
            elif command == 'в меню':
                self.user["room_num"] = 0
                self.user['stupid_dictionary']['stupid_dictionary_step_num'] = 0
                return self.get_menu()
            elif command == "в главное меню":
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['stupid_dictionary']['stupid_dictionary_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            else:
                return self.get_incomprehension()

    def get_incomprehension(self):
        self.res['response']['text'] = random.choice(dialogues_info["incomprehension"])
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res

    def get_res(self):
        if len(self.user["stupid_dictionary"]['list']) == 0:
            words = data["stupid_dictionary"][:]
            random.shuffle(words)
            self.user["stupid_dictionary"]['list'] = words
        self.user['stupid_dictionary']['stupid_dictionary_step_num'] += 1
        ex = self.user["stupid_dictionary"]['list'].pop(0)
        self.res['response']['text'] = 'Слово: {}.\nМожет означать:\n{}'.format(list(ex.keys())[0],
                                                                                " ".join(
                                                                                    list(map(lambda x: (
                                                                                            " • " + x[:1].upper() + x[
                                                                                                                    1:] + "\n"),
                                                                                             ex[list(ex.keys())[0]]))))
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[1]
        return self.res

    def get_menu(self):
        self.res['response']['text'] = dialogues_info['info_for_menu']['stupid_dictionary']
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[0]
        return self.res


class Vocabulary_words():
    def __init__(self, res, req, user_id):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.buttons = dialogues_info['buttons']["vocabulary_words"][:]

    def sequence(self):
        command = self.req['request']["command"].strip().lower()
        if self.user["room_num"] == 0:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["vocabulary_words"]['menu']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command in dialogues_info['structure']["vocabulary_words"]:
                ind = dialogues_info['structure']["vocabulary_words"].index(command)
                if ind + 1 == len(dialogues_info['structure']["vocabulary_words"]):

                    self.user["passage_num"] = 0
                    self.user["room_num"] = 0
                    self.user['vocabulary_words']['vocabulary_words_step_num'] = 0
                    menu = Menu(self.res, self.req, self.user_id)
                    return menu.get_res()
                else:

                    self.user["room_num"] = ind + 1
                    if self.user['room_num'] == 1:
                        return self.get_res()
                    else:
                        return self.get_test_res(0)
            else:
                return self.get_incomprehension()

        elif self.user["room_num"] == 1:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["vocabulary_words"]['learn']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "далее":
                return self.get_res()
            elif command == 'в меню':
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_step_num'] = 0
                return self.get_menu()
            elif command == "в главное меню":
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 2:
            if command == "помощь":
                self.res['response']['text'] = dialogues_info["helps"]["vocabulary_words"]['test']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "повтори":
                self.res['response']['tts'] = self.user["vocabulary_words"]['previous_test_list'][0]
                self.res['response']['text'] = "..."
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "в главное меню":
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_test_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif command == 'в меню':
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_test_step_num'] = 0
                return self.get_menu()
            elif command == "не могу отгадать":
                return self.get_test_res(1)
            elif command in self.user["vocabulary_words"]['previous_test_list']:
                return self.get_test_res(2)
            else:
                return self.get_test_res(3)

    def get_incomprehension(self):
        self.res['response']['text'] = random.choice(dialogues_info["incomprehension"])
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res

    def get_res(self):
        if len(self.user["vocabulary_words"]['list']) == 0:
            words = data["vocabulary_words"][:]
            random.shuffle(words)
            self.user["vocabulary_words"]['list'] = words
        self.user['vocabulary_words']['vocabulary_words_step_num'] += 1
        self.res['response']['text'] = random.choice(dialogues_info["vocabulary_learn"]).format(
            self.user["vocabulary_words"]['list'].pop(0).capitalize())
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res

    def get_test_res(self, answer=0):

        def func(dont_know=False):
            if len(self.user["vocabulary_words"]['test_list']) == 0:
                words = data["vocabulary_words"][:]
                random.shuffle(words)
                self.user["vocabulary_words"]['test_list'] = words

            self.user['vocabulary_words']['vocabulary_words_test_step_num'] += 1
            element = self.user["vocabulary_words"]['test_list'].pop(0)
            template = random.choice(dialogues_info["vocabulary_test"])
            text = template[:].format("...")
            tts = template[:].format(element)
            if dont_know:
                previous = 'Правильное написание слова — \"{}\".\n'.format(
                    self.user["vocabulary_words"]['previous_test_list'][0].capitalize())
                text = previous + "\n" + text
            self.res['response']['tts'] = tts
            self.user["vocabulary_words"]['previous_test_list'] = [element]
            return text

        if answer == 0:
            text = func()
            self.res['response']['text'] = text
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        elif answer == 1:
            text = func(True)
            self.res['response']['text'] = text
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        elif answer == 2:
            text = func()
            self.res['response']['text'] = random.choice(dialogues_info['its_true']) + "\n\n" + text
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        else:
            self.res['response']['text'] = random.choice(dialogues_info["more_options"])
            self.user["previous_buttons"] = self.res['response']['buttons'] = [{"title": "Не могу отгадать",
                                                                                "hide": True},
                                                                               {"title": "Повтори",
                                                                                "hide": True}, {
                                                                                   "title": "В главное меню",
                                                                                   "hide": True
                                                                               }]
        return self.res

    def get_menu(self):
        self.res['response']['text'] = dialogues_info['info_for_menu']['vocabulary_words']
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res


class Menu():
    def __init__(self, res, req, user_id):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]

    def get_res(self):
        self.res['response']['text'] = dialogues_info['info_for_menu']['main']
        self.user["previous_buttons"] = self.res['response']['buttons'] = dialogues_info['buttons']["main"]
        return self.res
