import random
from datetime import datetime


#objects: tri, square, i, s, rs, l, j

class Object:
    def __init__(self, shape=None, r=0, c=0):
        self.c = c
        self.r = r
        if shape is None:
            print('Shape is None')
            raise AttributeError
        if shape == 'tri':
            self.cmap = [['gold4', None],
                         ['gold4', 'gold4'],
                         ['gold4', None]]
        elif shape == 'square':
            self.cmap = [['blue', 'blue'],
                         ['blue', 'blue']]
        elif shape == 'i':
            self.cmap = [['red'], ['red'], ['red'], ['red']]
        elif shape == 's':
            self.cmap = [['green2', None],
                         ['green2', 'green2'],
                         [None, 'green2']]

        elif shape == 'rs':
            self.cmap = [[None, 'deep sky blue'],
                         ['deep sky blue', 'deep sky blue'],
                         ['deep sky blue', None]]
        elif shape == 'l':
            self.cmap = [['purple', None],
                         ['purple', None],
                         ['purple', 'purple']]
        elif shape == 'j':
            self.cmap = [[None, 'tomato'],
                         [None, 'tomato'],
                         ['tomato', 'tomato']]
        #construct from another object
        elif type(shape) == Object:
            self = shape
        #construct from cmap
        elif type(shape) == list:
            if type(shape[0]) != list:
                print('Shape[0] is not list')
                raise AttributeError
            self.cmap = shape

        if type(shape) != Object:
            self.leftmost = []
            self.rightmost = []
            self.bottom = []
            self.updateLimits()

    def centerPos(self):
        pass

    def updateLimits(self):
        self.leftmost = []
        self.rightmost = []
        self.width = 0
        for r in self.cmap:
            if len(r) > self.width: self.width = len(r)
        self.height = len(self.cmap)
        self.bottom = [None for i in range(0, self.width)]
        for y, row in enumerate(self.cmap):
            rightmost = leftmost = None
            for x, block in enumerate(row):
                if block:
                    if leftmost is None or x < leftmost: leftmost = x
                    if rightmost is None or x > rightmost: rightmost = x
                    if self.bottom[x] is None or y > self.bottom[x]: self.bottom[x] = y
            self.leftmost.append(leftmost)
            self.rightmost.append(rightmost)

        leftmin = min([item for item in self.leftmost if item is not None])
        rightmax = max([item for item in self.rightmost if item is not None])
        width = rightmax - leftmin

    def getRotatedCmap(self):
        cmap = [[]]
        longestRow = 0
        for y in range(len(self.cmap) - 1, -1, -1):

            for x, block in enumerate(self.cmap[y]):
                if len(cmap) < x + 1: cmap.append([])
                cmap[x].append(block)
        return cmap

    def getRotatedObject(self):
        return Object(self.getRotatedCmap(), self.r, self.c)


