import pygame
import random
import os
import time

#inicjalizacja okna gry, dodanie obrazów i postaci, dźwięków oraz ścieżęk
pygame.font.init()
pygame.init()
WIDTH=500
HEIGHT =500
g_sound = pygame.mixer.Sound("goood_sound.mp3")
b_sound = pygame.mixer.Sound("bad_sound.mp3")
path1 = ".\\wyniki.txt"
Window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NEW PACKMAN")
bg=pygame.transform.scale(pygame.image.load(os.path.join(".\\bg.png")), (WIDTH, HEIGHT))


useColorKey=True
def image_bg(name, useColorKey=True):
    """Funkcja do kowertowania obrazów, głowne zadanie to nadawanie przezroczystości tłu"""
    path= os.path.join(".\\" + name)
    image = pygame.image.load(path)
    image = image.convert()
    if useColorKey is True:
        image= image.convert()
        c_key= image.get_at((0,0))
        image.set_colorkey(c_key, pygame.RLEACCEL)
    return image



class Packman:
    """Klasa obiektu Packman, czyli głównego bohatera gry, nadająca mu współrzednę, wyrysowująca go na ekranie"""
    def __init__(self, x, y, health=100):
        self.x=x
        self.y=y
        self.packman_img= None

    def draw(self, window):
        window.blit(self.packman_img, (self.x, self.y))
        pygame.display.flip()

class good_Bullet():
    """Klasa obiektu good_Bullet, czyli diamencika dodającego punkty, z funkcją wyrysowującą na ekran"""
    def __init__(self, health=100):
        self.x=random.randint(40, WIDTH-40)
        self.y=random.randint(0, 100)
        self.packman_img= None
        self.pow_img=None
        self.pow=[]
        self.cool_down_counter=0
        self.y_velocity=random.randint(1, 5)


    def draw(self, window):
        window.blit(self.pow_img, (self.x, self.y))
        pygame.display.flip()

class bad_Bullet():
    """Klasa obiektu bad_Bullet, czyli diamencika odejmującego życia, z funkcją wyrysowującą na ekran"""
    def __init__(self, health=100):
        self.x=random.randint(10, WIDTH-30)
        self.y=random.randint(0, 100)
        self.packman_img= None
        self.pow_red_img=None
        self.pow=[]
        self.cool_down_counter=0
        self.y_velocity=random.randint(1, 5)

    def draw(self, window):
        window.blit(self.pow_red_img, (self.x, self.y))
        pygame.display.flip()


class Player(Packman):
    """Klasa dodająca wygląd Packmana, nadająca mu atrybut mask oraz funkcje wysokości i szerokości położenia, potrzebne w dalszych etapach"""
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.packman_img = image_bg("packman.png")
        self.mask = pygame.mask.from_surface(self.packman_img)
        self.rect = self.packman_img.get_rect()
    def get_width(self):
        return self.packman_img.get_width()
    def get_height(self):
        return self.packman_img.get_height()


class Player_2(good_Bullet):
    """Klasa dodająca obiektowi Bullet obraz, nadająca mu funckję swobodnego spadania, wysokości i szerokości położenia oraz kolizji"""
    def __init__(self, health=100):
        super().__init__(health)
        self.pow_img=image_bg("navy.png")
        self.mask = pygame.mask.from_surface(self.pow_img)
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
    """Klasa dodająca obiektowi Bullet obraz, nadająca mu funckję swobodnego spadania, wysokości i szerokości położenia oraz kolizji"""
    def __init__(self, health=100):
        super().__init__(health)
        self.pow_red_img=image_bg("red.png")
        self.mask = pygame.mask.from_surface(self.pow_red_img)
        self.rect = self.pow_red_img.get_rect()
    def move(self, vel):
        self.y += vel
    def get_height(self):
        return self.pow_red_img.get_height()
    def get_width(self):
        return self.pow_red_img.get_width()
    def collision(self, obj):
        return collide(self, obj)



def collide(obj1, obj2):
    """Funkcja sprawdzająca czy dwa objekty - obj1 oraz obj2  na siebie nachodzą, tu konkretnie chodzi o obiekty Bullet oraz Packamana. dlatego z góry został nadany promień"""
    #if math.fabs((obj1.x)- (obj2.x)) < 40:
        #if math.fabs((obj1.y) - (obj2.y)) < 40:
            #return True
    if ((obj1.x+40)- (obj2.x+15))**2 + ((obj1.y+30) - (obj2.y+15))**2 < 1650:
        return True

def sound(music):
    """Funkcja dodająca efekty dziękowe do zdarzeń, przyjmuje plik dźwiękowy"""
    music.play()
    time.sleep(0.07)
    music.stop()


