#!/usr/bin/env python

'''A UDP client for data transmission to server.'''

import socket
import sys
import select
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
        amount[0] = 0

    def open_socket(self):
        try:
          self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error:
          print "Error, server refused connection"

    def close_socket(self):
        self.socket.close()

    def send(self, message):
        try:
          self.socket.sendto(message, (self.host, self.port))
        except socket.error:
          print "Error, send request failed"
          self.close_socket()
          sys.exit(0)
         
    def spam(self):
      buff = 65507 * '\0' 
      #this is the maximum amount of data we can send. 65536 - 65507 = 29 bytes of 'header and other'.
      #Almost certainly results in IP fragmentation
      print "spamming server"
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

    try:
        ip = sys.argv[1]
        host = sys.argv[2]
    except IndexError:
        print '<ip> <port>'
        sys.exit(0)

    print "Starting UDP client"

    amount = []
    amount.append(0)

    c = UDP_Client(ip, int(host))
    c.open_socket()
    t = threading.Thread(target = c.spam)
    t.setDaemon(False)
    t.start()

    b = BandwidthMonitor()

    while 1:
      b.initiate()
      time.sleep(1)
      b.terminate()
      print str(b.get_bandwidth()/(1000*1000)) + 'MBytes/s OUT'
