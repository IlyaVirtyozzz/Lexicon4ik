from flask import Flask, request
import json, logging

app = Flask(__name__)
with open('/home/AbilityForAlice/mysite/data.json', 'r', encoding='utf-8') as fh:
    data = json.load(fh)
with open('/home/AbilityForAlice/mysite/dialogues_info.json', 'r', encoding='utf-8') as fh:
    dialogues_info = json.load(fh)

sessionStorage = {}