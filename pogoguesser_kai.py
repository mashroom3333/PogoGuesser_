import pygame
import math
import sys
import os
import random
import numpy as np
import webbrowser
from pygame.locals import*



SCREEN_SIZE = (1920,1080)
SCREEN_SIZE_X = SCREEN_SIZE[0]
SCREEN_SIZE_Y = SCREEN_SIZE[1]
SCREEN_SIZE_CENTER_X = SCREEN_SIZE_X // 2
SCREEN_SIZE_CENTER_Y = SCREEN_SIZE_Y // 2

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


MAP_FOR_GUESS_IMG_PATH = {
    1: get_resource_path("assets/images/map1.png"),
    2: get_resource_path("assets/images/map2.png"),
    3: get_resource_path("assets/images/map3.png"),
}

MAP_IMG_PATH = {
    1: get_resource_path("assets/images/map1.jpeg"),
    2: get_resource_path("assets/images/map2.jpeg"),
    3: get_resource_path("assets/images/map3.jpeg"),
}

CHOSEABLE_AREA_IMG_PATH = {
    1: get_resource_path("assets/images/map1_choseable_area.png"),
    2: get_resource_path("assets/images/map2_choseable_area.png"),
    3: get_resource_path("assets/images/map3_choseable_area.png"),
}

ANOTHER_ASSETS_IMG_PATH = {
    "pogo": get_resource_path("assets/images/pogo.png"),
    "flag": get_resource_path("assets/images/flag.png"),
}

BACKGROUND_IMG_PATH = get_resource_path("assets/images/background.jpg")
LOGO_IMG_PATH = get_resource_path("assets/images/logo.png")
URL_BUTTON_IMG_PATH = get_resource_path("assets/images/urlbutton.png")
FONT_TIMER_PATH = get_resource_path("assets/fonts/digitalism.ttf")
DISTANCE_MAX = 100
DISTANCE_MAX_FOR_PERFECT = 30


URL = "https://store.steampowered.com/app/688130/Pogostuck_Rage_With_Your_Friends/"

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
        self.ans_x = 0
        self.ans_y = 0
        self.player_x = 0
        self.player_y = 0
        self.map = 1
        self.mode = "normal"
        self.color_r = 255
        self.color_g = 255
        self.color_b = 255
        self.ready_to_ques = False
        self.need_reset = False
        self.menuing = True
        self.distance = 0
        self.current_question = 1
        self.correct_answer = 0
        self.max_question = 3
        self.map1_chosearea_points = None
        self.map2_chosearea_points = None
        self.map3_chosearea_points = None
        self.image_chache = {}
        self.maintimer_ms = 0
        self.maintimer_active = False
        self.subtimer_ms = 0
        self.subtimer_active = False
        self.timeover = False

    def setMode(self,mode):
        self.mode = mode

    def getMode(self):
        return self.mode
        
    def reset_maintimer(self):
        self.maintimer_ms = 0
        self.maintimer_active = True

    def stop_maintimer(self):
        self.maintimer_active = False

    def get_time_str(self):
        minutes = self.maintimer_ms // 60000
        seconds = (self.maintimer_ms % 60000) // 1000
        ms = (self.maintimer_ms % 1000) // 10
        return f"{minutes:02}m {seconds:02}s {ms:02}ms"

    def reset_subtimer(self):
        self.subtimer_ms = 6000
        self.subtimer_active = True

    def stop_subtimer(self):
        self.subtimer_active = False

    def get_subtime_str(self):
        seconds = (self.subtimer_ms % 60000) // 1000
        ms = (self.subtimer_ms % 1000) // 10
        return f"{seconds:02}s {ms:02}ms"



    def addCorrectAnswer(self):
        self.correct_answer += 1

    def getCorrectAnswer(self):
        return self.correct_answer

    def get_image(self,path):
        if path not in self.image_chache:
            print(f"Loading image: {path}")
            self.image_chache[path] = pygame.image.load(path).convert_alpha()
        return self.image_chache[path]
    
    def getChoseableArea(self,map):
        if(map == 1):
            return self.map1_chosearea_points
        if(map == 2):
            return self.map2_chosearea_points
        if(map == 3):
            return self.map3_chosearea_points
    
    def setChoseableArea(self,map,points):
        if(map == 1):
            self.map1_chosearea_points = points
        if(map == 2):
            self.map2_chosearea_points = points
        if(map == 3):
            self.map3_chosearea_points = points
            
    def getMaxQ(self):
        return self.max_question
            
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

    def addCurrentQ(self):
        self.current_question += 1
        
    def isQuestionContinue(self):
        if(self.current_question <= self.max_question):
            return True
        else:
            return False

    def resetCurrentQues(self):
        self.current_question = 1

    def resetCorrectAns(self):
        self.correct_answer = 0
    

