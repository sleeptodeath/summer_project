# coding=utf-8
"""
玩家飞机类：

"""
from planebase import *


class Plane(PlaneBase):
    """玩家飞机类"""
    def __init__(self, screen, img_name, dead_img_list):
        """构造函数"""
        # 调用父类构造函数
        PlaneBase.__init__(self, screen, img_name, dead_img_list)
        # 血量
        self.hp = 3
        # 无敌
        self.WUDI = False
        # 种类
        self.kind = 1
        # 飞机的等级，用来发射不用的子弹
        self.level = 1
        # 初始化飞机位置为窗口正下方
        self.rect.left = (self.screen_w - self.img.get_size()[0]) // 2
        self.rect.top = self.screen_h - self.img.get_size()[1]

        # 飞机移动的速度
        self.speed = 10

    def collision(self):
        """检查敌机是否碰到四周"""
        if self.rect.right > self.screen_w:
            self.rect.right = self.screen_w
        elif self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > self.screen_h:
            self.rect.bottom = self.screen_h

    def update(self, pressed_keys=None):
        """监听相应键盘事件，进行移动"""
        # 按方向移动
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)
        # 与墙壁碰撞
        self.collision()

    def daiding(self):
        """绘制血量"""
        self.screen.blit(self.tail,
                         (self.rect.left + self.img.get_size()[0] // 4, self.rect.bottom))

    def shoot(self):
        """
        发射子弹，并将子弹存入子弹组,
        根据飞机等级更新不同类型的子弹
        """
        self.kind = self.level // 1
        if self.kind >= 5:
            self.kind = 5
        new_bullet = self.bullet_factory.\
            make_bullet(self.screen, (self.rect.left, self.rect.top),
                        self.img.get_size(), self.kind)
        # 添加到子弹组
        self.bullets.add(new_bullet)

    def dead(self):
        """飞机被击毁动画绘制结束后， 重置飞机位置和LIVE"""
        self.img = self.main_img
        self.rect.left = (self.screen_w - self.img.get_size()[0]) // 2
        self.dead_index = 0
        self.rect.top = self.screen_h - self.img.get_size()[1]
        self.LIVE = True