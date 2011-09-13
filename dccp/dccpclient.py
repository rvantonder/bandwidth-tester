#!/usr/bin/python

import socket
import time
import sys

socket.DCCP_SOCKOPT_PACKET_SIZE = 1
socket.DCCP_SOCKOPT_SERVICE = 2
socket.SOCK_DCCP = 6
socket.IPROTO_DCCP = 33
socket.SOL_DCCP = 269
#packet_size = 256 
packet_size = 512


try:
  #address = (sys.argv[1]+'.narga.sun.ac.za',int(sys.argv[2]))
  address = (sys.argv[1],int(sys.argv[2]))
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
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #TODO only in server?

print 'connecting...'
client.connect(address) #XXX problem here?
print 'connected...'

#buff = '\0' * 1024
buff = 1400 * '\0'

print 'spamming server'
while True:
   try:
    time.sleep(.0025) #.000001 -> this value is too small .000005
    client.send(buff)

    #num_bytes_sent = 0
    #while (num_bytes_sent == 0):
    #  num_bytes_sent = client.send(buff)

   except socket.error as (errno, strerror): #if we are flooding it
    if errno == 32 or errno == 104:
      print 'Connection lost, fatal'
      sys.exit(1)
    #print num_bytes_sent
    #print 'damn'
    #pass 


#recommend packet size: 1400
#ip header, 20 bytes, dccp, 32 bytes
#maximum transmission unit 1500 (UDP is like, what, something huge)
