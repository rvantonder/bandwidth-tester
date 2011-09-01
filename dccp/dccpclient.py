#!/usr/bin/python

import socket
import time
import sys

socket.DCCP_SOCKOPT_PACKET_SIZE = 1
socket.DCCP_SOCKOPT_SERVICE = 2
socket.SOCK_DCCP = 6
socket.IPROTO_DCCP = 33
socket.SOL_DCCP = 269
packet_size = 256 


try:
  #address = (sys.argv[1]+'.narga.sun.ac.za',int(sys.argv[2]))
  address = (sys.argv[1],int(sys.argv[2]))
  #address = ('146.232.49.32',int(sys.argv[2]))
  #address = ('localhost',int(sys.argv[2]))
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
print 'connecting...'
client.connect(address) #XXX problem here?
print 'connected...'

buff = '\0' * 1024

print 'spamming server'
while True:
#  try:
    time.sleep(.00001) #.000001 -> this value is too small
    client.send(buff)
#  except socket.error: #if we are flooding it
#    time.sleep(.1) 


#recommend packet size: 1400
#ip header, 20 bytes, dccp, 32 bytes
#maximum transmission unit 1500 (UDP is like, what, something huge)
