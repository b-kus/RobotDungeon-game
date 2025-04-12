# Complete your game here
import pygame
import random
from random import randint

class RobotDungeon:
    def __init__(self):
        pygame.init()

        self.game_over = False  

        self.load_char() 
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Dungeon")
        self.init_char()

        self.clock = pygame.time.Clock()

        self.game_font = pygame.font.SysFont("Arial", 24)

        self.main_loop()

        
    def load_char(self):
        self.robot = pygame.image.load("robot.png")
        self.rpos = []
        self.rheight = self.robot.get_height()
        self.rwidth = self.robot.get_width()

        self.width = self.rwidth * 20
        self.height = self.rheight * 9.2

        self.wall = pygame.image.load("wall.png")
        self.wwidth = self.wall.get_width()
        self.wheight = self.wall.get_height()
        self.wpos = []

        self.door = pygame.image.load("door.png")
        self.dheight = self.door.get_height()
        self.dwidth = self.door.get_width()
        self.doorpos = [[self.width - self.dwidth, self.height - self.wheight - self.dheight]]

        self.monster = pygame.image.load("monster.png")
        self.mwidth = self.monster.get_width()
        self.mheight = self.monster.get_height()
        self.monpos = [
            [self.width/2, self.height - self.wheight - self.mheight],
            [self.width/2, self.height - self.wheight - self.mheight - 2.9 * self.rheight],
            ]

        self.coin = pygame.image.load("coin.png")
        self.cwidth = self.coin.get_width()
        self.cheight = self.coin.get_height()
        self.cpos = []

    def init_char(self):
        self.coins = 0
        self.dir = -1
        self.cpos = []
        self.platform = 0
        x = 0 
        y = self.height - self.wheight 
        for times in range(4):
            for i in range(20):
                if i % 5 == 2:
                    self.cpos.append([x,y - self.cheight])
                self.wpos.append([x,y])
                x += self.wwidth
            y -= 2.9 * self.rheight
            x = 0

        self.rpos = [0, self.rheight * 9.2 - self.wheight - self.rheight]

        self.monpos = [
            [self.width/2 - self.mwidth, self.height - self.wheight - self.mheight],
            [self.width/2 - self.mwidth, self.height - self.wheight - self.mheight - 2.9 * self.rheight ],
            [self.width/2 - self.mwidth, self.height - self.wheight - self.mheight - 2.9 * self.rheight ],
            [self.width/2 - self.mwidth, self.height - self.wheight - self.mheight - 5.8 * self.rheight ],
            [self.width/2 - self.mwidth, self.height - self.wheight - self.mheight - 5.8 * self.rheight ],
            [self.width/2 - self.mwidth, self.height - self.wheight - self.mheight - 5.8 * self.rheight ],
            ]

        self.doorpos = [
            [0, self.height - self.wheight - self.dheight],
            [self.width - self.dwidth, self.height - self.wheight - self.dheight],
            [0, self.height - self.wheight - self.dheight - 2.9 * self.rheight ],
            [self.width - self.dwidth, self.height - self.wheight - self.dheight - 2.9 * self.rheight],
            [0, self.height - self.wheight - self.dheight - 2.9 * 2 * self.rheight ],
            [self.width - self.dwidth, self.height - self.wheight - self.dheight - 2.9 * 2 * self.rheight ]]

    def main_loop(self):
        self.dy = 0
        self.to_left = False
        self.to_right = False
        self.to_up = False
        
        while True:
            self.check_events()
            self.draw_window()
            self.clock.tick(50)
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.to_left = True
                if event.key == pygame.K_RIGHT:    
                    self.to_right = True
                if event.key == pygame.K_UP:
                    self.to_up = True
                
            
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.to_left = False
                if event.key == pygame.K_RIGHT:
                    self.to_right = False
                if event.key == pygame.K_UP:
                    self.to_up = False
                

            if event.type == pygame.QUIT:
                exit()

        if not self.game_over:
            self.move()

    def move_monster(self):
        if self.monpos[0][0] == 0:
            self.dir = 1
        if self.monpos[0][0] == self.width - self.mwidth:
            self.dir = -1
        self.monpos[0][0] += self.dir
        self.monpos[1][0] += self.dir
        self.monpos[3][0] += self.dir 
        self.monpos[2][0] -= self.dir
        self.monpos[4][0] -= self.dir
        if randint(0, 60) == 0:
            self.monpos[5][0] = randint(200, 800)


    def check_hit(self, name):
        if name == "coin":
            i = 0
            while i < len(self.cpos):
                xrob = self.rpos[0] + self.rwidth/2
                xcoin = self.cpos[i][0] + self.cwidth / 2
                yrob = self.rpos[1] + self.rheight /2
                ycoin = self.cpos[i][1] + self.cheight / 2

                xdiff = abs(xrob - xcoin)
                ydiff = abs(yrob - ycoin)

                xtot = self.rwidth/2 + self.cwidth / 2
                ytot = self.rheight/2 + self.cheight / 2

                if xdiff < xtot and ydiff < ytot:
                    self.cpos.pop(i)
                    self.coins += 1
                    return
                i += 1

        if name == "door":
            for i in self.doorpos:
                xrob = self.rpos[0] + self.rwidth/2
                xcoin = i[0] + self.dwidth / 2
                yrob = self.rpos[1] + self.rheight /2
                ycoin = i[1] + self.dheight / 2

                xdiff = abs(xrob - xcoin)
                ydiff = abs(yrob - ycoin)

                xtot = self.rwidth/2 + self.dwidth / 2
                ytot = self.rheight/2 + self.dheight / 2

                if xdiff < xtot and ytot > ydiff:
                    if self.doorpos.index(i) == 1:
                        self.rpos[0] = 0
                        self.rpos[1] = self.height - self.wheight - self.rheight - 2.9 * self.rheight
                        self.platform = 1
                        return
                    if self.doorpos.index(i) == 3:
                        self.rpos[0] = 0
                        self.rpos[1] = self.height - self.wheight - self.rheight - 5.8 * self.rheight
                        self.platform = 2
                        return
                    if self.doorpos.index(i) == 5:
                        self.game_over = True
                        return True

        if name == "monster":
            for i in self.monpos:
                xrob = self.rpos[0] + self.rwidth/2
                xcoin = i[0] + self.dwidth / 2
                yrob = self.rpos[1] + self.rheight /2
                ycoin = i[1] + self.dheight / 2

                xdiff = abs(xrob - xcoin)
                ydiff = abs(yrob - ycoin)

                xtot = self.rwidth/2 + self.dwidth / 2 - 10
                ytot = self.rheight/2 + self.dheight / 2 - 10

                if xdiff < xtot and ytot > ydiff:
                    self.init_char()

        
    def win(self):
        self.game_over = True
        game_text = self.game_font.render("Congratulations, you won!", True, (150, 20, 100))
        game_text_x = self.width / 2 - game_text.get_width() / 2
        game_text_y = self.height / 2 - game_text.get_height() / 2
        pygame.draw.rect(self.screen, (0, 0, 0), (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))            
        self.screen.blit(game_text, (game_text_x, game_text_y))

    def move(self):
        base_height = self.height - self.wheight - self.rheight

        if self.to_right:
            self.rpos[0] += 5

        if self.to_left:
            self.rpos[0] -= 5

        if self.to_up:
            self.jump()

        if self.dy >= 0:
            self.rpos[1] -= self.dy 
            self.dy -= 1
        
        if -16 < self.dy <= 0:
            self.rpos[1] -= self.dy
            self.dy -= 1
            
        if self.height - self.wheight < self.rpos[1] + self.rheight:
            self.rpos[1] = self.height - self.wheight - self.rheight 
            
        if self.platform == 1:
            if self.rpos[1] >= base_height - 2.9 * self.rheight:
                self.rpos[1] = base_height - 2.9 * self.rheight
                self.dy = 0

        if self.platform == 2:
            if self.rpos[1] >= base_height - 5.8 * self.rheight:
                self.rpos[1] = base_height - 5.8 * self.rheight
                self.dy = 0
        
        if self.rpos[0] <= 0:
            self.rpos[0] = 0

        if self.rpos[0] >= self.width - self.rwidth:
            self.rpos[0] = self.width - self.rwidth
            

        self.move_monster()

        self.check_hit("coin")
        self.check_hit("door")
        self.check_hit("monster")


    def jump(self):
        base_height = self.height - self.wheight - self.rheight
        if (
            self.rpos[1] == base_height
            or self.rpos[1] == base_height - 2.9 * self.rheight
            or self.rpos[1] == base_height - 5.8 * self.rheight
        ):
            self.dy = 15

    def draw_window(self):
        self.screen.fill((0, 80, 88))

        for i in self.wpos:
            self.screen.blit(self.wall, (i[0], i[1]))

        for i in self.doorpos:
            self.screen.blit(self.door, (i[0], i[1]))

        for i in self.cpos:
            self.screen.blit(self.coin, (i[0], i[1]))

        for i in self.monpos:
            self.screen.blit(self.monster, (i[0], i[1]))

        if self.game_over:
            self.win()

        self.screen.blit(self.robot, (self.rpos[0], self.rpos[1]))

        game_text = self.game_font.render(f"Coins: {self.coins}", True, (150, 80, 80))
        self.screen.blit(game_text, (self.width - 100, 0))

        

        pygame.display.flip()


if __name__ == "__main__":
    RobotDungeon()

       
