import os
import sys
import pygame as pg
import random
import time
import math

os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH, HEIGHT = 1600,900

def main():
    pg.display.set_caption("逃げろ！こうかとん")

    # 初期化 #
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"),0,2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900,400
    kk_speed = 5
    DELTA = {False:(0,0),pg.K_UP:(0,-kk_speed),pg.K_DOWN:(0,+kk_speed),pg.K_LEFT:(-kk_speed,0),pg.K_RIGHT:(+kk_speed,0)}
    def kk_turn(x,y):
        kk_rotozoom = {(0,0):0,(0,-kk_speed):270,(0,+kk_speed):90,
                       (+kk_speed,-kk_speed):235,(+kk_speed,0):180,(+kk_speed,+kk_speed):135,
                       (-kk_speed,-kk_speed):315,(-kk_speed,+kk_speed):45,(-kk_speed,0):0}
        return pg.transform.rotozoom(pg.image.load("fig/3.png"),kk_rotozoom[x,y],2.0)
    bomb = pg.Surface((20,20))
    pg.draw.circle(bomb,(255,0,0),(10,10),10)
    bomb.set_colorkey((0,0,0))
    bomb_rct = bomb.get_rect()
    bomb_rct.center = random.randint(400,1200),random.randint(225,675)
    vx,vy = 5,5
    accs = [a for a in range(1, 11)]
    def bomb_big():
        a = []
        for r in range(1, 11):
            bomb_img = pg.Surface((20*r, 20*r))
            pg.draw.circle(bomb_img, (255, 0, 0), (10*r, 10*r), 10*r)
            a += bomb_img
        print(a)
    Vev = False
    i = 0
    clock = pg.time.Clock()
    tmr = 0
    
    # ゲーム開始 #
    while True:

        # ゲームイベント #
        key_lst = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # プレイヤー #
        kk_move = [0,0]
        for x,y in DELTA.items():
            if key_lst[x]:
                kk_move[0] += y[0]
                kk_move[1] += y[1]
        kk_img = kk_turn(kk_move[0],kk_move[1])
        kk_rct.move_ip(kk_move)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-kk_move[0],-kk_move[1])

        # エネミー

        if Vev or abs(kk_rct.x**2+kk_rct.y**2 - bomb_rct.x**2+bomb_rct.y**2) < 300:
            kk_x,kk_y = kk_rct.x,kk_rct.y
            vx,vy = update_position(kk_x,kk_y)
            bomb_rct.move_ip(vx,vy)
            if bomb_rct.x == kk_x or bomb_rct.y == kk_y:
                i += 1
                if 20 < i:
                    i = 0
                    Vev = False
                else:
                    update_position(vx,vy)
            else:
                Vev = True
        else:
            vx,vy = update_position(bomb_rct,kk_rct)
            bomb_rct.move_ip(vx,vy)

        # 画面更新 #
        screen.blit(bg_img,[0,0])
        screen.blit(kk_img,kk_rct)
        screen.blit(bomb,bomb_rct)
        pg.display.update()

            # 衝突判定
        if kk_rct.colliderect(bomb_rct):
            bg_gameover_rct = bomb.get_rect()
            scr =pg.Surface((WIDTH,HEIGHT),flags=pg.SRCALPHA)
            scr.fill((0,0,0,200))
            font = pg.font.Font(None, 80)
            txt = font.render(str("Game Over"), True, (255,255,255))
            kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"),0,2.0)
            screen.blit(scr,bg_gameover_rct)
            screen.blit(kk_img,[WIDTH/2-200,HEIGHT/2])
            screen.blit(kk_img,[WIDTH/2+400,HEIGHT/2])
            screen.blit(txt,[WIDTH/2,HEIGHT/2])
            pg.display.update()
            time.sleep(5)
            return 0

            # 環境変数
        tmr += 1
        clock.tick(50)

def check_bound(obj,x=True,y=True):
    if obj.left < 0 or WIDTH < obj.right:
        x = False
    if obj.top < 0 or HEIGHT < obj.bottom :
        y = False
    return (x,y)
def update_position(obj_k,obj_s,speed=5):
        vector_x = obj_s.x - obj_k.x
        vector_y = obj_s.y - obj_k.y
        distance = (vector_x**2 + vector_y**2)**0.5
        speed_x = speed * vector_x / distance
        speed_y = speed * vector_y / distance
        return (speed_x,speed_y)

# 動作 #
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
