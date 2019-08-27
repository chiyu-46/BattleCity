"""
author:程鑫达
time:2019.8.10
version:1.0
说明：
    所有坦克的根类(含子弹的实现)
    坦克图层：50
    子弹图层：50
"""

from pygame.sprite import DirtySprite
import pygame

IMG = pygame.image.load(r'./resource/img/General-Sprites_1.png')


class Zidan(DirtySprite):
    def __init__(self, faction, level, rect=(), direction=()):
        DirtySprite.__init__(self)
        self.faction = faction
        self.level = level
        self.speed = 7
        self.cunhuo = True
        self.zidan_u = IMG.subsurface(pygame.Rect(969, 306, 12, 12))
        self.zidan_d = IMG.subsurface(pygame.Rect(1017, 306, 12, 12))
        self.zidan_l = IMG.subsurface(pygame.Rect(987, 306, 12, 12))
        self.zidan_r = IMG.subsurface(pygame.Rect(1038, 306, 12, 12))
        self.rect = pygame.Rect(rect[0], rect[1], 12, 12)
        self.layer = 50
        self.direction_x, self.direction_y = direction[0], direction[1]
        if self.direction_x == 0 and self.direction_y == -1:
            self.image = self.zidan_u
        elif self.direction_x == 0 and self.direction_y == 1:
            self.image = self.zidan_d
        elif self.direction_x == -1 and self.direction_y == 0:
            self.image = self.zidan_l
        elif self.direction_x == 1 and self.direction_y == 0:
            self.image = self.zidan_r

    def update(self):
        if self.rect.left == 3 or self.rect.top == 3 or self.rect.bottom == 621 \
                or self.rect.right == 621:
            self.cunhuo = False
        if self.cunhuo:
            self.rect.move_ip(self.speed * self.direction_x, self.speed * self.direction_y)


class Tank(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)
        self.level = 0
        self.speed = 0
        self.shengming = 0
        self.cunhuo = False
        self.can_move = False
        self.tabing = False
        self.img = IMG
        self.rect = pygame.Rect(10, 10, 48, 48)
        self._layer = 50
        self.direction_x, self.direction_y = 0, 1
        self.zidan = None
        self.tianzhuang = 10
        self.zidanlevel = 0
        self.zidanspeed = 0

    def shoot(self):
        pass

    def turn(self, direction):
        pass

    def move(self):
        pass
