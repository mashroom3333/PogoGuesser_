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
SCREEN_SIZE_CENTER_X = SCREEN_SIZE_X // 2
SCREEN_SIZE_CENTER_Y = SCREEN_SIZE_Y // 2

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
        self.origin_r = 40.0
        self.r = self.origin_r
        self.color = 0
        self.speed = 0.8
        self.step = None

        self.target_r = self.Data.getColorR() #255
        self.target_g = self.Data.getColorG() #255
        self.target_b = self.Data.getColorB() #255

        self.get_step()

        self.dr_step = (255.0 - self.target_r) / self.step
        self.dg_step = (255.0 - self.target_g) / self.step
        self.db_step = (255.0 - self.target_b) / self.step

        
    def get_step(self):
        self.step = self.r // self.speed

    def update_size(self):
        self.r -= self.speed
        if self.r < 0:
            self.r = 0

    def draw(self, screen):
        if self.r > 0:
            
            ratio = 1.0 - (self.r / self.origin_r)
            
            curr_r = 255 + (self.target_r - 255) * ratio
            curr_g = 255 + (self.target_g - 255) * ratio
            curr_b = 255 + (self.target_b - 255) * ratio

            color = (int(curr_r),int(curr_g),int(curr_b))
            pygame.draw.circle(screen,color , (int(self.x), int(self.y)) , int(self.r))
        
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
        self.g = 4
        self.counter = 0
        self.max_counter = 30
        self.color_usui = random.uniform(0,240)
        
    
        self.v_x = random.uniform(self.vmax * -1,self.vmax) 
        self.v_y = random.uniform(self.vmax * -1,self.vmax) 
        self.r = random.uniform(4,9) 

    def update_counter(self):
        self.counter += 1
        self.y += self.g

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
        self.player_x = None
        self.player_y = None
        self.map = 1
        self.color_r = 255
        self.color_g = 255
        self.color_b = 255
        self.ready_to_ques = False
        self.need_reset = False
        self.distance = 0
    
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
    
    def setPlayerX(self,x):
        self.player_x = x
    def setPlayerY(self,y):
        self.player_y = y

    def getPlayerX(self):
        return self.player_x
    def getPlayerY(self):
        return self.player_y

    def setDistance(self,distance):
        self.distance = distance
    def getDistance(self):
        return self.distance

    def setAnsX(self,x):
        self.ans_x = x
    def setAnsY(self,y):
        self.ans_y = y

    def getAnsX(self):
        return self.ans_x
    def getAnsY(self):
        return self.ans_y

class MenuScene:
    def __init__(self,screen,data):
        self.Data = data
        self.screen = screen
        self.font = pygame.font.Font(None,60)
        self.map = None
        self.finished = False
        self.next_scene = None
        self.map1button = MenuMapButton(self.screen,self.Data,1)
        self.map2button = MenuMapButton(self.screen,self.Data,2)
        self.map3button = MenuMapButton(self.screen,self.Data,3)
        self.colorvar_r = MenuColorBar(self.screen,self.Data,"red")
        self.colorvar_g = MenuColorBar(self.screen,self.Data,"green")
        self.colorvar_b = MenuColorBar(self.screen,self.Data,"blue")


    def buttonupdate(self):
        self.map1button.update()
        self.map2button.update()
        self.map3button.update()

    def barupdate(self):
        self.colorvar_r.update()
        self.colorvar_g.update()
        self.colorvar_b.update()

    def drawbutton(self):
        self.map1button.draw()
        self.map2button.draw()
        self.map3button.draw()

    def drawbar(self):
        self.colorvar_r.draw()
        self.colorvar_g.draw()
        self.colorvar_b.draw()

    def any_button_pushed(self):
        if (self.map1button.button_pushed == True):
            print("map1buttonwas pushed")
            return self.map1button.map
        if (self.map2button.button_pushed == True):
            print("map2buttonwas pushed")
            return self.map2button.map
        if (self.map3button.button_pushed == True):
            print("map3buttonwas pushed")
            return self.map3button.map
        
    def update(self):
        self.buttonupdate()
        self.barupdate()
        pass

    def draw(self):
        self.screen.fill((0,0,0))
        text = self.font.render("Press any key to exit", True,(255,255,255))
        rect = text.get_rect(center = self.screen.get_rect().center)
        pygame.draw.circle(self.screen,(self.Data.getColorR(),self.Data.getColorG(),self.Data.getColorB()),(400,300),50)
        self.screen.blit(text,rect)
        self.drawbutton()
        self.drawbar()

    def handle_events(self,event):
        self.map1button.handle_events(event)
        self.map2button.handle_events(event)
        self.map3button.handle_events(event)

        self.colorvar_r.handle_events(event)
        self.colorvar_g.handle_events(event)
        self.colorvar_b.handle_events(event)

        if(self.any_button_pushed()):
            self.Data.map = self.any_button_pushed()
            te = f"map{self.Data.map} was chosed"
            print(te)
            self.finished = True
            self.next_scene = "viewer"

