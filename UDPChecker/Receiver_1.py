from concurrent.futures import ThreadPoolExecutor
import socket
import pickle
import time
# from xarm.wrapper import XArmAPI

class Client:
    def __init__(self, port) -> None:
        self.ip = ''
        self.port = port
        # self.buf = 4096
        self.buf=8192*4

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.sock.settimeout(0.0001)

    def receive(self):
        try:
            data = self.sock.recv(self.buf)
            self.data = pickle.loads(data)
            # time.sleep(1)
        except socket.timeout:
            self.data = {}
        return self.data



if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix='thread')
    # ---------------------------
    client_1 = Client(port=6000)
    # ----------------------------
    client_2 = Client(port=9999)

    receive_1 = []
    receive_2 = []

    while True:
        try:    
            receive_1.append(pool.submit(client_1.receive))
            # print(client_1.receive)
            data_1 = receive_1[-1].result()

            print(data_1)
            

            receive_2.append(pool.submit(client_2.receive))
            data_2 = receive_2[-1].result()
        except KeyboardInterrupt:
            break