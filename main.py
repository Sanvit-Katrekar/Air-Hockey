import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
pygame.init()

def resourcePath(relativePath='', subdir='', path=False):
    ''' Returns project absolute path '''
    try:
        basePath = sys._MEIPASS
    except AttributeError:
        basePath = os.path.abspath('Images')
        basePath = os.path.join(basePath, subdir)
    if path:
        return basePath
    return os.path.join(basePath, relativePath)

class Button:
    def __init__(self, screen, position, text, **kwargs):
        self.screen = screen
        self.position = position
        self.font = pygame.font.SysFont('Garamond', 40)
        self.bg = kwargs.get('bg', (255,165,0)) #Default bg colour: Orange
        self.fg = kwargs.get('fg', (255, 0, 0)) #Default fg colour: Red
        self.state = kwargs.get('state', 'normal')
        pad = kwargs.get('pad', 0)
        self.text_render = self.font.render(text.center(len(text) + pad), 1, self.fg)
        self.draw()                
 
    def draw(self):
        x, y, w, h = self.text_render.get_rect()
        x, y = self.position
        pygame.draw.line(self.screen, self.bg, (x, y), (x + w , y), 5)
        pygame.draw.line(self.screen, self.bg, (x, y - 2), (x, y + h), 5)
        pygame.draw.line(self.screen, [abs(val-100) for val in self.bg], (x, y + h), (x + w , y + h), 5)
        pygame.draw.line(self.screen, [abs(val-100) for val in self.bg], (x + w , y+h), [x + w , y], 5)
        pygame.draw.rect(self.screen, [abs(val-50) for val in self.bg], (x, y, w , h))
        self.render_object = self.screen.blit(self.text_render, (x, y))

    def clicked(self):
        if self.state == 'normal':
            return self.render_object.collidepoint(pygame.mouse.get_pos())
        return False

#Defining some colours:
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.exit = False
        y = 400
        self.controlsBtn = Button(self.screen, (75, y), 'Controls', pad=5)
        self.startBtn = Button(self.screen, (290, y), 'Start', pad=5)
        self.quitBtn = Button(self.screen, (440, y), 'Quit', pad=6)
        base = resourcePath(path=True)
        self.titleImgs = [
            pygame.image.load(resourcePath(img)) 
            for img in os.listdir(base) if img.startswith('frame')
            ]
        self.count = 0
        self.clock = pygame.time.Clock()
        self.mainloop()

    def redrawGame(self):
        self.screen.fill((0, 200, 0))
        self.screen.blit(self.titleImgs[self.count//2], (75, 0))
        self.controlsBtn.draw()
        self.startBtn.draw()
        self.quitBtn.draw()
        pygame.draw.line(self.screen, WHITE, (0, 250), (700, 250), 5)
        pygame.draw.circle(self.screen, WHITE, (350, 250), 75, 5)
        pygame.display.update()
    
    def updateCount(self):
        if self.count < len(self.titleImgs)-1:
            self.count += 1
        else:
            self.count = 0

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.startBtn.clicked():
                        return
                    elif self.quitBtn.clicked():
                        self.exit = True
                        return
            self.redrawGame()
            self.updateCount()
            self.clock.tick(60)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.mainloop()
    
    def redrawGame(self):
        self.screen.fill(GREEN)
        pygame.draw.line(self.screen, WHITE, (0, 250), (700, 250), 5)
        pygame.draw.circle(self.screen, WHITE, (350, 250), 75, 5)
        pygame.display.update()

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.redrawGame()
            self.clock.tick(self.FPS)

WIDTH = 700
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Air Hockey!')
while not StartScreen(window).exit:
    Game(window)
pygame.quit()

