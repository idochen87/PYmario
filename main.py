from ursina import *
from controller import PlatformerController2d
from Enemys import goomba
from Blocks import Blocks

#tiles
ground = 'assets/D.png'
Bricks = 'assets/Blocks/Bricks.png'


game_map = [[0,0,0,0,0,0,0,0,0,0,0,0,0,70,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,70,0,0,0,75,70,75,70,75,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,],
            [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,],
            [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,],
            [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,],
            [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]]



app = Ursina()

y = 4
for row in game_map:
    x = 0
    for tile in row:
        if tile == 0:
            pass

        if tile == 3:
            Entity(model='quad', x=x, y=y, scale=(1, 1, 1), collider='box', texture=ground)

        if tile == 75:
            Entity(model='quad', x=x, y=y, scale=(1, 1, 1), collider='box', texture=Bricks)

        if tile == 70:
            Blocks.LuckBlock().position = (x,y)

        if tile == 4:
            nigga = goomba.Goomba()
            nigga.position = (x,y)
        x += 1
    y -= 1



def update():
    global cuurent_texture

    if mario.moving_state == 'idle_left':
        mario.texture = 'assets/mario_Move/Left/tile000.png'
    if mario.moving_state == 'idle_right':
        mario.texture = 'assets/mario_Move/Right/tile000.png'
        cuurent_texture = 0

    if mario.moving_state == 'jump':
       if mario.jump_state == 'r':
           mario.texture = 'assets/mario_Move/Right/tile006.png'
       if mario.jump_state == 'l':
           mario.texture = 'assets/mario_Move/Left/tile006.png'

    if mario.moving_state == 'run_right':
        mario.texture = mario_right_textures[int(cuurent_texture)]
        if cuurent_texture >= 3:
            cuurent_texture = 0
        cuurent_texture += 1 * time.dt * 5

    if mario.moving_state == 'run_left':
        mario.texture = mario_left_textures[int(cuurent_texture)]
        if cuurent_texture >= len(mario_left_textures) - 1:
            cuurent_texture = 0
        cuurent_texture += 1 * time.dt * 5







mario = PlatformerController2d(y=5, scale=(1.5, 2))
camera.fov = 60
mario.jump_force = 650
cuurent_texture = 0





mario_right_textures = ['assets/mario_Move/Right/tile001.png',
                        'assets/mario_Move/Right/tile002.png',
                        'assets/mario_Move/Right/tile003.png',
                        'assets/mario_Move/Right/tile003.png']
mario_left_textures =   ['assets/mario_Move/Left/tile001.png',
                         'assets/mario_Move/Left/tile002.png',
                         'assets/mario_Move/Left/tile003.png',
                         'assets/mario_Move/Left/tile003.png']

camera.add_script(SmoothFollow(target=mario, offset=[0, 4, -30], speed=3))
camera.fov = 40







background = Entity(model='quad',z = 0.1, scale=(100, 100), texture = 'assets\mario world.png')


app.run()


