#!/usr/bin/python

import socket
import time

socket.DCCP_SOCKOPT_PACKET_SIZE = 1
socket.DCCP_SOCKOPT_SERVICE = 2
socket.SOCK_DCCP = 6
socket.IPROTO_DCCP = 33
socket.SOL_DCCP = 269
packet_size = 256 #hmmm?
address = ('d38.narga.sun.ac.za',3002)


socket.DCCP_SOCKOPT_AVAILABLE_CCIDS = 12
socket.DCCP_SOCKOPT_CCID = 13
socket.DCCP_SOCKOPT_TX_CCID = 14
socket.DCCP_SOCKOPT_RX_CCID = 15

client = socket.socket(socket.AF_INET, socket.SOCK_DCCP, socket.IPROTO_DCCP) 

client.setsockopt(socket.SOL_DCCP, socket.DCCP_SOCKOPT_PACKET_SIZE, packet_size)
client.setsockopt(socket.SOL_DCCP, socket.DCCP_SOCKOPT_SERVICE, True)
print 'a'
client.connect(address)
print 'b'

buff = '\0' * 1024

print 'spamming server'
while True:
#  try:
    time.sleep(.0001) #.000001 -> this value is too small
    client.send(buff)
#  except socket.error: #if we are flooding it
#    time.sleep(.1) 


#recommend packet size: 1400
#ip header, 20 bytes, dccp, 32 bytes
#maximum transmission unit 1500 (UDP is like, what, something huge)