class MenuMapButton:
    def __init__(self,screen,data,map):
        self.Data = data
        self.screen = screen
        self.font = pygame.font.Font(None,50)
        self.map = map
        self.width = 1000
        self.height = 50
        self.left_top_x = None
        self.offset= 20
        self.x1 = SCREEN_SIZE_CENTER_X - int(self.width / 2)
        self.y1 = SCREEN_SIZE_CENTER_Y + (self.height) * self.map
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height - self.offset
        self.color = 150
        self.button_pushed = False
        
    def check_on_mouse(self):
        mx,my = pygame.mouse.get_pos()
        if(self.x1 < mx and mx < self.x2) and (self.y1 < my and my < self.y2):
            self.change_color("light")
            return True
        else:
            self.change_color("dark")
            return False

    def change_color(self,str):
        if(str == "light"):
            self.color = 230
        if(str == "dark"):
            self.color = 150
    
    def drawMapStr(self):
        f = f"MAP{self.map}"
        
        text = self.font.render(f,True,(255,255,255))
        rect = text.get_rect()
        x = SCREEN_SIZE_CENTER_X - rect.width/2
        y = SCREEN_SIZE_CENTER_Y +self.height * self.map
        self.screen.blit(text,(x,y))

    def update(self):
        self.check_on_mouse()
        pass
    def draw(self):
        pygame.draw.rect(self.screen,(self.color,self.color,self.color),(self.x1, self.y1,self.width,self.height -self.offset))
        self.drawMapStr()

    def handle_events(self,event):
        if((event.type == MOUSEBUTTONDOWN) and (event.button == 1) and (self.check_on_mouse())):
            self.button_pushed = True
    
class MenuColorBar:
    def __init__(self,screen,data,color):
        self.Data = data
        self.screen = screen
        self.font = pygame.font.Font(None,60)
        self.width = 20
        self.height = 50
        self.left_top_x = None
        self.color = 150
        self.button_pushed = False
        self.offset= 20
        self.bar_value = 0
        self.color_name = color
        self.color= 0
        self.color_value = 0
        self.map = None
        self.bar_x_value = SCREEN_SIZE_CENTER_X - int(self.width / 2)
        self.dragging = False
        self.max_zahyou = 1400
        self.min_zahyou = 500


        if self.color_name == "red":
            self.map = 1
        elif self.color_name == "green":
            self.map = 2
        elif self.color_name == "blue":
            self.map = 3
        else:
            self.map = 1
        
        self.x1 = SCREEN_SIZE_CENTER_X - int(self.width / 2) + self.bar_value#左上の基準点
        self.y1 = SCREEN_SIZE_CENTER_Y + (self.height) + 200  + self.map * 40
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height - self.offset
        
    def check_on_mouse(self):
        mx,my = pygame.mouse.get_pos()
        if(self.x1 < mx and mx < self.x2) and (self.y1 < my and my < self.y2):
            self.change_color("light")
            return True
        else:
            self.change_color("dark")
            return False

    def change_color(self,str):
        if(str == "light"):
            self.color = 230
        if(str == "dark"):
            self.color = 150

    def update_values(self):
        self.x1 = self.bar_x_value - int(self.width / 2) #左上の基準点
        self.y1 = SCREEN_SIZE_CENTER_Y + (self.height) + 200  + self.map * 40
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height - self.offset

        self.color_value = (self.max_zahyou - self.bar_x_value) / (self.max_zahyou - self.min_zahyou)
        self.color_value = 255 - int(255 * self.color_value)

    def updateColors(self):
        if(self.color_name == "red"):
            self.Data.setColorR(self.color_value)
        elif(self.color_name == "green"):
            self.Data.setColorG(self.color_value)
        elif(self.color_name == "blue"):
            self.Data.setColorB(self.color_value)
    
    def update(self):
        self.check_on_mouse()
        self.update_values()
        self.updateColors()
        pass
    def draw(self):
        pygame.draw.line(self.screen,(128,128,128),(self.min_zahyou,int(((self.y1+self.y2)/2))),(self.max_zahyou, int((self.y1 + self.y2)/2)),5)
        pygame.draw.rect(self.screen,(self.color,self.color,self.color),(self.x1, self.y1,self.width,self.height - self.offset))

    def handle_events(self,event):
        if((event.type == MOUSEBUTTONDOWN) and (event.button == 1) and (self.check_on_mouse())):
            self.dragging = True
            self.button_pushed = True

        if event.type == MOUSEBUTTONDOWN and event.button == 1 and (self.check_on_mouse()):
            self.dragging = True
            mx,my = event.pos

        #ドラッグ中========================================
        if event.type == MOUSEMOTION and self.dragging:
            mx,my = event.pos
            if((self.min_zahyou) < mx and (mx < self.max_zahyou)):
                self.bar_x_value = mx
            
        if event.type == MOUSEBUTTONUP and event.button == 1:
            self.dragging = False


