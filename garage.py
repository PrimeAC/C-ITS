import threading
import communication
import datetime
import time
import garageManager
import netifaces as ni

#----------------------------------------------
#CONSTANTS
#----------------------------------------------

threads = []
neighbor_table={}  # creates a dictionary that saves all the neighbors status
DEN_msg_Id=0
inOperation=False

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

def getPositionByNodeId(nodeID):
    if nodeID in neighbor_table:
        return [neighbor_table[nodeID][0],neighbor_table[nodeID][1]]
    else:
        return None

def printTable():
    print("Neighbor table:")
    sem.acquire()
    for key in neighbor_table:
        print(str(key) + "|" + neighbor_table[key][0] + "|" + neighbor_table[key][1] + "|" + neighbor_table[key][2] +
              "|" + neighbor_table[key][3] + "|" + neighbor_table[key][4])
    sem.release()


def createDenResponse(event_type, description):
    type = "DEN"
    time = str(datetime.datetime.now().time())
    msgId = DEN_msg_Id + 1
    msg = type + "|" + time + "|" + str(msgId) + "|" + event_type + "|" + description
    return msg

#------------------------------------------------
#INITIALIZATIONS
#------------------------------------------------
sem = threading.Semaphore()
receiverSocket = communication.initializeReceiverSocket()
senderSocket = communication.initializeSenderSocket()
myIP = ni.ifaddresses('en0')[ni.AF_INET6][0]['addr']
myNodeID = communication.converIpToNodeId(myIP)

#----------------------------------------------
#CLASS
#----------------------------------------------

class Handler(threading.Thread):
    def __init__(self, msg, clientIP):
        threading.Thread.__init__(self)
        self.msg = msg
        self.clientIP = clientIP

    def run(self):
        msg = self.msg.decode('utf-8').split("|")
        type = msg[0]

        if not msg:
            exit(-1, "Empty message!")

        elif type == "BEACON":
            nodeID = communication.converIpToNodeId(self.clientIP[0])
            print (nodeID, myNodeID)
            if nodeID != myNodeID:
                print("Message: [" + self.msg.decode('utf-8') + "] received on IP/PORT: [" + str(nodeID) + "," + str(self.clientIP) + "]")
                tableUpdate(msg, nodeID)
                printTable()

        elif type == "DEN":
            nodeID = communication.converIpToNodeId(self.clientIP[0])
            if nodeID != myNodeID:

                if inOperation:
                    den_msg = createDenResponse("-1", "Parking/Exiting process in progress.")
                    communication.Sender(senderSocket, den_msg)
                else:
                    if msg[3] == "RequestParking":
                        currentPosition = msg[4].split(",")
                        path = garageManager.pathFinder(currentPosition)

                        if path is None: #If no parking spaces are available
                            den_msg = createDenResponse("-1", "No parking spaces available")
                            communication.Sender(senderSocket, den_msg)
                        else:
                            for step in path:
                                den_msg = createDenResponse("Movement", str(step))
                                communication.Sender(senderSocket, den_msg)

                                #Wait for beacon confirming position changed
                                while neighbor_table[nodeID][0] != step[0] and neighbor_table[nodeID][1] != step[1]:
                                    time.sleep(1)

                            den_msg = createDenResponse("ParkingDone", "Parking operation sucessefull")
                            communication.Sender(senderSocket, den_msg)


                    elif msg[3] == "RequestExit":
                        currentPosition = msg[4].split(",")
                        path = garageManager.pathFinder(currentPosition)

                        if path is None: #If no parking spaces are available
                            den_msg = createDenResponse("-1", "It was not possible to calculate a exit route")
                            communication.Sender(senderSocket, den_msg)
                        else:
                            for step in path:
                                den_msg = createDenResponse("Movement", str(step))
                                communication.Sender(senderSocket, den_msg)

                                #Wait for beacon confirming position changed
                                while neighbor_table[nodeID][0] != step[0] and neighbor_table[nodeID][1] != step[1]:
                                    time.sleep(1)

                            den_msg = createDenResponse("ExitDone", "You can drive away now")
                            communication.Sender(senderSocket, den_msg)


#-------------------------------------------------
#MAIN
#-------------------------------------------------

while True:
    (ClientMsg, (ClientIP)) = communication.Receiver(receiverSocket)
    handler = Handler(ClientMsg, ClientIP)
    # Add threads to thread list
    threads.append(handler)
    handler.start()
