#sprite classes 
import pygame
from random import choice, randrange

from settings import *
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        self._layer = PLAYER_LAYER
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.loadImages()
        self.current_frame = 0
        self.walking = False
        self.jumping = False
        self.last_update = 0
        self.image = self.standing_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (50, HEIGHT - 50)
        self.pos = vec(50, HEIGHT - 50)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
    
    def loadImages(self):
        self.standing_frames = [pygame.image.load("./img/bunny1.png").convert_alpha(),
                                pygame.image.load("./img/bunny2.png").convert_alpha()]
        self.walking_frames_r = [pygame.image.load("./img/bunny3.png").convert_alpha(),
                                pygame.image.load("./img/bunny4.png").convert_alpha()]
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            self.walking_frames_l.append(pygame.transform.flip(frame, True, False))
        
        self.jumping_frame = pygame.image.load("./img/bunny5.png").convert_alpha()
    
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        #jump only if standing on a platforms
        self.rect.x += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = MAX_JUMP
            self.game.jump_sound.play()

    def update(self):
        self.animate()
        self.acc = vec(0, GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        #adjust acceleration based on friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #equations of motion
        self.vel += self.acc #(v = u + a*t)
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc #(s = ut + 1/2 * a * (t^2))

        #wrap around the sides of the screen
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2

        #place the player at the calculated position
        self.rect.midbottom = self.pos
    
    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking =True
        else:
            self.walking = False
        
        #walking animation
        if self.walking:
            if now - self.last_update > 280:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        #idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % (len(self.standing_frames))
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        self.mask = pygame.mask.from_surface(self.image)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image_list = [pygame.image.load("./img/ground_cake_broken.png").convert_alpha(),
                       pygame.image.load("./img/ground_cake_small.png").convert_alpha()]
        self.image = choice(self.image_list)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() // 3, self.image.get_height() // 3))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Mob(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_list = []
        for i in range(1, 6):
            img = pygame.image.load(f"./img/wingMan{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() // 2, img.get_height() // 2))
            self.image_list.append(img)

        self.curr_frame = 0
        self.last_update = 0
        self.image = self.image_list[self.curr_frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT / 5)
    
    def update(self):
        self.animate()
        self.rect.x += self.vx

        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
    
    def animate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 160:
            self.last_update = now
            self.curr_frame = (self.curr_frame + 1) % len(self.image_list)
            self.image = self.image_list[self.curr_frame]
        
        self.mask = pygame.mask.from_surface(self.image)