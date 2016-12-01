#!/usr/bin/env python
# coding=utf-8
import time
from Queue import Queue
from threading import Thread
import pickle


def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start


def follow(thefile, target):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        target.send(line)


@coroutine
def grep(pattern, target):
    print "looking for pattern %s" % pattern
    try:
        while True:
            line = (yield)
            if pattern in line:
                target.send(line)
    except GeneratorExit:
        print "Going away. "


@coroutine
def printer():
    print "this is printer "
    try:
        while True:
            line = (yield)
            print line
            time.sleep(1)
    except GeneratorExit:
        print "Printer exits"


@coroutine
def broadcast(targets):
    print "broadcast to multiple targets"
    try:
        while True:
            msg = (yield)
            for target in targets:
                target.send(msg)
    except GeneratorExit:
        print "broadcast over"


@coroutine
def threaded(target):
    messages = Queue()

    def run_target():
        while True:
            item = messages.get()
            if item is GeneratorExit:
                target.close()
                return
            else:
                target.send(item)
    thread = Thread(target=run_target)
    thread.setDaemon(True)
    thread.start()
    try:
        while True:
            item = (yield)
            messages.put(item)
    except GeneratorExit:
        messages.put(GeneratorExit)


@coroutine
def send_to(f):
    try:
        while True:
            item = (yield)
            pickle.dump(item, f)
            f.flush()
    except StopIteration:
        f.close()


@coroutine
def recv_from(f, target):
    try:
        while True:
            item = pickle.load(f)
            target.send(item)
    except EOFError:
        target.close()


def send_func(target):
    for i in range(1000):
        target.send(i)

if __name__ == '__main__':
    # log_file = open("access.log")
    # follow(
    #    log_file, threaded(
    #        broadcast([
    #                grep('python', printer()),
    #                grep('java', printer()),
    #                grep('lisp', printer())
    #            ]
    #        )
    #    )
    #)
    printer01 = printer()
    # t1 = threaded(printer01)
    # t2 = threaded(printer01)
    # for i in range(1000):
    #    t1.send(i)
    #    t2.send(i)

    Thread(target=send_func, args=(printer01,)).start()
    Thread(target=send_func, args=(printer01,)).start()
