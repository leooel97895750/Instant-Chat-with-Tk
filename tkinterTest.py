# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 21:42:44 2019

@author: leooe
"""
from tkinter import *

fruits = ["Leo", "Tony", "Andy", "Judy", "Alex", "Frank", "Jimmy", "John", "Cindy", "Tom", "Jack"]
rooms = {}

class RoomItems():
    def __init__(self, room, message, entry):
        self.room = room
        self.message = message
        self.entry = entry

def sendMessage(event, name):
    global rooms
    
    text = rooms[name].entry.get()
    rooms[name].entry.delete(0, END)
    rooms[name].message.insert(END, text)
    rooms[name].message.see(END)

def callback(event):
    obj = event.widget
    obj.button.click()

def chat():
    global rooms
    
    indexes = listbox.curselection()
    name = listbox.get(indexes[0])
    room = Toplevel()
    room.title(name)
    
    message = Listbox(room)
    message.pack()
    
    entry = Entry(room)
    entry.pack()
    entry.bind("<Return>", sendMessage(name))

    NewRoom = RoomItems(room, message, entry)
    rooms[name] = NewRoom
    
root = Tk()

label = Label(root, text="Line")
label.pack()

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(root, yscrollcommand=scrollbar.set)
for fruit in fruits:
    listbox.insert(END, fruit)
listbox.pack()
scrollbar.config(command=listbox.yview)

button = Button(root, text="開始聊天", command=chat)
button.pack()

root.mainloop()