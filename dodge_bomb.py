import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1600, 900
DELTA = {False:(0,0),
         pg.K_UP:(0,-5),
         pg.K_DOWN:(0,+5),
         pg.K_LEFT:(-5,0),
         pg.K_RIGHT:(+5,0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bomb = pg.Surface((20,20))
    pg.draw.circle(bomb,(255,0,0),(10,10),10)
    bomb.set_colorkey((0,0,0))
    bomb_rct = bomb.get_rect()
    bomb_rct.center = random.randint(400,1200),random.randint(225,675)
    vx,vy = 5,5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        kk_move = [0,0]
        for x,y in DELTA.items():
            if key_lst[x]:
                kk_move[0] += y[0]
                kk_move[1] += y[1]
        kk_rct.move_ip(kk_move)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-kk_move[0],-kk_move[1])
        screen.blit(kk_img, kk_rct)
        bomb_rct.move_ip(vx,vy)
        screen.blit(bomb,bomb_rct)
        vx *= 1 if check_bound(bomb_rct)[0] else -1
        vy *= 1 if check_bound(bomb_rct)[1] else -1
        pg.display.update()
        if kk_rct.colliderect(bomb_rct):
            return 0
        tmr += 1
        clock.tick(50)

def check_bound(obj,x=True,y=True):
    if obj.left < 0 or WIDTH < obj.right:
        x = False
    if obj.top < 0 or HEIGHT < obj.bottom :
        y = False
    return (x,y)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
