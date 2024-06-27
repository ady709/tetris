class Animation:
    def __init__(self, parent):
        self.parent = parent
        self.animationStep = 0
        self.lastStep = 10

        self.colors = ['grey99','grey90','grey80','grey70','grey60','grey50','grey40','grey30','grey20','grey10']
        self.completeRows = [item for item in self.parent.model.completeRows]
        self.nextStep()
        #self.parent.root.after(20, self.nextStep)

    def nextStep(self):
        if self.animationStep == self.lastStep:
            self.parent.view.drawPlayArea()
            return

        # print(self.colors[self.animationStep])
        # self.parent.view.animateCompleteRows(self.colors[self.animationStep])

        for r in self.completeRows:
            b = self.parent.view.viewarea[r][self.animationStep]
            #self.parent.view.can.itemconfig(b, fill='black')
            self.parent.view.can.delete(b)
            #self.parent.root.update()

        self.animationStep += 1
        self.parent.root.after(20, self.nextStep)
