#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
window = display.set_mode((700,500)) 
display.set_caption('Шутер')
clock = time.Clock()
game = True
finish = False
prop = 0
score = 0
number = 0
life = 3
num_fire = 0
timer = 3
rel_time = False
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 36)
font3 = font.SysFont('Arial', 36)
win = font1.render('Ты победил!', True, (255,200,0))
lose = font2.render('ты проиграл!', True, (255,0,0))
lose1 = font3.render('К сожалению, ты потратил все жизни', True, (255,0,0))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
window.blit(background, (0, 0))
mixer.init()
mixer.music.load('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
mixer.music.play()
class GameSprite(sprite.Sprite): 
    def __init__(self,player_image,player_x,player_y,player_speed): 
        super().__init__() 
        self.image = transform.scale(image.load(player_image),(65,65)) 
        self.rect = self.image.get_rect() 
        self.speed = player_speed 
        self.rect.x = player_x 
        self.rect.y = player_y 
    def reset(self): 
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
           self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 635:
           self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15)
        bullets.add(bullet)
        
        
class Enemy(GameSprite):
    direction = 'down'
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 650)
            global prop
            prop += 1 
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()
rocket = Player('rocket.png', 50, 400, 4)
monster1 = Enemy('ufo.png', 450, -40, (randint(1, 5)))
monster2 = Enemy('ufo.png', 400, -40, (randint(1, 5)))
monster3 = Enemy('ufo.png', 350, -40, (randint(1, 5)))
monster4 = Enemy('ufo.png', 300, -40, (randint(1, 5)))
monster5 = Enemy('ufo.png', 250, -40, (randint(1, 5)))
asteroid1 = Enemy('asteroid.png', 400, -40, (randint(1, 5)))
asteroid2 = Enemy('asteroid.png', 375, -40, (randint(1, 5)))
asteroid3 = Enemy('asteroid.png', 425, -40, (randint(1, 5)))
asteroid4 = Enemy('asteroid.png', 350, -40, (randint(1, 5)))
asteroid5 = Enemy('asteroid.png', 325, -40, (randint(1, 5)))
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
asteroids.add(asteroid1)
asteroids.add(asteroid2)
asteroids.add(asteroid3)
asteroids.add(asteroid4)
asteroids.add(asteroid5)
life2 = sprite.spritecollide(rocket, monsters, False)
while game:
    text_lose = font1.render('Пропущено:' + str(prop), 1, (255,255,255))
    text_score = font1.render('Счёт:' + str(score), 1, (255,255,255))
    text_life = font1.render('Жизнь:' + str(life2), 1, (255,255,255))
    for e in event.get(): 
        if e.type == QUIT: 
            game = False 
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire <= 5 and rel_time == False:
                    fire_sound.play()
                    rocket.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if rel_time == True:
        now_time = timer()
        if now_time - last_time < 3:
            reload = font.render('Перзарядка', 1,(150,0,0))
            window.blit(reload,(260,460))
        else:
            num_fire = 0
            rel_time = False 
            

    if finish != True:
        window.blit(background,(0,0))
        rocket.update()
        rocket.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.draw(window)
        asteroids.update()
        window.blit(text_lose, (25, 50))
        window.blit(text_score, (25, 30))
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list = sprite.groupcollide(asteroids, bullets, True, True)
        for i in sprites_list:
            score += 1
            monster = Enemy('ufo.png', 450, -40, (randint(1, 5)))
            monsters.add(monster)
            asteroid = Enemy('asteroid.png', 450, -40, (randint(1, 5)))
            asteroids.add(asteroid)
        if score > 42:
            finish = True
            window.blit(win, (150, 150))
        if prop == 200000 or sprite.spritecollide(rocket, monsters, False):
            finish = True
            window.blit(lose, (150, 150))
        if life2 == 0:
            finish = True
            window.blit(lose1, (150, 150))
    clock.tick(60)
    display.update()