import os
import random
import sys
import time
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

def get_bb_accs_imgs(limit:int)->tuple[list[int],list[pg.Surface]]:
    """
    加速度と拡大されていく画像を生成し返却します

    :param: int limit : 最大段階
    :return: [accs,imgs]:加速度と画像のtupleを返します。加速度と画像はlimitに渡した分の長さがあります
    :rtype: tuple[list[int],list[pg.Surface]]: [加速度s,画像s]
    """
    # 加速度のリスト
    accs = [a for a in range(1, limit+1)]

    # 拡大爆弾リスト
    imgs = [get_bb_img(i) for i in range(1, limit+1)]

    return (accs,imgs)

def get_bb_img(r:int)->pg.Surface:
    """
    渡された値の倍数分の画像を作成します
    :param: int r: 半径を何倍にするか設定する任意の値
    :return: bb_img: 爆弾の画像
    :rtype: pg.Surface
    """
    bb_img = pg.Surface((20*r,20*r))
    bb_img.set_colorkey((0,0,0)) # 爆弾の背景画像を透過する
    pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)

    return bb_img

def get_target_mv(target:pg.Rect,my:pg.Rect)->tuple[int]:
    """
    ターゲットに追従するためのベクトルを返します
    :param Rect target : ターゲット先のRect
    :param Rect my : 自身のRect
    :return: 速度ベクトル
    :rtype: tuple[int]
    """
    pass

def get_kk_img_map()->dict[tuple[int,int]:pg.Surface]:
    """
    
    飛ぶ方向に従うこうかとんの辞書を返えす関数

    :return: キー操作パターンをKeyとし、対応した画像を値とした辞書を返します
    :rtype: dict[tuple[int,int]:pg.Surface]
    """

    # 真ん中より左側3つ分のパターン
    mv_sums1 = (
        (-5,-5),(-5,0),(-5,5),
    )
    # 真ん中から右側5つ分のパターン
    mv_sums2 = (
        (0,-5),(5,-5),(5,0),
        (5,5),(0,5),
    )

    # 無動作時のパターンで初期化
    img_dict = {(0,0):pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)}

    # 真ん中より左側3つ分の画像作成
    for i in range(len(mv_sums1)):
        img_dict[mv_sums1[i]] = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45.0+45.0*float(i), 0.9)
    
    # 残り分作成
    for i in range(len(mv_sums2)):
        tmp = pg.transform.rotozoom(pg.image.load("fig/3.png"), -90+45.0*float(i), 0.9)
        img_dict[mv_sums2[i]] = pg.transform.flip(tmp, True, False)

    return img_dict

def main():
    # 画面初期化
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    bg_img = pg.image.load("fig/pg_bg.jpg")  # 背景画像読み込み

    # こうかとん初期化
    kk_imgs = get_kk_img_map()
    kk_img:pg.Surface = kk_imgs[(0,0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾初期化
    bb_accs, bb_imgs = get_bb_accs_imgs(10)
    bb_img = bb_imgs[0]
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
        kk_img = kk_imgs[tuple(sum_mv)]

        # こうかとんの移動反映
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)

        # 爆弾の移動反映
        bb_img = bb_imgs[min(tmr//500, 9)]
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx,avy)
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
