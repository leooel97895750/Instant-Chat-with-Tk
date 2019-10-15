# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 19:21:55 2019

@author: leooe
"""

import socket
import threading
import json

userDict = {}

def sendThread():    
    while True:
        # 輸入編號已決定要穿送訊息的對象(用空白隔開)
        myMsg = input()
        sock.sendall(myMsg.encode('UTF-8'))

def recvThread():
    global userDict
    
    while True:
        otherMsg = sock.recv(65536).decode('UTF-8')
        msgType = otherMsg.split()
        msgText = otherMsg[otherMsg.index(" ")+1:]
        
        # 其他使用者的訊息
        if msgType[0] == 'messagePass': 
            print(msgText)
        
        # 更新使用者列表
        else:
            userDict = json.loads(otherMsg)
            print(userDict)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 12345))

# 輸入暱稱
nickname = input("What's your nickname...")
sock.sendall(nickname.encode('UTF-8'))

th1 = threading.Thread(target=sendThread)
th2 = threading.Thread(target=recvThread)
th1.setDaemon(True)
th2.setDaemon(True)
th1.start()
th2.start()

# 等待結束
th1.join()
th2.join()