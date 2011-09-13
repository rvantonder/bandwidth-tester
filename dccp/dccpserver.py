#!/usr/bin/python

'''A DCCP server for receiving data from client.'''

from numpy import *
from pylab import *

import socket
import time
import threading
import sys
import select

socket.DCCP_SOCKOPT_PACKET_SIZE = 1
socket.DCCP_SOCKOPT_SERVICE = 2
socket.SOCK_DCCP = 6
socket.IPROTO_DCCP = 33
socket.SOL_DCCP = 269
packet_size = 512

socket.DCCP_SOCKOPT_AVAILABLE_CCIDS = 12
socket.DCCP_SOCKOPT_CCID = 13
socket.DCCP_SOCKOPT_TX_CCID = 14
socket.DCCP_SOCKOPT_RX_CCID = 15

global amount

class DCCPServer:
  def __init__(self, port):
    amount[0] = 0

    self.server = socket.socket(socket.AF_INET, socket.SOCK_DCCP, socket.IPROTO_DCCP)

    self.server.setsockopt(socket.SOL_DCCP, socket.DCCP_SOCKOPT_PACKET_SIZE, packet_size)
    self.server.setsockopt(socket.SOL_DCCP, socket.DCCP_SOCKOPT_SERVICE, True)
    self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    self.server.bind(('0.0.0.0', port))
    self.server.listen(1)

    self.threads = []

  def run(self):
    input = [self.server, sys.stdin]
    running = 1

    while running:
        inputready, outputready, exceptready = select.select(input, [], [])

        for s in inputready:

            if s == self.server:
                # create new thread for incoming connection
                c = Client(self.server.accept())
                c.setDaemon(True)
                c.start()
                self.threads.append(c)

            elif s == sys.stdin:
                # handle standard input
                line = sys.stdin.readline()
                if line.strip() == 'q':
                  running = 0
                else:
                  print "Type 'q' to stop the server"

    print 'Received signal to stop'

    self.socket.close()

    for c in self.threads:
        c.running = 0
        c.join()

class Client(threading.Thread): #client thread
  def __init__(self,(client, address)):
    threading.Thread.__init__(self) 
    self.client = client #the socket
    self.address = address #the address
    self.size = 1024 #the message size
    self.running = 1 #running state variable

  def run(self):
    while self.running:
        try:
          data = self.client.recv(self.size)
        except socket.error:
          print 'receive error'

        if data:
          amount[0] += len(data)
        else:
            amount[0] = 0
            self.client.close()
            self.running = 0

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

    amount = []
    amount.append(0)

    try:
      port = sys.argv[1]  
    except:
      print '<port>'
      sys.exit(0)

    s = DCCPServer(int(port))
    t = threading.Thread(target = s.run)
    t.setDaemon(False)
    t.start()
 
    print 'Starting Bandwidth monitor'

    b = BandwidthMonitor()    

    x = arange(0,100,1)
    y = []
        
    ion() #animated graphs

    while len(y) < 100:
      y.append(0)

    line, = plot(x,y,'b')
    axis(array([0,100,0,140]))

    xticks([])
    grid('on')
    title('DCCP')
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
