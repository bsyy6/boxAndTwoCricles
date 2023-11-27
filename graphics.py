import pygame
import numpy as np
from scipy.interpolate import interp1d

class GraphicsHandler:
    def __init__(self, width = 800, height=600):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        
        self.midX = self.width / 2
        self.midY = self.height / 2

        # colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)

        # interaction parameters
        self.max_scale = 0.1
        self.intersection = 0.1
        self.startColor = self.black
        self.finalColor = self.white
        self.dcolor = tuple(np.subtract(self.finalColor,self.startColor))

        # define box parameters
        self.box_width = 200
        self.box = self.makeBox(self.box_width,self.white)
        # position on screen
        self.xPos_Box = self.midX - self.box_width / 2
        self.yPos_Box = self.midY - self.box_width / 2

        # define circle parameters
        self.circle_radius = 50
        self.circle = self.makeCircle(self.circle_radius,self.red)

        # postion on screen
        self.xPos_CirL = self.midX - (self.box_width / 2 + self.circle_radius)
        self.xPos_CirR = self.midX + (self.box_width / 2 + self.circle_radius)
        self.yPos_Cir = self.midY

        self.scale = 1 # 1 is no scale 

        # define circle position parameters
        self.CirclePos_max =  self.width/2  - self.box_width/2 - self.circle_radius
        self.CirclePos_min =  self.width/4  - self.circle_radius
        self.dCircle = self.CirclePos_max - self.CirclePos_min

        # define voltage parameters
        self.x_touchPoint = 4
        self.x_max = 10
        self.x_min = 0
        self.vibrate = True


    def makeBox(self, box_width, color):
        box = pygame.Surface((box_width, box_width), pygame.SRCALPHA)
        pygame.draw.rect(box, color, (0, 0, box_width, box_width))
        return box
       
    def makeCircle(self,r,color):
        circle = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(circle, color, (r, r), r)
        return circle

    def draw_circle(self, color):
        pygame.draw.circle(self.window, color, (self.circle_x, self.circle_y), self.circle_radius)
        
    def draw_box(self, color):
        pygame.draw.rect(self.window, color, (self.xPos_Box, self.yPos_Box, self.box_width, self.box_width))
    
    
    def updatePosition(self, x_input):
        squeezing = (x_input >= self.x_touchPoint)
        if squeezing:
            self.vibrate = False
            portion =  (x_input - self.x_touchPoint) / (self.x_max - self.x_touchPoint)
            scale = self.max_scale * portion
            self.scale = scale + 1
            circleRaduisH = round(self.circle_radius/self.scale)
            self.xPos_CirL = self.xPos_Box - circleRaduisH * (1 - self.intersection*portion) +1
            if portion > 0.9:
                color = self.finalColor
            else:
                color = self.startColor 
        else:
            self.vibrate = True
            portion =  (x_input - self.x_min) / (self.x_touchPoint - self.x_min)
            self.scale = 1 # 1 is no scale
            self.xPos_CirL = self.CirclePos_min + self.dCircle* portion
            color = self.startColor
        
        self.xPos_CirR = self.width - self.xPos_CirL
        return 

    def draw(self):
        self.screen.fill(self.black)
        self.screen.blit(self.circle, (round(self.xPos_CirR-self.circle_radius/self.scale), self.yPos_Cir-self.circle_radius*self.scale)) 
        self.screen.blit(self.circle, (round(self.xPos_CirL-self.circle_radius/self.scale), self.yPos_Cir-self.circle_radius*self.scale))
        self.screen.blit(self.box, (self.xPos_Box, self.yPos_Box))
        pygame.display.flip()

    def close(self):
        pygame.quit()

