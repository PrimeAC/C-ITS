import socket

SCOPEID = 3 #Change value for your network interface index
PORT = 5005

ClientSock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
dest_addr = input("Enter destination IP Address: ")
message = input("Enter the message to send and press ENTER: ")
print("Sending message [" + message + "] to " + dest_addr)
ClientSock.sendto(message.encode(), (dest_addr, PORT, 0, SCOPEID))
print("Message sent!")
