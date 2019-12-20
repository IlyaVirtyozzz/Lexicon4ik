import json, os.path


def read_json():
    with open("data.json", "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    return data


def dumb_json(data):
    with open("data.json", "w", encoding='utf-8') as write_file:
        json.dump(data, write_file, ensure_ascii=False)


def add_log_text(text):
    with open("dont_know.txt", "a", encoding='utf-8') as write_file:
        write_file.write(text + "\n")
