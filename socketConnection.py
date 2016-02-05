#!/usr/bin/python

import socket

class SocketConnection:

    def __init__(self,host,port):
        self.sock = socket.socket()
        self.sock.connect(host, port)

    def send(self, data):
        self.sock.send(data)
        return

    def recv(self):
        return self.sock.recv(1024)
