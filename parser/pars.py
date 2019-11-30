from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from argparse import ArgumentParser
import urllib.request
import os


def get_img(query, browser, count=1):
    url = 'https://yandex.com.tr/gorsel/search?text=' + query
    browser.get(url)
    time.sleep(1)
    element = browser.find_element_by_tag_name("body")
    # Scroll down
    for i in range(count // 10):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id("smb").click()
        for i in range(count // 10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)  # bot id protection
    except:
        for i in range((count // 100) + 1):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)  # bot id protection
    time.sleep(0.5)
    source = browser.page_source
    soup = BeautifulSoup(source, 'lxml')  # choose lxml parser
    # find the tag : <img ... >
    image_tags = soup.findAll('img')
    # print out image urls
    counter = 0
    for image_tag in image_tags:
        if counter == count:
            break
        link = image_tag.get('src')
        if link is None or link == '':
            continue
        link = 'http:' + link
        print(link, counter + 1)  # page source1
        for i in range(3):
            try:
                urllib.request.urlretrieve(link, "./photo/" + query + ".jpeg")
                counter += 1
                break
            except:
                print("\tSleeping..")
                time.sleep(2)
        time.sleep(0.1)


def run(list_, count):
    browser = webdriver.Firefox(executable_path=os.getcwd() + "\geckodriver.exe")
    browser.set_window_size(1024, 768)
    for query in list_:
        get_img(query, browser, count)
    browser.close()


words = ['Буря в стакане воды', 'Вилами по воде писано', 'Воду в решете носить', 'Воды в рот набрать',
         'Вывести на чистую воду',
         'Выйти сухим из воды', 'Гнать волну', 'Деньги как вода', 'Держаться на плаву', 'Ждать у моря погоды',
         'Жизнь бьёт ключом', 'Как в воду глядел', 'Как в воду канул', 'Как в воду опущенный', 'Как вода сквозь пальцы',
         'Как две капли воды', 'Как пить дать', 'Как с гуся вода', 'Как снег на голову', 'Кануть в лету',
         'Купаться в золоте',
         'Лёд тронулся', 'Лить воду', 'Много воды утекло', 'Море по колено', 'Мрачнее тучи', 'Мутить воду',
         'На вершине волны',
         'Не разлей вода', 'Переливать из пустого в порожнее', 'Плыть по течению', 'Подводные камни',
         'После дождичка в четверг', 'Последняя капля', 'Пройти огонь, воду и медные трубы', 'Пруд пруди',
         'С лица воду не пить', 'Со дна моря достать', 'Спрятать концы в воду', 'Тише воды, ниже травы',
         'Толочь воду в ступе',
         'Умывать руки', 'Чистой воды', 'Бурчать под нос', 'Вешать нос', 'Водить за нос', 'Выше нос!', 'Задирать нос',
         'Зарубить на носу', 'Клевать носом', 'Морщить нос', 'На носу', 'Не видеть дальше своего носа',
         'Нос к носу или лицом к лицу', 'Нос по ветру держать', 'Остаться с носом или уйти с носом', 'Под самым носом',
         'С гулькин нос', 'Совать свой нос не в своё дело', 'Тыкать носом', 'Утереть нос', 'Уткнуться носом',
         'Говорить сквозь зубы', 'Заговаривать зубы', 'Знать на зубок', 'Зубы скалить или показывать зубы',
         'Не по зубам',
         'Ни в зуб ногой', 'Положить зубы на полку', 'Стиснуть зубы', 'Держать язык за зубами', 'Длинный язык',
         'Прикусить язык', 'Распускать язык', 'Язык проглотить', 'Держать ухо востро', 'Держать ушки на макушке',
         'За глаза и за уши', 'Не видать как своих ушей', 'Покраснеть до ушей', 'Развесить уши', 'Глаза на лоб вылезли',
         'Глаза разгорелись', 'Глазками стрелять', 'Как бельмо на глазу', 'Пускать пыль в глаза', 'С точки зрения',
         'Смотреть сквозь пальцы', 'Строить глазки', 'В рот не возьмёшь', 'Губа не дура', 'Надуть губы',
         'Раскатать губу',
         'С открытым ртом', 'Вылетело из головы', 'Иметь голову на плечах', 'Ломать голову', 'Морочить голову',
         'С головы до ног', 'Ставить с ног на голову', 'Сломя голову', 'Ударить лицом в грязь', 'Быть под рукой',
         'Держать себя в руках', 'Как рукой сняло', 'Кусать локти', 'Не покладая рук', 'Рука об руку', 'Рукой подать',
         'Ухватиться обеими руками', 'Золотые руки', 'Встать не с той ноги', 'Вытирать ноги (об кого-либо)',
         'Делать ноги',
         'Наступать на пятки', 'Ноги в руки', 'Сам чёрт ногу сломит', 'Сбиться с ног', 'Даром хлеб есть', 'И то хлеб',
         'На своих хлебах', 'Не хлебом единым', 'Отбивать хлеб', 'Перебиваться с хлеба на квас (на воду)',
         'Садиться на хлеб и воду', 'Хлеб насущный', 'Хлеб-соль', 'Хлеба и зрелищ!', 'Хлебом не корми',
         'Бесплатный сыр',
         'Вариться в собственном соку', 'Выеденного яйца не стоит', 'Дырка от бублика', 'За семь вёрст киселя хлебать',
         'Заварить кашу', 'И калачом не заманишь', 'Как кур во щи', 'Как по маслу', 'Как сыр в масле кататься',
         'Каши не сваришь', 'Молочные реки, кисельные берега', 'Не в своей тарелке', 'Несолоно хлебавши',
         'Ни за какие коврижки', 'Ни рыба ни мясо', 'Отрезанный ломоть', 'Профессор кислых щей', 'Проще парёной репы',
         'Расхлёбывать кашу', 'Сбоку припёка', 'Седьмая вода на киселе', 'Собаку съесть', 'Тёртый калач',
         'Хрен редьки не слаще', 'Хуже горькой редьки', 'Чепуха на постном масле', 'Через час по чайной ложке',
         'Гоняться за двумя зайцами', 'Делать из мухи слона', 'Дразнить гусей', 'Ежу понятно (козе понятно)',
         'И волки сыты, и овцы целы', 'Как кошка с собакой', 'Как курица лапой', 'Как курица с яйцом',
         'Как мышь на крупу',
         'Когда рак на горе свистнет', 'Кошки скребут на душе', 'Крокодиловы слёзы', 'Курам на смех', 'Куры не клюют',
         'Львиная доля', 'Мартышкин труд', 'Медведь на ухо наступил', 'Медвежий угол', 'Медвежья услуга',
         'Метать бисер перед свиньями', 'На кривой козе не подъедешь', 'На птичьих правах', 'Не в коня корм (овёс)',
         'Не пришей кобыле хвост', 'Покажу, где раки зимуют', 'Прятать голову в песок', 'Пустить красного петуха',
         'С высоты птичьего полёта', 'Свинью подложить', 'Смотреть, как баран на новые ворота', 'Собачий холод',
         'Считать ворон', 'Тёмная лошадка', 'Тянуть кота за хвост', 'Убить двух зайцев сразу', 'Хоть волком вой',
         'Чёрная кошка пробежала', 'Битый час', 'Бить баклуши', 'Бросить на произвол судьбы', 'Вам зелёный свет!',
         'Вставлять палки в колёса', 'Гору обойти', 'Держать в узде', 'Держать карман шире', 'Из грязи в князи',
         'Из ряда вон выходящий', 'Изобретать велосипед', 'Испокон веков', 'Камень с души (с сердца) свалился',
         'Картина маслом', 'Катить бочку', 'Мама не горюй', 'Менять шило на мыло', 'Накрыться медным тазом',
         'Нашла коса на камень', 'Не горит', 'Не за горами', 'Не лыком шит', 'Не по карману',
         'От нашего стола к вашему',
         'Откладывать в долгий ящик', 'Перегибать палку', 'Песенка спета', 'По плечу', 'По существу',
         'Подливать масло в огонь',
         'Поезд ушёл', 'Раз, два', 'Родиться в рубашке', 'Сводить концы с концами', 'Сдвинуть гору',
         'Сидеть как на иголках',
         'Хоть бы хны']
imgCount = 1
run(words, imgCount)
