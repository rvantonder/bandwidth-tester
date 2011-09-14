#!/usr/bin/python

'''A DCCP client for data transmission to server.'''

import socket
import time
import sys

socket.DCCP_SOCKOPT_PACKET_SIZE = 1
socket.DCCP_SOCKOPT_SERVICE = 2
socket.SOCK_DCCP = 6
socket.IPROTO_DCCP = 33
socket.SOL_DCCP = 269
packet_size = 512

try:
  address = (sys.argv[1], int(sys.argv[2]))
except:
  print '<ip> <port>'
  sys.exit(0)

socket.DCCP_SOCKOPT_AVAILABLE_CCIDS = 12
socket.DCCP_SOCKOPT_CCID = 13
socket.DCCP_SOCKOPT_TX_CCID = 14
socket.DCCP_SOCKOPT_RX_CCID = 15

client = socket.socket(socket.AF_INET, socket.SOCK_DCCP, socket.IPROTO_DCCP) 

client.setsockopt(socket.SOL_DCCP, socket.DCCP_SOCKOPT_PACKET_SIZE, packet_size)
client.setsockopt(socket.SOL_DCCP, socket.DCCP_SOCKOPT_SERVICE, True)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

print 'connecting...'

try:
  client.connect(address)
except socket.error as (errno, strerror):
  #for connecting dccp clients en masse, ignore error 87 'too many users'
  if not(errno == 87):
    print 'Error, server refused connection'
    sys.exit(1)
 
print 'connected...'

buff = 1400 * '\0'

print 'spamming server'
while True:
   try:
    time.sleep(.0025)
    client.send(buff)
   except socket.error as (errno, strerror):
    #Congestion control protocol might refuse to send (error 11), in which case, retry. 
    if (errno == 32) or (errno == 104):
      #Server has terminated.
      print 'Connection lost, fatal'
      sys.exit(1)
