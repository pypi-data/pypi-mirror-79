# -*- coding: utf8 -*-

from select import select
from socket import socket, socketpair, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from time import sleep


class Tcps:
    def __init__(self,
                 host=('127.0.0.1', 30000),
                 log=None):
        self.pair = socketpair()  # пара сокетов для self-pipe трюка
        self.log = log
        self.host = host
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server.bind(host)
        self.server.listen(5)
        self.clients = []
        if self.log:
            self.log.debug(f"tcps{host} wait connection")
        self.busy = False

    def close(self):
        self.pair[1].send(b'\0')  # self-pipe трюк
        while self.busy:
            sleep(.1)
        for s in self.clients:
            s.close()
        if self.log:
            self.log.debug(f"tcps{self.host} close")

    def new_client_cb(self, newclient):
        pass

    def read(self, timeout=None):
        rx = ''
        self.busy = True
        rs, [], [] = select([self.server, self.pair[0]] + self.clients, [], [], timeout)
        for s in rs:
            if s == self.server:
                newclient, addr = s.accept()
                self.clients.append(newclient)
                self.new_client_cb(newclient)
                if self.log:
                    self.log.debug(f"tcps{self.host} new client {addr}")
            elif s == self.pair[0]:
                if self.log:
                    self.log.debug(f"tcps{self.host} self-pipe trick signal")
                break
            else:  # clients
                try:
                    rx = s.recv(4096)
                except (ConnectionResetError, ConnectionAbortedError) as e:
                    if self.log:
                        self.log.error(f"tcps{self.host} read fail {e}")
                    self.clients.remove(s)
                    s.close()
                break
        self.busy = False
        return rx

    def write(self, data):
        ret = 0
        for s in self.clients:
            try:
                s.send(data)
                ret += 1
            except (ConnectionResetError, BrokenPipeError) as e:
                if self.log:
                    self.log.error(f"tcps{self.host} write fail {e}")
                self.clients.remove(s)
                s.close()
        return ret != 0


# from sdg_utils import log_open, DEBUG
#
# if __name__ == "__main__":
#     tcps = Tcps(log=log_open(level=DEBUG))
#     while 1:
#         sleep(1)

