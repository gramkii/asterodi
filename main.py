from pygame import *
from random import *


w, h = 700, 500
window = display.set_mode((w, h))

display.set_caption("Астероидс")

clock = time.Clock()
game = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__(self,pImage, pX, pY, sizeX, sixeY, pSpeed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale           (image.load(pImage), (sizeX, sixeY))
        self.speed = pSpeed
        self.rect = self.image.get_rect()
        self.rect.x = pX
        self.rect.y = pY

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx -7, self.rect.top, 15,30, -15)
        bullets.add(bullet)

bullets = sprite.Group()


mixer.init()
mixer.music.load("kaboom.ogg")
mixer.music.play() 

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global hearts
        if self.rect.y >= h:
            try:
                hearts.pop(0)
            except:
                pass
            self.rect.x = randint(0, w -80)
            self.rect.y = 0
            lost += 1

background = transform.scale(image.load("sky.jpg"), (w, h))

ship = Player("f16.png", 10, h-130, 155, 145, 4)

asteroids = sprite.Group()
for i in range(1,6):
    randpic = randint(1,2)
    if randpic == 1:
        pic = "mig29.png"
    if randpic == 2:
        pic = "optimuspraim.png"
    asteroid = Enemy(pic, randint(10, w-50), -40, 90, 90, randint(1,5))
    asteroids.add(asteroid)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()
            ship_fire.play()


ship_fire = mixer.Sound("fire.ogg")
ship_fire.set_volume(0.1)
score = 0
font.init()
mainfont = font.SysFont("Arial", 40)
score_text = mainfont.render("Збитих" + str(score), True, (0,255,0))
lost_text = mainfont.render("Пропущених" + str(lost), True, (0, 255,0))

reload_time = False
num_fire = 0
from time import time as timer

lives = 10
hearts = []
heart_x = 250
for i in range(lives):
    heart = GameSprite("heart.png", heart_x, 10, 40, 39, 0)
    hearts.append(heart)
    heart_x += 35

restart = GameSprite("restartb.png", 255, 200, 200, 120, 0)

def gameloop():
    global game, finish, score, reload_time, num_fire, lost, hearts
    while game:
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if num_fire < 20 and reload_time == False:
                        ship.fire()
                        ship_fire.play()
                        num_fire += 1
                    if num_fire >= 20 and reload_time == False:
                        
                        reload_start = timer()
                        reload_time = True
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x,y = e.pos
                if restart.rect.collidepoint(x,y):
                    for a in asteroids:
                        a.rect.y = -100
                        a.rect.x = randint(0, w-100)
                    finish, lost, score = 0,0,0
                    lives = 10
                    hearts = []
                    heart_x = 250
                    for i in range(lives):
                        heart = GameSprite("heart.png", heart_x, 10, 40, 39, 0)
                        hearts.append(heart)
                        heart_x += 35

                     


        if not finish:
            window.blit(background, (0,0))
            score_text = mainfont.render("KILLED " + str(score), True, (0,255,0))
            lost_text = mainfont.render("MISSED " + str(lost), True, (0, 255,0))
            window.blit(score_text, (5,10))
            window.blit(lost_text, (5, 50))
            ship.draw()
            ship.update()

            bullets.draw(window)
            bullets.update()

            asteroids.draw(window)
            asteroids.update()


            collides = sprite.groupcollide(bullets, asteroids, True, True)
            for c in collides:
                randpic = randint(1,2)
                if randpic == 1:
                    pic = "mig29.png"
                if randpic == 2:
                    pic = "optimuspraim.png"
                asteroid = Enemy(pic, randint(10, w-50), -40, 90, 90, randint(1,5))
                asteroids.add(asteroid)
                score += 1
            print(score)

            if reload_time == True:
                reload_end = timer()
                if reload_end - reload_start < 3:
                    reload2 = mainfont.render("RELOADING" ,True , (255, 0 ,0))
                    window.blit(reload2, (260,170))
                else:
                    num_fire = 0
                    reload_time = False
                    
            if sprite.spritecollide(ship, asteroids, False):
                    restart.draw()
                    reload2 = mainfont.render("YOU LOSE" ,True , (255, 0 ,0))
                    window.blit(reload2, (260,200))
                    finish = True
            
            for heart in hearts:
                heart.draw()

            if len(hearts) <= 0:
                restart.draw()
                lose = mainfont.render("YOU LOSE", True, (255, 0 ,0))
                window.blit(lose, (200,200))
                finish = True

        display.update()
        clock.tick(60)
gameloop()