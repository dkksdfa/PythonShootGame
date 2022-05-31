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

#총알 아이템
bullet_item_rect = pygame.Rect(269, 398, 54, 86)
bullet_item_img = plane_img.subsurface(bullet_item_rect)

#폭탄
bomb_rect = pygame.Rect(830, 693, 23, 53)
bomb_img = plane_img.subsurface(bomb_rect)

#폭탄 아이템
bomb_item_rect = pygame.Rect(105, 120, 55, 102)
bomb_item_img  = plane_img.subsurface(bomb_item_rect)

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

items = pygame.sprite.Group()

shoot_frequency = 0
enemy_frequency = 0

player_down_index = 16

score = 0

running = True

while running:
    # 게임의 최대 프레임 속도를 60으로 제어
    clock.tick(60)

    # 총알 발사 빈도 및 총알 발사 빈도 제어
    if player.health > 0:
        if shoot_frequency % 5 == 0:
            bullet_sound.play()
            player.shoot(bullet_img)
        shoot_frequency += 1
        if shoot_frequency >= 15:
            shoot_frequency = 0

    # 적 비행기 생성
    if enemy_frequency % 60 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1
    if enemy_frequency >= 120:
        enemy_frequency = 0

    #폭탄 이동, 타이머가 다 되면 폭발
    for bomb in player.bombs:
        bomb.move()
        if (bomb.timer < 0):
            player.bombs.remove(bomb)
            for enemy in enemies1:
                enemies_down.add(enemy)
                enemies1.remove(enemy)

    # 총알 이동, 창 범위를 초과하면 삭제
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    # 적 이동, 창 범위를 초과하면 삭제
    for enemy in enemies1:
        enemy.move()
        # 플레이어가 공격을 받았는지 확인
        if pygame.sprite.collide_circle(enemy, player):
            enemies_down.add(enemy)
            enemies1.remove(enemy)
            player.is_hit = True
            player.health -= 1
            if player.health <= 0:
                game_over_sound.play()
                break
        if enemy.rect.top > SCREEN_HEIGHT:
            enemies1.remove(enemy)
    # 파괴 애니메이션을 렌더링하는 데 사용되는 파괴된 적 항공기 그룹에 적중된 적 항공기 개체를 추가합니다.
    enemies1_down = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy_down in enemies1_down:
        enemies_down.add(enemy_down)

    # 배경 그리기
    screen.fill(0)
    screen.blit(background, (0, 0))
    
    # 플레이어 비행기 그리기
    if player.is_hit and player.health > 0: #데미지를 입었으나 죽지는 않음
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            player.is_hit = False
            player_down_index = 16
    elif player.health > 0:
        screen.blit(player.image[player.img_index], player.rect)
        # 비행기에 애니메이션을 적용하기 위해 그림 인덱스를 변경했습니다.
        player.img_index = shoot_frequency // 8
    else:
        player.img_index = player_down_index // 8
        screen.blit(player.image[player.img_index], player.rect)
        player_down_index += 1
        if player_down_index > 47:
            running = False

    # 난파선 애니메이션 그리기
    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies_down.remove(enemy_down)
            score += 10
            item = BulletItem(bullet_item_img, enemy_down.rect.center)
            items.add(item)
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # 총알과 적 비행기 그리기
    player.bullets.draw(screen)
    player.bombs.draw(screen)
    enemies1.draw(screen)
    items.draw(screen)

    #생명력 UI 그리기
    for i in range(player.health):
        screen.blit(black_heart, (i*30+10, 5))
    for i in range(1, player.maxHealth - player.health + 1):
        screen.blit(white_heart, ((player.health-1)*30+10+(i*30), 5))

    # 폭탄 UI 그리기
    for i in range(player.bomb):
        bomb_img = pygame.transform.scale(bomb_img,(15, 30))
        screen.blit(bomb_img, ((i*20+10)+(player.maxHealth*30+15), 5))
        
    # 점수 UI 그리기
    score_font = pygame.font.Font(None, 36)
    score_text = score_font.render(str(score), True, (128, 128, 128))
    text_width = score_font.size(str(score))[0]
    text_rect = score_text.get_rect()
    text_rect.topleft = [SCREEN_WIDTH-text_width-10, 10]
    
    screen.blit(score_text, text_rect)

    # 업데이트 화면
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                if player.bomb > 0:
                    player.bomb -= 1
                    player.throw(bomb_img)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
    # 키보드 이벤트 수신
    key_pressed = pygame.key.get_pressed()
    # 플레이어가 명중되면 효과가 없습니다.
    if player.health > 0:
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()


font = pygame.font.Font(None, 48)
text = font.render('Score: '+ str(score), True, (255, 0, 0))
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery + 24
screen.blit(game_over, (0, 0))
screen.blit(text, text_rect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