class MenuScene:
    def __init__(self,screen,data):
        self.Data = data
        self.screen = screen
        self.font = pygame.font.Font(None,60)
        self.map = None
        self.finished = False
        self.next_scene = None
        self.logo_img = pygame.image.load(LOGO_IMG_PATH)
        bairitu = 0.7
        width = self.logo_img.get_rect().width
        height = self.logo_img.get_rect().height
        self.logo_img = pygame.transform.smoothscale(self.logo_img,(width * bairitu,height*bairitu))
        self.map1button = MenuMapButton(self.screen,self.Data,1)
        self.map2button = MenuMapButton(self.screen,self.Data,2)
        self.map3button = MenuMapButton(self.screen,self.Data,3)
        self.colorvar_r = MenuColorBar(self.screen,self.Data,"red")
        self.colorvar_g = MenuColorBar(self.screen,self.Data,"green")
        self.colorvar_b = MenuColorBar(self.screen,self.Data,"blue")
        self.urlbutton = UrlButton(self.screen,self.Data)
        self.modebutton_normal = MenuModeButton(self.screen,self.Data,"normal")
        self.modebutton_timeattack = MenuModeButton(self.screen,self.Data,"timeattack")
        self.modebutton_perfect = MenuModeButton(self.screen,self.Data,"perfect")
        self.modebutton_long = MenuModeButton(self.screen,self.Data,"marathon")


    def buttonupdate(self):
        self.map1button.update()
        self.map2button.update()
        self.map3button.update()

    def barupdate(self):
        self.colorvar_r.update()
        self.colorvar_g.update()
        self.colorvar_b.update()

    def modebutton_update(self):
        self.modebutton_normal.update()
        self.modebutton_timeattack.update()
        self.modebutton_perfect.update()
        self.modebutton_long.update()

    def drawbutton(self):
        self.map1button.draw()
        self.map2button.draw()
        self.map3button.draw()

    def drawbar(self):
        self.colorvar_r.draw()
        self.colorvar_g.draw()
        self.colorvar_b.draw()
    
    def drawmodebutton(self):
        self.modebutton_normal.draw()
        self.modebutton_timeattack.draw()
        self.modebutton_perfect.draw()
        self.modebutton_long.draw()
        

    def drawlogo(self):
        width = self.logo_img.get_rect().width
        x = SCREEN_SIZE_CENTER_X - int(width / 2)
        y = 100
        self.screen.blit(self.logo_img,(x,y))

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

    def modetext(self): 
        mode = self.Data.getMode()
        if(mode == "normal"):#あほくせーｗ
            mode = "Normal"  #頭文字大文字嫌いなんだよな
        if(mode == "timeattack"):
            mode = "TimeAttack"
        if(mode == "perfect"):
            mode = "Perfect"
        if(mode == "marathon"):
            mode = "Marathon"
        t = f"Mode: {mode}"
        text = self.font.render(t,True,(255,255,255))
        tx = SCREEN_SIZE_CENTER_X - (text.get_rect().width / 2)
        self.screen.blit(text,(tx,800))
        
    def update(self):
        self.buttonupdate()
        self.barupdate()
        self.modebutton_update()
        pass

    def draw(self):
        self.screen.fill((30,30,50))
        text = self.font.render("Press Esc key to exit", True,(255,255,255))
        tex = SCREEN_SIZE_CENTER_X - text.get_rect().width / 2#La
        tey = 350
        text2 = self.font.render("Laser Color", True,(255,255,255))
        pygame.draw.circle(self.screen,(self.Data.getColorR(),self.Data.getColorG(),self.Data.getColorB()),(1600,900),50)
        self.screen.blit(text,(tex,tey))
        self.screen.blit(text2,(SCREEN_SIZE_CENTER_X - (text2.get_rect().width / 2), 1000))

        self.draw
        self.drawbutton()
        self.drawbar()
        self.drawlogo()
        self.drawmodebutton()
        self.modetext()
        self.urlbutton.draw()

    def handle_events(self,event):
        self.map1button.handle_events(event)
        self.map2button.handle_events(event)
        self.map3button.handle_events(event)

        self.colorvar_r.handle_events(event)
        self.colorvar_g.handle_events(event)
        self.colorvar_b.handle_events(event)
        self.urlbutton.handle_events(event)

        self.modebutton_normal.handle_events(event)
        self.modebutton_timeattack.handle_events(event)
        self.modebutton_perfect.handle_events(event)
        self.modebutton_long.handle_events(event)

        pushed_map = self.any_button_pushed()
        if pushed_map is not None:
            self.Data.map = pushed_map
            self.map1button.button_pushed = False
            self.map2button.button_pushed = False
            self.map3button.button_pushed = False
            self.Data.resetCurrentQues()
            self.Data.reset_maintimer()
            self.Data.resetCorrectAns()
            if(self.Data.getMode() == "marathon"):
                self.Data.reset_subtimer()
                self.Data.timeover = False

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
        self.y1 = SCREEN_SIZE_CENTER_Y + (self.height) * self.map - 150
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height - self.offset
        self.r = 150
        self.g = 150
        self.b = 150
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
            self.r = 255
            self.g = 200
            self.b = 0
        if(str == "dark"):
            self.r = 50
            self.g = 50
            self.b = 50
    
    def drawMapStr(self):
        f = f"MAP{self.map}"
        
        text = self.font.render(f,True,(255,255,255))
        rect = text.get_rect()
        x = SCREEN_SIZE_CENTER_X - rect.width/2
        y = SCREEN_SIZE_CENTER_Y +self.height * self.map - 150
        self.screen.blit(text,(x,y))

    def update(self):
        self.check_on_mouse()
        pass
    def draw(self):
        pygame.draw.rect(self.screen,(self.r,self.g,self.b),(self.x1, self.y1,self.width,self.height -self.offset))
        self.drawMapStr()

    def handle_events(self,event):
        if((event.type == MOUSEBUTTONDOWN) and (event.button == 1) and (self.check_on_mouse())):
            self.Data.reset_maintimer()
            self.button_pushed = True

