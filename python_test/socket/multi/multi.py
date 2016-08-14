#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
import time
import socket

HOST = ''
PORT = 9999
ADDR = (HOST, PORT)
BUFFER = 1024

ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ser_socket.bind(ADDR)
ser_socket.listen(4)


def recv_from(sock, buf=1024):
    data = ""
    try:
        while True:
            tmp = sock.recv(buf)
            if not tmp:
                break
            data += tmp
    except:
       pass 
    return data



if __name__ == '__main__':
    pid = os.fork()
    
    
    if pid == 0:
        print "this is child process."
        while True:
            cli_sock, cli_addr = ser_socket.accept()
            print "connection from ", cli_addr
            request = recv_from(cli_sock)
            print request
            time.sleep(10)
    
    else:
        print "this is parent process."
        time.sleep(1000)


