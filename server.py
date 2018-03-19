import socket
import struct

SCOPEID = 3 #Change value for your network interface index
PORT = 5005

group_bin = socket.inet_pton(socket.AF_INET6, 'ff02::0')
mreq = group_bin + struct.pack('@I', 0) 

ServerSock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
ServerSock.bind(('', PORT))
print("Server listening for messages on port: " + str(PORT))

ServerSock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

(ClientMsg, (ClientIP, ClientPort, ClientFlow, ClientScopeId)) = ServerSock.recvfrom (1024)
print("Message: [" + ClientMsg.decode('utf-8') + "] received on IP/PORT: [" + ClientIP + "," +
      str(ClientPort) + "]")
