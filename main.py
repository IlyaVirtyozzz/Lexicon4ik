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
        self.dangerous = self.req["request"].get("markup")
        self.res['response']['buttons'] = []
        self.res['response']['text'] = ''
        self.res['response']['tts'] = ''

    def if_not_in_base(self):
        self.user = sessionStorage[self.user_id] = {"passage_num": 0, "room_num": 0, "previous_buttons": [],
                                                    "previous_tts": "а", "previous_text": "а",
                                                    "screen": False,
                                                    "pls_like": False,
                                                    "first_help": True,
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
            if "screen" in self.req["meta"]["interfaces"]:
                self.screen = self.user["screen"] = True
            else:
                self.screen = self.user["screen"] = False
            menu = Menu(self.res, self.req, self.user_id, self.screen, True)
            self.res = menu.get_res()
        else:
            if not self.user:
                self.if_new_session()
                if "screen" in self.req["meta"]["interfaces"]:
                    self.screen = self.user["screen"] = True
                else:
                    self.screen = self.user["screen"] = False
            self.screen = self.user["screen"]
            self.check_answer()

    def check_answer(self):

        if self.req['request'].get("original_utterance"):
            command = self.req['request']["original_utterance"].strip().lower()
            tokens = self.req['request']['nlu']['tokens']

        else:
            command = self.req['request']["payload"]["text"]
            tokens = list(map(lambda x: x.lower(), self.req['request']["payload"]["text"].split()))
            self.payload = True

        if command == "screen_true123":
            self.res['response']['text'], self.res['response']['tts'] = "Для телефонов", "Для телефонов"
            self.user["screen"] = True
            return
        elif command == "screen_false123":
            self.res['response']['text'], self.res['response']['tts'] = "Для колонок", "Для колонок"
            self.user["screen"] = False
            return

        elif (any(word in tokens for word in ["повторить", "повтори", "повтор"]) or ("еще раз" in command)) and (
                not self.screen) and not ((self.user["passage_num"] in [4, 2, 5]) and ((self.user["room_num"] == 2))):
            self.res['response']['text'] = self.user['previous_text'][:]
            self.res['response']['tts'] = self.user['previous_tts'][:]
            self.res['response']['buttons'] = self.user["previous_buttons"]
            return
        if not self.payload:
            if any(word in tokens for word in
                   ["открыть", "открой", "начать", "зайти", "включи", "начни", "зайди"]) and \
                    any(word in tokens for word in ["категорию", "категория"]):
                if any(word in tokens for word in ["интересные"]):
                    self.user["passage_num"] = 1
                    self.user["room_num"] = 0
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                    self.res = a.get_menu()
                    return self.res
                elif any(word in tokens for word in ["словарные", "словарная", "сс", "словарь", "словарный"]):
                    self.user["passage_num"] = 2
                    self.user["room_num"] = 0
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                    self.res = a.get_menu()
                    return self.res
                elif any(word in tokens for word in ["фразеологизмы", "фразеологизм"]):
                    self.user["passage_num"] = 3
                    self.user["room_num"] = 0
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                    self.res = a.get_menu()
                    return self.res
                elif any(word in tokens for word in ["антоним", "антонимы", "антон"]):
                    self.user["passage_num"] = 4
                    self.user["room_num"] = 0
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                    self.res = a.get_menu()
                    return self.res
                elif any(word in tokens for word in ["пароним", "парон", "парные", "паронимы"]):
                    self.user["passage_num"] = 5
                    self.user["room_num"] = 0
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                    self.res = a.get_menu()
                    return self.res
                elif any(word in tokens for word in ["глупые", "бестолковые"]):
                    self.user["passage_num"] = 6
                    self.user["room_num"] = 0
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                    self.res = a.get_menu()
                    return self.res

            if all(word in tokens for word in ["что", "умеешь"]):
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

                if self.screen:
                    self.res['response']['text'], self.res['response']['tts'] = [
                        "Благодарю Тебя.",
                        "Благодар+ю Теб+я."]
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = [
                        "Для того чтобы оценить навык, нужно зайти на страницу навыка через телефон или компьютер.",
                        "Для тог+о чт+обы оцен+ить н+авык, н+ужно зайт+и на стран+ицу н+авыка ч+ерез"
                        " телеф+он +или компь+ютер."]
                    self.res['response']['buttons'] = self.user["previous_buttons"]

            elif any(word in tokens for word in ["спасибо", "благодарю", "сенкс"]):
                self.res['response']['text'], self.res['response']['tts'] = random.choice(
                    [["Мне очень приятно это слышать.",
                      "Мн+е +очень при+ятно +это сл+ышать."],
                     ["Всегда рада помочь)",
                      "Всегд+а р+ада пом+очь)"],
                     ["Твоя благодарность для меня это лучший подарок",
                      "Тво+я благод+арность для мен+я это л+учший под+арок"]])
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
                self.res['response']['text'], self.res['response']['tts'] = random.choice(
                    [["Так исторически сложилось", "Так истор+ически слож+илось"],
                     ["Вот так вот)", "Вот так вот"]])
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif any(word in tokens for word in ["алиса", "alice", "алис"]):
                self.res['response']['text'], self.res['response']['tts'] = random.choice([[
                    "Ой. Я не Алиса. Можно сказать, я дополнение к ней.",
                    "Ой.sil <[300]> Я не Ал+иса. М+ожно сказ+ать, я дополн+ение к ней."],
                    ["Алиса - это Алиса. Я - это я. Я не Алиса. Голос разве что одинаковый...",
                     "Ал+иса sil <[400]> это Ал+иса. Я sil <[400]> это я. Я sil <[200]> не sil <[100]>Ал+иса."
                     "  Г+олос р+азве что один+аковый..."]])
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif any(word in tokens for word in dialogues_info['is_hello']):
                self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info['hello'])
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif all(word in tokens for word in ["ты", "кто"]):
                self.res['response']['text'], self.res['response']['tts'] = [
                    "Я та, кто может научить Тебя полезным словам)",
                    "Я та, кто м+ожет науч+ить Теб+я пол+езным слов+ам)"]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif (any(word in tokens for word in ["категория", "категории", "категорий"]) and len(tokens) == 1) or \
                    (any(word in tokens for word in ["какие"]) or (
                            any(word in tokens for word in ["категория", "категории", "категорий"]))):
                if self.screen:
                    menu = Menu(self.res, self.req, self.user_id, self.screen, False)
                    self.res = menu.get_res(0)
                    self.user["previous_buttons"] = self.res['response']['buttons'] = [{
                        "title": "Что ты умеешь?",
                        "hide": True
                    }, {
                        "title": "Помощь",
                        "hide": True
                    }]
                else:
                    self.res['response']['text'], self.res['response']['tts'] = [
                        "Интересные слова. Словарные слова. Фразеологизмы. Паронимы. Антонимы. Бестолковые слова.",
                        "Интер+есные слов+а. Слов+арные слов+а. Фразеолог+измы. Пар+онимы. Ант+онимы. Бестолк+овые слов+а."]
                    self.res['response']['buttons'] = self.user["previous_buttons"]
            elif all(word in tokens for word in ["как", "приложение", "называется"]) or all(
                    word in tokens for word in ["как", "навык", "называется"]):
                self.res['response']['text'], self.res['response']['tts'] = [
                    "\"Прокачай Лексикон\" По-моему звучит прикольно)",
                    "\"Прокач+ай Лексик+он\" По-м+оему звуч+ит прик+ольно!)"]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif all(word in tokens for word in ["ау", "эй", "уау"]):
                self.res['response']['text'], self.res['response']['tts'] = random.choice([[
                    "Да-да, я здесь.",
                    "Да-да, я зд+есь."], ["Да-да",
                                          "Да-да"]])
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif any(word in tokens for word in dialogues_info['is_bye']):
                self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info['bye'])
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif any(word in command.split() for word in dialogues_info['fuck_words']) or self.dangerous:
                self.res['response']['text'], self.res['response']['tts'] = random.choice(dialogues_info["fuck_answer"])
                self.res['response']['buttons'] = self.user["previous_buttons"]
                add_log_text(command)

            elif all(word in tokens for word in ["как", "тебя", "зовут"]) or all(
                    word in tokens for word in ["как", "вас", "зовут"]):
                self.res['response']['text'], self.res['response']['tts'] = ["Сама прихожу.",
                                                                             "Сама прихож+у."]
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif any(word in tokens for word in ["ясно", "понятно"]):
                self.res['response']['text'], self.res['response']['tts'] = random.choice(
                    [["Это отлично.", "Это отлично."], ["Хорошо", "Хорошо"],
                     ["Мне приятно знать, что Ты всё понимаешь)",
                      "Мне при+ятно зн+ать, что Ты всё поним+аешь)"]])
                self.res['response']['buttons'] = self.user["previous_buttons"]

            elif self.user["passage_num"] == 0:
                if any(word in tokens for word in dialogues_info['is_help']):
                    if self.screen:
                        self.res['response']['text'], self.res['response']['tts'] = dialogues_info["helps"]["main"]
                        self.res['response']['buttons'] = self.user["previous_buttons"]
                    else:
                        self.res['response']['text'], self.res['response']['tts'] = \
                            dialogues_info["helps_without_screen"]["main"]
                elif any(word in tokens for word in ["меню", "главное"]):
                    if self.screen:
                        self.res['response']['text'], self.res['response']['tts'] = ["Ты и так уже здесь.",
                                                                                     "Ты и так уже зд+есь."]
                        self.res['response']['buttons'] = self.user["previous_buttons"]
                        menu = Menu(self.res, self.req, self.user_id, self.screen, False)
                        self.res = menu.get_res(0, ["Ты и так уже здесь.",
                                                    "Ты и так уже зд+есь."])
                    else:
                        self.res['response']['text'], self.res['response']['tts'] = [
                            "Тебе доступны категории Интересные слова. Словарные слова. Фразеологизмы. Паронимы. Антонимы. Бестолковые слова. Выбери, что тебе интересно. ",
                            "Тебе дост+упны катег+ории Интер+есные слов+а. Слов+арные слов+а. Фразеолог+измы. Пар+онимы. Ант+онимы. Бестолк+овые слов+а. В+ыбери, что тебе интер+есно."]

                elif any(word in tokens for word in ["интересные"]):
                    self.user["passage_num"] = 1
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                    self.res = a.get_menu()
                elif any(word in tokens for word in ["словарные", "словарная", "сс", "словарь", "словарный"]):
                    self.user["passage_num"] = 2
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                    self.res = a.get_menu()
                elif any(word in tokens for word in ["фразеологизмы", "фразеологизм"]):
                    self.user["passage_num"] = 3
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                    self.res = a.get_menu()
                elif any(word in tokens for word in ["антоним", "антонимы", "антон"]):
                    self.user["passage_num"] = 4
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                    self.res = a.get_menu()
                elif any(word in tokens for word in ["пароним", "парон", "парные", "паронимы"]):
                    self.user["passage_num"] = 5
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                    self.res = a.get_menu()
                elif any(word in tokens for word in ["глупые", "бестолковые"]):
                    self.user["passage_num"] = 6
                    a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                    self.res = a.get_menu()
                elif any(word in tokens for word in
                         ["поехали", "давай", "начать", "начинаем", "старт", "стартуем", "да", "погнали"]):
                    self.res['response']['text'], self.res['response']['tts'] = [
                        "Поехали! Ой, выбери сначала категорию.",
                        "По+ехали! Ой,sil <[200]> в+ыбери снач+ала катег+орию."]
                    self.res['response']['buttons'] = self.user["previous_buttons"]
                else:
                    if self.screen:
                        self.res['response']['text'], self.res['response']['tts'] = random.choice(
                            [[
                                "На данный момент Ты находишся в Главном меню. Для того чтобы продолжить,"
                                " Тебе следует выбрать категорию. И да, при любой непонятной ситуации"
                                " Ты можешь воспользоваться командой \"Помощь\".",
                                "На д+анный мом+ент Ты нах+одишся в Гл+авном мен+ю. Для тог+о чт+обы прод+олжить,"
                                " Теб+е сл+едует в+ыбрать катег+орию."
                                " И да,sil <[300]> при люб+ой непон+ятной ситу+ации"
                                " Ты м+ожешь восп+ользоваться ком+андой \"Помощь\"."]])
                    else:
                        self.res['response']['text'], self.res['response']['tts'] = random.choice([[
                            "На данный момент Ты находишся в Главном меню. Тебе доступны категории Интересные слова."
                            " Словарные слова. Фразеологизмы. Паронимы. Антонимы. Бестолковые слова."
                            "Что выбираешь?",
                            "На д+анный момент Ты нах+одишся в Гл+авном мен+ю. Тебе дост+упны катег+ории sil <[100]> Интер+есные слов+а."
                            " Слов+арные слов+а. Фразеолог+измы. Пар+онимы. Ант+онимы. Бестолк+овые слов+а."
                            "Что выбир+аешь?"]])
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
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                self.res = a.get_menu()
            elif any(word in tokens for word in ["словарные", "словарная", "сс", "словарь", "словарный"]):
                self.user["passage_num"] = 2
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                self.res = a.get_menu()
            elif any(word in tokens for word in ["фразеологизмы", "фразеологизм"]):
                self.user["passage_num"] = 3
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                self.res = a.get_menu()

            elif any(word in tokens for word in ["антоним", "антонимы", "антон"]):
                self.user["passage_num"] = 4
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                self.res = a.get_menu()

            elif any(word in tokens for word in ["пароним", "парон", "парные", "паронимы"]):
                self.user["passage_num"] = 5
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                self.res = a.get_menu()
            elif any(word in tokens for word in ["глупые", "бестолковые"]):
                self.user["passage_num"] = 6
                a = self.classes_list[self.user["passage_num"] - 1](self.res, self.req, self.user_id, self.screen)
                self.res = a.get_menu()
            elif any(word in tokens for word in ["вперёд"]):
                self.user["passage_num"] = 0
                menu = Menu(self.res, self.req, self.user_id, self.screen, False)
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
                menu = Menu(self.res, self.req, self.user_id, self.screen, False)
                self.res = menu.get_res(0)
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

        buzzwordsmenu = Buzzwords(self.res, self.req, self.user_id, self.screen)
        self.res = buzzwordsmenu.sequence()

    def antonyms_menu(self):
        antonymsmenu = Antonyms(self.res, self.req, self.user_id, self.screen)
        self.res = antonymsmenu.sequence()

    def phraseologisms_menu(self):
        phraseologismsmenu = Phraseologisms(self.res, self.req, self.user_id, self.screen)
        self.res = phraseologismsmenu.sequence()

    def paronyms_menu(self):
        paronymsmenu = Paronyms(self.res, self.req, self.user_id, self.screen)
        self.res = paronymsmenu.sequence()

    def stupid_dictionary_menu(self):
        stupidmenu = Stupid_Dictionary(self.res, self.req, self.user_id, self.screen)
        self.res = stupidmenu.sequence()

    def vocabulary_words_menu(self):
        vocabularymenu = Vocabulary_words(self.res, self.req, self.user_id, self.screen)
        self.res = vocabularymenu.sequence()

    def get_response(self):
        self.user['previous_text'] = self.res['response']['text'][:]
        self.user['previous_tts'] = self.res['response']['tts'][:]
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
