import pygame

import random
import os
import math
import time

pygame.font.init()
pygame.init()
WIDTH=500
HEIGHT =500

Window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEW PACKMAN")
#red_man= pygame.image.load(os.path.join(".\\d_packman.png"))
green_man= pygame.image.load(os.path.join("c:/Users/48724/PycharmProjects/pythonProject13/packman.png"))

#red_pow=pygame.image.load(os.path.join(".\\red.png"))
navy_pow=pygame.image.load(os.path.join("c:/Users/48724/PycharmProjects/pythonProject13/navy.png"))

useColorKey=True
def image_bg(name, useColorKey=True):
    path= os.path.join(".\\" + name)
    image = pygame.image.load(path)
    image = image.convert()
    if useColorKey is True:
        image= image.convert()
        c_key= image.get_at((0,0))
        image.set_colorkey(c_key, pygame.RLEACCEL)
    return image


bg=pygame.transform.scale(pygame.image.load(os.path.join("c:/Users/48724/PycharmProjects/pythonProject13/bg.png")), (WIDTH, HEIGHT))
#BG = pygame.transform.scale(pygame.image.load(os.path.join(".\\black.png")), (WIDTH, HEIGHT))
class Packman:
    def __init__(self, x, y, health=100):
        self.x=x
        self.y=y
        self.health=health
        self.packman_img= None
        self.pow_img=None
        self.pow=[]
        self.cool_down_counter=0

    def draw(self, window):
        window.blit(self.packman_img, (self.x, self.y))
        pygame.display.flip()

class good_Bullet():
    def __init__(self, health=100):
        self.x=random.randint(10, WIDTH-10)
        self.y=random.randint(0, 100)
        self.health=health
        self.packman_img= None
        self.pow_img=None
        self.pow=[]
        self.cool_down_counter=0
        self.y_velocity=random.randint(1, 5)


    def draw(self, window):
        window.blit(self.pow_img, (self.x, self.y))
        pygame.display.flip()

class bad_Bullet():
    def __init__(self, health=100):
        self.x=random.randint(10, WIDTH-10)
        self.y=random.randint(0, 100)
        self.health=health
        self.packman_img= None
        self.pow_red_img=None
        self.pow=[]
        self.cool_down_counter=0
        self.y_velocity=random.randint(1, 5)

    def draw(self, window):
        window.blit(self.pow_red_img, (self.x, self.y))
        pygame.display.flip()


class Player(Packman):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.packman_img = image_bg("packman.png")
        self.pow_img= navy_pow
        self.mask = pygame.mask.from_surface(self.packman_img)
        self.max_health= health
        self.rect = self.packman_img.get_rect()
    def get_width(self):
        return self.packman_img.get_width()
    def get_height(self):
        return self.packman_img.get_height()




class Player_2(good_Bullet):
    def __init__(self, health=100):
        super().__init__(health)
        startpos=(self.x, self.y)
        self.pow_img=image_bg("navy.png")
        self.mask = pygame.mask.from_surface(self.pow_img)
        self.max_health= health
        self.rect = self.pow_img.get_rect()
    def move(self, vel):
        self.y += vel
    def get_height(self):
        return self.pow_img.get_height()
    def get_width(self):
        return self.pow_img.get_width()
    def collision(self, obj):
        return collide(self, obj)


class Player_3(bad_Bullet):
    def __init__(self, health=100):
        super().__init__(health)
        startpos=(self.x, self.y)
        self.pow_red_img=image_bg("red.png")
        self.mask = pygame.mask.from_surface(self.pow_red_img)
        self.max_health= health
        self.rect = self.pow_red_img.get_rect()
    def move(self, vel):
        self.y += vel
    def get_height(self):
        return self.pow_red_img.get_height()
    def get_width(self):
        return self.pow_red_img.get_width()



def collide(obj1, obj2):
    #if math.fabs((obj1.x)- (obj2.x)) < 40:
        #if math.fabs((obj1.y) - (obj2.y)) < 40:
            #return True
    if ((obj1.x+40)- (obj2.x+15))**2 + ((obj1.y+30) - (obj2.y+15))**2 < 1650:
        return True

