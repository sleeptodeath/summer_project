# coding=utf-8
"""
资源类，敌机有几率掉落
"""
import pygame
import random
from source import *


class EnergyFactory(object):
    """子弹工产，用来生产敌机"""
    def __init__(self):
        pass

    @staticmethod
    def make_energy(screen, pos):
        """产生资源"""
        if random.random() < 0.2:
            return Energy2(screen, pic["energy2"], pos)
        else:
            return Energy1(screen, pic["energy1"], pos)


class Energy(pygame.sprite.Sprite):
    """资源类"""
    def __init__(self, screen, img_name, pos):
        """构造函数"""
        super(Energy, self).__init__()
        # pygame的窗口
        self.screen = screen
        self.screen_w, self.screen_h = self.screen.get_size()
        # 资源的种类
        self.kind = 1
        # 资源的图片
        self.img = self.deal_img(img_name)
        self.rect = self.img.get_rect()
        self.rect.left, self.rect.top = pos[0], pos[1]
        # 资源移动的速度
        self.speed = 4

    def deal_img(self, img_name):
        """图像的处理"""
        return pygame.image.load(img_name).convert_alpha()

    def update(self, *args):
        """移动"""
        self.rect.move_ip(0, self.speed)
        if self.rect.top > self.screen_h:
            self.kill()

    def draw(self):
        """资源类的绘制"""
        self.screen.blit(self.img, self.rect)

    def supply(self, player):
        """玩家吃到资源时调用"""
        pass


class Energy1(Energy):
    """资源类1"""
    def deal_img(self, img_name):
        """图片处理"""
        img = pygame.image.load(img_name).convert_alpha()
        img = img.subsurface(pygame.Rect(38, 20, 28, 42))
        img = pygame.transform.scale(img, (28, 30))
        return img

    def supply(self, player):
        """资源作用"""
        # 玩家等级提升
        player.level += 1

class Energy2(Energy):
    """资源类1"""

    def deal_img(self, img_name):
        """图片处理"""
        img = pygame.image.load(img_name).convert_alpha()
        img = pygame.transform.scale(img, (img.get_size()[0] // 4, img.get_size()[1] // 4))
        return img

    def supply(self, player):
        """资源作用"""
        # 玩家加血
        if player.hp < 3:
            player.hp += 1
