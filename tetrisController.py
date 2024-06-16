class TetrisController:
    def __init__(self, root, model, view):
        self.gameStatus = 'stopped'
        self.root = root
        self.model = model
        self.view = view
        self.root.after(self.model.timer, self.tick)
        #TODO load high score
        
            

    def keyInput(self,event):
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
        else:
            self.root.after(self.model.timer, self.tick)

    def button(self):
        if self.gameStatus=='stopped':
            self.model.init()
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

        