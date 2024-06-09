import tkinter as tk
from tkinter import ttk


class TetrisView:
    def __init__(self,root,controller,model, blockSize, rows, columns):
        self.root = root
        self.root.bind("<KeyPress>", self.keyInput)
        self.controller = controller
        self.model = model
        self.blockSize = blockSize
        self.canH = blockSize*rows
        self.canW = blockSize*columns

        self.frame = ttk.Frame(root, borderwidth=2, relief='ridge')
        self.frame.pack()

        self.can = tk.Canvas(self.frame, width=self.canW + 1, height=self.canH + 1, background='darkgrey')
        self.can.pack()
        self.can.config(scrollregion=(0, 0, self.canW, self.canH))

    def updateView(self):
        #clear all shapes
        for item in self.can.find_all():
            self.can.delete(item)
        #draw playfield
        for y,row in enumerate(self.model.playArea):
            for x,color in enumerate(row):
                if color:
                    xpos = x*self.blockSize
                    ypos = y*self.blockSize
                    self.can.create_rectangle(xpos, ypos, xpos+self.blockSize, ypos+self.blockSize, fill=color)
        #draw played object
        for y in range(0,len(self.model.object.cmap)):
            for x in range(0,len(self.model.object.cmap[y])):
                xpos = (self.model.object.c)*self.blockSize+x*self.blockSize
                ypos = self.model.object.r * self.blockSize+y*self.blockSize
                clr = self.model.object.cmap[y][x]
                if clr:
                    self.can.create_rectangle(xpos, ypos, xpos + self.blockSize, ypos + self.blockSize,
                                              fill=clr)

    def keyInput(self,event):
        self.controller.keyInput(event)