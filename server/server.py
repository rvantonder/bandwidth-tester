#!/usr/bin/env python

"""
An echo server that uses threads to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
"""

import select
import socket
import sys
import threading
import logging
import os
import pickle
import time

class ServerLogger:
  def __init__(self, logfilename):
    if os.path.isfile(logfilename):
      os.remove(logfilename)

    self.logger = logging.getLogger("serverlogger")
    self.hdlr = logging.FileHandler(logfilename)
    self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(threadName)s %(message)s')
    self.hdlr.setFormatter(self.formatter)
    self.logger.addHandler(self.hdlr)
    self.logger.setLevel(logging.INFO)

def isOpen(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      s.connect((ip, port))
      s.shutdown(2)
      serverLogger.logger.info('port '+str(port)+' open')
    except:
      serverLogger.logger.warn('port '+str(port)+' blocked')

class Server:
  def __init__(self, port):
    self.host = ''
    self.port = port 
    self.backlog = 5
    self.size = 1024
    self.socket = None
    self.threads = []

  def open_socket(self):
    serverLogger.logger.info("Attempting to open socket")
    try:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a = self.socket.bind((self.host,self.port))
        b = self.socket.listen(self.backlog)
    except socket.error, (value,message):
        if self.socket:
            self.socket.close()
        serverLogger.logger.warn("Could not open socket")
        print "Could not open socket: " + message
        sys.exit(1)
    serverLogger.logger.info("Socket open")

  def run(self):
    self.open_socket()
    input = [self.socket,sys.stdin]
    running = 1

    serverLogger.logger.info("Running")
    while running:
        inputready,outputready,exceptready = select.select(input,[],[])

        for s in inputready:

            if s == self.socket:
                serverLogger.logger.info("New connection incoming")  
                c = Client(self.socket.accept())
                c.setDaemon(True)
                c.start()
                self.threads.append(c)

            elif s == sys.stdin:
                # handle standard input
                junk = sys.stdin.readline()
                running = 0

    serverLogger.logger.info('Server shutdown requested.')
    serverLogger.logger.info('Close client sockets.')
  
    serverLogger.logger.info('Closing server socket')
    self.socket.close()

    serverLogger.logger.info('Terminating client threads')
    for c in self.threads:
        c.join()

    serverLogger.logger.info('Client threads terminated')

class Client(threading.Thread): #client thread
  def __init__(self,(client,address)):
    threading.Thread.__init__(self) 
    self.client = client #the socket
    self.address = address #the address
    self.size = 1024 #the message size
    self.username = None
    self.running = 1 #running state variable

  def run(self):
    while self.running:
        try:
          data = self.client.recv(self.size)
        except socket.error:
          serverLogger.logger.warn("socket closed on receive")

        if data:
          #print 'data length',len(data)
          #print 'data',data
          print data
        else:
            self.client.close()
            serverLogger.logger.info('client disconnected')
            self.running = 0

    serverLogger.logger.info("Thread terminating") 

if __name__ == "__main__":
  try:
    connections = {} 
    
    serverLogger = ServerLogger('server.log') 
    serverLogger.logger.info("starting server")
    s = Server(int(sys.argv[1]))
    print 'Hit any key to terminate server'
    s.run() 
  except IndexError:
    print 'Usage: python server.py <port number>'
