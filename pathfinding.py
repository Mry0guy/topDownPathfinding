__author__ = 'Ryan'

path = []
blockList = []
widget = 1
level = []

def __init__(map):
    global blockList
    global level
    global widget
    global path
    widget = 0
    level = map
    blockList = []
    printLevel()
    for x in range(len(level)):
        blockList.append([])
        for y in range(len(level[x])):
            blockList[x].append(' ')

def setStart(x, y):
    blockList[x][y] = startblock(x,y)



def setEnd(i, n):
    for x in range(len(blockList)):
        for y in range(len(blockList[i])):
            if type(blockList[x][y]) is startblock :
                    blockList[x][y].endX = i
                    blockList[x][y].endY = n
                    return None
    print('no start')

def start(map):
    level = map
    path = None
    for x in range(len(blockList)):
        for y in range(len(blockList[x])):
            if type(blockList[x][y]) is startblock:
                if blockList[x][y].endX is not None and blockList[x][y].endY is not None:
                    path = blockList[x][y].search()
            else:
                blockList[x][y] = ' '
    return path



def retrace(last):
    path = []
    path.append((last.x, last.y))
    block = last.prev
    while block.prev != None:
        path.append((block.x,block.y))
        block = block.prev
    for x in range(len(blockList)):
        for y in range(len(blockList[x])):
            if type(blockList[x][y]) is startblock :
                    blockList[x][y].compleated = path



def printLevel():
    for n in range(len(level)):
        print('~',end='   ')
    print('~\n')
    for y in range(len(level[0])):
        print('|',end='')
        for x in range(len(level)):
            tile = level[x][y]
            if tile == 0:
                print(' ', end='   ')
            elif tile == 2:
                print('#', end='   ')
            elif tile == 1:
                print('@', end='   ')
        print('|\n')
    for n in range(len(level)):
        print('~',end='   ')
    print('~\n')

def printBlocks():
    for n in range(len(blockList)):
        print('~',end='   ')
    print('~\n')
    for y in range(len(blockList[0])):
        print('|',end='')
        for x in range(len(blockList)):
            if type(blockList[x][y]) is block:
                print(blockList[x][y].gen,end='   ')
            if type(blockList[x][y]) is startblock:
                print('S',end='   ')
            if type(blockList[x][y]) is str:
                print(' ', end='   ')
        print('|\n')
    for n in range(len(blockList)):
        print('~',end='   ')
    print('~\n')

class block(object):
    def __init__(self, x, y, prev):
        self.x = x
        self.y = y
        self.prev = prev
        self.gen = prev.gen + 1
        self.children = []
        for x in range(len(blockList)):
            for y in range(len(blockList[x])):
                if type(blockList[x][y]) is startblock :
                    if (self.x, self.y) == (blockList[x][y].endX, blockList[x][y].endY):
                        startblock.compleated = True
                        retrace(self)


    def spread(self, age):
        if self.gen <= age:
            try:
                if blockList[self.x][self.y+1] == ' ' and level[self.x][self.y+1] != 2:
                    blockList[self.x][self.y+1] = block(self.x, self.y + 1, self)
                    self.children.append(blockList[self.x][self.y+1])
            except:
                widget =1
            try:
                if blockList[self.x+1][self.y] == ' ' and level[self.x+1][self.y] != 2:
                    blockList[self.x+1][self.y] = block(self.x + 1, self.y, self)
                    self.children.append(blockList[self.x+1][self.y])
            except:
                widget = 1
            if self.y != 0:
                if blockList[self.x][self.y-1] == ' ' and level[self.x][self.y-1] != 2:
                    blockList[self.x][self.y-1] = block(self.x, self.y - 1, self)
                    self.children.append(blockList[self.x][self.y-1])

            if self.x != 0:
                if blockList[self.x-1][self.y] == ' ' and level[self.x-1][self.y] != 2:
                    blockList[self.x-1][self.y] = block(self.x - 1, self.y, self)
                    self.children.append(blockList[self.x-1][self.y])

            for child in self.children:
                child.spread(age)

class startblock(block):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prev = None
        self.gen = 0
        self.children = []
        self.compleated = False
        self.endX = None
        self.endY = None

        for x in range(len(blockList)):
            for y in range(len(blockList[x])):
                if type(blockList[x][y]) is startblock :
                    blockList[x][y] = ' '

    def search(self):
        age = 0
        while self.compleated == False:
            print(age)
            printBlocks()
            self.spread(age)
            age += 1
        return self.compleated
