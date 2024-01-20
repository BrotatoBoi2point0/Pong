# Programmer: Aaron Cassell. (@BrotatoBoi)
# Program Name: Pong.
# Date: April/06/2023.
# Description: A simple Pong game to ease back into programming.


import pygame
from random import choices
from time import sleep

pygame.init()

SCREEN = pygame.display.set_mode((800, 600))


class Ball(pygame.Rect):
    def __init__(self):
        super(Ball, self).__init__(SCREEN.get_width()//2, SCREEN.get_height()//2, 25, 25)
        self.center = (self.x, self.y)
        self.speed = choices([(1, 1), (-1, -1), (-1, 1), (1, -1)], [25, 25, 25, 25])[0]

    def render(self):
        pygame.draw.rect(SCREEN, (255, 255, 255), self)

    def move(self):
        self.x = self.x+self.speed[0]
        self.y = self.y+self.speed[1]

    def bounce(self):
        if self.top <= 0 or self.bottom >= SCREEN.get_height():
            self.speed = (self.speed[0], self.speed[1]*-1)

    def reset_ball(self):
        resetBall = False

        if self.right <= 0:
            print("Right scored a goal!")
            resetBall = True
        elif self.left >= SCREEN.get_width():
            print("Left scored a goal!")
            resetBall = True

        if resetBall:
            self.x = SCREEN.get_width()//2
            self.y = SCREEN.get_height()//2
            self.speed = choices([(1, 1), (-1, -1), (-1, 1), (1, -1)], [25, 25, 25, 25])[0]

class Paddle(pygame.Rect):
    def __init__(self, isBot, isFirst, ball):
        if isFirst:
            x = 50
        else:
            x = SCREEN.get_width()-50

        super(Paddle, self).__init__(x, SCREEN.get_height()//2, 10, 200)
        self.center = (self.x, self.y)
        self._isBot = isBot
        self._isFirst = isFirst
        self.ball = ball

    def render(self):
        pygame.draw.rect(SCREEN, (255, 255, 255), self)

    def move(self, dir):
        if dir == 'UP' and self.top != 0:
            self.y = self.y-1
        elif dir == 'DOWN' and self.bottom != SCREEN.get_height():
            self.y = self.y+1

    def hit_ball(self):
        if self._isFirst:
            if ((self.ball.left <= self.right and self.ball.top <= self.bottom and self.ball.bottom >= self.top)):
                self.ball.speed = (self.ball.speed[0]*-1.13, self.ball.speed[1])
        else:
            if (self.ball.right >= self.left and self.ball.top <= self.bottom and self.ball.bottom >= self.top):
                self.ball.speed = (self.ball.speed[0]*-1.13, self.ball.speed[1])



class Main:
    class Menu:
        def __init__(self, mainClass):
            self.mainClass = mainClass
            self.playColor = (61, 61, 61)
            self.exitColor = (61, 61, 61)

        def render(self):
            titleFont = pygame.font.SysFont('jokerman', 60)
            title = titleFont.render("Pong!", False, (125, 125, 125))
            SCREEN.blit(title, ((SCREEN.get_width()//2)-75, 50))


            btnFont = pygame.font.SysFont('jokerman', 50)

            # Render Play game
            btnPlay = btnFont.render("Start!", False, (125, 125, 125))
            pygame.draw.rect(SCREEN, self.playColor, ((SCREEN.get_width()//2)-200, 200, 400, 100))
            SCREEN.blit(btnPlay, ((SCREEN.get_width()//2)-60, 210))
                
            # Render exit
            btnExit = btnFont.render("Exit!", False, (125, 125, 125))
            pygame.draw.rect(SCREEN, self.exitColor, ((SCREEN.get_width()//2)-200, 400, 400, 100))
            SCREEN.blit(btnExit, ((SCREEN.get_width()//2)-60, 410))
                
            # Render version
            vFont = pygame.font.SysFont('jokerman', 15)
            vText = vFont.render("Version: 1.0", False, (125, 125, 125))
            SCREEN.blit(vText, (SCREEN.get_width()-150, SCREEN.get_height()-50))

        def update(self):
            #check where the mouse is located.
            mouse_pos = pygame.mouse.get_pos()

            #if the mouse cursor is over a button, highlight it.
            if mouse_pos[0] >= 200 and mouse_pos[0] <= 600 and mouse_pos[1] >= 200 and mouse_pos[1] <= 300:
                self.playColor = (100, 100 ,100)

                if self.mainClass._clicked:
                    self.mainClass._currentScreen = "playing"

            elif mouse_pos[0] >= 200 and mouse_pos[0] <= 600 and mouse_pos[1] >= 400 and mouse_pos[1] <= 500:
                self.exitColor = (100, 100 ,100)

                if self.mainClass._clicked:
                    self.mainClass._isRunning = False
            else:
                self.exitColor = (61, 61, 61)
                self.playColor = (61, 61, 61)

            #if the mouse has been clicked run the buttons action.
            # Play Game : 'playing'
            # Exit Game : self._isPlaying = False
            pass

    def __init__(self):
        self._isRunning = True
        self._currentScreen = 'menu'
        self._clicked = False

        self.menu = self.Menu(self)
        self.ball = Ball()
        self.paddle = Paddle(False, True, self.ball)
        self.paddle2 = Paddle(False, False, self.ball)
    
        self.execute()
    

    def render(self):
        SCREEN.fill((0, 0, 0))

        match self._currentScreen:
            case 'menu':
                self.menu.render()
            case 'playing':
                self.ball.render()
                #draw paddle1
                self.paddle.render()
                self.paddle2.render()
                #draw paddle2

        pygame.display.flip()

    def update(self):
        match self._currentScreen:
            case 'menu':
                self.menu.update()
            case 'playing':
                

                #move ball
                self.ball.move()
                #check collisions
                self.ball.bounce()
                self.ball.reset_ball()
                self.paddle.hit_ball()
                self.paddle2.hit_ball()
                #keep track of game info
                pass

    def get_events(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.paddle.move('UP')
        elif keys[pygame.K_s]:
            self.paddle.move('DOWN')
        if keys[pygame.K_i]:
            self.paddle2.move('UP')
        elif keys[pygame.K_k]:
            self.paddle2.move('DOWN')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._clicked = not self._clicked
            

    def execute(self):
        while self._isRunning:
            self.render()
            self.update()
            self.get_events()

            sleep(0.00013)


if __name__ == '__main__':
    Main()
