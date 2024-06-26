import tkinter as tk
from tkinter import ttk
#TODO:animation

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
        self.combos = {1:'Singles', 2:'Doubles', 3:'Tripples', 4:'Tetris'}
        self.selectedScorePos = None
        self.playedobjectblocks = list()
        self.viewarea = list()
        self.playedobjectblocks = list()

        # root.columnconfigure(0, weight=2)
        # root.columnconfigure(1, weight=2)
        # root.columnconfigure(3, weight=2)
        # root.columnconfigure(4, weight=2)
        # root.columnconfigure(5, weight=1)
        # root.columnconfigure(6, weight=1)

        #column 0-4 : play area
        #score colum 0-1
        ttk.Label(root, text='Score:', font=('Arial', 16), background=self.background).grid(row=0, column=0, sticky='e')
        self.score = ttk.Label(root, font=('Arial', 16), background=self.background, text='0')
        self.score.grid(row=0, column=1, sticky='w')
        #level column 2-3
        ttk.Label(root, text='Level:', font=('Arial', 16), background=self.background).grid(row=0, column=2, sticky='e')
        self.level = ttk.Label(root, font=('Arial', 16), background=self.background)
        self.level.grid(row=0, column=3, sticky='w')
        #playArea column 0-3
        self.frame = tk.Frame(root, borderwidth=8, relief='ridge', background=self.background)
        self.frame.grid(row=1, column=0, columnspan=4, rowspan=30)
        self.can = tk.Canvas(self.frame, width=self.canW + 1, height=self.canH + 1, background='darkgrey',
                             borderwidth=0, relief='ridge')
        self.can.config(highlightthickness=0)
        self.can.pack()
        self.can.config(scrollregion=(0, 0, self.canW, self.canH))

        #column 4 : separator
        ttk.Label(root, text='', width=1, background=self.background).grid(row=0, column=4)

        #column 5.. : next piece and information
        startcolumn = 5
        length = 20
        #nextPiece text
        ttk.Label(root, background=self.background, width=5, font=('Arial',12), text='Next:').grid(row=0, column=startcolumn, columnspan=length)
        # nextPiece graphics
        self.frameNext = tk.Frame(root, borderwidth=4, relief='ridge', background=self.background)
        self.frameNext.grid(row=1, column=startcolumn, columnspan=length, sticky='n')
        self.canNextBlockSize = 10
        self.canNextW = self.canNextH = self.canNextBlockSize * 5
        self.canNext = tk.Canvas(self.frameNext, width=self.canNextW, height=self.canNextH, background='grey25', highlightthickness=0)
        self.canNext.pack()
        self.canNext.config(scrollregion=(0, 0, self.canNextW, self.canNextH))
        #combos
        self.comboLabel = dict()
        for i,txt in enumerate(self.combos):
            ttk.Label(root, text=self.combos[i+1], background=self.background, width=8, font=('Arial', 10)).grid(
                row=3+i, column=startcolumn, columnspan=10)
            cb = tk.Label(text='0', background=self.background, width=4, font=('Arial',10))
            cb.grid(row=3+i, column=startcolumn+10+1, columnspan=4)
            self.comboLabel.setdefault(i+1, cb)
        #highScores
        self.highScoreRow = 3+i+1
        tk.Label(text='High score:', font=('Arial',10), background=self.background)\
            .grid(row=self.highScoreRow, column=startcolumn, columnspan=length, sticky='w')
        self.highScoreLabels = list() #added by self.addHighScores()

        #button
        self.button = tk.Button(root, text='Start', command=self.button, width=9)
        self.button.grid(row=21, column=startcolumn, sticky='n', columnspan=length)


    def updateView(self):
        def drawObject(obj, canv, blockSize, xadd=0, yadd=0):
            for y in range(0,len(obj.cmap)):
                for x in range(0,len(obj.cmap[y])):
                    xpos = (obj.c+xadd) * blockSize+x*blockSize
                    ypos = (obj.r+yadd) * blockSize+y*blockSize
                    blockColor = obj.cmap[y][x]
                    if blockColor:
                        canv.create_rectangle(xpos, ypos, xpos + blockSize, ypos + blockSize, fill=blockColor)

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
        drawObject(self.model.object, self.can, self.blockSize)
        #draw next object
        for item in self.canNext.find_all():
            self.canNext.delete(item)
        drawObject(self.model.nextObject, self.canNext, self.canNextBlockSize,
                   xadd=int(self.canNextW/self.canNextBlockSize/2) - int(self.model.nextObject.width/2),
                   yadd=int(self.canNextH/self.canNextBlockSize/2) - int(self.model.nextObject.height/2))




    def updateScore(self):
        #print score
        self.score.configure(text=self.model.score)
        #print combos
        for k,v in self.model.combos.items():
            self.comboLabel[k].configure(text=v)
    def updateLevel(self):
        #print level
        self.level.configure(text=self.model.level)


    def drawPlayArea(self):
        #clear existing blocks
        for r in self.viewarea:
            for b in r:
                self.can.delete(b)
        #draw new playarea
        self.viewarea = list()
        for y,modelrow in enumerate(self.model.playArea):
            viewrow = list()
            for x,color in enumerate(modelrow):
                if color:
                    xpos = x*self.blockSize
                    ypos = y*self.blockSize
                    a = self.can.create_rectangle(xpos, ypos, xpos+self.blockSize, ypos+self.blockSize, fill=color)
                    viewrow.append(a)
            self.viewarea.append(viewrow)

    def drawObject1(self, obj, canv, blockSize, xadd=0, yadd=0):
        #clear current
        if canv is self.can:
            for b in self.playedobjectblocks:
                self.can.delete(b)
            self.playedobjectblocks = []

        if canv is self.canNext:
            for b in self.canNext.find_all():
                self.canNext.delete(b)
        #draw new
        for y in range(0, len(obj.cmap)):
            for x in range(0, len(obj.cmap[y])):
                xpos = (obj.c + xadd) * blockSize + x * blockSize
                ypos = (obj.r + yadd) * blockSize + y * blockSize
                blockColor = obj.cmap[y][x]
                if blockColor:
                    a = canv.create_rectangle(xpos, ypos, xpos + blockSize, ypos + blockSize, fill=blockColor)
                    if canv is self.can:
                        self.playedobjectblocks.append(a)


    def clearPlayArea(self):
        for item in self.can.find_all():
            self.can.delete(item)

    #game over
    def gameOver(self):
        self.can.create_text((self.canW/2,self.canH/2), text='Game Over', font=('Arial',28), anchor="center", fill='black')


    def keyInput(self,event):
        self.controller.keyInput(event)

    def button(self):
        self.controller.button()

    def on_score_pos_label_entered(self, event):
        if self.controller.gameStatus != 'stopped' or event.widget is self.selectedScorePos:
            return
        event.widget.configure(background='tan1')
    def on_score_pos_label_left(self, event):
        if not event.widget is self.selectedScorePos:
            event.widget.configure(background=self.root.cget('background'))

    def clear_pos_label(self):
        for label in self.highScoreLabels:
            label['pos'].configure(background = self.root.cget('background'))

    def on_score_pos_label_click(self,event):
        if self.controller.gameStatus != 'stopped':
            return
        self.clear_pos_label()
        if self.selectedScorePos is event.widget:
            self.selectedScorePos = None
            return
        self.selectedScorePos = event.widget
        event.widget.configure(background='IndianRed1')
        print(f"{self.selectedScorePos.cget('text')} selected")

    def addHighScores(self):
        for r in self.highScoreLabels:
            for l in r.values():
                l.destroy()
        self.selectedScorePos = None
        self.highScoreLabels = list()
        for i,s in enumerate(self.controller.highScore):
            r=dict()
            pos = tk.Label(text=str(i+1), font=('Arial',10), background=self.background ,width=2)
            pos.grid(row=self.highScoreRow+1+i, column=5, sticky='e')
            pos.bind('<Enter>', self.on_score_pos_label_entered)
            pos.bind('<Leave>', self.on_score_pos_label_left)
            pos.bind('<ButtonPress-1>', self.on_score_pos_label_click)
            r['pos'] = pos
            name = tk.Label(text=s['name'], font=('Arial',10), background=self.background, width=10)
            name.grid(row=self.highScoreRow+1+i, column=6, columnspan=10, sticky='w')
            r['name'] = name
            score = tk.Label(text=s['score'], font=('Arial',10), background=self.background, width=10)
            score.grid(row=self.highScoreRow+1+i, column=17, columnspan=9, sticky='w')
            r['score'] = score
            self.highScoreLabels.append(r)
#end class