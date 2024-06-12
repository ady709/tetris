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

        #playArea
        self.frame = ttk.Frame(root, borderwidth=2, relief='ridge')
        self.frame.grid(row=1, column=1, rowspan=2)

        self.can = tk.Canvas(self.frame, width=self.canW + 1, height=self.canH + 1, background='darkgrey')
        self.can.pack()
        self.can.config(scrollregion=(0, 0, self.canW, self.canH))

        #nextPiece
        self.frameNext = ttk.Frame(root, borderwidth=0, relief = 'ridge')
        self.frameNext.grid(row=1, column=2, sticky='n')
        self.canNextW = self.canNextH = self.blockSize*5
        self.canNext = tk.Canvas(self.frameNext, width=self.canNextW, height=self.canNextH)
        self.canNext.pack()
        self.canNext.config(scrollregion=(0, 0, self.canNextW, self.canNextH))

    def updateView(self):

        def drawObject(obj, canv):
            for y in range(0,len(obj.cmap)):
                for x in range(0,len(obj.cmap[y])):
                    xpos = (obj.c)*self.blockSize+x*self.blockSize
                    ypos = obj.r * self.blockSize+y*self.blockSize
                    blockColor = obj.cmap[y][x]
                    if blockColor:
                        canv.create_rectangle(xpos, ypos, xpos + self.blockSize, ypos + self.blockSize,
                                                  fill=blockColor)


        #clear all shapes
        for item in self.can.find_all():
            self.can.delete(item)
        for item in self.canNext.find_all():
            self.canNext.delete(item)
        #draw playfield
        for y,row in enumerate(self.model.playArea):
            for x,color in enumerate(row):
                if color:
                    xpos = x*self.blockSize
                    ypos = y*self.blockSize
                    self.can.create_rectangle(xpos, ypos, xpos+self.blockSize, ypos+self.blockSize, fill=color)
        #draw played object
        drawObject(self.model.object, self.can)

        #draw next object
        drawObject(self.model.nextObject, self.canNext)

    def keyInput(self,event):
        self.controller.keyInput(event)