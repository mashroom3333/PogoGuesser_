import pygame
import math
import sys
import os
import random
import numpy as np
from pygame.locals import*
from dataclasses import dataclass

SCREEN_SIZE = (1920,1080)
SCREEN_SIZE_X = SCREEN_SIZE[0]
SCREEN_SIZE_Y = SCREEN_SIZE[1]
MAP_FOR_GUESS_IMG_PATH = {
    1: "assets/map1.png",
    2: "assets/map2.png",
    3: "assets/map3.png",
}

MAP_IMG_PATH = {
    1: "assets/map1.jpeg",
    2: "assets/map2.jpeg",
    3: "assets/map3.jpeg",
}

CHOSEABLE_AREA_IMG_PATH = {
    1: "assets/map1_choseable_area.png",
    2: "assets/map2_choseable_area.png",
    3: "assets/map3_choseable_area.png",
}

class Hitmark:
    def __init__(self,screen,x,y,data):
        self.Data = data
        self.screen = screen
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
            cr = self.Data.getColorR()
            cg = self.Data.getColorG()
            cb = self.Data.getColorB()
            pygame.draw.circle(screen,(cr,230 - cg,230 - cb) , (int(self.x), int(self.y)) , int(self.r))
        
    def is_dead(self):
        return self.r <= 0
    
class Perticle:
    def __init__(self,screen,x,y,data):
        self.Data = data
        self.vmax = 3
        self.screen = screen
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
            cr = self.Data.getColorR()
            cg = self.Data.getColorG()
            cb = self.Data.getColorB()
            pygame.draw.circle(screen,(cr,cg,cb) , (int(self.x) + (self.counter  * self.v_x * 3.5), int(self.y) + (self.counter * self.v_y * 3.5)) , int(self.r))
        
    def is_dead(self):
        return self.counter >= self.max_counter

class Data:
    def __init__(self):
        self.ans_x = None
        self.ans_y = None
        self.map = None
        self.color_r = 255
        self.color_g = 0
        self.color_b = 0
        self.ready_to_ques = False
        self.need_reset = False
    
    def setColorR(self,x):
        self.color_r = x
    def setColorG(self,x):
        self.color_g = x
    def setColorB(self,x):
        self.color_b = x
    
    def getColorR(self):
        return self.color_r
    def getColorG(self):
        return self.color_g
    def getColorB(self):
        return self.color_b

    def setNeedReset(self,bool):
        self.need_reset = bool
    def getNeedReset(self):
        return self.need_reset
    

class MenuScene:
    def __init__(self,screen,data):
        self.Data = data
        self.screen = screen
        self.font = pygame.font.Font(None,60)
        self.map = None
        self.finished = False
        self.next_scene = None
    
    def set_map(self,map):
        self.map = map

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0,0,0))
        text = self.font.render("Press any key to exit", True,(255,255,255))
        rect = text.get_rect(center = self.screen.get_rect().center)
        self.screen.blit(text,rect)

    def handle_events(self,event):
        if(event.type == KEYDOWN):
            self.finished = True
            self.next_scene = "viewer"


