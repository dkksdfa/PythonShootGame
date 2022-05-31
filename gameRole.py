# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
"""

from turtle import right
import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1000

TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3

class Item(pygame.sprite.Sprite):
    def __init__(self, bullet_item_img, bomb_item_img, item_index, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.images = [bullet_item_img, bomb_item_img]
        self.index = item_index
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = init_pos
        self.xSpeed = 2
        self.ySpeed = 2
    def move(self):
        self.rect.left -= self.xSpeed
        self.rect.top -= self.ySpeed

# 총알
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 20

    def move(self):
        self.rect.top -= self.speed

class Bomb(pygame.sprite.Sprite):
    def __init__(self, bomb_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bomb_img
        self.rect = self.image.get_rect()
        self.rect .midbottom = init_pos
        self.speed = 3
        self.timer = 80
    def move(self):
        self.rect.top -= self.speed
        self.timer -= 1

# 플레이어 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []                                 # 플레이어 오브젝트 스프라이트 이미지를 저장할 목록
        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(player_rect[i]).convert_alpha())
        self.rect = player_rect[0]                      # 이미지가 위치한 사각형 초기화
        self.rect.topleft = init_pos                    # 사각형의 왼쪽 위 모서리 좌표를 초기화합니다.
        self.speed = 8                                  # 플레이어 속도를 초기화합니다. 여기에 확실한 값이 있습니다.
        self.bullets = pygame.sprite.Group()            # 플레이어의 항공기에서 발사된 총알 모음
        self.bombs = pygame.sprite.Group()              # 발사된 폭탄 모음
        self.img_index = 0                              # 플레이어 스프라이트 이미지 인덱스
        self.is_hit = False                             # 플레이어가 맞았는지 여부
        self.maxHealth = 3                              # 최대 생명력
        self.health = self.maxHealth                    # 생명력
        self.maxBomb = 3
        self.bomb = self.maxBomb

    def throw(self, bomb_img):
        bomb = Bomb(bomb_img, (self.rect.midtop))
        self.bombs.add(bomb)

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, (self.rect.centerx, self.rect.top))
        #bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

# 적군
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs
       self.speed = 2
       self.down_index = 0

    def move(self):
        self.rect.top += self.speed