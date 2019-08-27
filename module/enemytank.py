"""
author:程鑫达
time:2019.8.10
version:1.0
说明：
    敌方坦克
    图层：50（属性在父类）
    携带道具可能20%
"""
import copy

from module import tank, daoju
import pygame
import random


class Enemytank(tank.Tank):
    """所有敌人的父类"""
    def __init__(self):
        tank.Tank.__init__(self)
        self.cunhuo = False
        self.level = 1
        self.speed = 1
        self.shengming = 1
        self.tianzhuang = 60
        self.zidanlevel = 1
        # 用于AI
        self.zhuanxiangtime = int(random.uniform(50, 150))
        self.shejitime = int(random.uniform(152, 180))
        # 用于提醒主程序接收子弹
        self.newzidan = False
        # 用于坦克出生时的星星
        self.t = 0  # 出生时星星显示顺序
        self.born = False
        self.xing_0 = self.img.subsurface(pygame.Rect(768, 288, 48, 48))
        self.xing_1 = self.img.subsurface(pygame.Rect(816, 288, 48, 48))
        self.xing_2 = self.img.subsurface(pygame.Rect(864, 288, 48, 48))
        self.xing_3 = self.img.subsurface(pygame.Rect(912, 288, 48, 48))
        # 如果捡到秒表
        self.jingzhi = 200
        # 道具相关
        self.red = random.choice((True, False, False, False, False))
        # self.red = True  # 用于测试道具
        if self.red:
            self.daoju = daoju.Shengchengqi().run()
        # 原始图片中各敌方坦克差别仅在纵坐标
        self.y = 0
        self.tank_u_0 = self.img.subsurface(pygame.Rect(384, self.y, 48, 48))
        self.tank_u_1 = self.img.subsurface(pygame.Rect(432, self.y, 48, 48))
        self.tank_d_0 = self.img.subsurface(pygame.Rect(576, self.y, 48, 48))
        self.tank_d_1 = self.img.subsurface(pygame.Rect(624, self.y, 48, 48))
        self.tank_l_0 = self.img.subsurface(pygame.Rect(480, self.y, 48, 48))
        self.tank_l_1 = self.img.subsurface(pygame.Rect(528, self.y, 48, 48))
        self.tank_r_0 = self.img.subsurface(pygame.Rect(672, self.y, 48, 48))
        self.tank_r_1 = self.img.subsurface(pygame.Rect(720, self.y, 48, 48))
        self.tank_img = [self.tank_u_0, self.tank_u_1]
        self.image = self.tank_img[1]
        self.rect = pygame.Rect(0, 0, 48, 48)
        self.old_x, self.old_y = self.rect.x, self.rect.y

    def turn(self, direction):
        """根据AI玩家方向，加载对应不同方向的图片组并改变前进方向属性"""
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
        """如果处于被静止状态，将在200帧后解除；若能移动，则处理动态效果"""
        if not self.born:  # 如果还没有出生
            self.cunhuo = True  # 防止因子弹击中出生地而死亡
            if self.t == 0:
                self.image = self.xing_0
            elif self.t == 1:
                self.image = self.xing_1
            elif self.t == 2:
                self.image = self.xing_2
            elif self.t == 3:
                self.image = self.xing_3
            elif self.t == 4:
                self.image = self.xing_1
            elif self.t == 5:
                self.image = self.xing_2
            self.t += 1  # 此上用于实现出生时星星动态效果
            if self.t == 6:  # 出生结束，能移动，初始方向下，加载初始图片组，加载初始图片
                self.born = True
                self.can_move = True
                self.direction_x, self.direction_y = 0, 1
                self.tank_img = [self.tank_d_0, self.tank_d_1]
                self.image = self.tank_img[1]
        else:  # 已出生的坦克执行以下代码
            if not self.can_move:  # 如果受到秒表效果
                self.jingzhi -= 1
                if self.jingzhi == 0:
                    self.can_move = True
                    self.jingzhi = 200
            else:  # 正常情况下，移动动态效果
                if args[0]:
                    self.image = self.tank_img[1]
                elif not args[0]:
                    self.image = self.tank_img[0]
                self.move()
                if self.rect.left < 0 or self.rect.top < 0 or self.rect.bottom > 624 \
                        or self.rect.right > 624:  # 如果超出边界，不容许移动
                    self.move_back()
            # 转向，填装，射击倒计时
            self.zhuanxiangtime -= 1
            self.tianzhuang -= 1
            self.shejitime -= 1
            # 转向
            if self.zhuanxiangtime == 0:
                temp = int(random.random()*4)
                if temp == 0:
                    self.turn('U')
                elif temp == 1:
                    self.turn('D')
                elif temp == 2:
                    self.turn('L')
                elif temp == 3:
                    self.turn('R')
                self.zhuanxiangtime = int(random.uniform(50, 150))
            # 射击
            if self.shejitime == 0:
                self.shoot()
                self.newzidan = True
                if isinstance(self, BasicTank) or isinstance(self, ArmorTank):
                    self.shejitime = int(random.uniform(91, 110))
                    self.tianzhuang = 60
                else:
                    self.shejitime = int(random.uniform(61, 100))
                    self.tianzhuang = 30

    def shoot(self):
        if self.tianzhuang <= 0:
            weizhi = copy.deepcopy(self.rect)
            if self.direction_x == 0 and self.direction_y == -1:
                weizhi.x += 18
            elif self.direction_x == 0 and self.direction_y == 1:
                weizhi.x += 18
                weizhi.y += 34
            elif self.direction_x == -1 and self.direction_y == 0:
                weizhi.y += 18
            elif self.direction_x == 1 and self.direction_y == 0:
                weizhi.x += 34
                weizhi.y += 18
            self.zidan = tank.Zidan(3, self.zidanlevel, weizhi, (self.direction_x, self.direction_y))


