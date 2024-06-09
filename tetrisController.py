class TetrisController:
    def __init__(self, root, model, view):
        self.root = root
        self.model = model
        self.view = view

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
