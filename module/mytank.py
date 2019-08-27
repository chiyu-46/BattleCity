"""
author:程鑫达
time:2019.8.10
version:1.0
说明：
    我方坦克
    护盾时间：250
    图层：50（属性在父类）
    一级
        速度3    填装10   子弹等级1   子弹速度5
    二级
        速度2    填装10   子弹等级1   子弹速度5
    三级
        速度2    填装5    子弹等级1   子弹速度5
    四级
        速度1    填装5    子弹等级2   子弹速度4
    坦克移送由turn和move共同处理，玩家键盘控制turn，改备方向参数和加载对应等级的方向图片，
    move再可移动属性为真时按turn方向移动
"""

from module import tank
import pygame


class Mytank(tank.Tank):
    def __init__(self, player):
        tank.Tank.__init__(self)
        # 不同玩家的出生位置不同
        self.player = player
        if player == 1:
            self.left, self.top = 192, 576
            # 初始坦克（一级）
            self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 0, 48, 48))
            self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 0, 48, 48))
            self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 0, 48, 48))
            self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 0, 48, 48))
            self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 0, 48, 48))
            self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 0, 48, 48))
            self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 0, 48, 48))
            self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 0, 48, 48))
            # 坦克图片组（按方向）为了轮子特效
            self.tank_img = [self.tank_u_0, self.tank_u_1]
        elif player == 2:
            self.left, self.top = 384, 576
            # 初始坦克（一级）
            self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 384, 48, 48))
            self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 384, 48, 48))
            self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 384, 48, 48))
            self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 384, 48, 48))
            self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 384, 48, 48))
            self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 384, 48, 48))
            self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 384, 48, 48))
            self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 384, 48, 48))
            # 坦克图片组（按方向）为了轮子特效
            self.tank_img = [self.tank_u_0, self.tank_u_1]
        else:
            raise ValueError('不存在的己方坦克')
        # 坦克等级，速度，能否移动
        self.level = 1
        self.speed = 3
        self.can_move = False
        # 生命值
        self.shengming = 1
        # 子弹相关
        self.tianzhuang = 60
        self.zidanlevel = 1
        # 护盾
        self.hudun = True
        self.huduntime = 250
        # 初始位置和方向
        self.image = self.tank_img[1]
        self.rect = pygame.Rect(self.left, self.top, 48, 48)
        self.direction_x, self.direction_y = 0, -1
        self.old_x, self.old_y = self.rect.x, self.rect.y

    def turn(self, direction):
        """根据玩家方向，加载对应不同方向的图片组并改变前进方向属性"""
        if self.cunhuo:
            if direction == 'U':
                self.direction_x, self.direction_y = 0, -1
                self.tank_img = [self.tank_u_0, self.tank_u_1]
            elif direction == 'D':
                self.direction_x, self.direction_y = 0, 1
                self.tank_img = [self.tank_d_0, self.tank_d_1]
            elif direction == 'L':
                self.direction_x, self.direction_y = -1, 0
                self.tank_img = [self.tank_l_0, self.tank_l_1]
            elif direction == 'R':
                self.direction_x, self.direction_y = 1, 0
                self.tank_img = [self.tank_r_0, self.tank_r_1]
            else:
                raise Exception

    def move(self):
        """坦克根据方向属性移动，到达边界将不被允许移动"""
        self.old_x, self.old_y = self.rect.x, self.rect.y
        if self.cunhuo and self.can_move:
            self.rect.move_ip(self.speed * self.direction_x, self.speed * self.direction_y)

    def move_back(self):
        """由于撞墙不能移动效果"""
        self.rect.x, self.rect.y = self.old_x, self.old_y

    def update(self, *args):
        """坦克移动时，实现动态效果
        仅实现护盾计时，显示由main实现
        计算填装时间
        如果在冰面上速度增加"""
        self.tianzhuang -= 1
        if self.can_move:
            if args[0]:
                self.image = self.tank_img[1]
            elif not args[0]:
                self.image = self.tank_img[0]
        if self.hudun:
            self.huduntime -= 1
            if self.huduntime <= 0:
                self.hudun = False
        if self.tabing:
            if self.level == 1:
                self.speed = 5
            elif self.level == 2 or self.level == 3:
                self.speed = 4
            else:
                self.speed = 3
            self.tabing = False
        else:
            if self.level == 1:
                self.speed = 3
            elif self.level == 2 or self.level == 3:
                self.speed = 2
            else:
                self.speed = 1

    def reset(self):
        """重生"""
        self.level = 1
        self.shengming = 1
        self.cunhuo = True
        self.tianzhuang = 60
        # 护盾
        self.hudun = True
        self.huduntime = 250
        # 初始位置和方向
        self.rect = pygame.Rect(self.left, self.top, 48, 48)
        self.direction_x, self.direction_y = 0, -1

    def level_up(self):
        if self.player == 1:
            if self.level < 4:
                self.level += 1
                self.shengming += 1
                if self.level == 2:
                    # 二级坦克
                    self.speed = 2
                    self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 48, 48, 48))
                    self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 48, 48, 48))
                    self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 48, 48, 48))
                    self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 48, 48, 48))
                    self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 48, 48, 48))
                    self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 48, 48, 48))
                    self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 48, 48, 48))
                    self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 48, 48, 48))
                    self.tank_img = [self.tank_u_0, self.tank_u_1]
                elif self.level == 3:
                    # 三级坦克
                    self.tianzhuang = 30
                    self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 96, 48, 48))
                    self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 96, 48, 48))
                    self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 96, 48, 48))
                    self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 96, 48, 48))
                    self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 96, 48, 48))
                    self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 96, 48, 48))
                    self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 96, 48, 48))
                    self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 96, 48, 48))
                    self.tank_img = [self.tank_u_0, self.tank_u_1]
                else:
                    # 四级坦克
                    self.speed = 1
                    self.zidanlevel = 2
                    self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 144, 48, 48))
                    self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 144, 48, 48))
                    self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 144, 48, 48))
                    self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 144, 48, 48))
                    self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 144, 48, 48))
                    self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 144, 48, 48))
                    self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 144, 48, 48))
                    self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 144, 48, 48))
                    self.tank_img = [self.tank_u_0, self.tank_u_1]
        elif self.player == 2:
            if self.level < 4:
                self.level += 1
                self.shengming += 1
                if self.level == 2:
                    # 二级坦克
                    self.speed = 2
                    self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 432, 48, 48))
                    self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 432, 48, 48))
                    self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 432, 48, 48))
                    self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 432, 48, 48))
                    self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 432, 48, 48))
                    self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 432, 48, 48))
                    self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 432, 48, 48))
                    self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 432, 48, 48))
                    self.tank_img = [self.tank_u_0, self.tank_u_1]
                elif self.level == 3:
                    # 三级坦克
                    self.tianzhuang = 30
                    self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 480, 48, 48))
                    self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 480, 48, 48))
                    self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 480, 48, 48))
                    self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 480, 48, 48))
                    self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 480, 48, 48))
                    self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 480, 48, 48))
                    self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 480, 48, 48))
                    self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 480, 48, 48))
                    self.tank_img = [self.tank_u_0, self.tank_u_1]
                else:
                    # 四级坦克
                    self.speed = 1
                    self.zidanlevel = 2
                    self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 528, 48, 48))
                    self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 528, 48, 48))
                    self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 528, 48, 48))
                    self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 528, 48, 48))
                    self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 528, 48, 48))
                    self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 528, 48, 48))
                    self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 528, 48, 48))
                    self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 528, 48, 48))
                    self.tank_img = [self.tank_u_0, self.tank_u_1]

    def level_down(self):
        if self.player == 1:
            if self.level >= 1:
                self.level -= 1
                self.shengming -= 1
                if self.level == 2:
                    # 二级坦克
                    self.tianzhuang = 60
                    self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 48, 48, 48))
                    self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 48, 48, 48))
                    self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 48, 48, 48))
                    self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 48, 48, 48))
                    self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 48, 48, 48))
                    self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 48, 48, 48))
                    self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 48, 48, 48))
                    self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 48, 48, 48))
                    self.tank_img = [self.tank_u_0, self.tank_u_1]
                elif self.level == 3:
                    # 三级坦克
                    self.speed = 2
                    self.zidanlevel = 1
                    self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 96, 48, 48))
                    self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 96, 48, 48))
                    self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 96, 48, 48))
                    self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 96, 48, 48))
                    self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 96, 48, 48))
                    self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 96, 48, 48))
                    self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 96, 48, 48))
                    self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 96, 48, 48))
                    self.tank_img = [self.tank_u_0, self.tank_u_1]
                elif self.level == 1:
                    # 一级坦克
                    self.speed = 3
                    self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 0, 48, 48))
                    self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 0, 48, 48))
                    self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 0, 48, 48))
                    self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 0, 48, 48))
                    self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 0, 48, 48))
                    self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 0, 48, 48))
                    self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 0, 48, 48))
                    self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 0, 48, 48))
                    self.tank_img = [self.tank_u_0, self.tank_u_1]
                else:
                    self.cunhuo = False
        elif self.player == 2:
            if self.level >= 1:
                self.level -= 1
                self.shengming -= 1
                if self.level == 2:
                    # 二级坦克
                    self.tianzhuang = 60
                    self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 432, 48, 48))
                    self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 432, 48, 48))
                    self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 432, 48, 48))
                    self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 432, 48, 48))
                    self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 432, 48, 48))
                    self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 432, 48, 48))
                    self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 432, 48, 48))
                    self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 432, 48, 48))
                    self.tank_img = [self.tank_u_0, self.tank_u_1]
                elif self.level == 3:
                    # 三级坦克
                    self.speed = 2
                    self.zidanlevel = 1
                    self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 480, 48, 48))
                    self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 480, 48, 48))
                    self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 480, 48, 48))
                    self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 480, 48, 48))
                    self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 480, 48, 48))
                    self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 480, 48, 48))
                    self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 480, 48, 48))
                    self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 480, 48, 48))
                    self.tank_img = [self.tank_u_0, self.tank_u_1]
                elif self.level == 1:
                    # 一级坦克
                    self.speed = 3
                    self.tank_u_0 = self.img.subsurface(pygame.Rect(0, 384, 48, 48))
                    self.tank_u_1 = self.img.subsurface(pygame.Rect(48, 384, 48, 48))
                    self.tank_l_0 = self.img.subsurface(pygame.Rect(96, 384, 48, 48))
                    self.tank_l_1 = self.img.subsurface(pygame.Rect(144, 384, 48, 48))
                    self.tank_d_0 = self.img.subsurface(pygame.Rect(192, 384, 48, 48))
                    self.tank_d_1 = self.img.subsurface(pygame.Rect(240, 384, 48, 48))
                    self.tank_r_0 = self.img.subsurface(pygame.Rect(288, 384, 48, 48))
                    self.tank_r_1 = self.img.subsurface(pygame.Rect(336, 384, 48, 48))
                    self.tank_img = [self.tank_u_0, self.tank_u_1]
                else:
                    self.cunhuo = False
