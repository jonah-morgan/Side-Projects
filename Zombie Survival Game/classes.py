import pygame
import math
from asset_load import *

class Projectile:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, vel):
        if self.direction == 'up':
            self.y -= vel
        elif self.direction == 'down':
            self.y += vel
        elif self.direction == 'left':
            self.x -= vel
        elif self.direction == 'right':
            self.x += vel
        elif self.direction == 'up_right':
            self.x += vel // 2
            self.y -= vel // 2
        elif self.direction == 'up_left':
            self.x -= vel // 2
            self.y -= vel // 2
        elif self.direction == 'down_right':
            self.x += vel // 2
            self.y += vel // 2
        elif self.direction == 'down_left':
            self.x -= vel // 2
            self.y += vel // 2

    def draw(self, window):
        # Parent draw function, blits the img at x and y
        window.blit(self.ent_img, (self.x, self.y))


class Bullet(Projectile):
    def __init__(self, x, y, direction=''):
        super().__init__(x, y)
        self.ent_img = BULLET
        self.mask = pygame.mask.from_surface(self.ent_img)
        self.direction = direction

    def draw(self, window):
        # Parent draw function, blits the img at x and y
        super().draw(window)


class Entity:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ent_imgs = []
        self.ent_img = None
        self.animation_tick = 0

    def draw(self, window):
        # Parent draw function, blits the img at x and y
        window.blit(self.ent_img, (self.x, self.y))

    def update(self):
        pass

    def get_height(self):
        return self.ent_img.get_height()

    def get_width(self):
        return self.ent_img.get_width()

    def get_distance(self, obj):
        return math.sqrt(((abs(self.x - obj.x))**2) + ((abs(self.y - obj.y))**2))

    def animate(self, imglist):
        if self.counter == 15:
            self.counter = 0
        self.counter += 1
        if self.counter > 5:
            self.current_img = imglist[0]
        if self.counter > 10:
            self.current_img = imglist[1]

    def update(self):
        if self.is_moving and (self.direction == 'left' or self.direction == 'up_left'):
            self.animate(self.left_run_imgs)
        elif self.is_moving and (self.direction == 'right' or self.direction == 'down_right'):
            self.animate(self.right_run_imgs)
        elif self.is_moving and (self.direction == 'up' or self.direction == 'up_right'):
            self.animate(self.up_run_imgs)
        elif self.is_moving and (self.direction == 'down' or self.direction == 'down_left'):
            self.animate(self.down_run_imgs)
        else:
            if self.direction == 'left' or self.direction == 'up_left':
                self.current_img = PLAYER_LEFT
            elif self.direction == 'right' or self.direction == 'down_right':
                self.current_img = PLAYER_RIGHT
            elif self.direction == 'up' or self.direction == 'up_right':
                self.current_img = PLAYER_UP
            elif self.direction == 'down' or self.direction == 'down_left':
                self.current_img = PLAYER_DOWN
            self.counter = 0


class Player(Entity):
    def __init__(self, x, y, health=100, animation_tick=0):
        super().__init__(x, y, health)
        self.animation_tick = 0
        self.counter = 0
        # Masks are good with pixel perfect detection, used for images.
        self.ammo = 10
        self.max_ammo = 10
        self.max_health = 100
        self.direction = ''
        self.is_moving = False
        self.current_img = PLAYER_LEFT
        self.mask = pygame.mask.from_surface(self.current_img)
        self.left_run_imgs = [PLAYER_RUN_LEFT_1, PLAYER_RUN_LEFT_2]
        self.right_run_imgs = [PLAYER_RUN_RIGHT_1, PLAYER_RUN_RIGHT_2]
        self.down_run_imgs = [PLAYER_RUN_DOWN_1, PLAYER_RUN_DOWN_2]
        self.up_run_imgs = [PLAYER_RUN_UP_1, PLAYER_RUN_UP_2]

    def draw(self, window):
        self.mask = pygame.mask.from_surface(self.current_img)
        window.blit(self.current_img, (self.x, self.y))

    def get_height(self):
        return self.current_img.get_height()

    def get_width(self):
        return self.current_img.get_width()


class Zombie(Player):
    def __init__(self, x, y, health=100, current_img=ZOMBIE):
        super().__init__(x, y, health, current_img)
        self.current_img = ZOMBIE
        self.walk_count = 0
        self.randy = 0
        self.randd = 0
        self.is_moving = True
        # Masks are good with pixel perfect detection, used for images.

    def draw(self, window):
        super().draw(window)

    def move(self, axis, dist):
        if axis == 3:
            self.y += dist + 1 // 2
            self.x += dist + 1 // 2
        elif axis == 2:
            self.y -= dist + 1 // 2
            self.x += dist + 1 // 2
        elif axis == 1:
            self.y += dist + 1 // 2
        else:
            self.x += dist + 1 // 2

    def attack_move(self, vel, obj):
        dist = get_distance(self, obj)
        pos_x_dist = test_posx_distance(self, obj)
        neg_x_dist = test_negx_distance(self, obj)
        pos_y_dist = test_posy_distance(self, obj)
        neg_y_dist = test_negy_distance(self, obj)

        if pos_x_dist < dist and neg_y_dist < dist:
            self.x += vel
            self.y -= vel
            self.direction = 'up_right'
        elif pos_x_dist < dist and pos_y_dist < dist:
            self.x += vel
            self.y += vel
            self.direction = 'down_right'
        elif neg_x_dist < dist and neg_y_dist < dist:
            self.x -= vel
            self.y -= vel
            self.direction = 'up_left'
        elif neg_x_dist < dist and pos_y_dist < dist:
            self.x -= vel
            self.y += vel
            self.direction = 'down_left'
        elif pos_x_dist < dist:
            self.x += vel
            self.direction = 'right'
        elif neg_x_dist < dist:
            self.x -= vel
            self.direction = 'left'
        elif pos_y_dist < dist:
            self.y += vel
            self.direction = 'down'
        elif neg_y_dist < dist:
            self.y -= vel
            self.direction = 'up'


class Ammo(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.ent_img = AMMO
        self.mask = pygame.mask.from_surface(self.ent_img)

    def draw(self, window):
        super().draw(window)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    if obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None:
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y))


def get_distance(obj1, obj2):
    return math.sqrt(((abs(obj2.x - obj1.x))**2) + ((abs(obj2.y - obj1.y))**2))


def get_distance_cords(x1, y1, x2, y2):
    return math.sqrt(((abs(x2 - x1))**2) + ((abs(y2 - y1))**2))


def test_posx_distance(obj1, obj2):
    return math.sqrt((abs(obj2.x - (obj1.x + 1))**2) + ((abs(obj2.y - obj1.y))**2))


def test_negx_distance(obj1, obj2):
    return math.sqrt((abs(obj2.x - (obj1.x - 1))**2) + ((abs(obj2.y - obj1.y))**2))


def test_posy_distance(obj1, obj2):
    return math.sqrt((abs(obj2.x - obj1.x)**2) + ((abs(obj2.y - (obj1.y + 1)))**2))


def test_negy_distance(obj1, obj2):
    return math.sqrt((abs(obj2.x - obj1.x)**2) + ((abs(obj2.y - (obj1.y - 1)))**2))
