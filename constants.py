from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json, logging, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqldatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'key?'
db = SQLAlchemy(app)
with open('/home/IlyaVirtyozzzproject/mysite/data.json', 'r', encoding='utf-8') as fh:
    data = json.load(fh)
