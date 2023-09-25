# напиши здесь код основного окна игры
from direct.showbase.ShowBase import ShowBase
from mapmanager import *
from hero import *
class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager()
        self.hero = Hero((0,0,0), self.land)
game = Game()
game.camLens.setFov(120)
game.land.loadLand('land.txt')
game.run()
