import os
import sys
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from sprites import Player, Ball
from widgets import Button, InputBox, Screen
pygame.init()

def resourcePath(relativePath='', subdir='', path=False):
    ''' Returns absolute path of project resource '''
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

#Defining some colours:
RED = (255, 55, 55)
BLUE = (20, 20, 255)
YELLOW = (255, 255, 0)

class Animation:
    ''' Class for game animations '''
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

class ControlScreen(Screen):
    ''' Class for the game controls screen '''
    def __init__(self, screen):
        super().__init__(screen)
        self.subPath = os.path.join('Header frames', 'Control screen')
        base = resourcePath(path=True, subdir=self.subPath)
        frames = [
            pygame.image.load(resourcePath(img, subdir=self.subPath))
            for img in os.listdir(base) if img.startswith('controls')
            ]
        self.title = Animation(frames, (self.w//4 - 10, 0))
        self.ball = Ball(self.w//2, self.h//2, 20)
        self.sprites.add(
            Player(75, 250, 35, RED),
            Player(self.w-75, 250, 35, BLUE),
            self.ball)
        with open(resourcePath('controls.txt'), 'r', encoding='utf-8') as f:
            delimiter = f.read(1)
            self.text = f.read()
        self.controls = self.text.split(delimiter)
        self.mainloop()

    def displayUI(self):
        ''' Displays the controls text, and inits back button '''
        xStart = 225
        yStart = 100
        xGap, yGap = 400, 40
        for i in range(len(self.controls)-1):
            for j, line in enumerate(self.controls[i].splitlines()):
                text_render = self.font.render(line, 1, RED)
                self.screen.blit(text_render, (xStart + i*xGap, yStart + j*yGap))
        self.backBtn = Button(self.screen, (0, 0), '\u2190', pad=2)
        self.backBtn.draw()

    def redrawGame(self):
        ''' Redraws the controls screen '''
        self.drawHockeyGround()
        self.title.update(self.screen)
        self.displayUI()
        self.sprites.update(self.screen)
        pygame.display.update()

    def mainloop(self):
        ''' Controls screen event loop '''
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
            self.clock.tick(self.FPS)

class StartScreen(Screen):
    ''' Class for the game start screen '''
    def __init__(self, screen, entryText='Enter name'):
        super().__init__(screen)
        self.exit = False
        y = 425
        self.controlsBtn = Button(
            self.screen, (self.w//2-190, y), 'Controls', pad=6, center=1
            )
        self.startBtn = Button(self.screen, (self.w//2, y), 'Start', pad=6, center=1)
        self.quitBtn = Button(self.screen, (self.w//2+160, y), 'Quit', pad=6, center=1)
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
        self.entryWidgets = [
            InputBox(self.w//5-25, self.h//2-40, 200, 75, entryText),
            InputBox(self.w//2+100, self.h//2-40, 200, 75, entryText)
            ]
        self.mainloop()

    def redrawGame(self):
        ''' Redraws the start screen '''
        self.screen.fill((0, 200, 0))
        self.drawHockeyGround()
        #Updating sprites
        self.sprites.update(self.screen)
        #Drawing UI
        self.controlsBtn.draw()
        self.startBtn.draw()
        self.quitBtn.draw()
        for e in self.entryWidgets:
            e.draw(self.screen)
            e.update()
        #Drawing start title
        self.title.update(self.screen)
        pygame.display.update()

    def mainloop(self):
        ''' Start screen event loop '''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                    return
                [e.handle_event(event) for e in self.entryWidgets]
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.startBtn.clicked():
                        if all(e.val for e in self.entryWidgets):
                            return
                    if self.quitBtn.clicked():
                        self.exit = True
                        return
                    if self.controlsBtn.clicked():
                        ControlScreen(self.screen)
            self.redrawGame()
            self.clock.tick(self.FPS)

    def getPlayerNames(self):
        ''' Returns the values from entry widgets '''
        return [e.val.title() for e in self.entryWidgets]

class PauseScreen(Screen):
    ''' Class for the game pause screen '''
    def __init__(self, screen, scoreToWin, endTime):
        super().__init__(screen)
        self.backBtn = Button(
            self.screen,
            (self.w//2-150, self.h-100),
            'Return to game',
            pad=5
            )
        self.font = pygame.font.SysFont('Verdana', 35)
        delim = '$'
        aboutText = f'''
        Air Hockey is a great two-player game! $RED
        Control the mallet using the keyboard to score! $YELLOW
        There are only two rules to the game: $BLUE
        1. Be the first to score {scoreToWin} goals in {endTime} $RED
        2. Enjoy! $RED
        '''
        self.aboutText = dict(
            [line.strip().split(delim) for line in aboutText.splitlines()[1:-1]]
            )
        self.subPath = os.path.join('Header frames', 'Pause screen')
        base = resourcePath(path=True, subdir=self.subPath)
        frames = [
            pygame.image.load(resourcePath(img, subdir=self.subPath))
            for img in os.listdir(base) if img.startswith('pause')
            ]
        self.title = Animation(frames, (self.w//5-5, 0))
        self.pauseTime = time.time()
        self.mainloop()

    def redrawGame(self):
        ''' Redraws the pause screen '''
        self.screen.fill((0, 200, 0))
        self.drawHockeyGround()
        #Drawing UI
        for i, line in enumerate(self.aboutText):
            self.screen.blit(
                self.font.render(line, 1, eval(self.aboutText[line])),
                (self.w//4-100, i*50 + 125)
                )
        self.backBtn.draw()
        #Drawing start title
        self.title.update(self.screen)
        pygame.display.update()

    def updateTime(self):
        ''' Calculates the time paused '''
        self.pauseTime = int(time.time() - self.pauseTime)

    def mainloop(self):
        ''' Pause screen event loop '''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.updateTime()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.backBtn.clicked():
                        self.updateTime()
                        return
            self.redrawGame()
            self.clock.tick(self.FPS)

class EndScreen(Screen):
    ''' Class for the game end screen '''
    def __init__(self, screen, winners):
        super().__init__(screen)
        for i, winner in enumerate(winners):
            winner.x = self.w//2 - 3.5*winner.r*(len(winners) - 1) + 7*winner.r*i
            winner.y = self.h//2
            winner.controls = None
        self.winners = winners
        self.backBtn = Button(
            self.screen,
            (self.w//2-160, self.h-50),
            'Back to menu',
            pad=5,
            center=1
            )
        self.playBtn = Button(
            self.screen,
            (self.w//2+135, self.h-50),
            'Play again',
            pad=5,
            center=1
            )
        creditsText = '''
        Created by: Sanvit Katrekar
        Images: Generated by textanim.com
        '''
        self.creditsText = [line.strip() for line in creditsText.splitlines()[1:]]
        self.subPath = os.path.join('Header frames', 'End screen')
        base = resourcePath(path=True, subdir=self.subPath)
        frames = [
            pygame.image.load(resourcePath(img, subdir=self.subPath))
            for img in os.listdir(base) if img.startswith('end')
            ]
        self.title = Animation(frames, (self.w//4 - 20, 10))
        self.playAgain = False
        self.mainloop()

    def redrawGame(self):
        ''' Redraws the end screen '''
        self.screen.fill((0, 200, 0))
        self.drawHockeyGround()
        #Drawing UI
        self.backBtn.draw()
        self.playBtn.draw()
        for i, line in enumerate(self.creditsText):
            self.screen.blit(
                self.font.render(line, 1, RED),
                (self.w//4 + 25, i*50 + self.h//2 + 80)
                )
        #Displaying win text
        text = self.font.render(
                ' and '.join(w.name for w in self.winners) +
                ' win' + 's'*(not bool(len(self.winners)-1)) + '!', 1, RED
                )
        rect = text.get_rect()
        rect.center = (self.w//2, self.h//2 - 100)
        self.screen.blit(text, (rect.x, rect.y))
        drawText = self.font.render('Draw'*(bool(len(self.winners)-1)), 1, RED)
        rect = drawText.get_rect()
        rect.center = (self.w//2, self.h//2)
        self.screen.blit(drawText, (rect.x, rect.y))
        #Drawing start title
        self.title.update(self.screen)
        #Drawing winner sprite
        for winner in self.winners:
            winner.update(self.screen)
        pygame.display.update()

    def mainloop(self):
        ''' Win screen event loop '''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.backBtn.clicked():
                        return
                    if self.playBtn.clicked():
                        self.playAgain = True
                        return
            self.redrawGame()
            self.clock.tick(self.FPS)

class Game(Screen):
    ''' Class for the main game screen '''
    def __init__(self, screen, names, **kwargs):
        super().__init__(screen, fontsize=60)
        self.displayFont = pygame.font.SysFont('Garamond', 125)
        self.pauseBtn = Button(self.screen, (self.w//2-70, self.h-100), 'Pause', pad=5)
        self.ball = Ball(self.w//2, self.h//2, 20, (0, self.w), (0, self.h))
        self.sprites.add(
            Player(
                75, self.h//2-10, 35, RED,
                (0, self.w//2), (0, self.h),
                controls='WSAD'
                ),
            Player(
                self.w-75, self.h//2-10, 35, BLUE,
                (self.w//2, self.w), (0, self.h),
                controls='IKJL'
                ),
            self.ball)
        for i, sprite in enumerate(self.sprites):
            if i == len(names):
                break
            sprite.name = names[i]
        #Defining game play attributes
        self.elapsedTime = '00:00'
        self.showTime = True
        self.showGoal = False
        self.run = False
        self.goalCounter = 0
        self.endTime = kwargs.get('endTime', '01:00')
        self.goalTextTime = kwargs.get('goalTextTime', 2)
        self.goalWaitTime = kwargs.get('goalWaitTime', 1)
        self.scoreToWin = kwargs.get('scoreToWin', 7)
        self.startTime = time.time()
        self.mainloop()

    def resetGame(self):
        ''' Resets sprites to default and adds up player score '''
        symbols = '<>'
        for sprite in self.sprites:
            sprite.x = sprite.defaultX
            sprite.y = sprite.defaultY
            if not any(
                eval(
                    f'self.ball.x{sym}self.w//2 and sprite.x{sym}self.w//2',
                    {'self': self, 'sprite': sprite}
                    )
                    for sym in symbols
                    ):
                sprite.score += 1

        self.ball = Ball(self.w//2, self.h//2, 20, (0, self.w), (0, self.h))
        self.sprites.add(self.ball)

        self.redrawGame()
        self.goalCounter = time.time()
        while time.time() - self.goalCounter <= self.goalWaitTime:
            pass
        self.ball.lastTouched = True
        self.goalCounter = 0

    def displayText(self, text, pos):
        ''' Displas game announcements '''
        text = self.displayFont.render(text, 1, RED)
        self.screen.blit(text, pos)

    def checkGoal(self):
        ''' Resets game if goal is scored '''
        if self.ball.alive():
            return
        if not self.goalCounter:
            self.goalCounter = time.time()
            self.showTime = False
            self.showGoal = True

        if time.time() - self.goalCounter >= self.goalTextTime:
            self.showGoal = False
            self.resetGame()
            self.showTime = True
            self.startTime += self.goalTextTime + self.goalWaitTime

    def updateTime(self):
        ''' Updating game time '''
        diff = int(time.time() - self.startTime)
        self.elapsedTime = ':'.join(
            [str(val).zfill(2) for val in divmod(diff, 60)]
            )

    def redrawGame(self):
        ''' Redraws entire game screen '''
        self.screen.fill((0, 200, 0))
        #Drawing Hockey Ground
        self.drawHockeyGround()
        #Drawing game time
        if self.showTime:
            text = self.font.render(self.elapsedTime, 1, RED)
            self.screen.blit(text, (self.w//2 - 50, 50))
        if self.showGoal:
            self.displayText('Goal!', (self.w//3 + 25, self.h//4 + 50))
        #Updating sprites
        self.sprites.update(self.screen)
        for sprite in self.sprites:
            if callable(getattr(sprite, 'checkCollision', None)):
                sprite.checkCollision(self.ball)
            else:
                break
        #Updating game time
        self.updateTime()
        #Drawing UI
        self.pauseBtn.draw()
        pygame.display.update()

    def timeUpWinner(self):
        ''' Compares player scores and returns the winner '''
        maxScore = -1
        for sprite in self.sprites:
            if sprite.score == maxScore:
                winner = None
                break
            if sprite.score > maxScore:
                winner = sprite
                maxScore = sprite.score
        return winner


    def gameOver(self, winner=None):
        ''' Creates an end screen instance and checks for Play Again '''
        self.ball.kill()
        end = EndScreen(
            self.screen,
            pygame.sprite.GroupSingle(winner) if winner else self.sprites
            )
        self.run = end.playAgain

    def mainloop(self):
        ''' Main game event loop '''
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pauseBtn.clicked():
                        pauseTime = PauseScreen(
                            self.screen, self.scoreToWin, self.endTime
                            ).pauseTime
                        self.startTime += pauseTime
            self.checkGoal()
            #Checking if player has scored the required no. of goals to win
            for sprite in self.sprites:
                if hasattr(sprite, 'score') and sprite.score == self.scoreToWin:
                    self.gameOver(sprite)
                    return
            #Checking if time is up
            if self.elapsedTime == self.endTime and self.showTime:
                self.ball.kill()
                self.redrawGame()
                self.displayText('Time Up!', (self.w//3-50, self.h//4 + 40))
                pygame.display.update()
                counter = time.time()
                while time.time() - counter < self.goalTextTime:
                    pass
                self.gameOver(self.timeUpWinner())
                return
            self.redrawGame()
            self.clock.tick(self.FPS)

#Initializing game window
WIDTH = 1000
HEIGHT = 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Air Hockey!')
pygame.display.set_icon(
    pygame.image.load(resourcePath('icon.png', subdir='Game icons'))
    )

while True:
    startScreen = StartScreen(window)
    playerNames = startScreen.getPlayerNames()
    if startScreen.exit:
        break
    while Game(window, playerNames, endTime='03:00').run:
        pass
pygame.quit()
