import pygame
import math
import sys
import os
import random
import numpy as np
from pygame.locals import*

def get_resource_path(relative_path):
    """ 
    実行時（exe）でも開発時（python script）でも
    正しいリソースへの絶対パスを返す関数
    """
    try:
        # PyInstallerで実行された時の一時フォルダのパスを取得
        base_path = sys._MEIPASS
    except AttributeError:
        # 通常のPython実行時は、このファイル（main.py等）がある場所を起点にする
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

SCREEN_SIZE = (1920,1080)
SCREEN_CENTER_X = 1920/2
SCREEN_CENTER_Y = 1080/2

MAP1_IMG_PATH = get_resource_path("assets/map1.jpeg")
MAP1_FOR_GUESS_IMG_PATH = get_resource_path("assets/map1.png")
MAP1_PICK_AREA_PATH  = get_resource_path("assets/map1_choseable_area.png")
MAP2_IMG_PATH = get_resource_path("assets/map2.jpeg")
MAP2_FOR_GUESS_IMG_PATH = get_resource_path("assets/map2.png")
MAP2_PICK_AREA_PATH  = get_resource_path("assets/map2_choseable_area.png")
MAP3_IMG_PATH = get_resource_path("assets/map3.jpeg")
MAP3_FOR_GUESS_IMG_PATH = get_resource_path("assets/map3.png")
MAP3_PICK_AREA_PATH  = get_resource_path("assets/map3_choseable_area.png")
BACKGROUND_IMG_PATH = get_resource_path("assets/background.jpg")

POGO_KING_PATH = get_resource_path("assets/pogo_king.png")
FLAG_PATH = get_resource_path("assets/flag.png")
GAME_KAISUU = 10

class Hitmark:
    def __init__(self,x,y):
        self.x = x 
        self.y = y 
        self.r = 40.0
        self.color = 0
        self.speed = 0.8
        
    def update_size(self):
        self.r -= self.speed
        self.color += 4
        
    def draw(self, screen):
        if self.r > 0:
            pygame.draw.circle(screen,(255,230-self.color,230 - self.color) , (int(self.x), int(self.y)) , int(self.r))
        
    def is_dead(self):
        return self.r <= 0
    
class Perticle:
    def __init__(self,x,y):
        self.vmax = 3
        self.x = x 
        self.y = y 
        self.r = 5.0
        self.g = 0.01
        self.counter = 0
        self.max_counter = 30
        self.color_usui = random.uniform(0,240)
        
    
        self.v_x = random.uniform(self.vmax * -1,self.vmax) 
        self.v_y = random.uniform(self.vmax * -1,self.vmax) 
        self.r = random.uniform(4,9) 

    def update_counter(self):
        self.counter += 1

    def draw(self, screen):
        if self.counter < self.max_counter:
            pygame.draw.circle(screen,(255,self.color_usui,self.color_usui) , (int(self.x) + (self.counter  * self.v_x * 3.5), int(self.y) + (self.counter * self.v_y * 3.5)) , int(self.r))
        
    def is_dead(self):
        return self.counter >= self.max_counter


