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

order = [(1, ), (2, ), (1, ), (2,), (3, 3), (1, 3), (2, 3), (2, 1), (4, ), (6, 1), (5, 3), (1, 2, 4), (4, 5), (3, 7), (6, 1, 2),
         (999, )]

# order = [(1, ), (2, ), (1, ), (999, )]

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


def display():
    pass


def main():
    """主函数"""
    n = 0
    # pygame初始化
    pygame.init()
    pygame.mixer.init()

    # 设置尺寸参数
    size = (width, height) = (448, 650)
    # 初始化窗口
    screen = pygame.display.set_mode(size)
    # 背景图片加载
    background = pygame.image.load("../picture/background.png").convert()
    background_index = -background.get_size()[1] + height
    # 设置标题
    pygame.display.set_caption("飞机大战")
    # 设置icon
    icon = pygame.image.load("../picture/icon.png").convert_alpha()
    pygame.display.set_icon(icon)

    # 主循环标志
    running = True
    # 游戏是否开始标志
    game_start = False
    # 游戏是否暂停
    game_stop = False
    # 游戏结束标志
    game_over = False
    # 大招是否充能完毕
    can_jineng = False
    # 是否开启声音
    sound_is_on = True
    # 帧率
    fps = 30
    # 得分
    score = 0
    # 获得最高分
    file_name = "score.txt"
    high_score = get_high_score(file_name)
    # boss提示
    warning = False
    # 是否最小化
    minsize = False

    # 玩家
    player = None
    # 敌机组
    enemies = None
    # 资源组s
    energy = None

    # 设置字体
    font = pygame.freetype.Font("../font/msyh.ttc", 26)
    WHITE = (255, 255, 255)

    # 得分图片加载
    score_pic = pygame.image.load("../picture/score.png").convert_alpha()
    score_pic = pygame.transform.scale(score_pic, (40, 30))
    # 分数文字
    score_surf, score_rect = font.render("{}".format(score), WHITE)

    # 大招图标加载和处理
    bomb_pic = pygame.image.load("../picture/jineng_2.png").convert_alpha()
    b_w, b_h = bomb_pic.get_size()
    bomb_pic = pygame.transform.scale(bomb_pic, (80, 56))

    # 玩家hp图标加载和处理
    hp_pic = pygame.image.load(pic['plane'][0]).convert_alpha()
    hp_pic = pygame.transform.scale(hp_pic, (40, 40))
    hp_w, hp_h = hp_pic.get_size()
    # 警告
    warning_pic = pygame.image.load(pic['warning']).convert_alpha()
    # 暂停图标加载和处理
    pause_button = pygame.image.load("../picture/pause_button.png").convert_alpha()
    pause_button = pygame.transform.scale(pause_button, (30, 32))
    pause_rect = pause_button.get_rect()
    pause_rect.left, pause_rect.top = width - pause_button.get_size()[0] - 5, 0

    # 暂停页面加载和处理
    pause_page = pygame.image.load("../picture/pause_page.png").convert_alpha()
    pause_page = pygame.transform.scale(pause_page, (448, 302))
    # 暂停页的声音图标加载
    sound_on_pic = pygame.image.load("../picture/sound_on.png").convert_alpha()
    sound_off_pic = pygame.image.load("../picture/sound_off.png").convert_alpha()
    sound_on_pic = sound_on_pic.subsurface((0, 0, 96, 73))
    sound_off_pic = sound_off_pic.subsurface((0, 0, 96, 73))

    # 声音图标的矩形
    sound_rect = pygame.Rect((170, 362), (96, 73))
    # 继续开始的矩形
    regame_rect = pygame.Rect((110, 90 + 150), (205, 40))
    # 返回菜单的矩形
    remenu_rect = pygame.Rect((110, 145 + 150), (208, 45))

    # 游戏结束页面:
    over_page = pygame.image.load("../picture/game_over1.jpg").convert_alpha()
    over_page = pygame.transform.scale(over_page, (width, height))
    overremenu_rect = pygame.Rect((180, 329), (124, 33))

    # 获得时间
    fclock = pygame.time.Clock()

    # 自定义添加敌人事件
    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 0)
    # 自定义添加玩家射击事件
    PLAYER_SHOOT = pygame.USEREVENT + 2
    pygame.time.set_timer(PLAYER_SHOOT, 0)
    # 自定义大招充能事件
    CHARGE_ENERGY = pygame.USEREVENT + 3
    pygame.time.set_timer(CHARGE_ENERGY, 0)  # 计时器
    # 自定义飞机击毁重生的无敌事件
    WUDI = pygame.USEREVENT + 4
    pygame.time.set_timer(WUDI, 0)  # 计时器
    # warning
    WARNING = pygame.USEREVENT + 5
    pygame.time.set_timer(WARNING, 0)  # 计时器
    # 开始页面加载
    start_page = pygame.image.load("../picture/main_page.png").convert_alpha()
    screen.blit(start_page, (0, 0))
    # 开始游戏的矩形
    start_button = pygame.Rect((156, 430), (167, 50))

    # 游戏背景音乐
    pygame.mixer.set_num_channels(8)
    # 背景音乐的音量
    pygame.mixer.music.set_volume(0.6)
    # 大招音效
    dazhao_sound = pygame.mixer.Sound("../music/bomb_sound.ogg")
    # 子弹音效
    bullet_sound = pygame.mixer.Sound("../music/bullet.wav")
    # 敌机死亡音效
    enemydead_sound = pygame.mixer.Sound("../music/enemydead_sound.wav")
    # 游戏结束音效
    game_over_sound = pygame.mixer.Sound("../music/gameover_sound.ogg")

    # 主循环
    while running:
        # 是否最小化，最小化的话游戏暂停
        if pygame.display.get_active():
            minsize = False
        else:
            minsize = True
            game_stop = True
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
                if not game_start and pygame.Rect.collidepoint(start_button, event.pos[0], event.pos[1]):
                    # 设置游戏开始标志为True
                    # 播放游戏背景声音
                    pygame.mixer.music.load("../music/background_sound.ogg")
                    pygame.mixer.music.play(-1)
                    # 设置游戏开始
                    game_start = True
                    # 得分
                    score = 0
                    n = 0
                    # 初始化玩家飞机和敌人飞机,和资源
                    player = Plane(screen, pic['plane'], dead_pic['plane'])
                    enemies = pygame.sprite.Group()
                    new_enemy = Enemy2(screen, pic['enemy-2'], dead_pic['enemy_2'], (10, -8))
                    enemies.add(new_enemy)
                    energy = pygame.sprite.Group()

                    # 初始化各种计时器
                    pygame.time.set_timer(ADDENEMY, 4000)
                    pygame.time.set_timer(PLAYER_SHOOT, 33)
                    pygame.time.set_timer(CHARGE_ENERGY, 5000)

                # 检查是否暂停，当点击暂停按钮时暂停
                if game_start and not game_stop and pygame.Rect.collidepoint(pause_rect, event.pos[0], event.pos[1]):
                        game_stop = True
                        # 暂停时，背景音乐暂停
                        pygame.mixer.music.pause()

                # 暂停页面的事件处理
                if game_start and game_stop:
                    # 点击继续游戏
                    if pygame.Rect.collidepoint(regame_rect, event.pos[0], event.pos[1]):
                        game_stop = False
                        # 游戏从新开始，背景音乐从新开始
                        pygame.mixer.music.unpause()
                    # 点击返回主菜单
                    elif pygame.Rect.collidepoint(remenu_rect, event.pos[0], event.pos[1]):
                        # 全部初始化
                        game_start = False
                        game_stop = False
                        game_over = False
                        # 得分
                        score = 0
                        n = 0
                        # 大招是否充能完毕
                        can_jineng = False

                        player = None
                        enemies = None
                        energy = None

                        # 事件计时重置
                        pygame.time.set_timer(ADDENEMY, 0)
                        pygame.time.set_timer(PLAYER_SHOOT, 0)
                        pygame.time.set_timer(CHARGE_ENERGY, 0)
                        pygame.time.set_timer(WUDI, 0)  # 计时器
                        pygame.time.set_timer(WARNING, 0)  # 计时器

                    # 声音暂停和开启
                    elif pygame.Rect.collidepoint(sound_rect, event.pos[0], event.pos[1]):
                        if sound_is_on:
                            sound_is_on = False
                            # 全部静音
                            pygame.mixer.music.set_volume(0)
                            bullet_sound.set_volume(0)
                            enemydead_sound.set_volume(0)
                            dazhao_sound.set_volume(0)
                            game_over_sound.set_volume(0)
                        else:
                            sound_is_on = True
                            # 声音开启
                            pygame.mixer.music.set_volume(0.6)
                            bullet_sound.set_volume(0.6)
                            enemydead_sound.set_volume(0.6)
                            dazhao_sound.set_volume(0.6)
                            game_over_sound.set_volume(0.6)

                # 游戏结束时返回主菜单的按钮
                if game_over and pygame.Rect.collidepoint(overremenu_rect, event.pos[0], event.pos[1]):
                    game_start = False
                    game_stop = False
                    game_over = False
                    # 关闭所有声音
                    pygame.mixer.music.stop()
                    bullet_sound.stop()
                    enemydead_sound.stop()
                    dazhao_sound.stop()
                    game_over_sound.stop()
                    n = 0
                    # 得分
                    score = 0
                    # 大招是否充能完毕
                    can_jineng = False
                    player = None
                    enemies = None
                    energy = None

                    # 事件计时重置
                    pygame.time.set_timer(ADDENEMY, 0)
                    pygame.time.set_timer(PLAYER_SHOOT, 0)
                    pygame.time.set_timer(CHARGE_ENERGY, 0)
                    pygame.time.set_timer(WUDI, 0)

            # 自定义事件的检测
            # 检测是否放大招, 按空格放大招
            elif game_start and not game_stop and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if can_jineng:
                        dazhao_sound.play()
                        can_jineng = False
                        # 开始重新大招充能
                        pygame.time.set_timer(CHARGE_ENERGY, 5000)  # 计时器
                        # 清全图
                        # 清敌机
                        for enty in enemies:
                            enty.hp -= 100
                            if enty.hp >= 1:
                                score += enty.grade
                            else:
                                score += enty.grade * enty.total_hp
                                enty.LIVE = False
                                enty.kill()
                            # 清敌机子弹
                            for bullet in enty.bullets:
                                bullet.rect.top = height + 100
                        # 清玩家子弹
                        for enty in player.bullets:
                            enty.kill()

            # 判断无敌时间是否到
            elif game_start and event.type == WUDI:
                player.WUDI = False
                # 结束无敌事件
                pygame.time.set_timer(WUDI, 0)

            # 检查警告事件是否到了
            elif game_start and event.type == WARNING:
                warning = False

            # 检查是否添加敌人
            elif game_start and not game_stop and event.type == ADDENEMY:
                # boss的提醒
                if n == len(order) - 1:
                    warning = True
                    pygame.time.set_timer(WARNING, 1500)
                for i in order[n]:
                    # 调用创建敌人
                    new_enemy = EnemyFactory.make_enemies(screen, i)
                    enemies.add(new_enemy)
                n += 1
                if n >= len(order):
                    pygame.time.set_timer(ADDENEMY, 0)

            # 检查是否自动射击
            elif game_start and not game_stop and event.type == PLAYER_SHOOT:
                if player.LIVE:
                    player.shoot()

            # 检查是否充能
            elif game_start and not game_stop and event.type == CHARGE_ENERGY:
                can_jineng = True
                pygame.time.set_timer(CHARGE_ENERGY, 0)

        # 游戏开始
        if game_start:
            # 碰撞检测

            # 检测玩家子弹是否击中敌机,并产生资源
            for enty in enemies:
                if not enty.LIVE:
                    continue
                # 遍历玩家的子弹
                for bullet in player.bullets:
                    score += bullet.hurt(enty)
                    if not enty.LIVE:
                        # 调用敌机死亡的声音
                        enemydead_sound.play()
                        # 是否爆资源
                        if random.random() < enty.energy_rate:
                            new_energy = EnergyFactory().make_energy(screen, (enty.rect.left, enty.rect.top))
                            energy.add(new_energy)
                        if enty.kind == -5:
                            n = 0
                            pygame.time.set_timer(ADDENEMY, 3000)
                        break

            # 碰撞检测，检测敌机和敌机子弹是否碰撞玩家，判断玩家是否GG
            if not player.WUDI:
                # 检查是否吃到能量
                for enty in energy:
                    if pygame.Rect.colliderect(player.rect, enty.rect):
                        enty.supply(player)
                        enty.kill()
                        break
                flag = 0
                # 检查敌机和玩家飞机的碰撞， 判断玩家是否GG
                for enty in enemies:
                    if enty.LIVE:
                        if pygame.Rect.colliderect(player.rect, enty.rect):
                            if player.hp <= 1:
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
                        if pygame.Rect.colliderect(player.rect, bullet.rect):
                            if player.hp <= 0:
                                # 游戏结束
                                bullet.kill()
                                flag = 1
                            else:
                                flag = 2
                            break
                    # 玩家飞机GG
                    if flag == 1:
                        pygame.mixer.music.stop()
                        bullet_sound.stop()
                        enemydead_sound.stop()
                        dazhao_sound.stop()
                        # 游戏结束声音
                        game_over_sound.play()
                        n = 0
                        game_start = False
                        game_over = True
                        if score > high_score:
                            high_score = score
                        with open("score.txt", "w", encoding="utf-8") as f:
                            f.write(str(high_score))
                        # 计时器结束
                        pygame.time.set_timer(ADDENEMY, 0)
                        pygame.time.set_timer(PLAYER_SHOOT, 0)
                        pygame.time.set_timer(CHARGE_ENERGY, 0)
                        pygame.time.set_timer(WUDI, 0)  # 计时器

                    # 玩家飞机扣血
                    elif flag == 2:
                        player.hp -= 1
                        player.WUDI = True
                        player.LIVE = False
                        # 设置无敌事件
                        pygame.time.set_timer(WUDI, 1000)  # 计时器

                    if player.WUDI:
                        break

            # 游戏进行时，没暂停
            if not game_stop:
                # 获取键盘输入表
                pressed_keys = pygame.key.get_pressed()
                # 更新玩家的移动
                # if not player.WUDI:
                player.update(pressed_keys)
                # 绘制移动的background
                background_index += 1
                screen.blit(background, (0, background_index))
                if background_index > -100:  # 重置background，从头开始
                    background_index = -background.get_size()[1] + height
                # 绘制敌机和敌机子弹
                for enty in enemies:
                    enty.update()
                    enty.draw()
                # 画玩家飞机
                player.draw()
                if warning:
                    screen.blit(warning_pic, (150, 200))
                # 画能量：
                for enty in energy:
                    enty.update()
                    enty.draw()
                # 绘制分数
                screen.blit(score_pic, (5, 5))
                score_surf, score_rect = font.render("{}".format(score), WHITE)
                screen.blit(score_surf, (50, 8))
                # 绘制暂停按钮
                screen.blit(pause_button, pause_rect)
                # 画血槽
                for i in range(player.hp):
                    locate_w = width - (i+1) * (hp_w + 10)
                    screen.blit(hp_pic, (locate_w, height - hp_h))
                # 画大招
                if can_jineng:
                    screen.blit(bomb_pic, (0, height - bomb_pic.get_size()[1]))
            # 暂停时绘制的内容
            else:
                # 绘制敌机和敌机子弹
                for enty in enemies:
                    # enty.update()
                    enty.draw(paused=True)
                # 绘制玩家飞机
                player.draw(paused=True)
                # 画能量：
                for enty in energy:
                    # enty.update()
                    enty.draw()
                # 绘制分数
                screen.blit(score_pic, (5, 5))
                score_surf, score_rect = font.render("{}".format(score), WHITE)
                screen.blit(score_surf, (50, 8))
                # 画血槽
                for i in range(player.hp):
                    locate_w = width - (i + 1) * (hp_w + 10)
                    screen.blit(hp_pic, (locate_w, height - hp_h))
                # 画大招
                if can_jineng:
                    screen.blit(bomb_pic, (0, height - bomb_pic.get_size()[1]))
                # 暂停的选项
                screen.blit(pause_page, (0, 150))
                if sound_is_on:
                    screen.blit(sound_on_pic, sound_rect)
                else:
                    screen.blit(sound_off_pic, sound_rect)
        # 游戏结束
        elif game_over:
            # 绘制游戏结束画面
            screen.blit(over_page, (0, 0))
            score_surf, score_rect = font.render("{}".format(score), WHITE)
            screen.blit(score_surf, (226, 195))
            score_surf, score_rect = font.render("{}".format(high_score), WHITE)
            screen.blit(score_surf, (251, 253))
        # 开始菜单
        else:
            # 绘制开始菜单
            screen.blit(start_page, (0, 0))

        pygame.display.update()
        fclock.tick(fps)


if __name__ == '__main__':
    # gogogo
    main()
