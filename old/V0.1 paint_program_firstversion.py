import pygame
from pygame import * 
size=(900,600)
screen = display.set_mode(size) 


#Colours
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
orange = (255,152,0)
yellow = (255,255,0)
green = (0,255,0)
blue = (0,0,255)
colour = black

'''
=========== All Commands ===========
black - 1
red - 2
orange - 3
yellow - 4
green - 5
blue - 6


leftmouse - draw with selected colour
rightmouse - erase
f - fill screen with selected colour
c - clear screen

+ - increase brush/eraser size
- - decrease brush/eraser size
'''

shapeDrawn = False

#Size of brush (min of 1, max of 10)
brushSize = 2


#Background colour
screen.fill(white)

running = True
while running:
    for evt in event.get():
        
        

        #FInds out which mouse button is being pressed
        m1, m2, m3 = pygame.mouse.get_pressed()
        #If left mouse is being pressed, draw circles
        if m1 == 1:
            pos1, pos2 = pygame.mouse.get_pos()
            draw.circle(screen, colour,(pos1, pos2), brushSize)
            print("Drawing in", colour, "with a brush size of", brushSize)

        #If right mouse is eing pressed, erase (draw white circles)
        if m3 == 1:
            pos1, pos2 = pygame.mouse.get_pos()
            draw.circle(screen, white, (pos1, pos2), brushSize)
            print("Erasing with brush size of", brushSize)
        #Changing colours
            
        elif (pygame.key.get_pressed()[pygame.K_1]):
            colour = black
            print("Colour was changed to black")
            time.wait(50)
        elif (pygame.key.get_pressed()[pygame.K_2]):
            colour = red
            print("Colour was changed to red")
            time.wait(50)
        elif (pygame.key.get_pressed()[pygame.K_3]):
            colour = orange
            print("Colour was changed to orange")
            time.wait(50)
        elif (pygame.key.get_pressed()[pygame.K_4]):
            colour = yellow
            print("Colour was changed to yellow")
            time.wait(50)
        elif (pygame.key.get_pressed()[pygame.K_5]):
            colour = green
            print("Colour was changed to green")
        elif (pygame.key.get_pressed()[pygame.K_6]):
            colour = blue
            print("Colour was changed to blue")
            time.wait(50)
                
        #Changing brush sizes

        elif (pygame.key.get_pressed()[pygame.K_EQUALS]):
            brushSize += 1
            if brushSize > 20:
                brushSize -= 1
            print("Brush size was changed to", brushSize)
            time.wait(50)
        elif (pygame.key.get_pressed()[pygame.K_MINUS]):
            brushSize -= 1
            if brushSize < 2:
                brushSize += 1
            print("Brush size was changed to", brushSize)
            time.wait(50)

        #Screen fill the selected colour
        elif (pygame.key.get_pressed()[pygame.K_f]):
            screen.fill(colour)
            time.wait(50)
            print("Screen was filled in with", colour)

        #Clear screen
        elif (pygame.key.get_pressed()[pygame.K_c]):
            screen.fill(white)
            time.wait(50)
            print("Screen was cleared")

        #Draw a line
        elif (pygame.key.get_pressed()[K_l]):
            while shapeDrawn != True:
                if m1 == 1:
                    print("Drwing line")
                    lineX1, lineY1 = pygame.mouse.get_pos()
                    time.wait(100)
                    if m1 == 1:
                        lineX2, lineY2 = pygame.mouse.get_pos()
                        draw.line (screen, colour, (lineX1, lineY1), (lineX2, lineY2), brushSize)
                        print("Drwing line")
                        shapeDrawn = True
                
        elif evt.type == QUIT:
            running = False 
            
    
    
    display.flip() 

quit()