def hantei_mask(screen, mask, rect, start, end, step=1):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1

    length = (dx*dx + dy*dy) ** 0.5
    if length == 0:
        return None

    ux = dx / length
    uy = dy / length

    # マスク（または画面）の対角線分だけ進めば十分
    max_len = (mask.get_size()[0]**2 + mask.get_size()[1]**2) ** 0.5
    steps = int(max_len // step)

    last_px, last_py = x1, y1

    for i in range(steps):
        px = int(x1 + ux * i * step)
        py = int(y1 + uy * i * step)

        # マスク範囲外に出たら終了
        if not (0 <= px < mask.get_size()[0] and 0 <= py < mask.get_size()[1]):
            break

        last_px, last_py = px, py

        if mask.get_at((px, py)):
            pygame.draw.line(screen, (255, 0, 0), (x1, y1), (px, py), 40)
            pygame.draw.line(screen, (255, 150, 150), (x1, y1), (px, py), 30)
            pygame.draw.line(screen, (255, 230, 230), (x1, y1), (px, py), 20)
            return (px, py)
            return (px, py)

    # ヒットしなかった場合でも、延長線を描画
    pygame.draw.line(screen, (255, 0, 0), (x1, y1), (last_px, last_py), 40)
    pygame.draw.line(screen, (255, 150, 150), (x1, y1), (last_px, last_py), 30)
    pygame.draw.line(screen, (255, 230, 230), (x1, y1), (last_px, last_py), 20)
    return None


def pointing(screen,mask_bg_edge,rect_bg,marks,perticles,my_center,mouse_moving):
    mouse = pygame.mouse.get_pos()

    hit_pos = hantei_mask(screen,mask_bg_edge,rect_bg,my_center,mouse)

    if hit_pos is not None:
        if(mouse_moving):
            new_mark = Hitmark(hit_pos[0],hit_pos[1])
            marks.append(new_mark)
            new_perticle = Perticle(hit_pos[0],hit_pos[1])
            perticles.append(new_perticle)
        
    for m in marks[:]:
        m.update_size()
        m.draw(screen)

        if m.is_dead():
            marks.remove(m)

    for p in perticles[:]:
        p.update_counter()
        p.draw(screen)

        if p.is_dead():
            perticles.remove(p)
    
def check_can_telepote(mx,my,mask):
    if 0 <= mx < mask.get_size()[0] and 0 <= my < mask.get_size()[1]:
        if not mask.get_at((mx, my)):
            return True

    
def set_position(x,y,mapimg_4guess,map):
    if(map == 1):
        honmono_bairitu =  int(1340/250) #とある地点に対してゲームと画像のピクセルを数えて求めた比率。
    if(map == 2):
        honmono_bairitu = int(1860/300)
    if(map == 3):
        honmono_bairitu = int(1300/330) #とある地点に対してゲームと画像のピクセルを数えて求めた比率。
        
    src_w = int(1920 / honmono_bairitu)
    src_h = int(1080 / honmono_bairitu)

    src_rect = pygame.Rect(
        x - src_w // 2,
        y - src_h // 2,
        src_w,
        src_h
    )
    src_rect.clamp_ip(mapimg_4guess.get_rect())
    sub = mapimg_4guess.subsurface(src_rect)
    image_scaled_2 = pygame.transform.smoothscale(sub,(1920,1080))
    mask_4guess = pygame.mask.from_surface(image_scaled_2)
    rect_4guess = mask_4guess.get_rect()

    return image_scaled_2,mask_4guess,rect_4guess

def get_ans_scaled(x, y, mapimg, scale):
    src_w = int(SCREEN_SIZE[0] / scale)
    src_h = int(SCREEN_SIZE[1] / scale)

    left = x - src_w // 2
    top  = y - src_h // 2
    right = src_w
    bottom = src_h

    src_rect = pygame.Rect(left, top,right,bottom)
    sub = mapimg.subsurface(src_rect)
    image = pygame.transform.smoothscale(sub, (SCREEN_SIZE[0], SCREEN_SIZE[1]))
    src_rect.clamp_ip(mapimg.get_rect())
    sub = mapimg.subsurface(src_rect)
    image = pygame.transform.smoothscale(sub,(1920,1080))

    return image

def image_to_screen(img_x, img_y, center_x, center_y, scale):
    screen_w,screen_h = SCREEN_SIZE
    screen_x = (img_x - center_x) * scale + screen_w / 2
    screen_y = (img_y - center_y) * scale + screen_h / 2
    return screen_x, screen_y


def main():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    my_center = (SCREEN_CENTER_X,SCREEN_CENTER_Y)#中心を任意の座標にする。要するにデバッグ用,明日のバイト鬱すぎる
    pygame.init()
    map = 1

    #VIEEWR用初期化
    mapimg_4guess = pygame.image.load(MAP1_FOR_GUESS_IMG_PATH).convert_alpha()
    ans_x = 0 
    ans_y = 0
    player_ans_x = 0
    player_ans_y = 0
    image_scaled_2,mask_4guess,rect_4guess = set_position(ans_x,ans_y,mapimg_4guess,map)

    #MAP用初期化
    mapimg = pygame.image.load(MAP1_IMG_PATH).convert_alpha()
    scale = 1.0

    sw, sh = SCREEN_SIZE
    def get_scaled():
        sw, sh = SCREEN_SIZE
        iw, ih = mapimg.get_size()
        base_scale = min(sw / iw, sh / ih)

        final_scale = base_scale * scale
        w = int(iw * final_scale)
        h = int(ih * final_scale)
        img = pygame.transform.smoothscale(mapimg, (w, h))
        return img, final_scale, w, h

    image_scaled, final_scale, new_w, new_h = get_scaled()
    print(final_scale)

    #正解発表用画像等初期化
    pogo_king = pygame.image.load(POGO_KING_PATH).convert_alpha()
    pogo_king = pygame.transform.smoothscale(pogo_king,(40,40))
    background_img = pygame.image.load(BACKGROUND_IMG_PATH).convert_alpha()

    flag_img = pygame.image.load(FLAG_PATH).convert_alpha()
    flag_img = pygame.transform.smoothscale(flag_img,(40,40))

    #MAP1用解答作成用マップ
    map_area_img = pygame.image.load(MAP1_PICK_AREA_PATH).convert_alpha()


    # 初期位置（中央）
    img_x = (sw - new_w) // 2
    img_y = (sh - new_h) // 2

    # ドラッグ管理
    dragging = False
    mouse_moving = False
    last_mx = last_my = 0
    zoom_counter = 0
    wheel_direction = 0

    marks = []
    perticles = []
    distane_arr = []
    current_mode = 4 #mode0はビューワー,mode1はマップ
    position_was_changed = 0

    def make_valid_points(mask):
        points = []
        w, h = mask.get_size()

        for y in range(h):
            for x in range(w):
                if mask.get_at((x, y)):
                    points.append((x, y))
        return points

    mask_area_choseable = pygame.mask.from_surface(map_area_img)
    choseable_area = make_valid_points(mask_area_choseable)


    def set_ans():
        x,y = random.choice(choseable_area)
        return x,y

    ans_x,ans_y = set_ans()
    image_scaled_2,mask_4guess,rect_4guess = set_position(ans_x,ans_y,mapimg_4guess,map)

    next_level = 0
    game_counter = GAME_KAISUU
    start = 0
    font = pygame.font.Font(None, 100)
    font_mini = pygame.font.Font(None, 60)
    gaming = False
    map1_loaded = False
    map2_loaded = False
    map3_loaded = False
    answer_correct = True
    choseable_area_1 = None
    choseable_area_2 = None
    choseable_area_3 = None
    show_result_surface = None

    while True:
        clock.tick(60)
        if (gaming):
            screen.blit(background_img,(0,0))
            ms = pygame.time.get_ticks() - start
            
            minutes = ms //60000
            seconds = (ms // 1000) % 60
            centiseconds = (ms % 1000) // 10

            time_str = f"{minutes:02}:{seconds:02}.{centiseconds:02}"
            text_time = font.render(time_str, True, (0,255,0))

            map_str = f"map:{map}"
            text_map = font.render(map_str,True,(255,255,255))
            nokori_game_counter = GAME_KAISUU - game_counter

            mondai_str = f"{nokori_game_counter}/{GAME_KAISUU}"
            text_mondai = font_mini.render(mondai_str,True,(255,255,255))

            if(game_counter == 0):
                result_time = time_str
                text_result_time = text_time = font.render(time_str, True, (0,255,0))
                print(np.average(distane_arr))
                current_mode = 5
                gaming = False
                
            if(next_level):
                ans_x,ans_y = set_ans()
                image_scaled_2,mask_4guess,rect_4guess = set_position(ans_x,ans_y,mapimg_4guess,map)
                next_level = 0
                game_counter -= 1
                my_center = (SCREEN_CENTER_X,SCREEN_CENTER_Y)#中心を任意の座標にする。要するにデバッグ用,明日のバイト鬱すぎる
                
            if(position_was_changed):
                image_scaled_2,mask_4guess,rect_4guess = set_position(ans_x,ans_y,mapimg_4guess,map)
                position_was_changed = 0
                

            if(current_mode == 0):
                pointing(screen,mask_4guess,rect_4guess,marks,perticles,my_center,mouse_moving)
                pygame.draw.circle(screen,(255,255,255),(SCREEN_CENTER_X,SCREEN_CENTER_Y),5)
                pygame.draw.circle(screen,(0,0,255),(SCREEN_CENTER_X,SCREEN_CENTER_Y),3)
                mouse_pressed = pygame.mouse.get_pressed()
                mx, my = pygame.mouse.get_pos()
                #screen.blit(image_scaled_2,(0 ,0 ))
                text_1 = font_mini.render("left click : change laser origin",True,(255,255,255))
                text_2 = font_mini.render("M : map",True,(255,255,255))
                screen.blit(text_1,[0,SCREEN_SIZE[1]-120])
                screen.blit(text_2,[0,SCREEN_SIZE[1]-60])

                
                if mouse_pressed[0]:
                    if(check_can_telepote(mx,my,mask_4guess)):
                        my_center= (mx,my)
            
            if(current_mode == 1):
                screen.fill((0,0,0))

                if zoom_counter > 0:
                    cx = sw // 2
                    cy = sh // 2

                    # 現在の中心位置を記録
                    img_cx = (cx - img_x) / final_scale
                    img_cy = (cy - img_y) / final_scale

                    scale += wheel_direction * (zoom_counter * 0.02)
                    scale = max(0.1, min(scale, 14.0))

                    image_scaled, final_scale, new_w, new_h = get_scaled()

                    # スケール後の位置を再計算
                    img_x = cx - img_cx * final_scale
                    img_y = cy - img_cy * final_scale
                    # カウンターを減らす
                    print(zoom_counter)
                    zoom_counter -= 1
                screen.blit(image_scaled, (img_x, img_y))

                t1 = font_mini.render("drag : move",True,(255,255,255))
                t2 = font_mini.render("wheel : zoom",True,(255,255,255))
                t3 = font_mini.render("rightClick : answer",True,(255,255,255))
                t4 = font_mini.render("M : close map",True,(255,255,255))
                screen.blit(t1,[0,SCREEN_SIZE[1]-240])
                screen.blit(t2,[0,SCREEN_SIZE[1]-180])
                screen.blit(t3,[0,SCREEN_SIZE[1]-120])
                screen.blit(t4,[0,SCREEN_SIZE[1]-60])

            if(current_mode == 2): # 正解発表
                screen.fill((0,0,0))

                screen_w, screen_h = SCREEN_SIZE
                img_orig_w, img_orig_h = mapimg.get_size()

                # 1. 画像が画面に収まるためのスケーリング比率を計算
                ratio = min(screen_w / img_orig_w, screen_h / img_orig_h)
                
                new_w = int(img_orig_w * ratio)
                new_h = int(img_orig_h * ratio)

                # 2. 中央に配置するためのオフセット計算
                offset_x = (screen_w - new_w) // 2
                offset_y = (screen_h - new_h) // 2

                screen.fill((0, 0, 0))

                draw_ans_x = int(ans_x * ratio + offset_x)
                draw_ans_y = int(ans_y * ratio + offset_y)
                
                draw_player_x = int(player_ans_x * ratio + offset_x)
                draw_player_y = int(player_ans_y * ratio + offset_y)

                # 正解の円
                distance = math.hypot(dx, dy)
                distane_arr.append(distance)

                dx = max(abs(ans_x - player_ans_x), 1)
                dy = max(abs(ans_y - player_ans_y), 1)
                
                scale_x = screen_w / dx
                scale_y = screen_h / dy
                scale2 = min(scale_x, scale_y)
                scale2 = min(scale2, 3)
                
                midle_x = (ans_x + player_ans_x) // 2
                midle_y = (ans_y + player_ans_y) // 2

                pogoking_x,pogoking_y = image_to_screen(ans_x,ans_y,midle_x,midle_y,scale2)
                flag_x,flag_y = image_to_screen(player_ans_x,player_ans_y,midle_x,midle_y,scale2)
                pygame.draw.line(screen, (255,255,255),(pogoking_x,pogoking_y),(flag_x,flag_y),3)
                screen.blit(pogo_king,(pogoking_x - 20,pogoking_y - 20))
                screen.blit(flag_img,(flag_x - 20,flag_y - 20))
                pygame.draw.circle(screen, (255, 0, 0), (draw_ans_x, draw_ans_y), 5)
                pygame.draw.circle(screen, (0, 0, 255), (draw_player_x, draw_player_y), 5)

                if(show_result_surface == None):
                    show_result_surface = get_ans_scaled(midle_x,midle_y,mapimg_4guess,scale2)
                screen.blit(show_result_surface,(0,0) )

                correct = False
                if((map == 1 or map == 3) and distance < 100):
                    correct = True
                elif(map == 2 and distance < 90):
                    correct = True
                else:
                    correct = False

                if(correct):
                    pygame.draw.circle(screen,(255,0,0),(SCREEN_CENTER_X,SCREEN_CENTER_Y), 100,10)
                else:
                    pygame.draw.line(screen,(0,0,255),(SCREEN_CENTER_X - 50,SCREEN_CENTER_Y - 50),(SCREEN_CENTER_X + 50,SCREEN_CENTER_Y+50),10)
                    pygame.draw.line(screen,(0,0,255),(SCREEN_CENTER_X - 50,SCREEN_CENTER_Y + 50),(SCREEN_CENTER_X + 50,SCREEN_CENTER_Y-50),10)
                    answer_correct = False

                t_d = f"distance:{math.floor(distance)}"
                td = font.render(t_d,True,(255,255,255))
                rect_td = td.get_rect()
                w = rect_td.width
                t1 = font_mini.render("rightClick : next",True,(255,255,255))
                rect_t1 = t1.get_rect()
                w1 = rect_t1.width
                screen.blit(t1,[SCREEN_CENTER_X-(w1/2),SCREEN_CENTER_Y - 100])
                screen.blit(td,[SCREEN_CENTER_X- (w/2),SCREEN_CENTER_Y-200])

            screen.blit(text_time,[SCREEN_SIZE[0]-300,0])
            screen.blit(text_map,[0,0])
            screen.blit(text_mondai,[0,100])
        else:
            if(current_mode == 4):
                screen.fill((0,0,0))
                te = font.render("Press Key 1,2,3", True, (255,255,255))
                te2 = font.render("to choose map", True,(255,255,255))

                tw = te.get_rect().width
                tw2 = te2.get_rect().width
                screen.blit(te,[SCREEN_CENTER_X-(tw/2),SCREEN_CENTER_Y])
                screen.blit(te2,[SCREEN_CENTER_X-(tw2/2),SCREEN_CENTER_Y + 60])
            
            if(current_mode == 5):
                tr_w = text_result_time.get_rect().width
                tm_w = text_map.get_rect().width
                screen.blit(text_result_time,[SCREEN_CENTER_X - (tr_w / 2),SCREEN_CENTER_Y - 50])
                screen.blit(text_map,[SCREEN_CENTER_X - (tm_w / 2),SCREEN_CENTER_Y - 150])


        mouse_moving = False
        pygame.display.update()
        #スーパーイベントタイム
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            if event.type == KEYDOWN and not current_mode == 4 and not current_mode == 2 and not current_mode == 5:
                if event.key == K_m:
                    if(current_mode == 0):
                        print("aj")
                        current_mode = 1
                    else:
                        print("b")
                        current_mode = 0
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_s:
                    ans_y += 500
                if event.key == K_d:
                    ans_x += 500
        
            if(current_mode == 0):
                if event.type == MOUSEMOTION:
                    mouse_moving = True
                    
            if(current_mode == 2):
                if event.type == MOUSEBUTTONDOWN and event.button == 3:
                    if not answer_correct:
                        current_mode = 5
                        gaming = False
                    else:
                        next_level = 1
                        current_mode = 0
                        ans_x,ans_y = set_ans()
                        zoom_counter =1
                    answer_correct = True
                    show_result_surface = None

            if(current_mode == 1):#マップモード
                # ===== ズーム（画面中心固定）=====
                if event.type == MOUSEWHEEL:
                    wheel_direction = event.y
                    zoom_counter = 5
                    print(wheel_direction)
                
                # ===== ドラッグ開始 =====
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    dragging = True
                    last_mx, last_my = event.pos

                    mx, my = event.pos
                    
                    original_x = (mx - img_x) / final_scale
                    original_y = (my - img_y) / final_scale

                    print(f"元画像座標:({original_x:.1f},{original_y:.1f})")

                # ===== ドラッグ終了 =====
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    dragging = False

                # ===== ドラッグ中 =====
                if event.type == MOUSEMOTION and dragging:
                    mx, my = event.pos
                    dx = mx - last_mx
                    dy = my - last_my

                    img_x += dx
                    img_y += dy

                    last_mx, last_my = mx, my          
                
                if event.type == MOUSEBUTTONDOWN and event.button == 3:
                    print("右クリックが押されました")
                    current_mode = 2 
                    mx, my = event.pos
                    
                    original_x = (mx - img_x) / final_scale
                    original_y = (my - img_y) / final_scale


                    print(f"元画像座標:({original_x:.1f},{original_y:.1f})")
                    position_was_changed = 1
                    player_ans_x = int(original_x)
                    player_ans_y = int(original_y)
                    
                    are_you_sure = 1
            if(current_mode == 4):
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        mapimg_4guess = pygame.image.load(MAP1_FOR_GUESS_IMG_PATH).convert_alpha()
                        mapimg = pygame.image.load(MAP1_IMG_PATH).convert_alpha()
                        map_area_img = pygame.image.load(MAP1_PICK_AREA_PATH).convert_alpha()
                        mask_area_choseable = pygame.mask.from_surface(map_area_img)
                        if(map1_loaded == False):
                            choseable_area_1 = make_valid_points(mask_area_choseable)
                            map1_loaded = True
                        choseable_area = choseable_area_1
                        map = 1
                        image_scaled, final_scale, new_w, new_h = get_scaled()
                        ans_x,ans_y = set_ans()
                        image_scaled_2,mask_4guess,rect_4guess = set_position(ans_x,ans_y,mapimg_4guess,map)
                        start = pygame.time.get_ticks()
                        current_mode = 0
                        gaming = True

                    if event.key == K_2:
                        mapimg_4guess = pygame.image.load(MAP2_FOR_GUESS_IMG_PATH).convert_alpha()
                        mapimg = pygame.image.load(MAP2_IMG_PATH).convert_alpha()
                        map_area_img = pygame.image.load(MAP2_PICK_AREA_PATH).convert_alpha()
                        mask_area_choseable = pygame.mask.from_surface(map_area_img)
                        if(map2_loaded == False):
                            choseable_area_2 = make_valid_points(mask_area_choseable)
                            map2_loaded = True
                        choseable_area = choseable_area_2
                        map = 2
                        image_scaled, final_scale, new_w, new_h = get_scaled()
                        ans_x,ans_y = set_ans()
                        image_scaled_2,mask_4guess,rect_4guess = set_position(ans_x,ans_y,mapimg_4guess,map)
                        start = pygame.time.get_ticks()
                        current_mode = 0
                        gaming = True

                    if event.key == K_3:
                        mapimg_4guess = pygame.image.load(MAP3_FOR_GUESS_IMG_PATH).convert_alpha()
                        mapimg = pygame.image.load(MAP3_IMG_PATH).convert_alpha()
                        map_area_img = pygame.image.load(MAP3_PICK_AREA_PATH).convert_alpha()
                        mask_area_choseable = pygame.mask.from_surface(map_area_img)
                        if(map3_loaded == False):
                            choseable_area_3 = make_valid_points(mask_area_choseable)
                            map3_loaded = True
                        choseable_area = choseable_area_3
                        map = 3
                        image_scaled, final_scale, new_w, new_h = get_scaled()
                        ans_x,ans_y = set_ans()
                        image_scaled_2,mask_4guess,rect_4guess = set_position(ans_x,ans_y,mapimg_4guess,map)
                        start = pygame.time.get_ticks()
                        current_mode = 0
                        gaming = True
                    
            if(current_mode == 5):
                if event.type == MOUSEBUTTONDOWN:
                    current_mode = 4
                    game_counter = GAME_KAISUU

        pygame.display.update()
if __name__ == "__main__":
    main()