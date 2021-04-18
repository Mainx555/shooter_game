from pygame import *
from random import randint
window = display.set_mode((800,600))
display.set_caption('Украинская база данных')
background = transform.scale(image.load("xoxls.jpg"),(800,600))
global miss
miss=0
global hits
hits=0
global hp
hp=10

font.init()
font1=font.SysFont('Arial',36)
font2=font.SysFont('Arial',36)
font3=font.SysFont('Arial',36)
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, player_speed,width,height):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(width,height))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
class Bullet(GameSprite):
    def fire(self):
        self.rect.y-=self.speed
class Meteor(GameSprite):
    def go(self):
        self.rect.y+=self.speed        
clock = time.Clock()
FPS=60
player=GameSprite('kaban.png',350,500,10,100,100)
ufo_enemy=Enemy('ufo.png',randint(0,700),randint(0,5),randint(1,4),128,64)
bullet=Bullet('bullet.png',player.rect.x,player.rect.y,20,10,10)
meteor=Meteor('shot1.png',randint(0,700),randint(0,10),4,75,100)
bullet.rect.x=-10
mixer.init()
mixer.music.load('kiev.mp3')
mixer.music.play()
monsters=sprite.Group()
monsters.add(ufo_enemy)
bullets=sprite.Group()
bullets.add(bullet)
meteors=sprite.Group()
meteors.add(meteor)
def new_enemy():
    ufo_enemy=Enemy('ufo.png',randint(0,700),randint(0,5),5,128,64)
    monsters.add(ufo_enemy)
def new_bullet():
    bullet=Bullet('bullet.png',player.rect.x,player.rect.y,20,10,10)
    bullet.rect.x=-10
def new_meteor():
    meteor=Meteor('shot1.png',randint(0,700),randint(0,10),10,75,100)
    meteors.add(meteor)
game=True
while game:
    window.blit(background,(0,0))
    text_lose=font1.render("Пропущенно:"+ str(miss), 1,(255,255,255))
    text_hits=font2.render("Счёт:"+ str(hits),1 ,(255,255,255))
    text_hp=font3.render("Здоровье:"+str(hp),1,(255,255,255))
    window.blit(text_hits,(1,26))
    window.blit(text_lose,(1,1))
    window.blit(text_hp,(1,50))
    meteor.go()
    bullets.update()
    monsters.update()
    bullets.draw(window)
    monsters.draw(window)
    keys_pressed = key.get_pressed()
    clock.tick(FPS)
    player.reset()
    ufo_enemy.reset()
    bullet.reset()
    meteor.reset()
    bullet.fire()
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYUP:
            if e.key == K_SPACE:
                if bullet.rect.y>=0:
                    bullet.rect.x=-10
                bullet.fire()
                bullet=Bullet('bullet.png',player.rect.x,player.rect.y,20,10,10)
                bullets.add(bullet)
                bullet.rect.x=player.rect.x+45
    for ufo_enemy in monsters:
        if sprite.collide_rect(bullet,ufo_enemy):
            bullet.rect.x=-1
            bullet.rect.y=-1
            bullets.remove(bullet)
            monsters.remove(ufo_enemy)
            if len(monsters) <= 7:
                new_enemy()
            hits+=1      
    for ufo_enemy in monsters:
        if ufo_enemy.rect.y>500:
            ufo_enemy.rect.x=randint(0,700)
            ufo_enemy.rect.y=0
            miss+=1
            if len(monsters) <= 4:
                new_enemy()
    for meteor in meteors:
        if sprite.collide_rect(bullet,meteor):
            bullet.rect.x=-10
            bullet.rect.y=-10
            bullets.remove(bullets)
            meteors.remove(meteor)
            hp-=1
        if len(meteors)==0:
            new_meteor()
        if meteor.rect.y>=600:
            meteors.remove(meteor)
            new_meteor()
    if hp == 0:
        for ufo_enemy in monsters:
            ufo_enemy.rect.y=ufo_enemy.rect.y
            ufo_enemy.hide()
        for meteor in meteors:
            meteor.rect.y=meteor.rect.y
            meteor.hide()
        text_hits.hide()
        text_hp.hide()
        text_lose.hide()
        font4=font.Font(None,36)
        text_final=font4.render("YOU LOSE!",1,(255,0,0))
    if player.rect.x>=700:
        player.rect.x-=10
    if player.rect.x<=0:
        player.rect.x+=10
    if keys_pressed[K_a]:
        player.rect.x-=10
    if keys_pressed[K_d]:
        player.rect.x+=10
    display.update()
