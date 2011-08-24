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

    def close_socket(self):
        self.socket.close()
        clientLogger.logger.info('Connection closed.')

    def request_username(self):
        user =  raw_input('Please enter a username: ')

        try:
            self.open_socket()
        except socket.error:
            print "Error. Server refused connection."
            clientLogger.logger.exception('Server refused connection.')
            return False
        clientLogger.logger.info('Connection open.')

        self.send('request:' + user)
        response = self.socket.recv(self.size)
        if (response == 'REJECT'):
            self.close_socket()
            print 'Username already in use.'
            clientLogger.logger.info('Username ' + user + ' already in use.')
            return False
        elif (response == 'ACCEPT'):
            print 'Welcome ' + user
            clientLogger.logger.info('Username ' + user + ' accepted by server.')
            self.username = user
            return True
    
    def send(self, message):
        self.socket.send(message)
         
    def run(self):       
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

if __name__ == '__main__':

    clientLogger = Logger('client.log')
    clientLogger.logger.info('Starting client.');

    c = Client(sys.argv[1], int(sys.argv[2]))

    if c.request_username():
        c.run()
    else:
        print 'Something went wrong, restart client.'

