class Animation:
    def __init__(self, parent, anim):
        self.parent = parent
        self.animationStep = 0
        #copy complete rows to own list
        self.completeRows = [item for item in self.parent.model.completeRows]
        self.parent.gameStatus = 'suspended'
        self.anim = anim
        self.timer = 20
        if not anim in (1,2,3,4):
            anim = 1
        #delete from left to right
        if anim == 1:
            self.lastStep = self.parent.model.columns - 1
        #move down
        if anim == 2:
            self.lastStep = len(self.completeRows) * self.parent.view.blockSize + 1
        #shrink to disappear
        if anim == 3:
            self.lastStep = self.parent.view.blockSize/2
        #
        if anim == 4:
            #TBC
            pass

        self.timer = int(self.parent.model.timer / self.lastStep)

        self.nextStep()
        #self.parent.root.after(20, self.nextStep)


    def nextStep(self):
        if self.anim == 1:
            for r in self.completeRows:
                b = self.parent.view.viewarea[r][self.animationStep]
                self.parent.view.can.delete(b)

        if self.anim == 2:
            for r in self.completeRows:
                for b in self.parent.view.viewarea[r]:
                    self.parent.view.can.move(b,0,1)

        if self.anim == 3:
            for r in self.completeRows:
                for c in range(0, self.parent.view.columns):
                    b = self.parent.view.viewarea[r][c]
                    coords = self.parent.view.can.coords(b)
                    self.parent.view.can.coords(b, coords[0]+1, coords[1]+1, coords[2]-1, coords[3]-1)

        if self.anim == 4:
            #TBC
            pass

        self.animationStep += 1

        if self.animationStep <= self.lastStep:
            self.parent.root.after(self.timer, self.nextStep)

        if self.animationStep > self.lastStep:
            self.parent.gameStatus = 'continuing'
            self.parent.tick(True)