def save_score(path, scorex):
    """Funkcja zapisująca wyniki - scorex, gry do pliku o ścieżce path"""
    if os.path.exists(path):
        open(path, "a").write(";" + str(scorex))
    else:
        f = open(path, "a")
        f.write("0;0")
        f.write(";" + str(scorex))
        f.close()

def get_score(path="wyniki.txt"):
    """Funkcja zwracająca z pliku z wynikami gry trzy najlepsze wyniki jako listę"""
    plik = open(path, "r")
    scores = []
    for el in plik.read().split(";"):
        scores.append(int(el))
    plik.close()
    high_score = sorted(scores)
    return  [high_score [-3], high_score [-2], high_score [-1]]


def main():
    """Funkcja wywołująca grę, adająca jej wszystkie parametry, kontroluje wszystkie pętle, ruchy klawiszami itp """
    go =True
    fps =30     #częstotliwość odświeżania
    live=3      #ilość żyć obiektu Packman
    score=0     #początkowa liczba punktów

    good_pows=[] #pudełko na obiekty typu Bullet oraz początkowe ilości wywolań tych obiektów
    gpow_len=1
    bad_pows=[]
    bpow_len=0

    font= pygame.font.SysFont("algerian", 20)       #czcionka
    font1 = pygame.font.SysFont("algerian", 40)

    player= Player(200, 400) #wywołanie obiektu Packman i nadanie pozycji początkowej
    player_vel = 5  # prędkość obiektu Packman
    times= pygame.time.Clock()

    lost = False #elementy do obsługi zdarzenia "końca gry"
    lost_count = 0

    def new_draw():
        """Funkcja wyrysowująca na ekran elementy, teksty oraz obiekty gry, zawiera pętle i obsługuje różne zdarzenia"""

        Window.blit(bg, (0,0)) #ustawianie tła, dodawnaie licznika żyć oraz punktów do ekranu
        lives = font.render(f"Lives: {live}", 1, (0, 0, 0))
        scores = font.render(f"Score: {score}", 1, (0, 0, 0))
        Window.blit(lives, (5, 3))
        Window.blit(scores, (5, 23))


        #for gp in good_pows:
         #   if collide(gp, player):
          #      print("kolizja")

        for badpow in bad_pows: #pętle dodające do okna gry elemnty Bullet
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

        #obsługa zdarzenia przegranej- utraty wszystkich żyć
        if live <= 0:
            lost = True
            lost_count += 1
        if lost:
            if lost_count > fps :
                go = False
                save_score("wyniki.txt", score)
            else:
                continue
        if lost: #dodanie inforamcji o przegranej na ekran
            lost_label = font1.render("LOST!!!", 1, (0,0,0))
            Window.blit(lost_label, (220, 20))

        if len(good_pows) == 0:
            gpow_len+=1
            for i in range(0, gpow_len):
                good_pow=Player_2()
                if random.randint(0,2)==1:
                    good_pows.append(good_pow)

        #dodawanie w pętli elemntów Bullet na ekran według zadanego tempa
        if len(bad_pows) == 0:
            bpow_len += 1
            for i in range(0, bpow_len):
                bad_pow = Player_3()
                if random.randint(0, 3) == 1:
                    bad_pows.append(bad_pow)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


        # obsługa klawiszy i poruszanie się Packmana
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

        # pętla obsługi zderzenia się obiektów typu Bullet z Packmanem
        for gp in good_pows:
            if collide(player, gp):
                good_pows.remove(gp)
                score +=1
                sound(g_sound)
        for bp in bad_pows:
            if collide( player, bp) is True:
                bad_pows.remove(bp)
                live-=1
                sound(b_sound)

        #pętla swobodnego spadania obiektów typu Bullet według zadanego tempa
        for gp in good_pows:
            good_vel= random.choice([ 2, 4])
            gp.move(random.choice([ 2, 4]))
            if gp.y+gp.get_height() > HEIGHT:
                good_pows.remove(gp)

        for bp in bad_pows:
            bad_vel = random.choice([1, 2, 3])
            bp.move(random.choice([1, 2, 3]))
            if bp.y+bp.get_height() > HEIGHT:
                bad_pows.remove(bp)



