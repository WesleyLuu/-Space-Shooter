import pygame
import random
import time
from os import path

width = 480 
height = 600
FPS = 60

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Init Image folder
img_dir = path.join(path.dirname(__file__), 'img')

# intizate the game and window
pygame.init()
start = time.time()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('My Space Invader')
clock = pygame.time.Clock()
player_health = 3

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('player.png')
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0
        self.speedy = 0
    
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        
        # Controls for X-Axis
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        self.rect.x += self.speedx
        
        # Controls for Y-Axis
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.y += self.speedy
        
        # Boundaries for the Player
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height
    
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 9)
        self.speedx = random.randrange(-4, 4)
    
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 20:
            self.rect.x = random.randrange(0, width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 9)
            self.speedx = random.randrange(-3, 3)
    
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = - 10
    
    def update(self):
        self.rect.y += self.speedy
        # Kill it if it moves off the map
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
mob = 2
for i in range(mob):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# for i in range(10):
#     m = Mob()
#     all_sprites.add(m)
#     mobs.add(m)

# Game Loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Proceesed Input (events)
    for event in pygame.event.get():
        # check for quitting
        if event.type == pygame.QUIT:
            running = False   
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # Update
    all_sprites.update()
    # Spawns a mob every 5 seconds
    now = time.time()
    dt = now - start
    if dt > 5:
        start = now
        if len(mobs) < 12:
            m = Mob()
            m.speedy += 1
            m.speedx += 1
            all_sprites.add(m)
            mobs.add(m)
        if len(mobs) == 12:
           m.speedy += 5
           m.speedx += 2
    
    print(len(mobs))
    # Check if bulet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    
    # Check if mob hit player
    hits = pygame.sprite.spritecollide(player, mobs, False)
    if hits:
        hit_time = time.time()
        player_health -= 1
        if player_health < 1:
            runnung == False


    # Draw/ render
    screen.fill(black)
    all_sprites.draw(screen)
    
    # after drawing everything (flips display)
    pygame.display.flip()

pygame.quit()

# # Intialize the pygame
# pygame.init()

# # Create the screen
# screen = pygame.display.set_mode((800,600))

# # Background
# background = pygame.image.load("background.png")

# #Title and Icon
# pygame.display.set_caption("Space Invaders")
# icon = pygame.image.load('spaceship.png')
# pygame.display.set_icon(icon)  

# # Player
# playerImg = pygame.image.load('player.png')
# playerX = 370
# playerY = 480
# playerX_change = 0

# # Enemy
# enemyImg = pygame.image.load('monster.png')
# enemyX = random.randint(0,800)
# enemyY = random.randint(50,150)
# enemyX_change = 0.3    
# enemyY_change = 40

# # Ready - can't see bullet on scrren
# # Fire bullet currently fired 
# bulletImg = pygame.image.load('monster.png')
# bulletX = 0
# bulletY = 480
# bulletX_change = 0
# bulletY_change = 10
# bullet_state = "ready" 

# def player(x, y):
#     screen.blit(playerImg, (x, y))

# def enemy(x, y):
#     screen.blit(enemyImg, (x, y))

# def fire_bulllet(x,y):
#     global bullet_state
#     bullet_state = "fire"
#     screen.blit(bulletImg, (x + 16, y - 10))

# # Game Loop
# running = True
# while running:
      
#     # RGB = Red, Green, Blue (max(255))
#     screen.fill((0, 0, 0))
#     # background image
#     screen.blit(background,(0, 0))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
    
#     # If keystroke is pressed check whether its right or left
#     if event.type == pygame.KEYDOWN:         
        
#         if event.key == pygame.K_LEFT:
#             playerX_change = - 0.2
#             print('LEFT')
#         if event.key == pygame.K_RIGHT:
#             playerX_change = 0.2
#             print('RIGHT')
#         if event.key == pygame.K_SPACE:
#             print(one)
#             fire_bullet(playerX, bulletY)
#             print('SPACE') 
#     if event.type == pygame.KEYUP:
#         if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
#             playerX_change = 0

#     # Walls (bounds)
#     playerX += playerX_change
    
#     if playerX <= 0:
#         playerX = 0
#     elif playerX >= 736:
#         playerX = 736   
    
#     #Enemy Movement
#     enemyX += enemyX_change
    
#     if enemyX <= 0:
#         enemyX_change = 0.2
#         enemyY += enemyY_change
#     elif enemyX >= 736:
#         enemyX_change = -0.2
#         enemyY += enemyY_change
    
#     # Bullet Movement
#     if bullet_state == 'fire':
#         fire_bullet(playerX, bulletY)
#         bulletY -= bulletY_change
    
#     player(playerX, playerY)
#     enemy(enemyX, enemyY)
#     pygame.display.update()
