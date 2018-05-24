import threading
import communication
import datetime
import time
import netifaces as ni

#----------------------------------------------
#CONSTANTS
#----------------------------------------------

threads = []
neighbor_table={}  # creates a dictionary that saves all the neighbors status

#------------------------------------------------
#FUNCTIONS
#------------------------------------------------
def checkTimer(sent_time):
    now = datetime.datetime.strptime(str(datetime.datetime.now().time()).split(".")[0], '%H:%M:%S')
    last_sent = datetime.datetime.strptime(sent_time.split(".")[0], '%H:%M:%S')
    time.sleep(1)

    if (now - last_sent).total_seconds() >= 4:
        return True
    return False

def validateTime():
    timedOut = False
    sem.acquire()
    for key in neighbor_table:
        lastUpdate = datetime.datetime.strptime(neighbor_table[key][4], '%H:%M:%S')
        now = datetime.datetime.strptime(str(datetime.datetime.now().time()).split(".")[0], '%H:%M:%S')
        difference = now - lastUpdate
        if difference.total_seconds() > 30:
            timedOut = True
            print("Time out:")
            print(str(key) + "|" + neighbor_table[key][0] + "|" + neighbor_table[key][1] + "|" + neighbor_table[key][2] +
                "|" + neighbor_table[key][3] + "|" + neighbor_table[key][4])
            del neighbor_table[key]
            break
    sem.release()
    if timedOut:
        sem.acquire()
        printTable()
        sem.release()

def checkMsgID(msgID, nodeID):
    sem.acquire()
    if int(neighbor_table[nodeID][3]) < int(msgID):
        sem.release()
        return True
    sem.release()
    return False

def tableUpdate(msg, nodeID):
    latitude = msg[1]
    longitude = msg[2]
    time = msg[3].split(".")[0]
    msgID = msg[4]
    if nodeID in neighbor_table:  # means that the table already has that node
        if checkMsgID(msgID, nodeID):  # valid message id
            sem.acquire()
            neighbor_table[nodeID] = [latitude, longitude, time, msgID, str(datetime.datetime.now().time()).split(".")[0]]
            sem.release()
        else:
            print("Invalid message ID")
    else:
        # else we need to add it to the table
        sem.acquire()
        neighbor_table[nodeID] = [latitude, longitude, time, msgID, str(datetime.datetime.now().time()).split(".")[0]]
        sem.release()

def printTable():
    print("Neighbor table:")
    sem.acquire()
    for key in neighbor_table:
        print(str(key) + "|" + neighbor_table[key][0] + "|" + neighbor_table[key][1] + "|" + neighbor_table[key][2] +
              "|" + neighbor_table[key][3] + "|" + neighbor_table[key][4])
    sem.release()

#------------------------------------------------
#INITIALIZATIONS
#------------------------------------------------
sem = threading.Semaphore()
receiverSocket = communication.initializeReceiverSocket()
senderSocket = communication.initializeSenderSocket()
myIP = ni.ifaddresses('en1')[ni.AF_INET6][0]['addr']
myNodeID = communication.converIpToNodeId(myIP)

#----------------------------------------------
#CLASS
#----------------------------------------------

class Handler(threading.Thread):
    def __init__(self, msg, clientIP):
        self.msg = msg
        self.clientIP = clientIP

    def run(self):
        msg = self.msg.decode('utf-8').split("|")
        type = msg[0]

        if not msg:
            exit(-1, "Empty message!")

        elif type == "BEACON":
            nodeID = communication.converIpToNodeId(self.clientIP)
            print (nodeID, myNodeID)
            if nodeID != myNodeID:
                print("Message: [" + self.msg.decode('utf-8') + "] received on IP/PORT: [" + str(nodeID) + "," + str(self.clientIP) + "]")
                tableUpdate(msg, nodeID)
                printTable()

        elif type == "DEN":
            nodeID = communication.converIpToNodeId(self.clientIP)
            if nodeID != myNodeID:
                print("Message: [" + self.msg.decode('utf-8'))

class Beacon_Service(threading.Thread):

    def __init__(self, f):
        self.msgID = 0
        self.file = f
        self.type = "BEACON"

    def run(self):
        for line in self.file:
            gps_message = line.split(";")[2].split("(")[1].split(" ")
            latitude = gps_message[0]
            longitude = gps_message[1].split(")")[0]
            msgID = self.msgID + 1
            message = self.type + "|" + latitude + "|" + longitude + "|" + str(datetime.datetime.now().time()) + "|" + str(
                msgID)
            print("Sent: " + message)
            communication.Sender(senderSocket,message)
            sent_time = str(datetime.datetime.now().time())
            while True:
                if checkTimer(sent_time) == True:
                    break

class Timer(threading.Thread):
    def __init__(self, loopTime):
        threading.Thread.__init__(self)
        self.loopTime = loopTime

    def run(self):
        while True:
            validateTime()
            time.sleep(self.loopTime)

#-------------------------------------------------
#MAIN
#-------------------------------------------------
beaconService = Beacon_Service(open("taxi_february.txt", "r")) # opens the file taxi_february.txt on read mode
beaconService.run()

while True:
    (ClientMsg, (ClientIP, ClientPort)) = communication.Receiver(receiverSocket)
    handler = Handler(ClientMsg, ClientIP, ClientPort)
    # Add threads to thread list
    threads.append(handler)
    handler.run()
