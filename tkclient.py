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

def rootClose():
    global fileno
    sock.sendall(("deleteDict "+fileno).encode('UTF-8'))
    sock.close()
    root.destroy()

# 建立聊天室類別，紀錄獨立各別物件
class RoomItems():
    def __init__(self, room, message, entry):
        self.room = room
        self.message = message
        self.entry = entry

def recvThread():
    global userDict, rooms
    
    while True:
        otherMsg = sock.recv(65536).decode('UTF-8')
        msgType = otherMsg.split()
        msgText = otherMsg[otherMsg.index(" ")+1:]
        
        # 其他使用者的訊息
        if msgType[0] == 'messagePass': 
            global rooms
            
            try:
                # 顯示對方的訊息
                rooms[msgType[2]].message.insert(END, otherMsg[otherMsg.index(msgType[3]):]+'\n', "tagOther")
                rooms[msgType[2]].message.see(END)
            except:
                pass
        
        # 被通知開啟聊天室
        elif msgType[0] == 'roomOpen':
            room = Toplevel()
            room.title(msgType[2])
            room.configure(background='#AAFFAA')
            
            message = Text(room, exportselection=False, width=30, font=('微軟正黑體', 10, 'bold'))
            message.grid(row=0, column=0, padx=5, pady=5)
            message.tag_config("tagOther", foreground="black", justify=LEFT)
            message.tag_config("tagMe", foreground="black", background="#DDFFDD", justify=RIGHT)
            
            entry = Entry(room, width=30, font=('微軟正黑體', 10, 'bold'))
            entry.grid(row=1, column=0, sticky=E, padx=5, pady=5)
            entry.bind("<Return>", handlerAdaptor(sendMessage, msgType[2], msgType[1]))
        
            # 建立物件
            NewRoom = RoomItems(room, message, entry)
            rooms[msgType[2]] = NewRoom
        
        # 更新使用者列表
        else:
            userDict = json.loads(otherMsg)
            try:
                updateUserList()
            except:
                # server產生thread時，第一次更新UserList會因為listbox尚未定義而進入except
                pass

def updateUserList():
    global userDict, nickname, fileno
    
    # 刪除原本的lsitbox並更新
    listbox.delete(0, END)
    bcolor = 0
    for k, v in userDict.items():
        if k != fileno or v != nickname:
            bcolor = bcolor + 1
            userID = v + ":" + str(k)
            listbox.insert(END, userID)
            if bcolor%2 == 1:
                listbox.itemconfig(END, bg="#DDFFDD")
            else:
                listbox.itemconfig(END, bg="#FFFFFF")

# binding enter，傳送entry中的訊息到對應的聊天室
def sendMessage(event, roomName, myName):
    global rooms
    
    # 顯示於自己的視窗
    text = rooms[roomName].entry.get()
    if text != "" and text != " ":
        rooms[roomName].entry.delete(0, END)
        rooms[roomName].message.insert(END, text+'\n', "tagMe")
        rooms[roomName].message.see(END)
        
        # 傳送至對方的聊天室
        sock.sendall(("messagePass "+roomName+" "+myName+" "+text).encode('UTF-8'))

def handlerAdaptor(fun, roomName, myName):
    return lambda event, fun=fun, roomName=roomName, myName=myName: fun(event, roomName, myName)

# 初始化聊天室
def chat(nickname, fileno):
    global rooms
    
    # 建立自己對應的獨立聊天室
    indexes = listbox.curselection()
    name = listbox.get(indexes[0])
    room = Toplevel()
    room.title(name)
    room.configure(background='#AAFFAA')
    
    message = Text(room, exportselection=False, width=30, font=('微軟正黑體', 10, 'bold'))
    message.grid(row=0, column=0, padx=5, pady=5)
    message.tag_config("tagOther", foreground="black", justify=LEFT)
    message.tag_config("tagMe", foreground="black", background="#DDFFDD", justify=RIGHT)
    
    entry = Entry(room, width=30, font=('微軟正黑體', 10, 'bold'))
    entry.grid(row=1, column=0, sticky=E, padx=5, pady=5)
    entry.bind("<Return>", handlerAdaptor(sendMessage, name, (nickname+":"+fileno)))

    # 建立物件
    NewRoom = RoomItems(room, message, entry)
    rooms[name] = NewRoom
    
    # 通知對方開啟聊天室
    sock.sendall(("roomOpen "+name+" "+nickname+":"+fileno).encode('UTF-8'))

# 主程式開始
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 12345))

# 輸入暱稱
nickname = input("請輸入你的暱稱...\n")
sock.sendall(nickname.encode('UTF-8'))
fileno = sock.recv(1024).decode('UTF-8')

th1 = threading.Thread(target=recvThread)
th1.setDaemon(True)
th1.start()

# 圖形介面布局
root = Tk()
root.title("Line")
root.configure(background='#AAFFAA')
root.protocol('WM_DELETE_WINDOW', rootClose)

# 標題
label = Label(root, text="使用者(線上)", width=30, bg='#AAFFAA', font=('微軟正黑體', 10, 'bold'))
label.grid(row=0, column=0, pady=5)

# 使用者列表
listbox = Listbox(root, width=30, height=15, font=('微軟正黑體', 15, 'bold'))
listbox.grid(row=1, column=0, padx=5)

# 開啟聊天室按鍵
button = Button(root, text="開始聊天", width=15, relief=GROOVE, fg="white", bg="green3", font=('微軟正黑體', 10, 'bold'), command=lambda:chat(nickname, fileno))
button.grid(row=2, column=0, pady=5)

updateUserList()

root.mainloop()