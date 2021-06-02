from ursina import *


class LuckBlock(Entity):
    def __init__(self, ):
        super().__init__()

        self.model = 'quad'
        self.collider = 'box'
        self.scale = (1, 1)
        self.texture = 'assets\Blocks\lucky_block.jpg'
        self.Coin_Clock = 0
        self.Ori_y = -1#self.y


        self.Boppable = True
        self.Bopped = False
        self.Stop = False
        self.Down_Collider = Entity(model='quad', scale=(self.scale_x - 0.2, 0.06), collider='box', visible=True)





