import pygame
import numpy as np
from scipy.interpolate import interp1d

def fcn(v_input, y_input, yPosIn_box, yPosIn_circle):
    """
    % Waleed - 2023
    % This function moves two circles towards a box and squeezes them against it.
    %
    % args:
    % x is the scaled voltage from the ADC.
    % MUST BE 0 minimum 10 maximum. change code for other ranges.
    % 
    % returns:
    % this code shows x = 0->3.999 as the free movment of the cricles towards the box.
    % 4 means it touched the object
    % 4-10 the balls squeeze against the box:
    %
    %  To do:
    %  - Linearly changing the box color.
    %  - Scaling the cricles to show them squeezing.
    """


    # Initialize Pygame
    pygame.init()

    # Pygame window setup
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    midY = screen_height / 2
    midX = screen_width / 2

    # Define colors
    black = (0, 0, 0)
    white = (255, 255, 255)
   
    # Define parameters
    max_scale = 0.1 
    intersection = 0.1
    startColor = (0, 0, 0)
    finalColor = (255, 255, 255)
    dColor = tuple(np.subtract(finalColor,startColor))
    
    circleRadius = 50
    box_width = 200
    
    minV = 0
    maxV = 3


    x_touchPoint = 4
    x_max = 10
    x_min = 0

    # box pos is calculated from the left top corner of screen to the left top corner of the box
    xPos_Box = midX - box_width / 2
    yPos_Box = midY - box_width / 2

    # circle pos is calculated the left top corner of screen to the center of the circle
    xPos_CirL = midX - (box_width / 2 + circleRadius)
    xPos_CirR = midX + (box_width / 2 + circleRadius)
    yPos_Cir = midY

    # map the input voltage to the x values between 0(x_min) and 10(x_max)

    mapper = interp1d([minV, maxV], [x_min,x_max])
    #x_input = float(mapper(v_input))
    x_input = v_input # debugging
    
    
    
    CirclePos_max =  screen_width/2  - box_width/2 - circleRadius
    CirclePos_min =  screen_width/4 - circleRadius
    dCircle = CirclePos_max - CirclePos_min
    circleSurface = pygame.Surface((circleRadius * 2, circleRadius * 2), pygame.SRCALPHA)
    # circleSurface.fill((250,200,0))
    squareSurface = pygame.Surface((box_width, box_width), pygame.SRCALPHA)
    pygame.draw.circle(circleSurface, white, (circleRadius,circleRadius), circleRadius)
    pygame.draw.rect(squareSurface, white, (0,0,box_width,box_width))
    
    squeezing = (x_input >= x_touchPoint)
    if squeezing:
        vibrate = False
        portion =  (x_input - x_touchPoint) / (x_max - x_touchPoint)
        scale = max_scale * portion
        scale = scale + 1
        circleRaduisH = round(circleRadius/scale)
        xPos_CirL = xPos_Box - circleRaduisH * (1 - intersection*portion) +1
        if portion > 0.9:
            color = finalColor
        else:
            color = startColor 
    else:
        vibrate = True
        portion =  (x_input - x_min) / (x_touchPoint - x_min)
        scale = 1 # 1 is no scale
        xPos_CirL = CirclePos_min + dCircle* portion
        color = startColor
    
    xPos_CirR = screen_width - xPos_CirL
    


    
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(black)  # Clear screen

        # Logic for circles and box animation goes here

        # screen.blit(scaled_surface, (width // 2 - 50, height // 2 - int(100 * 1.5) // 2))  # Place the oval in the center
        if(not vibrate):
            circleSurface = pygame.transform.scale_by(circleSurface, (1/scale, scale))
            vibrate = True
        
        screen.blit(circleSurface, (round(xPos_CirR-circleRadius/scale), yPos_Cir-circleRadius*scale)) 
        screen.blit(circleSurface, (round(xPos_CirL-circleRadius/scale), yPos_Cir-circleRadius*scale))
        screen.blit(squareSurface, (xPos_Box, yPos_Box))

        pygame.display.flip()  # Update the display
        clock.tick(60)  # Control frame rate

    pygame.quit()

fcn(3.9,0,0,0)