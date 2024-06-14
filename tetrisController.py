class TetrisController:
    def __init__(self, root, model, view):
        self.root = root
        self.model = model
        self.view = view
        self.root.after(500, self.tick)

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
        print('ctl.tick')
        self.model.tick()
        self.view.updateView()
        self.root.after(300, self.tick)

