import os
import sys
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from sprites import Player, Ball
pygame.init()

def resourcePath(relativePath='', subdir='', path=False):
    ''' Returns project absolute path '''
    try:
        basePath = sys._MEIPASS
    except AttributeError:
        if relativePath.endswith('.txt'):
            folder = 'Text files'
        else:
            folder = 'Images'
        basePath = os.path.abspath(folder)
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
RED = (255, 55, 55)
GREEN = (0, 200, 0)
BLUE = (20, 20, 255)
BLACK = (0, 0, 0)

class Animation:
    def __init__(self, frames, pos):
        self.frames = frames
        self.pos = pos
        self.count = 0
    
    def update(self, screen):
        if self.count < len(self.frames)-1:
            self.count += 1
        else:
            self.count = 0
        screen.blit(self.frames[self.count//2], self.pos)

class ControlScreen:
    def __init__(self, screen, textFg=(255, 0, 0)):
        self.screen = screen
        self.w, self.h = self.screen.get_size()
        self.subPath = os.path.join('Header frames', 'Control screen')
        base = resourcePath(path=True, subdir=self.subPath)
        frames = [
            pygame.image.load(resourcePath(img, subdir=self.subPath))
            for img in os.listdir(base) if img.startswith('controls')
            ]
        self.title = Animation(frames, (self.w//4 - 10, 0))
        self.sprites = pygame.sprite.Group()
        self.ball = Ball(self.w//2, self.h//2, 20)
        self.sprites.add(
            Player(75, 250, 35, RED),
            Player(self.w-75, 250, 35, BLUE),
            self.ball)
        self.font = pygame.font.SysFont('Didot', 40)
        self.textFg = textFg
        with open(resourcePath('controls.txt'), 'r', encoding='utf-8') as f:
            delimiter = f.read(1)
            self.text = f.read()
        self.controls = self.text.split(delimiter)
        self.clock = pygame.time.Clock()
        self.mainloop()

    def displayUI(self):
        xStart = 225
        yStart = 100
        xGap, yGap = 400, 40
        for i in range(len(self.controls)-1):
            for j, line in enumerate(self.controls[i].splitlines()):
                text_render = self.font.render(line, 1, self.textFg)
                self.screen.blit(text_render, (xStart + i*xGap, yStart + j*yGap))
        self.backBtn = Button(self.screen, (0, 0), '\u2190', pad=2)
    
    def redrawGame(self):
        #Drawing Hockey Ground
        self.screen.fill(GREEN)
        pygame.draw.line(self.screen, WHITE, (self.w//2, 0), (self.w//2, self.h), 5)
        pygame.draw.circle(self.screen, WHITE, (self.w//2, self.h//2), 75, 5)
        pygame.draw.line(self.screen, BLACK, (2, 175), (2, 325), 5)
        pygame.draw.line(self.screen, BLACK, (self.w-3, 175), (self.w-3, 325), 5)
        pygame.draw.rect(self.screen, WHITE, (-1, self.h//5, 150, 300), 5)
        pygame.draw.rect(self.screen, WHITE, (self.w-148, self.h//5, 150, 300), 5)
        #Drawing game title
        self.title.update(self.screen)
        #Drawing controls text
        self.displayUI()
        #Drawing players in background
        self.sprites.update(self.screen)
        pygame.display.update()

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.backBtn.clicked():
                        return
            self.redrawGame()
            self.clock.tick(60)

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.w, self.h = self.screen.get_size()
        self.exit = False
        start = self.w//7 + 5
        y = 400
        self.controlsBtn = Button(self.screen, (start + 75, y), 'Controls', pad=5)
        self.startBtn = Button(self.screen, (start + 290, y), 'Start', pad=5)
        self.quitBtn = Button(self.screen, (start + 440, y), 'Quit', pad=6)
        self.subPath = os.path.join('Header frames', 'Start screen')
        base = resourcePath(path=True, subdir=self.subPath)
        frames = [
            pygame.image.load(resourcePath(img, subdir=self.subPath))
            for img in os.listdir(base) if img.startswith('start')
            ]
        self.title = Animation(frames, (self.w//4 - 10, 0))
        self.sprites = pygame.sprite.Group()
        self.ball = Ball(self.w//2, self.h//2, 20)
        self.sprites.add(
            Player(75, 250, 35, RED),
            Player(self.w-75, 250, 35, BLUE),
            self.ball)
        self.clock = pygame.time.Clock()
        self.mainloop()

    def redrawGame(self):
        ''' Redraws entire game screen '''
        self.screen.fill((0, 200, 0))
        #Drawing Hockey Ground
        pygame.draw.line(self.screen, WHITE, (self.w//2, 0), (self.w//2, self.h), 5)
        pygame.draw.circle(self.screen, WHITE, (self.w//2, self.h//2), 75, 5)
        pygame.draw.line(self.screen, BLACK, (2, 175), (2, 325), 5)
        pygame.draw.line(self.screen, BLACK, (self.w-3, 175), (self.w-3, 325), 5)
        pygame.draw.rect(self.screen, WHITE, (-1, self.h//5, 150, 300), 5)
        pygame.draw.rect(self.screen, WHITE, (self.w-148, self.h//5, 150, 300), 5)
        #Updating sprites
        self.sprites.update(self.screen)
        #Drawing UI
        self.controlsBtn.draw()
        self.startBtn.draw()
        self.quitBtn.draw()
        #Drawing start title
        self.title.update(self.screen)
        pygame.display.update()

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
                    elif self.controlsBtn.clicked():
                        ControlScreen(self.screen)
            self.redrawGame()
            self.clock.tick(60)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Didot', 60)
        self.w, self.h = self.screen.get_size()
        self.pauseBtn = Button(self.screen, (self.w//2-70, self.h-100), 'Pause', pad=5)
        self.sprites = pygame.sprite.Group()
        self.ball = Ball(self.w//2, self.h//2, 20)
        self.sprites.add(
            Player(75, 250, 35, RED, (0, self.w//2), (0, self.h), 'WSAD'),
            Player(self.w-75, 250, 35, BLUE, (self.w//2, self.w), (0, self.h), 'IKJL'),
            self.ball)
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.startTime = time.time()
        self.mainloop()

    def updateTime(self):
        time_elapsed = int(time.time() - self.startTime)
        return ':'.join([str(val).zfill(2) for val in divmod(time_elapsed, 60)])

    def redrawGame(self):
        ''' Redraws entire game screen '''
        self.screen.fill((0, 200, 0))
        #Drawing Hockey Ground
        pygame.draw.line(self.screen, WHITE, (self.w//2, 0), (self.w//2, self.h), 5)
        pygame.draw.circle(self.screen, WHITE, (self.w//2, self.h//2), 75, 5)
        pygame.draw.line(self.screen, BLACK, (2, 175), (2, 325), 5)
        pygame.draw.line(self.screen, BLACK, (self.w-3, 175), (self.w-3, 325), 5)
        pygame.draw.rect(self.screen, WHITE, (-1, self.h//5, 150, 300), 5)
        pygame.draw.rect(self.screen, WHITE, (self.w-148, self.h//5, 150, 300), 5)
        #Drawing game header
        self.text_render = self.font.render(self.updateTime(), 1, RED)
        self.screen.blit(self.text_render, (self.w//2 - 50, 50))
        #Updating sprites
        self.sprites.update(self.screen)
        #Drawing UI
        self.pauseBtn.draw()
        pygame.display.update()

    def mainloop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pauseBtn.clicked():
                        return
            self.redrawGame()
            self.clock.tick(self.FPS)

WIDTH = 1000
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Air Hockey!')
while not StartScreen(window).exit:
    Game(window)
pygame.quit()

