import socket
import threading
sem = threading.Semaphore()
import struct
import hashlib

BUFFSIZE = 1024
PORT = 5005
SCOPEID = 5  # Change value for your network interface index


def converIpToNodeId(originalIp):
    h = hashlib.blake2s(digest_size=2)
    h.update(originalIp.encode('utf-8'))
    nodeId = int(h.hexdigest(), 16)
    return nodeId


def initializeReceiverSocket():
    group_bin = socket.inet_pton(socket.AF_INET6, 'ff02::0')
    mreq = group_bin + struct.pack('@I', SCOPEID)

    senderSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    senderSocket.bind(('', PORT))
    print("listening for messages on port: " + str(PORT))
    return senderSocket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)


def initializeSenderSocket():
    ttl_bin = struct.pack('@i', SCOPEID)

    receiverSocket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
    print ("Criei o socket para enviar")
    return receiverSocket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)


def Receiver(serverSocket):
    print ("Estou a receber")
    return serverSocket.recvfrom(BUFFSIZE)


def Sender(clientSocket,message):
    dest_addr = 'ff02::0'
    print ("Estou a enviar")
    return clientSocket.sendto(message.encode(), (dest_addr, PORT, 0, SCOPEID))
