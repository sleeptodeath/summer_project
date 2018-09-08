# coding=utf-8
import pygame
# from pygame.locals import  *
pygame.init()
pygame.mixer.init()
# 标题
# icon
# 窗口
# 背景图片
pygame.mixer.music.load()
screen = pygame.display.set_mode((800, 600))
print(pygame.display.Info().current_w)
surf = pygame.Surface((100, 100))
surf.fill((255, 255, 255))
pygame.Rect.collidepoint()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False
