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

class MySprite(pygame.sprite.Sprite):
    speed = 5
    def __init__(self, paddle, bricks):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image("ball.png")
        self.dx = self.dy = 0  # ボールの速度
        self.paddle = paddle  # パドルへの参照
        self.bricks = bricks  # ブロックグループへの参照
        self.update = self.start
    def start(self):
        """ボールの位置を初期化"""
        # パドルの中央に配置
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top
        # 左クリックで移動開始
        if pygame.mouse.get_pressed()[0] == 1:
            self.dx = self.speed
            self.dy = -self.speed
            # update()をmove()に置き換え
            self.update = self.move
    def move(self):
        """ボールの移動"""
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        # 壁との反射
        if self.rect.left < SCR_RECT.left:  # 左側
            self.rect.left = SCR_RECT.left
            self.dx = -self.dx  # 速度を反転
        if self.rect.right > SCR_RECT.right:  # 右側
            self.rect.right = SCR_RECT.right
            self.dx = -self.dx
        if self.rect.top < SCR_RECT.top:  # 上側
            self.rect.top = SCR_RECT.top
            self.dy = -self.dy
        # パドルとの反射
        if self.rect.colliderect(self.paddle.rect) and self.dy > 0:
            self.dy = -self.dy
        # ボールを落とした場合
        if self.rect.top > SCR_RECT.bottom:
            self.update = self.start  # ボールを初期状態に
        # ブロックを壊す
        # ボールと衝突したブロックリストを取得
        bricks_collided = pygame.sprite.spritecollide(self, self.bricks, True)
        if bricks_collided:  # 衝突ブロックがある場合
            oldrect = self.rect
            for brick in bricks_collided:  # 各衝突ブロックに対して
                # ボールが左から衝突
                if oldrect.left < brick.rect.left < oldrect.right < brick.rect.right:
                    self.rect.right = brick.rect.left
                    self.dx = -self.dx
                # ボールが右から衝突
                if brick.rect.left < oldrect.left < brick.rect.right < oldrect.right:
                    self.rect.left = brick.rect.right
                    self.dx = -self.dx
                # ボールが上から衝突
                if oldrect.top < brick.rect.top < oldrect.bottom < brick.rect.bottom:
                    self.rect.bottom = brick.rect.top
                    self.dy = -self.dy
                # ボールが下から衝突
                if brick.rect.top < oldrect.top < brick.rect.bottom < oldrect.bottom:
                    self.rect.top = brick.rect.bottom
                    self.dy = -self.dy

if __name__ == "__main__":
    main()