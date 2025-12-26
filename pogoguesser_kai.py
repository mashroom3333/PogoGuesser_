import pygame
import math
import sys
import os
import random
import numpy as np
from pygame.locals import*

SCREEN_SIZE = (1920,1080)
SCREEN_SIZE_X = SCREEN_SIZE[0]
SCREEN_SIZE_Y = SCREEN_SIZE[1]
MAP_FOR_GUESS_IMG_PATH = {
    1: "assets/map1.png",
    2: "assets/map2.png",
    3: "assets/map3.png",
}

class Hitmark:
    def __init__(self,screen,x,y):
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
            pygame.draw.circle(screen,(255,230-self.color,230 - self.color) , (int(self.x), int(self.y)) , int(self.r))
        
    def is_dead(self):
        return self.r <= 0
    
class Perticle:
    def __init__(self,screen,x,y):
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

class MenuScene:
    def __init__(self,screen):
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
            self.next_scene = ViwerScene


class ViwerScene:
    def __init__(self,screen):
        self.screen = screen
        self.finished = False
        self.next_scene = None
        self.map = 1
        self.mapimg = None
        self.mapimg_scaled = None
        self.mask_scaled = None
        self.rect_scaled = None
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
        
        self.set_mapimg()
        self.set_new_ques(1400,5300)
    
    def set_map(self,map):
        self.map = map

    def set_mapimg(self):
        self.mapimg = pygame.image.load(MAP_FOR_GUESS_IMG_PATH[self.map]).convert_alpha()

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

    def draw_marks(self):
        if self.hit is not None:
            new_mark = Hitmark(self.screen,self.hit_x,self.hit_y)
            self.marks.append(new_mark)

        for m in self.marks[:]:
            m.update_size()
            m.draw(self.screen)

            if m.is_dead():
                self.marks.remove(m)

    
    def draw_perticles(self):
        if self.hit is not None:
            new_perticle = Perticle(self.screen,self.hit_x,self.hit_y)
            self.perticles.append(new_perticle)
            
            for p in self.perticles[:]:
                p.update_counter()
                p.draw(self.screen)

                if p.is_dead():
                    self.perticles.remove(p)

    def draw_laser(self):
        pygame.draw.line(self.screen,(255,0,0),(self.laser_origin_x,self.laser_origin_y),(self.laser_last_x,self.laser_last_y),40)
        pygame.draw.line(self.screen,(255,150,150),(self.laser_origin_x,self.laser_origin_y),(self.laser_last_x,self.laser_last_y),30)
        pygame.draw.line(self.screen,(255,230,230),(self.laser_origin_x,self.laser_origin_y),(self.laser_last_x,self.laser_last_y),20)
                
    def update(self):
        self.pointing()

    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.mapimg_scaled,(0,0))
        self.draw_marks()
        self.draw_perticles()
        self.draw_laser()

    def handle_events(self,event):
        if(event.type == KEYDOWN):
            self.finished = True
            self.next_scene = MenuScene




class Game:#=================================ゲームクラス================================
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_SIZE))
        pygame.display.set_caption("test")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.scene = MenuScene(self.screen)
        self.set_scene(MenuScene(self.screen))

    def set_scene(self,scene):
        self.scene = scene

    def handle_events(self):
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                self.running = False
            else:
                self.scene.handle_events(event)
    
    def update(self):
        self.scene.update()

        if self.scene.next_scene:
            self.set_scene(self.scene.next_scene(self.screen))


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