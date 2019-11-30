import requests
import json
import os


def read_json():
    with open("data.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    return data


data = read_json()

dir_name = "./after_edit/"
url = "https://dialogs.yandex.net/api/v1/skills/258d1716-2aea-4e4a-8d4e-198f448f72e1/images"

for file in os.listdir(path=dir_name):
    files = {"file": open(dir_name + file, "rb")}
    a = requests.post(url,
                      headers={"Authorization": "OAuth AQAAAAAbmj-UAAT7o2_k9MfXh00huVG9-nCl1zg",

                               },
                      files=files,
                      )

    id = a.json()["image"]["id"]
    for i in data["buzzwords"]:
        if list(i.keys())[0] == file[:file.find(".")]:
            i["id"] = id


def dumb_json(data):
    with open("data.json", "w",encoding='utf-8') as write_file:
        json.dump(data, write_file, ensure_ascii=False)


dumb_json(data)
