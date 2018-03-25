import socket
import threading 
import struct
import time


PORT=5005
SCOPEID = 3 #Change value for your network interface index

class Receiver(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.port = PORT
		self.bufsize = 1024
		group_bin = socket.inet_pton(socket.AF_INET6, 'ff02::0')
		mreq = group_bin + struct.pack('@I', 0) 

		self.socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		self.socket.bind(('', PORT))
		#ServerSock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		#ServerSock.bind(('', PORT))
		print("Server listening for messages on port: " + str(PORT))
		#ServerSock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)	
		self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

	def run(self):
		while True:
			time.sleep(5)
			#(ClientMsg, (ClientIP, ClientPort, ClientFlow, ClientScopeId)) = ServerSock.recvfrom (self.bufsize)
			(ClientMsg, (ClientIP, ClientPort, ClientFlow, ClientScopeId)) = self.socket.recvfrom (self.bufsize)
			if not ClientMsg:
				continue
			print("Message: [" + ClientMsg.decode('utf-8') + "] received on IP/PORT: [" + ClientIP + "," + str(ClientPort) + "]")
	              


class Sender(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.port = PORT
		self.bufsize = 1024

		ttl_bin = struct.pack('@i', 3)
		self.dest_addr = 'ff02::0' #input("Enter destination IP Address: ")

		self.socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)
		#ClientSock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		#ClientSock.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)

	def run(self):
		while True:
			time.sleep(5)
			message = input("Enter the message to send and press ENTER: ")
			if not message:
				continue
			print("Sending message [" + message + "] to " + self.dest_addr)
			self.socket.sendto(message.encode(), (self.dest_addr, PORT, 0, SCOPEID))
			#ClientSock.sendto(message.encode(), (self.dest_addr, PORT, 0, SCOPEID))
			print("Message sent!")



receiver = Receiver()
sender = Sender()

receiver.start()
sender.start()

threads = []

# Add threads to thread list
threads.append(receiver)
threads.append(sender)

# Wait for all threads to complete
for t in threads:
	t.join()
print("Exiting Main Thread")
