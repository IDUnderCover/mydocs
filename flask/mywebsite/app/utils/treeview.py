# -*- coding:utf8 -*-

# tree_node 是由单个文件的目录地址转换而成 {'text': "目录名",  "nodes": [tree_node1] }

# tree 是由多个 tree_node 构成  tree = [tree_node1, tree_node2 ]

from flask import url_for
# 因为都是相对目录, 所以目录都以字母开头
def gen_tree_node(path,fullpath=None):
    split_path = path.split('/', 1)

    if len(split_path) == 1:
        return { 'text' : split_path[0], 'href': url_for("page", path=fullpath)}
    else:
        return { 'text' : split_path[0],
                 'nodes' : [gen_tree_node(split_path[1],fullpath)]}

def new_tree(tree_node=[]):
    return []

def add_tree_node(tree, add_node):
    if not tree:
        tree = [add_node]
    else:
        for i in range(len(tree)):
            if tree[i]['text'] == add_node['text']:
                new_node = combine_node(tree[i],add_node)
                tree[i] = new_node
                break;
            if i == len(tree) - 1:
                tree = tree + [add_node]

    return tree


def combine_node(node_1, node_2):
    print("node_1",node_1)
    print("node_2", node_2)
    if node_1['text'] == node_2['text']:
        if node_1.has_key('nodes'):
            if node_2.has_key('nodes'):
                return {'text': node_1['text'] , 'nodes': add_tree_node(node_1['nodes'],node_2['nodes'][0])}
            else:
                return { 'text': node_2['text'] , 'nodes': node_1['nodes'] + [ node_2 ]}
        else:
            if node_2.has_key('nodes'):
                return node_2
            else:
                return node_1




if __name__ == '__main__':
    path1 = 'docker'
    path2 = 'docker/flask'
    path3 = 'python/pip'
    path4 = 'docker/flask/index'
    path5 = 'docker/flask/index2'
    tree = new_tree(gen_tree_node(path1))
    print(tree)
    tree = add_tree_node(tree, gen_tree_node(path2))
    print(tree)
    tree = add_tree_node(tree, gen_tree_node(path3))
    print(tree)
    tree = add_tree_node(tree, gen_tree_node(path4))
    print(tree)
    tree = add_tree_node(tree, gen_tree_node(path5))
    print(tree)