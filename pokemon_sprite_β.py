"""
＿人人人人人人人人人人人人人＿
＞　計算資源(≒PC)を抽象化　＜
￣Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y^Y￣
"""

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCR_RECT = Rect(0, 0, 800, 600)

group = pygame.sprite.RenderUpdates()

class MySprite(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, vx, vy):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.image.load(filename).convert_alpha()
        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = Rect(x, y, width, height)
        self.vx = vx
        self.vy = vy
        
    def update(self, grp):
        """ 他のメタモンとぶつかったら跳ね返るようにしたい """
        metamon_collide = pygame.sprite.spritecollide(self, grp, False)
        self.rect.move_ip(self.vx, self.vy)
        # 壁にぶつかったら跳ね返る
        if self.rect.left < 0 or self.rect.right > SCR_RECT.width:
            self.vx = -self.vx
        if self.rect.top < 0 or self.rect.bottom > SCR_RECT.height:
            self.vy = -self.vy
        if metamon_collide:
            pokerect = self.rect
            for grp in metamon_collide:  # 各衝突ブロックに対して
                # ボールが左から衝突
                if pokerect.right >= grp.rect.left and pokerect.centerx < 0 or pokerect.right <= grp.rect.left and pokerect.centerx > 0:
                    self.vx = -self.vx
                # ボールが右から衝突
                if pokerect.left <= grp.rect.right and pokerect.centerx > 0 or pokerect.left >= grp.rect.right and pokerect.centerx < 0:
                    self.vx = -self.vx
                # ボールが上から衝突
                if pokerect.bottom <= grp.rect.top and pokerect.centery < 0 or pokerect.bottom >= grp.rect.top and pokerect.centery > 0:
                    self.vy = -self.vy
                # ボールが下から衝突
                if pokerect.top >= grp.rect.bottom and pokerect.centery > 0 or pokerect.bottom <= grp.rect.top and pokerect.centery < 0:
                    self.vy = -self.vy
        # 画面からはみ出ないようにする
        self.rect = self.rect.clamp(SCR_RECT)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"sprite_group")
    group = pygame.sprite.RenderUpdates()
    MySprite.containers = group
    
    # スプライトを作成
    metamon0 = MySprite("pygame_image/74.132.png", 0, 0, 2, 2)
    metamon1 = MySprite("pygame_image/68.132.png", 10, 320, -2, 2)
    metamon2 = MySprite("pygame_image/88.132.png", 320, 240, 2, -2)
    
    group01 = pygame.sprite.RenderUpdates()
    group12 = pygame.sprite.RenderUpdates()
    group02 = pygame.sprite.RenderUpdates()

    group01.add(metamon0)
    group02.add(metamon0)
    group01.add(metamon1)
    group12.add(metamon1)
    group02.add(metamon2)
    group12.add(metamon2)

    clock = pygame.time.Clock()
    
    while True:
        clock.tick(60)  # 60fps
        screen.fill((0,0,255))
        # スプライトを更新
        metamon0.update(group12)
        metamon1.update(group02)
        metamon2.update(group01)
        # スプライトグループを描画
        group.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

if __name__ == "__main__":
    main()