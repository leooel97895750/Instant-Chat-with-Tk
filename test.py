# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 15:42:43 2019

@author: leooe
"""

from tkinter import *
root = Tk()
ncnu = PhotoImage(file="anime.png")
text = Text(root)
text.image_create(END, image=ncnu)
text.insert(END, "\nNCNU LOGO\n")
text.pack()
root.mainloop()