#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception, e:
        print "[!!] failed to listen on %s:%s, exception %s" % (local_host, local_port, str(e))
        sys.exit(0)

    print "[!!] listening on %s:%d" % (local_host, local_port)

    server.listen(5)

    while True:
        cli_sock, addr = server.accept()
        print "[==>] receive incoming connection from %s:%s" % (addr[0], addr[1]) 
        #proxy_handler(cli_sock, remote_host, remote_port, receive_first)
        proxy_thread = threading.Thread(target=proxy_handler, 
            args=(cli_sock, remote_host, remote_port, receive_first))
        proxy_thread.start()

def proxy_handler(cli_sock, remote_host, remote_port, receive_first):
    remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_sock.connect((remote_host,remote_port))
    if receive_first:
        remote_buffer = receive_from(remote_sock)
        hexdump(remote_buffer)

        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer):
            print "sending %d bytes to localhost." % len(remote_buffer)
            cli_sock.send(remote_buffer)

    while True:

        local_buffer = receive_from(cli_sock)
        if len(local_buffer):
            print "[==>] received %d bytes from localhost" % len(local_buffer)
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_sock.send(local_buffer)
            print "[==>] send to remote"

        remote_buffer = receive_from(remote_sock)
        if len(remote_buffer):
            print "[<==] received %d bytes from remote" % len(remote_buffer)
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            cli_sock.send(remote_buffer)
            print "[<==] send to localhost"

        if not len(local_buffer) and not len(remote_buffer):
            cli_sock.close()
            remote_sock.close()
            print "[*] no more data. Closing connections."
            break


def receive_from(sock):
    buffer = ""
    sock.settimeout(2)
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer        

def hexdump(src, length=8):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
        result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    print b'\n'.join(result)


def response_handler(remote_buffer):
    return remote_buffer
def request_handler(remote_buffer):
    return remote_buffer

if __name__ == '__main__':
    if len(sys.argv[1:]) != 5:
        print "Usage: ./proxy.py [localhost] [port] [remotehost] [remoteport] [receive_first]"
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port= int(sys.argv[4])
    receive_first = sys.argv[5]

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)
