import socket
import pickle
from screeninfo import get_monitors
from pynput import mouse
from PIL import Image, ImageTk
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
class Client:
    def __init__(self, port) -> None:
        self.ip = ''
        self.port = port
        self.buf = 4096

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.sock.settimeout(0.0001)

    def receive(self):
        try:
            data = self.sock.recv(self.buf)
            self.data = pickle.loads(data)
            # time.sleep(1)
        except socket.timeout:
            self.data={'front':0, 'right':0, 'left':0, 'back':0, 'pitch_plus':0, 'pitch_minus':0, 'yaw_plus':0, 'yaw_minus':0, 'roll_plus':0, 'roll_minus':0, 'up':0, 'down':0, 'open':0, 'close':0}
            # self.data = {}
        return self.data


class Monitor:
    def __init__(self) -> None:
        self.screen_info = get_monitors()[0]
        self.screen_width = self.screen_info.width
        self.screen_height = self.screen_info.height

        self.listener = mouse.Listener(on_click=self.on_click)
        self.listener.start()

    def on_click(self, x, y, button, pressed):
        try:
            if pressed:
                self.b_front = 1
                self.b_right = 0
                self.b_left = 0
                self.b_back = 0
                self.b_pitch_plus = 0
                self.b_pitch_minus = 0
                self.b_yaw_plus = 0
                self.b_yaw_minus = 0
                self.b_roll_plus = 0
                self.b_roll_minus = 0
                self.b_up = 0
                self.b_down = 0
                self.b_open = 0
                self.b_close = 0
            

                self.message = {'front':self.b_front, 'right':self.b_right, 'left':self.b_left, 'back':self.b_back, 'pitch_plus':self.b_pitch_plus, 'pitch_minus':self.b_pitch_minus, 'yaw_plus':self.b_yaw_plus, 'yaw_minus':self.b_yaw_minus, 'roll_plus':self.b_roll_plus, 'roll_minus':self.b_roll_minus, 'up':self.b_up, 'down':self.b_down, 'open':self.b_open, 'close':self.b_close}
                # print(self.message)

                self.message = pickle.dumps(self.message)
                sock.sendto(self.message, (ip, port))

        except KeyboardInterrupt:
            return False

if __name__ == '__main__':


    pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix='thread')

    client_1 = Client(port=8888)
    client_2 = Client(port=9999)

    receive_1 = []
    receive_2 = []


    # ip = '133.68.35.141'
    ip='192.168.0.4'
    port = 8888
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    monitor = Monitor()


    while True:
        try:    
            receive_1.append(pool.submit(client_1.receive))
            # print(client_1.receive)
            data_1 = receive_1[-1].result()

            # print(data_1['front'])
            print(type(data_1))

            receive_2.append(pool.submit(client_2.receive))
            data_2 = receive_2[-1].result()
        except KeyboardInterrupt:
            break
    