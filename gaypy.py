import pygame
import random
import os

WIN_SIZE = (1282,660)
size_hero = (60, 49)
tube_size = (148, 569)
BUTTON_SIZE = (200,80)
BG_COLOR = (113, 120, 207)
BLACK = (20,20,20)
FPS = 60

pygame.init()
window = pygame.display.set_mode(WIN_SIZE)
clock = pygame.time.Clock()

class Bird(pygame.Rect):
    def __init__(self, x, y, width, height, image_list, step):
        super().__init__(x, y, width, height)
        self.image_list = image_list
        self.image = self.image_list[0]
        self.image_count = 10
        self.change_image = int(FPS / 10)
        self.step = step
        self.start_x = self.x
        self.start_y = self.y
        self.move_check = {"up": False}
        self.gravity_power = 6
        self.static_jump = 15
        self.jump = 0

    def move_image(self):
        if self.image_count == len(self.image_list) * self.change_image - 1:
            self.image_count = 0
        if self.image_count % self.change_image == 0:
            self.image = self.image_list[self.image_count // self.change_image]
        self.image_count += 1

    def move(self, window):
        self.y += self.gravity_power

        if self.move_check["up"] and self.y > 0:
            self.jump = self.static_jump
        

        if self.jump != 0:
            self.y -= self.jump
            self.jump -= 1
            self.move_image()
        else:
            self.image = self.image_list[0]

        
        window.blit(self.image, (self.x, self.y))

class Tube(pygame.Rect):

    tube_list = list()

    def __init__(self, x, y, width, height, image, speed, orientation = False):
        super().__init__(x, y, width, height)
        self.image = image
        self.speed = speed
        if orientation:
            self.image = pygame.transform.flip(self.image, False, True)
        
    def move(self, window):
        self.x -= self.speed

        if self.x < - self.width:
            Tube.tube_list.remove(self)
        
        window.blit(self.image, (self.x, self.y))



class Button(pygame.Rect):
    def __init__(self,x,y,width,height,colors_background,colors_text,text):
        super().__init__(x,y,width,height)
        self.colors = colors_background
        self.colors_text = colors_text
        self.color = self.colors[0]
        self.font = pygame.font.SysFont("Robotic",40)
        self.text = self.font.render(text,True,self.colors_text[0])
        self.hover = False
        self.clicked = False
        self.calm = False

    def draw(self,window):
        if self.calm:
            self.color = self.colors[0]
            self.calm = False
        elif self.hover:
            self.color = self.colors[1]
        if self.clicked:
            self.color = self.colors[2]
            self.clicked = False
        pygame.draw.rect(window,self.color,self)
        window.blit(self.text,
                    (self.centerx - self.text.get_width()// 2,
                     self.centery - self.text.get_height() // 2))

    def active(self):
        if self.collidepoint(pygame.mouse.get_pos()):
            self.hover = True
            if pygame.mouse.get_pressed()[0]:
                self.clicked = True
                return True
            else:
                return False
        else:
            self.hover = False
            self.clicked = False 
            self.calm = True
            return False        

play_button = Button(WIN_SIZE[0]//2 - BUTTON_SIZE[0]//2,100,BUTTON_SIZE[0]
                     ,BUTTON_SIZE[1],((67, 14, 88),(148, 8, 69),(67, 52, 42)),
                     ((0,0,0),(148, 8, 67),(149, 255, 88)),"PLAY")

close_button = Button(WIN_SIZE[0]//2 - BUTTON_SIZE[0]//2,200,BUTTON_SIZE[0]
                     ,BUTTON_SIZE[1],((113, 85, 129),(203, 10, 0),(203, 10, 0)),
                     ((0,0,0),(134, 234, 67),(48, 69, 61)),"CLOSE")

abs_path = os.path.abspath(__file__+"/..")

hero_image_list = [
    pygame.transform.scale(pygame.image.load(os.path.join(abs_path, "hero0.png")), size_hero),
    pygame.transform.scale(pygame.image.load(os.path.join(abs_path, "hero0.png")), size_hero)
]

tube_image = pygame.transform.scale(pygame.image.load(os.path.join(abs_path, "tube.png")), tube_size)



game_over_text = pygame.font.Font(None,70).render("GAME OVER",True,BLACK)
font_count = pygame.font.Font(None,50)
        
hero = Bird(WIN_SIZE[0] // 2 - size_hero[0] // 2,
            10,
            size_hero[0],
            size_hero[1],
            hero_image_list,
            5)

font = pygame.font.Font(None, 60)


tube_speed = 2
score = 0
game = True
which_window = "MENU"
while game:
    events = pygame.event.get()
    if which_window == "MENU":
        window.fill(BG_COLOR)
        play_button.draw(window)
        close_button.draw(window)
        if play_button.active():
            which_window = "GAME"
            time_start = pygame.time.get_ticks()
            time_start1= pygame.time.get_ticks()
        if close_button.active():
            which_window = "CLOSE"
    elif which_window == "GAME":
        window.fill((255,255,255))

        window.blit(font.render(str(score), True, (255,255,255)), (WIN_SIZE[0] -75, 15))

        hero.move(window)

        end_time = pygame.time.get_ticks()
        if end_time - time_start >= 2500:
            time_start = end_time
            Tube.tube_list.append(
                Tube(WIN_SIZE[0],
                    random.randint (-tube_size[1] +200, 0),
                    tube_size[0],
                    tube_size[1],
                    tube_image,
                    2))
            Tube.tube_list.append(
                Tube(WIN_SIZE[0],
                    Tube.tube_list[-1].bottom + 200,
                    tube_size[0],
                    tube_size[1],
                    tube_image,
                    2,
                    orientation = True))

        for tube in Tube.tube_list:
            tube.move(window)

        score += tube_speed

        if hero.collidelist(Tube.tube_list) != -1:
            what_window = "game menu"
            Tube.tube_list = list()
            hero.x = hero.start_x
            hero.y = hero.start_y
            score = 0



        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    hero.move_check["up"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    hero.move_check["up"] = False
                


    elif which_window == "CLOSE":
        game = False
    elif which_window == "GAME MENU":
        window.blit(game_over_text,(WIN_SIZE(0) // 2- game_over_text.get_width() // 2,WIN_SIZE[1] // 2))
    
    for event in events:
        if event.type == pygame.QUIT:
            game = False

    clock.tick(60)       
    pygame.display.flip()
