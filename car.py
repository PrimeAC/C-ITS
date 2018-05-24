import threading
import time
import datetime
import hashlib
import netifaces as ni
import communication
sem = threading.Semaphore()



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

table = {}  # creates a dictionary that saves all the neighbors status
sent_time = ""

f = open("taxi_february.txt", "r")  # opens the file taxi_february.txt on read mode


class Handler(threading.Thread):
    def __init__(self, msg, clientIP, clientPort):
        self.msg = msg
        self.clientIP = clientIP
        self.clientPort = clientPort

    def run(self):
        msg = self.msg.decode('utf-8').split("|")
        type = msg[0]

        if not msg:
            exit(-1, "Empty message!")

        elif type == "BEACON":
            nodeID = communication.converIpToNodeId(self.clientIP)
            print (nodeID, My_nodeID)
            if nodeID != My_nodeID:
                print("Message: [" + self.msg.decode('utf-8') + "] received on IP/PORT: [" + str(nodeID) + "," + str(self.clientIP) + "]")
                check(msg, nodeID)
                printTable()

        elif type == "DEN":
            nodeID = communication.converIpToNodeId(self.clientIP)
            if nodeID != My_nodeID:
                print("Message: [" + self.msg.decode('utf-8'))

    def Beacon_Sender(self):
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
            communication.Sender(communication.initializeSenderSocket(),self.message)
            sent_time = str(datetime.datetime.now().time())
            while True:
                if checkTimer() == True:
                    break

    def Den_Sender(self):
        global sent_time
        input("Press Enter to park... " + "\n")
        self.type = "DEN"
        self.msgID = self.msgID + 1
        self.event_type = FORWARD
        self.duration = TIME
        self.message = self.type + "|" + str(datetime.datetime.now().time()) + "|" + str(self.msgID) + "|" + self.event_type + "|" + self.duration
        print("Sent: " + self.message)
        communication.Sender(communication.initializeSenderSocket(),self.message)
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
    if nodeID in table:  # means that the table already has that node
        if checkMsgID(msgID, nodeID):  # valid message id
            sem.acquire()
            table[nodeID] = [latitude, longitude, time, msgID, str(datetime.datetime.now().time()).split(".")[0]]
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


socket = communication.initializeReceiverSocket()

while True:
    (ClientMsg, (ClientIP, ClientPort)) = communication.Receiver(socket)
    handler = Handler(ClientMsg,ClientIP,ClientPort)

    timer = Timer()

    handler.start()
    timer.start()

    threads = []

    # Add threads to thread list
    threads.append(handler)
    threads.append(timer)


    # Wait for all threads to complete
    for t in threads:
        t.join()
    f.close()  # closes the txt file
    print("Exiting Main Thread")

