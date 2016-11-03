#!/usr/bin/env python
# coding=utf-8

def echo(value=None):
    print "Execution start"
    try:
        while True:
            try:
                value = (yield value)
            except Exception, e:
                value = e
    finally:
        print "Don't forget to clean up when 'close()' is called."

if __name__ == '__main__':
    gen = echo(1)
    print "---"
    print gen.next()
    print gen.send(2)
    gen.close()