class ViwerScene: #推測画面クラス=============================================
    def __init__(self,screen,data):
        self.Data = data
        self.screen = screen
        self.finished = False
        self.next_scene = None
        self.map = 1
        self.mapimg = None
        self.mapimg_scaled = None
        self.mask_scaled = None
        self.rect_scaled = None
        self.choseable_mask = None
        self.choseable_img = None
        self.ans_x = None
        self.ans_y = None
        self.laser_origin_x = 0
        self.laser_origin_y = 0
        self.laser_last_x = 0
        self.laser_last_y = 0
        self.hit_x = None
        self.hit_y = None
        self.marks = []
        self.perticles = []
        self.hit = None
        
        self.choseable_img = pygame.image.load(CHOSEABLE_AREA_IMG_PATH[self.map]).convert_alpha()
        self.choseable_mask = pygame.mask.from_surface(self.choseable_img)
        
        self.choseable_points = []
        self.make_valid_points()
        self.set_ans()
        
        self.set_mapimg()
        self.set_new_ques(self.ans_x, self.ans_y)
    
    def make_valid_points(self):
        w,h = self.choseable_mask.get_size()
        
        for y in range(h):
            for x in range(w):
                if self.choseable_mask.get_at((x,y)):
                    self.choseable_points.append((x,y))


    def image_to_screen(self,img_x, img_y, center_x, center_y, scale):
        screen_w,screen_h = SCREEN_SIZE
        screen_x = (img_x - center_x) * scale + screen_w / 2
        screen_y = (img_y - center_y) * scale + screen_h / 2
        return screen_x, screen_y

    def screen_to_image(self,screen_x, screen_y, center_x, center_y, scale):
        screen_w, screen_h = SCREEN_SIZE
        img_x = (screen_x - screen_w / 2) / scale + center_x
        img_y = (screen_y - screen_h / 2) / scale + center_y
        return img_x, img_y

    def set_ans(self):
        self.ans_x, self.ans_y = random.choice(self.choseable_points)
        
    def set_map(self,map):
        self.map = map

    def set_mapimg(self):
        self.mapimg = pygame.image.load(MAP_FOR_GUESS_IMG_PATH[self.map]).convert_alpha()
        
    def reset(self):
        self.set_ans()
        self.set_new_ques(self.ans_x, self.ans_y)

    def set_new_ques(self,x,y):
        if(self.map == 1):
            g_bairitu =  int(1340/250) #とある地点に対してゲームと画像のピクセルを数えて求めた比率。
        if(self.map == 2):
            g_bairitu = int(1860/300)
        if(self.map == 3):
            g_bairitu = int(1300/330) #とある地点に対してゲームと画像のピクセルを数えて求めた比率。
            
        src_w = int(1920 / g_bairitu)
        src_h = int(1080 / g_bairitu)

        src_rect = pygame.Rect(x-src_w // 2, y-src_h // 2, src_w, src_h)
        src_rect.clamp_ip(self.mapimg.get_rect())
        sub = self.mapimg.subsurface(src_rect)
        self.mapimg_scaled = pygame.transform.smoothscale(sub,(SCREEN_SIZE))
        self.mask_scaled = pygame.mask.from_surface(self.mapimg_scaled)
        self.rect_scaled = self.mask_scaled.get_rect()
        print("image scaled")
        print(self.mask_scaled)

    def pointing(self):
        mouse =pygame.mouse.get_pos()
        self.hit = self.hantei_collision(mouse)

    def hantei_collision(self,mouse):
        step = 1
        x1,y1 = self.laser_origin_x,self.laser_origin_y
        x2,y2 = mouse

        dx = x2 - x1
        dy = y2 - y1
        
        length = (dx*dx + dy*dy) **0.5
        if length == 0:
            return None
        
        ux = dx /length
        uy = dy /length
        
        max_len = (self.mask_scaled.get_size()[0] ** 2 + self.mask_scaled.get_size()[1]**2) ** 0.5
        steps = int(max_len // step)

        self.laser_last_x, self.laser_last_y = x1,y1

        for i in range(steps):
            px = int(x1 + ux * i * step)
            py = int(y1 + uy * i * step)

            if not (0 <= px < self.mask_scaled.get_size()[0] and 0 <= py < self.mask_scaled.get_size()[1]):
                break
                
            self.laser_last_x, self.laser_last_y = px,py

            if self.mask_scaled.get_at((px,py)):
                self.laser_last_x = px
                self.laser_last_y = py
                self.hit_x = px
                self.hit_y = py
                return True
        return None

    def change_laser_origin(self,x,y):
        if 0 <= x < self.mask_scaled.get_size()[0] and 0 <= y < self.mask_scaled.get_size()[1]:
            if not self.mask_scaled.get_at((x,y)):
                self.laser_origin_x = x
                self.laser_origin_y = y


    #---------描画系---------------------------------------------------------
    def draw_marks(self):
        if self.hit is not None:
            new_mark = Hitmark(
                self.screen,
                self.hit_x,self.hit_y,self.Data)
            self.marks.append(new_mark)

        for m in self.marks[:]:
            m.update_size()
            m.draw(self.screen)

            if m.is_dead():
                self.marks.remove(m)

    
    def draw_perticles(self):
        if self.hit is not None:
            new_perticle = Perticle(
                self.screen,
                self.hit_x,self.hit_y,self.Data)
            self.perticles.append(new_perticle)

        for p in self.perticles[:]:
            p.update_counter()
            p.draw(self.screen)

            if p.is_dead():
                self.perticles.remove(p)

    def draw_laser(self):
        cr = self.Data.getColorR()
        cg = self.Data.getColorG()
        cb = self.Data.getColorB()
        pygame.draw.line(self.screen,(cr,cg,cb),(self.laser_origin_x,self.laser_origin_y),(self.laser_last_x,self.laser_last_y),40)
        pygame.draw.line(self.screen,(255,150,150),(self.laser_origin_x,self.laser_origin_y),(self.laser_last_x,self.laser_last_y),30)
        pygame.draw.line(self.screen,(255,230,230),(self.laser_origin_x,self.laser_origin_y),(self.laser_last_x,self.laser_last_y),20)
                
    #------------------------------------------------------------------
    def update(self):
        self.pointing()
        if(self.Data.getNeedReset()):
            self.reset()
            self.Data.setNeedReset(False)

    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.mapimg_scaled,(0,0))
        self.draw_marks()
        self.draw_perticles()
        self.draw_laser()

    def handle_events(self,event):
        if(event.type == KEYDOWN):
            self.finished = True
            self.next_scene = "map"

        if(event.type == MOUSEBUTTONDOWN and event.button == 1):
            mx,my = event.pos
            self.change_laser_origin(mx,my)
        
        self.Data.setColorR(0)



class MapScene: #マップクラス=============================================
    def __init__(self,screen,data):
        self.Data = data
        self.screen = screen
        self.sw,self.sh = SCREEN_SIZE
        self.font = pygame.font.Font(None,60)
        self.font_mini = pygame.font.Font(None,40)
        self.finished = False
        self.next_scene = None
        self.map = 1
        self.mapimg_original = None
        self.mapimg_scaled = None
        self.mask_scaled = None
        self.rect_scaled = None
        self.ans_x = None
        self.ans_y = None
        self.scale = 1.0
        self.final_scale = 1.0
        self.img_x = 0
        self.img_y = 0

        self.dragging = False
        self.mouse_moving = False
        self.zoom_counter = 0
        self.wheel_direction = 0
        self.last_mx = 0
        self.last_my = 0
        
        
        self.set_mapimg()
        self.get_scaled()
    
    def set_map(self,map):
        self.map = map
    
    def set_mapimg(self):
        self.mapimg_original = pygame.image.load(MAP_IMG_PATH[self.map]).convert_alpha()

    def get_scaled(self):
        sw, sh = SCREEN_SIZE
        iw, ih = self.mapimg_original.get_size()
        base_scale = min(sw/ iw, sh/ih)

        self.final_scale = base_scale * self.scale
        self.w = int(iw * self.final_scale)
        self.h = int(ih * self.final_scale)
        self.mapimg_scaled = pygame.transform.smoothscale(self.mapimg_original, (self.w,self.h))
    
    def scaling_value(self):
        if self.zoom_counter > 0:
            center_x = self.sw // 2 
            center_y = self.sw // 2 

            img_cx = (center_x - self.img_x)/self.final_scale
            img_cy = (center_y - self.img_y)/self.final_scale

            self.scale += self.wheel_direction * (self.zoom_counter * 0.02)
            self.scale = max(0.5,min(self.scale, 20))

            self.image_scaled = self.get_scaled()

            self.img_x = center_x - img_cx * self.final_scale
            self.img_y = center_y - img_cy * self.final_scale
            self.zoom_counter -= 1


    def update(self):
        self.scaling_value()
        pass

    def draw_setumei(self):
        t1 = self.font_mini.render("drag : move",True,(255,255,255))
        t2 = self.font_mini.render("wheel : zoom",True,(255,255,255))
        t3 = self.font_mini.render("rightClick : answer",True,(255,255,255))
        t4 = self.font_mini.render("M : close map",True,(255,255,255))
        self.screen.blit(t1,[0,SCREEN_SIZE[1]-240])
        self.screen.blit(t2,[0,SCREEN_SIZE[1]-180])
        self.screen.blit(t3,[0,SCREEN_SIZE[1]-120])
        self.screen.blit(t4,[0,SCREEN_SIZE[1]-60])

    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.mapimg_scaled,(self.img_x,self.img_y))
        self.draw_setumei()

    def handle_events(self,event):
        if(event.type == KEYDOWN):
            self.finished = True
            self.next_scene = "viewer"

        if event.type == MOUSEWHEEL:
            self.wheel_direction = event.y
            self.zoom_counter = 5
        
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.dragging = True
            self.last_mx, self.last_my = event.pos
            mx,my = event.pos

        #ドラッグ中========================================
        if event.type == MOUSEMOTION and self.dragging:
            mx,my = event.pos
            dx = mx - self.last_mx
            dy = my - self.last_my

            self.img_x += dx
            self.img_y += dy

            self.last_mx = mx
            self.last_my = my
            
        if event.type == MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        if event.type == MOUSEBUTTONDOWN and event.button == 3:
            self.finished = True
            self.next_scene = "answer"
            self.Data.setNeedReset(True)

            
