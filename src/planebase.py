# coding=utf-8
"""
敌机和玩家飞机的基类

"""
from bullet import *


class PlaneBase(pygame.sprite.Sprite):
    """敌机和玩家飞机的基类"""
    def __init__(self, screen, img_name, dead_img_list):
        """构造函数， 初始化
        screen:
        img_name:
        deal_img_list:
        """
        super(PlaneBase, self).__init__()
        # pygame的主窗口
        self.screen = screen
        self.screen_w, self.screen_h = self.screen.get_size()

        # 是否存活
        self.LIVE = True
        # 是否可见
        self.VISIBLE = True
        # 血量
        self.hp = 1
        # 种类, 用来标记不同的飞机
        self.kind = 1
        # 变化图片
        self.cnt = 0
        self.switch_hz = 5
        # 用来产生子弹的工厂函数
        self.bullet_factory = BulletFactory()
        # 子弹组
        self.bullets = pygame.sprite.Group()

        # 飞机显示的图片列表
        self.main_img = self.deal_img(img_name[0])
        self.img = self.main_img
        self.index = 0
        self.tail_list = []

        for i in range(1, len(img_name)):
            tail = pygame.image.load(img_name[i])
            self.tail_list.append(pygame.transform.scale(tail, (self.img.get_size()[0] // 2, self.img.get_size()[0] // 2)))
        self.tail = self.tail_list[0]

        # 敌机爆炸的动画图片列表
        self.dead_img_list = []
        for name in dead_img_list:
            img = self.deal_dead_img(name)
            self.dead_img_list.append(img)
        self.dead_index = 0
        self.dead_img = self.dead_img_list[0]
        # 获得敌机图像对应的矩形
        self.rect = self.img.get_rect()

    def deal_dead_img(self, img_name):
        img = pygame.image.load(img_name).convert_alpha()
        img = pygame.transform.scale(img, (self.img.get_size()[0], self.img.get_size()[1]))
        return img

    def deal_img(self, img_name):
        """子弹的图片处理"""
        return pygame.image.load(img_name).convert_alpha()

    def collision(self):
        """与窗口的碰撞检测"""
        pass

    def shoot_hz(self):
        """设计频率设置"""
        pass

    def switch_img(self):
        """图片改变"""
        self.cnt += 1
        if self.cnt > self.switch_hz:
            self.cnt = 0
            self.index += 1
            if self.index >= len(self.tail_list):
                self.index = 0
        self.tail = self.tail_list[self.index]

    def daiding(self):
        """待定事件"""
        pass

    def draw(self, paused=False):
        """敌机的绘制"""
        # 不在暂停情况下
        if not paused:
            # 存活并且不再死亡动画状态
            if self.LIVE and self.VISIBLE:
                self.switch_img()
                self.daiding()
                # 射击
                self.shoot_hz()
                self.screen.blit(self.img, self.rect)
            # 被击毁，但在死亡状态下
            elif not self.LIVE and self.VISIBLE:
                # 设置图片为死亡动画
                self.screen.blit(self.img, self.rect)
                self.death()

            # 敌机子弹的移动和绘制
            for enty in self.bullets:
                enty.update()
                enty.draw()

        # 暂停情况下， 停止移动
        else:
            if self.VISIBLE:
                self.screen.blit(self.img, self.rect)
            # 敌机子弹的绘制， 不移动
            for enty in self.bullets:
                enty.draw()

    def collision(self):
        """检查敌机是否碰到四周， 如果敌机到达最下方则删除"""
        pass

    def shoot(self, kind=None):
        """发射子弹，并将子弹存入子弹组, 需要自己写"""
        pass

    def death(self):
        """敌机死亡时绘制爆炸动画"""
        # 绘制动画
        self.dead_img = self.dead_img_list[self.dead_index]
        self.screen.blit(self.dead_img, self.rect)
        self.dead_index += 1
        if self.dead_index >= len(self.dead_img_list):
            self.dead()

    def dead(self):
        """死亡动画绘制完后"""
        pass
