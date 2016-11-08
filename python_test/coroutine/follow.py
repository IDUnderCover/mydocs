#!/usr/bin/python2
# coding=utf-8
import time

def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start

def follow(thefile, target):
    thefile.seek(0,2)
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


if __name__ == '__main__':
    log_file = open("access.log")
    follow(
        log_file, broadcast([
            grep('python', printer()),
            grep('java', printer()),
            grep('lisp', printer())
            ]
        )
    )