class ViwerScene: #推測画面クラス=============================================
    def __init__(self,screen,data):
        self.Data = data
        self.screen = screen
        self.finished = False
        self.next_scene = None
        self.map = self.Data.map
        self.mapimg = None
        self.mapimg_scaled = None
        self.mask_scaled = None
        self.rect_scaled = None
        self.choseable_mask = None
        self.choseable_img = None
        self.laser_origin_x = SCREEN_SIZE_CENTER_X
        self.laser_origin_y = SCREEN_SIZE_CENTER_Y
        self.laser_last_x = 0
        self.laser_last_y = 0
        self.hit_x = None
        self.hit_y = None
        self.marks = []
        self.perticles = []
        self.hit = None
        
        self.choseable_img = pygame.image.load(CHOSEABLE_AREA_IMG_PATH[self.Data.map]).convert_alpha()
        self.choseable_mask = pygame.mask.from_surface(self.choseable_img)
        
        self.choseable_points = []
        self.make_valid_points()
        self.set_ans()
        
        self.set_mapimg()
        self.set_new_ques(self.Data.getAnsX(), self.Data.getAnsY())
    
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
        x,y = random.choice(self.choseable_points)
        self.Data.setAnsX(x) 
        self.Data.setAnsY(y) 
        
    def set_map(self,map):
        self.map = map

    def set_mapimg(self):
        self.mapimg = pygame.image.load(MAP_FOR_GUESS_IMG_PATH[self.map]).convert_alpha()
        
    def reset(self):
        self.set_ans()
        self.set_new_ques(self.Data.getAnsX(), self.Data.getAnsY())
        self.laser_origin_x = SCREEN_SIZE_CENTER_X
        self.laser_origin_y = SCREEN_SIZE_CENTER_Y

    def reset_map(self):
        self.set_map(self.Data.map)
        self.choseable_img = pygame.image.load(CHOSEABLE_AREA_IMG_PATH[self.Data.map]).convert_alpha()
        self.choseable_mask = pygame.mask.from_surface(self.choseable_img)
        
        self.choseable_points = []
        self.make_valid_points()
        self.set_ans()
        
        self.set_mapimg()
        self.set_new_ques(self.Data.getAnsX(), self.Data.getAnsY())

    def set_new_ques(self,x,y):
        print("new question")
        if(self.Data.map == 1):
            g_bairitu =  int(1340/250) #とある地点に対してゲームと画像のピクセルを数えて求めた比率。
        if(self.Data.map == 2):
            g_bairitu = int(1860/300)
        if(self.Data.map == 3):
            g_bairitu = int(1300/330) #とある地点に対してゲームと画像のピクセルを数えて求めた比率。
            
        print(self.Data.map)
        print(g_bairitu)

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

    def is_map_correct(self):
        if(not self.map == self.Data.map):
            self.reset_map()
        else:
            return None


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
        pygame.draw.line(self.screen,(255,250,250),(self.laser_origin_x,self.laser_origin_y),(self.laser_last_x,self.laser_last_y),20)
                
    #------------------------------------------------------------------
    def update(self):
        self.pointing()
        self.is_map_correct()
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
        

