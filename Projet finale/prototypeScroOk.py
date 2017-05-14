
# -*- coding: cp1252 -*-
import pygame
from random import randrange
import random
from os import path

#Credit à :
# https://www.freesound.org/people/StudioCopsey/
# https://www.soundjay.com/human/sounds/applause-01.mp3
# Zakru
# Prius247

#Variable
LARGEUR = 480
HAUTEUR = 480
FPS = 60
COMPTEUR= 0
TEMPSBONUS = 5000


# Couleur
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialisation des module pygame 
pygame.init()
pygame.mixer.init()

#Affichage de l'écran
screen = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Fatty Against Junk Food")
clock = pygame.time.Clock()

#Dossier 
img_dir = path.join(path.dirname(__file__), 'image')
wav_dir = path.join(path.dirname(__file__), 'wav')



#Charger les graphismes du jeu
background = pygame.image.load(path.join(img_dir, "fond.png")).convert_alpha()
background_rect = background.get_rect()
homescreen = pygame.image.load(path.join(img_dir, "homescreen.png")).convert_alpha()
homescreen_rect = homescreen.get_rect()
bonfin = pygame.image.load(path.join(img_dir, "good_end.png")).convert()
bonfin_rect = bonfin.get_rect()
mfin = pygame.image.load(path.join(img_dir, "bad_end.png")).convert()
mfin_rect = mfin.get_rect()

                    
                            

#Musique
#son = pygame.mixer.Sound()
hitsound = pygame.mixer.Sound(path.join(wav_dir, "laser3.wav"))
boum = pygame.mixer.Sound(path.join(wav_dir, "explode.wav"))
pain = pygame.mixer.Sound(path.join(wav_dir, "pain.wav"))
mort = pygame.mixer.Sound(path.join(wav_dir, "die.wav"))
down = pygame.mixer.Sound(path.join(wav_dir, "zbeb.wav"))
pup  = pygame.mixer.Sound(path.join(wav_dir, "powerup.wav"))
clap = pygame.mixer.Sound(path.join(wav_dir, "clap.wav"))
pupshield= pygame.mixer.Sound(path.join(wav_dir, "pupshield.wav"))



#Graphisme
animationexp = {}
animationexp = []
#Permet de mettre tous les sprites de l'animation de l'explosion dans une liste
for i in range(8) :
    filename = 'explosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir , filename)).convert_alpha()
    animationexp.append(img)
    
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = animationexp[0]
        self.rect = self.image.get_rect()
        self.rect.center= center
        self.frame= 0
        #Verification dernière update de la frame
        self.last_update = pygame.time.get_ticks()
        #Pour controler la vitesse de l'animation
        self.frame_rate = 50
        
    def update(self):
        #Permet de changer la frame de l'explosion 
        now= pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            #Si la frame atteint la dernière frame de l'explosion
            if self.frame == len(animationexp):
                self.kill()
            else:
                center = self.rect.center
                self.image = animationexp[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, "sante.png")).convert_alpha()
powerup_images['guns'] = pygame.image.load(path.join(img_dir, "power.png")).convert_alpha()
#Score de base
score = 0


#Fonction pour afficher le score
font_name = pygame.font.match_font('arial')
def afficher_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

#Fonction pour afficher la barre de vie du joueur
def afficher_vie(surf, x , y , pct):
 
  BAR_LARG = 100 
  BAR_HAUT = 10
  inter = player.vie
  if inter <0 :
    inter = 0
  ext_rect = pygame.Rect(x, y , BAR_LARG, BAR_HAUT)
  inter_rect = pygame.Rect (x, y ,inter, BAR_HAUT)
  pygame.draw.rect(surf , RED, inter_rect)
  pygame.draw.rect(surf , WHITE , ext_rect , 2)

#Fonction affichage écran game over et écran d'acceuil
def end():
  screen.fill((0,0,0))
  screen.blit(mfin , mfin_rect)
  afficher_text(screen, "Appuyer sur retour pour rejouer" , 30 , LARGEUR/2 , HAUTEUR-100 )
  pygame.display.flip()
  waiting = True
  while waiting :
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            waiting = False
def home():
  screen.fill((0,0,0))
  screen.blit(homescreen , homescreen_rect)
  pygame.display.flip()
  waiting = True
  while waiting :
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            waiting = False

