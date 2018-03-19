import socket
import struct

SCOPEID = 3 #Change value for your network interface index
PORT = 5005
ttl_bin = struct.pack('@i', 3)

ClientSock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
dest_addr = 'ff02::0' #input("Enter destination IP Address: ")
message = input("Enter the message to send and press ENTER: ")
print("Sending message [" + message + "] to " + dest_addr)
ClientSock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)
ClientSock.sendto(message.encode(), (dest_addr, PORT, 0, SCOPEID))
print("Message sent!")
