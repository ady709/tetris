class Animation:
    def __init__(self, parent):
        self.parent = parent
        self.animationStep = 0
        self.lastStep = self.parent.model.columns-1
        #copy complete rows to own list
        self.completeRows = [item for item in self.parent.model.completeRows]

        self.parent.gameStatus = 'suspended'
        self.nextStep()
        #self.parent.root.after(20, self.nextStep)


    def nextStep(self):
        for r in self.completeRows:
            b = self.parent.view.viewarea[r][self.animationStep]
            self.parent.view.can.delete(b)

        if self.animationStep == self.lastStep:
            self.parent.model.removeCompleteRows()
            self.parent.view.drawPlayArea()
            self.parent.gameStatus = 'running'
            self.parent.tick(True)
            return

        self.animationStep += 1
        self.parent.root.after(20, self.nextStep)
