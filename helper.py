import json


def read_json():
    with open("data.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    return data


def dumb_json(data):
    with open("data.json", "w",encoding='utf-8') as write_file:
        json.dump(data, write_file, ensure_ascii=False)
