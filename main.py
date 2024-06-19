import tkinter as tk
from tkinter import ttk

from tetrisView import TetrisView
from tetrisModel import TetrisModel
from tetrisController import TetrisController

blockSize = 20
playAreaColumns = 10
playAreaRows = 21


#maint window
root = tk.Tk()
root.title('Tetris')
background = 'DarkOrange4'
root.configure(padx=5, pady=5, background=background)
root.resizable(False, False)


#view
model = TetrisModel(playAreaRows, playAreaColumns)
view = TetrisView(root, controller=None, model=model, blockSize=blockSize, rows=playAreaRows, columns=playAreaColumns, background=background)
controller = TetrisController(root, model, view)
view.controller = controller

view.addHighScores()

root.mainloop()

