# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 19:21:27 2019

@author: leooe
"""

import socket
import threading
import json

myNameDict = {}
mySockDict = {}

def updateDict():
    global myNameDict, mySockDict
    
    for s in mySockDict.values():
        s.sendall(json.dumps(myNameDict).encode('UTF-8'))

def subThread(connection, myfileno):
    global myNameDict, mySockDict
    
    # 接收使用者傳來的暱稱
    nickname = connection.recv(1024).decode('UTF-8')
    
    myNameDict[myfileno] = nickname
    mySockDict[myfileno] = connection
    
    # 傳送線上使用者列表
    updateDict()
    
    while True:
        # 接收使用者傳來的編號和訊息
        msg = connection.recv(65536).decode('UTF-8')
        msgInfo = msg.split()
        msgType = int(msgInfo[0])
        msgText = msg[msg.index(" ")+1:]
        
        # 在server上顯示的系統訊息
        print(myNameDict[myfileno], ':', msg)
        
        # 傳送給特定使用者的私人訊息
        mySockDict[msgType].sendall(("messagePass "+msgText).encode('UTF-8'))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 12345))
sock.listen(5)
print('Waiting for someone to connect...')

while True:
    connection, addr = sock.accept()
    print(addr, connection.fileno())
    
    mythread = threading.Thread(target=subThread, args=(connection, connection.fileno()))
    mythread.setDaemon(True)
    mythread.start()