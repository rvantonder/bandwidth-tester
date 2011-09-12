#!/usr/bin/python

import socket

socket.DCCP_SOCKOPT_PACKET_SIZE = 1
socket.DCCP_SOCKOPT_SERVICE = 2
socket.SOCK_DCCP = 6
socket.IPROTO_DCCP = 33
socket.SOL_DCCP = 269
packet_size = 256 #hmmm?
address = (socket.gethostname(),3001)


socket.DCCP_SOCKOPT_AVAILABLE_CCIDS = 12
socket.DCCP_SOCKOPT_CCID = 13
socket.DCCP_SOCKOPT_TX_CCID = 14
socket.DCCP_SOCKOPT_RX_CCID = 15


server,client = [socket.socket(socket.AF_INET, socket.SOCK_DCCP, socket.IPROTO_DCCP) for i in range(2)]

for s in (server, client):
  s.setsockopt(socket.SOL_DCCP, socket.DCCP_SOCKOPT_PACKET_SIZE, packet_size)
  s.setsockopt(socket.SOL_DCCP, socket.DCCP_SOCKOPT_SERVICE, True)

server.bind(address)
server.listen(1)
client.connect(address)
s,a = server.accept()


while True:
  client.send(raw_input(">>"))
  print s.recv(1024)



#recommend packet size: 1400
#ip header, 20 bytes, dccp, 32 bytes
#maximum transmission unit 1500 (UDP is like, what, something huge)
