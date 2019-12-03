import socket
import http.client

serverPort = 12000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP socket
serverSocket.bind(('' , serverPort))
serverSocket.listen(1)  # Allows 1 connection at a time
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    print("Got connection from", addr)
    sentence = connectionSocket.recv(1024).decode()
    print(sentence)
    connection = http.client.HTTPSConnection("127.0.0.1", 33333)
    connection.request("GET", "/")
    response = connection.getresponse()
    print("Status: {} and reason: {}".format(response.status, response.reason))
    connection.close()

    connectionSocket.send(("Sen bana {} gönderdin".format(sentence)).encode())
    connectionSocket.close()