class BasicTank(Enemytank):
    """速度1    填装10   子弹等级1   子弹速度1"""
    def __init__(self):
        Enemytank.__init__(self)
        self.level = 1
        self.speed = 1
        self.shengming = 1
        self.tianzhuang = 60
        self.zidanlevel = 1
        self.points = 100
        self.y = 192
        if self.red == True:
            self.y += 384
        self.tank_u_0 = self.img.subsurface(pygame.Rect(384, self.y, 48, 48))
        self.tank_u_1 = self.img.subsurface(pygame.Rect(432, self.y, 48, 48))
        self.tank_d_0 = self.img.subsurface(pygame.Rect(576, self.y, 48, 48))
        self.tank_d_1 = self.img.subsurface(pygame.Rect(624, self.y, 48, 48))
        self.tank_l_0 = self.img.subsurface(pygame.Rect(480, self.y, 48, 48))
        self.tank_l_1 = self.img.subsurface(pygame.Rect(528, self.y, 48, 48))
        self.tank_r_0 = self.img.subsurface(pygame.Rect(672, self.y, 48, 48))
        self.tank_r_1 = self.img.subsurface(pygame.Rect(720, self.y, 48, 48))
        self.tank_img = [self.tank_d_0, self.tank_d_1]
        self.image = self.tank_img[1]
        self.direction_x, self.direction_y = 0, -1


class FastTank(Enemytank):
    """速度3    填装5   子弹等级1   子弹速度2"""
    def __init__(self):
        Enemytank.__init__(self)
        self.level = 2
        self.speed = 3
        self.shengming = 1
        self.tianzhuang = 30
        self.shejitime = int(random.uniform(91, 150))
        self.zidanlevel = 1
        self.points = 200
        self.y = 240
        if self.red == True:
            self.y += 384
        self.tank_u_0 = self.img.subsurface(pygame.Rect(384, self.y, 48, 48))
        self.tank_u_1 = self.img.subsurface(pygame.Rect(432, self.y, 48, 48))
        self.tank_d_0 = self.img.subsurface(pygame.Rect(576, self.y, 48, 48))
        self.tank_d_1 = self.img.subsurface(pygame.Rect(624, self.y, 48, 48))
        self.tank_l_0 = self.img.subsurface(pygame.Rect(480, self.y, 48, 48))
        self.tank_l_1 = self.img.subsurface(pygame.Rect(528, self.y, 48, 48))
        self.tank_r_0 = self.img.subsurface(pygame.Rect(672, self.y, 48, 48))
        self.tank_r_1 = self.img.subsurface(pygame.Rect(720, self.y, 48, 48))


class PowerTank(Enemytank):
    """速度2    填装10   子弹等级1   子弹速度3"""
    def __init__(self):
        Enemytank.__init__(self)
        self.level = 3
        self.speed = 2
        self.shengming = 1
        self.tianzhuang = 30
        self.shejitime = int(random.uniform(91, 150))
        self.zidanlevel = 1
        self.points = 300
        self.y = 288
        if self.red == True:
            self.y += 384
        self.tank_u_0 = self.img.subsurface(pygame.Rect(384, self.y, 48, 48))
        self.tank_u_1 = self.img.subsurface(pygame.Rect(432, self.y, 48, 48))
        self.tank_d_0 = self.img.subsurface(pygame.Rect(576, self.y, 48, 48))
        self.tank_d_1 = self.img.subsurface(pygame.Rect(624, self.y, 48, 48))
        self.tank_l_0 = self.img.subsurface(pygame.Rect(480, self.y, 48, 48))
        self.tank_l_1 = self.img.subsurface(pygame.Rect(528, self.y, 48, 48))
        self.tank_r_0 = self.img.subsurface(pygame.Rect(672, self.y, 48, 48))
        self.tank_r_1 = self.img.subsurface(pygame.Rect(720, self.y, 48, 48))


class ArmorTank(Enemytank):
    """速度2    填装10   子弹等级2   子弹速度2"""
    def __init__(self):
        Enemytank.__init__(self)
        self.level = 4
        self.speed = 2
        self.shengming = 4
        self.tianzhuang = 60
        self.zidanlevel = 2
        self.points = 400
        self.y = 336
        if self.red == True:
            self.y += 384
        self.tank_u_0 = self.img.subsurface(pygame.Rect(384, self.y, 48, 48))
        self.tank_u_1 = self.img.subsurface(pygame.Rect(432, self.y, 48, 48))
        self.tank_d_0 = self.img.subsurface(pygame.Rect(576, self.y, 48, 48))
        self.tank_d_1 = self.img.subsurface(pygame.Rect(624, self.y, 48, 48))
        self.tank_l_0 = self.img.subsurface(pygame.Rect(480, self.y, 48, 48))
        self.tank_l_1 = self.img.subsurface(pygame.Rect(528, self.y, 48, 48))
        self.tank_r_0 = self.img.subsurface(pygame.Rect(672, self.y, 48, 48))
        self.tank_r_1 = self.img.subsurface(pygame.Rect(720, self.y, 48, 48))
