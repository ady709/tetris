import random
from datetime import datetime
random.seed(datetime.now().microsecond)

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
        self.rows = rows
        self.columns = columns
        self.playArea = [[None for i in range(0, columns)] for o in range(0, rows)]
        self.addObject = True
        self.landed = False
        self.completeRows = []
        self.nextObject = Object(shape=self.getRandomObject())
        self.gameOver = False

    def tick(self):
        if self.gameOver:
            return
        if self.addObject:
            #add new object if needed
            self.object = Object(shape=self.nextObject.cmap, r=0, c=int(self.columns / 2))
            self.nextObject = Object(shape=self.getRandomObject())
            self.addObject = False
            #check for game over
            gameOver=False
            for y,row in enumerate(self.object.cmap):
                for x,block in enumerate(row):
                    if self.object.cmap[y][x] and self.playArea[self.object.r+y][self.object.c+x]:
                        gameOver = True
                        break
                    if gameOver:
                        break
            if gameOver:
                self.gameOver = True
            return

        #see if the objact has landed
        for x, y in enumerate(self.object.bottom):
            if not y is None:
                if self.object.r + y == self.rows - 1 or self.playArea[self.object.r + y + 1][self.object.c + x]:
                    self.landed = True

        if self.landed:
            for y, row in enumerate(self.object.cmap):
                for x, block in enumerate(row):
                    if block:
                        self.playArea[self.object.r + y][self.object.c + x] = block
            self.addObject = True
            self.landed = False
            self.checkCompleteRows()
            self.removeCompleteRows()
            self.tick()

        #fall the object down
        if not self.landed and not self.addObject:
            self.object.r += 1
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

