__author__ = 'rguild'
import pygame
import pathfinding

pygame.init()
class levelmaker(object):
    def __init__(self):
        self.level = []
        for x in range(10):
            self.level.append([])
            for y in range(10):
                self.level[x].append(0)
        self.leveleditor = False
        self.tileSurface = pygame.Surface((100, 100))
        self.mapSurface = pygame.Surface((1000, 1000))
        self.grass = pygame.Surface.convert(pygame.image.load("grass.PNG"))
        self.rocks = pygame.Surface.convert(pygame.image.load("rocks.PNG"))
        self.water = pygame.Surface.convert(pygame.image.load("water.png"))
        self.grassBorderN = pygame.Surface.convert_alpha(pygame.image.load("grassBorderN.png"))
        self.grassBorderS = pygame.Surface.convert_alpha(pygame.image.load("grassBorderS.png"))
        self.grassBorderE = pygame.Surface.convert_alpha(pygame.image.load("grassBorderE.png"))
        self.grassBorderW = pygame.Surface.convert_alpha(pygame.image.load("grassBorderW.png"))

    def new_level(self, X, Y):
        self.level = []
        for x in range(X):
            self.level.append([])
            for y in range(Y):
                self.level[x].append(0)
        self.mapSurface = pygame.Surface((100 * len(self.level), 100 * len(self.level[1])))

    def draw_map(self):
        for x in range(len(self.level)):
            for y in range(len(self.level[x])):
                tile = self.level[x][y]
                if tile == 1:
                    self.tileSurface = self.rocks.copy()
                elif tile == 2:
                    self.tileSurface = self.water.copy()
                elif tile == 0:
                    self.tileSurface = self.grass.copy()
                    if self.checkrocks(x, y) != False:
                        rlist = self.checkrocks(x, y)
                        if "W" in rlist:
                            self.tileSurface.blit(self.grassBorderW, pygame.Rect((0, 0), (5, 100)))
                        if "E" in rlist:
                            self.tileSurface.blit(self.grassBorderE, pygame.Rect((0, 0), (5, 100)))
                        if "N" in rlist:
                            self.tileSurface.blit(self.grassBorderN, pygame.Rect((0, 0), (5, 100)))
                        if "S" in rlist:
                            self.tileSurface.blit(self.grassBorderS, pygame.Rect((0, 0), (5, 100)))
                self.mapSurface.blit(self.tileSurface, pygame.Rect((x*100, y*100), (100, 100)))
        screen.blit(self.mapSurface, pygame.Rect((0, 0), (100 * len(self.level), 100 * len(self.level))))

    def checkrocks(self, x, y):
        ret = []
        if self.level[x][y-1] == 1 or self.level[x][y-1] == 2:
            ret.append("N")
        if self.level[x-1][y] == 1 or self.level[x-1][y] == 2:
            ret.append("W")
        if y < len(self.level[1])-1:
            if self.level[x][y+1] == 1 or self.level[x][y+1] == 2:
                ret.append("S")
        if x < len(self.level)-1:
            if self.level[x+1][y] == 1 or self.level[x+1][y] == 2:
                ret.append("E")
        elif ret == []:
            ret = False
        return ret

    def edit(self, type, x, y):
        try:
            self.level[x][y] = type
        except:
            print('could not edit block')

screen = pygame.display.set_mode([1600, 800])
levelmaker = levelmaker()
running = True
levelmaker.new_level(16, 8)
levelmaker.draw_map()
levelmaker.leveleditor = True
pathfinding.__init__(levelmaker.level)
pathnode = pygame.Surface((100, 100))
pygame.draw.circle(pathnode, (0, 0, 255), (50, 50), 25)
pathnode.set_colorkey((0, 0, 0))
pathstart = pygame.Surface((100, 100))
pygame.draw.circle(pathstart, (0, 255, 0), (50, 50), 50)
pathstart.set_colorkey((0, 0, 0))
pathend = pygame.Surface((100, 100))
pygame.draw.circle(pathend, (255, 0, 0), (50, 50), 50)
pathend.set_colorkey((0, 0, 0))
path = None

type = 1
scroll = 0
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 9:
                if levelmaker.leveleditor:
                    levelmaker.leveleditor = False
                else:
                    levelmaker.leveleditor = True
            elif not levelmaker.leveleditor:
                if event.key == 32:
                    path = pathfinding.start(levelmaker.level)
                    print(path)
            if event.key == 304:
                path = None

            print(event.key)
        m1, m2, m3 = pygame.mouse.get_pressed()
        mX, mY = pygame.mouse.get_pos()
        if levelmaker.leveleditor:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4 and scroll < 5:
                    scroll += 1
                elif event.button == 5 and scroll > -5:
                    scroll -= 1
                if scroll >= 0:
                    type = 2
                elif scroll < 0:
                    type = 1
            if m1:
                levelmaker.edit(type, int(str(mX/100)[:str(mX/100).index(".")]), int(str(mY/100)[:str(mY/100).index(".")]))
            elif m3:
                levelmaker.edit(0, int(str(mX/100)[:str(mX/100).index(".")]), int(str(mY/100)[:str(mY/100).index(".")]))
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if m1:
                    pathfinding.setStart(int(str(mX/100)[:str(mX/100).index(".")]), int(str(mY/100)[:str(mY/100).index(".")]))
                    print('start:', int(str(mX/100)[:str(mX/100).index(".")]), int(str(mY/100)[:str(mY/100).index(".")]))
                if m3:
                    pathfinding.setEnd(int(str(mX/100)[:str(mX/100).index(".")]), int(str(mY/100)[:str(mY/100).index(".")]))
                    print('end:', int(str(mX/100)[:str(mX/100).index(".")]), int(str(mY/100)[:str(mY/100).index(".")]))

        levelmaker.draw_map()
        if path is not None:
            x, y = path[0]
            x, y = x*100, y*100
            screen.blit(pathstart, pygame.Rect((x, y), (100, 100)))
            for point in path:
                x, y = point
                x, y = x*100, y*100
                screen.blit(pathnode, pygame.Rect((x, y), (100, 100)))
            x, y = path[len(path)-1]
            x, y = x*100, y*100
            screen.blit(pathend, pygame.Rect((x, y), (100, 100)))
        pygame.display.flip()