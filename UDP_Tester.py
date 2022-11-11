from socket import socket, AF_INET, SOCK_DGRAM
import pickle
from screeninfo import get_monitors
from pynput import mouse
from PIL import Image, ImageTk
import tkinter as tk


if __name__ == '__main__':
    # HOST = '133.68.35.220'   
    # PORT = 6000
    # data=1024

    # # ソケットを用意
    # s = socket(AF_INET, SOCK_DGRAM)
    # # バインドしておく
    # s.bind((HOST, PORT))

    # while True:
    #     # 受信
    #     msg, address = s.recvfrom(data)
    #     print(msg.decode(),address)
    #     print('a')


    HOST = ''   
    PORT = 6000

    # ソケットを用意
    s = socket(AF_INET, SOCK_DGRAM)
    # バインドしておく
    s.bind((HOST, PORT))

    while True:
        # 受信
        # print('a')
        msg, address = s.recvfrom(1024)
        # udpが送信されていないとここで止まる↑
        # print(f"message: {msg.decode()}\nfrom: {address}")
        print(msg.decode())

        
        

    # ソケットを閉じておく
    s.close()
# とりまできました．touchdesignerの方のUDPOUTにはなぜか出力されない
    

    