def main_menu():
    """Menu, pozwala na wybór pięciu opcji, wyjśćie, start gry, o autorze, najlepsze wyniki, zasady. Prosty manipualtor, opcje wybieramy myszką"""
    #czcionki, teksty, okno menu
    font = pygame.font.SysFont("algerian", 21)
    font1 = pygame.font.SysFont("algerian", 40)
    font2 = pygame.font.SysFont("algerian", 60)
    Window.blit(bg, (0, 0))
    n_packman=font2.render('NEWPACKMAN', True, (0,150 , 0))
    title=font1.render('MENU', True, (0, 190, 0))
    text1 = font.render('quit', True, (255, 255, 255))
    text2 = font.render('start', True, (255, 255, 255))
    text3 = font.render('author', True, (255, 255, 255))
    text4 = font.render('high score', True, (255, 255, 255))
    text5 = font.render('rules', True, (255, 255, 255))
    Window.blit(n_packman, (60, 70))
    Window.blit(title, (210, 140))


    #pętla zdarzeń wyboru danje opcji, nadanie miejśca i koloru przyciskom opcji
    while True:

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:

                # if the mouse is clicked on the
                # button the game is terminated
                if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 +50<= mouse[1] <= HEIGHT / 2 + 90:
                    pygame.quit()
                if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2+90 <= mouse[1] <= HEIGHT / 2 + 130:
                    main()
                if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2+130 <= mouse[1] <= HEIGHT / 2 + 170:
                    author()
                if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2+170 <= mouse[1] <= HEIGHT / 2 + 210:
                    best_game()
                if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2+210 <= mouse[1] <= HEIGHT / 2 + 250:
                    rules()
        mouse = pygame.mouse.get_pos()
        if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT/ 2 +50<= mouse[1] <= HEIGHT / 2 + 90:
            pygame.draw.rect(Window, (0,100,0), [WIDTH/ 2, HEIGHT / 2+50, 140, 40])
        else:
            pygame.draw.rect(Window, (0, 168, 0), [WIDTH / 2, HEIGHT / 2+50, 140, 40])
        Window.blit(text1, (WIDTH / 2 + 10, HEIGHT / 2+50))

        if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2+30+50 <= mouse[1] <= HEIGHT / 2 + 70+50:
            pygame.draw.rect(Window, (0, 100, 0), [WIDTH / 2, HEIGHT / 2+40+50, 140, 40])
        else:
            pygame.draw.rect(Window, (0, 168, 0), [WIDTH / 2, HEIGHT / 2+40+50, 140, 40])
        Window.blit(text2, (WIDTH / 2 + 10, HEIGHT / 2+40+50))

        if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 + 80+50 <= mouse[1] <= HEIGHT / 2 + 120+50:
            pygame.draw.rect(Window, (0, 100, 0), [WIDTH / 2, HEIGHT / 2 + 80+50, 140, 40])
        else:
            pygame.draw.rect(Window, (0, 168, 0), [WIDTH / 2, HEIGHT / 2 + 80+50, 140, 40])
        Window.blit(text3, (WIDTH / 2 + 10, HEIGHT / 2 + 80+50))

        if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 + 120+50 <= mouse[1] <= HEIGHT / 2 + 160+50:
            pygame.draw.rect(Window, (0, 100, 0), [WIDTH / 2, HEIGHT / 2 + 120+50, 140, 40])
        else:
            pygame.draw.rect(Window, (0, 168, 0), [WIDTH / 2, HEIGHT / 2 + 120+50, 140, 40])
        Window.blit(text4, (WIDTH / 2 + 10, HEIGHT / 2 + 120+50))
        if WIDTH / 2 <= mouse[0] <= WIDTH / 2 + 140 and HEIGHT / 2 + 160+50 <= mouse[1] <= HEIGHT / 2 + 200+50:
            pygame.draw.rect(Window, (0, 100, 0), [WIDTH / 2, HEIGHT / 2 + 160+50, 140, 40])
        else:
            pygame.draw.rect(Window, (0, 168, 0), [WIDTH / 2, HEIGHT / 2 + 160+50, 140, 40])
            Window.blit(text5, (WIDTH / 2 + 10, HEIGHT / 2 + 160+50))


        pygame.display.update()
    pygame.quit()


