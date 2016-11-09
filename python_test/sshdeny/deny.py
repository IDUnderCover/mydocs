#!/usr/bin/python2
# -*- coding: utf8 -*-
import time
import sys
import re
def coroutine(func):
    def start(*args, **kwargs):
        rc = func(*args, **kwargs)
        rc.next()
        return rc
    return start


def follow(thefile, target):
    print "following the file %s" % thefile.name
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if line:
            target.send(line)
        time.sleep(0.2)

@coroutine
def filter_pattern(pattern, target):
    print "searching for pattern <%s>" % pattern 
    try:
        while True:
            line = (yield)
            if pattern in line:
                target.send(line)
    except GeneratorExit:
        print "filter coroutine exited"

@coroutine 
def grep_ip_addr(target):
    print "grep ip address"
    reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
    try:
        while True:
            line = (yield)
            ips = reip.findall(line)
            if ips:
                for ip in ips:
                    target.send(ip) 
    except GeneratorExit:
        print "grep ip exited"

@coroutine
def write_to_file(dest, mode):
    print "write to file"
    thefile = open(dest, mode)
    try:
        while True:
            ip = (yield)
            line = 'sshd:' + ip + '\n' 
            print line
            thefile.write(line)
            thefile.flush()
    except GeneratorExit:
        print "writing process exited"
    finally:
        thefile.close()

    


if __name__ == '__main__':
    logfile = open(sys.argv[1])
    follow(logfile, 
            filter_pattern("Failed",
                grep_ip_addr(write_to_file('/etc/hosts.deny','a+'))
            )
        )
     


