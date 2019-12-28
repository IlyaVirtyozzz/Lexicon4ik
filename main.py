import random
from helper import add_log_text
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
        self.payload = False

    def if_not_in_base(self):
        self.user = sessionStorage[self.user_id] = {"passage_num": 0, "room_num": 0, "previous_buttons": [],
                                                    "pls_like": False,
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

    def if_new_session(self):
        if not self.user:
            self.if_not_in_base()
        self.user["passage_num"] = 0
        self.user["room_num"] = 0

    def start(self):
        if self.req['session']['new']:
            self.if_new_session()
            menu = Menu(self.res, self.req, self.user_id, True)
            self.res = menu.get_res()
        else:
            if not self.user:
                self.if_new_session()
            self.check_answer()

    def check_can(self):
        if 'умеешь' in list(map(lambda x: x.lower(), self.req['request']['nlu']["tokens"])):
            return True
        return False

    def check_answer(self):

        if self.req['request'].get("original_utterance"):
            command = self.req['request']["original_utterance"].strip().lower()
            tokens = self.req['request']['nlu']['tokens']

        else:
            command = self.req['request']["payload"]["text"]
            tokens = list(map(lambda x: x.lower(), self.req['request']["payload"]["text"].split()))
            self.payload = True

        if not self.payload:
            if self.check_can():
                self.res['response']['text'], self.res['response']['tts'] = dialogues_info["ican"]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif all(word in tokens for word in ["как", "дела"]) or all(
                    word in tokens for word in ["как", "настроение"]):
                self.res['response']['text'], self.res['response']['tts'] = [
                    "Нормально, нормально нереально, не будем тратить время на житейские разговоры, приступим к делу.",
                    "Норм+ально, норм+ально нере+ально,"
                    " не б+удем тр+атить вр+емя на жит+ейские разгов+оры, прист+упим к д+елу."]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif all(word in tokens for word in ["оценить", "навык"]):
                self.res['response']['text'], self.res['response']['tts'] = [
                    "Благодарю Тебя.",
                    "Благодар+ю Теб+я."]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif any(word in tokens for word in ["спасибо", "благодарю", "сенкс"]):
                self.res['response']['text'], self.res['response']['tts'] = ["Тебе спасибо, что зашёл)",
                                                                             "Тебе спас+ибо, что заш+ёл"]
                self.res['response']['buttons'] = self.user["previous_buttons"]
                self.user['pls_like'] = True
                buttons = self.res['response']['buttons'][:]
                buttons.insert(0, {
                    "title": "Оценить навык",
                    "url": "https://dialogs.yandex.ru/store/skills/376e3bb3-prokachaj-leksiko",
                    "hide": True
                })
                self.res['response']['buttons'] = buttons

            elif all(word in tokens for word in ["как", "это"]) or all(
                    word in tokens for word in ["почему", "так"]) or all(
                word in tokens for word in ["почему", "это"]):
                self.res['response']['text'], self.res['response']['tts'] = ["Вот так вот)",
                                                                             "Вот так вот"]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif any(word in tokens for word in ["алиса", "alice", "алис"]):
                self.res['response']['text'], self.res['response']['tts'] = [
                    "Ой. Я не Алиса. Можно сказать, я её друг.",
                    "Ой. Я не Ал+иса. Можно сказ+ать, я её др+уг."]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif any(word in tokens for word in dialogues_info['is_hello']):
                self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info['hello'])
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif all(word in tokens for word in ["ты", "кто"]):
                self.res['response']['text'], self.res['response']['tts'] = [
                    "Я тот кто может научить Тебя полезным словам)",
                    "Я тот кто м+ожет науч+ить Теб+я пол+езным слов+ам)"]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif all(word in tokens for word in ["ты", "мальчик"]):
                self.res['response']['text'], self.res['response']['tts'] = [
                    "Скорее всего, я навык мужского пола. Увы, так исторически сложилось.",
                    "Скор+ее вс+его, я н+авык мужск+ого п+ола. Ув+ы, так истор+ически слож+илось."]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif all(word in tokens for word in ["как", "приложение", "называется"]) or all(
                    word in tokens for word in ["как", "навык", "называется"]):
                self.res['response']['text'], self.res['response']['tts'] = [
                    "\"Прокачай Лексикон\" По-моему звучит прикольно)",
                    "\"Прокач+ай Лексик+он\" По-м+оему звуч+ит прик+ольно!)"]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif all(word in tokens for word in ["ау", "эй", "уау"]):
                self.res['response']['text'], self.res['response']['tts'] = [
                    "Да-да, я здесь.",
                    "Да-да, я зд+есь."]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif any(word in tokens for word in dialogues_info['is_bye']):
                self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info['bye'])
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif any(word in command.split() for word in dialogues_info['fuck_words']):
                self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info["fuck_answer"])
                self.res['response']['buttons'] = self.user["previous_buttons"]
                add_log_text(command)

            elif all(word in tokens for word in ["как", "тебя", "зовут"]) or all(
                    word in tokens for word in ["как", "вас", "зовут"]):
                self.res['response']['text'], self.res['response']['tts'] = ["Сам прихожу. А так, имени у меня нет)",
                                                                             "Сам прихож+у. А т+ак, +имени у мен+я н+ет)"]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif any(word in tokens for word in ["ясно", "понятно"]):
                self.res['response']['text'], self.res['response']['tts'] = ["Хе-хе",
                                                                             "Хе-хе"]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif self.user["passage_num"] == 0:
                if any(word in tokens for word in dialogues_info['is_help']):
                    self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["main"]
                    self.res['response']['buttons'] = self.user["previous_buttons"]

                elif any(word in tokens for word in
                         ["поехали", "давай", "начать", "начинаем", "старт", "стартуем", "да", "погнали"]):
                    self.res['response']['text'], self.res['response']['tts'] = [
                        "Поехали! Ой, выбери сначала категорию.",
                        "По+ехали! Ой,sil <[200]> в+ыбери снач+ала катег+орию."]
                    self.res['response']['buttons'] = self.user["previous_buttons"]

                elif any(word in tokens for word in
                         ["категория", "категории", "категорий"]):
                    self.res['response']['text'], self.res['response']['tts'] = [
                        "Выбери категорию с помощью кнопок на панели.",
                        "В+ыбери катег+орию с п+омощью кн+опок на пан+ели."]
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                elif any(word in tokens for word in
                         ["меню", "главное"]):
                    self.res['response']['text'], self.res['response']['tts'] = ["Ты и так уже здесь.",
                                                                                 "Ты и так уже зд+есь."]
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                    menu = Menu(self.res, self.req, self.user_id, False)
                    self.res = menu.get_res(0, ["Ты и так уже здесь.",
                                                "Ты и так уже зд+есь."])
                elif any(word in tokens for word in ["интересные"]):
                    self.user["passage_num"] = 1
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                    self.res = a.get_menu()
                elif any(word in tokens for word in ["словарные", "словарная", "сс", "словарь", "словарный"]):
                    self.user["passage_num"] = 2
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                    self.res = a.get_menu()
                elif any(word in tokens for word in ["фразеологизмы", "фразеологизм"]):
                    self.user["passage_num"] = 3
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                    self.res = a.get_menu()
                elif any(word in tokens for word in ["антоним", "антонимы", "антон"]):
                    self.user["passage_num"] = 4
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                    self.res = a.get_menu()
                elif any(word in tokens for word in ["пароним", "парон", "парные", "паронимы"]):
                    self.user["passage_num"] = 5
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                    self.res = a.get_menu()
                elif any(word in tokens for word in ["глупые", "бестолковые"]):
                    self.user["passage_num"] = 6
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                    self.res = a.get_menu()
                else:
                    self.res['response']['text'], self.res['response']['tts'] = random.choice(
                        dialogues_info["incomprehension"])
                    add_log_text(command)
                    self.user["previous_buttons"] = self.res['response']['buttons'] = [{
                        "title": "Что ты умеешь?",
                        "hide": True
                    }, {
                        "title": "Помощь",
                        "hide": True
                    }]
            else:
                self.mains_passage[self.user["passage_num"]]()
        else:
            self.user["room_num"] = 0
            if any(word in tokens for word in ["интересные"]):
                self.user["passage_num"] = 1
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                self.res = a.get_menu()
            elif any(word in tokens for word in ["словарные", "словарная", "сс", "словарь", "словарный"]):
                self.user["passage_num"] = 2
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                self.res = a.get_menu()
            elif any(word in tokens for word in ["фразеологизмы", "фразеологизм"]):
                self.user["passage_num"] = 3
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                self.res = a.get_menu()

            elif any(word in tokens for word in ["антоним", "антонимы", "антон"]):
                self.user["passage_num"] = 4
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                self.res = a.get_menu()

            elif any(word in tokens for word in ["пароним", "парон", "парные", "паронимы"]):
                self.user["passage_num"] = 5
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                self.res = a.get_menu()
            elif any(word in tokens for word in ["глупые", "бестолковые"]):
                self.user["passage_num"] = 6
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id)
                self.res = a.get_menu()
            elif any(word in tokens for word in ["вперёд"]):
                self.user["passage_num"] = 0
                menu = Menu(self.res, self.req, self.user_id, False)
                self.res = menu.get_res(1)
                self.user["previous_buttons"] = self.res['response']['buttons'] = [{
                    "title": "Что ты умеешь?",
                    "hide": True
                }, {
                    "title": "Помощь",
                    "hide": True
                }]
            elif any(word in tokens for word in ["назад"]):
                self.user["passage_num"] = 0
                menu = Menu(self.res, self.req, self.user_id, False)
                self.res = menu.get_res(0)
                self.user["previous_buttons"] = self.res['response']['buttons'] = [{
                    "title": "Что ты умеешь?",
                    "hide": True
                }, {
                    "title": "Помощь",
                    "hide": True
                }]
            else:
                self.res['response']['text'], self.res['response']['tts'] = random.choice(
                    dialogues_info["incomprehension"])
                add_log_text(command)
                self.user["previous_buttons"] = self.res['response']['buttons'] = [{
                    "title": "Что ты умеешь?",
                    "hide": True
                }, {
                    "title": "Помощь",
                    "hide": True
                }]
        return

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
        if self.req['session']["message_id"] >= 20 and not self.user['pls_like'] and self.user["passage_num"] != 0:
            self.user['pls_like'] = True

            if self.res['response'].get('tts'):
                self.res['response'][
                    'text'] = "Понравился навык? Оцени, пожалуйста) Твоё мнение для меня на вес золота.\n\n" + \
                              self.res['response']['text']
                self.res['response']['tts'] = "Понр+авился н+авык? Оцени, пож+алуйста)" \
                                              " Тво+ё мн+ение для мен+я на в+ес з+олота. sil <[500]>" + \
                                              self.res['response']['tts']
            else:
                text = self.res['response']['text'][:]
                self.res['response'][
                    'text'] = "Понравился навык? Оцени, пожалуйста) Твоё мнение для меня на вес золота.\n\n" + text
                self.res['response'][
                    'tts'] = "Понр+авился н+авык? Оцен+и, пож+алуйста) Тво+ё мн+ение для мен+я на в+ес з+олота.\n\n" + \
                             text
            buttons = self.res['response']['buttons'][:]
            buttons.insert(0, {
                "title": "Оценить навык",
                "url": "https://dialogs.yandex.ru/store/skills/376e3bb3-prokachaj-leksiko",
                "hide": True
            })
            self.res['response']['buttons'] = buttons

        return self.res
