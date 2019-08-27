"""
坦克大战复刻版（受苦向）
author:程鑫达
time:2019.8.10
version:1.0(alpha)
说明：
    图层：60
    为避免占用内存过大，原始图像使用类常量
"""

from pygame.sprite import DirtySprite
import pygame

boom_img_1 = pygame.image.load(r'./resource/img/General-Sprites_1.png')
boom_img_2 = pygame.transform.scale(boom_img_1, (600, 384))


class Boom(DirtySprite):
    """初始化时传入子弹对象，用于决定爆炸位置"""
    def __init__(self, yuan):
        DirtySprite.__init__(self)
        self.boom_0 = boom_img_1.subsurface(pygame.Rect(768, 384, 48, 48))
        self.boom_1 = boom_img_1.subsurface(pygame.Rect(816, 384, 48, 48))
        self.boom_2 = boom_img_1.subsurface(pygame.Rect(864, 384, 48, 48))
        self.boom_3 = boom_img_2.subsurface(pygame.Rect(456, 192, 48, 48))
        self.boom_4 = boom_img_2.subsurface(pygame.Rect(504, 192, 48, 48))
        self.image = self.boom_0
        self.rect = pygame.Rect(0, 0, 48, 48)
        self.rect.centerx, self.rect.centery = yuan.rect.centerx, yuan.rect.centery
        self.layer = 60
        # 实现动态效果
        self.cunhuo = True
        self.time = 0

    def update(self, *args):
        """实现动态效果和自我消亡"""
        if self.time == 0:
            self.image = self.boom_0
        elif self.time == 1:
            self.image = self.boom_1
        elif self.time == 2:
            self.image = self.boom_2
        elif self.time == 3:
            self.image = self.boom_3
        elif self.time == 4:
            self.image = self.boom_4
        elif self.time == 5:
            self.image = self.boom_3
        elif self.time == 6:
            self.cunhuo = False
        self.time += 1

