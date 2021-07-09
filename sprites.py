import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, r, colour, xLimits=None, yLimits=None, controls=None):
        super().__init__()
        self.x = x
        self.y = y
        self.r = r
        self.colour = colour
        self.xLimits = xLimits
        self.yLimits = yLimits
        if controls:
            self.controls = dict(
                zip(
                    ['Up', 'Down', 'Left', 'Right'],
                    [eval('pygame.K_' + c.lower()) for c in controls]
                ))
        else:
            self.controls = controls
        self.vel = 10

    def check_movement(self):
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

    def update(self, screen):
        if self.controls:
            self.check_movement()
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.r+1, 1)
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.r)
        spacing = 4
        for i in range(1, 3):
            pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.r-spacing*i, 1)
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.r//4, 2)

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, r, colour=(255, 255, 255)):
        super().__init__()
        self.x = x
        self.y = y
        self.r = r
        self.colour = colour

    def update(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.r+1, 1)
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.r)