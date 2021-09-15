#2-D platformer game
#art from kenny.nl
#happytune - https://opengameart.org/content/happy-tune
#yippee - https://opengameart.org/content/yippee-0

import pygame
from random import randrange

from settings import *
from sprites import *

class Game:
    def __init__(self):
        #initialize game window, etc
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(FONT_NAME)
        self.loadData()    

    def loadData(self):
        #jump sound
        self.jump_sound = pygame.mixer.Sound("./snd/jump.wav")
        self.game_over_sound = pygame.mixer.Sound("./snd/game_over.wav")

        try:
            with open("./highscore.txt", 'r') as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0

    def newGame(self):
        #start a new game
        self.score = 0

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.mob_timer = 0

        self.player = Player(self)

        for plat in PLATFORM_LIST:
            p = Platform(*plat, game) #explode the plat list

        pygame.mixer.music.load("./snd/happytune.ogg") #load the game music
        self.run()

    def run(self):
        #game loop
        self.playing = True
        pygame.mixer.music.play(loops = -1) #loop the music until game finishes
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500) #fadeout the music at the end of game for half a second

    def events(self):
        #game loop - events
        for event in pygame.event.get():
            #check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            #close the window using escape key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.playing:
                        self.playing = False
                    self.running = False
            
                #jump when up key is pressed
                if event.key == pygame.K_UP:
                    self.player.jump()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.player.jump_cut()

    def update(self):
        #game loop - update
        self.all_sprites.update()

        #spawn mob
        now  = pygame.time.get_ticks()
        if now - self.mob_timer > MOB_FREQ + choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self) 

        #hit mobs?
        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, False, pygame.sprite.collide_mask)
        if mob_hits:
            self.playing = False
            self.game_over_sound.play()

        #check if player hits a platform only if falling
        if self.player.vel.y > 0 : 
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 15 and \
                    self.player.pos.x > lowest.rect.left - 15:
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        #if player reaches top 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
        
        #game over condition
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
            if len(self.platforms) == 0:
                self.playing = False
                self.game_over_sound.play()

        #spawn new platforms to keeps same average number
        while len(self.platforms) < 6:
            width = randrange(50, 100)
            p = Platform(randrange(0, WIDTH - width),
                         randrange(-75, -30), game)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def draw(self):
        #game loop - draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.drawText(str(self.score), 22, WHITE, WIDTH / 2, 15)
        #after drawing everything - flip the display
        pygame.display.flip()

    def showStartScreen(self):
        #game splash screen
        pygame.mixer.music.load("./snd/Yippee.ogg")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops = -1)

        self.screen.fill(BGCOLOR)
        self.drawText(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4) 
        self.drawText("Arrows to move, Up to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT * 3 / 4)
        self.drawText("High Score : " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pygame.display.flip()
        self.waitForKey()

        pygame.mixer.music.fadeout(500)

    def showGameOverScreen(self):
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.drawText("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4) 
        self.drawText("Score : " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Press a key to play", 22, WHITE, WIDTH/2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.drawText("NEW HIGH SCORE!", 22, WHITE, WIDTH/2, HEIGHT / 2 + 40)
            with open("./highscore.txt", "w") as f:
                f.write(str(self.highscore))
        else:
            self.drawText("High Score : " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pygame.display.flip()
        self.waitForKey()

    def drawText(self, text, size, color, x, y):
        font  = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
    
    def waitForKey(self):
        waiting  = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        waiting = False
                        self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False
game = Game()
game.showStartScreen()

while game.running:
    game.newGame()
    game.showGameOverScreen()

pygame.quit()
