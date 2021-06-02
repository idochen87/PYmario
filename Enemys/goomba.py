from ursina import *

class Goomba(Entity):
    def __init__(self, **kwargs):
        super().__init__()



        self.model = 'quad'
        self.collider = 'box'
        self.scale_x = 1.2

        self.left_right = False#false = left, true = right
        self.Squashed = False
        self.Squashed_clock=0
        self.textures = ['assets\goomba_s\\tile000.png','assets\goomba_s\\tile000.png','assets\goomba_s\\tile001.png','assets\goomba_s\\tile001.png']
        self.current_texture = 0
        self.Squashed_colloder = Entity(model='cube', scale=(self.scale_x - 0.7, 0.06), collider='box', visible=False)
        self.Static_Y = self.y
        self.Hit_Info = self.intersects(ignore=[self,self.Squashed_colloder])

    def update(self):

        self.Squashed_colloder.position = self.position + Vec3(0,0.5,0)

        hitted_collider = self.Squashed_colloder.intersects(ignore=[self])

        if hitted_collider.hit:
            self.Squashed = True

        if self.Squashed == False:
            self.Static_Y = self.y
            self.current_texture += 1 * time.dt * 6
            self.walking()
            if self.current_texture >= 4:
                self.current_texture = 0
            self.texture = self.textures[int(self.current_texture)]

        if self.Squashed == True:
            self.Squashed_clock += 1 * time.dt
            self.scale_y = 0.5
            self.y = self.Static_Y - 0.23
            self.Squashed_colloder.disable()
            if self.Squashed_clock >= 0.2:
                self.Squashed = False
                self.disable()

    def walking(self):
        if self.left_right:
            self.x += 1 * time.dt
        if self.left_right == False:
            self.x -= 1 * time.dt


        if self.x >= self.origin.x + 3 or self.Hit_Info.hit:
            self.left_right = False
        if self.x <= self.origin.x - 3 or self.Hit_Info.hit:
            self.left_right = True