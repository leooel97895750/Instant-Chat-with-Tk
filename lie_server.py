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
    connection.sendall(str(myfileno).encode('UTF-8'))
    
    myNameDict[myfileno] = nickname
    mySockDict[myfileno] = connection
    
    # 傳送線上使用者列表
    updateDict()
    
    while True:
        # 接收使用者傳來的編號和訊息
        msg = connection.recv(65536).decode('UTF-8')
        msgType = msg.split()
        
        # 在server上顯示的系統訊息
        print(myNameDict[myfileno], ':', msg)
        
        if msgType[0] == "roomOpen":
            print(msgType[1])
            mySockDict[int(msgType[1].split(':')[1])].sendall(msg.encode('UTF-8'))
            
        # 傳送給特定使用者的私人訊息
        elif msgType[0] == "messagePass":
            mySockDict[int(msgType[1].split(':')[1])].sendall(msg.encode('UTF-8'))
        
        elif msgType[0] == "deleteDict":
            del myNameDict[int(msgType[1])]
            del mySockDict[int(msgType[1])]
            updateDict()


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