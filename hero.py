class Hero():
    def __init__(self, pos, land):
        self.mode = True
        self.land = land
        self.hero = loader.loadModel('smiley')
        self.hero.setColor(1, 0.5, 0)
        self.hero.setScale(0.3)
        self.hero.setPos(pos)
        self.hero.reparentTo(render)
        self.cameraUp()
        self.accept_events()
        self.changeView()
        self.cameraBind()
    def cameraBind(self):
        base.disableMouse()
        base.camera.setH(180)
        base.camera.reparentTo(self.hero)
        base.camera.setPos(0,0,1.5)
        self.cameraOn = True
    def cameraUp(self):
        pos = self.hero.getPos()
        base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2] - 3)
        self.hero.reparentTo(render)
        base.enableMouse()
        self.cameraOn = False
    def accept_events(self):
        base.accept('c', self.changeView)
        base.accept('j', self.turn_left)
        base.accept('j'+'-repeat', self.turn_left)
        base.accept('l', self.turn_right)
        base.accept('l'+'-repeat', self.turn_right)
        base.accept('i', self.turn_up)
        base.accept('i'+'-repeat', self.turn_up)
        base.accept('k', self.turn_down)
        base.accept('k'+'-repeat', self.turn_down)
        base.accept('a', self.left)
        base.accept('a'+'-repeat', self.left)
        base.accept('d', self.right)
        base.accept('d'+'-repeat', self.right)
        base.accept('w', self.forward)
        base.accept('w'+'-repeat', self.forward)
        base.accept('s', self.back)
        base.accept('s'+'-repeat', self.back)

        base.accept('e', self.up)
        base.accept('e' + '-repeat', self.up)
        base.accept('q', self.down)
        base.accept('q' + '-repeat', self.down)

        base.accept('z', self.changeMode)
        base.accept('z'+'-repeat', self.changeMode)

        base.accept('b', self.build)
        base.accept('b'+'-repeat', self.build)
        base.accept('v', self.destroy)
        base.accept('v'+'-repeat', self.destroy)

        base.accept('f', self.land.saveMap)
        base.accept('g', self.land.loadMap)

    def changeView(self):
        if self.cameraOn:
            self.cameraUp()
        else:
            self.cameraBind()
    def turn_left(self):
        self.hero.setH((self.hero.getH() + 30) % 360)
    def turn_right(self):
        self.hero.setH((self.hero.getH() - 30) % 360)
    def turn_up(self):
        self.hero.setP((self.hero.getP() - 30) % 360)
    def turn_down(self):
        self.hero.setP((self.hero.getP() + 30) % 360)

    def just_move(self, angle):
        pos = self.look_at(angle)
        self.hero.setPos(pos)
    def try_move(self, angle):
        pos = self.look_at(angle)
        if self.land.isEmpty(pos):
            pos = self.land.findHighestEmpty(pos)
            self.hero.setPos(pos)
        else:
            pos = pos[0], pos[1], pos[2] + 1
            if self.land.isEmpty(pos):
                self.hero.setPos(pos)

    def move_to(self, angle):
        if self.mode:
            self.just_move(angle)
        else:
            self.try_move(angle)
    def look_at(self, angle):
        x_from = round(self.hero.getX())
        y_from = round(self.hero.getY())
        z_from = round(self.hero.getZ())
        dx, dy = self.check_dir(angle)
        x_to = x_from + dx
        y_to = y_from + dy
        return x_to, y_to, z_from
    def check_dir(self,angle):
        if 0 <= angle <= 20:
            return 0, -1
        elif 20 <= angle <= 65:
            return 1, -1
        elif 65 <= angle <= 110:
            return 1, 0
        elif 110 <= angle <= 155:
            return 1, 1
        elif 155 <= angle <= 200:
            return 0, 1
        elif 200 <= angle <= 245:
            return -1, 1
        elif 245 <= angle <= 290:
            return -1, 0
        elif 290 <= angle <= 335:
            return -1, -1
        elif 335 <= angle <= 359:
            return 0, -1
    def forward(self):
        angle = (self.hero.getH()+ 0) % 360
        self.move_to(angle)
    def left(self):
        angle = (self.hero.getH()+ 90) % 360
        self.move_to(angle)
    def back(self):
        angle = (self.hero.getH()+ 180) % 360
        self.move_to(angle)
    def right(self):
        angle = (self.hero.getH()+ 270) % 360
        self.move_to(angle)
    def up(self):
        if self.mode:
            self.hero.setZ(self.hero.getZ()+1)
    def down(self):
        if self.mode and self.hero.getZ()>1:
            self.hero.setZ(self.hero.getZ()-1)
    def changeMode(self):
        self.mode = not self.mode

    def build(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.addBlock(pos, (1,1,1,1))
        else:
            self.land.buildBlock(pos)
    def destroy(self):
        angle = self.hero.getH() % 360
        pos = self.look_at(angle)
        if self.mode:
            self.land.deBlock(pos)
        else:
            self.land.deBlockFrom(pos)