class TetrisModel:
    shapes = {0:'tri', 1:'square', 2:'i', 3:'s', 4:'rs', 5:'l', 6:'j'}

    def __init__(self, rows, columns):
        self.randomSeed = None
        self.rows = rows
        self.columns = columns
        self.init()

    def init(self, randomSeed=None):
        self.playArea = [[None for i in range(0, self.columns)] for o in range(0, self.rows)]
        self.addObject = True
        self.landed = False
        self.completeRows = []
        self.gameOver = False
        self.score = 0
        self.level = 1
        self.beginTimer = 500
        self.timer = self.beginTimer
        self.removedRows = 0
        self.combos = {1:0, 2:0, 3:0, 4:0}
        self.randomSeed = 123
        if not randomSeed is None and type(randomSeed) == int:
            self.randomSeed = randomSeed
            print('seed loaded')
        else:
            self.randomSeed = datetime.now().microsecond
        random.seed(self.randomSeed)
        print(f'Starting with seed {self.randomSeed}')
        self.nextObject = Object(shape=self.getRandomObject())
        self.status = []
        self.object = None

    def addObjectF(self):
        self.object = Object(shape=self.nextObject.cmap, r=0, c=int(self.columns / 2))
        self.nextObject = Object(shape=self.getRandomObject())
        self.status.append('objectAdded')
        self.addObject = False

    def tick(self):
        self.status = []
        #do not tick if gameOver
        if self.gameOver:
            return
        #remove completed rows from previous tick from playarea
        #the point is that the view has a chance to make an animation between the two ticks
        #it's necessary, however, that the view.playarea has been updated, removing the complete rows even before
        #they dissappear from model.playarea
        if len(self.completeRows):
            self.removeCompleteRows()
            self.status.append('scoreChanged')

        #add object if needed
        if self.addObject:
            self.addObjectF()
            return


        # check if landed
        self.landed = False
        for x, y in enumerate(self.object.bottom):
            if y is not None:
                if self.object.r + y == self.rows - 1 or self.playArea[self.object.r + y + 1][self.object.c + x]:
                    self.landed = True

        if self.landed:
            # copy object to playArea
            for y, row in enumerate(self.object.cmap):
                for x, block in enumerate(row):
                    if block:
                        self.playArea[self.object.r + y][self.object.c + x] = block
            #add new piece
            self.addObject = True
            self.status.append('landed')
            # check complete rows
            self.checkCompleteRows()
            if len(self.completeRows):
                self.status.append('rowsCompleted')

            # check level
            level = int(self.removedRows / 30) + 1
            if level != self.level:
                self.level = level
                self.timer = self.beginTimer - (self.level - 1) * 50
                if self.timer < 50: self.timer = 50
                self.status.append('levelChanged')

            #if new object and landed  and no complete rows -> gameover
            if self.landed and not 'rowsCompleted' in self.status and self.object.r == 0:
                self.gameOver = True
                self.status.append('gameOver')
            #return if landed
            return

        # fall
        self.object.r += 1

        return
    #end of tick

    def goLeft(self):
        if self.gameOver:
            return
        cando = True
        for r, x in enumerate(self.object.leftmost):
            if not x is None:
                if self.object.c + x == 0:
                    cando = False
                else:
                    if self.playArea[self.object.r + r][self.object.c + x - 1]:
                        cando = False
        if cando:
            self.object.c -= 1
    def goRight(self):
        if self.gameOver:
            return
        cando = True
        for r, x in enumerate(self.object.rightmost):
            if not x is None:
                if self.object.c + x == self.columns - 1:
                    cando = False
                else:
                    if self.playArea[self.object.r + r][self.object.c + x + 1]:
                        cando = False
        if cando:
            self.object.c += 1

    def rotate(self):
        if self.gameOver:
            return
        rotatedObject = self.object.getRotatedObject()
        shift = (self.object.width - rotatedObject.width) / 2
        addition = 0.5 if shift > 0 else -0.5
        rotatedObject.c += (int(shift + addition))
        #see if rotated object fits in the playArea
        #tryto shift it if it does not to see if it can be rotated afterwards
        #tupple shift (column,row)
        first_r = rotatedObject.r
        first_c = rotatedObject.c
        shift = [(0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0), (3, 0), (0, -1), (-1, -1), (1, -1)]
        for sh in shift:
            canRotate = True
            rotatedObject.r = first_r + sh[1]
            rotatedObject.c = first_c + sh[0]
            if rotatedObject.r + rotatedObject.height > self.rows\
            or rotatedObject.c < 0\
            or rotatedObject.c + rotatedObject.width > self.columns:
                canRotate = False
                continue
            for y, r in enumerate(rotatedObject.cmap):
                for x, block in enumerate(r):
                    if self.playArea[rotatedObject.r + y][rotatedObject.c + x] and rotatedObject.cmap[y][x]:
                        canRotate = False
                        break
                if not canRotate:
                    break
            if canRotate:
                break
        if canRotate:
            self.object = rotatedObject

    def getRandomObject(self):
        return self.shapes[int(random.random() * 1000) % 7]


    def checkCompleteRows(self):
        self.completeRows = []
        for r,row in enumerate(self.playArea):
            compl = True
            for block in row:
                if not block:
                    compl = False
                    break
            if compl:
                self.completeRows.append(r)


    def removeCompleteRows(self):
        if not len(self.completeRows):
            return
        for r in self.completeRows:
            del(self.playArea[r])
            self.playArea.insert(0,[None for item in range(0,self.columns)])
        self.score += len(self.completeRows)**2
        self.removedRows += len(self.completeRows)
        self.combos[len(self.completeRows)] += 1
        self.completeRows = []

