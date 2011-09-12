#!/usr/bin/env python

"""
An echo client that allows the user to send multiple lines to the server.
Entering a blank line will exit the client.
"""

import socket
import sys
import select
from logger import Logger
import threading
import time

global amount

class UDP_Client:

    def __init__(self, ip, port):
        self.host = ip
        self.port = port 
        self.size = 1024
        self.socket = None
        self.username = ''
        clientLogger = Logger('udpclient.log')
        clientLogger.logger.info('Starting UDP client.');
        amount[0] = 0

    def open_socket(self):
        try:
          self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #socket.SOCK_DGRAM for datagrams
          #self.socket.connect((self.host, self.port))
          #clientLogger.logger.info('Connection to server made')
        except socket.error:
          clientLogger.logger.error('Server refused connection.')
          print "Error, server refused connection"

    def close_socket(self):
        self.socket.close()
        clientLogger.logger.info('Connection closed.')

    def send(self, message):
        try:
          self.socket.sendto(message, (self.host, self.port))
        except socket.error:
          clientLogger.logger.error('Send request failed')
          print "Error, send request failed"
          self.close_socket()
          sys.exit(0)
         
    def spam(self):
      buff = 65507 * '\0' #this is the maximum amount of data we can send. 65536 - 65507 = 29 bytes of 'header and other junk'. Almost certainly results in IP fragmentation
      #buff = 45000 * '\0'
      #buff = 576 * '\0' #minimum reassembly buffer size, guaranteed size any implementation must support
      #buff = 1024 * '\0'
      clientLogger.logger.info('Spamming the server now')
      print "Spamming the server now"
      while 1:
        self.send(buff)
        amount[0] += len(buff)


class BandwidthMonitor(threading.Thread):
  def __init__(self):
    self.start = 0
    self.end = 0
    self.amount_now = 0

  def initiate(self):
    self.start = time.time()

  def terminate(self):
    self.amount_now = amount[0]
    amount[0] = 0
    self.end = time.time()

  def get_bandwidth(self):
    return self.amount_now/(self.end-self.start)


if __name__ == '__main__':

    clientLogger = Logger('udpclient.log')
    clientLogger.logger.info('Starting UDP client')
    print "Starting UDP client"

    amount = []
    amount.append(0)

    try:
      c = UDP_Client(sys.argv[1], int(sys.argv[2]))
      #c = UDP_Client(sys.argv[1]+'.narga.sun.ac.za', int(sys.argv[2]))
      c.open_socket()
      t = threading.Thread(target = c.spam)
      t.setDaemon(False)
      t.start()

      b = BandwidthMonitor()

      while 1:
        b.initiate()
        time.sleep(1)
        b.terminate()
        print str(b.get_bandwidth()/(1024*1024)) + 'MBytes/s OUT'

    except IndexError:
      print 'Enter <ip> and <port>' 
