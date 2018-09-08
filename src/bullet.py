# coding=utf-8
"""
子弹类的集合
玩家子弹：
    Bullet
    Bullet1
    Bullet2
敌机子弹：
    EnemyBullet1
    EnemyBullet2
    EnemyBullet3
"""
import pygame
from pygame.locals import *
from source import *


class BulletFactory(object):
    """子弹工产，用来生产子弹"""
    def __init__(self):
        pass

    def make_bullet(self, screen, pos, plane_size, kind):
        """根据不同的飞机类型，创建子弹"""
        # level1
        if kind == 1:
            return [Bullet(screen, (pos[0] + plane_size[0]//2 - 10, pos[1] + 5), pic['bullet-1'], plane_size)]
        # level2
        elif kind == 2:
            return [Bullet(screen, (pos[0], pos[1] + 5), pic['bullet-1'], plane_size),
                    Bullet(screen, (pos[0] + plane_size[0] - 10, pos[1] + 5), pic['bullet-1'], plane_size)]
        # level3
        elif kind == 3:
            return [Bullet1(screen, (pos[0], pos[1] + 5), pic['bullet-1'], plane_size, (-3, 13)),
                    Bullet(screen, (pos[0] + plane_size[0] // 2 - 10, pos[1] + 5), pic['bullet-1'], plane_size),
                    Bullet1(screen, (pos[0] + plane_size[0] - 20, pos[1] + 5), pic['bullet-1'], plane_size, (3, 13))]
        # # level5
        # elif kind == 4:
        #     return [Bullet2(screen, (pos[0], pos[1] + 5), pic['bullet-3'], plane_size)]
        # level6
        elif kind == 4:
            return [Bullet2(screen, (pos[0] - 16, pos[1] + 5), pic['bullet-3'], plane_size),
                    Bullet2(screen, (pos[0] + plane_size[1] - 16, pos[1] + 5), pic['bullet-3'], plane_size)]
        # level7
        elif kind == 5:
            return [Bullet2(screen, (pos[0] - 16, pos[1] + 5), pic['bullet-3'], plane_size),
                    Bullet2(screen, (pos[0] + plane_size[1] // 2, pos[1] + 5), pic['bullet-3'], plane_size),
                    Bullet(screen, (pos[0] - 10, pos[1] + 15), pic['bullet-1'], plane_size),
                    Bullet(screen, (pos[0] + plane_size[1] + 10, pos[1] + 15), pic['bullet-1'], plane_size)
                    ]
        # enemy_1
        elif kind == -1:
            return EnemyBullet1(screen, (pos[0] + plane_size[0]//2 - 10, pos[1] - 5), pic['bullet-2'], plane_size)
        # enemy_2
        elif kind == -2:
            return [EnemyBullet2(screen, (pos[0] + 20, pos[1] - 10), pic['bullet-2'], plane_size),
                    EnemyBullet2(screen, (pos[0] + plane_size[0] - 30, pos[1] - 10), pic['bullet-2'], plane_size)]
        # enemy_3
        elif kind == -3:
            return [EnemyBullet3(screen, (pos[0] + plane_size[0] // 2, pos[1] - 2), pic['bullet-2'], plane_size)
                    ]

        elif kind == -4:
            return [EnemyBullet2(screen, (pos[0] + plane_size[0] // 2, pos[1] - 2), pic['bullet-2'], plane_size),
                    EnemyBullet4(screen, (pos[0] + plane_size[0] - 10, pos[1] - 5), pic['bullet-2'], plane_size, (3, 6)),
                    EnemyBullet4(screen, (pos[0] + 10, pos[1] - 5), pic['bullet-2'], plane_size, (-3, 6))]

        elif kind == -5:
            return [EnemyBullet2(screen, (pos[0] + plane_size[0] // 2, pos[1] - 2), pic['bullet-2'], plane_size),
                    EnemyBullet4(screen, (pos[0] + plane_size[0] - 10, pos[1] - 5), pic['bullet-2'], plane_size, (3, 6)),
                    EnemyBullet4(screen, (pos[0] + 10, pos[1] - 5), pic['bullet-2'], plane_size, (-3, 6)),
                    EnemyBullet4(screen, (pos[0] + plane_size[0] - 35, pos[1] - 5), pic['bullet-2'], plane_size, (3, 6)),
                    EnemyBullet4(screen, (pos[0] + 25, pos[1] - 5), pic['bullet-2'], plane_size, (-3, 6)),

                    EnemyBullet2(screen, (pos[0] + plane_size[0] // 2, pos[1] + 22), pic['bullet-2'], plane_size),
                    EnemyBullet4(screen, (pos[0] + plane_size[0] - 10, pos[1] + 25), pic['bullet-2'], plane_size,
                                 (3, 6)),
                    EnemyBullet4(screen, (pos[0] + 10, pos[1] - 5), pic['bullet-2'], plane_size, (-3, 6)),
                    EnemyBullet4(screen, (pos[0] + plane_size[0] - 35, pos[1] + 25), pic['bullet-2'], plane_size,
                                 (3, 6)),
                    EnemyBullet4(screen, (pos[0] + 25, pos[1] + 25), pic['bullet-2'], plane_size, (-3, 6))]


        elif kind == -6:
            return [EnemyBullet3(screen, (pos[0] + plane_size[0] // 2, pos[1] - 2), pic['bullet-2'], plane_size),
                    EnemyBullet3(screen, (pos[0] + plane_size[0] // 2, pos[1] + 18), pic['bullet-2'], plane_size),
                    EnemyBullet3(screen, (pos[0] + plane_size[0] // 2 - 18, pos[1] - 2), pic['bullet-2'], plane_size),
                    EnemyBullet3(screen, (pos[0] + plane_size[0] // 2 - 18, pos[1] + 18), pic['bullet-2'], plane_size),
                    EnemyBullet3(screen, (pos[0] + plane_size[0] // 2 - 36, pos[1] - 2), pic['bullet-2'], plane_size),
                    EnemyBullet3(screen, (pos[0] + plane_size[0] // 2 - 36, pos[1] + 18), pic['bullet-2'], plane_size),
                    EnemyBullet3(screen, (pos[0] + plane_size[0] // 2 - 36, pos[1] + 42), pic['bullet-2'], plane_size),
                    EnemyBullet3(screen, (pos[0] + plane_size[0] // 2 - 18, pos[1] + 42), pic['bullet-2'], plane_size),
                    ]


class BulletBase(pygame.sprite.Sprite):
    """子弹的基类

    __init__(self, screen, pos, img_name)
    collision(self):
    draw(self):
    deal_img(img_name):
    """
    def __init__(self, screen, pos, img_name):
        super().__init__()
        """
        构造函数
        screen: pygame的主窗口
        pos： 子弹开始绘制坐标
        img_name: 子弹对应的图片
        """
        # pygame的主窗口
        self.screen = screen
        self.screen_w, self.screen_h = self.screen.get_size()
        # 加载子弹对应图像
        self.img = self.deal_img(img_name)
        # 获得敌机图像对应的矩形
        self.rect = self.img.get_rect()
        # 设置初始位置
        self.x = pos[0]
        self.y = pos[1]
        self.rect.left, self.rect.top = self.x, self.y

        # 设置移动速度
        self.speed_x = 0
        self.speed_y = 0

    def collision(self):
        """检查子弹是否碰到四周， 如果子弹到达最下方则删除"""
        if self.rect.right > self.screen_w - 10:
            self.rect.right = self.screen_w - 10
            self.speed_x = -self.speed_x
        if self.rect.left < 10:
            self.rect.left = 10
            self.speed_x = -self.speed_x
        if self.rect.bottom > self.screen_h:
            # 删除
            self.kill()

    def draw(self):
        """子弹绘制"""
        self.screen.blit(self.img, self.rect)

    def deal_img(self, img_name):
        """子弹的图片处理"""
        pass
        # return pygame.image.load(img_name).convert_alpha()


class Bullet(BulletBase):
    """最基础的子弹，直线"""
    def __init__(self, screen, pos, img_name, plane_size):
        BulletBase.__init__(self, screen, pos, img_name)
        # 子弹移动的速度
        self.speed = 13

    def update(self):
        """子弹移动"""
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill()

    def hurt(self, enemy):
        """子弹击中敌机"""
        if pygame.Rect.colliderect(self.rect, enemy.rect):
            self.kill()
            # 调用敌机的被攻击方法
            return enemy.be_attacked()
        return 0

    def deal_img(self, img_name):
        """子弹的图片处理"""
        img = pygame.image.load(img_name).convert_alpha()
        img = pygame.transform.scale(img, (15, 15))
        return img


class Bullet1(BulletBase):
    """子弹类型2，能左右移动的子弹"""
    def __init__(self, screen, pos, img_name, plane_size, speed):
        """构造函数"""
        BulletBase.__init__(self, screen, pos, img_name)
        # 设置子弹速度
        self.speed_x = speed[0]
        self.speed_y = speed[1]
        self.start_x = pos[0]

    def update(self):
        """子弹移动"""
        self.rect.move_ip(self.speed_x, -self.speed_y)
        if self.rect.left > self.start_x + 30:
            self.rect.left = self.start_x + 30
            self.speed_x = -self.speed_x
        elif self.rect.left < self.start_x - 30:
            self.rect.left = self.start_x - 30
            self.speed_x = -self.speed_x

        if self.rect.left < 0 or self.rect.left > self.screen_w or self.rect.bottom < 0:
            # 删除
            self.kill()

    def hurt(self, enemy):
        """子弹击中敌机"""
        if pygame.Rect.colliderect(self.rect, enemy.rect):
            self.kill()
            # 调用敌机的被攻击方法
            return enemy.be_attacked()
        return 0

    def deal_img(self, img_name):
        """子弹的图片处理"""
        img = pygame.image.load(img_name).convert_alpha()
        img = pygame.transform.scale(img, (15, 15))
        return img


class Bullet2(BulletBase):
    """激光子弹"""
    def __init__(self, screen, pos, img_name, plane_size):
        """构造函数"""
        BulletBase.__init__(self, screen, pos, img_name)
        # 设置子弹的速度
        self.speed_x = 0
        self.speed_y = 0
        self.rect.left, self.rect.bottom = self.x, self.y
        self.daojishi = 0

    def update(self):
        self.screen.blit(self.img, self.rect)
        # pass
        # self.rect.move_ip(0, 400)
        # if self.rect.top < 0:
        #     self.kill()

    def draw(self):
        """绘制激光子弹"""
        self.screen.blit(self.img, self.rect)
        self.kill()

    def hurt(self, enemy):
        """子弹击中敌机"""
        if pygame.Rect.colliderect(self.rect, enemy.rect):
            # 调用敌机被攻击函数
            return enemy.be_attacked()
        return 0

    def deal_img(self, img_name):
        """子弹的图片处理"""
        img = pygame.image.load(img_name).convert_alpha()
        img = pygame.transform.scale(img, (52, self.screen_h))
        return img


class EnemyBullet1(BulletBase):
    """
    斜着运动的子弹
    __init__(self, screen, pos, img_name, plane_size=None)
    update(self)
    """
    def __init__(self, screen, pos, img_name, plane_size=None):
        """
        EnemyBullet2的构造函数
        这里只重写速度
        """
        BulletBase.__init__(self, screen, pos, img_name)

        self.speed_x = 6
        self.speed_y = 6
        self.start_x = pos[0]

    def deal_img(self, img_name):
        """子弹的图片处理"""
        img = pygame.image.load(img_name).convert_alpha()
        img = pygame.transform.scale(img, (12, 15))
        return img

    def update(self):
        """子弹移动, 不同的子弹有不同的移动方式"""
        self.rect.move_ip(self.speed_x, self.speed_y)

        if self.rect.left > self.start_x + 20:
            self.rect.left = self.start_x + 20
            self.speed_x = -self.speed_x
        elif self.rect.left < self.start_x - 20:
            self.rect.left = self.start_x - 20
            self.speed_x = -self.speed_x

        if self.rect.bottom > self.screen_h:
            # 删除
            self.kill()


class EnemyBullet2(BulletBase):
    """
        这是斜着运动的子弹
        __init__(self, screen, pos, img_name, plane_size=None)
        update(self)
    """
    def __init__(self, screen, pos, img_name, plane_size=None):
        """构造函数，重写速度"""
        BulletBase.__init__(self, screen, pos, img_name)
        # 重写速度
        self.speed_y = 6
        self.speed_x = 0

    def deal_img(self, img_name):
        """子弹的图片处理"""
        return pygame.image.load(img_name).convert_alpha()

    def update(self):
        """子弹的运动, 这里能够斜线运动"""
        self.rect.move_ip(0, self.speed_y)
        self.collision()


class EnemyBullet3(BulletBase):
    """
    斜着运动的子弹
    __init__(self, screen, pos, img_name, plane_size=None)
    update(self)
    """
    def __init__(self, screen, pos, img_name, plane_size=None):
        BulletBase.__init__(self, screen, pos, img_name)
        # 判断向左还是向右
        self.sign = 1
        self.increase = 0
        self.speed_y = 1
        # 敌机出现在窗口靠右，则sign=-1
        if self.x > self.screen_w // 2:
            self.sign = -1
        self.gengxin = 0

    def deal_img(self, img_name):
        """子弹的图片处理"""
        img = pygame.image.load(img_name).convert_alpha()
        img = pygame.transform.scale(img, (8, 16))
        return img

    def collision(self):
        """碰撞检测"""
        if self.rect.left < 0:
            self.kill()
        elif self.rect.right > self.screen_w:
            self.kill()
        elif self.rect.top > self.screen_h:
            self.kill()

    def update(self):
        """设置子弹移动"""
        self.gengxin += 1
        if self.gengxin % 6 == 0:
            """子弹的运动, 这里能够斜线运动"""
            self.rect.y += self.speed_y + 30
            self.increase += self.speed_y
            # x = 1/2 y * y
            self.rect.x += self.increase * self.increase * self.sign
            # self.rect.move_ip(self.speed_x, self.speed_y)
        self.collision()


class EnemyBullet4(BulletBase):
    """
    斜着运动的子弹
    __init__(self, screen, pos, img_name, plane_size=None)
    update(self)
    """
    def __init__(self, screen, pos, img_name, plane_size=None, speed=None):
        """
        EnemyBullet2的构造函数
        这里只重写速度
        """
        BulletBase.__init__(self, screen, pos, img_name)

        self.speed_x = speed[0]
        self.speed_y = speed[1]
        self.start_x = pos[0]

    def deal_img(self, img_name):
        """子弹的图片处理"""
        img = pygame.image.load(img_name).convert_alpha()
        return img

    def update(self):
        """子弹移动, 不同的子弹有不同的移动方式"""
        self.rect.move_ip(self.speed_x, self.speed_y)

        if self.rect.left < 0:
            self.kill()
        elif self.rect.left > self.screen_w:
            self.kill()
        if self.rect.bottom > self.screen_h:
            # 删除
            self.kill()



