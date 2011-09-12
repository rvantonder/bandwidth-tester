import socket
import sys

socket.DCCP_SOCKOPT_PACKET_SIZE = 1
socket.DCCP_SOCKOPT_SERVICE     = 2
socket.SOCK_DCCP                = 6
socket.IPPROTO_DCCP             = 33
socket.SOL_DCCP                 = 269
packet_size                     = 256

try:
  address                         = (socket.gethostname(),int(sys.argv[1]))
except:
  print '<port>'
  sys.exit(0)

# Create sockets
server,client = [socket.socket(socket.AF_INET, socket.SOCK_DCCP, 
                               socket.IPPROTO_DCCP) for i in range(2)]
for s in (server,client):
    s.setsockopt(socket.SOL_DCCP, socket.DCCP_SOCKOPT_PACKET_SIZE, packet_size)
    s.setsockopt(socket.SOL_DCCP, socket.DCCP_SOCKOPT_SERVICE, True)

# Connect sockets
server.bind(address)
server.listen(1)
#client.connect(address)
s,a = server.accept()

# Echo
while True:
    #client.send(raw_input("IN: "))
    print "OUT:", s.recv(1024)

