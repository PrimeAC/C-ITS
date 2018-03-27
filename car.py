import socket
import threading 
import struct
import time
import datetime


BUFFSIZE = 1024
PORT=5005
SCOPEID = 3 #Change value for your network interface index
loopTime = 1 

table = {}  #creates a dictionary that saves all the neighbors status

class Receiver(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.port = PORT
		self.bufsize = BUFFSIZE
		
		group_bin = socket.inet_pton(socket.AF_INET6, 'ff02::0')
		mreq = group_bin + struct.pack('@I', SCOPEID) 

		self.serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		self.serverSocket.bind(('', PORT))
		print("Server listening for messages on port: " + str(PORT))
		self.serverSocket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

	def run(self):
		while True:
			#time.sleep(5)
			(ClientMsg, (ClientIP, ClientPort, ClientFlow, ClientScopeId)) = self.serverSocket.recvfrom (self.bufsize)
			if not ClientMsg:
				continue
			print("Message: [" + ClientMsg.decode('utf-8') + "] received on IP/PORT: [" + ClientIP + "," + str(ClientPort) + "]")
			check(ClientMsg, ClientIP)
			'''ClientMsg = ClientMsg.decode('utf-8').split("|")
			msg = ClientMsg[0]
			time = ClientMsg[1].split(".")[0]
			msgID = ClientMsg[2]
			print(str(msg) + "------" + str(time) + "****" + str(msgID))
			table[ClientIP] = ["lat", "long", time, msgID, str(datetime.datetime.now().time())]
			print(table)'''
	              


class Sender(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.port = PORT
		self.bufsize = BUFFSIZE
		self.msgID = 0   #message ID starts at zero and is incremented every time a user sends a message

		ttl_bin = struct.pack('@i', SCOPEID)
		self.dest_addr = 'ff02::0' 

		self.clientSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		self.clientSocket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)

	def run(self):
		while True:
			#time.sleep(5)
			message = input("Enter the message to send and press ENTER: ")
			if not message:
				continue
			print("Sending message [" + message + "] to " + self.dest_addr + " time: " + str(datetime.datetime.now().time()))
			self.msgID = self.msgID + 1
			print(self.msgID)
			message = message + "|" + "AS" + "|" + str(datetime.datetime.now().time()) + "|" + str(self.msgID)
			self.clientSocket.sendto(message.encode(), (self.dest_addr, PORT, 0, SCOPEID))
			print("Message sent!")



class Loop(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.loopTime = loopTime
		

	def run(self):
		while True:
			validateTime()
			time.sleep(self.loopTime)
			

def validateTime():
	print("VALIDATE--------")
	for key in table:
		lastUpdate = datetime.datetime.strptime(table[key][4], '%H:%M:%S')
		now = datetime.datetime.strptime(str(datetime.datetime.now().time()).split(".")[0], '%H:%M:%S')
		difference = now - lastUpdate
		print("KEY: " + key + "last: " + str(lastUpdate) + "now: " + str(now) + "difference: " + str(difference.total_seconds()))
		if difference.total_seconds() > 30:
			del table[key]
			break



def checkMsgID(msgID, ClientIP):
	if ClientIP in table:
		if table[ClientIP][3] < msgID:
			print("msgID valid")
			return True
		print("msgID invalid")
		return False
	return True

	

def check(ClientMsg, ClientIP):
	ClientMsg = ClientMsg.decode('utf-8').split("|")
	latitude = ClientMsg[0]
	longitude = ClientMsg[1]
	time = ClientMsg[2].split(".")[0]
	msgID = ClientMsg[3]
	if ClientIP in table:   #means that the table already has that node
		print("ja estou " + msgID)
		if checkMsgID(msgID, ClientIP): #valid message id
			table[ClientIP] = [latitude, longitude, time, msgID, str(datetime.datetime.now().time()).split(".")[0]]
			print("adicionei")
		else:
			#invalid message id
			print("Nao adicionei")

	else:
		#else we need to add it to the table	
		table[ClientIP] = [latitude, longitude, time, msgID, str(datetime.datetime.now().time()).split(".")[0]]
		print(table)


receiver = Receiver()
sender = Sender()
timer = Loop()


receiver.start()
sender.start()
timer.start()

threads = []

# Add threads to thread list
threads.append(receiver)
threads.append(sender)
threads.append(timer)


# Wait for all threads to complete
for t in threads:
	t.join()
print("Exiting Main Thread")
