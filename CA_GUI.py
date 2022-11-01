import threading
import tkinter as tk
from PIL import Image, ImageTk
from screeninfo import get_monitors
from pynput import mouse
import socket
import pickle
import threading

class Socket:
    def __init__(self, ip, port) -> None:
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class Mouse:
    def __init__(self) -> None:
        global pos_x, pos_y, press
        self.get_mouse = mouse.Listener(
            on_move = self.on_move,
            on_click = self.on_click)
        self.get_mouse.start()

    def on_move(self, x, y):
        global pos_x, pos_y
        pos_x = x
        pos_y = y

    def on_click(self, x, y, button, pressed):
        global pos_x, pos_y, press
        if pressed:
            pos_x = x
            pos_y = y
            press = pressed

class Button:
    def __init__(self, x, y, button, file_on, file_off, size=100) -> None:
        self.button = button
        self.on = False
        self.x1 = x - size/2
        self.y1 = y - size/2
        self.x2 = x + size/2
        self.y2 = y + size/2
        self.size = size
        self.x = x
        self.y = y
        self.image_on = Image.open(file_on)
        self.image_off = Image.open(file_off)
        self.image_on = self.image_on.resize((size,size))
        self.image_off = self.image_off.resize((size,size))
        self.image_on = ImageTk.PhotoImage(self.image_on)
        self.image_off = ImageTk.PhotoImage(self.image_off)
        self.on_time = 0
        self.c_flag = 0
        
    def draw(self, canvas, reset=True):
        canvas.delete(self.button)
        if self.c_flag == 0:
            self.switch = canvas.create_image(self.x, self.y, image=self.image_off)
            self.c_flag = 1
        elif self.c_flag == 1:
            if self.on:
                print(self.button, self.on)
                # canvas.itemconfig(self.switch, image=self.image_on)
                # time.sleep(0.1)
                pass
            else:
                # canvas.itemconfig(self.switch, image=self.image_off)
                pass
        if reset:
            self.on = False

    def change(self):
        global pos_x, pos_y, press
        self.s_on = 0
        if press:
            if self.x1 < pos_x and pos_x < self.x2 and self.y1 < pos_y and pos_y <self.y2:
                self.on = True
                press = False
                self.s_on = 1
        return self.s_on

class Manager:
    TICK = 1
    def __init__(self) -> None:
        self.master = tk.Tk()

        # self.master.attributes('-fullscreen', True)
        self.master.attributes('-topmost', True)
        self.master.wm_attributes('-transparentcolor', 'white')

        self.s_info = get_monitors()[0]
        self.s_width = self.s_info.width
        self.s_height = self.s_info.height

        self.canvas = tk.Canvas(self.master, width=self.s_width, height=self.s_height, bg='white')

        self.create_widgets()

        self.draw()

    def create_widgets(self):
        self.s_center = (self.s_width//2, self.s_height//2)
        self.b_front = Button(self.s_width*0.5, self.s_height*0.4, 'front', 'button_fig/front_on.png', 'button_fig/front.png')
        self.b_right = Button(self.s_width*0.65, self.s_height*0.5, 'right', 'button_fig/right_on.png', 'button_fig/right.png')

    def show(self):
        self.is_playing = 1
        self.play()
        try:
            self.master.mainloop()
        except:
            self.quit()

    def play(self):
        try:
            if self.is_playing == 1:
                # self.operate()
                # self.draw()
                self.master.after(self.TICK,self.play)
                if press:
                    print(pos_x, pos_y)
                # self.message = '%f,%f' % (self.front, self.right)
                # print(self.message)
                # sock.sock.sendto(self.message.encode('utf-8'), (sock.ip, sock.port))
                self.message = {'front':self.front, 'right':self.right}
                # print(self.message)
                self.message = pickle.dumps(self.message)
                sock.sock.sendto(self.message, (sock.ip, sock.port))
            else:
                self.quit()
        except KeyboardInterrupt:
            sock.sock.close()
            self.quit()

    def operate(self):
        self.front = self.b_front.change()
        self.right = self.b_right.change()

    def draw(self):
        self.b_front.draw(self.canvas)
        self.b_right.draw(self.canvas)
        self.canvas.pack()

    def quit(self, *args):
        self.master.quit()

class test:
    def send(self):
        self.counter = 0
        while True:
            try:
                if self.counter % 100 == 0:
                    self.message = {'front':1, 'right':1}
                else:
                    self.message = {'front':0, 'right':0}
                self.message = pickle.dumps(self.message)
                sock.sock.sendto(self.message, (ip, port))

                self.counter += 1
            except:
                pass

if __name__ == '__main__':
    pos_x = pos_y = 0.5
    press = False

    # ip = '133.68.35.155'
    ip = '133.68.35.160'


    # manager = Manager()
    # get_pos = Mouse()
    sock = Socket(ip, port)
    manager = test()
    th = threading.Thread(target=manager.send)
    th.start()
    # manager.show()