class MenuModeButton:
    def __init__(self,screen,data,mode):
        self.Data = data
        self.screen = screen
        self.font = pygame.font.Font(None,50)
        self.width = 150
        self.height = 150
        self.left_top_x = None
        self.offset= 20
        self.mode = mode
        self.get_x_kizyun()

        self.y_offset = 120
        self.x1 = self.x_kizyun - int(self.width / 2)
        self.y1 = SCREEN_SIZE_CENTER_Y + 120
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height - self.offset
        self.r = 150
        self.g = 150
        self.b = 150
        self.button_pushed = False
        

    def get_x_kizyun(self):
        kizyun = 550
        if(self.mode == "normal"):
            self.x_kizyun =  kizyun + self.width * 1
        if(self.mode == "timeattack"):
            self.x_kizyun = kizyun + self.width * 2 + self.offset * 1
        if(self.mode == "perfect"):
            self.x_kizyun = kizyun + self.width * 3 + self.offset * 2
        if(self.mode == "marathon"):
            self.x_kizyun = kizyun + self.width * 4 + self.offset * 3
    
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
            self.r = 255
            self.g = 200
            self.b = 0
        if(str == "dark"):
            self.r = 50
            self.g = 50
            self.b = 50

    def is_mode_chosed(self):
        if(self.Data.getMode() == self.mode):
            self.y1 = SCREEN_SIZE_CENTER_Y + 80
            self.change_color("light")
        else:
            self.y1 = SCREEN_SIZE_CENTER_Y + 120
            self.change_color("dark")

    def update(self):
        self.check_on_mouse()
        self.is_mode_chosed()
        pass
    def draw(self):
        pygame.draw.rect(self.screen,(self.r,self.g,self.b),(self.x1, self.y1,self.width,self.height -self.offset))

    def handle_events(self,event):
        if ((event.type == MOUSEBUTTONDOWN) and (self.check_on_mouse())):
            self.Data.setMode(self.mode)
    
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
        self.perticles = []


        if self.color_name == "red":
            self.map = 1
        elif self.color_name == "green":
            self.map = 2
        elif self.color_name == "blue":
            self.map = 3
        else:
            self.map = 1
        
        self.x1 = SCREEN_SIZE_CENTER_X - int(self.width / 2) + self.bar_value#左上の基準点
        self.y1 = SCREEN_SIZE_CENTER_Y + (self.height) + 250  + self.map * 40
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
        self.y1 = SCREEN_SIZE_CENTER_Y + (self.height) + 250  + self.map * 40
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

    def make_perticles(self):
        new_perticle = Perticle(
            self.screen,
            1600,900,self.Data)
        self.perticles.append(new_perticle)
    
    def draw_perticles(self):
        for p in self.perticles[:]:
            p.update_counter()
            p.draw(self.screen)

            if p.is_dead():
                self.perticles.remove(p)


    def draw(self):
        pygame.draw.line(self.screen,(128,128,128),(self.min_zahyou,int(((self.y1+self.y2)/2))),(self.max_zahyou, int((self.y1 + self.y2)/2)),5)
        pygame.draw.rect(self.screen,(self.color,self.color,self.color),(self.x1, self.y1,self.width,self.height - self.offset))
        self.draw_perticles()

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

            self.make_perticles()
            
        if event.type == MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

