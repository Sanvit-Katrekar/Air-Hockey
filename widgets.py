'''
This module defines game widgets.
Includes:
    1. Button
    2. Input box
    3. Basic pygame screen
'''
import pygame
pygame.font.init()
#Defining game colours
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

class Button:
    ''' Class for a pygame button widget '''
    def __init__(self, screen, position, text, **kwargs):
        self.screen = screen
        self.position = position
        self.font = pygame.font.SysFont('Garamond', 40)
        self.bg = kwargs.get('bg', ORANGE)
        self.fg = kwargs.get('fg', RED)
        self.state = kwargs.get('state', 'normal')
        self.center = kwargs.get('center', False)
        self.text_render = self.font.render(
            text.center(len(text) + kwargs.get('pad', 0)), #Centering text
            1, #Anti-aliasing
            self.fg #Button foreground colour
            )
        self.render_object = None

    def draw(self):
        rect = self.text_render.get_rect()
        #Checking if given position is the position of the center of button
        if self.center:
            rect.center = self.position
        else:
            rect.topleft = self.position
        x, y, w, h = rect
        pygame.draw.line(self.screen, self.bg, (x, y), (x+w , y), 5)
        pygame.draw.line(self.screen, self.bg, (x, y-2), (x, y+h), 5)
        pygame.draw.line(self.screen, [abs(val-100) for val in self.bg], (x, y+h), (x+w , y+h), 5)
        pygame.draw.line(self.screen, [abs(val-100) for val in self.bg], (x+w , y+h), (x+w , y), 5)
        pygame.draw.rect(self.screen, [abs(val-50) for val in self.bg], (x, y, w , h))
        self.render_object = self.screen.blit(self.text_render, (x, y))

    def clicked(self):
        if self.state == 'normal':
            return self.render_object.collidepoint(pygame.mouse.get_pos())
        return False

class InputBox:
    ''' Class for a pygame entry widget '''
    def __init__(self, x, y, w, h, text=''):
        self.colour_inactive = RED
        self.colour_active = BLUE
        self.gen_colour = BLACK
        self.max_length = 10
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = self.colour_inactive
        self.default_text = self.text = text
        self.font = pygame.font.SysFont('Arial', 50)
        self.text_surface = self.font.render(text, 1, self.colour)
        self.active = False
        self.val = ''

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            #If the user clicked on the input box rect.
            if self.rect.collidepoint(event.pos):
                #Toggle the active variable.
                self.active = not self.active
                if self.text == '':
                    self.text = self.default_text
                elif self.text == self.default_text and self.active:
                    self.text = ''
                self.text_surface = self.font.render(
                    self.text.center(self.max_length), 1, self.colour
                    )
            else:
                self.active = False
            #Change the current colour of the input box.
            if self.active:
                self.colour = self.colour_active
            elif self.val:
                self.colour = self.gen_colour
            else:
                self.colour = self.colour_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.val = self.text.strip()
                self.colour = self.gen_colour
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text.strip()) < self.max_length:
                self.text += event.unicode
            #Re-render the text.
            self.text_surface = self.font.render(
                self.text.center(self.max_length), 1, self.colour
                )

    def update(self):
        ''' Resizes the box if the text is too long. '''
        width = max(200, self.text_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.colour, self.rect, 2)

class Screen:
    ''' Base class for the pygame game screen '''
    def __init__(self, screen, FPS=60, fontsize=30):
        self.screen = screen
        self.w, self.h = self.screen.get_size()
        self.sprites = pygame.sprite.Group()
        self.FPS = FPS
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Segoe UI Black', fontsize)

    def drawHockeyGround(self):
        ''' Draws the hockey field '''
        self.screen.fill(GREEN)
        #Center line
        pygame.draw.line(self.screen, WHITE, (self.w//2, 0), (self.w//2, self.h), 5)
        #Center circle
        pygame.draw.circle(self.screen, WHITE, (self.w//2, self.h//2), 75, 5)
        #The goals
        pygame.draw.line(self.screen, BLACK, (2, 175), (2, 325), 5)
        pygame.draw.line(self.screen, BLACK, (self.w-3, 175), (self.w-3, 325), 5)
        #Goal area lines
        pygame.draw.rect(self.screen, WHITE, (-1, self.h//5, 150, 300), 5)
        pygame.draw.rect(self.screen, WHITE, (self.w-148, self.h//5, 150, 300), 5)

if __name__ == '__main__':
    import os
    os.system('python main.py')
