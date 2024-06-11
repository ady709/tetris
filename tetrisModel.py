from random import random


#objects: tri, square, i, s, rs, l, j

class Object:
    def __init__(self, shape=None, r=0, c=0):
        self.c = c
        self.r = r
        if shape is None:
            raise AttributeError
        if shape == 'tri':
            self.cmap = [['gold4', None],
                         ['gold4', 'gold4'],
                         ['gold4', None]]
        elif shape == 'square':
            self.cmap = [['blue', 'blue'],
                         ['blue', 'blue']]
        elif shape == 'i':
            self.cmap = [['red', 'red', 'red', 'red']]
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
        #TODO?? self.c = self.c - int(width)/2

        print(f'L:{self.leftmost}')
        print(f'R:{self.rightmost}')
        print(f'B:{self.bottom}')

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
    probability = {'tri': 20, 'square': 40, 'i': 50, 's': 60, 'rs': 70, 'l': 80, 'j': 100}

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.playArea = [[None for i in range(0, columns)] for o in range(0, rows)]
        self.addObject = True
        self.landed = False

    def tick(self):
        if self.addObject:
            #add new object if needed
            self.object = Object(shape=self.getRandomObject(), r=0, c=int(self.columns / 2))
            self.addObject = False
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

        #fall the object down
        if not self.landed and not self.addObject:
            self.object.r += 1
        print(f'xpos:{self.object.c} ypos:{self.object.r}')

    def goLeft(self):
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
        print(f'xpos:{self.object.c} ypos:{self.object.r}')
    def goRight(self):
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
        print(f'xpos:{self.object.c} ypos:{self.object.r}')

    def rotate(self):
        rotatedObject = self.object.getRotatedObject()
        shift = (self.object.width - rotatedObject.width) / 2
        addition = 0.5 if shift > 0 else -0.5
        rotatedObject.c += (int(shift + addition))
        print(f'rotated object x:{rotatedObject.c} y:{rotatedObject.r}')
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
            print(f'shifting {sh}')
            if rotatedObject.r + rotatedObject.height > self.rows\
            or rotatedObject.c < 0\
            or rotatedObject.c + rotatedObject.width > self.columns:
                print(f'ng {rotatedObject.c} {rotatedObject.r}')
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
            print(f'Rotated, new pos x:{rotatedObject.c} y:{rotatedObject.r}')
            self.object = rotatedObject

    def getRandomObject(self):
        r = int(random() * 100)
        for k, v in self.probability.items():
            if r < v:
                print(k)
                return k
