# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

import pygame
from sys import exit
from pygame.locals import *
from gameRole import *
import random


# 게임 초기화
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('항공기 전쟁')
clock = pygame.time.Clock()

# 게임 음악 로드
bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# 배경 이미지 로드
background = pygame.image.load('resources/image/background.png').convert()
game_over = pygame.image.load('resources/image/gameover.png')

filename = 'resources/image/shoot.png'
plane_img = pygame.image.load(filename)

#생명력 이미지 로드
black_heart = pygame.image.load('resources/image/black_heart.png')
black_heart = pygame.transform.scale(black_heart, (30,30))
white_heart = pygame.image.load('resources/image/white_heart.png')
white_heart = pygame.transform.scale(white_heart, (30,30))

# 플레이어 관련 매개변수 설정  
player_rect = []
player_rect.append(pygame.Rect(0, 99, 102, 126))        # 플레이어 스프라이트 그림 영역
player_rect.append(pygame.Rect(165, 360, 102, 126))
player_rect.append(pygame.Rect(165, 234, 102, 126))     # 플레이어 폭발 스프라이트 그림 영역
player_rect.append(pygame.Rect(330, 624, 102, 126))
player_rect.append(pygame.Rect(330, 498, 102, 126))
player_rect.append(pygame.Rect(432, 624, 102, 126))
player_pos = [200, 600]
player = Player(plane_img, player_rect, player_pos)

# 글머리 기호 개체에서 사용하는 표면 관련 매개변수 정의
bullet_rect = pygame.Rect(1004, 987, 9, 21)
bullet_img = plane_img.subsurface(bullet_rect)

# 적 항공기 개체가 사용하는 표면 관련 매개변수 정의
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies1 = pygame.sprite.Group()

# 난파선 스프라이트 애니메이션을 렌더링하기 위해 난파선 저장
enemies_down = pygame.sprite.Group()

shoot_frequency = 0
enemy_frequency = 0

player_down_index = 16

score = 0

running = True

while running:
    # 게임의 최대 프레임 속도를 60으로 제어
    clock.tick(45)

    # 배경 그리기
    screen.fill(0)
    screen.blit(background, (0, 0))
    #screen.blit(plane_img.subsurface(105, 120, 55, 102), (0,0)) #폭탄 아이템
    #screen.blit(plane_img.subsurface(269, 398, 54, 86), (0,0)) #총알 아이템

    #screen.blit(plane_img.subsurface(830, 693, 23, 53), (0, 0)) 폭탄
    
    #screen.blit(plane_img.subsurface(169, 752, 164, 255), (0, 0)) #보스
    #screen.blit(plane_img.subsurface(338, 752, 164, 255), (0,0)) #보스
    #screen.blit(plane_img.subsurface(507, 752, 164, 255), (0, 0)) #보스
    #screen.blit(plane_img.subsurface(676, 752, 164, 255), (0, 0)) #보스
    #screen.blit(plane_img.subsurface(845, 752, 157, 255), (0, 0)) #보스
    #screen.blit(plane_img.subsurface(0, 225, 164, 255),(0,0)) #보스
    #screen.blit(plane_img.subsurface(0, 488, 164, 255),(0,0)) #보스
    #screen.blit(plane_img.subsurface(164, 488, 164, 255),(0,0)) #보스

    #screen.blit(plane_img.subsurface(1, 4, 67, 87), (0,0)) #적
    #screen.blit(plane_img.subsurface(433, 529, 67, 94), (0,0)) #적
    #screen.blit(plane_img.subsurface(535, 655, 67, 94), (0,0)) #적
    #screen.blit(plane_img.subsurface(604, 655, 67, 94), (0,0)) #적
    #screen.blit(plane_img.subsurface(673, 655, 70, 94), (0,0)) #적

    # 업데이트 화면
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # 키보드 이벤트 수신
    key_pressed = pygame.key.get_pressed()
    if player.health > 0:
        if key_pressed[K_LSHIFT] or key_pressed[K_RSHIFT]:
            print("폭탄")

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