class AnswerScene:
    def __init__(self,screen,data):
        self.screen = screen
        self.finished = False
        self.next_scene = None

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0,0,0))
        pygame.draw.line(self.screen,(255,150,150),(0,0),(1900,1080),30)

    def handle_events(self,event):
        if(event.type == MOUSEBUTTONDOWN and event.button == 3):
            self.finished = True
            self.next_scene = "viewer"
        

class Game:#=================================ゲームクラス================================
    def __init__(self):
        pygame.init()

        self.Data = Data()
        self.screen = pygame.display.set_mode((SCREEN_SIZE))
        pygame.display.set_caption("test")
        self.clock = pygame.time.Clock()
        self.running = True
        self.scenes = {
            "menu":MenuScene(self.screen,self.Data),
            "map":MapScene(self.screen,self.Data),
            "viewer":ViwerScene(self.screen,self.Data),
            "answer":AnswerScene(self.screen,self.Data),
        }

        
        self.set_scene("menu")

    def set_scene(self,name):
        self.scene = self.scenes[name]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                self.running = False
            else:
                self.scene.handle_events(event)
    
    def update(self):
        self.scene.update()

        if self.scene.next_scene:
            next_name = self.scene.next_scene
            self.scene.next_scene = None
            self.set_scene(next_name)


    def draw(self):
        self.scene.draw()
        pygame.display.update()

    def run(self):
        while self.running:
            self.clock.tick(60)
            
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()