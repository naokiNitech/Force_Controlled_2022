from concurrent.futures import ThreadPoolExecutor
import socket
import pickle
from xarm.wrapper import XArmAPI
import ast
import threading

class Client:
    def __init__(self, port) -> None:
        self.ip = ''
        self.port = port
        # self.buf = 1024
        self.buf=512

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.sock.settimeout(0.0001)

    def receive(self):
        try:
            data= self.sock.recv(self.buf)
            self.data=data.decode()
            self.data=self.data.replace('\x00','')
            # 空白を削除していないとdict型に変換できない
            self.data=ast.literal_eval(self.data)
        except socket.timeout:
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
                    # gripper += self.diff
                    gripper+=6
                    if gripper>840:
                        gripper=840
                elif sign == '-':
                    # gripper -= self.diff
                    gripper-=6
                    if gripper<0:
                        gripper=0
            except StopIteration:
                self.diff = 0
                self.s_flag = 0

class RobotControll:
    def __init__(self, isEnableArm=False) -> None:
        self.isEnableArm = isEnableArm
        self.xArmIP = '192.168.1.217'
        self.initX, self.initY, self.initZ, self.initRoll, self.initPitch, self.initYaw = 200,0,400,90,0,0
        self.max_X, self.max_Y, self.max_Z = 460, 300, 300
        self.min_X, self.min_Y, self.min_Z = 180, -300, 70
        self.init_gripper_position = 650
        self.init_position = [self.initX, self.initY, self.initZ, self.initRoll, self.initPitch, self.initYaw]

        self.ip = '133.68.35.220'
        self.port = 7000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        if isEnableArm:
            self.arm = XArmAPI(self.xArmIP)
            self.initialize_all(self.arm)
            self.loadcell_setup()
            print('!!!ready!!!')

    def send_data_to_robot(self):
        global position, gripper
        if self.isEnableArm:
            self.arm.set_servo_cartesian(position)
            self.arm.getset_tgpio_modbus_data(self.convert_to_modbus_data(gripper))
        else:
            pass
        
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

    def loadcell_setup(self):
        self.init_loadval = self.arm.get_tgpio_analog(0)[1] #analogポートの番号とそのデータリストのうちの1のデータを取り出す　これがロードセルの値の初期値
        self.load_thread = threading.Thread(target=self.get_loadcell_value, daemon=True)
        self.load_thread.start()
    
    def get_loadcell_value(self):
        global loadcell_val
        while True:
            try:
                loadcell_val = self.arm.get_tgpio_analog(1)[1] - self.init_loadval
                self.Loadcell=str(loadcell_val)
                self.sock.sendto(self.Loadcell.encode(),(self.ip,self.port))
            except:
                loadcell_val = 0

