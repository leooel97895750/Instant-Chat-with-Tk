# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 21:42:44 2019

@author: leooe
"""
from tkinter import *
import socket
import threading
import json

rooms = {}
userDict = {}

def sendThread():    
    while True:
        # 輸入編號已決定要穿送訊息的對象(用空白隔開)
        myMsg = input()
        sock.sendall(myMsg.encode('UTF-8'))

def recvThread():
    global userDict, rooms
    
    while True:
        otherMsg = sock.recv(65536).decode('UTF-8')
        msgType = otherMsg.split()
        msgText = otherMsg[otherMsg.index(" ")+1:]
        
        # 其他使用者的訊息
        if msgType[0] == 'messagePass': 
            print(msgText)
        
        # 被通知開啟聊天室
        elif msgType[0] == 'roomOpen':
            room = Toplevel()
            room.title(name)
            
            message = Text(room, exportselection=False)
            message.pack()
            message.tag_config("tagOther", foreground="black", justify=LEFT)
            message.tag_config("tagMe", foreground="black", justify=RIGHT)
            
            entry = Entry(room)
            entry.pack()
            entry.bind("<Return>", handlerAdaptor(sendMessage,name))
        
            # 建立物件
            NewRoom = RoomItems(room, message, entry)
            rooms[name] = NewRoom
        
        # 更新使用者列表
        else:
            userDict = json.loads(otherMsg)
            try:
                updateUserList()
            except:
                print('updateUserList Error')

def updateUserList():
    global userDict
    
    # 刪除原本的lsitbox並更新
    listbox.delete(0, END)
    for k, v in userDict.items():
        userID = v + " : " + str(k)
        listbox.insert(END, userID)

# 建立聊天室類別，紀錄獨立各別物件
class RoomItems():
    def __init__(self, room, message, entry):
        self.room = room
        self.message = message
        self.entry = entry

# binding enter，傳送entry中的訊息到對應的聊天室
def sendMessage(event, name):
    global rooms
    
    # 顯示於自己的視窗
    text = rooms[name].entry.get()
    rooms[name].entry.delete(0, END)
    rooms[name].message.insert(END, text+'\n', "tagMe")
    rooms[name].message.see(END)
    
    # 傳送至對方的聊天室

def handlerAdaptor(fun, name):
    return lambda event,fun=fun,name=name: fun(event, name)

# 初始化聊天室
def chat():
    global rooms
    
    # 建立自己對應的獨立聊天室
    indexes = listbox.curselection()
    name = listbox.get(indexes[0])
    room = Toplevel()
    room.title(name)
    
    message = Text(room, exportselection=False)
    message.pack()
    message.tag_config("tagOther", foreground="black", justify=LEFT)
    message.tag_config("tagMe", foreground="black", justify=RIGHT)
    
    entry = Entry(room)
    entry.pack()
    entry.bind("<Return>", handlerAdaptor(sendMessage,name))

    # 建立物件
    NewRoom = RoomItems(room, message, entry)
    rooms[name] = NewRoom
    
    # 通知對方開啟聊天室
    sock.sendall("roomOpen".encode('UTF-8'))

# 主程式開始
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 12345))

# 輸入暱稱
nickname = input("請輸入你的暱稱...\n")
sock.sendall(nickname.encode('UTF-8'))

th1 = threading.Thread(target=sendThread)
th2 = threading.Thread(target=recvThread)
th1.setDaemon(True)
th2.setDaemon(True)
th1.start()
th2.start()

# 圖形介面布局
root = Tk()

# 標題
label = Label(root, text="Line")
label.pack()

# 使用者列表
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)
listbox = Listbox(root, yscrollcommand=scrollbar.set)
listbox.pack()
scrollbar.config(command=listbox.yview)

# 開啟聊天室按鍵
button = Button(root, text="開始聊天", command=chat)
button.pack()

updateUserList()

root.mainloop()