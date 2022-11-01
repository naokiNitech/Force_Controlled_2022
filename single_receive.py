import socket
import pickle

ip = ''
port = 8888
buf = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

while True:
    data = sock.recv(buf)
    data = pickle.loads(data)
    print(data)