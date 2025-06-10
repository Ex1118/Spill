import pygame, time
from states.mainmenu import MainMenu

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 22)
        self.running = True
        self.screen = pygame.display.set_mode((500, 500))
        self.dt, self.prev_time = 0, 0
        self.main_menu = MainMenu(self)
        self.state = self.main_menu
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_asleep = True
        
        self.set_up_actions()

    def set_up_actions(self):
        self.actions = {
            "escape" : Action(pygame.K_ESCAPE), 
            "return" : Action(pygame.K_RETURN),
            "up" : Action(pygame.K_UP),
            "down" : Action(pygame.K_DOWN),
            "left" : Action(pygame.K_LEFT),
            "right" : Action(pygame.K_RIGHT),
            "action" : Action(pygame.K_SPACE),
            "1" : Action(pygame.K_1), 
            "2" : Action(pygame.K_2),
            "3" : Action(pygame.K_3),
            "4" : Action(pygame.K_4),
            "5" : Action(pygame.K_5),
            "6" : Action(pygame.K_6),
            "7" : Action(pygame.K_7),
            "8" : Action(pygame.K_8),
            "9" : Action(pygame.K_9),
            "leftmouse" : Action(1)
        }

    def reset_actions(self):
        for action in self.actions:
            self.actions[action].pressed = False

    def main_loop(self):
        if self.running:
            self.update_time()
            self.handle_events()
            self.update()
            self.render()

    def update(self):
        self.state.update(self.actions, self.dt)

    def update_time(self):
        self.dt = time.time() - self.prev_time
        self.prev_time = time.time()
    
    def render(self):
        # Render state
        self.state.render(display = self.screen)
        pygame.display.flip()

    def handle_events(self):
        # Get mouse position and if it has updated
        if pygame.mouse.get_pos() != self.mouse_pos:
            self.mouse_asleep = False
            self.mouse_post = pygame.mouse.get_pos()
        else:
            self.mouse_asleep = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Keydown
            if event.type == pygame.KEYDOWN:
                for action_name in self.actions:
                    if event.key == self.actions[action_name].pygame_event:
                        self.actions[action_name].held = True
                        self.actions[action_name].pressed = True
                        if self.actions[action_name].held_time is None:
                            self.actions[action_name].held_time = time.time()
                
            # Keyup
            if event.type == pygame.KEYUP:
                for action_name in self.actions:
                    if event.key == self.actions[action_name].pygame_event:
                        self.actions[action_name].held = False
                        self.actions[action_name].held_time = None

            # Mousebuttondown
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.actions["leftmouse"].held = True
                    self.actions["leftmouse"].pressed = True
                    if self.actions["leftmouse"].held_time is None:
                        self.actions["leftmouse"].held_time = time.time()
                
            # Mousebuttonup
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.actions["leftmouse"].held = False
                    self.actions["leftmouse"].held_time = None             

class Action:
    def __init__(self, pygame_event):
        """
        Actions kan brukes på to måter.

        actions["key"].pressed er buffered, altså True eller False. Tenk Flappy Bird. Husk å sette til False etter at knappen er trykket på.

        actions["key"].held er True mens knappen er holdt inne og False når den ikke er det. Du trenger ikke gjøre noe spess med denne.
        """
        self.pygame_event = pygame_event
        self.held = False
        self.held_time = None
        self.pressed = False

if __name__ == "__main__":
    game = Game()
    while game.running:
        game.main_loop()
