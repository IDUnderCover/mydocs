#!/usr/bin/python
from flask import url_for, render_template
from app import app, flatpages
import json


from utils import treeview



@app.route('/index/', methods = ['GET'])
@app.route('/')
def index():

    pages = (p for p in flatpages)
    return render_template('index.html', pages=pages, tree=json.dumps(treeview.get_tree_view()))

@app.route('/pages/<path:path>/')
def page(path):
  page = flatpages.get_or_404(path)
  return render_template('page.html', page=page,tree=json.dumps(treeview.get_tree_view()))


@app.route('/blogs/', methods = ['GET'])
def get_blogs_list():
    return render_template('documents.html')


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404