class MapScene: #マップクラス=============================================
    def __init__(self,screen,data):
        self.Data = data
        self.screen = screen
        self.sw,self.sh = SCREEN_SIZE
        self.font = pygame.font.Font(None,60)
        self.font_mini = pygame.font.Font(None,40)
        self.finished = False
        self.next_scene = None
        self.map = self.Data.map
        self.mapimg_original = None
        self.mapimg_scaled = None
        self.mask_scaled = None
        self.rect_scaled = None
        self.scale = 1.0
        self.final_scale = 1.0
        self.img_x = 0
        self.img_y = 0
        self.distance = None

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
        self.mapimg_original = pygame.image.load(MAP_IMG_PATH[self.Data.map]).convert_alpha()

    def get_scaled(self):
        sw, sh = SCREEN_SIZE
        iw, ih = self.mapimg_original.get_size()
        base_scale = min(sw/ iw, sh/ih)

        self.final_scale = base_scale * self.scale
        self.w = int(iw * self.final_scale)
        self.h = int(ih * self.final_scale)
        self.mapimg_scaled = pygame.transform.smoothscale(self.mapimg_original, (self.w,self.h))

    def reset_map(self):
        self.scale = 1.0
        self.final_scale = 1.0
        self.img_x = 0
        self.img_y = 0
        self.set_map(self.Data.map)

        self.set_mapimg()
        self.get_scaled()
        print("リセットしました。現在のマップは")
        print(self.map)

    
    def scaling_value(self):
        if self.zoom_counter > 0:
            center_x = self.sw // 2 
            center_y = self.sh // 2 

            img_cx = (center_x - self.img_x)/self.final_scale
            img_cy = (center_y - self.img_y)/self.final_scale

            self.scale += self.wheel_direction * (self.zoom_counter * 0.02)
            self.scale = max(0.5,min(self.scale, 20))

            self.image_scaled = self.get_scaled()

            self.img_x = center_x - img_cx * self.final_scale
            self.img_y = center_y - img_cy * self.final_scale
            self.zoom_counter -= 1

    def check_answer_correct(self):
        ax = self.Data.getAnsX()
        ay = self.Data.getAnsY()
        px = self.Data.getPlayerX()
        py = self.Data.getPlayerY()
        print(ax)
        print(ay)
        print(px)
        print(py)
        
        dx = max(abs(ax - px),1)
        dy = max(abs(ay - py),1)

        distance = math.hypot(dx,dy)
        self.Data.setDistance(distance)
        print("distance is")
        print(distance)

    def is_map_correct(self):
        if(not self.map == self.Data.map):
            self.reset_map()
        else:
            return None

    def image_to_screen(img_x, img_y, center_x, center_y, scale):
        screen_w,screen_h = SCREEN_SIZE
        screen_x = (img_x - center_x) * scale + screen_w / 2
        screen_y = (img_y - center_y) * scale + screen_h / 2
        return screen_x, screen_y


    def screen_to_image(self, screen_x, screen_y):
        img_x = (screen_x - self.img_x) / self.final_scale
        img_y = (screen_y - self.img_y) / self.final_scale
        return img_x, img_y


    def update(self):
        self.scaling_value()
        self.is_map_correct()
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

            mx, my = event.pos
            player_x, player_y = self.screen_to_image(mx, my)

            self.Data.setPlayerX(player_x)
            self.Data.setPlayerY(player_y)
            self.check_answer_correct()
            self.Data.setNeedReset(True)
            
class AnswerScene:
    def __init__(self,screen,data):
        self.Data = data
        self.map = self.Data.map
        self.mapimg = pygame.image.load(MAP_IMG_PATH[self.map]).convert_alpha()
        self.mapimg_scaled = None
        self.screen = screen
        self.finished = False
        self.next_scene = None
        self.scale = 0
        self.scale_bool = False
        self.finalzahyou = None

    def keisan(self):
        px = self.Data.getPlayerX()
        py = self.Data.getPlayerY()
        ax = self.Data.getAnsX()
        ay = self.Data.getAnsY()

        midle_x = (px + ax) // 2
        midle_y = (py + ay) // 2

        dx = abs(px - ax)
        dy = abs(py - ay)
        print(self.mapimg.get_size()[1])
        print(self.mapimg.get_size()[0])

        print(dx)
        print(dy)
        if(dx < dy):
            self.scale = min(self.mapimg.get_size()[1]/dy,4)
        else:
            self.scale = min(self.mapimg.get_size()[0]/dx,4)

        print(self.scale)
        self.mapimg_scaled = pygame.transform.scale(self.mapimg,(int(self.mapimg.get_rect().width * self.scale),int(self.mapimg.get_rect().height * self.scale)))
        self.screen.blit(self.mapimg_scaled,(0,0))
        

    def update(self):
        pass

    def draw(self):
        pygame.draw.line(self.screen,(255,255,255),(0,0),(1920,1080),20)
        pass
    
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