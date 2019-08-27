# -*- coding:utf-8 -*-
"""
author:程鑫达
time:2019.8.10
version:1.0
说明：
    用于生成地图
    图层：1
        草（树）99
    为避免占用内存过大，原始图像使用类常量
"""

from pygame.sprite import DirtySprite
from module import main
import pygame, os, json, random

IMG = pygame.image.load(r'./resource/img/General-Sprites_1.bmp')


class Shiqiang(DirtySprite):
    """type属性对应墙的形状"""
    def __init__(self, type, rect):
        DirtySprite.__init__(self)
        self.shiqiang_0 = IMG.subsurface(pygame.Rect(768, 0, 48, 48))  # 全
        self.shiqiang_1 = IMG.subsurface(pygame.Rect(840, 0, 24, 48))  # 右
        self.shiqiang_2 = IMG.subsurface(pygame.Rect(864, 24, 48, 24))  # 下
        self.shiqiang_3 = IMG.subsurface(pygame.Rect(912, 0, 24, 48))  # 左
        self.shiqiang_4 = IMG.subsurface(pygame.Rect(960, 0, 48, 24))  # 上
        self.shiqiang_5 = IMG.subsurface(pygame.Rect(768, 192, 24, 24))  # 小
        self.image = self.shiqiang_5
        self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        # 根据种类确定墙位置和形状
        if type == 1:  # 右下
            self.image = self.shiqiang_5
            self.rect = pygame.Rect(rect[0] + 24, rect[1] + 24, 24, 24)
        elif type == 2:  # 左下
            self.image = self.shiqiang_5
            self.rect = pygame.Rect(rect[0], rect[1] + 24, 24, 24)
        elif type == 3:  # 完整
            self.image = self.shiqiang_0
            self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        elif type == 4:  # 上
            self.image = self.shiqiang_4
            self.rect = pygame.Rect(rect[0], rect[1], 48, 24)
        elif type == 5:  # 下
            self.image = self.shiqiang_2
            self.rect = pygame.Rect(rect[0], rect[1] + 24, 48, 24)
        elif type == 6:  # 右
            self.image = self.shiqiang_1
            self.rect = pygame.Rect(rect[0] +24, rect[1], 24, 48)
        elif type == 7:  # 左
            self.image = self.shiqiang_3
            self.rect = pygame.Rect(rect[0], rect[1], 24, 48)
        self.layer = 1
        self.cunhuo = True
        self.shengming = 2

    def update(self):
        pass


class Tieqiang(DirtySprite):
    """type属性对应墙的形状"""
    def __init__(self, type, rect):
        DirtySprite.__init__(self)
        self.tie_0 = IMG.subsurface(pygame.Rect(768, 48, 48, 48))  # 全
        self.tie_1 = IMG.subsurface(pygame.Rect(840, 48, 24, 48))  # 右
        self.tie_2 = IMG.subsurface(pygame.Rect(864, 72, 48, 24))  # 下
        self.tie_3 = IMG.subsurface(pygame.Rect(912, 48, 24, 48))  # 左
        self.tie_4 = IMG.subsurface(pygame.Rect(960, 48, 48, 24))  # 上
        self.tie_5 = IMG.subsurface(pygame.Rect(768, 216, 24, 24))  # 小
        self.image = self.tie_0
        self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        # 根据种类确定墙位置和形状
        if type == 3:  # 完整
            self.image = self.tie_0
            self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        elif type == 4:  # 上
            self.image = self.tie_4
            self.rect = pygame.Rect(rect[0], rect[1], 48, 24)
        elif type == 5:  # 下
            self.image = self.tie_2
            self.rect = pygame.Rect(rect[0], rect[1] + 24, 48, 24)
        elif type == 6:  # 右
            self.image = self.tie_1
            self.rect = pygame.Rect(rect[0] + 24, rect[1], 24, 48)
        elif type == 7:   # 左
            self.image = self.tie_3
            self.rect = pygame.Rect(rect[0], rect[1], 24, 48)
        self.layer = 1
        self.cunhuo = True
        self.shengming = 2

    def update(self):
        pass


class Caodi(DirtySprite):
    def __init__(self, rect):
        DirtySprite.__init__(self)
        self.image = IMG.subsurface(pygame.Rect(816, 96, 48, 48))
        self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        self.layer = 99
        self.cunhuo = True


class Bing(DirtySprite):
    def __init__(self, rect):
        DirtySprite.__init__(self)
        self.image = IMG.subsurface(pygame.Rect(864, 96, 48, 48))
        self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        self._layer = 100
        self.cunhuo = True


