import os
import sys
import time
import random
import pygame as pg


WIDTH, HEIGHT = 1100, 650

# キーバインドと移動量の定義
DELTA = {
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct:pg.Rect):
    """

    動くオブジェクトが画面端に当たってい無い場合、その方向に対しTrueを返します。
    返すtupleは(横,縦)の順番です。

    :param Rect obj_rct : こうかとん、または爆弾のRect
    :return: 真理値タプルを返します(横,縦)。画面内ならTrue、画面外ならFalse
    :rtype: (bool,bool)
    """
    yoko, tate = True,True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko,tate

def show_gameover(screen:pg.Surface)->None:
    """

    ゲームオーバー時の画面を描画します。

    :param: Surface screen : ゲーム画面の描画先
    """
    # 背景暗転部
    trans_img = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(trans_img,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    trans_img.set_alpha(150)
    trans_rct = trans_img.get_rect()
    screen.blit(trans_img,trans_rct)

    # GameOver文字表示部
    font = pg.font.Font(None,80)
    txt = font.render("Game Over",
                      True,(255,255,255))
    txt_rct = txt.get_rect(center=(WIDTH//2,HEIGHT//2))
    screen.blit(txt,txt_rct)

    # 泣いてるこうかとん表示部
    for i in range(2):
        nkk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.1)
        nkk_rct =  nkk_img.get_rect()
        nkk_rct.center = (WIDTH//2+200+(-400*i),HEIGHT//2)
        screen.blit(nkk_img,nkk_rct)

    
    pg.display.update()
    time.sleep(5)

def main():
    # 画面初期化
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    bg_img = pg.image.load("fig/pg_bg.jpg")  # 背景画像読み込み

    # こうかとん初期化
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾初期化
    bb_img = pg.Surface((20,20))
    bb_img.set_colorkey((0,0,0)) # 爆弾の背景画像を透過する
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy = +5,+5  # 爆弾の移動量初期化

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        screen.blit(bg_img, [0, 0])  # 背景描画

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            print("Game Over")
            show_gameover(screen)
            return

        # キー操作読み取り部
        key_lst = pg.key.get_pressed()  # キー操作読み取り
        sum_mv = [0, 0]
        for k in DELTA:
            if key_lst[k]:
                sum_mv[0] += DELTA[k][0]
                sum_mv[1] += DELTA[k][1]
        
        # こうかとんの移動反映
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)

        # 爆弾の移動反映
        bb_rct.move_ip(vx,vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
