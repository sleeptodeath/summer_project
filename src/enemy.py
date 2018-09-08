# coding=utf-8
"""
敌机类：
EnemyBase: 基类
Enemy1: 敌机1
Enemy2: 敌机2
Enemy3: 敌机3
"""
import random
from planebase import *


class EnemyFactory(object):
    """子弹工产，用来生产敌机"""
    def __init__(self):
        pass
    @staticmethod
    def make_enemies(screen, kind):
        """生产敌机"""
        if kind == 1:
            new_enemy = [Enemy1(screen, pic['enemy-1'], dead_pic['enemy_1'], (0, 40)),
                         Enemy1(screen, pic['enemy-1'], dead_pic['enemy_1'], (20, 100)),
                         Enemy1(screen, pic['enemy-1'], dead_pic['enemy_1'], (40, 160)),
                         ]
        elif kind == 2:
            new_enemy = [Enemy1(screen, pic['enemy-1'], dead_pic['enemy_1'], (400, 10), (-2, 2)),
                         Enemy1(screen, pic['enemy-1'], dead_pic['enemy_1'], (380, 70), (-2, 2)),
                         Enemy1(screen, pic['enemy-1'], dead_pic['enemy_1'], (360, 130), (-2, 2))
                         ]
        elif kind == 3:
            new_enemy = Enemy2(screen, pic['enemy-2'], dead_pic['enemy_2'],
                               (random.randint(10, screen.get_size()[0] - 10), -8))
        elif kind == 4:
            new_enemy = [Enemy2(screen, pic['enemy-2'], dead_pic['enemy_2'], (0, 100), (4, 0)),
                         Enemy2(screen, pic['enemy-2'], dead_pic['enemy_2'], (200, 20), (0, 2)),
                         Enemy2(screen, pic['enemy-2'], dead_pic['enemy_2'], (400, 20), (-4, 0))]
        elif kind == 5:
            new_enemy = Enemy3(screen, pic['enemy-3'], dead_pic['enemy_3'],
                               (random.randint(10, screen.get_size()[0] - 10), -8))
        elif kind == 6:
            new_enemy = Enemy4(screen, pic['enemy-4'], dead_pic['enemy_4'],
                               (random.randint(10, screen.get_size()[0] - 10), -8))
        elif kind == 7:
            new_enemy = [Enemy3(screen, pic['enemy-3'], dead_pic['enemy_3'], (60, -8)),
                         Enemy3(screen, pic['enemy-3'], dead_pic['enemy_3'], (320, -8))
                         ]
        elif kind == 999:
            new_enemy = Enemy5(screen, pic['enemy-5'], dead_pic['enemy_5'], (60, -8))

        return new_enemy


class EnemyBase(PlaneBase):
    """敌机的基类"""
    def __init__(self, screen, img_name, dead_img_list, pos):
        """构造函数， 初始化
        screen:
        pos：
        img_name:
        deal_img_list:
        """
        # 调用父类构造函数
        PlaneBase.__init__(self, screen, img_name, dead_img_list)
        # 爆率
        self.energy_rate = 0.1
        # 被击败时的分数
        self.grade = 0
        # 当前血量
        self.hp = 1
        # 总的血量
        self.total_hp = 1
        # 种类, 用来标记不同的飞机
        self.kind = 1
        # 用来改变射击频率的计数
        self.hz_cnt = 1

        # 设置初始位置
        self.x, self.y = pos[0], pos[1]
        self.rect.left, self.rect.top = self.x, self.y

        # 设置速度
        self.speed_x = 1
        self.speed_y = 1
        # 血条设置
        self.blood = pygame.image.load("../picture/blood_bar.png")
        self.blood = pygame.transform.scale(self.blood, (self.img.get_size()[0], 8))
        self.blood_cur = self.blood

    def collision(self):
        """检查敌机是否碰到四周， 如果敌机到达最下方则删除"""
        if self.rect.right > self.screen_w:
            self.rect.right = self.screen_w
            self.speed_x = -self.speed_x
        elif self.rect.left < 0:
            self.rect.left = 0
            self.speed_x = -self.speed_x
        if self.rect.bottom > self.screen_h:
            # 删除
            self.kill()

    def dead(self):
        """死亡动画绘制完后"""
        self.dead_index -= 1
        # 爆炸动画绘制结束， 改为不可见
        self.VISIBLE = False

    def be_attacked(self):
        """飞机被玩家子弹击中时调用，
            return 相应的分数
        """
        if self.hp <= 1: # 没有血了。GG
            self.hp -= 1
            self.LIVE = False
            return self.grade * self.total_hp
        else:
            self.hp -= 1
            return self.grade

    def draw_blood(self):
        """血条绘制"""
        w = self.hp / self.total_hp * self.blood.get_size()[0]
        self.blood_cur = self.blood.subsurface(pygame.Rect(0, 0, int(w), 8))
        self.screen.blit(self.blood_cur, (self.rect.left, self.rect.top - 8))


