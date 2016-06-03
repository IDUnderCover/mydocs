# -*- coding:utf8 -*-

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from flask_flatpages import FlatPages
flatpages = FlatPages(app)

from app import view
