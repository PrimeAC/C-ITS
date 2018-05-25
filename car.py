import threading, _thread
import time
import datetime
import communication
import test_carMovement
import netifaces as ni
import garage
#----------------------------------------------
#CONSTANTS
#----------------------------------------------

TYPE = 0
LATITUDE = 1
LONGITUDE = 2

neighbor_table={}  # creates a dictionary that saves all the neighbors status
DEN_msg_Id=0


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

def processMessager(msg, serverIp):
    msg = msg.decode('utf-8').split("|")
    type = msg[0]
    event_type = msg[3]
    description = msg[4]

    if not msg:
        exit(-1, "Empty message!")

    elif type == "BEACON":
        nodeID = communication.converIpToNodeId(serverIp[0])
        print (nodeID, myNodeID)
        if nodeID != myNodeID:
            tableUpdate(msg, nodeID)
            printTable()

    elif type == "DEN":
        nodeID = communication.converIpToNodeId(serverIp[0])
        if nodeID != myNodeID:
            if event_type == "-1":
                print (description) #if error print description of message
            elif event_type == "Movements":
                des = description.split(",")
                x = des[0]
                y = des[1]
                front_back = des[2]
                right_left = des[3]
                get_position = test_carMovement.virtualToRealMovement(front_back, right_left, x, y)
                if get_position != -1:
                    my_current_position_w.write(x + ";" + y)


def read_input():
    while True:
        i = input("Press E to park, S to leave \n")
        if i == "E":
            new_den_msg = garage.createDenResponse("RequestParking",(x,y))
            communication.Sender(senderSocket, new_den_msg)
        elif i == "S":
            new_den_msg = garage.createDenResponse("RequestExit",(x,y))
            communication.Sender(senderSocket, new_den_msg)


#------------------------------------------------
#INITIALIZATIONS
#------------------------------------------------

sem = threading.Semaphore()
receiverSocket = communication.initializeReceiverSocket()
senderSocket = communication.initializeSenderSocket()
myIP = ni.ifaddresses('en1')[ni.AF_INET6][0]['addr']
myNodeID = communication.converIpToNodeId(myIP)

my_current_position_r = open("position.txt", "r").readline()
my_current_position_w = open("position.txt", "w")

x,y = my_current_position_r.split(';')

print (x,y)

#----------------------------------------------
#CLASS
#----------------------------------------------


class Beacon_Service(threading.Thread):
    def __init__(self, f):
        threading.Thread.__init__(self)
        self.msgID = 0
        self.file = f
        self.type = "BEACON"

    def run(self):
        msg = msg.decode('utf-8').split("|")
        description = msg[4]
        des = description.split(",")
        x = des[0]
        y = des[1]
        msgID = self.msgID + 1
        message = self.type + "|" + x + "|" + y + "|" + str(datetime.datetime.now().time()) + "|" + str(msgID)
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
timer = Timer(1)
timer.start()
beaconService = Beacon_Service()
beaconService.start()

_thread.start_new_thread(read_input(),())

while True:
    (ServerMsg, (ServerIP)) = communication.Receiver(receiverSocket)
    processMessager(ServerMsg, ServerIP)


