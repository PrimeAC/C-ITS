import socket
import threading
sem = threading.Semaphore()
import struct
import time
import datetime
import hashlib
import netifaces as ni

#import test_motor.py

BUFFSIZE = 1024
PORT = 5005
SCOPEID = 5  # Change value for your network interface index
loopTime = 1

TYPE = 0
LATITUDE = 1
LONGITUDE = 2

FORWARD = "126"
BACKWARD = "125"
RIGHT = "124"
LEFT = "123"
TIME = "15"
STOP = "49"


get_addr = ni.ifaddresses('en1')
ip = get_addr[ni.AF_INET6][0]['addr']

h = hashlib.blake2s(digest_size=2)
h.update(ip.encode('utf-8'))
My_nodeID = int(h.hexdigest(), 16)
print (My_nodeID)

table = {}  # creates a dictionary that saves all the neighbors status
sent_time = ""

f = open("taxi_february.txt", "r")  # opens the file taxi_february.txt on read mode


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
            (ClientMsg, (ClientIP, ClientPort, ClientFlow, ClientScopeId)) = self.serverSocket.recvfrom(self.bufsize)
            msg = ClientMsg.decode('utf-8').split("|")
            type = msg[0]
            if not msg:
                continue
            elif type == "beacon":
                h = hashlib.blake2s(digest_size=2)
                h.update(ClientIP.encode('utf-8'))
                nodeID = int(h.hexdigest(), 16)
                if nodeID != My_nodeID:
                    print("Message: [" + ClientMsg.decode('utf-8') + "] received on IP/PORT: [" + str(nodeID) + "," + str(ClientPort) + "]")
                    check(msg, nodeID)
                    printTable()
                else:
                    break
            elif type == "DEN":
                print("Message: [" + ClientMsg.decode('utf-8'))


class Beacon(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.port = PORT
        self.bufsize = BUFFSIZE
        self.msgID = 0  # message ID starts at zero and is incremented every time a user sends a message

        ttl_bin = struct.pack('@i', SCOPEID)
        self.dest_addr = 'ff02::0'

        self.clientSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.clientSocket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)

    def run(self):
        global sent_time
        for line in f:
            self.gps_message = line.split(";")[2].split("(")[1].split(" ")
            self.type = "beacon"
            self.latitude = self.gps_message[0]
            self.longitude = self.gps_message[1].split(")")[0]
            self.msgID = self.msgID + 1
            self.message = self.type + "|" + self.latitude + "|" + self.longitude + "|" + str(datetime.datetime.now().time()) + "|" + str(
                self.msgID)
            print("Sent: " + self.message)
            self.clientSocket.sendto(self.message.encode(), (self.dest_addr, PORT, 0, SCOPEID))
            sent_time = str(datetime.datetime.now().time())
            while True:
                if checkTimer() == True:
                    break


class DEN_Sender(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.port = PORT
        self.bufsize = BUFFSIZE
        self.msgID = 0  # message ID starts at zero and is incremented every time a user sends a message

        ttl_bin = struct.pack('@i', SCOPEID)
        self.dest_addr = 'ff02::0'

        self.clientSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        self.clientSocket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)

    def run(self):
        global sent_time
        input("Press Enter to park... " + "\n")
        self.type = "DEN"
        self.msgID = self.msgID + 1
        self.event_type = FORWARD
        self.duration = TIME
        self.message = self.type + "|" + str(datetime.datetime.now().time()) + "|" + str(self.msgID) + "|" + self.event_type + "|" + self.duration
        print("Sent: " + self.message)
        self.clientSocket.sendto(self.message.encode(), (self.dest_addr, PORT, 0, SCOPEID))
        sent_time = str(datetime.datetime.now().time())


class Timer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.loopTime = loopTime

    def run(self):
        while True:
            validateTime()
            time.sleep(self.loopTime)


def checkTimer():
    now = datetime.datetime.strptime(str(datetime.datetime.now().time()).split(".")[0], '%H:%M:%S')
    last_sent = datetime.datetime.strptime(sent_time.split(".")[0], '%H:%M:%S')
    time.sleep(1)

    if (now - last_sent).total_seconds() >= 4:
        return True
    return False



def validateTime():
    timedOut = False
    sem.acquire()
    for key in table:
        lastUpdate = datetime.datetime.strptime(table[key][4], '%H:%M:%S')
        now = datetime.datetime.strptime(str(datetime.datetime.now().time()).split(".")[0], '%H:%M:%S')
        difference = now - lastUpdate
        if difference.total_seconds() > 30:
            timedOut = True
            print("Time out:")
            print(
            str(key) + "|" + table[key][0] + "|" + table[key][1] + "|" + table[key][2] + "|" + table[key][3] + "|" +
            table[key][4])
            del table[key]
            break
    sem.release()
    if timedOut:
        sem.acquire()
        printTable()
        sem.release()


def checkMsgID(msgID, nodeID):
    sem.acquire()
    if int(table[nodeID][3]) < int(msgID):
        sem.release()
        return True
    sem.release()
    return False


def check(msg, nodeID):
    latitude = msg[1]
    longitude = msg[2]
    time = msg[3].split(".")[0]
    msgID = msg[4]
    if nodeID in table and nodeID != My_nodeID:  # means that the table already has that node
        if checkMsgID(msgID, nodeID):  # valid message id
            sem.acquire()
            print ("Node_ID = " + str(nodeID))
            table[nodeID] = [latitude, longitude, time, msgID, str(datetime.datetime.now().time()).split(".")[0]]
            print (len(table))
            sem.release()
        else:
            print("Invalid message ID")
    else:
        # else we need to add it to the table
        sem.acquire()
        table[nodeID] = [latitude, longitude, time, msgID, str(datetime.datetime.now().time()).split(".")[0]]
        sem.release()


def printTable():
    print("Neighbor table:")
    sem.acquire()
    for key in table:
        print(str(key) + "|" + table[key][0] + "|" + table[key][1] + "|" + table[key][2] + "|" + table[key][3] + "|" +
              table[key][4])
    sem.release()

receiver = Receiver()
beacon = Beacon()
den = DEN_Sender()
timer = Timer()

receiver.start()
beacon.start()
den.start()
timer.start()

threads = []

# Add threads to thread list
threads.append(receiver)
threads.append(beacon)
threads.append(den)
threads.append(timer)


# Wait for all threads to complete
for t in threads:
    t.join()
f.close()  # closes the txt file
print("Exiting Main Thread")
