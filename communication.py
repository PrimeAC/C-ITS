import socket
import threading
sem = threading.Semaphore()
import struct
import time
import datetime
import hashlib
import netifaces as ni

BUFFSIZE = 1024
PORT = 5005
SCOPEID = 5  # Change value for your network interface index


def initializeSocket():

    group_bin = socket.inet_pton(socket.AF_INET6, 'ff02::0')
    mreq = group_bin + struct.pack('@I', SCOPEID)

    serverSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    serverSocket.bind(('', PORT))
    print("Server listening for messages on port: " + str(PORT))
    return serverSocket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

def Receiver(serverSocket):
    while True:
        (ClientMsg, (ClientIP, ClientPort, ClientFlow, ClientScopeId)) = serverSocket.recvfrom(BUFFSIZE)