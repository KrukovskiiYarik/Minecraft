from hero import *
import pickle
class Mapmanager():
    def clear(self):
        self.land.removeNode()
        self.startNew()
    def __init__(self):
        self.model = 'block.egg'
        self.texture = 'block.png'
        self.startNew()
    def addBlock(self, pos, color):
        self.block  = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture))
        self.block.setPos(pos)
        self.block.setColor(color)
        self.block.reparentTo(self.land)
        self.block.setTag('at', str(pos))
    def startNew(self):
        self.land = render.attachNewNode('land')
    def loadLand(self, filename):
        with open(filename, 'r') as file:
            y = 0
            for string in file:
                x = 0
                string = string.split()
                for symbol in string:
                    for z in range(int(symbol)+1):
                        block = self.addBlock((y,x,z),(0.2,0.33*z, 0.2, 1))
                    x+=1
                y+=1
    def isEmpty(self,pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True
    def findBlocks(self,pos):
        return self.land.findAllMatches('=at='+str(pos))
    def findHighestEmpty(self,pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)
    def deBlock(self,pos):
        block = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()
    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z+1:
            self.addBlock(new, (1,1,0,1))
    def deBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos = x, y, z-1
        blocks = self.findBlocks(pos)
        for block in blocks:
            block.removeNode()
    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos,fout)
    def loadMap(self):
        self.clear()
        with open ('my_map.dat', 'rb') as fin:
            length = pickle.load(fin)
            for i in range(length):
                pos = pickle.load(fin)
                self.addBlock(pos, (0, 0.33, 0.66, 1))