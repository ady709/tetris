import csv
import tkinter as tk

import os

class TetrisController:
    def __init__(self, root, model, view):
        self.gameStatus = 'stopped'
        self.root = root
        self.model = model
        self.view = view
        self.root.after(self.model.timer, self.tick)
        #cwd = os.getcwd()
        self.cwd=os.path.dirname(os.path.realpath(__file__))
        self.loadScore()
        self.randomSeed = None



            

    def keyInput(self,event):
        if self.gameStatus=='frozen':
            return
        if event.keysym == 'space':
            self.button()
        if self.gameStatus=='running':
            if event.keysym == 'Down':
                self.model.tick()
            elif event.keysym == 'Left':
                self.model.goLeft()
            elif event.keysym == 'Right':
                self.model.goRight()
            elif event.keysym == 'Up':
                self.model.rotate()
            self.view.updateView()




    def tick(self):
        if not self.gameStatus == 'running':
            return
        self.model.tick()
        self.view.updateView()
        #check for game over
        if self.model.gameOver:
            self.gameStatus = 'stopped'
            self.view.gameOver()
            self.view.button.configure(text='Start')
            self.checkHighScore()
        else:
            self.root.after(self.model.timer, self.tick)

    def button(self):
        if self.gameStatus=='stopped':
            try:
                print(f'Challenging {self.view.selectedScorePos.cget('text')}')
                seedPos = int(self.view.selectedScorePos.cget('text'))-1 \
                    if isinstance(self.view.selectedScorePos, tk.Label)\
                    else None
                self.randomSeed = int(self.highScore[seedPos]['seed'])
            except:
                self.randomSeed = None
            self.model.init(self.randomSeed)
            self.view.button.configure(text='Pause')
            self.gameStatus = 'running'
            self.tick()
        elif self.gameStatus == 'running':
            self.view.button.configure(text='Continue')
            self.gameStatus = 'paused'
        elif self.gameStatus == 'paused':
            self.view.button.configure(text='Pause')
            self.gameStatus = 'running'
            self.tick()

    def loadScore(self):
        try:
            with open(self.cwd+'/scores.csv','r') as file:
                reader = csv.DictReader(file, delimiter=';')
                self.highScore = list(reader)
                self.sortScore()
                if len(self.highScore)>10: self.highScore = self.highScore[:10]
        except:
            self.highScore = list()
        
    def sortScore(self):
        sortedScore = list()
        while(len(self.highScore)):
            idx = max = 0
            for i,s in enumerate(self.highScore):
                try:
                    if int(s['score']) > max:
                        max = int(s['score'])
                        idx = i
                except ValueError:
                    s['score'] = '0'
            sortedScore.append(self.highScore.pop(idx))
        self.highScore = sortedScore

    def checkHighScore(self):

        def getName():
            name = entry.get()
            if len(name):
                newrecord = {'name': name, 'score': self.model.score, 'level': self.model.level,
                             'singles': self.model.combos[1], 'doubles': self.model.combos[2],
                             'tripples': self.model.combos[3], 'tetris': self.model.combos[4],
                             'seed': self.model.randomSeed}
                nameWindow.destroy()
                if len(self.highScore)<10:
                    self.highScore.append(newrecord)
                else:
                    self.highScore[-1] = newrecord

                self.sortScore()
                self.view.addHighScores()
                self.saveHighScore()
                self.gameStatus = 'stopped'
                self.view.button.configure(state=tk.NORMAL)
                print(newrecord)

        if len(self.highScore)==0 or self.model.score > int(self.highScore[-1]['score']) and self.model.score>0:
            self.gameStatus='frozen'
            self.view.button.configure(state=tk.DISABLED)
            nameWindow = tk.Tk()
            nameWindow.eval('tk::PlaceWindow . center')
            nameWindow.configure(padx=30, pady=10)
            nameWindow.title('Enter Name')
            tk.Label(nameWindow, text='Enter your name').grid(row=0,column=0)
            entry = tk.Entry(nameWindow, width=20)
            entry.grid(row=1, column=0, columnspan=4)
            nameWindow.focus_set()
            entry.focus_set()
            entry.bind('<KeyPress>', lambda x: getName() if x.keysym=='Return' else  None)
            tk.Button(nameWindow,text='OK', command=getName, width=4).grid(row=2, column=2)
            nameWindow.protocol("WM_DELETE_WINDOW", getName)

    def saveHighScore(self):
        with open(self.cwd+'/scores.csv','w') as file:
            savelist = ['name','score','level','singles','doubles','tripples','tetris','seed']
            header = ';'.join(savelist)
            file.write(header)
            file.write('\n')
            for row in self.highScore:
                record = [str(row[item]) for item in savelist]
                saverow = ';'.join(record)
                file.write(saverow)
                file.write('\n')

    def setRandomSeed(self, posNr):
        print(posNr)
        print(self.highScore)
        try:
            self.randomSeed = int(self.highScore[int(posNr)-1]['seed'])
        except:
            self.view.selectedScorePos = None
            print(self.highScore[int(posNr)-1]['seed'])