if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix='thread')

    client_1 = Client(port=6000)
    client_2 = Client(port=9999)


    receive_1 = []
    receive_2 = []

    xarm = RobotControll(isEnableArm=True)
    position = xarm.init_position
    gripper = xarm.init_gripper_position

    s_front = 'front'
    s_right = 'right'
    s_left = 'left'
    s_back = 'back'
    s_pitch_plus = 'pitch_plus'
    s_pitch_minus = 'pitch_minus'
    s_yaw_plus = 'yaw_plus'
    s_yaw_minus = 'yaw_minus'
    s_roll_plus = 'roll_plus'
    s_roll_minus = 'roll_minus'
    s_up = 'up'
    s_down = 'down'
    s_open = 'open'
    s_close = 'close'

    m_front_1 = Move(s_front)
    # m_right_1 = Move(s_right)
    m_right_1 = Move(s_up)
    # m_right_1 = Move(s_down, length=20)
    m_left_1 = Move(s_left)
    # m_left_1 = Move(s_up, length=20)
    m_back_1 = Move(s_back)
    m_pitch_plus_1 = Move(s_pitch_plus, length=15)
    m_pitch_minus_1 = Move(s_pitch_minus, length=15)
    m_yaw_plus_1 = Move(s_yaw_plus, length=15)
    m_yaw_minus_1 = Move(s_yaw_minus, length=15)
    m_roll_plus_1 = Move(s_roll_plus, length=15)
    m_roll_minus_1 = Move(s_roll_minus, length=15)
    m_up_1 = Move(s_up, length=20)
    # m_up_1 = Move(s_right, length=50)
    m_down_1 = Move(s_down, length=20)
    # m_down_1 = Move(s_left, length=50)
    m_open_1 = Move(s_open, frequency=10, length=100)
    m_close_1 = Move(s_close, frequency=10, length=100)

    m_front_2 = Move(s_front)
    m_right_2 = Move(s_right)
    m_left_2 = Move(s_left)
    m_back_2 = Move(s_back)
    m_pitch_plus_2 = Move(s_pitch_plus, length=15)
    m_pitch_minus_2 = Move(s_pitch_minus, length=15)
    m_yaw_plus_2 = Move(s_yaw_plus, length=15)
    m_yaw_minus_2 = Move(s_yaw_minus, length=15)
    m_roll_plus_2 = Move(s_roll_plus, length=15)
    m_roll_minus_2 = Move(s_roll_minus, length=15)
    m_up_2 = Move(s_up, length=20)
    m_down_2 = Move(s_down, length=20)
    m_open_2 = Move(s_open, frequency=10, length=100)
    m_close_2 = Move(s_close, frequency=10, length=100)

    while True:
        try:    
            receive_1.append(pool.submit(client_1.receive))
            # print(receive_1)
            data_1 = receive_1[-1].result()

            receive_2.append(pool.submit(client_2.receive))
            data_2 = receive_2[-1].result()

            m_front_1.liner(data_1, s_front, 0)
            # m_right_1.liner(data_1, s_right, 1, '-')
            # m_right_1.liner(data_1, s_right, 2, '-')
            m_right_1.liner(data_1, s_up, 2)
            # m_left_1.liner(data_1, s_left, 1)
            m_left_1.liner(data_1, s_up, 2)
            m_back_1.liner(data_1, s_back, 0, '-')
            m_pitch_plus_1.liner(data_1, s_pitch_plus, 4)
            m_pitch_minus_1.liner(data_1, s_pitch_minus, 4, '-')
            m_roll_plus_1.liner(data_1, s_roll_plus, 5, '-')
            m_roll_minus_1.liner(data_1, s_roll_minus, 5)
            m_yaw_plus_1.liner(data_1, s_yaw_plus, 3)
            m_yaw_minus_1.liner(data_1, s_yaw_minus, 3, '-')
            # m_up_1.liner(data_1, s_up, 2)
            m_up_1.liner(data_1, s_right, 1, '-')
            # m_down_1.liner(data_1, s_down, 2, '-')
            m_down_1.liner(data_1, s_left, 1)
            m_open_1.g_liner(data_1, s_open)
            m_close_1.g_liner(data_1, s_close, '-')

            m_front_2.liner(data_2, s_front, 0)
            m_right_2.liner(data_2, s_right, 1, '-')
            m_left_2.liner(data_2, s_left, 1)
            m_back_2.liner(data_2, s_back, 0, '-')
            m_roll_plus_2.liner(data_2, s_roll_plus, 5, '-')
            m_roll_minus_2.liner(data_2, s_roll_minus, 5)
            m_yaw_plus_2.liner(data_2, s_yaw_plus, 3)
            m_yaw_minus_2.liner(data_2, s_yaw_minus, 3, '-')
            m_up_2.liner(data_2, s_up, 2)
            m_down_2.liner(data_2, s_down, 2, '-')
            m_open_2.g_liner(data_2, s_open)
            m_close_2.g_liner(data_2, s_close, '-')
            
            print(position, gripper)

            xarm.send_data_to_robot()

        except KeyboardInterrupt:
            break