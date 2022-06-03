# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:36:03 2013

@author: Leo
"""

from turtle import right
import pygame
import random
import copy

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3

class Item(pygame.sprite.Sprite):
    def __init__(self, bullet_item_img, bomb_item_img, bullet_item_alpha_img, bomb_item_alpha_img, item_index, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.images = [bullet_item_img, bomb_item_img]
        self.images_alpha = [bullet_item_alpha_img, bomb_item_alpha_img]
        self.index = item_index
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = init_pos
        self.xSpeed = 2
        self.ySpeed = 2
        self.yTime = 0
        self.time = 0
    def move(self):
        self.rect.left += self.xSpeed
        self.rect.top += self.ySpeed

# 총알
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
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
            image = plane_img.subsurface(player_rect[i])
            image = pygame.transform.scale(image, (68,84))
            self.image.append(image)
        self.rect = player_rect[0]                      # 이미지가 위치한 사각형 초기화
        self.rect.topleft = init_pos                    # 사각형의 왼쪽 위 모서리 좌표를 초기화합니다.
        self.speed = 5                                  # 플레이어 속도를 초기화합니다. 여기에 확실한 값이 있습니다.
        self.bullets = pygame.sprite.Group()            # 플레이어의 항공기에서 발사된 총알 모음
        self.bombs = pygame.sprite.Group()              # 발사된 폭탄 모음
        self.img_index = 0                              # 플레이어 스프라이트 이미지 인덱스
        self.is_hit = False                             # 플레이어가 맞았는지 여부
        self.maxHealth = 1000                              # 최대 생명력
        self.health = self.maxHealth                    # 생명력
        self.bomb = 0                                   # 폭탄
        self.bullet = 1                                 # 총알

    def throw(self, bomb_img):
        bomb = Bomb(bomb_img, (self.rect.midtop))
        self.bombs.add(bomb)

    def shoot(self, bullet_img):
        bulletsWidth = (self.bullet*12-3)/2+7
        for i in range(0, self.bullet):
            posX = (self.rect.centerx-bulletsWidth)+i*12
            posY = self.rect.top
            bullet = Bullet(bullet_img, (posX, posY))
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
    def damage(self):
        self.is_hit = True
        self.health -= 1

# 적군
class Enemy1(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy_img
       self.rect = self.image.get_rect()
       self.rect.topleft = init_pos
       self.down_imgs = enemy_down_imgs
       self.speed = 5
       self.down_index = 0
       self.moveInt = random.randint(1,3)

    def move(self):
        self.rect.top += self.speed
        if self.moveInt == 1:
            self.rect.left += self.rect.top*0.01
        elif self.moveInt == 2:
            self.rect.left -= self.rect.top*0.01

class Enemy2(pygame.sprite.Sprite):
    def __init__(self, enemy2_img, enemy2_damage_img, enemy2_down_imgs, init_pos):
       pygame.sprite.Sprite.__init__(self)
       self.image = enemy2_img
       self.enemy2_damage_img = enemy2_damage_img
       self.down_imgs = enemy2_down_imgs
       self.rect = self.image.get_rect()
       self.rect.center = init_pos
       self.speed = 3
       self.down_index = 0
       self.maxHealth = 250
       self.health = self.maxHealth
       self.direction = -1                                   # -1: 왼쪽   1: 오른쪽
       self.bullets = pygame.sprite.Group()
    def move(self):
        if self.rect.centery < 150:
            self.rect.top += self.speed*2
        else:
            if self.direction == -1:
                self.rect.left -= self.speed
            else:
                self.rect.left += self.speed
            
            if self.rect.left < 10 or self.rect.right > SCREEN_WIDTH-10:
                self.direction *= -1
    def damage(self, damage):
        self.health -= damage
    def shoot(self, bullet_img):
        for i in [0.001, 0.005]:
            bullet = BulletEnemy(bullet_img, self.rect.midbottom, i)
            self.bullets.add(bullet)

class BulletEnemy(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos, coefficient):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midtop = init_pos
        self.speed = 3
        self.coefficient = coefficient
    def move(self):
        self.rect.top += self.speed
        self.rect.left += self.rect.top*self.coefficient