'''
This module defines game sprites.
Includes:
    1. Player
    2. Ball
'''
import math
import random
import pygame

class Player(pygame.sprite.Sprite):
    ''' Class that defines the game mallets '''
    def __init__(self, x, y, r, colour, xLimits=None, yLimits=None, **kwargs):
        super().__init__()
        self.x = self.defaultX = x
        self.y = self.defaultY = y
        self.r = r
        self.colour = colour
        self.xLimits = xLimits
        self.yLimits = yLimits
        self.vel = 10
        self.score = 0
        self.name = kwargs.get('name')
        arrowKeyControls = kwargs.get('arrowKeyControls')
        controls = kwargs.get('controls')  or arrowKeyControls
        if arrowKeyControls:
            eventList = [
                eval('pygame.K_' + c) for c in ('UP', 'DOWN', 'LEFT', 'RIGHT')
            ]
        elif controls:
            eventList = [eval('pygame.K_' + c.lower()) for c in controls]

        if controls:
            self.controls = dict(
                zip(['Up', 'Down', 'Left', 'Right'], eventList)
                )
        else:
            self.controls = controls

    def checkCollision(self, ball):
        ''' Checks for collision between player and ball, and bounces ball '''
        dist = math.sqrt((self.x-ball.x)**2 + (self.y-ball.y)**2) - (self.r + ball.r + ball.vel)
        if dist > 0:
            return False
        dx = -(self.x - ball.x)
        dy = self.y - ball.y
        tangent = math.atan2(dy, dx or 1)
        ball.angle = -tangent

        if ball.lastTouched != self:
            ball.vel += ball.incrementVel
        ball.lastTouched = self
        ball.x += dist*math.cos(ball.angle)*(-1)
        ball.y += dist*math.sin(ball.angle)*(-1)
        ball.move()

    def checkMovement(self):
        ''' Checks for key pressed for player movement '''
        keys = pygame.key.get_pressed()
        for control, key in self.controls.items():
            if keys[key]:
                if control == 'Up' and self.y >= self.yLimits[0]+self.vel+self.r:
                    self.y -= self.vel
                elif control == 'Down' and self.y <= self.yLimits[1]-self.vel-self.r:
                    self.y += self.vel
                elif control == 'Left' and self.x >= self.xLimits[0]+self.vel+self.r+5:
                    self.x -= self.vel
                elif control == 'Right' and self.x <= self.xLimits[1]-self.vel-self.r-5:
                    self.x += self.vel

    def drawScore(self, screen):
        ''' Draws the players score '''
        font = pygame.font.SysFont('Segoe UI Black', 30)
        text = font.render(f'Score: {self.score}', 1, (0, 0, 0))
        if self.x < screen.get_width()//2:
            screen.blit(text, (self.xLimits[0] + 10, 0))
        else:
            screen.blit(text, (self.xLimits[1] - 150, 0))

    def update(self, screen):
        ''' Updates the player sprite '''
        if self.controls:
            self.checkMovement()
            self.drawScore(screen)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.r+1, 1)
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.r)
        spacing = 4
        for i in range(1, 3):
            pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.r-spacing*i, 1)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.r//4, 2)

class Ball(pygame.sprite.Sprite):
    ''' Class that defines the game puck '''
    def __init__(self, x, y, r, xLimits=None, yLimits=None, colour=(255, 255, 255)):
        super().__init__()
        self.x = x
        self.y = y
        self.r = r
        self.colour = colour
        self.vel = 10
        self.xLimits = xLimits
        self.yLimits = yLimits
        self.angle = random.choice([math.pi-0.01, -0.01])
        self.lastTouched = None
        self.incrementVel = 0.5

    def isCollided(self):
        ''' Checks for collision with boundaries '''
        if self.x - (self.r + self.vel) <= self.xLimits[0]: #Left Boundary
            return 'left'
        if self.x + self.r + self.vel >= self.xLimits[1]: #Right boundary
            return 'right'
        if self.y + self.r + self.vel >= self.yLimits[1]: #Lower Boundary
            return 'down'
        if self.y - (self.r + self.vel) <= self.yLimits[0]: #Upper boundary
            return 'up'
        return False

    def checkGoal(self):
        ''' Checks whether a goal is scored '''
        goalYBounds = all([
            self.y - self.r >= 175,
            self.y + self.r <= 325
            ])
        goalXBounds = any([
            self.x - (self.r + self.vel) <= self.xLimits[0],
            self.x + self.r + self.vel >= self.xLimits[1]
            ])
        return goalYBounds and goalXBounds

    def bounce(self, direction):
        ''' Bounces the ball from the boundaries '''
        if direction in ['up', 'down']:
            self.angle = -self.angle
            if direction == 'up':
                self.y = self.yLimits[0] + (self.r + self.vel)
            else:
                self.y = self.yLimits[1] - (self.r + self.vel)
        else:
            if self.checkGoal():
                self.kill()
                return
            self.angle = math.pi - self.angle
            if direction == 'left':
                self.x = self.xLimits[0] + self.r + self.vel
            else:
                self.x = self.xLimits[1] - (self.r +self.vel)

    def move(self):
        ''' Handles ball movement '''
        collided = self.isCollided()
        if collided:
            self.bounce(collided)
        self.x += self.vel*math.cos(self.angle)*bool(self.lastTouched)
        self.y += self.vel*math.sin(self.angle)*bool(self.lastTouched)

    def update(self, screen):
        ''' Updates ball sprite '''
        if self.xLimits:
            self.move()
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.r+1, 1)
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.r)
