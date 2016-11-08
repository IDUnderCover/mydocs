#!/usr/bin/python2
# coding=utf-8
import time
def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

@coroutine
def grep(pattern):
    print "looking for pattern %s" % pattern
    try:
        while True:
            line = (yield)
            if pattern in line:
                yield line
    except GeneratorExit:
        print "Going away. "
    

def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
        return cr
    return start

if __name__ == '__main__':
    logfile = open("access.log")
    loglines = follow(logfile)

    for line in loglines:
        print grep("python").send(line) 
