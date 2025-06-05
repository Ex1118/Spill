import pygame, time, random
from states.mainmenu import State

class CatchTheFallingBlock(State):
    def __init__(self, game):
        self.game = game
        self.fail = False
        self.ended = False
        self.winner = False
        self.pos = random.randint(30, self.game.screen.get_width()-30)
        self.side_hit = False
        self.box = [
            [self.pos-30, self.game.screen.get_height()-100, 10, 80],
            [self.pos+30, self.game.screen.get_height()-100, 10, 80],
            [self.pos-30, self.game.screen.get_height()-20, 70, 10],
        ]
        self.object_pos_x = random.randint(20, self.game.screen.get_width()-20)
        self.object = [self.object_pos_x, 0, 20 , 20]
        self.object_speed = 180
        
    def update(self, actions, dt):
        if actions["escape"].pressed or self.ended:
            self.end()
            actions["escape"].pressed = False
        
        
        if actions["left"].held and not self.fail and not self.side_hit:
            for rect in self.box:
                if self.pos > 30:
                    
                    rect[0] -= 200*dt 
                    
            if self.pos > 30:
                self.pos -= 200*dt
                
                
                
        if actions["right"].held and not self.fail and not self.side_hit:
            for rect in self.box:
                if self.pos < self.game.screen.get_width()-40:
                    rect[0] += 200*dt 
                    
            if self.pos < self.game.screen.get_width()-40:
                self.pos += 200*dt 
                    
        ting1 = pygame.Rect(self.box[0])
        ting2 = pygame.Rect(self.box[1])
        object = pygame.Rect(self.object)
        #print(ting1.top,ting1.bottom, object.bottom, object.top)
        #print(ting1.top < object.bottom, ting1.left == object.right, ting1.right==object.left)
        if (ting1.left == object.right or ting1.right==object.left) and ting1.top < object.bottom:
            self.side_hit = True
        elif (ting2.left == object.right or ting2.right==object.left) and ting2.top < object.bottom:
            self.side_hit = True
        
        if self.object[1] < self.game.screen.get_height()+50 and not self.fail:
            
            
            
            if pygame.Rect.colliderect(ting1, object) and not self.fail and ting1.top - ting1.height//2 < object.bottom:
                self.fail = True
            
            elif pygame.Rect.colliderect(ting2, object) and not self.fail and ting2.top - ting2.height//2 < object.bottom:
                self.fail = True
            if pygame.Rect.colliderect(pygame.Rect(self.box[2]), object):
                self.winner = True
            self.object[1]+=self.object_speed*dt
        else:
            self.fail = True
            
                
        """
        if self.object[1] < self.game.screen.get_height()+50 and not self.fail:
            a1 = pygame.Rect(self.box[0])
            a2 = pygame.Rect(self.box[1])
            object = pygame.Rect(self.object[0], self.object[1], self.object[2], self.object[3])
            print((a1.top -2  == object.bottom) , (pygame.Rect.colliderect(a1, object)))
            if (a1.top == object.bottom)  and (pygame.Rect.colliderect(a1, object)) :
                self.fail = True
            elif (a2.top == object.bottom) and (pygame.Rect.colliderect(a2, object)):
                self.fail = True
            elif pygame.Rect.colliderect(pygame.Rect(self.box[2]), self.object):
                self.winner = True
            self.object[1] += self.object_speed *dt
            
        else:
            self.fail = True"""
            
        
    def render(self, display):
        display.fill((0,0,0))
        for rect in self.box:
            pygame.draw.rect(display, (255, 0,0), rect)
        pygame.draw.rect(display, (0,255,0), self.object)
        #pygame.draw.rect(display, "red", (self.pos, 200, 20, 20))
        self.draw_text(display, "Catch the falling Object", (255, 255, 255), (display.get_width()//2, 50)) #type:ignore
        
        if self.fail:
            self.draw_text(display, "you failed", (255, 0,0), display.get_rect().center)
            pygame.display.flip()
            time.sleep(1)
            self.ended = True
        elif self.winner:
            self.draw_text(display, "you won", (0,255, 0), display.get_rect().center)
            pygame.display.flip()
            time.sleep(1)
            self.ended = True
            
    def end(self):
        self.game.state = self.game.main_menu
        self.game.reset_actions()

