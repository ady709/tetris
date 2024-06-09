from random import random
#objects: tri, square, i, s, rs, l, j

class Object:
    def __init__(self, shape, r, c):
        if shape == 'tri':
            self.cmap = [[None,'gold4',None,None],
                        [None,'gold4','gold4',None],
                        [None,'gold4',None,None],
                        [None,None,None,None]]
        elif shape == 'square':
            self.cmap = [['blue','blue',None,None],
                         ['blue','blue',None,None],
                         [None,None,None,None],
                         [None,None,None,None]]
        elif shape == 'i':
            self.cmap = [['red','red','red','red'],
                         [None,None,None,None],
                         [None,None,None,None],
                         [None,None,None,None]]
        elif shape == 's':
            self.cmap = [['green2', None, None, None],
                         ['green2', 'green2', None, None],
                         [None, 'green2', None, None],
                         [None, None, None, None]]

        elif shape == 'rs':
            self.cmap = [[None, 'deep sky blue', None, None],
                         ['deep sky blue', 'deep sky blue', None, None],
                         ['deep sky blue', None, None, None],
                         [None, None, None, None]]
        elif shape == 'l':
            self.cmap = [['purple',None,None,None],
                         ['purple',None,None,None],
                         ['purple','purple',None,None],
                         [None,None,None,None]]
        elif shape == 'j':
            self.cmap = [[None,'tomato',None,None],
                         [None,'tomato',None,None],
                         ['tomato','tomato',None,None],
                         [None,None,None,None]]

        self.c = c
        self.r = r
        self.leftmost = []
        self.rightmost = []
        self.bottom = []
        self.updateLimits()

    def centerPos(self):
        pass

    def updateLimits(self):
        self.leftmost = []
        self.rightmost = []
        self.bottom = [None,None,None,None]
        for y,row in enumerate(self.cmap):
            rightmost = leftmost = None
            for x,block in enumerate(row):
                if block:
                    if leftmost is None or x<leftmost: leftmost = x
                    if rightmost is None or x>rightmost: rightmost = x
                    if self.bottom[x] is None or y>self.bottom[x]: self.bottom[x] = y
            self.leftmost.append(leftmost)
            self.rightmost.append(rightmost)

        leftmin = min([item for item in self.leftmost if item is not None])
        rightmax = max([item for item in self.rightmost if item is not None])
        width = rightmax-leftmin
        #TODO?? self.c = self.c - int(width)/2

        print(f'L:{self.leftmost}')
        print(f'R:{self.rightmost}')
        print(f'B:{self.bottom}')

    def getRotatedCmap(self):
        longestRow=0
        for r in self.cmap:
            if len(r)>longestRow:
                longestRow = len(r)
        cmap = [[None for i in range(0,longestRow)] for o in range(0,len(self.cmap))]
        for y,row in enumerate(self.cmap):
            for x,block in enumerate(row):
                cmap[x][len(cmap)-1-y] = block
        return cmap

class TetrisModel:
    probability = {'tri': 20, 'square': 40, 'i': 50, 's': 60, 'rs': 70, 'l': 80, 'j': 100}
    def __init__(self,rows, columns):
        self.rows = rows
        self.columns = columns
        self.playArea = [[None for i in range(0,columns)] for o in range(0,rows)]
        self.addObject = True
        self.landed = False


    def tick(self):
        if self.addObject:
            #add new object if needed
            self.object = Object(shape=self.getRandomObject(), r=0, c=int(self.columns/2))
            self.addObject = False
            return

        #see if the objact has landed
        for x,y in enumerate(self.object.bottom):
            if not y is None:
                if self.object.r+y==self.rows-1 or self.playArea[self.object.r+y+1][self.object.c+x]:
                    self.landed = True

        if self.landed:
            for y,row in enumerate(self.object.cmap):
                for x,block in enumerate(row):
                    if block:
                        self.playArea[self.object.r+y][self.object.c+x] = block
            self.addObject = True
            self.landed = False


        #fall the object down
        if not self.landed and not self.addObject:
            self.object.r+=1
        print(f'xpos:{self.object.c} ypos:{self.object.r}')

    def goLeft(self):
        cando = True
        for r,x in enumerate(self.object.leftmost):
            if not x is None:
                if self.object.c+x == 0:
                    cando = False
                else:
                    if self.playArea[self.object.r+r][self.object.c+x-1]:
                        cando = False
        if cando:
            self.object.c-=1

    def goRight(self):
        cando = True
        for r,x in enumerate(self.object.rightmost):
            if not x is None:
                if self.object.c + x == self.columns-1:
                    cando = False
                else:
                    if self.playArea[self.object.r + r][self.object.c + x + 1]:
                        cando = False
        if cando:
            self.object.c += 1

    def rotate(self):
        self.object.cmap = self.object.getRotatedCmap()
        self.object.updateLimits()

    def getRandomObject(self):
        r = int(random()*100)
        for k,v in self.probability.items():
            if r<v:
                print(k)
                return k