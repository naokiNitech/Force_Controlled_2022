import socket
import pickle
from screeninfo import get_monitors
from pynput import mouse
from PIL import Image, ImageTk
import tkinter as tk

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
                self.b_front = 0
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
                
                if manager.button_front.x1 < x and x < manager.button_front.x2 and manager.button_front.y1 < y and y < manager.button_front.y2:
                    self.b_front = 1
                if manager.button_right.x1 < x and x < manager.button_right.x2 and manager.button_right.y1 < y and y < manager.button_right.y2:
                    self.b_right = 1
                if manager.button_left.x1 < x and x < manager.button_left.x2 and manager.button_left.y1 < y and y < manager.button_left.y2:
                    self.b_left = 1
                if manager.button_back.x1 < x and x < manager.button_back.x2 and manager.button_back.y1 < y and y < manager.button_back.y2:
                    self.b_back = 1
                if manager.button_pitch_plus.x1 < x and x < manager.button_pitch_plus.x2 and manager.button_pitch_plus.y1 < y and y < manager.button_pitch_plus.y2:
                    self.b_pitch_plus = 1
                if manager.button_pitch_minus.x1 < x and x < manager.button_pitch_minus.x2 and manager.button_pitch_minus.y1 < y and y < manager.button_pitch_minus.y2:
                    self.b_pitch_minus = 1
                if manager.button_yaw_plus.x1 < x and x < manager.button_yaw_plus.x2 and manager.button_yaw_plus.y1 < y and y < manager.button_yaw_plus.y2:
                    self.b_yaw_plus = 1
                if manager.button_yaw_minus.x1 < x and x < manager.button_yaw_minus.x2 and manager.button_yaw_minus.y1 < y and y < manager.button_yaw_minus.y2:
                    self.b_yaw_minus = 1
                if manager.button_roll_plus.x1 < x and x < manager.button_roll_plus.x2 and manager.button_roll_plus.y1 < y and y < manager.button_roll_plus.y2:
                    self.b_roll_plus = 1
                if manager.button_roll_minus.x1 < x and x < manager.button_roll_minus.x2 and manager.button_roll_minus.y1 < y and y < manager.button_roll_minus.y2:
                    self.b_roll_minus = 1
                if manager.button_up.x1 < x and x < manager.button_up.x2 and manager.button_up.y1 < y and y < manager.button_up.y2:
                    self.b_up = 1
                if manager.button_down.x1 < x and x < manager.button_down.x2 and manager.button_down.y1 < y and y < manager.button_down.y2:
                    self.b_down = 1
                if manager.button_open.x1 < x and x < manager.button_open.x2 and manager.button_open.y1 < y and y < manager.button_open.y2:
                    self.b_open = 1
                if manager.button_close.x1 < x and x < manager.button_close.x2 and manager.button_close.y1 < y and y < manager.button_close.y2:
                    self.b_close = 1

                self.message = {'front':self.b_front, 'right':self.b_right, 'left':self.b_left, 'back':self.b_back, 'pitch_plus':self.b_pitch_plus, 'pitch_minus':self.b_pitch_minus, 'yaw_plus':self.b_yaw_plus, 'yaw_minus':self.b_yaw_minus, 'roll_plus':self.b_roll_plus, 'roll_minus':self.b_roll_minus, 'up':self.b_up, 'down':self.b_down, 'open':self.b_open, 'close':self.b_close}
                print(self.message)

                self.message = pickle.dumps(self.message)
                sock.sendto(self.message, (ip, port))

        except KeyboardInterrupt:
            return False

class Button:
    def __init__(self, x, y, button, file_on, file_off, size=100) -> None:
        self.button = button

        self.on = 0
        self.on_time = 0

        self.x1 = x - size/2
        self.y1 = y - size/2
        self.x2 = x + size/2
        self.y2 = y + size/2

        self.x = x
        self.y = y

        self.image_off = Image.open(file_off)
        self.image_off = self.image_off.resize((size,size))
        self.image_off = ImageTk.PhotoImage(self.image_off)

    def draw(self, canvas):
        canvas.create_image(self.x, self.y, image=self.image_off)