class Enemy1(EnemyBase):
    """敌机1"""
    def __init__(self, screen, img_name, deal_img_list, pos, speed=(2, 2)):
        """构造函数"""
        EnemyBase.__init__(self, screen, img_name, deal_img_list, pos)
        # 爆率
        self.energy_rate = 0.05
        # 被击败时的分数
        self.grade = 1
        # 血量
        self.hp = 8
        # 飞机总的血量
        self.total_hp = 8
        # 种类, 用来标记不同的飞机
        self.kind = -1

        self.rect.left, self.rect.top = self.x, self.y
        # 设置速度
        self.speed_x = speed[0]
        self.speed_y = speed[1]

    def deal_img(self, img_name):
        img = pygame.image.load(img_name)
        img = img.subsurface(pygame.Rect(44, 49, 116, 90))
        img = pygame.transform.scale(img, (img.get_size()[0] // 2, img.get_size()[1] // 2))
        return img

    def update(self):
        """敌机移动， 具体移动方式，
        左右摇摆"""
        if self.rect.top < 0:
            self.rect.move_ip(0, 10)
        else:
            self.rect.move_ip(self.speed_x, self.speed_y)
        self.collision()

    def shoot_hz(self):
        """射击频率， """
        if self.hz_cnt % 400 == 0 or self.hz_cnt == 2 or self.hz_cnt == 10:
            self.shoot()
        self.hz_cnt += 1
        if self.hz_cnt > 770:
            self.hz_cnt = 1

    def daiding(self):
        """绘制血量"""
        self.screen.blit(self.tail, (self.rect.left + self.img.get_size()[0] // 4, self.rect.top-self.img.get_size()[0] // 3))
        self.draw_blood()

    def shoot(self):
        """具体的射击方式， 什么子弹等等"""
        new_bullet = self.bullet_factory.\
            make_bullet(self.screen, (self.rect.left, self.rect.bottom),
                        self.img.get_size(), self.kind)
        self.bullets.add(new_bullet)


class Enemy2(EnemyBase):
    """敌机2"""
    def __init__(self, screen, img_name, deal_img_list, pos, speed=(0, 2)):
        """fda"""
        EnemyBase.__init__(self, screen, img_name, deal_img_list, pos)
        # 爆率
        self.energy_rate = 0.1
        # 被击败时的分数
        self.grade = 3
        # 血量
        self.hp = 18
        self.total_hp = 18
        # 种类
        self.kind = -2

        self.x, self.y = random.randint(10, self.screen_w), -2
        self.rect.left, self.rect.top = self.x, self.y
        # 设置速度
        self.speed_x = 0
        self.speed_y = 2

    def deal_img(self, img_name):
        img = pygame.image.load(img_name)
        img = img.subsurface(pygame.Rect(7, 21, 184, 140))
        img = pygame.transform.scale(img, (img.get_size()[0] // 2, img.get_size()[1] // 2))
        return img

    def update(self):
        """敌机移动"""
        if self.rect.top < 0:
            self.rect.move_ip(0, 10)
        else:
            self.rect.move_ip(self.speed_x, self.speed_y)
        self.collision()

    def daiding(self):
        """绘制血量"""
        self.screen.blit(self.tail, (self.rect.left + self.img.get_size()[0] // 4, self.rect.top-self.img.get_size()[0] // 4))
        self.draw_blood()

    def shoot_hz(self):
        """射击频率， """
        if self.hz_cnt % 400 == 0 or self.hz_cnt == 2 or self.hz_cnt == 40:
            self.shoot()
        self.hz_cnt += 1
        if self.hz_cnt > 770:
            self.hz_cnt = 1

    def shoot(self):
        """具体的射击方式， 什么子弹等等"""
        new_bullet = self.bullet_factory.\
            make_bullet(self.screen, (self.rect.left, self.rect.bottom),
                        self.img.get_size(), self.kind)
        self.bullets.add(new_bullet)


class Enemy3(EnemyBase):
    """敌机3"""
    def __init__(self, screen, img_name, deal_img_list, pos):
        """构造函数"""
        EnemyBase.__init__(self, screen, img_name, deal_img_list, pos)
        # 爆率
        self.energy_rate = 0.3
        # 被击败时的分数
        self.grade = 5
        # 血量
        self.hp = 80
        self.total_hp = 80
        # 种类
        self.kind = -3

        self.x, self.y = random.randint(10, self.screen_w), -2
        self.rect.left, self.rect.top = self.x, self.y
        # 设置速度
        self.speed_x = 1
        self.speed_y = 0

    def deal_img(self, img_name):
        img = pygame.image.load(img_name)
        img = img.subsurface(pygame.Rect(0, 58, 199, 110))
        img = pygame.transform.scale(img, (img.get_size()[0] // 2, img.get_size()[1] // 2))
        return img

    def update(self):
        """敌机移动"""
        if self.rect.top < 0:
            self.rect.move_ip(0, 10)
        else:
            self.rect.move_ip(self.speed_x, self.speed_y)
        self.collision()

    def shoot_hz(self):
        """射击频率， """
        self.hz_cnt += 1
        if self.hz_cnt % 25 == 0 and self.hz_cnt < 400:
            self.shoot()
        if self.hz_cnt > 700:
            self.hz_cnt = 1

    def daiding(self):
        """绘制血量"""
        self.screen.blit(self.tail, (self.rect.left + self.img.get_size()[0] // 4, self.rect.top-self.img.get_size()[0] // 4))
        self.draw_blood()

    def shoot(self):
        """具体的射击方式， 什么子弹等等"""
        new_bullet = self.bullet_factory.\
            make_bullet(self.screen, (self.rect.left, self.rect.bottom),
                        self.img.get_size(), self.kind)
        self.bullets.add(new_bullet)


class Enemy4(EnemyBase):
    """敌机3"""
    def __init__(self, screen, img_name, deal_img_list, pos):
        """构造函数"""
        EnemyBase.__init__(self, screen, img_name, deal_img_list, pos)
        # 爆率
        self.energy_rate = 0.2
        # 被击败时的分数
        self.grade = 3
        # 血量
        self.hp = 50
        self.total_hp = 50
        # 种类
        self.kind = -4

        self.x, self.y = random.randint(10, self.screen_w), -2
        self.rect.left, self.rect.top = self.x, self.y
        # 设置速度
        self.speed_x = 0
        self.speed_y = 2

    def deal_img(self, img_name):
        img = pygame.image.load(img_name)
        img = img.subsurface(pygame.Rect(0, 40, 199, 130))
        img = pygame.transform.scale(img, (img.get_size()[0] // 2, img.get_size()[1] // 2))
        return img

    def update(self):
        """敌机移动"""
        if self.rect.top < 0:
            self.rect.move_ip(0, 10)
        else:
            self.rect.move_ip(self.speed_x, self.speed_y)
        self.collision()

    def shoot_hz(self):
        """射击频率， """
        self.hz_cnt += 1
        if self.hz_cnt % 25 == 0 and self.hz_cnt < 400:
            self.shoot()
        if self.hz_cnt > 700:
            self.hz_cnt = 1

    def daiding(self):
        """绘制血量"""
        self.screen.blit(self.tail, (self.rect.left + self.img.get_size()[0] // 4, self.rect.top-self.img.get_size()[0] // 4))
        self.draw_blood()

    def shoot(self):
        """具体的射击方式， 什么子弹等等"""
        new_bullet = self.bullet_factory.\
            make_bullet(self.screen, (self.rect.left, self.rect.bottom),
                        self.img.get_size(), self.kind)
        self.bullets.add(new_bullet)


class Enemy5(EnemyBase):
    """敌机3"""
    def __init__(self, screen, img_name, deal_img_list, pos):
        """构造函数"""
        EnemyBase.__init__(self, screen, img_name, deal_img_list, pos)
        # 爆率
        self.energy_rate = 1
        # 被击败时的分数
        self.grade = 5
        # 血量
        self.hp = 800
        self.total_hp = 800
        # 种类
        self.kind = -5

        self.x, self.y = random.randint(10, self.screen_w), -2
        self.rect.left, self.rect.top = self.x, self.y
        # 设置速度
        self.speed_x = 2
        self.speed_y = 0

    def deal_img(self, img_name):
        img = pygame.image.load(img_name).convert_alpha()
        # img = img.subsurface(pygame.Rect(0, 40, 199, 130))
        img = pygame.transform.scale(img, (img.get_size()[0] // 2, img.get_size()[1] // 2))
        return img

    def update(self):
        """敌机移动"""
        if self.rect.top < 0:
            self.rect.move_ip(0, 10)
        else:
            self.rect.move_ip(self.speed_x, self.speed_y)
        self.collision()

    def shoot_hz(self):
        """射击频率， """
        self.hz_cnt += 1
        if self.hz_cnt % 25 == 0 and self.hz_cnt < 250:
            self.shoot(-5)
        if self.hz_cnt > 250 and self.hz_cnt % 20 == 0:
            self.shoot(-6)
        if self.hz_cnt > 900:
            self.hz_cnt = 1

    def daiding(self):
        """绘制血量"""
        self.screen.blit(self.tail, (self.rect.left + self.img.get_size()[0] // 4, self.rect.top-self.img.get_size()[0] // 4))
        self.draw_blood()

    def shoot(self, kind=0):
        """具体的射击方式， 什么子弹等等"""
        new_bullet = self.bullet_factory.\
            make_bullet(self.screen, (self.rect.left, self.rect.bottom),
                        self.img.get_size(), kind)
        self.bullets.add(new_bullet)