def main():
    go =True
    fps =30
    live=3
    score=0

    good_pows=[]

    gpow_len=1

    bad_pows=[]

    bpow_len=0

    font= pygame.font.SysFont("algerian", 20)
    font1 = pygame.font.SysFont("algerian", 40)
    player_vel =5
    packman= Packman(300, 400)
    player= Player(300, 400)
    good_pow=Player_2()
    bad_pow=Player_3()
    times= pygame.time.Clock()
    lost = False
    lost_count = 0
    def new_draw():
        Window.blit(bg, (0,0))
        lives = font.render(f"Lives: {live}", 1, (0, 0, 0))
        scores = font.render(f"Score: {score}", 1, (0, 0, 0))
        Window.blit(lives, (5, 3))
        Window.blit(scores, (5, 23))






        #for gp in good_pows:
         #   if collide(gp, player):
          #      print("kolizja")

        for badpow in bad_pows:
            badpow.draw(Window)
        for goodpow in good_pows:
            goodpow.draw(Window)

        player.draw(Window)
        #good_pow.draw(Window)
        #bad_pow.draw(Window)
        if lost:
            lost_label = font1.render("LOST!!!", 1, (0,0,0))
            Window.blit(lost_label, (200, 200))
            newgame = font.render("press mouse", 1, (0, 0, 0))
            Window.blit(newgame, (150, 100))

        pygame.display.update()

    while go:
        times.tick(fps)
        new_draw()
        vel=3

        if live <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > fps :
                go = False
            else:
                continue

        if len(good_pows)==0:
            gpow_len+=1
            for i in range(0, gpow_len):
                good_pow=Player_2()
                good_pows.append(good_pow)

        if len(bad_pows) == 0:
            bpow_len += 1
            for i in range(0, bpow_len):
                bad_pow = Player_3()
                bad_pows.append(bad_pow)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.y - player_vel > 430:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y +player_vel + 80< HEIGHT:
            player.y += player_vel
        if keys[pygame.K_LEFT] and player.x - player_vel >0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + 80 < WIDTH:
            player.x += player_vel
        if keys[pygame.K_ESCAPE]:
            go = False
        if keys[pygame.K_m]:
            main_menu()


        for gp in good_pows:
            if collide(player, gp):
                good_pows.remove(gp)
                score +=1
        for bp in bad_pows:
            if collide( player, bp) is True:
                bad_pows.remove(bp)
                live-=1
                if live<0:
                    print("LOST!")


        for gp in good_pows:
            good_vel = random.choice([ 1, 3])
            gp.move(good_vel)
            if gp.y+gp.get_height() > HEIGHT:
                good_pows.remove(gp)

        for bp in bad_pows:
            bad_vel = random.choice([1, 2, 3])
            bp.move(bad_vel)
            if bp.y+bp.get_height() > HEIGHT:
                bad_pows.remove(bp)

def main_menu():
    smallfont = pygame.font.SysFont('Arial', 30)
    Window.blit(bg, (0, 0))
    text1 = smallfont.render('quit', True, (255, 255, 255))
    text2 = smallfont.render('start', True, (255, 255, 255))
    text3 = smallfont.render('author', True, (255, 255, 255))
    text4 = smallfont.render('high score', True, (255, 255, 255))
    while True:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is terminated
                if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 <= mouse[1] <= HEIGHT / 2 + 40:
                    pygame.quit()
                if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2+40 <= mouse[1] <= HEIGHT / 2 + 80:
                    main()
                if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2+80 <= mouse[1] <= HEIGHT / 2 + 120:
                    menu()
                if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2+120 <= mouse[1] <= HEIGHT / 2 + 160:
                    best_game()
        mouse = pygame.mouse.get_pos()
        if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT/ 2 <= mouse[1] <= HEIGHT / 2 + 40:
            pygame.draw.rect(Window, (0,100,0), [WIDTH/ 2, HEIGHT / 2, 140, 40])
        else:
            pygame.draw.rect(Window, (0, 0, 0), [WIDTH / 2, HEIGHT / 2, 140, 40])
        Window.blit(text1, (WIDTH / 2 + 10, HEIGHT / 2))

        if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2+30 <= mouse[1] <= HEIGHT / 2 + 70:
            pygame.draw.rect(Window, (0, 100, 0), [WIDTH / 2, HEIGHT / 2+40, 140, 40])
        else:
            pygame.draw.rect(Window, (0, 0, 0), [WIDTH / 2, HEIGHT / 2+40, 140, 40])
        Window.blit(text2, (WIDTH / 2 + 10, HEIGHT / 2+40))

        if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 + 80 <= mouse[1] <= HEIGHT / 2 + 120:
            pygame.draw.rect(Window, (0, 100, 0), [WIDTH / 2, HEIGHT / 2 + 80, 140, 40])
        else:
            pygame.draw.rect(Window, (0, 0, 0), [WIDTH / 2, HEIGHT / 2 + 80, 140, 40])
        Window.blit(text3, (WIDTH / 2 + 10, HEIGHT / 2 + 80))

        if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 + 120 <= mouse[1] <= HEIGHT / 2 + 160:
            pygame.draw.rect(Window, (0, 100, 0), [WIDTH / 2, HEIGHT / 2 + 120, 140, 40])
        else:
            pygame.draw.rect(Window, (0, 0, 0), [WIDTH / 2, HEIGHT / 2 + 120, 140, 40])
        Window.blit(text4, (WIDTH / 2 + 10, HEIGHT / 2 + 120))




        # updates the frames of the game
        pygame.display.update()



def menu():
    go = True
    while go:
        keys = pygame.key.get_pressed()
        font = pygame.font.SysFont("algerian", 20)
        Window.blit(bg, (0, 0))
        game_label = font.render("o autorze slow kilka", 1, (0,0,0))
        Window.blit(game_label, (140, 10))
        pygame.display.update()
        for el in pygame.event.get():
            if el.type == pygame.QUIT:
                go = False
            if keys[pygame.K_m]:
                main_menu()
            if keys[pygame.K_ESCAPE]:
                go = False
                pygame.display.update()

    pygame.quit()
def best_game():
    go = True
    while go:
        keys = pygame.key.get_pressed()
        font = pygame.font.SysFont("algerian", 20)
        Window.blit(bg, (0, 0))
        game_label = font.render("The best score of game", 1, (0, 0, 0))
        Window.blit(game_label, (140, 10))
        pygame.display.update()
        for el in pygame.event.get():
            if el.type == pygame.QUIT:
                go = False
            if keys[pygame.K_m]:
                main_menu()
            if keys[pygame.K_ESCAPE]:
                go = False
                pygame.display.update()
    pygame.quit()

main_menu()