import pygame, random, time
from states.state import State

class Object:
    def __init__(self, pos, size, tekst, color=(0, 0, 0), tekst_color=(255, 255, 255)):
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.color = color
        self.pos = pos
        self.size = size

        self.tekst = tekst
        self.tekst_color = tekst_color
        self.font = pygame.font.Font(None, 24)
    
    def render(self, display, display_tekst=True):
        pygame.draw.rect(display, self.color, self.rect)
        if display_tekst:
            text_surface = self.font.render(self.tekst, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.rect.center)
            display.blit(text_surface, text_rect)

class Player(Object):
    def __init__(self, pos, size, tekst, color=(0, 255, 255), tekst_color=(255, 255, 255)):
        super().__init__(pos, size, tekst, color, tekst_color)
        self.speed = 400
        self.bilde = pygame.image.load("assets/SubToWaluigi/Wario.png").convert_alpha()
        self.bilde = pygame.transform.scale(self.bilde, (self.size[0], self.size[1]))
    
    def update(self, actions, dt):
        if actions["up"].held:
            self.pos[1] -= self.speed * dt
            
        if actions["down"].held:
            self.pos[1] += self.speed * dt
        
        if actions["left"].held:
            self.pos[0] -= self.speed * dt
            
        if actions["right"].held:
            self.pos[0] += self.speed * dt
        
    def render(self, display):
        display.blit(self.bilde, (self.pos[0], self.pos[1]))
            

        # Keep player within screen bounds
        self.pos[0] = max(0, min(self.pos[0], pygame.display.get_surface().get_width() - self.size[0]))
        self.pos[1] = max(0, min(self.pos[1], pygame.display.get_surface().get_height() - self.size[1]))

        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


class SubToWaluigi(State):
    def __init__(self, game):
        self.game = game
        self.counter = 0
        self.game_size = 10
        self.objects = [Object((self.game.screen.get_width()//self.game_size*random.randint(0, self.game_size-1), self.game.screen.get_height()//self.game_size*random.randint(0, self.game_size-1)), (110, 50), f"Subscribe", color="red") for i in range(1)]
        self.objects.append(Object((self.game.screen.get_width()//self.game_size*random.randint(0, self.game_size-1), self.game.screen.get_height()//self.game_size*random.randint(0, self.game_size-1)), (110, 50), f"Like", color="blue"))
        self.objects.append(Object((self.game.screen.get_width()//self.game_size*random.randint(0, self.game_size-1), self.game.screen.get_height()//self.game_size*random.randint(0, self.game_size-1)), (110, 50), f"Comment", color="green"))
        self.objects.append(Object((self.game.screen.get_width()//self.game_size*random.randint(0, self.game_size-1), self.game.screen.get_height()//self.game_size*random.randint(0, self.game_size-1)), (110, 50), f"Notifcation", color="yellow"))
        self.player = Player([self.game.screen.get_width() // 2, self.game.screen.get_height() //1.1], (50, 50), "Wario", color=(255, 255, 0))
    
    def draw_text(self, surface, string: str, color: pygame.Color, center: tuple, tekst_size: int = 24):
        font = pygame.font.Font(None, tekst_size)
        text_surf = font.render(string, False, (255, 255, 255)) # Tekst
        text_rect = text_surf.get_rect(center=center) # Sentrer
        self.game.screen.blit(text_surf, text_rect)
    
    def endscreen(self, did_win):
        if did_win:
            self.game.screen.blit(pygame.transform.scale(pygame.image.load("assets/SubToWaluigi/WaluigiHappy.png").convert(), (self.game.screen.get_width(), self.game.screen.get_height())), (0, 0))
            self.draw_text(self.game.screen, "Waluigi glad!", (0, 255, 0), (self.game.screen.get_width() // 2, self.game.screen.get_height() // 2), tekst_size = 50)
        else:
            self.game.screen.blit(pygame.transform.scale(pygame.image.load("assets/SubToWaluigi/WaluigiCrying.png").convert(), (self.game.screen.get_width(), self.game.screen.get_height())), (0, 0))
            self.draw_text(self.game.screen, "Waluigi trist!", (255, 0, 0), (self.game.screen.get_width() // 2, self.game.screen.get_height() // 2), tekst_size = 50)

        pygame.display.flip()
        pygame.time.delay(1000)
        self.game.state = self.game.main_menu
        self.game.reset_actions()
        self.game.set_up_actions()


        
    def update(self, actions, dt):
        if 3 - self.counter <= 0:
            self.endscreen(False)
        # Tilbake til main menu
        if actions["escape"].pressed:
            self.game.state = self.game.main_menu
            actions["escape"].pressed = False
        if self.objects == []:
            self.endscreen(True)
        for i in self.objects:
            if self.player.rect.colliderect(i.rect):
                i.color = (255, 50, 50) if i.tekst == "Subscribe" else (50, 50, 255) if i.tekst == "Like" else (255, 255, 50) if i.tekst == "Notifcation" else (255, 255, 255)
            else:
                i.color = (255, 0, 0) if i.tekst == "Subscribe" else (0, 0, 255) if i.tekst == "Like" else (255, 255, 0) if i.tekst == "Notifcation" else (200, 200, 200)
            if actions["1"].pressed and self.player.rect.colliderect(i.rect):
                self.objects.remove(i)
                self.game.actions["1"].pressed = False
        if actions["1"].pressed:
            self.game.actions["1"].pressed = False
        # Update player
        self.player.update(actions, dt)
        self.counter += dt


    def render(self, display):
        display.blit(pygame.transform.scale(pygame.image.load("assets/SubToWaluigi/WaluigiYT.png").convert(), (self.game.screen.get_width(), self.game.screen.get_height())), (0, 0))
        self.draw_text(display, f"Hit dat sub button Wario på: {abs(3-self.counter):.1f} s (trykk ESC for å gå tilbake)", (123, 4, 20), (self.game.screen.get_width() // 2, 20))
        self.draw_text(display, f"Trykk 1 for å trykke", (123, 4, 20), (self.game.screen.get_width() // 2, self.game.screen.get_height() - 20))
        for obj in self.objects:
            obj.render(display)
        self.player.render(display)
        