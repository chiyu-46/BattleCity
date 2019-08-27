"""
author:程鑫达
time:2019.8.10
version:1.0
说明：
    用于生成道具
    time属性用于定时消失效果
    图层数：25
    如果敌方坦克携带道具，那么应调用生成器方法，随机决定携带的道具和道具位置
    拾取方法由main处理
"""

import pygame
import random
from pygame.sprite import DirtySprite

IMG = pygame.image.load(r'./resource/img/General-Sprites_1.bmp')


class Toukui(DirtySprite):
    def __init__(self, rect):
        DirtySprite.__init__(self)
        self.image = IMG.subsurface(pygame.Rect(768, 336, 48, 48))
        self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        self.layer = 25
        self.kind = 1
        self.cunhuo = False
        self.time = 200

    def update(self):
        self.time -= 1
        if self.time == 0:
            self.cunhuo = False


class Miaobiao(DirtySprite):
    def __init__(self, rect):
        DirtySprite.__init__(self)
        self.image = IMG.subsurface(pygame.Rect(816, 336, 48, 48))
        self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        self.layer = 25
        self.kind = 2
        self.cunhuo = False
        self.time = 200

    def update(self):
        self.time -= 1
        if self.time == 0:
            self.cunhuo = False


class Chanzi(DirtySprite):
    def __init__(self, rect):
        DirtySprite.__init__(self)
        self.image = IMG.subsurface(pygame.Rect(864, 336, 48, 48))
        self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        self.layer = 25
        self.kind = 3
        self.cunhuo = False
        self.time = 200

    def update(self):
        self.time -= 1
        if self.time == 0:
            self.cunhuo = False


class Xingxing(DirtySprite):
    def __init__(self, rect):
        DirtySprite.__init__(self)
        self.image = IMG.subsurface(pygame.Rect(912, 336, 48, 48))
        self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        self.layer = 25
        self.kind = 4
        self.cunhuo = False
        self.time = 200

    def update(self):
        self.time -= 1
        if self.time == 0:
            self.cunhuo = False


class Shoulei(DirtySprite):
    def __init__(self, rect):
        DirtySprite.__init__(self)
        self.image = IMG.subsurface(pygame.Rect(960, 336, 48, 48))
        self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        self.layer = 25
        self.kind = 5
        self.cunhuo = False
        self.time = 200

    def update(self):
        self.time -= 1
        if self.time == 0:
            self.cunhuo = False


class Tanke(DirtySprite):
    def __init__(self, rect):
        DirtySprite.__init__(self)
        self.image = IMG.subsurface(pygame.Rect(1008, 336, 48, 48))
        self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        self.layer = 25
        self.kind = 6
        self.cunhuo = False
        self.time = 200

    def update(self):
        self.time -= 1
        if self.time == 0:
            self.cunhuo = False


class Qiang(DirtySprite):
    def __init__(self, rect):
        DirtySprite.__init__(self)
        self.image = IMG.subsurface(pygame.Rect(1056, 336, 48, 48))
        self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        self.layer = 25
        self.kind = 7
        self.cunhuo = False
        self.time = 200

    def update(self):
        self.time -= 1
        if self.time == 0:
            self.cunhuo = False


class Shengchengqi:
    def __init__(self):
        self.kind = random.randint(1, 7)
        self.rect = (random.uniform(0, 576), random.uniform(0, 528))

    def run(self):
        if self.kind == 1:
            return Toukui(self.rect)
        elif self.kind == 2:
            return Miaobiao(self.rect)
        elif self.kind == 3:
            return Chanzi(self.rect)
        elif self.kind == 4:
            return Xingxing(self.rect)
        elif self.kind == 5:
            return Shoulei(self.rect)
        elif self.kind == 6:
            return Tanke(self.rect)
        elif self.kind == 7:
            return Qiang(self.rect)
