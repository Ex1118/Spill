import pygame, time, random
import numpy as np
from states.state import State

file = "StateManagementTemplate/assets/mrpresident/"
GRAVITY = 11000
JUMP_VEL = -2100

class Object:
    def __init__(self, texture, pos, vel):
        self.texture = texture
        self.pos = pos
        self.vel = vel
        self.rect = pygame.Rect((0, 0), self.texture.get_size())
        self.rect.center = self.pos
    
    def update(self, dt):
        self.pos = np.add(self.pos, np.multiply(self.vel, dt))
    
    def render(self, display):
        self.rect = pygame.Rect((0, 0), self.texture.get_size())
        self.rect.center = self.pos
        display.blit(self.texture, self.rect)
        
    

class MrPresident(State):
    def __init__(self, game):
        self.game = game
        self.running = True
        self.did_win = False
        self.background = pygame.transform.scale(pygame.image.load(file + "background.jpeg").convert_alpha(), (500, 500))
        self.game.font = pygame.font.SysFont(None, 128)
        
        pygame.mixer.init()
        self.jump_sound = pygame.mixer.Sound(file + "getdown.wav")
        self.lose_sound = pygame.mixer.Sound(file + "presidentded.wav")
        self.win_sound = pygame.mixer.Sound(file + "catchbulltet.wav")
        
        self.bullet = Object(
            pygame.transform.scale(pygame.image.load(file + "bullet.png").convert_alpha(), (70, 20)),
            (2100 + 2000 * random.random(), 120),
            (-1100, 0)
        )
        
        self.onground = True
        self.bodyguard = Object(
            pygame.transform.scale(pygame.image.load(file + "bodyguard.png").convert_alpha(), (85, 140)),
            (200, 250),
            (0, 0)
        )
        
        self.lectern = Object(
            pygame.transform.scale(pygame.image.load(file + "lectern.png").convert_alpha(), (183, 288)),
            (70, 260),
            (0, 0)
        )
        
        self.president = Object(
            pygame.transform.scale(pygame.image.load(file + "president.png").convert_alpha(), (140, 140)),
            (70, 120),
            (0, 0)
        )
    
    
    
    def win(self):
        self.running = False
        self.did_win = True
        self.win_sound.play()
        self.time = time.time()
    
    def lose(self):
        self.running = False
        self.lose_sound.play()
        self.time = time.time()
    
    
    def update(self, actions, dt):
        if self.running:
            # Jump
            if actions["action"].pressed:
                actions["action"].pressed = False
                if self.onground:
                    self.jump_sound.play()
                    self.onground = False
                    self.bodyguard.vel = (0, JUMP_VEL)
            
            if self.bodyguard.pos[1] >= 300 and self.bodyguard.vel[1] >= 0:
                self.bodyguard.vel = (0, 0)
                self.bodyguard.pos = (self.bodyguard.pos[0], 300)
            
            self.bodyguard.vel = np.add(self.bodyguard.vel, np.multiply((0, GRAVITY), dt))
            
            self.president.update(dt)
            self.bodyguard.update(dt)
            self.bullet.update(dt)
            
            
            # Win / Lose - Conditions
            if self.bullet.rect.colliderect(self.bodyguard.rect) and self.bullet.pos[0] > self.bodyguard.pos[0]:
                self.win()
            if self.bullet.pos[0] < 100:
                self.lose()
        else:
            if time.time() - self.time > 1.0:
                self.game.font = pygame.font.SysFont(None, 22)
                self.game.reset_actions()
                self.game.state = self.game.main_menu
    
    

    def render(self, display):
        display.blit(self.background, (0, 0))
        
        self.president.render(display)
        self.lectern.render(display)
        self.bodyguard.render(display)
        self.bullet.render(display)
        
        if not(self.running):
            if self.did_win:
                self.draw_text(display, "WIN", "#000000", (250, 250))
            else:
                self.draw_text(display, "LOSE", "#000000", (250, 250))