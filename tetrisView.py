import tkinter as tk
from tkinter import ttk


class TetrisView:
    def __init__(self,root,controller,model, blockSize, rows, columns, background):
        self.root = root
        self.root.bind("<KeyPress>", self.keyInput)
        self.controller = controller
        self.model = model
        self.blockSize = blockSize
        self.canH = blockSize*rows
        self.canW = blockSize*columns
        self.background = background

        #score
        ttk.Label(text='Score:', font=('Arial',16), background=self.background).grid(row=0,column=0, sticky='e')
        self.score = ttk.Label(font=('Arial',16), background=self.background, text='0')
        self.score.grid(row=0, column=1, sticky='w')
        #level
        ttk.Label(text='Level:', font=('Arial', 16), background=self.background).grid(row=0, column=2, sticky='e')
        self.level = ttk.Label(font=('Arial', 16), background=self.background)
        self.level.grid(row=0, column=3, sticky='w')

        #playArea
        self.frame = tk.Frame(root, borderwidth=8, relief='ridge', background=self.background)
        self.frame.grid(row=1, column=0, rowspan=8, columnspan=4)

        self.can = tk.Canvas(self.frame, width=self.canW + 1, height=self.canH + 1, background='darkgrey', borderwidth=0, relief='ridge')
        self.can.config(highlightthickness=0)
        self.can.pack()
        self.can.config(scrollregion=(0, 0, self.canW, self.canH))

        #separator
        ttk.Label(root,text='', width=1, background=self.background).grid(row=0, column=4)

        #nextPiece
        ttk.Label(root, background=self.background, width=5, font=('Arial',12), text='Next:').grid(row=0, column=5)
        self.frameNext = tk.Frame(root, borderwidth=4, relief='ridge', background=self.background)
        self.frameNext.grid(row=1, column=5, sticky='n')
        self.canNextBlockSize = 5
        self.canNextW = self.canNextH = self.blockSize*self.canNextBlockSize
        self.canNext = tk.Canvas(self.frameNext, width=self.canNextW, height=self.canNextH, background='grey25', highlightthickness=0)
        self.canNext.pack()
        self.canNext.config(scrollregion=(0, 0, self.canNextW, self.canNextH))

        #button
        self.button = tk.Button(root,text='Start', command=self.button)
        self.button.grid(row=2, column=5, sticky='n')

    def updateView(self):
        def drawObject(obj, canv, xadd=0, yadd=0):
            for y in range(0,len(obj.cmap)):
                for x in range(0,len(obj.cmap[y])):
                    xpos = (obj.c+xadd)*self.blockSize+x*self.blockSize
                    ypos = (obj.r+yadd) * self.blockSize+y*self.blockSize
                    blockColor = obj.cmap[y][x]
                    if blockColor:
                        canv.create_rectangle(xpos, ypos, xpos + self.blockSize, ypos + self.blockSize,
                                                  fill=blockColor)

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
        drawObject(self.model.object, self.can)
        #draw next object
        for item in self.canNext.find_all():
            self.canNext.delete(item)
        drawObject(self.model.nextObject, self.canNext,
                   xadd=int(self.canNextBlockSize/2) - int(self.model.nextObject.width/2),
                   yadd=int(self.canNextBlockSize/2) - int(self.model.nextObject.height/2))

        #print score
        self.score.configure(text=self.model.score)
        #print level
        self.level.configure(text=self.model.level)

    #game over
    def gameOver(self):
        self.can.create_text((self.canW/2,self.canH/2), text='Game Over', font=('Arial',36), anchor="center", fill='black')

    def keyInput(self,event):
        self.controller.keyInput(event)

    def button(self):
        self.controller.button()
