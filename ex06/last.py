import pygame as pg
import random
import sys
from time import sleep
import schedule


MAX_SHOTS = 20  # most player bullets onscreen
ALIEN_ODDS = 22  # chances a new alien appears
BOMB_ODDS = 60  # chances a new bomb will drop
ALIEN_RELOAD = 12  # frames between new aliens
SCREENRECT = pg.Rect(0, 0, 640, 480)
SCORE = 0

count = 0    # 3000フレームをカウントする際に用いる変数

class Screen:
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title) 
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)
        self.bgi_rct = self.bgi_sfc.get_rect() 

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct) 


class Bird:#(pg.sprite.Sprite):
    speed = 10
    bounce = 24
    gun_offset = -11

    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img_path, ratio, xy):
        #pg.sprite.Sprite.__init__(self.containers)
        self.sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)
        self.rct = self.sfc.get_rect()
        self.reloading = 0
        self.rct.center = xy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def gunpos(self):
        pos =  self.gun_offset + self.rct.centerx
        return pos, self.rct.top

    def update(self, scr:Screen):
        key_dct = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_dct[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]  
            if check_bound(self.rct, scr.rct) != (+1, +1):
                self.rct.centerx -= delta[0]
                self.rct.centery -= delta[1]
        self.blit(scr)                    


#追加したかった機能：ビーム
class Shot:#(pg.sprite.Sprite):                                                

    def __init__(self, chr: Bird):
        #pg.sprite.Sprite.__init__(self, self.containers)
        self.sfc = pg.image.load("fig/beam.jfif")
        self.sfc = pg.transform.rotozoom(self.sfc, 0, 0.2)
        self.rct = self.sfc.get_rect()
        self.rct.midleft = chr.rct.center

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)
    
    def update(self, scr: Screen):
        self.rct.move_ip(+1, 0)
        # yoko, tate = check_bound(self.rct, scr.rct)
        # self.vx *= yoko
        # self.vy *= tate
        self.blit(scr)


class Bomb:
    def __init__(self, color, rad, vxy, scr:Screen):
        self.sfc = pg.Surface((2*rad, 2*rad)) # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = 0 #random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        self.blit(scr)


#追加機能：音楽
def sound():                                        
    pg.mixer.init(frequency = 44100)
    pg.mixer.music.load("../fig/Clav_Dungeon.mp3")
    pg.mixer.music.play(1)


def check_bound(obj_rct, scr_rct):
    """
    第1引数：こうかとんrectまたは爆弾rect
    第2引数：スクリーンrect
    範囲内：+1／範囲外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate

'''
↓　C0A21155 橋本健

3000フレームをカウントし、
3000フレームが経過した際にクリア画面に遷移するトリガーを作動させる、定義
'''

def count_keika(self,scr:Screen):  # 3000フレームを数える定義
    global count
    count += 1  # 1フレーム経つ毎に変数countを1ずつ大きくする
    if count < 3000:   # 3000フレーム経っていない場合
        print(count)
    elif count >= 3000:    #3000フレーム経った場合    
        keika = count / 100
        print(count)
        print(keika)
        self.game_state == CLEAR    # ステータスをCLEARにする(クリア画面に遷移する)

'''
↑　C0A21155 橋本健
'''

def main():
    clock =pg.time.Clock()

    # 練習１
    scr = Screen("負けるな！こうかとん", (1200,700), "../fig/pg_bg.jpg")

    # 練習３
    kkt = Bird("../fig/6.png", 2.0, (600,350))
    kkt.update(scr)


    # 練習５
    bkd_lst = []
    def mk_bomb(scr:Screen):
        for i in range(8):
            color = "red"
            vx = random.choice([-1,+1])
            vy = random.choice([-1,+1])
            bkd = Bomb(color, 10, (vx, vy),scr)
            bkd_lst.append(bkd)
    schedule.every(1).seconds.do(mk_bomb,scr=scr)
    
    # 練習２
    while True:        
        scr.blit()
        keystate = pg.key.get_pressed()
        firing = keystate[pg.K_SPACE]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        kkt.update(scr)
       
        for bomb in bkd_lst:
            bomb.update(scr)
            if kkt.rct.colliderect(bomb.rct):
                #追加機能：Game Over
                pg.mixer.music.stop()
                tori_sfc = pg.image.load("../fig/8.png")
                tori_sfc = pg.transform.rotozoom(tori_sfc, 0,8.0)
                tori_rct = tori_sfc.get_rect()
                tori_rct.center = 600,350
                scr.sfc.blit(tori_sfc,tori_rct)
                fonto = pg.font.Font(None,80)
                text = fonto.render("Game Over",True,"RED")
                scr.sfc.blit(text,(400,200))
                pg.display.update()
                clock.tick(1)  
                return
        
        schedule.run_pending()
        pg.display.update()
        
        count_keika()   # 3000フレーム数える定義を呼び出す　C0A21155 橋本健

        #sleep(1)
        clock.tick(1000)

        
if __name__ == "__main__":
    sound()
    pg.init()
    main()
    pg.quit()
    sys.exit()