def win():
  screen.fill((0,0,0))
  screen.blit(bonfin , bonfin_rect)
  afficher_text(screen, "Appuyer sur retour pour rejouer" , 30 , LARGEUR/2 , HAUTEUR-480 )
  
  pygame.display.flip()
  waiting = True
  while waiting : 
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_BACKSPACE:
            waiting = False


    
  

class Player(pygame.sprite.Sprite) :
    def __init__(self):
        super(Player,self).__init__()
        self.image = pygame.image.load(path.join(img_dir, "perso.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx= LARGEUR/2
        self.rect.bottom = HAUTEUR - 10
        self.vie= 100
        # Nb = nombre de banane
        self.nb = 1
        #timenb = Temps des bonus
        self.timenb = pygame.time.get_ticks()
       
        
        
    def update(self):
        key = pygame.key.get_pressed()
        x, y =0 ,0

        #Bouge le personnage à l'endroit demander
        self.rect.move_ip((x,y))
       
        if key [pygame.K_LEFT]:
                self.rect.x-=5
        if key [pygame.K_RIGHT]:
                self.rect.x += 5
        if key [pygame.K_UP]:
                self.rect.y-= 5
        if key [pygame.K_DOWN]:
                self.rect.y+= 5
       
        #Permet au personnage de ne pas sortir de l'écran
        if self.rect.left + x < 0:
                self.rect.left = 0
        if self.rect.right + x > 480:
                self.rect.right = 480
        if self.rect.top + y < 0:
                self.rect.top = 0
        if self.rect.bottom + y > 480:
                self.rect.bottom = 480
        if self.rect.bottomright[1] + y > 480:
                self.rect.bottomright = 480
        else:
                self.rect.move_ip((x,y))

        #Réduit les effets des bonus quand la durée
        # Permet de réguler le temps de l'actif du bonus
        if self.nb ==3 and pygame.time.get_ticks() - self.timenb > TEMPSBONUS :
          self.nb =2
          down.play()
          self.timenb = pygame.time.get_ticks()
          

        if self.nb ==2 and pygame.time.get_ticks() - self.timenb > TEMPSBONUS :
          self.nb =1
          down.play()
          self.timenb = pygame.time.get_ticks()

      

    def bonus (self):
        self.nb += 1
        if self.nb >=3 :
            self.nb =3

       
        self.timenb = pygame.time.get_ticks()

    def shoot(self):
        if self.nb ==1:
          bullet = Bullet(self.rect.centerx, self.rect.top)
          all_sprites.add(bullet)
          bullets.add(bullet)
          hitsound.play()
        if self.nb ==2:
          bullet1 = Bullet(self.rect.left, self.rect.centery)
          bullet2 = Bullet(self.rect.right, self.rect.centery)
          all_sprites.add(bullet1)
          all_sprites.add(bullet2)
          bullets.add(bullet1)
          bullets.add(bullet2)
          hitsound.play()

        if self.nb ==3:
          bullet1 = Bullet(self.rect.left, self.rect.centery)
          bullet2 = Bullet(self.rect.right, self.rect.centery)
          bullet3 = Bullet(self.rect.centerx, self.rect.top)
          all_sprites.add(bullet1)
          all_sprites.add(bullet2)
          all_sprites.add(bullet3)
          bullets.add(bullet1)
          bullets.add(bullet2)
          bullets.add(bullet3)
          hitsound.play()
          
   
      
        

class Monstres(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load (path.join(img_dir, "hamburger.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.radius= int(self.rect.width*.9/2)
        self.rect.x = random.randrange(LARGEUR - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(4, 8)
        self.speedx = random.randrange(-3, 7)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HAUTEUR + 10 or self.rect.left< -25 or self.rect.right > LARGEUR + 20 :
            self.rect.x = random.randrange(LARGEUR - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(4, 8)
            self.speedx = random.randrange(-3, 3)

    def balle(self):
      balle = BalleEnnemy(self.rect.centerx, self.rect.bottom)
      all_sprites.add(balle)
      balles.add(balle)

   

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(img_dir, "Banana.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # fait disparaitre la balle quand elle atteint le haut de l'écran
        if self.rect.bottom < 0:
            self.kill()


class BalleEnnemy(pygame.sprite.Sprite):
    def __init__(self, x , y ):
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load(path.join(img_dir,"boum.png")).convert_alpha()
      self.rect = self.image.get_rect()
      self.rect.bottom = y
      self.rect.centerx = x
      self.speedy = 10
    def update(self):
      self.rect.y += self.speedy



class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type= random.choice(['shield' , 'guns'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HAUTEUR:
            self.kill()


def spawnmonstre():
        m = Monstres()
        all_sprites.add(m)
        monstres.add(m)
      
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
balles= pygame.sprite.Group()
monstres = pygame.sprite.Group()
player = Player()
powerups= pygame.sprite.Group()
all_sprites.add(player)
for i in range (4):
   spawnmonstre()
    

# Boucle du jeu
continuer = True
game_over = False
homed = True
wins = False
while continuer:
    
    if game_over :
      end()
      game_over = False
      all_sprites = pygame.sprite.Group()
      bullets = pygame.sprite.Group()
      balles= pygame.sprite.Group()
      monstres = pygame.sprite.Group()
      player = Player()
      powerups= pygame.sprite.Group()
      all_sprites.add(player)
      for i in range (4):
          spawnmonstre()
      score = 0
    if homed :
      home()
      homed = False
      all_sprites = pygame.sprite.Group()
      bullets = pygame.sprite.Group()
      balles= pygame.sprite.Group()
      monstres = pygame.sprite.Group()
      player = Player()
      powerups= pygame.sprite.Group()
      all_sprites.add(player)
      for i in range (4):
          spawnmonstre()
      score = 0

    if wins :
      win()
      wins = False
      all_sprites = pygame.sprite.Group()
      bullets = pygame.sprite.Group()
      balles= pygame.sprite.Group()
      monstres = pygame.sprite.Group()
      player = Player()
      powerups= pygame.sprite.Group()
      all_sprites.add(player)
      for i in range (4):
          spawnmonstre()
      score = 0
    
        
    # Vitesse d'execution de la boucle
    clock.tick(FPS)
    # Execution des evenemnt
    for event in pygame.event.get():
        # Pour fermer la fenêtre
        if event.type == pygame.QUIT:
            continuer = False
        # Quand le joueur appuie sur espace , le personnage tire
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # Mise à jour de la boucle
    all_sprites.update()
    #Boucle qui permet au ennemy de tirer + compteur qui détermine le temps d'apparition des balles
    
    COMPTEUR +=1
    if COMPTEUR >= 30 :
      COMPTEUR= 0
      for i in monstres:
        i.balle()
        
        

    #Vérification si il y a une collision entre un montre et une balle , les deux True True permettent de faire disparaitre les sprite lors de la collission
    frappe = pygame.sprite.groupcollide(monstres, bullets, True, True)
    #Fait spawn des monstres suite à leur morts
    for hit in frappe:
        score +=1
        boum.play()
        expl = Explosion(hit.rect.center,)
        all_sprites.add(expl)

        if random.random() >0.8 :
          pow = Pow(hit.rect.center)
          all_sprites.add(pow)
          powerups.add(pow)
          
        spawnmonstre()
       
    #Cette commande vérifie si le joueur touche les monstres 
    hits = pygame.sprite.spritecollide(player , monstres , True , pygame.sprite.collide_circle)
    #SiTouchéQuitterJeu
    for hit in hits :
      #Nombre de point de vie que les hamburger enlève à la collission
        player.vie -= 20
        expl = Explosion(hit.rect.center,)
        all_sprites.add(expl)
        pain.play()
        spawnmonstre()
        
        if player.vie <=0:
          mort.play()
          game_over = True

  
    
   #Cette commande vérifie si la balle ennemy touche le joueurs
    toucher = pygame.sprite.spritecollide(player, balles, True )
    for hit in toucher:
        player.vie -= 10
        pain.play()
        if player.vie <=0 :
            mort.play()
            
          
            game_over = True

    # Cette commande vérifie si le joueur touche un power up
    toucher = pygame.sprite.spritecollide(player, powerups, True)
    for hit in toucher :
      if hit.type == 'shield' :
          pupshield.play()
          player.vie += 20
          

      if player.vie >=100 :
          
            player.vie = 100

      if hit.type == 'guns' :
           pup.play()
           player.bonus()
           
      
        
          

     
          
    #SiScoreAtteintQuitterJeu
    if score  >=40:
        clap.play()

        #AfficherImageFin

        wins = True
        
    # Affiche ce qui a été mise à jour*
    screen.fill((0,0,0))
    screen.blit(background , background_rect)
    all_sprites.draw(screen)
    afficher_vie(screen ,0, 0, player.vie)
    afficher_text(screen, str(score),50,50,50)
    
    


    # raffraichis l'écran
    pygame.display.flip()

pygame.quit()
