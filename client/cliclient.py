#!/usr/bin/env python

"""
An echo client that allows the user to send multiple lines to the server.
Entering a blank line will exit the client.
"""

import socket
import sys
import select
from logger import Logger

class Client:

    def __init__(self, ip, port):
        self.host = ip
        self.port = port 
        self.size = 1024
        self.socket = None
        self.username = ''
        clientLogger = Logger('client.log')
        clientLogger.logger.info('Starting client.');

    def open_socket(self):
        try:
          self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.socket.connect((self.host, self.port))
        except socket.error:
          print "error, server refused connection"
          sys.exit(0)

    def close_socket(self):
        self.socket.close()
        clientLogger.logger.info('Connection closed.')

    def send(self, message):
        try:
          self.socket.send(message)
        except socket.error:
          print 'an error occurred, quiting'
          sys.exit(0)
         
    def run(self):       
      try:
        input = [self.socket, sys.stdin]

        while 1:
            inputready,outputready,exceptready = select.select(input,[],[])
            # read from keyboard
            for item in inputready:
                if item == sys.stdin: #if input from terminal
                    line = sys.stdin.readline()
                    if line == '\n':
                        break
                    self.send(line)
                else: #if socket
                    response = self.socket.recv(self.size)
                    sys.stdout.write(response)
        self.close_socket()
      except socket.error:
        print 'an error occurred'

    def spam(self):

      buff = '\0' * 341024 
      print buff
      print 'buff',len(buff)

      while 1:
        self.send(buff)

if __name__ == '__main__':

    clientLogger = Logger('client.log')
    clientLogger.logger.info('Starting client.');

    try:
      c = Client(sys.argv[1], int(sys.argv[2]))
      c.open_socket()
      c.spam()
    except IndexError:
      print 'Enter name and port' 
