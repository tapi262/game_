import pygame

import random
import os
import math
import time

pygame.font.init()

WIDTH=500
HEIGHT =500

Window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEW PACKMAN")
red_man= pygame.image.load(os.path.join(".\\d_packman.png"))
green_man= pygame.image.load(os.path.join(".\\packman.png"))

#red_pow=pygame.image.load(os.path.join(".\\red.png"))
navy_pow=pygame.image.load(os.path.join(".\\navy.png"))

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


bg=pygame.transform.scale(pygame.image.load(os.path.join(".\\bg.png")), (WIDTH, HEIGHT))

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

    def update_score(self, obj, score =0):
        """
        Jeśli trzeba przydziela punkty i ustawia piłeczkę w początkowym położeniu.
        """
        if (self.rect.y - obj.rect.y)**2 + (self.rect.x- obj.rect.x) <1600:
            score =score+1
        return score



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
    if math.fabs(obj1.x- obj2.x) < 50:
        if math.fabs(obj1.y - obj2.y) < 50:
            return True

def main():
    go =True
    fps =30
    live=3
    score=0

    good_pows=[]

    gpow_len=1

    bad_pows=[]

    bpow_len=1

    font= pygame.font.SysFont("algerian", 20)
    player_vel =5
    packman= Packman(300, 400)
    player= Player(300, 400)
    good_pow=Player_2()
    bad_pow=Player_3()
    times= pygame.time.Clock()

    def new_draw():
        Window.blit(bg, (0,0))
        lives = font.render(f"Lives: {live}", 1, (0, 0, 0))
        scores = font.render(f"Score: {score}", 1, (0, 0, 0))
        Window.blit(lives, (5, 3))
        Window.blit(scores, (5, 23))





        #for gp in good_pows:
         #   if collide(gp, player):
          #      print("kolizja")


        for godpow in good_pows:
            player.update_score(godpow)

        for badpow in bad_pows:
            badpow.draw(Window)
        for goodpow in good_pows:
            goodpow.draw(Window)

        player.draw(Window)
        #good_pow.draw(Window)
        #bad_pow.draw(Window)

        pygame.display.update()



    while go:
        times.tick(fps)
        new_draw()
        vel=3
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

        for el in pygame.event.get():
            if el.type == pygame.QUIT:
                go = False


        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.y - player_vel > 430:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y +player_vel + 80< HEIGHT:
            player.y += player_vel
        if keys[pygame.K_LEFT] and player.x - player_vel >0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + 80 < WIDTH:
            player.x += player_vel

        for gp in good_pows:
            if collide(gp, player):
                good_pows.remove(gp)
                score +=1
        for bp in bad_pows:
            if collide(bp, player) is True:
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

        new_draw()




main()