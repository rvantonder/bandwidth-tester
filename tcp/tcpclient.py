#!/usr/bin/env python

"""
An echo client that allows the user to send multiple lines to the server.
Entering a blank line will exit the client.
"""

import socket
import sys
import select
from logger import Logger

class TCP_Client:

    def __init__(self, ip, port):
        self.host = ip
        self.port = port 
        self.size = 1024
        self.socket = None
        self.username = ''
        clientLogger = Logger('udpclient.log')
        clientLogger.logger.info('Starting UDP client.');

    def open_socket(self):
        try:
          self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          self.socket.connect((self.host, self.port))
          clientLogger.logger.info('Connection to server made')
        except socket.error:
          clientLogger.logger.error('Server refused connection.')
          print "Error, server refused connection"

    def close_socket(self):
        self.socket.close()
        clientLogger.logger.info('Connection closed.')

    def send(self, message):
        try:
          self.socket.send(message)
        except socket.error:
          clientLogger.logger.error('Send request failed')
          print "Error, send request failed"
         
    def spam(self):
      buff = 1024 * '\0'
      clientLogger.logger.info('Spamming the server now')
      print "Spamming the server now"
      while 1:
        try:
          self.send(buff)
        except socket.error:
          print 'An error occurred'

if __name__ == '__main__':

    clientLogger = Logger('tcpclient.log')
    clientLogger.logger.info('Starting TCP client')
    print "Starting TCP client"

    try:
      c = TCP_Client(sys.argv[1]+'.narga.sun.ac.za', int(sys.argv[2]))
      c.open_socket()
      c.spam()
    except IndexError:
      print 'Enter name and port' 
