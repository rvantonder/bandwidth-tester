#!/usr/bin/env python

'''A UDP server for receiving data from client.'''

from pylab import *
from numpy import *

import select
import socket
import sys
import threading
#import logging
import os
import pickle
import time
#import datetime
#import signal

#def signal_handler(signal, frame):
#  print 'You pressed stuff'
#  sys.exit(0)

global amount

class Server:
  def __init__(self, port):
    self.host = '0.0.0.0'
    self.port = port 
    self.backlog = 5
    self.size = 70000 #max size apparently 65520
    self.socket = None
    self.threads = []
    amount[0] = 0

  def open_socket(self):
    try:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        a = self.socket.bind((self.host, self.port))
    except socket.error, (value, message):
        if self.socket:
            self.socket.close()
        print "Could not open socket: " + message
        sys.exit(1)

  def run(self):
    self.open_socket()
    running = 1

    while running:
        try:
          data = self.socket.recv(self.size)
        except socket.error:
          #Socket closed on receive
          pass

        if data:
          amount[0] += len(data)
        else:
            amount[0] = 0
            running = 0

    print 'Received signal to stop'

    self.socket.close()

    for c in self.threads:
        c.running = 0
        c.join()
        
  def receive(self):
    running = 1
    while running:
        try:
          data, address = self.socket.recvfrom(self.size)
        except socket.error:
          #Socket closed on receive
          pass

        if data:
          amount[0] += len(data)
        else:
            amount[0] = 0
            running = 0

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

if __name__ == "__main__":

  try:
    port = sys.argv[1]  
  except:
    print '<port>'
    sys.exit(0)
  
  amount = []
  amount.append(0)
    
  s = Server(int(port))
  print 'Hit any key to terminate server'
  t = threading.Thread(target = s.run)
  t.setDaemon(False)
  t.start()
  print 'Starting Bandwidth monitor'

  b = BandwidthMonitor()    
  x = arange(0,100,1)
  y = []

  ion()#animated graphing

  while len(y) < 100:
    y.append(0)
  
  line, = plot(x,y,'r')
  axis(array([0, 100, 0, 140]))

  xticks([]) #removes x axis tick marks
  grid('on')
  title('UDP')
  ylabel('MB/s')

  while 1:
    b.initiate()
    time.sleep(1)
    b.terminate()
    speed = b.get_bandwidth()/(1000*1000) 
    print str(speed) + ' MBytes/second'
    y.pop(0)
    y.append(speed)
    line.set_ydata(y)
    draw()
