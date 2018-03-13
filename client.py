import socket


ClientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

dest_addr = input("Enter destination IP Address: ")
message = input("Enter the message to send and press ENTER: ")
print("Sending message [" + message + "] to " + dest_addr)
ClientSock.sendto(message.encode(), (dest_addr, 5005))
print("Message sent!")
