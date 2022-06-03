# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:05:00 2013

@author: Leo
"""

from copy import deepcopy
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
background = pygame.image.load('resources/image/background.png')
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

# 총알
bullet_img = plane_img.subsurface(pygame.Rect(1004, 987, 9, 21))

# 총알 아이템
bullet_item_img = plane_img.subsurface(pygame.Rect(269, 398, 54, 86))
bullet_item_img = pygame.transform.scale(bullet_item_img, (40, 65))
bullet_item_alpha_img = plane_img.subsurface(pygame.Rect(269, 398, 54, 86))
bullet_item_alpha_img = pygame.transform.scale(bullet_item_alpha_img, (40, 65))
bullet_item_alpha_img.set_alpha(128)

# 폭탄
bomb_img = plane_img.subsurface(pygame.Rect(830, 693, 23, 53))

# 폭탄 아이템
bomb_item_img  = plane_img.subsurface(pygame.Rect(105, 120, 55, 102))
bomb_item_img = pygame.transform.scale(bomb_item_img, (40, 65))
bomb_item_alpha_img = plane_img.subsurface(pygame.Rect(105, 120, 55, 102))
bomb_item_alpha_img = pygame.transform.scale(bomb_item_alpha_img, (40, 65))
bomb_item_alpha_img.set_alpha(128)

# 적1 매개변수 정의
enemy1_rect = pygame.Rect(534, 612, 57, 43)
enemy1_img = plane_img.subsurface(enemy1_rect)
enemy1_down_imgs = []
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
enemy1_down_imgs.append(plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))
enemies1 = pygame.sprite.Group()
enemies1_down = pygame.sprite.Group()

# 적2 매개변수 정의
enemy2_img = plane_img.subsurface(pygame.Rect(1, 4, 67, 87))
enemy2_damage_img = plane_img.subsurface(pygame.Rect(433, 529, 67, 94))
enemy2_down_imgs = []
enemy2_down_imgs.append(plane_img.subsurface(535, 655, 67, 94))
enemy2_down_imgs.append(plane_img.subsurface(604, 655, 67, 94))
enemy2_down_imgs.append(plane_img.subsurface(673, 655, 70, 94))
enemies2 = pygame.sprite.Group()
enemies2_down = pygame.sprite.Group()

items = pygame.sprite.Group()

shoot_frequency = 0
enemy_frequency = 0
enemy_shoot_frequency = 0

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

    # 적1 생성
    if enemy_frequency % 30 == 0:
        enemy1_pos = [random.randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
        enemy1 = Enemy1(enemy1_img, enemy1_down_imgs, enemy1_pos)
        enemies1.add(enemy1)
    enemy_frequency += 1

    # 적2 생성
    if (score%100 == 0 or score>50) and len(enemies2) == 0:        
        enemy2 = Enemy2(enemy2_img, enemy2_damage_img, enemy2_down_imgs, (160, 0))
        enemies2.add(enemy2)
        enemy2 = Enemy2(enemy2_img, enemy2_damage_img, enemy2_down_imgs, (320, 0))
        enemies2.add(enemy2)

    #폭탄 이동, 타이머가 다 되면 폭발
    for bomb in player.bombs:
        bomb.move()
        if (bomb.timer < 0):
            player.bombs.remove(bomb)
            for enemy in enemies1:
                enemies1_down.add(enemy)
                enemies1.remove(enemy)

    # 총알 이동, 창 범위를 초과하면 삭제
    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    # 적 이동, 창 범위를 초과하면 삭제
    for enemy1 in enemies1:
        enemy1.move()
        # 플레이어가 공격을 받았는지 확인
        if pygame.sprite.collide_circle(enemy1, player):
            enemies1_down.add(enemy1)
            enemies1.remove(enemy1)
            player.is_hit = True
            player.health -= 1
            if player.health <= 0:
                game_over_sound.play()
                break
        if enemy1.rect.top > SCREEN_HEIGHT:
            enemies1.remove(enemy1)

    for enemy2 in enemies2:
        enemy2.move()
        for enemy2_bullt in enemy2.bullets:
            enemy2_bullt.move()
            if enemy2_bullt.rect.top > SCREEN_HEIGHT:
                enemy2.bullets.remove(enemy2_bullt)
        if enemy_shoot_frequency % 60 == 0:
            enemy2.shoot(bullet_img)
    enemy_shoot_frequency += 1

    # 아이템 이동, 창범위를 벗어나면 튕기도록
    for item in items:
        item.move()
        item.time += 1
        # 플레이어가 아이템을 획득했는지 확인
        if pygame.sprite.collide_circle(item, player):
            #아이템 획득 이벤트
            if item.index == 0 and player.bullet < 8:
                player.bullet += 1
            elif item.index == 1 and player.bomb < 3:
                player.bomb += 1
            items.remove(item)

        #아이템이 벽에서 튕기도록 함
        if item.rect.top <= 0 or item.rect.bottom >= SCREEN_HEIGHT:
            item.ySpeed *= -1
        if item.rect.left <= 0 or item.rect.right >= SCREEN_WIDTH:
            item.xSpeed *= -1
        
        #위쪽에 아이템이 오래 머물러 있다면 아래로 내려오도록 함
        if item.rect.top < 300:
            item.yTime += 1
            if item.yTime > 240:
                item.ySpeed = 2
                item.ytime = 0

        #아이템을 20초가 지나면 파괴
        if item.time > 1200:
            items.remove(item)

        #15초가 지나면 깜빡거림
        elif item.time > 900:
            if item.time%100 == 0:
                item.image = item.images_alpha[item.index]
            elif item.time%50 == 0:
                item.image = item.images[item.index]

    # 적1과 총알이 충돌할 시 적을 반환함. 충돌한 개체는 제거
    enemies1_collides = pygame.sprite.groupcollide(enemies1, player.bullets, 1, 1)
    for enemy in enemies1_collides:
        enemies1_down.add(enemy)

    # 적2과 총알이 충돌할 시 적을 반환함. 충돌한 총알만 제거
    enemies2_collides = pygame.sprite.groupcollide(enemies2, player.bullets, 0, 1)
    for enemy in enemies2_collides:
        enemy.damage(player.bullet)
        if enemy.health < enemy.maxHealth/2:
            enemy.image = enemy.enemy2_damage_img
        if enemy.health <= 0:
            score += 100
            enemies2.remove(enemy)
            enemies2_down.add(enemy)
    
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

    # 적1 파괴 애니메이션 그리기
    for enemy_down in enemies1_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 7:
            enemies1_down.remove(enemy_down)
            score += 10
            index = random.randint(0, 1)
            if index <= 1:
                item = Item(bullet_item_img, bomb_item_img, bullet_item_alpha_img, bomb_item_alpha_img, index, enemy_down.rect.center)
                items.add(item)
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2], enemy_down.rect)
        enemy_down.down_index += 1

    # 총알, 폭탄, 적, 아이템 그리기
    player.bullets.draw(screen)
    player.bombs.draw(screen)
    enemies1.draw(screen)
    enemies2.draw(screen)
    items.draw(screen)

    for enemy in enemies2:
        enemy.bullets.draw(screen)

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
