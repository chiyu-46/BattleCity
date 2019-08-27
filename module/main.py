"""
坦克大战复刻版（受苦向）
author:程鑫达
time:2019.8.10
version:1.0(alpha)
说明：
    本游戏的时间参数有两种计算方式，帧数和毫秒数
"""

import pygame
import sys
import random
import copy

from module import tank, mytank, map, enemytank, daoju, boom

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
GAME_WIDTH = 624
GAME_HEIGHT = 624
BG_COLOR = pygame.Color(0, 0, 0)
GAME_COLOR = pygame.Color(0, 0, 0)


class MainGame:
    def __init__(self):
        self.window = None
        # 存储敌方坦克的列表
        self.enemyTankList = pygame.sprite.LayeredUpdates()
        self.enemyTankList_canzhan = pygame.sprite.LayeredUpdates()
        self.enemynum = 0
        self.enemynum_canzhan = 0
        # 敌人产生相关参数
        self.chushengtime = 1100
        self.chushengdian = True  # 左
        self.shengcheng = False
        # 存储我方坦克的列表
        self.num = 0
        self.tank_1 = mytank.Mytank(1)
        self.tank_2 = mytank.Mytank(2)
        self.myTankList = pygame.sprite.LayeredUpdates()
        self.mynum = 0
        # 两个坦克死亡次数
        self.deadnum_1 = 0
        self.deadnum_2 = 0
        # 护盾相关
        self.hudunimg = pygame.image.load(r'./resource/img/protect.png')
        self.hudun_0 = self.hudunimg.subsurface(pygame.Rect(0, 0, 48, 48))
        self.hudun_1 = self.hudunimg.subsurface(pygame.Rect(48, 0, 48, 48))
        # 存储子弹的列表
        self.BulletList = pygame.sprite.LayeredUpdates()
        # 存储爆炸效果的列表
        self.explodeList = pygame.sprite.LayeredUpdates()
        # 存储场景的列表
        self.shiqiang_group = pygame.sprite.LayeredUpdates()
        self.tie_group = pygame.sprite.LayeredUpdates()
        self.bing_group = pygame.sprite.LayeredUpdates()
        self.he_group = pygame.sprite.LayeredUpdates()
        self.cao_group = pygame.sprite.LayeredUpdates()
        self.ying = pygame.sprite.LayeredUpdates()
        # 储存道具列表
        self.daoju_group = pygame.sprite.LayeredUpdates()
        # 当前关卡数
        self.stage = 34
        # 是否获胜
        self.win = False
        # 游戏是否结束(包括胜负两种)
        self.gameover = False
        # 实现平滑坦克改变移动方向
        self.temp_1 = ''
        self.temp_2 = ''
        # 实现动态效果
        self.change = True
        # 文字对象
        pygame.font.init()
        self.font = pygame.font.Font(r'./resource/font/simkai.ttf', 48)
        # 音乐对象
        pygame.mixer.init()

    # 开始界面
    def start_ui(self, sur):
        """
        按1单人模式，按2双人模式，回车确认；
        不能使用小键盘的键
        """
        img_1 = pygame.transform.scale(pygame.image.load(r'./resource/img/Miscellaneous_1.bmp'), (614, 537))
        img_2 = pygame.transform.scale(pygame.image.load(r'./resource/img/Miscellaneous_2.bmp'), (614, 537))
        image = img_1
        num = 1
        rect = img_1.get_rect()
        rect.centerx, rect.centery = sur.get_rect().centerx, sur.get_rect().centery
        while True:
            sur.blit(image, rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        image = img_1
                        num = 1
                    elif event.key == pygame.K_2:
                        image = img_2
                        num = 2
                    elif event.key == pygame.K_RETURN:
                        return num

    def switch_stage(self, sur, stage=-1):
        """
        如果stage传入参数，实现选关功能；
        如果不传入，进行下一个；
        如果已经是最后一个，通知用户已胜利
        """
        if stage == -1:
            stage = self.stage + 1
        if stage > 35:
            content = self.font.render(u'恭喜通关', True, (255, 255, 255))
            rect = content.get_rect()
            rect.centerx, rect.centery = sur.get_rect().centerx, sur.get_rect().centery
            self.window.fill(BG_COLOR)
            sur.blit(content, rect)
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
        else:
            # 显示接下来的关卡数
            content = self.font.render(u'第{}关'.format(stage), True, (255, 255, 255))
            rect = content.get_rect()
            rect.centerx, rect.centery = sur.get_rect().centerx, sur.get_rect().centery
            self.window.fill(BG_COLOR)
            sur.blit(content, rect)
            pygame.display.update()
            # 参数初始化
            self.stage = stage
            self.win = False
            self.gameover = False
            self.enemyTankList.empty()
            self.enemyTankList_canzhan.empty()
            self.enemynum = 0
            self.enemynum_canzhan = 0
            self.chushengtime = 50
            self.chushengdian = True  # 左
            self.shengcheng = False
            self.tank_1 = mytank.Mytank(1)
            self.tank_2 = mytank.Mytank(2)
            self.myTankList.empty()
            self.mynum = 0
            self.deadnum_1 = 0
            self.deadnum_2 = 0
            self.BulletList.empty()
            self.explodeList.empty()
            self.shiqiang_group.empty()
            self.tie_group.empty()
            self.bing_group.empty()
            self.he_group.empty()
            self.cao_group.empty()
            self.ying.empty()
            self.daoju_group.empty()
            # 读取地图
            guanqia = map.Map(stage)
            self.shiqiang_group, self.tie_group, self.bing_group, self.he_group, self.cao_group, self.ying = \
                guanqia.get_map()
            # 第几关文字显示1.5秒
            pygame.time.wait(1500)
            # 播放开始音效
            pygame.mixer.Sound(r'./resource/audio/stage_start.ogg').play()

    def is_gameover(self):
        """
        如果己方胜利，win为True;
        如果己方失败，win为False；
        两种情况均使gameover为True
        """
        if self.mynum == 0 or not self.ying.get_top_sprite().cunhuo:
            self.win = False
            self.gameover = True
            pygame.mixer.Sound(r'./resource/audio/game_over.ogg').play()
        elif self.enemynum_canzhan == 0:
            self.win = True
            self.gameover = True


    def game_over(self, sur):
        """
        己方失败，按R重玩
        """
        if self.gameover:
            content = self.font.render(u'游戏结束', True, (255, 255, 255))
            rect = content.get_rect()
            rect.centerx, rect.centery = self.window.get_rect().centerx, self.window.get_rect().centery
            self.window.blit(content, rect)
            pygame.display.update()
            # 文字显示1.5秒
            pygame.time.wait(1500)

            content = self.font.render(u'按R重玩', True, (255, 255, 255))
            rect = content.get_rect()
            rect.centerx, rect.centery = sur.get_rect().centerx, sur.get_rect().centery
            self.window.fill(BG_COLOR)
            sur.blit(content, rect)
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            return

    def chushihua_enemy(self):
        """初始化敌方坦克"""
        temp = map.Map(self.stage).get_enemy()  # 获取敌人配置

        n = 0  # 一种坦克的数量
        for a in temp:
            for b in a.split('*'):
                if b == 'basic':
                    for c in range(n):
                        self.enemyTankList.add(enemytank.BasicTank())
                elif b == 'fast':
                    for c in range(n):
                        self.enemyTankList.add(enemytank.FastTank())
                elif b == 'power':
                    for c in range(n):
                        self.enemyTankList.add(enemytank.PowerTank())
                elif b == 'armor':
                    for c in range(n):
                        self.enemyTankList.add(enemytank.ArmorTank())
                else:
                    self.enemynum += int(b)
                    n = int(b)

    def start(self):
        # 初始化窗口
        pygame.display.init()
        # 设置窗口大小及显示
        self.window = pygame.display.set_mode([GAME_WIDTH, GAME_HEIGHT])
        # 限制帧率以优化运行速度
        clock = pygame.time.Clock()
        # 为实现轮胎和场景动态效果
        times = 5
        # 设置窗口标题和图标
        pygame.display.set_caption('BattleCity v1.0')
        pygame.display.set_icon(pygame.image.load(r'.\resource\img\favicon.ico'))
        # 开始界面
        self.num = self.start_ui(self.window)
        while True:
            # 如果因胜利返回，加载下一关；否则按R重来，加载本关
            if self.win:
                self.switch_stage(self.window)
            else:
                self.game_over(self.window)
                self.switch_stage(self.window, self.stage)

            # 初始化己方坦克
            if self.num == 1:
                self.tank_1.cunhuo = True
                self.myTankList.add(self.tank_1)
                self.mynum = 1
            elif self.num == 2:
                self.tank_1.cunhuo = True
                self.myTankList.add(self.tank_1)
                self.tank_2.cunhuo = True
                self.myTankList.add(self.tank_2)
                self.mynum = 2
            # 初始化敌方坦克
            self.chushihua_enemy()
            # 游戏主循环
            while not self.gameover:
                # 限制帧率使坦克移动的速度慢一点
                clock.tick(30)
                # 给窗口设置填充色
                self.window.fill(BG_COLOR)
                # 获取事件
                self.get_event()
                # 实现场景和坦克的动态效果(按帧计算）
                if times == 3:
                    self.change = False
                elif times == 0:
                    self.change = True
                    times = 6
                times -= 1

                self.show_bing()
                self.show_he()
                self.show_enemy()
                self.show_mytank()
                self.show_qiang()
                self.show_cao()
                self.show_ying()
                self.show_bullet()
                self.show_explode()
                self.show_daoju()

                # 显示护盾
                if self.tank_1.cunhuo and self.tank_1.hudun:
                    if self.change:
                        self.window.blit(self.hudun_0, self.tank_1.rect)
                    else:
                        self.window.blit(self.hudun_1, self.tank_1.rect)
                if self.tank_2.cunhuo and self.tank_2.hudun:
                    if self.change:
                        self.window.blit(self.hudun_0, self.tank_2.rect)
                    else:
                        self.window.blit(self.hudun_1, self.tank_2.rect)

                pygame.display.update()
                # 判断游戏是否结束
                self.is_gameover()

    def get_event(self):
        """玩家操作相关方法，用于控制己方坦克移动和射击（也用于处理中途退出）"""
        # 获取所有事件
        event_list = pygame.event.get()
        # 遍历事件
        for event in event_list:
            # 判断按下的键是关闭还是键盘按下
            # 如果按的是退出，关闭窗口
            if event.type == pygame.QUIT:
                sys.exit()
            # 如果是键盘的按下，更改坦克方向并打开移动开关
            elif event.type == pygame.KEYDOWN:
                if self.tank_1.cunhuo:
                    if event.key == pygame.K_a:
                        self.tank_1.can_move = True
                        self.tank_1.turn('L')
                        self.temp_1 = 'L'
                    elif event.key == pygame.K_d:
                        self.tank_1.can_move = True
                        self.tank_1.turn('R')
                        self.temp_1 = 'R'
                    elif event.key == pygame.K_w:
                        self.tank_1.can_move = True
                        self.tank_1.turn('U')
                        self.temp_1 = 'U'
                    elif event.key == pygame.K_s:
                        self.tank_1.can_move = True
                        self.tank_1.turn('D')
                        self.temp_1 = 'D'
                    elif event.key == pygame.K_SPACE:
                        if self.tank_1.tianzhuang <= 0:
                            weizhi = copy.deepcopy(self.tank_1.rect)
                            if self.temp_1 == 'U':
                                weizhi.x += 18
                            elif self.temp_1 == 'D':
                                weizhi.x += 18
                                weizhi.y += 34
                            elif self.temp_1 == 'L':
                                weizhi.y += 18
                            elif self.temp_1 == 'R':
                                weizhi.x += 34
                                weizhi.y += 18
                            self.BulletList.add(tank.Zidan(1, self.tank_1.zidanlevel, (weizhi.left, weizhi.top),
                                                           (self.tank_1.direction_x, self.tank_1.direction_y)))
                            pygame.mixer.Sound(r'./resource/audio/bullet_shot.ogg').play()
                            if self.tank_1.level == 1 or self.tank_1.level == 2:
                                self.tank_1.tianzhuang = 60
                            elif self.tank_1.level == 3 or self.tank_1.level == 4:
                                self.tank_1.tianzhuang = 30
                if self.tank_2.cunhuo:
                    if event.key == pygame.K_LEFT:
                        self.tank_2.can_move = True
                        self.tank_2.turn('L')
                        self.temp_2 = 'L'
                    elif event.key == pygame.K_RIGHT:
                        self.tank_2.can_move = True
                        self.tank_2.turn('R')
                        self.temp_2 = 'R'
                    elif event.key == pygame.K_UP:
                        self.tank_2.can_move = True
                        self.tank_2.turn('U')
                        self.temp_2 = 'U'
                    elif event.key == pygame.K_DOWN:
                        self.tank_2.can_move = True
                        self.tank_2.turn('D')
                        self.temp_2 = 'D'
                    elif event.key == pygame.K_KP0:
                        if self.tank_2.tianzhuang <= 0:
                            weizhi = copy.deepcopy(self.tank_2.rect)
                            if self.temp_2 == 'U':
                                weizhi.x += 18
                            elif self.temp_2 == 'D':
                                weizhi.x += 18
                                weizhi.y += 34
                            elif self.temp_2 == 'L':
                                weizhi.y += 18
                            elif self.temp_2 == 'R':
                                weizhi.x += 34
                                weizhi.y += 18
                            self.BulletList.add(tank.Zidan(2, self.tank_2.zidanlevel, weizhi,
                                                           (self.tank_2.direction_x, self.tank_2.direction_y)))
                            pygame.mixer.Sound(r'./resource/audio/bullet_shot.ogg').play()
                            if self.tank_2.level == 1 or self.tank_2.level == 2:
                                self.tank_2.tianzhuang = 60
                            elif self.tank_2.level == 3 or self.tank_2.level == 4:
                                self.tank_2.tianzhuang = 30
            # 松开方向键，坦克停止移动，修改坦克的开关状态
            elif event.type == pygame.KEYUP:
                # 判断松开的键是最近一次按下的键的时候才停止坦克移动
                if self.tank_1.cunhuo:
                    if self.temp_1 == 'U' and event.key == pygame.K_w:
                        self.tank_1.can_move = False
                    elif self.temp_1 == 'D' and event.key == pygame.K_s:
                        self.tank_1.can_move = False
                    elif self.temp_1 == 'L' and event.key == pygame.K_a:
                        self.tank_1.can_move = False
                    elif self.temp_1 == 'R' and event.key == pygame.K_d:
                        self.tank_1.can_move = False
                if self.tank_2.cunhuo:
                    if self.temp_2 == 'U' and event.key == pygame.K_UP:
                        self.tank_2.can_move = False
                    elif self.temp_2 == 'D' and event.key == pygame.K_DOWN:
                        self.tank_2.can_move = False
                    elif self.temp_2 == 'L' and event.key == pygame.K_LEFT:
                        self.tank_2.can_move = False
                    elif self.temp_2 == 'R' and event.key == pygame.K_RIGHT:
                        self.tank_2.can_move = False

    def show_enemy(self):
        """功能：
            1.生成将备战坦克加入参战组
            2.敌人死亡，更改在场敌人人数，清理尸体；如果有道具，将道具加入道具组
            3.如果有参战敌人发射子弹，加入子弹组"""
        if self.enemynum > 0:  # 如果有坦克待命，就准备生成新敌人
            if self.enemynum_canzhan >= 2:  # 如果在场坦克大于2，每50帧生成一个
                self.chushengtime -= 1
                if self.chushengtime == 0:
                    self.shengcheng = True
                    self.chushengtime = 1100
            elif self.enemynum_canzhan < 2:  # 如果在场坦克小于2，立即生成一个
                self.shengcheng = True
                self.chushengtime = 1100
        if self.shengcheng:  # 如果要生成敌人，从待命区抽一个进入参战区，相关数量改变
            temp = self.enemyTankList.get_sprite(int(random.random() * self.enemynum))
            temp.cunhuo = True
            if self.chushengdian:
                temp.rect.x, temp.rect.y = 0, 0
            else:
                temp.rect.x, temp.rect.y = 576, 0
            self.chushengdian = not self.chushengdian
            self.enemyTankList.remove(temp)
            self.enemynum -= 1
            self.enemyTankList_canzhan.add(temp)
            self.enemynum_canzhan += 1
            self.shengcheng = False
        for each in self.enemyTankList_canzhan.sprites():
            if each.newzidan:  # 如果有参战敌人发射子弹，加入子弹组
                self.BulletList.add(each.zidan)
            # 两坦克相撞，不允许移动
            for my in self.myTankList.sprites():
                if pygame.sprite.collide_rect(each, my):
                    each.move_back()
                    my.move_back()
            for another in self.enemyTankList_canzhan.sprites():
                if pygame.sprite.collide_rect(each, another):
                    if each != another:
                        each.move_back()
                        another.move_back()

        self.enemyTankList_canzhan.draw(self.window)
        self.enemyTankList_canzhan.update(self.change)

    def show_daoju(self):
        """展示道具并发挥作用，生成由show_bullet负责"""
        for each in self.daoju_group.sprites():
            if not each.cunhuo:
                self.daoju_group.remove(each)
            for my in self.myTankList.sprites():
                if pygame.sprite.collide_rect(each, my):
                    pygame.mixer.Sound(r'./resource/audio/powerup_pick.ogg').play()
                    if each.kind == 1:  # 头盔
                        my.hudun = True
                        my.huduntime = 250
                    elif each.kind == 2:  # 秒表(由敌update解除静止状态)
                        for a in self.enemyTankList_canzhan.sprites():
                            a.can_move = False
                    elif each.kind == 3:  # 铲子（为游戏平衡移除）
                        pass
                    elif each.kind == 4:  # 星星
                        my.level_up()
                    elif each.kind == 5:  # 手雷
                        for a in self.enemyTankList_canzhan.sprites():
                            a.cunhuo = False
                            self.enemyTankList_canzhan.remove(a)
                        self.enemynum_canzhan = 0
                    elif each.kind == 6:  # 坦克
                        my.shengming += 1
                    elif each.kind == 7:  # 枪
                        my.level = 3
                        my.level_up()
                    each.cunhuo = False
                    self.daoju_group.remove(each)
        self.daoju_group.draw(self.window)
        self.daoju_group.update()

    def show_mytank(self):
        """功能：
            1.死亡时的复活和清理
            2。坦克移动"""
        if not self.tank_1.cunhuo:
            self.deadnum_1 += 1
            if self.deadnum_1 == 2:  # 防止已彻底死亡后重复执行
                self.myTankList.remove(self.tank_1)
                self.mynum -= 1
            elif self.deadnum_1 == 0 or self.deadnum_1 == 1:  # 死两次以下，复活
                self.tank_1.reset()
        else:  # 如果坦克活着，就可以移动，但不允许超出屏幕边界
            self.tank_1.move()
            if self.tank_1.rect.left < 0 or self.tank_1.rect.top < 0 or self.tank_1.rect.bottom > 624 \
                    or self.tank_1.rect.right > 624:
                self.tank_1.move_back()
        if self.num == 2:  # 在双人模式下（内容与上部分相同）
            if not self.tank_2.cunhuo:
                self.deadnum_2 += 1
                if self.deadnum_2 == 2:
                    self.myTankList.remove(self.tank_2)
                    self.mynum -= 1
                elif self.deadnum_2 == 0 or self.deadnum_2 == 1:
                    self.tank_2.reset()
            else:
                self.tank_2.move()
                if self.tank_2.rect.left < 0 or self.tank_2.rect.top < 0 or self.tank_2.rect.bottom > 624 \
                        or self.tank_2.rect.right > 624:
                    self.tank_2.move_back()
                if pygame.sprite.collide_rect(self.tank_1, self.tank_2):
                    self.tank_1.move_back()
                    self.tank_2.move_back()

        self.myTankList.update(self.change)
        self.myTankList.draw(self.window)

    def show_bullet(self):
        """子弹组包括敌我双方子弹，依靠阵营属性判断是否起作用"""
        for zidan in self.BulletList.sprites():
            if zidan.cunhuo:
                for my in self.myTankList.sprites():  # 与己方碰撞
                    if pygame.sprite.collide_rect(zidan, my):
                        if zidan.faction == 1 or zidan.faction == 2:  # 应当使己方坦克强制停止，看我有没有心情完成
                            pass
                        elif zidan.faction == 3:  # 受敌人进攻
                            if not my.hudun:  # 没有护盾降级（或死亡）；子弹爆炸
                                my.level_down()
                                zidan.cunhuo = False
                                self.explodeList.add(boom.Boom(zidan))
                                pygame.mixer.Sound(r'./resource/audio/explosion_1.ogg').play()
                            else:  # 有护盾，子弹消失
                                zidan.cunhuo = False
            if zidan.cunhuo:
                for enemy in self.enemyTankList_canzhan.sprites():  # 与敌方碰撞
                    if pygame.sprite.collide_rect(zidan, enemy):
                        if zidan.faction == 1 or zidan.faction == 2:
                            enemy.shengming -= 1
                            if enemy.shengming <= 0:
                                enemy.cunhuo = False
                                if enemy.red:  # 如果有道具，将道具加入道具组
                                    enemy.daoju.cunhuo = True
                                    self.daoju_group.add(enemy.daoju)
                                    pygame.mixer.Sound(r'./resource/audio/powerup_appear.ogg').play()
                                self.enemynum_canzhan -= 1
                                self.enemyTankList_canzhan.remove(enemy)
                            zidan.cunhuo = False
                            self.explodeList.add(boom.Boom(zidan))
                            pygame.mixer.Sound(r'./resource/audio/explosion_1.ogg').play()
            if zidan.cunhuo:
                for shi in self.shiqiang_group.sprites():  # 与石墙碰撞
                    if pygame.sprite.collide_rect(zidan, shi):
                        shi.shengming -= 1
                        if shi.shengming <= 0:
                            shi.cunhuo = False
                            self.shiqiang_group.remove(shi)
                        zidan.cunhuo = False
                        self.explodeList.add(boom.Boom(zidan))
                        if zidan.faction == 1 or zidan.faction == 2:
                            pygame.mixer.Sound(r'./resource/audio/explosion_2.ogg').play()
            if zidan.cunhuo:
                for tie in self.tie_group.sprites():  # 与铁墙碰撞
                    if pygame.sprite.collide_rect(zidan, tie):
                        if zidan.level == 2:
                            tie.shengming -= 1
                            if tie.shengming <= 0:
                                tie.cunhuo = False
                                self.tie_group.remove(tie)
                        zidan.cunhuo = False
                        self.explodeList.add(boom.Boom(zidan))
                        if zidan.faction == 1 or zidan.faction == 2:
                            pygame.mixer.Sound(r'./resource/audio/explosion_2.ogg').play()
            if zidan.cunhuo:
                for ying in self.ying.sprites():
                    if pygame.sprite.collide_rect(zidan, ying):
                        ying.cunhuo = False
                        zidan.cunhuo = False
                        self.explodeList.add(boom.Boom(zidan))
                        if zidan.faction == 1 or zidan.faction == 2:
                            pygame.mixer.Sound(r'./resource/audio/explosion_2.ogg').play()
            if zidan.cunhuo:
                for another in self.BulletList.sprites():
                    if pygame.sprite.collide_rect(zidan, another):
                        if zidan != another:
                            zidan.cunhuo = False
                            another.cunhuo = False

            if not zidan.cunhuo:  # 子弹消失
                self.BulletList.remove(zidan)
        self.BulletList.update()  # 实现移动和边界消亡
        self.BulletList.draw(self.window)

    def show_explode(self):
        """展示爆炸效果，结束后清理"""
        self.explodeList.draw(self.window)
        self.explodeList.update()  # 实现动态效果和自我消亡
        for each in self.explodeList.sprites():
            if not each.cunhuo:
                self.explodeList.remove(each)

    def show_qiang(self):
        """展示场景，并实现场景相关碰撞功能
        为方便操作，使用缩放碰撞判定"""
        self.shiqiang_group.draw(self.window)
        # self.shiqiang_group.update()   # 暂时无效
        for each in self.shiqiang_group.sprites():  # 不允许穿墙
            for my in self.myTankList.sprites():
                if pygame.sprite.collide_rect_ratio(0.9)(each, my):
                    my.move_back()
            for enemy in self.enemyTankList_canzhan.sprites():
                if pygame.sprite.collide_rect_ratio(0.9)(each, enemy):
                    enemy.move_back()

        self.tie_group.draw(self.window)
        # self.tie_group.update()   # 暂时无效
        for each in self.tie_group.sprites():  # 不允许穿墙
            for my in self.myTankList.sprites():
                if pygame.sprite.collide_rect_ratio(0.9)(each, my):
                    my.move_back()
            for enemy in self.enemyTankList_canzhan.sprites():
                if pygame.sprite.collide_rect_ratio(0.9)(each, enemy):
                    enemy.move_back()

    def show_bing(self):
        self.bing_group.draw(self.window)
        for each in self.bing_group.sprites():  # 走在冰上速度增加
            for my in self.myTankList.sprites():
                if pygame.sprite.collide_rect(each, my):
                    my.tabing = True
            for enemy in self.enemyTankList_canzhan.sprites():
                if pygame.sprite.collide_rect(each, enemy):
                    enemy.tabing = True

    def show_he(self):
        self.he_group.draw(self.window)
        self.he_group.update()   # 河流动态效果
        for each in self.he_group.sprites():  # 不允许穿河
            for my in self.myTankList.sprites():
                if pygame.sprite.collide_rect_ratio(0.9)(each, my):
                    my.move_back()
            for enemy in self.enemyTankList_canzhan.sprites():
                if pygame.sprite.collide_rect_ratio(0.9)(each, enemy):
                    enemy.move_back()

    def show_cao(self):
        self.cao_group.draw(self.window)

    def show_ying(self):
        self.ying.draw(self.window)
        self.ying.update()  # 大本营死亡更改图像
        for each in self.ying.sprites():  # 不允许穿大本营
            for my in self.myTankList.sprites():
                if pygame.sprite.collide_rect(each, my):
                    my.move_back()
            for enemy in self.enemyTankList_canzhan.sprites():
                if pygame.sprite.collide_rect(each, enemy):
                    enemy.move_back()
