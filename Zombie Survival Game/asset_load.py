import pygame
import os

HEIGHT = 720
WIDTH = 1200

BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "bg.png")), (WIDTH, HEIGHT))
PLAYER_HIT_OVERLAY = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "player_hit_overlay.png")), (WIDTH, HEIGHT))

PLAYER_LEFT = pygame.image.load(
    os.path.join('assets\\player\\player_left.png'))
PLAYER_RIGHT = pygame.image.load(
    os.path.join('assets\\player\\player_right.png'))
PLAYER_UP = pygame.image.load(os.path.join('assets\\player\\player_up.png'))
PLAYER_DOWN = pygame.image.load(
    os.path.join('assets\\player\\player_down.png'))
PLAYER_RUN_LEFT_1 = pygame.image.load(
    'assets\\player\\player_run_left_1.png')
PLAYER_RUN_LEFT_2 = pygame.image.load(
    'assets\\player\\player_run_left_2.png')
PLAYER_RUN_RIGHT_1 = pygame.image.load(
    'assets\\player\\player_run_right_1.png')
PLAYER_RUN_RIGHT_2 = pygame.image.load(
    'assets\\player\\player_run_right_2.png')
PLAYER_RUN_DOWN_1 = pygame.image.load(
    'assets\\player\\player_run_down_1.png')
PLAYER_RUN_DOWN_2 = pygame.image.load(
    'assets\\player\\player_run_down_2.png')
PLAYER_RUN_UP_1 = pygame.image.load(
    'assets\\player\\player_run_up_1.png')
PLAYER_RUN_UP_2 = pygame.image.load(
    'assets\\player\\player_run_up_2.png')
ZOMBIE = pygame.image.load(os.path.join("assets", 'zombie.png'))
ZOMBIE_HURT = pygame.image.load(os.path.join("assets", 'zombie_hurt.png'))
ZOMBIE_DEAD = pygame.image.load(os.path.join("assets", 'zombie_dead.png'))
AMMO = pygame.image.load(os.path.join('assets', 'ammo.png'))
BULLET = pygame.image.load(os.path.join('assets', 'bullet.png'))
PLAYER_DEAD = pygame.image.load(os.path.join('assets', 'player_dead.png'))