class UrlButton:
    def __init__(self,screen,data):
        self.Data = data
        self.screen = screen
        self.font = pygame.font.Font(None,50)
        self.map = map
        self.left_top_x = None
        self.image = pygame.image.load(URL_BUTTON_IMG_PATH)
        self.x1 = 50
        self.y1 = 900
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height
        self.x2 = self.x1 + self.width
        self.y2 = self.y1 + self.height
        
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
            self.r = 255
            self.g = 200
            self.b = 0
        if(str == "dark"):
            self.r = 50
            self.g = 50
            self.b = 50
    
    def update(self):
        self.check_on_mouse()
        pass
    def draw(self):
        #pygame.draw.rect(self.screen,(255,255,255),(self.x1, self.y1,self.width,self.height))
        self.screen.blit(self.image,(self.x1,self.y1))

    def handle_events(self,event):
        if((event.type == MOUSEBUTTONDOWN) and event.button == 1 and self.check_on_mouse()):
            self.Data.reset_maintimer()
            self.button_pushed = True
            webbrowser.open(URL)

class ViwerScene: #推測画面クラス=============================================
    def __init__(self,screen,data):
        self.Data = data
        self.font = pygame.font.Font(None,100)
        self.font_mini = pygame.font.Font(None,60)
        self.font_maintimer = pygame.font.Font(None,100)
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
        self.question_finished = False
        self.backimg = pygame.image.load(BACKGROUND_IMG_PATH).convert_alpha()
        self.timer_width_max = 0
        self.subtimer_width_max = 0
        
        self.choseable_img = pygame.image.load(CHOSEABLE_AREA_IMG_PATH[self.Data.map]).convert_alpha()
        self.choseable_mask = pygame.mask.from_surface(self.choseable_img)
        
        if(self.Data.getChoseableArea(self.map) == None):
            self.Data.setChoseableArea(self.map,self.make_valid_points())
        self.set_ans()
        
        self.set_mapimg()
        self.set_new_ques(self.Data.getAnsX(), self.Data.getAnsY())
    
    def make_valid_points(self):
        w,h = self.choseable_mask.get_size()
        a = []
        
        for y in range(h):
            for x in range(w):
                if self.choseable_mask.get_at((x,y)):
                    a.append((x,y))
                    
        return a


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
        x,y = random.choice(self.Data.getChoseableArea(self.map))
        self.Data.setAnsX(x) 
        self.Data.setAnsY(y) 
        
    def set_map(self,map):
        self.map = map

    def set_mapimg(self):
        path =  MAP_FOR_GUESS_IMG_PATH[self.map]
        self.mapimg = self.Data.get_image(path)
        
    def reset(self):
        self.set_ans()
        self.set_new_ques(self.Data.getAnsX(), self.Data.getAnsY())
        self.laser_origin_x = SCREEN_SIZE_CENTER_X
        self.laser_origin_y = SCREEN_SIZE_CENTER_Y

    def reset_map(self):
        self.set_map(self.Data.map)

        path = CHOSEABLE_AREA_IMG_PATH[self.map]
        self.choseable_img = self.Data.get_image(path)
        self.choseable_mask = pygame.mask.from_surface(self.choseable_img)
        
        if self.Data.getChoseableArea(self.map) is None:
            points = self.make_valid_points()
            self.Data.setChoseableArea(self.map, points)
        # -----------------------------------
        
        self.choseable_points = []
        self.make_valid_points()
        self.set_ans()
        
        self.set_mapimg()
        self.set_new_ques(self.Data.getAnsX(), self.Data.getAnsY())

    def set_new_ques(self,x,y):
        print("new question")
        if(self.Data.map == 1):
            g_bairitu =  1340/125 #とある地点に対してゲームと画像のピクセルを数えて求めた比率。
        if(self.Data.map == 2):
            g_bairitu = 1860/300
        if(self.Data.map == 3):
            g_bairitu = 1300/160 #とある地点に対してゲームと画像のピクセルを数えて求めた比率。
            
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

                
    def draw_maintimer(self):
        if(not (self.Data.getMode() == "marathon")):
            time_text = self.font_maintimer.render(self.Data.get_time_str(), True, (0, 255, 0))
            
            timer_rect = time_text.get_rect()
            if(self.timer_width_max < timer_rect.width):
                self.timer_width_max = timer_rect.width
            self.screen.blit(time_text, (SCREEN_SIZE[0] - self.timer_width_max, 20)) 

    def draw_subtimer(self):
        if(self.Data.getMode() == "marathon"):
            timer_text = self.font_maintimer.render(self.Data.get_subtime_str(), True,(255,0,0))

            timer_rect = timer_text.get_rect()
            if(self.subtimer_width_max < timer_rect.width):
                self.subtimer_width_max = timer_rect.width

            self.screen.blit(timer_text,(SCREEN_SIZE_CENTER_X - self.subtimer_width_max / 2,20))

    def draw_details(self):
        text_1 = self.font_mini.render("left click : change laser origin",True,(255,255,255))
        text_2 = self.font_mini.render("M : map",True,(255,255,255))
        self.screen.blit(text_1,[0,SCREEN_SIZE[1]-120])
        self.screen.blit(text_2,[0,SCREEN_SIZE[1]-60])
        pass

    def draw_current_map_qestion(self):
        map = self.Data.map
        map_str = f"MAP:{map}"
        text_map = self.font.render(map_str,True,(255,255,255))
        t_rect = text_map.get_rect()
        tm_width = t_rect.width
        tm_height = t_rect.height
        self.screen.blit(text_map,(30,30))

        mode = self.Data.getMode()
        mode_str = f"Mode:{mode}"
        text_mode = self.font_mini.render(mode_str,True,(255,255,255))
        m_height = text_mode.get_rect().height

        self.screen.blit(text_mode,(30,tm_height + 30))
        

        if (not self.Data.getMode() == "marathon"):
            ima = self.Data.current_question
            max = self.Data.max_question
            nokori_game_counter =ima
            mondai_str = f"{nokori_game_counter}/{max}"

            text_mondai = self.font_mini.render(mondai_str,True,(255,255,255))
            self.screen.blit(text_mondai,(30, tm_height + m_height + 30))

    def draw_crosshair(self):
        length = 30
        x1 = SCREEN_SIZE_CENTER_X - int(length / 2)
        x2 = SCREEN_SIZE_CENTER_X + int(length / 2)
        y = SCREEN_SIZE_CENTER_Y

        pygame.draw.line(self.screen,(0,255,0),(x1,y),(x2,y),3)

        x = SCREEN_SIZE_CENTER_X
        y1 = SCREEN_SIZE_CENTER_Y - int(length / 2)
        y2 = SCREEN_SIZE_CENTER_Y + int(length / 2)
        
        pygame.draw.line(self.screen,(0,255,0),(x,y1),(x,y2),3)

    def draw_streak(self):
        if(self.Data.getMode() == "marathon"):
            y = 135
            streak_t = self.font.render("streaks:",True,(255,255,255))
            streak_width = streak_t.get_rect().width
            streak_height = streak_t.get_rect().height
            self.screen.blit(streak_t,(30,y))
            value = self.Data.getCorrectAnswer()

            value_t = self.font.render(f"{value}",True,(0,255,0))
            self.screen.blit(value_t,(streak_width + 40, y))


    def update(self):
        self.pointing()
        self.is_map_correct()
        if(self.Data.getNeedReset()):
            self.reset()
            if(self.Data.isQuestionContinue()):
                None
            else:
                if(not (self.Data.getMode() == "marathon")):
                    self.question_finished == True
                    self.finished = True
                    self.Data.resetCurrentQues()
                    self.next_scene = "result"
                    self.Data.stop_maintimer()
                
            self.Data.setNeedReset(False)

        

    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.backimg,(0,0))
        self.draw_marks()
        self.draw_perticles()
        self.draw_laser()
        self.draw_maintimer()
        self.draw_streak()
        self.draw_subtimer()
        self.draw_details()
        self.draw_current_map_qestion()
        self.draw_crosshair()

    def handle_events(self,event):
        if(event.type == KEYDOWN and event.key == K_m):
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
        self.font_maintimer = pygame.font.Font(None,100)
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
        self.maintimer_width_max = 0
        self.subtimer_width_max = 0

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

    def distance_keisan(self):
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
        if((self.Data.map == 1) or (self.Data.map == 3)):
            distance *= 2
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



    def draw_setumei(self):
        t1 = self.font_mini.render("drag : move",True,(255,255,255))
        t2 = self.font_mini.render("wheel : zoom",True,(255,255,255))
        t3 = self.font_mini.render("rightClick : answer",True,(255,255,255))
        t4 = self.font_mini.render("M : close map",True,(255,255,255))
        self.screen.blit(t1,[0,SCREEN_SIZE[1]-240])
        self.screen.blit(t2,[0,SCREEN_SIZE[1]-180])
        self.screen.blit(t3,[0,SCREEN_SIZE[1]-120])
        self.screen.blit(t4,[0,SCREEN_SIZE[1]-60])

    def draw_maintimer(self):
        if(not (self.Data.getMode() == "marathon")):
            time_text = self.font_maintimer.render(self.Data.get_time_str(), True, (0, 255, 0))
            
            timer_rect = time_text.get_rect()
            if(self.maintimer_width_max < timer_rect.width):
                self.maintimer_width_max = timer_rect.width
            self.screen.blit(time_text, (SCREEN_SIZE[0] - self.maintimer_width_max, 20)) 

    def draw_subtimer(self):
        if(self.Data.getMode() == "marathon"):
            timer_text = self.font_maintimer.render(self.Data.get_subtime_str(), True,(255,0,0))

            timer_rect = timer_text.get_rect()
            if(self.subtimer_width_max < timer_rect.width):
                self.subtimer_width_max = timer_rect.width

            self.screen.blit(timer_text,(SCREEN_SIZE_CENTER_X - self.subtimer_width_max / 2,20))

    def update(self):
        self.scaling_value()
        self.is_map_correct()
        pass

    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.mapimg_scaled,(self.img_x,self.img_y))
        self.draw_setumei()
        self.draw_maintimer()
        self.draw_subtimer()

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
            self.distance_keisan()
            self.Data.setNeedReset(True)
            self.Data.stop_subtimer()
            
