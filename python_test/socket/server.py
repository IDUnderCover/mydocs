#!/usr/bin/env python
# -*- coding:utf8 -*-

from socket import *
from time import ctime
from threading import Thread

HOST = ''
PORT = 34567
BUFSIZE = 1024
ADDR = (HOST, PORT)
        
#tcp_ser_sock.close() 
def handle_client(cli_sock):
    while True:
        request = cli_sock.recv(BUFSIZE)
        if not request:
            cli_sock.close()
            print "close connection"
            break
        cli_sock.send('[%s] ACK!  %s' % (ctime(), request))
        print 'receive ' + request 

if __name__ == '__main__':
    try:
        tcp_ser_sock = socket(AF_INET, SOCK_STREAM)
        tcp_ser_sock.bind(ADDR)
        tcp_ser_sock.listen(5)
        while True:
            print "waiting for connection..."
            tcp_cli_sock, addr = tcp_ser_sock.accept()
            print "...connected from:", addr
            handle = Thread(target=handle_client, args=(tcp_cli_sock,))
            handle.start()
    except BaseException,e:
        print str(e)
    finally:
        tcp_ser_sock.close()

        
