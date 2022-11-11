from concurrent.futures import ThreadPoolExecutor
import socket
import pickle
import time
# from xarm.wrapper import XArmAPI
import json
import ast

class Client:
    def __init__(self, port) -> None:
        self.ip = ''
        self.port = port
        # self.buf = 4096
        self.buf=1024

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.sock.settimeout(0.0001)

    def receive(self):
        try:
            data = self.sock.recv(self.buf)
            self.data = pickle.loads(data)
            # print(type(self.data))

    
        except socket.timeout:
            # self.data={'front':0,'right':0, 'left':0, 'back':0, 'pitch_plus':0, 'pitch_minus':0, 'yaw_plus':0, 'yaw_minus':0, 'roll_plus':0, 'roll_minus':0, 'up':0, 'down':0, 'open':0, 'close':0}
            self.data = {}
            
        return self.data


class Move:
    def __init__(self, button, frequency=30, length=50) -> None:
        self.s_flag = 0
        self.button = button
        self.frequency = frequency
        self.length = length
        self.diff = 0
        self.set_liner()
    # def Liner(self, data, button, index, sign='+'):
    #     try:
    #         # print('a')
    #         print(data[button])
    #     except:
    #         pass

    def set_liner(self):
        self.interval = self.length * 1/self.frequency
        self.interval_list = [self.interval] * self.frequency

    def liner(self, data, button, index, sign='+'):
        global position
        try:
            if data[button] == 1:
                if self.s_flag == 0:
                    self.iter = iter(self.interval_list)
                    self.s_flag = 1
        except:
            pass
        if self.s_flag == 1:
            try:
                self.diff = next(self.iter)
                if sign == '+':
                    position[index] += self.diff
                elif sign == '-':
                    position[index] -= self.diff
            except StopIteration:
                self.diff = 0
                self.s_flag = 0

    def g_liner(self, data, button, sign='+'):
        global gripper
        try:
            if data[button] == 1:
                if self.s_flag == 0:
                    self.iter = iter(self.interval_list)
                    self.s_flag = 1
        except:
            pass
        if self.s_flag == 1:
            try:
                self.diff = next(self.iter)
                if sign == '+':
                    gripper += self.diff
                elif sign == '-':
                    gripper -= self.diff
            except StopIteration:
                self.diff = 0
                self.s_flag = 0



if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix='thread')

    client_1 = Client(port=6000)
   

    receive_1 = []
   

    gripper=1
    position=1

    s_front = 'front'
    m_front_1 = Move(s_front)

    while True:
        try:    
            receive_1.append(pool.submit(client_1.receive))
            # print(client_1.receive())
            data_1 = receive_1[-1].result()
            print(data_1)
            # print(data_1['front'])

            # if data_1['front']==0:
            #     print('HIEEEEED')
            # else:
            #     print('O')

            
            # data=client_1.receive()
            # print(data[1])
            # print(data)

            m_front_1.liner(data_1, s_front, 0)

            

            
        except KeyboardInterrupt:
            break
      