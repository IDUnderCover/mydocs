#!/usr/bin/python
from flask import url_for, render_template
from app import app, flatpages
from utils import treeview
import json
@app.route('/index/', methods = ['GET'])
@app.route('/')
def index():
    #pages = (p for p in flatpages if 'date' in p.meta)
    pages = (p for p in flatpages)
    pages2 = (p for p in flatpages)
    tree = treeview.new_tree()
    for page in list(pages):
        tree = treeview.add_tree_node(tree,treeview.gen_tree_node(page.path,page.path))

    print(tree)
    return render_template('index.html', pages=pages2, tree=json.dumps(tree))

@app.route('/pages/<path:path>/')
def page(path):
  page = flatpages.get_or_404(path)
  return render_template('page.html', page=page)


@app.route('/blogs/', methods = ['GET'])
def get_blogs_list():
    return render_template('documents.html')


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404