class Heliu(DirtySprite):
    """河流具有动态效果"""

    def __init__(self, rect):
        DirtySprite.__init__(self)
        self.he_0 = IMG.subsurface(pygame.Rect(768, 96, 48, 48))
        self.he_1 = IMG.subsurface(pygame.Rect(768, 144, 48, 48))
        self.he_2 = IMG.subsurface(pygame.Rect(816, 144, 48, 48))
        # 用于实现动态效果
        self.he_xiaoguo = [self.he_0, self.he_1, self.he_2]
        self.image = self.he_0
        self.time = (int(random.random() * 3) + 2)
        self.rect = pygame.Rect(rect[0], rect[1], 48, 48)
        self.layer = 1
        self.cunhuo = True

    def update(self):
        if self.time == 5:
            self.image = self.he_0
        elif self.time == 3:
            self.image = self.he_1
        elif self.time == 1:
            self.image = self.he_2
            self.time = 6
        self.time -= 1


class Dabenying(DirtySprite):
    def __init__(self):
        DirtySprite.__init__(self)
        self.image = IMG.subsurface(pygame.Rect(912, 96, 48, 48))
        self.rect = pygame.Rect(288, 576, 48, 48)
        self.layer = 1
        self.cunhuo = True
        self.shengming = 1

    def update(self):
        if not self.cunhuo:
            self.image = IMG.subsurface(pygame.Rect(960, 96, 48, 48))


class Map:
    def __init__(self, no):
        self.shiqiang_group = pygame.sprite.LayeredUpdates()
        self.tie_group = pygame.sprite.LayeredUpdates()
        self.bing_group = pygame.sprite.LayeredUpdates()
        self.he_group = pygame.sprite.LayeredUpdates()
        self.cao_group = pygame.sprite.LayeredUpdates()
        self.ying = pygame.sprite.LayeredUpdates()
        self.ying.add(Dabenying())
        self.data = {}
        self.stage = no
        self.file = r'./resource/map/stage-{}.json'.format(self.stage)

    def read(self):
        """读取地图文件"""

        assert os.path.exists(self.file), '未找到地图文件'
        with open(self.file, 'r') as f:
            self.data = json.load(f)

    def make(self):
        """
        地图文件映射表
        X空地     F草    S冰    R河    B石墙    T铁墙    f完整    3上    c下    a右    5左    E鹰    8右下    4左下
        """
        info = self.data["map"]
        for x, b in zip(info, range(len(info))):
            for y, a in zip(x.split(), range(len(x.split()))):
                if y == 'X':
                    pass
                elif y == 'F':
                    self.cao_group.add(Caodi((a*48, b*48)))
                elif y == 'S':
                    self.bing_group.add(Bing((a*48, b*48)), layer=0)
                elif y == 'R':
                    self.he_group.add(Heliu((a*48, b*48)))
                elif y == 'B8':
                    self.shiqiang_group.add(Shiqiang(1, (a * 48, b * 48)))
                elif y == 'B4':
                    self.shiqiang_group.add(Shiqiang(2, (a * 48, b * 48)))
                elif y == 'Bf':
                    self.shiqiang_group.add(Shiqiang(3, (a * 48, b * 48)))
                elif y == 'Tf':
                    self.tie_group.add(Tieqiang(3, (a * 48, b * 48)))
                elif y == 'B3':
                    self.shiqiang_group.add(Shiqiang(4, (a * 48, b * 48)))
                elif y == 'T3':
                    self.tie_group.add(Tieqiang(4, (a * 48, b * 48)))
                elif y == 'Bc':
                    self.shiqiang_group.add(Shiqiang(5, (a * 48, b * 48)))
                elif y == 'Tc':
                    self.tie_group.add(Tieqiang(5, (a * 48, b * 48)))
                elif y == 'Ba':
                    self.shiqiang_group.add(Shiqiang(6, (a * 48, b * 48)))
                elif y == 'Ta':
                    self.tie_group.add(Tieqiang(6, (a * 48, b * 48)))
                elif y == 'B5':
                    self.shiqiang_group.add(Shiqiang(7, (a * 48, b * 48)))
                elif y == 'T5':
                    self.tie_group.add(Tieqiang(7, (a * 48, b * 48)))
                elif y == 'E':
                    pass

    def get_difficulty(self):
        """返回此图难度"""
        self.read()
        return self.data["difficulty"]

    def get_enemy(self):
        """返回此图敌人配置"""
        self.read()
        return self.data['bots']

    def get_map(self):
        """返回地图"""
        self.read()
        self.make()
        return self.shiqiang_group, self.tie_group, self.bing_group, self.he_group, self.cao_group, self.ying
