from constants import data, sessionStorage, dialogues_info, logging
from helper import add_log_text
import random, string


def get_c_t(req):
    if req['request'].get("original_utterance"):
        command = req['request']["original_utterance"].strip().lower()
        tokens = req['request']['nlu']['tokens']
    else:
        command = req['request']["payload"]["text"]
        tokens = list(map(lambda x: x.lower(), req['request']["payload"]["text"].split()))
    return command, tokens


class Antonyms():
    def __init__(self, res, req, user_id, screen):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.buttons = dialogues_info['buttons']["antonyms"][:]
        self.screen = screen

    def sequence(self):
        command, tokens = get_c_t(self.req)
        if self.user["room_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["antonyms"]['menu']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["antonyms"]['menu']
                return self.res
            elif any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()

            elif any(word in tokens for word in ["изучить", "посмотреть", "изучить", "послушать", "прослушать"]):
                self.user["room_num"] = 1
                return self.get_res()
            elif any(word in tokens for word in ["игра", "мини", "угадай", "игрушка", "играем", "игру"]):
                self.user["room_num"] = 2
                return self.get_test_res(0)
            elif any(word in tokens for word in ["поехали", "давай", "начать", "начинаем", "старт", "стартуем"]):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = [
                        "Ты это... Определи что начинаем. Кнопки в помощь)",
                        "Ты это... Определ+и что начин+аем. Кн+опки в п+омощь)"]
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = [
                        "Ты это... Определи что начинаем. Игру или изучать?",
                        "Ты это... Определ+и что начин+аем. Игр+у или изуч+ать?"]
                return self.res
            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['antonyms']['menu']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['antonyms']['menu']
                add_log_text(command)
                return self.res

        elif self.user["room_num"] == 1:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["antonyms"]['learn']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["antonyms"]['learn']
                return self.res
            elif any(word in tokens for word in
                     ['включи', "включить", "открой", "запусти", "начни", "начать", "давай"]) and \
                    any(word in tokens for word in ["игра", "мини", "угадай", "игрушка", "играем", "игру", "играть"]):
                self.user["room_num"] = 2
                return self.get_test_res(0)

            elif any(word in tokens for word in dialogues_info["next"]):
                return self.get_res()
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "начало"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            elif command == 'в меню' or any(word in tokens for word in ["меню", "назад"]):
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_step_num'] = 0
                return self.get_menu()

            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['antonyms']['learn']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['antonyms']['learn']
                add_log_text(command)
                return self.res
        elif self.user["room_num"] == 2:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["antonyms"]['test']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["antonyms"]['test']
                return self.res
            elif (any(word in tokens for word in ["повторить", "повтори", "повтор"]) or (
                    "еще раз" in command)) and not self.screen:
                self.res['response']['text'] = self.user["antonyms"]['previous_test_list'][0]
                self.res['response']['tts'] = self.user["antonyms"]['previous_test_list'][0]
                return self.res
            elif any(word in tokens for word in
                     ['включи', "включить", "открой", "запусти", "начни", "начать", "давай"]) and \
                    any(word in tokens for word in ["изучать", "выучить", "осваивать"]):
                self.user["room_num"] = 1
                return self.get_res()
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "начало"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            elif command == 'в меню' or any(word in tokens for word in ["меню", "назад"]):
                self.user["room_num"] = 0
                self.user['antonyms']['antonyms_step_num'] = 0
                return self.get_menu()

            elif command == "не могу отгадать" or any(word in tokens for word in ["хз", "не"]):
                return self.get_test_res(1)
            elif command in self.user["antonyms"]['previous_test_list'][1]:
                return self.get_test_res(2)
            else:
                return self.get_test_res(3)

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
                for i in self.user["antonyms"]['previous_test_list'][1]:
                    previous += "•" + i.capitalize() + '\n'
                text = previous + "\n" + text
                tts = previous + "sil <[500]>" + tts

            self.user["antonyms"]['previous_test_list'] = ["Подбер+ите ант+оним к сл+ову " + list(element.keys())[0],
                                                           list(map(lambda x: x.lower(), variants))]
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
        if self.screen:
            self.res['response']['text'], self.res['response']['tts'] = \
                dialogues_info['info_for_menu']['antonyms']
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        else:
            self.res['response']['text'], self.res['response']['tts'] = \
                dialogues_info['info_for_menu_without_screen']['antonyms']
        return self.res


class Paronyms():
    def __init__(self, res, req, user_id, screen):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.buttons = dialogues_info['buttons']["paronyms"][:]
        self.screen = screen

    def sequence(self):
        command, tokens = get_c_t(self.req)
        if self.user["room_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["paronyms"][
                        'menu']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["paronyms"]['menu']
                return self.res

            elif any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            elif any(word in tokens for word in ["изучить", "посмотреть", "изучать", "послушать", "обучение"]):
                self.user["room_num"] = 1
                return self.get_res()
            elif any(word in tokens for word in ["игра", "мини", "подбери", "игрушка", "играем", "игру"]):
                self.user["room_num"] = 2
                return self.get_test_res(0)
            elif any(word in tokens for word in ["поехали", "давай", "начать", "начинаем", "старт", "стартуем"]):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = [
                        "Ты это... Определи что начинаем. Кнопки в помощь)",
                        "Ты это... Определ+и что начин+аем. Кн+опки в п+омощь)"]
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = [
                        "Ты это... Определи что начинаем. Игру или изучать?",
                        "Ты это... Определ+и что начин+аем. Игр+у или изуч+ать?"]
                return self.res
            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['paronyms']['menu']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['paronyms']['menu']
                add_log_text(command)
                return self.res
        elif self.user["room_num"] == 1:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["paronyms"]['learn']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["paronyms"]['learn']
                return self.res
            elif any(word in tokens for word in
                     ['включи', "включить", "открой", "запусти", "начни", "начать", "давай"]) and \
                    any(word in tokens for word in ["игра", "мини", "угадай", "игрушка", "играем", "игру", "играть"]):
                self.user["room_num"] = 2
                return self.get_test_res(0)
            elif any(word in tokens for word in dialogues_info["next"]):
                return self.get_res()
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "начало"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            elif command == 'в меню' or any(word in tokens for word in ["меню", "назад"]):
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_step_num'] = 0
                return self.get_menu()
            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['paronyms']['learn']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['paronyms']['learn']
                add_log_text(command)
                return self.res
        elif self.user["room_num"] == 2:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["paronyms"]['test']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["paronyms"]['test']
                return self.res
            elif (any(word in tokens for word in ["повторить", "повтори", "повтор"]) or (
                    "еще раз" in command)) and not self.screen:
                self.res['response']['text'] = self.user["paronyms"]['previous_test_list'][0]
                self.res['response']['tts'] = self.user["paronyms"]['previous_test_list'][0]
                return self.res
            elif any(word in tokens for word in
                     ['включи', "включить", "открой", "запусти", "начни", "начать", "давай"]) and \
                    any(word in tokens for word in ["изучать", "выучить", "осваивать"]):
                self.user["room_num"] = 1
                return self.get_res()
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "начало"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_test_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            elif command == 'в меню' or any(word in tokens for word in ["меню", "назад"]):
                self.user["room_num"] = 0
                self.user['paronyms']['paronyms_test_step_num'] = 0
                return self.get_menu()
            elif command == "не могу отгадать" or any(word in tokens for word in ["хз", "не"]):
                return self.get_test_res(1)
            elif command in self.user["paronyms"]['previous_test_list'][1]:
                return self.get_test_res(2)
            else:
                return self.get_test_res(3)

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
            tts += "•" + i + " — " + element[i] + "sil <[200]>"
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
                for i in self.user["paronyms"]['previous_test_list'][1]:
                    previous += "•" + i.capitalize() + '\n'
                text = previous + "\n" + text
                tts = previous + "sil <[500]>" + tts
            self.user["paronyms"]['previous_test_list'] = ["Какой пароним у слова " + word + "?",
                                                           list(map(lambda x: x.lower(), variants))]
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
        if self.screen:
            self.res['response']['text'], self.res['response']['tts'] = \
                dialogues_info['info_for_menu']['paronyms']
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        else:
            self.res['response']['text'], self.res['response']['tts'] = \
                dialogues_info['info_for_menu_without_screen']['paronyms']
        return self.res


class Phraseologisms():
    def __init__(self, res, req, user_id, screen):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.buttons = dialogues_info['buttons']["phraseologisms"][:]
        self.screen = screen

    def sequence(self):
        command, tokens = get_c_t(self.req)
        if self.user["room_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["phraseologisms"]['menu']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["phraseologisms"]['menu']
                return self.res

            elif any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['phraseologisms']['phraseologisms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            elif any(word in tokens for word in
                     ["изучить", "посмотреть", "поехали", "давай", "начать", "начинаем", "старт", "стартуем", "погнали",
                      "начинай", "да", "конечно", "послушать", "обучение"]):
                self.user["room_num"] = 1
                return self.get_res()
            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['phraseologisms']['menu']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['phraseologisms']['menu']
                add_log_text(command)
                return self.res
        elif self.user["room_num"] == 1:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["phraseologisms"]['learn']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["phraseologisms"]['learn']
                return self.res
            elif any(word in tokens for word in dialogues_info["next"]):
                return self.get_res()
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['phraseologisms']['phraseologisms_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['phraseologisms']['learn']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['phraseologisms']['learn']
                add_log_text(command)
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

        if self.screen:
            self.res['response']['text'], self.res['response']['tts'] = \
                dialogues_info['info_for_menu']['phraseologisms']
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[0]
        else:
            self.res['response']['text'], self.res['response']['tts'] = \
                dialogues_info['info_for_menu_without_screen']['phraseologisms']
        return self.res


class Buzzwords():
    def __init__(self, res, req, user_id, screen):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.buttons = dialogues_info['buttons']["buzzwords"][:]
        self.screen = screen

    def sequence(self):
        command, tokens = get_c_t(self.req)
        if self.user["room_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["buzzwords"]['menu']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["buzzwords"]['menu']
                return self.res
            elif any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['buzzwords']['buzzword_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            elif any(word in tokens for word in
                     ["изучить", "посмотреть", "поехали", "давай", "начать", "начинаем", "старт", "стартуем", "погнали",
                      "начинай", "послушать", "обучение", "да", "конечно", "играем"]):
                self.user["room_num"] = 1
                return self.get_res()
            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['buzzwords']['menu']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['buzzwords']['menu']
                add_log_text(command)
                return self.res
        elif self.user["room_num"] == 1:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["buzzwords"]['learn']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["buzzwords"]['learn']
                return self.res
            elif any(word in tokens for word in dialogues_info["next"]):
                return self.get_res()
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['buzzwords']['buzzword_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['buzzwords']['learn']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['buzzwords']['learn']
                add_log_text(command)
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
        if self.screen:
            self.res['response']['text'], self.res['response']['tts'] = \
                dialogues_info['info_for_menu']['buzzwords']
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[0]
        else:
            self.res['response']['text'], self.res['response']['tts'] = \
                dialogues_info['info_for_menu_without_screen']['buzzwords']
        return self.res


class Stupid_Dictionary():
    def __init__(self, res, req, user_id, screen):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.buttons = dialogues_info['buttons']["stupid_dictionary"][:]
        self.screen = screen

    def sequence(self):
        command, tokens = get_c_t(self.req)
        if self.user["room_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["stupid_dictionary"]['menu']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["stupid_dictionary"]['menu']
                return self.res

            elif any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['stupid_dictionary']['stupid_dictionary_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            elif any(word in tokens for word in
                     ["изучить", "посмотреть", "поехали", "давай", "начать", "начинаем", "старт", "стартуем", "погнали"
                                                                                                              "начинай",
                      "да", "конечно", "играем"]):
                self.user["room_num"] = 1
                return self.get_res()

            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['stupid_dictionary']['menu']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['stupid_dictionary']['menu']
                add_log_text(command)
                return self.res
        elif self.user["room_num"] == 1:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["stupid_dictionary"]['learn']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["stupid_dictionary"]['learn']
                return self.res
            elif any(word in tokens for word in dialogues_info["next"]):
                return self.get_res()
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['stupid_dictionary']['stupid_dictionary_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['stupid_dictionary']['learn']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['stupid_dictionary']['learn']
                add_log_text(command)
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
        if self.screen:
            self.res['response']['text'], self.res['response']['tts'] = \
                dialogues_info['info_for_menu']['stupid_dictionary']
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[0]
        else:
            self.res['response']['text'], self.res['response']['tts'] = \
                dialogues_info['info_for_menu_without_screen']['stupid_dictionary']
        return self.res


class Vocabulary_words():

    def __init__(self, res, req, user_id, screen):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.buttons = dialogues_info['buttons']["vocabulary_words"][:]
        self.screen = screen

    def sequence(self):
        command, tokens = get_c_t(self.req)
        if self.user["room_num"] == 0:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["vocabulary_words"][
                            'menu']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["vocabulary_words"]['menu']
                return self.res

            elif any(word in tokens for word in ["главное", "меню", "вернись", "назад"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            elif any(word in tokens for word in ["изучить", "посмотреть", "послушать", "обучение"]):
                self.user["room_num"] = 1
                return self.get_res_without_screen()
            elif any(word in tokens for word in ["игра", "мини", "угадай", "игрушка", "играем", "игру"]):
                self.user["room_num"] = 2
                if self.screen:
                    return self.get_test_res(0)
                else:
                    return self.get_test_res_without_screen(0)
            elif any(word in tokens for word in ["поехали", "давай", "начать", "начинаем", "старт", "стартуем"]):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = [
                        "Ты это... Определи что начинаем. Кнопки в помощь)",
                        "Ты это... Определ+и что начин+аем. Кн+опки в п+омощь)"]
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = [
                        "Ты это... Определи что начинаем. Игру или изучать?",
                        "Ты это... Определ+и что начин+аем. Игр+у или изуч+ать?"]
                return self.res

            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['vocabulary_words']['menu']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['vocabulary_words']['menu']
                add_log_text(command)
                return self.res
        elif self.user["room_num"] == 1:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["vocabulary_words"]['learn']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["vocabulary_words"]['learn']
                return self.res

            elif any(word in tokens for word in
                     ['включи', "включить", "открой", "запусти", "начни", "начать", "давай"]) and \
                    any(word in tokens for word in ["игра", "мини", "угадай", "игрушка", "играем", "игру", "играть"]):
                self.user["room_num"] = 2

                if self.screen:
                    return self.get_test_res(0)
                else:
                    return self.get_test_res_without_screen()
            elif any(word in tokens for word in dialogues_info["next"]):

                return self.get_res_without_screen()
            elif all(word in tokens for word in ["что", "означает"]):
                self.res['response']['text'] = "Открываю"
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "начало"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            elif command == 'в меню' or any(word in tokens for word in ["меню", "назад"]):
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_step_num'] = 0
                return self.get_menu()
            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['vocabulary_words']['learn']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['vocabulary_words']['learn']
                add_log_text(command)
                return self.res
        elif self.user["room_num"] == 2:
            if any(word in tokens for word in dialogues_info['is_help']):
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps"]["vocabulary_words"]['test']
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info["helps_without_screen"]["vocabulary_words"]['test']
                return self.res
            elif (any(word in tokens for word in ["повторить", "повтори", "повтор"]) or (
                    "еще раз" in command)) and not self.screen:

                self.res['response']['text'] = self.user["vocabulary_words"]['previous_test_list'][0]
                self.res['response']['tts'] = self.user["vocabulary_words"]['previous_test_list'][0]
                return self.res
            elif any(word in tokens for word in
                     ['включи', "включить", "открой", "запусти", "начни", "начать", "давай"]) and \
                    any(word in tokens for word in ["изучать", "выучить", "осваивать"]):
                self.user["room_num"] = 1
                if self.screen:
                    return self.get_res()
                else:
                    return self.get_res_without_screen()
            elif all(word in tokens for word in ["что", "означает"]):
                self.res['response']['text'] = "Открываю"
                self.res['response']['buttons'] = self.user["previous_buttons"]
                return self.res
            elif command == "в главное меню" or any(word in tokens for word in ["главное", "начало"]):
                self.user["passage_num"] = 0
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_test_step_num'] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen)
                return menu.get_res()
            elif command == 'в меню' or any(word in tokens for word in ["меню", "назад"]):
                self.user["room_num"] = 0
                self.user['vocabulary_words']['vocabulary_words_test_step_num'] = 0
                return self.get_menu()
            elif self.screen:
                if any(word in tokens for word in ["1", "однёрка", "один", "единица", "един"]):
                    return self.get_test_res(1)
                elif any(word in tokens for word in ["2", "два", "двойка", "коронная", "двоечка", "двояк", "где"]):
                    return self.get_test_res(2)
                else:
                    if self.screen:
                        self.res['response']['text'], self.res['response']['tts'] = \
                            dialogues_info['incomprehension']['vocabulary_words']['test']
                        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                            self.user["room_num"]]
                    else:
                        self.res['response']['text'], self.res['response']['tts'] = \
                            dialogues_info['incomprehension_without_screen']['vocabulary_words']['test']
                    add_log_text(command)
                    return self.res
            elif not self.screen:
                return self.get_test_res_without_screen(1, tokens, command)
            else:
                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension']['vocabulary_words']['test']
                    self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[
                        self.user["room_num"]]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = \
                        dialogues_info['incomprehension_without_screen']['vocabulary_words']['test']
                add_log_text(command)
                return self.res

    def get_test_res_without_screen(self, mode=0, tokens=[], command=""):
        if len(self.user["vocabulary_words"]['test_list']) == 0:
            words = data["vocabulary_words"][:]
            random.shuffle(words)
            self.user["vocabulary_words"]['test_list'] = words
        text, tts = "", ""
        word = self.user["vocabulary_words"]['test_list'].pop(0)
        temp = random.choice(dialogues_info['vocabulary_test_without_screen'][str(word[-1])])
        self.user['vocabulary_words']['vocabulary_words_test_step_num'] += 1

        random_letter = [word[-3], word[-2]][:]
        random.shuffle(random_letter)

        if mode == 1:
            if all(word in tokens for word in ["не", "знаю"]) \
                    or any(word in tokens for word in ["хз"]) \
                    or all(word in tokens for word in ["ума", "не", "приложу"]) \
                    or all(word in tokens for word in ["не", "шарю"]) \
                    or all(word in tokens for word in ["не", "могу", "отгадать"]):

                answer = self.user["vocabulary_words"]['previous_test_list'][1][0]
                mode_ = self.user["vocabulary_words"]['previous_test_list'][1][1]

                if mode_ == 0:
                    if any(word in tokens for word in ["1", "однёрка", "один", "единица", "един"]):
                        letter_text, letter_tts = self.check_letter(answer)
                        loss_ = random.choice(dialogues_info['loss_without_screen']['double']['double'])
                        text = loss_[0].format(l_1=letter_text) + "\n\n"
                        tts = loss_[0].format(l_1=letter_tts) + "sil <[400]>"

                    elif any(word in tokens for word in ["2", "два", "двойка", "коронная", "двоечка", "двояк", "где"]):
                        letter_text, letter_tts = self.check_letter(answer[:1])
                        loss_ = random.choice(dialogues_info['loss_without_screen']['double']["once"])
                        text = loss_[0].format(l_1=letter_text) + "\n\n"
                        tts = loss_[0].format(l_1=letter_tts) + "sil <[400]>"

                else:
                    letter_text, letter_tts = self.check_letter(answer)
                    true_ = random.choice(dialogues_info['loss_without_screen']['once'])
                    text = true_[0].format(l_1=letter_text) + "\n\n"
                    tts = true_[1].format(l_1=letter_tts) + "sil <[400]>"
            else:
                answer = self.user["vocabulary_words"]['previous_test_list'][1][0]
                mode_ = self.user["vocabulary_words"]['previous_test_list'][1][1]

                if mode_ == 0:
                    logging.info(tokens)
                    if any(word in tokens for word in ["одна", "один", "1", "ван"]):
                        if len(answer) == 1:
                            true_ = random.choice(dialogues_info['its_true'])
                            text = true_[0] + "\n\n"
                            tts = true_[1] + "sil <[400]>"
                        else:
                            letter_text, letter_tts = self.check_letter(answer[:1])
                            loss_ = random.choice(dialogues_info['loss_without_screen']['double']['double'])
                            text = loss_[0].format(l_1=letter_text) + "\n\n"
                            tts = loss_[0].format(l_1=letter_tts) + "sil <[400]>"
                    elif any(word in tokens for word in ["две", "два", "2", "ту"]):
                        if len(answer) == 2:
                            true_ = random.choice(dialogues_info['its_true'])
                            text = true_[0] + "\n\n"
                            tts = true_[1] + "sil <[400]>"
                        else:
                            letter_text, letter_tts = self.check_letter(answer[:1])
                            loss_ = random.choice(dialogues_info['loss_without_screen']['double']["once"])
                            text = loss_[0].format(l_1=letter_text) + "\n\n"
                            tts = loss_[0].format(l_1=letter_tts) + "sil <[400]>"
                    else:
                        self.res['response']['text'] = "Одна или две буквы?"
                        self.res['response']['tts'] = "Одн+а +или две б+уквы?"
                        return self.res
                else:
                    command = command.lower().strip()
                    command = command.translate(str.maketrans('', '', string.punctuation))

                    if any(word in answer for word in ["ъ", "ь", "ё", "е", "л", "щ", "а", "и"]):
                        variants = {"ъ": ["твердый знак", "ъ"], "ь": ["мягкий знак", "ь"], "ё": ["е", "ё", "йо"],
                                    "е": ["е", "ё", "ель"], "л": ["эль", "эл", "л"],
                                    "щ": ["ще", "ща", "щ", "щи", "че"],
                                    "а": ["да", "а"], "и": ["ип", "и"]}
                        list_answer = variants[answer]
                    else:
                        list_answer = [answer]

                    if command in list_answer:
                        true_ = random.choice(dialogues_info['its_true'])
                        text = true_[0] + "\n\n"
                        tts = true_[1] + "sil <[400]>"
                    elif (not (command in list_answer)) and (
                            len(command) == 1 or any(len(answ.split()) == 2 for answ in list_answer)):
                        if len(answer) == 2:
                            letter_text, letter_tts = self.check_letter(answer[:1])
                        else:
                            letter_text, letter_tts = self.check_letter(answer)
                        loss_ = random.choice(dialogues_info['loss_without_screen']['once'])
                        text = loss_[0].format(l_1=letter_text) + "\n\n"
                        tts = loss_[1].format(l_1=letter_tts) + "sil <[400]>"
                    else:
                        self.res['response']['text'] = "Назови только букву"
                        self.res['response']['tts'] = "Назов+и т+олько б+укву"
                        return self.res
        if word[-1] == 0:
            if len(random_letter[0]) == 1:
                letter_text, letter_tts = self.check_letter(random_letter[0])
                self.res['response']['text'] = text + temp[0].format(word=word[2], l_1=letter_text)
                self.res['response']['tts'] = tts + temp[0].format(word=word[1], l_1=letter_tts)
            else:
                letter_text, letter_tts = self.check_letter(random_letter[1])
                self.res['response']['text'] = text + temp[0].format(word=word[2], l_1=letter_text)
                self.res['response']['tts'] = tts + temp[0].format(word=word[1], l_1=letter_tts)
            tts_previous = "В слове {word} пишется две буквы sil <[300]> {l_1} sil <[200]> или одна?".format(
                word=word[1], l_1=letter_tts)
        else:
            letter_text_0, letter_tts_0 = self.check_letter(random_letter[0])
            letter_text_1, letter_tts_1 = self.check_letter(random_letter[1])
            self.res['response']['text'] = text + temp[0].format(word=word[2], l_1=letter_text_0,
                                                                 l_2=letter_text_1)
            self.res['response']['tts'] = tts + temp[0].format(word=word[1], l_1=letter_tts_0, l_2=letter_tts_1)
            tts_previous = "В слове {word} пишется буква sil <[300]> {l_1} sil <[300]> или sil <[300]> {l_2} ".format(
                word=word[1], l_1=letter_tts_0,
                l_2=letter_tts_1)
        self.user["vocabulary_words"]['previous_test_list'] = [tts_previous, [word[-3], word[-1]]]

        return self.res

    def check_letter(self, letter):
        lett = {'а': "+а", 'б': "бэ", 'в': "вэ", 'г': "гэ", 'д': "дэ", 'е': "+е", 'ё': "ё", 'ж': "жэ", 'з': "зэ",
                'и': "+и", 'й': "й краткое", 'к': "ка", 'л': "эль", 'м': "эм", 'н': "эн", 'о': "+о", 'п': "пэ",
                'р': "эр", 'с': "эс", 'т': "тэ", 'у': "у", 'ф': "эф", 'х': "ха", 'ц': "цэ", 'ч': "че", 'ш': "ша",
                'щ': "ща", 'ъ': "твёрдый знак", 'ы': "ы", 'ь': "мягкий знак", 'э': "э", 'ю': "ю", 'я': "+я"}
        return letter, lett[letter]

    def get_res_without_screen(self):

        if len(self.user["vocabulary_words"]['list']) == 0:
            words = data["vocabulary_words"][:]
            random.shuffle(words)
            self.user["vocabulary_words"]['list'] = words
        self.user['vocabulary_words']['vocabulary_words_step_num'] += 1

        word = self.user["vocabulary_words"]['list'].pop(0)
        word_text = word[0]
        word_tts = word[1]
        true_letter = word[-3]
        sil = 50
        if word[-1] == 0:
            if len(word[-3]) == 1:

                letter_text, letter_tts = self.check_letter(true_letter)
                temp = random.choice(dialogues_info["vocabulary_learn_without_screen"]["0"]['one'])
                self.res['response']['text'] = temp[0].format(word=word_text, l_=letter_text.upper())
                self.res['response']['tts'] = temp[1].format(sil=sil, word=word_tts, l_=letter_tts)
            else:
                letter_text, letter_tts = self.check_letter(true_letter[:1])

                temp = random.choice(dialogues_info["vocabulary_learn_without_screen"]["0"]['two'])
                self.res['response']['text'] = temp[0].format(word=word_text, l_=letter_text.upper())
                self.res['response']['tts'] = temp[1].format(sil=sil, word=word_tts, l_=letter_tts)
        else:
            letter_text, letter_tts = self.check_letter(true_letter)
            temp = random.choice(dialogues_info["vocabulary_learn_without_screen"][str(word[-1])])
            self.res['response']['text'] = temp[0].format(word=word_text, l_=letter_text.upper())
            self.res['response']['tts'] = temp[1].format(sil=sil, word=word_tts, l_=letter_tts)

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
        buttons = self.res['response']['buttons'][:]
        buttons.insert(1, {
            "title": "Что означает это слово?",
            "url": "https://yandex.ru/search?text=Что%20означает%20слово%20{}%20?".format(word[0]),
            "hide": True
        })
        self.res['response']['buttons'] = buttons
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

            self.res['response']['text'] = temp[0].format(word[2]) + "1) " + check_words[0] + " \n2) " + check_words[1]
            self.res['response']['tts'] = temp[0].format(word[1])

        else:
            check_list = self.user["vocabulary_words"]['previous_test_list']
            if check_list[0].strip().lower() == check_list[1][mode - 1].strip().lower():
                true_ = random.choice(dialogues_info['its_true'])

                self.res['response']['text'] = true_[0] + "\n\n" + temp[0].format(word[2]) + "1) " + check_words[
                    0] + " \n2) " + check_words[1]
                self.res['response']['tts'] = true_[1] + " " + temp[
                    1].format(
                    word[1])

            else:
                no = random.choice(dialogues_info['false'])
                previous = 'Правильное написание слова — \"{}\".\n'.format(check_list[0])
                previous_tts = 'Правильное написание сл+ова — \"{}\".\n'.format(check_list[0])
                self.res['response']['text'] = no[0] + previous + "\n\n" + temp[0].format(word[2]) + "1) " + \
                                               check_words[0] + "\n2)" + check_words[1]
                self.res['response']['tts'] = no[1] + previous_tts + " " + temp[1].format(
                    word[1])

        self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        self.user["vocabulary_words"]['previous_test_list'] = [word[0], check_words]
        buttons = self.res['response']['buttons'][:]
        buttons.insert(2, {
            "title": "Что означает это слово?",
            "url": "https://yandex.ru/search?text=Что%20означает%20слово%20{}%20?".format(word[0]),
            "hide": True
        })
        self.res['response']['buttons'] = buttons
        return self.res

    def get_menu(self):
        if self.screen:
            self.res['response']['text'], self.res['response']['tts'] = \
                dialogues_info['info_for_menu']['vocabulary_words']
            self.user["previous_buttons"] = self.res['response']['buttons'] = self.buttons[self.user["room_num"]]
        else:
            self.res['response']['text'], self.res['response']['tts'] = \
                dialogues_info['info_for_menu_without_screen']['vocabulary_words']
        return self.res


class Menu():
    def __init__(self, res, req, user_id, screen, new=False):
        self.res = res
        self.req = req
        self.user_id = user_id
        self.user = sessionStorage[user_id]
        self.new = new
        self.screen = screen

    def get_res(self, mode=0, ttext=""):
        if not ttext:
            if self.new:

                if self.screen:
                    if self.user['first_help']:
                        self.res['response']['text'] = dialogues_info['hello_menu']["new"][0]
                        self.res['response']['tts'] = dialogues_info['hello_menu']["new"][1]
                        self.user['first_help'] = False
                        logging.info(2)
                    else:
                        temp = random.choice(dialogues_info['hello_menu']["old"])
                        self.res['response']['text'] = temp[0]
                        self.res['response']['tts'] = temp[1]

                    self.res['response']["card"] = dialogues_info["icon_menu"][mode]
                    self.res['response']["card"]['header']['text'] = self.res['response']['text']
                else:

                    if self.user['first_help']:
                        self.res['response']['text'] = dialogues_info['hello_menu_without_screen']["new"][0]
                        self.res['response']['tts'] = dialogues_info['hello_menu_without_screen']["new"][1]
                        self.user['first_help'] = False
                    else:
                        temp = random.choice(dialogues_info['hello_menu_without_screen']["old"])
                        self.res['response']['text'] = temp[0]
                        self.res['response']['tts'] = temp[1]
            else:
                if self.screen:
                    temp = random.choice(dialogues_info['info_for_menu']['main'])
                    self.res['response']['text'] = temp[0]
                    self.res['response']['tts'] = temp[1]
                    self.res['response']["card"] = dialogues_info["icon_menu"][mode]
                    self.res['response']["card"]['header']['text'] = self.res['response']['text']
                else:
                    temp = random.choice(dialogues_info['info_for_menu_without_screen']['main'])
                    self.res['response']['text'] = temp[0]
                    self.res['response']['tts'] = temp[1]
        else:
            self.res['response']['text'] = ttext[0]
            self.res['response']['tts'] = ttext[1]
            self.res['response']["card"] = dialogues_info["icon_menu"][mode]
            self.res['response']["card"]['header']['text'] = self.res['response']['text']

        self.user["previous_buttons"] = self.res['response']['buttons'] = [{
            "title": "Что ты умеешь?",
            "hide": True
        },
            {
                "title": "Помощь",
                "hide": True
            }]

        return self.res
