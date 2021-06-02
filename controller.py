from ursina import *



class PlatformerController2d(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.model = 'quad'
        self.origin_y = -.5
        self.y = 2
        self.scale_y = 2
        self.collider = 'box'


        self.enemy_collider = Entity(model = 'cube',scale = (self.scale_x - 0.2,0.06),collider = 'box',visible = False)
        self.cleling_collider = Entity(model='cube', scale=(self.scale_x - 0.2, 0.06), collider='box', visible=False)
        self.idle_state = 'r'
        self.jump_state = 'r'
        self.moving_state = 'idle' #idle_R,idle_L,run_left,run_right

        self.animator = Animator({'idle' : None, 'walk' : None, 'jump' : None})
        # self.animation_state_machine.state = 'jump'
        # self.idle_animation = None
        # self.walk_animation = None
        # self.jump_animation = None
        # self.idle_animation = Entity(parent=self, model='cube', color=color.gray, origin_y=-.5, scale_z=2)
        # self.walk_animation = Animation(parent=self, texture='ursina_wink', color=color.red, origin_y=-.5, scale=(2,2), double_sided=True)
        # self.model = None

        self.decelarte_right = False
        self.decelarte_left = False
        self.fall = False

        self.walkvel = 0
        self.jump_force = 400
        self.jump_vel = 0
        self.fall_vel = 0
        self.walk_speed = 3
        self.walking = False
        self.velocity = 0 # the walk diection is stored here. -1 for left and 1 for right.
        self.jump_height = 4
        self.jump_duration = 0.1
        self.jumping = False
        self.max_jumps = 1
        self.jumps_left = self.max_jumps
        self.gravity = 0.4
        self.grounded = True
        self.air_time = 0   # this increase while we're falling and used when calculating the distance we fall so we fall faster and faster instead of linearly.
        self.traverse_target = scene     # by default, it wil collide with everything except itself. you can chage this to change the boxcast traverse target.
        self._start_fall_sequence = None # we need to store this so we can interrupt the fall call if we try to double jump.


        self.ray = boxcast(self.world_position, self.down, distance=10, ignore=(self,self.enemy_collider,self.cleling_collider ), traverse_target=self.traverse_target, thickness=.9)
        if self.ray.hit:
            self.y = self.ray.world_point[1] + .01
        # camera.add_script(SmoothFollow(target=self, offset=[0,1,-30], speed=4))

        for key, value in kwargs.items():
            setattr(self, key, value)

        # delay_gravity one frame
        target_gravity = self.gravity
        self.gravity = 0
        invoke(setattr, self, 'gravity', target_gravity, delay=1/60)
        self._original_scale_x = self.scale_x



    def update(self):
        self.enemy_collider.x = self.x
        self.enemy_collider.y = self.y


        self.cleling_collider.x = self.x
        self.cleling_collider.y = self.y + 1.8


        if self.grounded == True:
            self.fall = False
            self.jump_vel = 0

        if self.decelarte_right == True:
            self.velocity -= 2 * time.dt
            if self.velocity <= 0.1:
                self.velocity = 0
                self.decelarte_right = False
        if self.decelarte_left == True:
            self.velocity += 2 * time.dt
            if self.velocity >= -0.1:
                self.velocity = 0
                self.decelarte_left = False

        if self.velocity > 0:
            if self.grounded:
                self.jump_state = 'r'
            self.moving_state = 'run_right'
            if not held_keys['x']:
                self.velocity += 1 * time.dt
                if self.velocity >= 1:
                    self.velocity = 1
            if held_keys['x']:
                self.velocity += 1.5 * time.dt
                if self.velocity >= 2:
                    self.velocity = 2

        if self.velocity < 0:
            if self.grounded:
                self.jump_state = 'l'
            self.moving_state = 'run_left'
            if not held_keys['x']:
                self.velocity -= 1 * time.dt
                if self.velocity <= -1:
                    self.velocity = -1
            if held_keys['x']:
                self.velocity -= 1.5 * time.dt
                if self.velocity <= -2:
                    self.velocity = -2

        if self.velocity == 0:
            if self.idle_state == 'r':
                self.moving_state = 'idle_right'
            if self.idle_state == 'l':
                self.moving_state = 'idle_left'

        # check in the direction we're walking to see if there's a wall. If it does not hit, move.
        if self.fall == False:
            self.y += self.jump_vel * time.dt
        if boxcast(
            self.position+Vec3(self.velocity * time.dt * self.walk_speed,self.scale_y/2,0),
            # self.position+Vec3(sefl,self.scale_y/2,0),
            direction=Vec3(self.velocity,0,0),
            distance=abs(self.scale_x/2),
            ignore=(self, self.enemy_collider,self.cleling_collider),
            traverse_target=self.traverse_target,
            thickness=(self.scale_x*.9, self.scale_y*.9),
            ).hit == False:

            self.x += self.velocity * time.dt * self.walk_speed
        else:
            if self.velocity < 0:
                self.velocity = -0.1
            if self.velocity > 0:
                self.velocity = 0.1

        self.walking = held_keys['left arrow'] + held_keys['right arrow'] > 0 and self.grounded

        # animations
        if not self.grounded:
            self.animator.state = 'jump'
            self.moving_state = 'jump'
        else:
            if self.walking:
                self.animator.state = 'walk'
            else:
                self.animator.state = 'idle'


        #check if we're on the ground or not.
        #rays = self.Down.intersects(ignore = [self])
        ray = boxcast(
            self.world_position+Vec3(0,.1,0),
            self.down,
            distance=max(.1, self.air_time * self.gravity),
            debug = False,
            ignore=(self, self.enemy_collider,self.cleling_collider),
            traverse_target=self.traverse_target,
            thickness= 1  #2#self.boxcast_scale#8.5#self.scale_x * 4.25
            )

        if ray.hit:
            #if rays.entity == ground:
                if not self.grounded:
                    self.land()
                self.grounded = True
                self.y = ray.world_point[1
                ]
                return
        else:
            self.grounded = False

        # if not on ground and not on way up in jump, fall
        if not self.grounded and not self.jumping:
            self.fall_vel += 20 * time.dt
            self.y -= self.fall_vel * time.dt
            #self.y -= min(self.fall_vel, ray.distance-.1)
            #self.y -= min(self.air_time * self.gravity, ray.distance - .1)
           #self.air_time += time.dt*4 * self.gravity



        # if in jump and hit the ceiling, fall
        celling = self.cleling_collider.intersects(ignore=[self,self.enemy_collider])
        if celling.hit:
            self.jump_vel = 0
            self.fall_vel = 1
            self.fall = True
                #self.y_



    def input(self, key):
        if key == 'space':
            self.jump()


        if key == 'right arrow':
            self.decelarte_left = False
            self.idle_state = 'r'
            self.velocity = 0.1
            self.decelarte_right = False
        if key == 'right arrow up':
            self.decelarte_right = True
            #self.velocity = 0

        if key == 'left arrow':
            self.decelarte_right = False
            self.idle_state = 'l'
            if not self.decelarte_right == True:
                self.velocity = -0.1
                self.decelarte_left = False
        if key == 'left arrow up':
            #self.velocity = 0
            self.decelarte_left = True



    def jump(self):
        if not self.grounded and self.jumps_left <= 1:
            return

        if self._start_fall_sequence:
            self._start_fall_sequence.kill()

        # don't jump if there's a ceiling right above us
        if boxcast(self.position+(0,.1,0), self.up, distance=self.scale_y, thickness=.95, ignore=(self,self.enemy_collider,self.cleling_collider), traverse_target=self.traverse_target).hit:
            return

        if hasattr(self, 'y_animator'):
            self.y_animator.kill()

        self.jumping = True
        self.jumps_left -= 1
        self.grounded = False

        target_y = self.y + self.jump_height
        duration = self.jump_duration


        # check if we hit a ceiling and adjust the jump height accordingly
        hit_above = boxcast(self.position+(0,0.1,0), self.up, distance=self.scale_y, thickness=11, ignore=(self,self.enemy_collider,self.cleling_collider),debug = True)
        if hit_above.hit:
            #target_y = min(hit_above.world_point.y-self.scale_y, target_y)
            # print('------', target_y)
            try:
                self.jumping = False
            except ZeroDivisionError as e:
                return e

        #self.animate_y(target_y, duration, resolution=30, curve=curve.out_expo)
        self.jump_vel += self.jump_force * time.dt
        self._start_fall_sequence = invoke(self.start_fall, delay=duration)


    def start_fall(self):
        #self.y_animator.pause()
        self.jumping = False


    def land(self):
        # print('land')
        #self.jump_vel = 0
        self.fall_vel = 0
        self.fall = False
        self.air_time = 0
        self.jumps_left = self.max_jumps
        self.jumping = False
        self.grounded = True



if __name__ == '__main__':
    # window.vsync = False
    app = Ursina()
    EditorCamera()
    camera.orthographic = True
    camera.fov = 10

    ground = Entity(model='cube', color=color.white33, origin_y=.5, scale=(1, 1 , 1), collider='box')
    ground_dowd = Entity(model='cube', color=color.white33, origin_y=.5, scale=(1, 1 , 1), collider='box',y=-1)
    ground1 = Entity(model='cube', color=color.white33, origin_y=.5, scale=(1, 1, 1), collider='box',x = ground.x + ground.scale_x)
    ground2 = Entity(model='cube', color=color.white33, origin_y=.5, scale=(1, 1, 1), collider='box',x = ground1.x + ground.scale_x)
    ground3 = Entity(model='cube', color=color.white33, origin_y=.5, scale=(1, 1, 1), collider='box',x = ground2.x + ground.scale_x)
    ground.collider.visible = True
    wall = Entity(model='cube', color=color.azure, origin=(-.5,.5), scale=(5,10), x=10, y=.5, collider='box')
    wall_2 = Entity(model='cube', color=color.white33, origin=(-.5,.5), scale=(5,10), x=10, y=5, collider='box')
    #ceiling = Entity(model='cube', color=color.white33, origin_y=-.5, scale=(6, 1, 1), y=1, collider='box')

    def input(key):
        if key == 'c':
            wall.collision = not wall.collision
            print(wall.collision)


    player_controller = PlatformerController2d(y = 4)
    camera.add_script(SmoothFollow(target=player_controller, offset=[0,1,-30], speed=4))

    app.run()