def author():
    """Funkcja wyświetlająca informację o autorze po wyborze takiej opcji w menu, z możliością powrotu do menu lub rozpoczęcia gry"""
    go = True
    #teksty, czcionki, miejsca na ekranie
    while go:
        keys = pygame.key.get_pressed()
        font = pygame.font.SysFont("algerian", 18)
        font1 = pygame.font.SysFont("algerian", 25)
        Window.blit(bg, (0, 0))
        title= font1.render("About author", 1, (0,0,0))
        text1=font.render("I am a student of applied mathematics,", 1, (0,0,0))
        text2= font.render("I wrote this game for the programming course.", 1, (0,0,0))
        text3 = font.render("I wrote them about 5 longer evenings.", 1, (0, 0, 0))
        text4 = font.render("I was inspired by childhood games.", 1, (0, 0, 0))
        text5 = font.render("This is my new version of pacman.", 1, (0, 0, 0))
        text6 = font.render("Press    m    to back menu or   g   to go game!", 1, (0, 0, 0))
        Window.blit(title, (140, 10))
        Window.blit(text1, (10,50))
        Window.blit(text2, (10, 80))
        Window.blit(text3, (10, 110))
        Window.blit(text4, (10, 140))
        Window.blit(text5, (10, 170))
        Window.blit(text6, (40, 350))


        pygame.display.update()
        #obsłuha opcji powrotu do menu, wyjścia oraz rozpoczęcia gry
        for el in pygame.event.get():
            if el.type == pygame.QUIT:
                go = False
            if keys[pygame.K_m]:
                main_menu()
            if keys[pygame.K_g]:
                main()
            if keys[pygame.K_ESCAPE]:
                go = False
                pygame.display.update()

    pygame.quit()

def rules():
    """Funkcja wyświetlająca zasady gry po wyborze takiej opcji w menu, z możliością powrotu do menu lub rozpoczęcia gry"""
    go = True
    #czcionki, teksty, umiejscowienie na ekranie
    while go:
        keys = pygame.key.get_pressed()
        font = pygame.font.SysFont("algerian", 15)
        font1 = pygame.font.SysFont("algerian", 25)
        Window.blit(bg, (0, 0))
        title= font1.render("RULES", 1, (0,0,0))
        text1 = font.render("in the game you have to get green crystals and avoid ", 1, (0, 0, 0))
        text2 = font.render("red ones. if you catch a green crystal you get score.", 1, (0, 0, 0))
        text3 = font.render("if you catch a red crystal you lose a life.", 1, (0, 0, 0))
        text4 = font.render("the game ends when you lose 3 lives", 1, (0, 0, 0))
        text5 = font.render(" you can show the best score.  at any stage of the  ", 1, (0, 0, 0))
        text6 = font.render("game you can return to the menu by pressing  'm'.", 1, (0, 0, 0))
        text7 = font.render("Press    'm'    to back menu or   'g'   to go game!", 1, (0, 0, 0))
        Window.blit(title, (140, 10))
        Window.blit(text1, (10, 50))
        Window.blit(text2, (10, 80))
        Window.blit(text3, (10, 110))
        Window.blit(text4, (10, 140))
        Window.blit(text5, (10, 170))
        Window.blit(text6, (10, 200))
        Window.blit(text7, (40, 350))

        pygame.display.update()
        # obsłuha opcji powrotu do menu, wyjścia oraz rozpoczęcia gry
        for el in pygame.event.get():
            if el.type == pygame.QUIT:
                go = False
            if keys[pygame.K_m]:
                main_menu()
            if keys[pygame.K_g]:
                main()
            if keys[pygame.K_ESCAPE]:
                go = False
                pygame.display.update()

    pygame.quit()

def best_game():
    """Funkcja korzystająca z pliku wyniki.txt, tworzy listę trzech anjlepszych wyników za pomocą wcześniej zdefiniowanej funkcji  po wyborze takiej opcji w menu, z możliością powrotu do menu lub rozpoczęcia gry"""
    go = True
    SCORES = get_score()  #funckja podaje 3 najlepsze wyniki

        #teksty, czcionki, miejsce na ekranie
    while go:
        keys = pygame.key.get_pressed()
        font1 = pygame.font.SysFont("algerian", 20)
        font2 = pygame.font.SysFont("algerian", 18)
        font = pygame.font.SysFont("algerian", 30)
        Window.blit(bg, (0, 0))
        title = font1.render("The best score of game", 1, (0, 0, 0))

        score1 = font.render(f"1st: {SCORES[2]}", 1, (0, 0, 0))
        score2 = font.render(f"2nd: {SCORES[1]}", 1, (0, 0, 0))
        score3 = font.render(f"3rd: {SCORES[0]}", 1, (0, 0, 0))
        text = font2.render("Press    'm'    to back menu or   'g'   to go game!", 1, (0, 0, 0))
        Window.blit(title, (140, 10))
        Window.blit(score1, (220, 50))
        Window.blit(score2, (220,100))
        Window.blit(score3, (220, 150))
        Window.blit(text, (40, 350))

        pygame.display.update()
        # obsłuha opcji powrotu do menu, wyjścia oraz rozpoczęcia gry
        for el in pygame.event.get():
            if el.type == pygame.QUIT:
                go = False
            if keys[pygame.K_m]:
                main_menu()
            if keys[pygame.K_ESCAPE]:
                go = False
                pygame.display.update()
    pygame.quit()
main_menu() #wywołanie menu jako pierwszego etapu gry