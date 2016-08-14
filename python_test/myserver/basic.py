#!/usr/bin/env python
# -*- coding:utf8 -*-
import socket
import time

HOST, PORT = '', 9999

tcp_ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_ser_socket.bind((HOST,PORT))
tcp_ser_socket.listen(3)

print "Serving HTTP on port %s..." % PORT

try:
    while True:
        cli_socket, addr = tcp_ser_socket.accept()
        request = cli_socket.recv(1024)
        print request
    
        http_response = """
HTTP/1.1 200 OK

Hello, World!
"""
        cli_socket.sendall(http_response)
        cli_socket.close()
except BaseException, e:
    print str(e)
finally:
    tcp_ser_socket.close()