class AnswerScene:
    def __init__(self,screen,data):
        self.Data = data
        self.font = pygame.font.Font(None,160)
        self.font_mini = pygame.font.Font(None,60)
        self.font_maintimer = pygame.font.Font(None,100)
        self.map = self.Data.map
        self.mapimg = self.Data.get_image(MAP_IMG_PATH[self.map])
        self.mapimg_scaled = None
        self.screen = screen
        self.finished = False
        self.next_scene = None
        self.scale = 0
        self.scale_bool = False
        self.finalzahyou = None
        self.final_img = None # 最初は空にしておく
        self.crop_x = None
        self.crop_y = None
        self.view_width = None
        self.view_height = None
        self.margin = 1.2
        self.min_view_width = 300
        self.min_view_height = int(300 * (9/16))
        self.pogo_img = pygame.image.load(ANOTHER_ASSETS_IMG_PATH["pogo"])
        self.pogo_img = pygame.transform.smoothscale(self.pogo_img,(50,50))
        self.flag_img = pygame.image.load(ANOTHER_ASSETS_IMG_PATH["flag"])
        self.flag_img = pygame.transform.smoothscale(self.flag_img,(50,50))
        self.pogo_rect = self.pogo_img.get_rect()
        self.flag_rect = self.flag_img.get_rect()
        self.maintimer_width_max = 0
    

    def scaling_image(self):
        # ===== 画面・画像サイズ =====
        sw, sh = self.screen.get_size()
        image_x, image_y = self.mapimg.get_size()

        # ===== 座標取得 =====
        ansx = self.Data.getAnsX()
        ansy = self.Data.getAnsY()
        playerx = self.Data.getPlayerX()
        playery = self.Data.getPlayerY()

        dx = max(abs(ansx - playerx), 1)
        dy = max(abs(ansy - playery), 1)

        mid_x = (ansx + playerx) / 2
        mid_y = (ansy + playery) / 2

        # ===== 画面アスペクト比 =====
        screen_ratio = sw / sh

        # ===== 表示領域サイズ計算 =====
        if dx / dy > screen_ratio:
            view_width = dx
            view_height = dx / screen_ratio
        else:
            view_height = dy
            view_width = dy * screen_ratio

        view_width *= self.margin
        view_height *= self.margin

        view_width = int(view_width)
        view_height = int(view_height)

        view_width  = max(view_width,  self.min_view_width)
        view_height = max(view_height, self.min_view_height)
        # ===== 切り抜きRect =====
        crop_x = int(mid_x - view_width / 2)
        crop_y = int(mid_y - view_height / 2)
        crop_rect = pygame.Rect(crop_x, crop_y, view_width, view_height)

        # ===== ① 画像内に収まる場合 =====
        if crop_rect.left >= 0 and crop_rect.top >= 0 and \
        crop_rect.right <= image_x and crop_rect.bottom <= image_y:

            sub_image = self.mapimg.subsurface(crop_rect)

        # ===== ② はみ出す場合：黒背景キャンバス =====
        else:
            canvas = pygame.Surface((view_width, view_height))
            canvas.fill((0, 0, 0))

            # 元画像を貼る位置
            blit_x = -crop_x
            blit_y = -crop_y

            canvas.blit(self.mapimg, (blit_x, blit_y))
            sub_image = canvas

        # ===== 最終変形 =====
        self.mapimg_scaled = pygame.transform.smoothscale(
            sub_image, (sw, sh)
        )

        self.crop_x = crop_x
        self.crop_y = crop_y
        self.view_width = view_width
        self.view_height = view_height

    def draw_points(self):
        sw, sh = self.screen.get_size()

        crop_x = self.crop_x
        crop_y = self.crop_y
        view_width = self.view_width
        view_height = self.view_height

        scale_x = sw / view_width
        scale_y = sh / view_height

        # 正解位置
        ax = self.Data.getAnsX()
        ay = self.Data.getAnsY()
        ans_screen_x = (ax - crop_x) * scale_x
        ans_screen_y = (ay - crop_y) * scale_y

        # プレイヤー位置
        px = self.Data.getPlayerX()
        py = self.Data.getPlayerY()
        player_screen_x = (px - crop_x) * scale_x
        player_screen_y = (py - crop_y) * scale_y


        rect_f = self.flag_img.get_rect()
        flag_x = ans_screen_x - (rect_f.width/2)
        flag_y = ans_screen_y - (rect_f.height/2)

        rect_p = self.pogo_img.get_rect()
        pogo_x = player_screen_x - (rect_p.width/2)
        pogo_y = player_screen_y - (rect_p.height/2)
        

        pygame.draw.line(
            self.screen,(255,255,255),
            (int(ans_screen_x),int(ans_screen_y)),(int(player_screen_x),int(player_screen_y)),
            5
        )

        self.screen.blit(self.flag_img,(flag_x,flag_y))
        self.screen.blit(self.pogo_img,(pogo_x,pogo_y))

    def draw_marubatu(self):
        cx = SCREEN_SIZE_CENTER_X
        cy = SCREEN_SIZE_CENTER_Y
        offset_y = 150
        r = 100

        if(self.is_answer_correct()):
            pygame.draw.circle(self.screen,(255,0,0),(cx,cy - offset_y), r, 20)
        else:
            pygame.draw.line(self.screen,(0,0,255),(cx - r,cy - r),(cx + r,cy+r),20)
            pygame.draw.line(self.screen,(0,0,255),(cx - r,cy + r),(cx + r,cy-r),20)

            
    def draw_distance(self):
        distance = self.Data.getDistance()
        t_d = f"distance:{math.floor(distance)}"
        td = self.font.render(t_d,True,(255,255,255))
        rect_td = td.get_rect()
        w = rect_td.width
        t1 = self.font_mini.render("rightClick : next",True,(255,255,255))
        rect_t1 = t1.get_rect()
        w1 = rect_t1.width
        self.screen.blit(t1,[SCREEN_SIZE_CENTER_X-(w1/2),SCREEN_SIZE_CENTER_Y + 400])
        self.screen.blit(td,[SCREEN_SIZE_CENTER_X- (w/2),SCREEN_SIZE_CENTER_Y + 250])

    def draw_maintimer(self):
        if(not (self.Data.getMode() == "marathon")):
            time_text = self.font_maintimer.render(self.Data.get_time_str(), True, (0, 255, 0))
            
            timer_rect = time_text.get_rect()
            if(self.maintimer_width_max < timer_rect.width):
                self.maintimer_width_max = timer_rect.width
            self.screen.blit(time_text, (SCREEN_SIZE[0] - self.maintimer_width_max, 20)) 

    def draw_subtimer(self):
        if(self.Data.getMode() == "marathon"):
            timer_text = self.font_maintimer.render(self.Data.get_subtime_str(), True,(255,0,0))
            timer_rect = timer_text.get_rect()
            self.screen.blit(timer_text,(SCREEN_SIZE_CENTER_X - timer_rect.width / 2,20))


    def is_answer_correct(self):
        distance = self.Data.getDistance()
        if(self.Data.getMode() == "perfect"):
            if(distance <= DISTANCE_MAX_FOR_PERFECT):
                return True
            if(distance > DISTANCE_MAX_FOR_PERFECT):
                return False
        else:
            if(distance <= DISTANCE_MAX):
                return True
            if(distance > DISTANCE_MAX):
                return False

    def update(self):
        self.map = self.Data.map
        self.mapimg = self.Data.get_image(MAP_IMG_PATH[self.map])
        if(self.mapimg_scaled == None):
            self.scaling_image()

    def draw(self):
        if(not self.mapimg_scaled == None):
            self.screen.blit(self.mapimg_scaled,(0,0))
            self.draw_marubatu()
            self.draw_points()
            self.draw_distance()
            self.draw_maintimer()
            self.draw_subtimer()

    def handle_events(self,event):
        if(event.type == MOUSEBUTTONDOWN and event.button == 3):
            if self.is_answer_correct() or (self.Data.getMode() == "normal"):
                if self.is_answer_correct():
                    self.Data.addCorrectAnswer()
                self.finished = True
                self.next_scene = "viewer"
                self.mapimg_scaled = None
                self.mapimg = None
                self.Data.addCurrentQ()
                self.Data.reset_subtimer()
            else:
                if (self.Data.getMode() == "marathon"):
                    self.finished = True
                    self.next_scene = "result"
                else:
                    self.finished = True
                    self.next_scene = "menu"
        

