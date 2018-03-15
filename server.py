import socket

PORT = 5005

ServerSock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
ServerSock.bind(('', PORT))
print("Server listening for messages on port: " + str(PORT))
(ClientMsg, (ClientIP, ClientPort, ClientFlow, ClientScopeId)) = ServerSock.recvfrom (1024)
print("Message: [" + ClientMsg.decode('utf-8') + "] received on IP/PORT: [" + ClientIP + "," +
      str(ClientPort) + "]")
