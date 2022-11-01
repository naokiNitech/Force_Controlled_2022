import socket
import pickle
import threading
import numpy as np
from xarm.wrapper import XArmAPI
import time

class Signal:
    def __init__(self, port) -> None:
        self.ip = ''
        self.port = port
        self.bufsize = 1024
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))

    def receive(self):
        while True:
            try:
                self.data = self.sock.recv(self.bufsize)
                self.dat = pickle.loads(self.data)
                # print(self.dat)
            except:
                pass
            # return self.dat
            # print(self.data)
            # if self.dat['front'] == 1:
            #     print(self.dat)

class Check:
    def __init__(self) -> None:
        pass

    def discrimination(self, data, button):
        self.get = False
        if data[button] == 1:
            self.get = True
            # print(button, self.get)
        return self.get

class Move:
    def __init__(self, switch) -> None:
        self.switch = switch
        self.s_flag = 0
        self.freq = 200
        self.length = 10
        self.diff = 0
        self.set_liner(self.length)

    def set_liner(self, length):
        self.length = length
        self.interval = self.length * 1/self.freq
        self.division_list = [self.interval] * self.freq

    def liner(self, on, index):
        global position
        if on:
            if self.s_flag == 0:
                self.iter = iter(self.division_list)
                self.s_flag = 1
        if self.s_flag == 1:
            try:
                self.diff = next(self.iter)
                position[index] += self.diff
            except StopIteration:
                self.diff = 0
                self.s_flag = 0
                pass

    def grip_auto(self, force):
        self.grip_pos = 850

class RobotControll:
    def __init__(self, isEnableArm=False) -> None:
        self.isEnableArm = isEnableArm
        self.xArmIP = '192.168.1.240'
        self.initX, self.initY, self.initZ, self.initRoll, self.initPitch, self.initYaw = 200,0,200,180,0,0
        self.max_X, self.max_Y, self.max_Z = 460, 300, 300
        self.min_X, self.min_Y, self.min_Z = 180, -300, 70
        self.init_gripper_position = 850
        self.dx = 0
        self.dy = 0
        self.init_position = np.array([self.initX, self.initY, self.initZ, self.initRoll, self.initPitch, self.initYaw])
        if self.isEnableArm:
            self.arm = XArmAPI(self.xArmIP)
            self.initialize_all(self.arm)
            print('!!!ready!!!')

    def send_data_to_robot(self):
        global position
        if self.isEnableArm:
            # self.limitation_of_range(self.dx, self.dy)

            self.arm.set_servo_cartesian(position)
            # self.arm.set_gripper_position(self.init_gripper_position, speed=5000)

    def limitation_of_range(self, x, y):
        self.mvpose = [self.initX+x,self.initY+y,self.initZ,self.initRoll,self.initPitch,self.initYaw]
        if self.mvpose[0] > self.max_X:
            self.mvpose[0] = self.max_X
        elif self.mvpose[0] < self.min_X:
            self.mvpose[0] = self.min_X
        if self.mvpose[1] > self.max_Y:
            self.mvpose[1] = self.max_Y
        elif self.mvpose[1] < self.min_Y:
            self.mvpose[1] = self.min_Y
        if self.mvpose[2] > self.max_Z:
            self.mvpose[2] = self.max_Z
        elif self.mvpose[2] < self.min_Z:
            self.mvpose[2] = self.min_Z

    def initialize_all(self, robotArm, isSetInitPosition=True):
        robotArm.connect()
        if robotArm.warn_code != 0:
            robotArm.clean_warn()
        if robotArm.error_code != 0:
            robotArm.clean_error()
        robotArm.motion_enable(enable=True)
        robotArm.set_mode(0)
        robotArm.set_state(state=0)
        if isSetInitPosition:
            robotArm.set_position(x=self.initX, y=self.initY, z=self.initZ, roll=self.initRoll, pitch=self.initPitch, yaw=self.initYaw, wait=True)
        else:
            robotArm.reset(wait=True)
        print('Initialized > xArm')

        robotArm.set_tgpio_modbus_baudrate(2000000)
        robotArm.set_gripper_mode(0)
        robotArm.set_gripper_enable(True)
        robotArm.set_gripper_position(self.init_gripper_position, speed=5000)
        robotArm.getset_tgpio_modbus_data(self.convert_to_modbus_data(800))
        print('Initialized > xArm gripper')

        robotArm.motion_enable(enable=True)
        robotArm.set_mode(1)
        robotArm.set_state(state=0)

    def convert_to_modbus_data(self, value: int):
        if int(value) <= 255 and int(value) >= 0:
            dataHexThirdOrder = 0x00
            dataHexAdjustedValue = int(value)

        elif int(value) > 255 and int(value) <= 511:
            dataHexThirdOrder = 0x01
            dataHexAdjustedValue = int(value)-256

        elif int(value) > 511 and int(value) <= 767:
            dataHexThirdOrder = 0x02
            dataHexAdjustedValue = int(value)-512

        elif int(value) > 767 and int(value) <= 1123:
            dataHexThirdOrder = 0x03
            dataHexAdjustedValue = int(value)-768

        modbus_data = [0x08, 0x10, 0x07, 0x00, 0x00, 0x02, 0x04, 0x00, 0x00]
        modbus_data.append(dataHexThirdOrder)
        modbus_data.append(dataHexAdjustedValue)
        
        return modbus_data

if __name__ == '__main__':
    sock1 = Signal(8888)
    sock2 = Signal(9999)

    # t1 = MyThread(sock1.receive)
    # t2 = MyThread(sock2.receive)
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    # signal1 = t1.get_result()
    # signal1 = t2.get_result()

    check1 = Check()
    check2 = Check()

    xarm = RobotControll(isEnableArm=False)
    position = list(xarm.init_position)

    s_front = 'front'
    s_right = 'right'

    m_front1 = Move(s_front)
    m_front2 = Move(s_front)

    m_right1 = Move(s_right)
    m_right2 = Move(s_right)

    thr1 = threading.Thread(target=sock1.receive)
    thr1.start()
    # thr1.join()
    time.sleep(0.1)
    # thr2 = threading.Thread(target=sock2.receive, daemon=True)
    # thr2.start()
    while True:
        try:
            if sock1.dat['front'] == 1:
                print(sock1.dat)
            # print(sock1.dat)
            # data1 = sock1.receive()
            # data2 = sock2.receive()
            # # print(data1)
            # if data1['front'] == 1:
            #     print(1,data1)
            # if data2['front'] == 1:
            #     print(2,data2)

            # print(sock1.dat)
            # if sock1.dat['front'] == 1:
            #     print(sock1.dat)
            # if signal1['front'] == 1:
            #     print(signal1)
            # data1 = sock1.receive()
            # data1 = sock2.receive()

            # front1 = check1.discrimination(data1, s_front)
            # front2 = check2.discrimination(data1, s_front)

            # right1 = check1.discrimination(data1, s_right)
            # right2 = check2.discrimination(data1, s_right)

            # m_front1.liner(front1, 0)
            # m_front2.liner(front2, 0)
            
            # m_right1.liner(right1, 1)
            # m_right2.liner(right2, 1)

            # print(position)

            # if xarm.isEnableArm:
            #     xarm.send_data_to_robot()
            pass

        except KeyboardInterrupt:
            break