class ResultScene:
    def __init__(self,screen,data):
        self.Data = data
        self.font = pygame.font.Font(None,100)
        self.font_big = pygame.font.Font(None,150)
        self.font_very_big = pygame.font.Font(None,250)
        self.map = self.Data.map
        self.backimg = pygame.image.load(BACKGROUND_IMG_PATH).convert_alpha()
        self.screen = screen
        self.finished = False
        self.next_scene = None

    def draw_maintimer(self):
        if(not (self.Data.getMode() == "marathon")):
            time_text = self.font.render(self.Data.get_time_str(), True, (0, 255, 0))
            timer_rect = time_text.get_rect()
            x = SCREEN_SIZE_CENTER_X - (timer_rect.width //2)
            y = SCREEN_SIZE_CENTER_Y - (timer_rect.height //2)
            self.screen.blit(time_text, (x,y)) # 画面左上に表示

    def draw_mapname(self):
        map = self.Data.map
        map_str = f"MAP:{map}"
        t = self.font.render(map_str,True,(255,255,255))
        t_rect = t.get_rect()
        x = SCREEN_SIZE_CENTER_X - (t_rect.width//2)
        y = SCREEN_SIZE_CENTER_Y- (t_rect.height //2) - 70
        self.screen.blit(t,(x,y))

    def draw_how_many(self):
        if(self.Data.getMode() == "normal"):
            correct = self.Data.getCorrectAnswer()
            max = self.Data.getMaxQ()
            
            str = f"{correct} / {max}"
            t = self.font_big.render(str,True,(255,255,255))
            t_rect = t.get_rect()
            x = SCREEN_SIZE_CENTER_X - (t_rect.width//2)
            y = SCREEN_SIZE_CENTER_Y- (t_rect.height //2) + 100
            self.screen.blit(t,(x,y))
            
    def draw_streak(self):
        if(self.Data.getMode() == "marathon"):
            streak_t = self.font.render("streaks:",True,(255,255,255))
            streak_width = streak_t.get_rect().width
            streak_height = streak_t.get_rect().height
            st_x = SCREEN_SIZE_CENTER_X - (streak_width // 2)
            st_y = SCREEN_SIZE_CENTER_Y - (streak_height // 2)
            self.screen.blit(streak_t,(st_x,st_y))

            value = self.Data.getCorrectAnswer()
            value_t = self.font_very_big.render(f"{value}",True,(0,255,0))
            value_width = value_t.get_rect().width
            v_x = SCREEN_SIZE_CENTER_X - (value_width //2)
            v_y = st_y + 80
            self.screen.blit(value_t,(v_x,v_y))
            


    def update(self):
        pass

    def draw(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.backimg,(0,0))
        self.draw_maintimer()
        self.draw_how_many()
        self.draw_mapname()
        self.draw_streak()
    
    def handle_events(self,event):
        if(event.type == MOUSEBUTTONDOWN and event.button == 3):
            pass
            self.finished = True
            self.next_scene = "menu"
        
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
            "result":ResultScene(self.screen,self.Data),
        }

        
        self.set_scene("menu")

    def set_scene(self,name):
        self.scene = self.scenes[name]
        if name == "answer":
            self.scene = AnswerScene(self.screen,self.Data)
        else:
            self.scene = self.scenes[name]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                self.running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            else:
                self.scene.handle_events(event)
    
    def update(self):
        self.scene.update()
        dt = self.clock.get_time()

        if self.Data.maintimer_active:
            self.Data.maintimer_ms += dt

        if self.Data.subtimer_active:
            self.Data.subtimer_ms -= dt

        if self.Data.subtimer_ms < 0 and not self.Data.timeover:
            self.Data.timeover = True
            self.Data.stop_maintimer()
            self.set_scene("result")

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