class Manager:
    TICK = 1
    def __init__(self) -> None:
        self.master = tk.Tk()

        self.master.attributes('-fullscreen', True)
        self.master.attributes('-topmost', True)
        # self.master.wm_attributes('-transparentcolor', 'white')
        self.master.wm_attributes('-fullscreen')


        self.screen_info = get_monitors()[0]
        self.screen_width = self.screen_info.width
        self.screen_height = self.screen_info.height

        self.canvas = tk.Canvas(self.master, width=self.screen_width, height=self.screen_height, bg='white')

        self.create_widgets()
        self.draw()

    def create_widgets(self):
        self.screeen_center = (self.screen_width//2, self.screen_height//2)
        self.button_front = Button(self.screen_width*0.5, self.screen_height*0.4, 'front', 'button_fig/front_on.png', 'button_fig/front.png')
        self.button_right = Button(self.screen_width*0.6, self.screen_height*0.5, 'right', 'button_fig/right_on.png', 'button_fig/right.png')
        self.button_left = Button(self.screen_width*0.4, self.screen_height*0.5, 'left', 'butto_fig/left_on.png', 'button_fig/left.png')
        self.button_back = Button(self.screen_width*0.5, self.screen_height*0.6, 'back', 'butto_fig/back_on.png', 'button_fig/back.png')
        self.button_pitch_plus = Button(self.screen_width*0.5, self.screen_height*0.2, 'pitch_plus', 'butto_fig/pitch_1.png', 'button_fig/pitch_1.png')
        self.button_pitch_minus = Button(self.screen_width*0.5, self.screen_height*0.8, 'pitch_minus', 'butto_fig/pitch_2.png', 'button_fig/pitch_2.png')
        self.button_yaw_plus = Button(self.screen_width*0.8, self.screen_height*0.5, 'yaw_plus', 'butto_fig/yaw_1.png', 'button_fig/yaw_1.png')
        self.button_yaw_minus = Button(self.screen_width*0.2, self.screen_height*0.5, 'yaw_minus', 'butto_fig/yaw_2.png', 'button_fig/yaw_2.png')
        self.button_roll_plus = Button(self.screen_width*0.7, self.screen_height*0.3, 'roll_plus', 'butto_fig/roll_1.png', 'button_fig/roll_1.png')
        self.button_roll_minus = Button(self.screen_width*0.3, self.screen_height*0.3, 'roll_minus', 'butto_fig/roll_2.png', 'button_fig/roll_2.png')
        self.button_up = Button(self.screen_width*0.2, self.screen_height*0.8, 'up', 'butto_fig/up.png', 'button_fig/up.png')
        self.button_down = Button(self.screen_width*0.3, self.screen_height*0.8, 'down', 'butto_fig/down.png', 'button_fig/down.png')
        self.button_open = Button(self.screen_width*0.8, self.screen_height*0.7, 'open', 'butto_fig/open.png', 'button_fig/open.png')
        self.button_close = Button(self.screen_width*0.8, self.screen_height*0.8, 'close', 'butto_fig/close.png', 'button_fig/close.png')

    def show(self):
        try:
            self.master.mainloop()
        except:
            self.quit()

    def draw(self):
        self.button_front.draw(self.canvas)
        self.button_right.draw(self.canvas)
        self.button_left.draw(self.canvas)
        self.button_back.draw(self.canvas)
        self.button_pitch_plus.draw(self.canvas)
        self.button_pitch_minus.draw(self.canvas)
        self.button_yaw_plus.draw(self.canvas)
        self.button_yaw_minus.draw(self.canvas)
        self.button_roll_plus.draw(self.canvas)
        self.button_roll_minus.draw(self.canvas)
        self.button_up.draw(self.canvas)
        self.button_down.draw(self.canvas)
        self.button_open.draw(self.canvas)
        self.button_close.draw(self.canvas)
        self.canvas.pack()

    def quit(self):
        self.master.quit()

if __name__ == '__main__':
    manager = Manager()

    ip = '133.68.35.141'
    # ip='192.168.1.9'
    port = 8888
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    monitor = Monitor()
    
    manager.show()