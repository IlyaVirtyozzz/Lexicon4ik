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
        command = self.req['request']["original_utterance"].strip().lower()
        tokens = self.req['request']['nlu']['tokens']
        if self.user["room_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["antonyms"]['menu']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in ["поехали", "давай", "начать", "начинаем", "старт", "стартуем"]):
                self.res['response']['text'], self.res['response']['tts'] = [
                    "Ты это... Определи что начинаем. Кнопки в помощь)",
                    "Ты это... Определ+и что начин+аем. Кн+опки в п+омощь)"]
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()

            elif any(word in tokens for word in ["изучить", "посмотреть"]):
                self.user["room_num"] = 1
                return self.get_res()
            elif any(word in tokens for word in ["игра", "мини", "угадай", "игрушка"]):
                self.user["room_num"] = 2
                return self.get_test_res(0)
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 1:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["antonyms"]['learn']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in
                     ["далее", "дальше", "следующая", "следующее", "следующий", "дарья", "да"]):
                return self.get_res()
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "начало"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif command == 'в меню' or any(word in tokens for word in ["меню", "назад"]):
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_step_num'] = 0
                return self.get_menu()

            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 2:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["antonyms"]['test']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "начало"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif command == 'в меню' or any(word in tokens for word in ["меню", "назад"]):
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_step_num'] = 0
                return self.get_menu()
            elif command == "не могу отгадать" or any(word in tokens for word in ["хз", "не"]):
                return self.get_test_res(1)
            elif command in self.user["antonyms"]['previous_test_list']:
                return self.get_test_res(2)
            else:
                return self.get_test_res(3)

    def get_incomprehension(self):
        self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info["incomprehension"])
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
            tts = ""
            for i in element[list(element.keys())[0]]:
                text += "•" + i.capitalize() + "\n"
                tts += "•" + i.capitalize() + "\n"
            temp = random.choice(dialogues_info["аntonyms_learn"]["many"])
            text = temp[0].format(list(element.keys())[0], text)
            tts = temp[1].format(list(element.keys())[0], tts)
        else:
            temp = random.choice(dialogues_info["аntonyms_learn"]["one"])
            text = temp[0].format(list(element.keys())[0], element[list(element.keys())[0]][0])
            tts = temp[1].format(list(element.keys())[0], element[list(element.keys())[0]][0])

        self.res['response']['text'] = text
        self.res['response']['tts'] = tts
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
            temp = random.choice(dialogues_info["antonyms_test"])
            text = temp[0].format(list(element.keys())[0])
            tts = temp[1].format(list(element.keys())[0])
            if dont_know:
                previous = 'Правильные варианты ответов:\n'
                for i in self.user["antonyms"]['previous_test_list']:
                    previous += "•" + i.capitalize() + '\n'
                text = previous + "\n" + text
                tts = previous + "sil <[500]>" + tts

            self.user["antonyms"]['previous_test_list'] = list(map(lambda x: x.lower(), variants))
            return [text, tts]

        if answer == 0:
            self.res['response']['text'], self.res['response']['tts'] = func()
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        elif answer == 1:
            self.res['response']['text'], self.res['response']['tts'] = func(True)
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        elif answer == 2:
            text, tts = func()
            true_ = random.choice(dialogues_info['its_true'])
            self.res['response']['text'] = true_[0] + "\n\n" + text
            self.res['response']['tts'] = true_[1] + "\n\n" + tts
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        else:
            self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info["more_options"])
            self.user["previous_buttons"] = self.res['response']['buttons'] = [{"title": "Не могу отгадать",
                                                                                "hide": True}, {
                                                                                   "title": "В главное меню",
                                                                                   "hide": True
                                                                               }, {
                                                                                   "title": "Помощь",
                                                                                   "hide": True
                                                                               }]

        return self.res

    def get_menu(self):
        self.res['response']['text'], self.res['response']['tts'] = dialogues_info['info_for_menu']['antonyms']
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
        command = self.req['request']["original_utterance"].strip().lower()
        tokens = self.req['request']['nlu']['tokens']
        if self.user["room_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["paronyms"]['menu']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in ["поехали", "давай", "начать", "начинаем", "старт", "стартуем"]):
                self.res['response']['text'], self.res['response']['tts'] = [
                    "Ты это... Определи что начинаем. Кнопки в помощь)",
                    "Ты это... Определ+и что начин+аем. Кн+опки в п+омощь)"]
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif any(word in tokens for word in ["изучить", "посмотреть"]):
                self.user["room_num"] = 1
                return self.get_res()
            elif any(word in tokens for word in ["игра", "мини", "подбери", "игрушка"]):
                self.user["room_num"] = 2
                return self.get_test_res(0)
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 1:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["paronyms"]['learn']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in
                     ["далее", "дальше", "следующая", "следующее", "следующий", "дарья", "да"]):
                return self.get_res()
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "начало"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif command == 'в меню' or any(word in tokens for word in ["меню", "назад"]):
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_step_num'] = 0
                return self.get_menu()
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 2:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["paronyms"]['test']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "начало"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_test_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif command == 'в меню' or any(word in tokens for word in ["меню", "назад"]):
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_test_step_num'] = 0
                return self.get_menu()
            elif command == "не могу отгадать" or any(word in tokens for word in ["хз", "не"]):
                return self.get_test_res(1)
            elif command in self.user["paronyms"]['previous_test_list']:
                return self.get_test_res(2)
            else:
                return self.get_test_res(3)

    def get_incomprehension(self):
        self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info["incomprehension"])
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res

    def get_res(self):
        if len(self.user["paronyms"]['list']) == 0:
            words = data["paronyms"][:]
            random.shuffle(words)
            self.user["paronyms"]['list'] = words
        self.user['paronyms']['paronyms_step_num'] += 1
        element = self.user["paronyms"]['list'].pop(0)
        temp = random.choice(dialogues_info["paronyms_learn"])
        text = temp[0] + "\n\n"
        tts = temp[1]
        for i in list(element.keys()):
            text += "•" + i + " — " + element[i] + "\n\n"
            tts += "•" + i + " — " + element[i]
        self.res['response']['text'], self.res['response']['tts'] = text, tts
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
            temp = random.choice(dialogues_info["paronyms_test"])
            word = variants.pop(0)
            text = temp[0].format(word)
            tts = temp[1].format(word)
            if dont_know:
                previous = 'Правильные варианты ответов:\n'
                for i in self.user["paronyms"]['previous_test_list']:
                    previous += "•" + i.capitalize() + '\n'
                text = previous + "\n" + text
                tts = previous + "sil <[500]>" + tts
            self.user["paronyms"]['previous_test_list'] = list(map(lambda x: x.lower(), variants))
            return [text, tts]

        if answer == 0:
            self.res['response']['text'], self.res['response']['tts'] = func()
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        elif answer == 1:
            self.res['response']['text'], self.res['response']['tts'] = func(True)
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        elif answer == 2:
            text, tts = func()
            true_ = random.choice(dialogues_info['its_true'])
            self.res['response']['text'] = true_[0] + "\n\n" + text
            self.res['response']['tts'] = true_[1] + tts
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        else:
            self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info["more_options"])
            self.user["previous_buttons"] = self.res['response']['buttons'] = [{"title": "Не могу отгадать",
                                                                                "hide": True}, {
                                                                                   "title": "В главное меню",
                                                                                   "hide": True
                                                                               }, {
                                                                                   "title": "Помощь",
                                                                                   "hide": True
                                                                               }]

        return self.res

    def get_menu(self):
        self.res['response']['text'], self.res['response']['tts'] = dialogues_info['info_for_menu']['paronyms']
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
        command = self.req['request']["original_utterance"].strip().lower()
        tokens = self.req['request']['nlu']['tokens']
        if self.user["room_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["phraseologisms"][
                    'menu']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res

            elif any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['phraseologisms']['phraseologisms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif any(word in tokens for word in
                     ["изучить", "посмотреть", "поехали", "давай", "начать", "начинаем", "старт", "стартуем"]):
                self.user["room_num"] = 1
                return self.get_res()
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 1:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["phraseologisms"][
                    'learn']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in
                     ["далее", "дальше", "следующая", "следующее", "следующий", "дарья", "да"]):
                return self.get_res()
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['phraseologisms']['phraseologisms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            else:
                return self.get_incomprehension()

    def get_incomprehension(self):
        self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info["incomprehension"])
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
        self.res['response']['text'] = list(card.keys())[0] + ". " + card[list(card.keys())[0]]
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[1]

        return self.res

    def get_menu(self):
        self.res['response']['text'], self.res['response']['tts'] = dialogues_info['info_for_menu']['phraseologisms']
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
        command = self.req['request']["original_utterance"].strip().lower()
        tokens = self.req['request']['nlu']['tokens']
        if self.user["room_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["buzzwords"]['menu']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['buzzwords']['buzzword_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif any(word in tokens for word in
                     ["изучить", "посмотреть", "поехали", "давай", "начать", "начинаем", "старт", "стартуем"]):
                self.user["room_num"] = 1
                return self.get_res()
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 1:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["buzzwords"][
                    'learn']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in
                     ["далее", "дальше", "следующая", "следующее", "следующий", "дарья", "да"]):
                return self.get_res()
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['buzzwords']['buzzword_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            else:
                return self.get_incomprehension()

    def get_incomprehension(self):
        self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info["incomprehension"])
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
        self.res['response']['text'] = list(card.keys())[0] + "sil <[500]>" + card[list(card.keys())[0]]
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[1]
        return self.res

    def get_menu(self):
        self.res['response']['text'], self.res['response']['tts'] = dialogues_info['info_for_menu']['buzzwords']
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
        command = self.req['request']["original_utterance"].strip().lower()
        tokens = self.req['request']['nlu']['tokens']
        if self.user["room_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = \
                    dialogues_info["helps"]["stupid_dictionary"]['menu']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res

            elif any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['stupid_dictionary']['stupid_dictionary_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif any(word in tokens for word in
                     ["изучить", "посмотреть", "поехали", "давай", "начать", "начинаем", "старт", "стартуем"]):
                self.user["room_num"] = 1
                return self.get_res()

            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 1:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = \
                    dialogues_info["helps"]["stupid_dictionary"]['learn']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in
                     ["далее", "дальше", "следующая", "следующее", "следующий", "дарья", "да"]):
                return self.get_res()
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['stupid_dictionary']['stupid_dictionary_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            else:
                return self.get_incomprehension()

    def get_incomprehension(self):
        self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info["incomprehension"])
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
        self.res['response']['text'], self.res['response']['tts'] = dialogues_info['info_for_menu']['stupid_dictionary']
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
        command = self.req['request']["original_utterance"].strip().lower()
        tokens = self.req['request']['nlu']['tokens']
        if self.user["room_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'] = dialogues_info["helps"]["vocabulary_words"]['menu']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in ["поехали", "давай", "начать", "начинаем", "старт", "стартуем"]):
                self.res['response']['text'], self.res['response']['tts'] = [
                    "Ты это... Определи что начинаем. Кнопки в помощь)",
                    "Ты это... Определ+и что начин+аем. Кн+опки в п+омощь)"]
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif any(word in tokens for word in ["изучить", "посмотреть"]):
                self.user["room_num"] = 1
                return self.get_res()
            elif any(word in tokens for word in ["игра", "мини", "угадай", "игрушка"]):
                self.user["room_num"] = 2
                return self.get_test_res(0)

            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 1:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["vocabulary_words"][
                    'learn']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif any(word in tokens for word in
                     ["далее", "дальше", "следующая", "следующее", "следующий", "дарья", "да"]):
                return self.get_res()

            elif command == "в главное меню" or any(word in tokens for word in ["главное", "начало"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif command == 'в меню' or any(word in tokens for word in ["меню", "назад"]):
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_step_num'] = 0
                return self.get_menu()
            else:
                return self.get_incomprehension()
        elif self.user["room_num"] == 2:
            if any(word in tokens for word in dialogues_info['is_help']):
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["vocabulary_words"][
                    'test']
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res

            elif command == "в главное меню" or any(word in tokens for word in ["главное", "начало"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_test_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id)
                return menu.get_res()
            elif command == 'в меню' or any(word in tokens for word in ["меню", "назад"]):
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_test_step_num'] = 0
                return self.get_menu()
            elif any(word in tokens for word in ["1", "однёрка", "один", "единица", "един"]):
                return self.get_test_res(1)
            elif any(word in tokens for word in ["2", "два", "двойка", "двоечка", "коронная", "двояк"]):
                return self.get_test_res(2)
            else:
                return self.get_incomprehension()

    def get_incomprehension(self):
        self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info["incomprehension"])
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res

    def get_res(self):
        if len(self.user["vocabulary_words"]['list']) == 0:
            words = data["vocabulary_words"][:]
            random.shuffle(words)
            self.user["vocabulary_words"]['list'] = words
        self.user['vocabulary_words']['vocabulary_words_step_num'] += 1
        temp = random.choice(dialogues_info["vocabulary_learn"])
        word = self.user["vocabulary_words"]['list'].pop(0)
        self.res['response']['text'] = temp[0].format(word[0].capitalize())
        self.res['response']['tts'] = temp[1].format(word[1].capitalize())
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res

    def get_test_res(self, mode=0):

        if len(self.user["vocabulary_words"]['test_list']) == 0:
            words = data["vocabulary_words"][:]
            random.shuffle(words)
            self.user["vocabulary_words"]['test_list'] = words
        word = self.user["vocabulary_words"]['test_list'].pop(0)
        temp = random.choice(dialogues_info["vocabulary_test"])
        check_words = [word[2].replace("*", word[3].strip().upper()), word[2].replace("*", word[4].strip().upper())]
        random.shuffle(check_words)
        self.user['vocabulary_words']['vocabulary_words_test_step_num'] += 1

        if mode == 0:

            self.res['response']['text'] = temp[0].format("1) " + check_words[0] + " \n2) " + check_words[1])
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]

        else:
            check_list = self.user["vocabulary_words"]['previous_test_list']
            if check_list[0].strip().lower() == check_list[1][mode - 1].strip().lower():
                true_ = random.choice(dialogues_info['its_true'])

                self.res['response']['text'] = true_[0] + "\n\n" + temp[0].format(
                    "1) " + check_words[0] + " \n2) " + check_words[1])
                self.res['response']['tts'] = true_[1] + " " + temp[1].format(
                    "1) " + check_words[0] + " \n2) " + check_words[1])

            else:
                no = random.choice(dialogues_info['false'])
                previous = 'Правильное написание слова — \"{}\".\n'.format(check_list[0])
                previous_tts = 'Правильное написание сл+ова — \"{}\".\n'.format(check_list[0])

                self.res['response']['text'] = no[0] + previous + "\n\n" + temp[0].format(
                    "1) " + check_words[0] + " \n2) " + check_words[1])
                self.res['response']['tts'] = no[1] + previous_tts + " " + temp[1].format(
                    "1) " + check_words[0] + " \n2) " + check_words[1])

            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        self.user["vocabulary_words"]['previous_test_list'] = [word[0], check_words]
        return self.res

    def get_menu(self):
        self.res['response']['text'], self.res['response']['tts'] = dialogues_info['info_for_menu']['vocabulary_words']
        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        return self.res


class Menu():
    def __init__(self, res, req, user_id, new=False):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.new = new

    def get_res(self):
        if self.new:
            self.res['response']['text'] = "Привет! " + dialogues_info['info_for_menu']['main'][0]
            self.res['response']['tts'] = "Привет! " + dialogues_info['info_for_menu']['main'][1]
        else:
            self.res['response']['text'] = dialogues_info['info_for_menu']['main'][0]
            self.res['response']['tts'] = dialogues_info['info_for_menu']['main'][1]

        self.user["previous_buttons"] = self.res['response']['buttons'] = dialogues_info['buttons']["main"]
        return self.res
