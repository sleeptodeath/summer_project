# coding=utf-8
"""
冲鸭
许清源
16041187
2018.9.7
"""
import sys

from plane import *
from enemy import *
from energy import *

import pygame
from pygame.locals import *
import pygame.freetype

# order = [(1, ), (2, ), (1, ), (2,), (3, 3), (1, 3), (2, 3), (2, 1), (4, ), (6, 1), (5, 3), (1, 2, 4), (4, 5), (3, 7), (6, 1, 2),
#          (999, )]

# order = [(1, ), (2, ), (1, ), (999, )]

class Game(object):

    def __init__(self):

        self.order = [(1,), (2,), (1,), (2,), (3, 3), (1, 3), (2, 3), (2, 1), (4,), (6, 1), (5, 3), (1, 2, 4), (4, 5),
                      (3, 7), (6, 1, 2),
                      (999,)]
        self.n = 0

        # pygame初始化
        pygame.init()
        pygame.mixer.init()

        # 设置尺寸参数
        self.size = (self.width, self.height) = (448, 650)
        # 初始化窗口
        self.screen = pygame.display.set_mode(self.size)
        # 背景图片加载
        self.background = pygame.image.load("../picture/background.png").convert()
        self.background_index = -self.background.get_size()[1] + self.height
        # 设置标题
        pygame.display.set_caption("飞机大战")
        # 设置icon
        icon = pygame.image.load("../picture/icon.png").convert_alpha()
        pygame.display.set_icon(icon)


        # 主循环标志
        self.running = True
        # 游戏是否开始标志
        self.game_start = False
        # 游戏是否暂停
        self.game_stop = False
        # 游戏结束标志
        self.game_over = False
        # 大招是否充能完毕
        self.can_jineng = False
        # 是否开启声音
        self.sound_is_on = True
        # 帧率
        self.fps = 30
        # 得分
        self.score = 0
        # 获得最高分
        file_name = "score.txt"
        self.high_score = self.get_high_score(file_name)
        # boss提示
        self.warning = False
        # 是否最小化
        self.minsize = False

        # 玩家
        self.player = None
        # 敌机组
        self.enemies = None
        # 资源组s
        self.energy = None

        # 设置字体
        self.font = pygame.freetype.Font("../font/msyh.ttc", 26)
        self.WHITE = (255, 255, 255)

        # 得分图片加载
        score_pic = pygame.image.load("../picture/score.png").convert_alpha()
        self.score_pic = pygame.transform.scale(score_pic, (40, 30))
        # 分数文字
        self.score_surf, score_rect = self.font.render("{}".format(self.score), self.WHITE)

        # 大招图标加载和处理
        bomb_pic = pygame.image.load("../picture/jineng_2.png").convert_alpha()
        b_w, b_h = bomb_pic.get_size()
        self.bomb_pic = pygame.transform.scale(bomb_pic, (80, 56))

        # 玩家hp图标加载和处理
        hp_pic = pygame.image.load(pic['plane'][0]).convert_alpha()
        self.hp_pic = pygame.transform.scale(hp_pic, (40, 40))
        self.hp_w, self.hp_h = hp_pic.get_size()
        # 警告
        self.warning_pic = pygame.image.load(pic['warning']).convert_alpha()
        # 暂停图标加载和处理
        pause_button = pygame.image.load("../picture/pause_button.png").convert_alpha()
        self.pause_button = pygame.transform.scale(pause_button, (30, 32))
        self.pause_rect = pause_button.get_rect()
        self.pause_rect.left, self.pause_rect.top = self.width - pause_button.get_size()[0] - 5, 0

        # 暂停页面加载和处理
        pause_page = pygame.image.load("../picture/pause_page.png").convert_alpha()
        self.pause_page = pygame.transform.scale(pause_page, (448, 302))
        # 暂停页的声音图标加载
        sound_on_pic = pygame.image.load("../picture/sound_on.png").convert_alpha()
        sound_off_pic = pygame.image.load("../picture/sound_off.png").convert_alpha()
        self.sound_on_pic = sound_on_pic.subsurface((0, 0, 96, 73))
        self.sound_off_pic = sound_off_pic.subsurface((0, 0, 96, 73))

        # 声音图标的矩形
        self.sound_rect = pygame.Rect((170, 362), (96, 73))
        # 继续开始的矩形
        self.regame_rect = pygame.Rect((110, 90 + 150), (205, 40))
        # 返回菜单的矩形
        self.remenu_rect = pygame.Rect((110, 145 + 150), (208, 45))

        # 游戏结束页面:
        over_page = pygame.image.load("../picture/game_over1.jpg").convert_alpha()
        self.over_page = pygame.transform.scale(over_page, (self.width, self.height))
        self.overremenu_rect = pygame.Rect((180, 329), (124, 33))

        # 获得时间
        self.fclock = pygame.time.Clock()

        # 自定义添加敌人事件
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 0)
        # 自定义添加玩家射击事件
        self.PLAYER_SHOOT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.PLAYER_SHOOT, 0)
        # 自定义大招充能事件
        self.CHARGE_ENERGY = pygame.USEREVENT + 3
        pygame.time.set_timer(self.CHARGE_ENERGY, 0)  # 计时器
        # 自定义飞机击毁重生的无敌事件
        self.WUDI = pygame.USEREVENT + 4
        pygame.time.set_timer(self.WUDI, 0)  # 计时器
        # warning
        self.WARNING = pygame.USEREVENT + 5
        pygame.time.set_timer(self.WARNING, 0)  # 计时器
        # 开始页面加载
        self.start_page = pygame.image.load("../picture/main_page.png").convert_alpha()
        self.screen.blit(self.start_page, (0, 0))
        # 开始游戏的矩形
        self.start_button = pygame.Rect((156, 430), (167, 50))

        # 游戏背景音乐
        pygame.mixer.set_num_channels(8)
        # 背景音乐的音量
        pygame.mixer.music.set_volume(0.6)
        # 大招音效
        self.dazhao_sound = pygame.mixer.Sound("../music/bomb_sound.ogg")
        # 子弹音效
        self.bullet_sound = pygame.mixer.Sound("../music/bullet.wav")
        # 敌机死亡音效
        self.enemydead_sound = pygame.mixer.Sound("../music/enemydead_sound.wav")
        # 游戏结束音效
        self.game_over_sound = pygame.mixer.Sound("../music/gameover_sound.ogg")

    def run(self):
        # 主循环
        while self.running:
            # 是否最小化，最小化的话游戏暂停
            if pygame.display.get_active():
                self.minsize = False
            else:
                self.minsize = True
                self.game_stop = True
                # 暂停时，背景音乐暂停
                pygame.mixer.music.pause()
            # 遍历事件，对每一个进行处理
            for event in pygame.event.get():
                # 右上角退出
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # 检测是否开始游戏
                elif event.type == MOUSEBUTTONDOWN:
                    # 游戏没开始，并且点击开始游戏的矩形
                    if not self.game_start and pygame.Rect.collidepoint(self.start_button, event.pos[0], event.pos[1]):
                        # 设置游戏开始标志为True
                        # 播放游戏背景声音
                        pygame.mixer.music.load("../music/background_sound.ogg")
                        pygame.mixer.music.play(-1)
                        # 设置游戏开始
                        self.game_start = True
                        # 得分
                        self.score = 0
                        self.n = 0
                        # 初始化玩家飞机和敌人飞机,和资源
                        self.player = Plane(self.screen, pic['plane'], dead_pic['plane'])
                        self.enemies = pygame.sprite.Group()
                        new_enemy = Enemy2(self.screen, pic['enemy-2'], dead_pic['enemy_2'], (10, -8))
                        self.enemies.add(new_enemy)
                        self.energy = pygame.sprite.Group()

                        # 初始化各种计时器
                        pygame.time.set_timer(self.ADDENEMY, 4000)
                        pygame.time.set_timer(self.PLAYER_SHOOT, 33)
                        pygame.time.set_timer(self.CHARGE_ENERGY, 5000)

                    # 检查是否暂停，当点击暂停按钮时暂停
                    if self.game_start and not self.game_stop and pygame.Rect.collidepoint(self.pause_rect, event.pos[0],
                                                                                 event.pos[1]):
                        self.game_stop = True
                        # 暂停时，背景音乐暂停
                        pygame.mixer.music.pause()

                    # 暂停页面的事件处理
                    if self.game_start and self.game_stop:
                        # 点击继续游戏
                        if pygame.Rect.collidepoint(self.regame_rect, event.pos[0], event.pos[1]):
                            self.game_stop = False
                            # 游戏从新开始，背景音乐从新开始
                            pygame.mixer.music.unpause()
                        # 点击返回主菜单
                        elif pygame.Rect.collidepoint(self.remenu_rect, event.pos[0], event.pos[1]):
                            # 全部初始化
                            self.game_start = False
                            self.game_stop = False
                            self.game_over = False
                            # 得分
                            self.score = 0
                            self.n = 0
                            # 大招是否充能完毕
                            self.can_jineng = False

                            self.player = None
                            self.enemies = None
                            self.energy = None

                            # 事件计时重置
                            pygame.time.set_timer(self.ADDENEMY, 0)
                            pygame.time.set_timer(self.PLAYER_SHOOT, 0)
                            pygame.time.set_timer(self.CHARGE_ENERGY, 0)
                            pygame.time.set_timer(self.WUDI, 0)  # 计时器
                            pygame.time.set_timer(self.WARNING, 0)  # 计时器

                        # 声音暂停和开启
                        elif pygame.Rect.collidepoint(self.sound_rect, event.pos[0], event.pos[1]):
                            if self.sound_is_on:
                                self.sound_is_on = False
                                # 全部静音
                                pygame.mixer.music.set_volume(0)
                                self.bullet_sound.set_volume(0)
                                self.enemydead_sound.set_volume(0)
                                self.dazhao_sound.set_volume(0)
                                self.game_over_sound.set_volume(0)
                            else:
                                self.sound_is_on = True
                                # 声音开启
                                pygame.mixer.music.set_volume(0.6)
                                self.bullet_sound.set_volume(0.6)
                                self.enemydead_sound.set_volume(0.6)
                                self.dazhao_sound.set_volume(0.6)
                                self.game_over_sound.set_volume(0.6)

                    # 游戏结束时返回主菜单的按钮
                    if self.game_over and pygame.Rect.collidepoint(self.overremenu_rect, event.pos[0], event.pos[1]):
                        self.game_start = False
                        self.game_stop = False
                        self.game_over = False
                        # 关闭所有声音
                        pygame.mixer.music.stop()
                        self.bullet_sound.stop()
                        self.enemydead_sound.stop()
                        self.dazhao_sound.stop()
                        self.game_over_sound.stop()
                        self.n = 0
                        # 得分
                        self.score = 0
                        # 大招是否充能完毕
                        self.can_jineng = False
                        self.player = None
                        self.enemies = None
                        self.energy = None

                        # 事件计时重置
                        pygame.time.set_timer(self.ADDENEMY, 0)
                        pygame.time.set_timer(self.PLAYER_SHOOT, 0)
                        pygame.time.set_timer(self.CHARGE_ENERGY, 0)
                        pygame.time.set_timer(self.WUDI, 0)

                # 自定义事件的检测
                # 检测是否放大招, 按空格放大招
                elif self.game_start and not self.game_stop and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.can_jineng:
                            self.dazhao_sound.play()
                            self.can_jineng = False
                            # 开始重新大招充能
                            pygame.time.set_timer(self.CHARGE_ENERGY, 5000)  # 计时器
                            # 清全图
                            # 清敌机
                            for enty in self.enemies:
                                enty.hp -= 100
                                if enty.hp >= 1:
                                    self.score += enty.grade
                                else:
                                    self.score += enty.grade * enty.total_hp
                                    enty.LIVE = False
                                    enty.kill()
                                # 清敌机子弹
                                for bullet in enty.bullets:
                                    bullet.rect.top = self.height + 100
                            # 清玩家子弹
                            for enty in self.player.bullets:
                                enty.kill()

                # 判断无敌时间是否到
                elif self.game_start and event.type == self.WUDI:
                    self.player.WUDI = False
                    # 结束无敌事件
                    pygame.time.set_timer(self.WUDI, 0)

                # 检查警告事件是否到了
                elif self.game_start and event.type == self.WARNING:
                    self.warning = False

                # 检查是否添加敌人
                elif self.game_start and not self.game_stop and event.type == self.ADDENEMY:
                    # boss的提醒
                    if self.n == len(self.order) - 1:
                        self.warning = True
                        pygame.time.set_timer(self.WARNING, 1500)
                    for i in self.order[self.n]:
                        # 调用创建敌人
                        new_enemy = EnemyFactory.make_enemies(self.screen, i)
                        self.enemies.add(new_enemy)
                    self.n += 1
                    if self.n >= len(self.order):
                        pygame.time.set_timer(self.ADDENEMY, 0)

                # 检查是否自动射击
                elif self.game_start and not self.game_stop and event.type == self.PLAYER_SHOOT:
                    if self.player.LIVE:
                        self.player.shoot()

                # 检查是否充能
                elif self.game_start and not self.game_stop and event.type == self.CHARGE_ENERGY:
                    self.can_jineng = True
                    pygame.time.set_timer(self.CHARGE_ENERGY, 0)

            # 游戏开始
            if self.game_start:
                # 碰撞检测

                # 检测玩家子弹是否击中敌机,并产生资源
                for enty in self.enemies:
                    if not enty.LIVE:
                        continue
                    # 遍历玩家的子弹
                    for bullet in self.player.bullets:
                        self.score += bullet.hurt(enty)
                        if not enty.LIVE:
                            # 调用敌机死亡的声音
                            self.enemydead_sound.play()
                            # 是否爆资源
                            if random.random() < enty.energy_rate:
                                new_energy = EnergyFactory().make_energy(self.screen, (enty.rect.left, enty.rect.top))
                                self.energy.add(new_energy)
                            if enty.kind == -5:
                                self.n = 0
                                pygame.time.set_timer(self.ADDENEMY, 3000)
                            break

                # 碰撞检测，检测敌机和敌机子弹是否碰撞玩家，判断玩家是否GG
                if not self.player.WUDI:
                    # 检查是否吃到能量
                    for enty in self.energy:
                        if pygame.Rect.colliderect(self.player.rect, enty.rect):
                            enty.supply(self.player)
                            enty.kill()
                            break
                    flag = 0
                    # 检查敌机和玩家飞机的碰撞， 判断玩家是否GG
                    for enty in self.enemies:
                        if enty.LIVE:
                            if pygame.Rect.colliderect(self.player.rect, enty.rect):
                                if self.player.hp <= 1:
                                    # 游戏结束
                                    enty.LIVE = False
                                    enty.kill()
                                    flag = 1
                                    break
                                else:
                                    flag = 2
                                break
                        # 检查敌机子弹和玩家飞机的碰撞, 判断玩家是否GG
                        for bullet in enty.bullets:
                            if pygame.Rect.colliderect(self.player.rect, bullet.rect):
                                if self.player.hp <= 0:
                                    # 游戏结束
                                    bullet.kill()
                                    flag = 1
                                else:
                                    flag = 2
                                break
                        # 玩家飞机GG
                        if flag == 1:
                            pygame.mixer.music.stop()
                            self.bullet_sound.stop()
                            self.enemydead_sound.stop()
                            self.dazhao_sound.stop()
                            # 游戏结束声音
                            self.game_over_sound.play()
                            n = 0
                            self.game_start = False
                            self.game_over = True
                            if self.score > self.high_score:
                                self.high_score = self.score
                            with open("score.txt", "w", encoding="utf-8") as f:
                                f.write(str(self.high_score))
                            # 计时器结束
                            pygame.time.set_timer(self.ADDENEMY, 0)
                            pygame.time.set_timer(self.PLAYER_SHOOT, 0)
                            pygame.time.set_timer(self.CHARGE_ENERGY, 0)
                            pygame.time.set_timer(self.WUDI, 0)  # 计时器

                        # 玩家飞机扣血
                        elif flag == 2:
                            self.player.hp -= 1
                            self.player.WUDI = True
                            self.player.LIVE = False
                            # 设置无敌事件
                            pygame.time.set_timer(self.WUDI, 1000)  # 计时器

                        if self.player.WUDI:
                            break

                # 游戏进行时，没暂停
                if not self.game_stop:
                    # 获取键盘输入表
                    pressed_keys = pygame.key.get_pressed()
                    # 更新玩家的移动
                    # if not player.WUDI:
                    self.player.update(pressed_keys)
                    # 绘制移动的background
                    self.background_index += 1
                    self.screen.blit(self.background, (0, self.background_index))
                    if self.background_index > -100:  # 重置background，从头开始
                        self.background_index = -self.background.get_size()[1] + self.height
                    # 绘制敌机和敌机子弹
                    for enty in self.enemies:
                        enty.update()
                        enty.draw()
                    # 画玩家飞机
                        self.player.draw()
                    if self.warning:
                        self.screen.blit(self.warning_pic, (150, 200))
                    # 画能量：
                    for enty in self.energy:
                        enty.update()
                        enty.draw()
                    # 绘制分数
                    self.screen.blit(self.score_pic, (5, 5))
                    self.score_surf, score_rect = self.font.render("{}".format(self.score), self.WHITE)
                    self.screen.blit(self.score_surf, (50, 8))
                    # 绘制暂停按钮
                    self.screen.blit(self.pause_button, self.pause_rect)
                    # 画血槽
                    for i in range(self.player.hp):
                        locate_w = self.width - (i + 1) * (self.hp_w + 10)
                        self.screen.blit(self.hp_pic, (locate_w, self.height - self.hp_h))
                    # 画大招
                    if self.can_jineng:
                        self.screen.blit(self.bomb_pic, (0, self.height - self.bomb_pic.get_size()[1]))
                # 暂停时绘制的内容
                else:
                    # 绘制敌机和敌机子弹
                    for enty in self.enemies:
                        # enty.update()
                        enty.draw(paused=True)
                    # 绘制玩家飞机
                    self.player.draw(paused=True)
                    # 画能量：
                    for enty in self.energy:
                        # enty.update()
                        enty.draw()
                    # 绘制分数
                    self.screen.blit(self.score_pic, (5, 5))
                    self.score_surf, score_rect = self.font.render("{}".format(self.score), self.WHITE)
                    self.screen.blit(self.score_surf, (50, 8))
                    # 画血槽
                    for i in range(self.player.hp):
                        locate_w = self.width - (i + 1) * (self.hp_w + 10)
                        self.screen.blit(self.hp_pic, (locate_w, self.height - self.hp_h))
                    # 画大招
                    if self.can_jineng:
                        self.screen.blit(self.bomb_pic, (0, self.height - self.bomb_pic.get_size()[1]))
                    # 暂停的选项
                    self.screen.blit(self.pause_page, (0, 150))
                    if self.sound_is_on:
                        self.screen.blit(self.sound_on_pic, self.sound_rect)
                    else:
                        self.screen.blit(self.sound_off_pic, self.sound_rect)
            # 游戏结束
            elif self.game_over:
                # 绘制游戏结束画面
                self.screen.blit(self.over_page, (0, 0))
                self.score_surf, score_rect = self.font.render("{}".format(self.score), self.WHITE)
                self.screen.blit(self.score_surf, (226, 195))
                self.score_surf, score_rect = self.font.render("{}".format(self.high_score), self.WHITE)
                self.screen.blit(self.score_surf, (251, 253))
            # 开始菜单
            else:
                # 绘制开始菜单
                self.screen.blit(self.start_page, (0, 0))

            pygame.display.update()
            self.fclock.tick(self.fps)

    @staticmethod
    def get_high_score(filename):
        """获得最高分"""
        high_score = 0
        try:
            with open(filename, "r", encoding="utf-8") as f:
                high_score = f.readline()
                high_score.strip()
                high_score = high_score.replace('\n', "")
                high_score = int(high_score)
                f.close()
        except FileNotFoundError:
            high_score = 0
        return high_score


if __name__ == '__main__':
    game = Game()
    game.run()