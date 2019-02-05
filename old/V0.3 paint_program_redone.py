#Dank Paint Program
#Created by Daniel Liu
#Version 0.3 - redone running loop and performance improvements

import pygame
from pygame import * 
size=(900,600)
screen = display.set_mode(size) 


'''
=========== All Commands ===========
leftmouse - draw with selected colour
middlemouse - eye drop
rightmouse - erase
f - fill screen with selected colour
c - clear screen
t - toggle colour wheel

s- save drawing
o - open a saved drawing (.png)

l - click twice for startpoint and endpoint to draw line

(Ctrl + Z) - Undo

+ - increase brush/eraser size
- - decrease brush/eraser size
'''

#INITALIZATION
#Colours
white = (255,255,255)
black = (0,0,0)

colour = black
backGround = white

blender = []
c1 = 0
c2 = 0
c3 = 0

#Toggles
colourWheelOn = 1
inputToggle = 1

#Size of brush (min of 1, max of 30)
brushSize = 3

#Draw background
screen.fill(backGround)

#LOAD ASSETS
#Load colour wheel
colourWheel = pygame.image.load("colourwheel.png")
myClock = time.Clock()

#Running loop
running = True
while running:
    for evt in event.get():
        
        if evt.type == QUIT:
            running = False
        
        
    #FInds out which mouse button is being pressed and where the mouse is
    m1, m2, m3 = pygame.mouse.get_pressed()
    pos1, pos2 = pygame.mouse.get_pos()
        
        
    #If left mouse is being pressed, draw circles
    if m1 == 1:
        #If mouse is on colour wheel, don't draw
        if colourWheel.get_rect().collidepoint(pygame.mouse.get_pos()) and colourWheelOn == 1:
        #pos1 <= 220 and pos2 <= 220: works too
            brushSize += 0 #Do nothing
        else:
            draw.circle(screen, colour,(pos1, pos2), brushSize)
            print("Drawing in", colour, "with a brush size of", brushSize)
            
                
    #If middle mouse is being pressed, change colour to the clour under mouse
    #Eye-dropper tool
    if m2 == 1:
        colour = screen.get_at((pos1, pos2))
        time.wait(25)
        print("Colour was changed to", colour)
        
            
    #If right mouse is eing pressed, erase
    elif m3 == 1:
        draw.circle(screen, backGround, (pos1, pos2), brushSize)
        print("Erasing with brush size of", brushSize)
            

    #Colour wheel
    if colourWheelOn == 1:
        screen.blit(colourWheel, (0,0))
    #Toggles colour wheel
    if (pygame.key.get_pressed()[pygame.K_t]):
        colourWheelOn = 3 - colourWheelOn
        display.flip()
        time.wait(25)
        #If colour wheel is off 
        if colourWheelOn == 2:
            draw.rect(screen, backGround, (0, 0, 220, 220))
            time.wait(25)
            print("Colour wheel has been turned off")
        #If colour wheel is on
        elif colourWheelOn == 1:
            screen.blit(colourWheel, (0,0))
            time.wait(25)
            print("Colour wheel has been turned on")
    #Using colour wheel
    elif colourWheel.get_rect().collidepoint(pygame.mouse.get_pos()) and m1 == 1 and colourWheelOn == 1:
        colour = screen.get_at((pos1, pos2))
        time.wait(25)
        print("Colour was changed to", colour)
        

    #Changing brush sizes
    elif (pygame.key.get_pressed()[pygame.K_EQUALS]):
        brushSize += 1
        if brushSize > 30:
            brushSize -= 1
        print("Brush size was changed to", brushSize)
        time.wait(5)
    elif (pygame.key.get_pressed()[pygame.K_MINUS]):
        brushSize -= 1
        if brushSize < 2:
            brushSize += 1
        print("Brush size was changed to", brushSize)
        time.wait(25)


    #Screen fill the selected colour
    if (pygame.key.get_pressed()[pygame.K_f]):
        backGround = colour
        screen.fill(backGround)
        time.wait(25)
        print("Screen was filled in with", colour)


    #Clear screen
    if (pygame.key.get_pressed()[pygame.K_c]):
        backGround = white
        screen.fill(backGround)
        time.wait(25)
        print("Screen was cleared")


    #Save drawing
    if (pygame.key.get_pressed()[pygame.K_s]):
        name = input("Enter desired file name --> ")
        if name == "colourwheel" or name == "backGroundSave":
            print("Invalid save name")
        else:
            pygame.image.save(screen, name + ".png")
            print("Drawing was saved as", name + ".png")


    #Open saved drawing
    elif (pygame.key.get_pressed()[pygame.K_o]):
        drawingName = input("Enter the file name --> ")
        drawing = pygame.image.load(drawingName)
        screen.blit(drawing, (0,0))
        time.wait(25)
        print(drawingName + ".png was loaded")
        

    #Draw line - add dimmer lines (or dotted) while inputing end point
    elif (pygame.key.get_pressed()[pygame.K_l]):
        pygame.image.save(screen, "backGroundSave.png")
        print("Input start and end points of line")
        time.wait(25)

        #Toggle
        inputToggle = 1

        #drawLine loop
        while True:
            for evt in event.get():
                
                if evt.type == QUIT:
                    running = False
                    
            #Mouse input functions in drawLine loop
            m1, m2, m3 = pygame.mouse.get_pressed()
            pos1, pos2 = pygame.mouse.get_pos()
            
            #Getting start point of line
            if m1 == 1 and inputToggle == 1:
                time.wait(100)
                lineX1, lineY1 = pos1, pos2
                inputToggle = 2
                print("Start point of line :", lineX1, lineY1)

            #Getting end point of line
            elif inputToggle == 2:
                
                #Save Screen and reload
                screenSave = pygame.image.load("backGroundSave.png")
                screen.blit(screenSave, (0,0))

                lineX2, lineY2 = pos1, pos2
                draw.line(screen, colour, (lineX1, lineY1), (lineX2, lineY2), brushSize)
                display.flip()

                if m1 == 1:
                    time.wait(100)
                    print("End point of line :", lineX2, lineY2)
                    draw.line(screen, colour, (lineX1, lineY1), (lineX2, lineY2), brushSize)
                    print("Drawn line, exiting drawLine loop")
                    time.wait(100)
                    break

            #If x is clicked anytime, exit drawLine loop
            elif (pygame.key.get_pressed()[pygame.K_x]):
                print("Exiting drawLine loop")
                break

            
  


            
            
                    
                    
                    
            
            '''
         #Blend
        elif (pygame.key.get_pressed()[pygame.K_b]):
            time.wait(25)
            #pygame.mouse.set_cursor(pygame.cursors.broken_x)
            
            for i in range(0, 40):
                blend = screen.get_at((pos1 - 20 + i, pos2 - 20 + i))

                if i/3 == 0:
                    print("1")
                    c1 += blender[i]
                elif (i-1)/3 == 0:
                    print("2")
                    c2 += blender[i]
                elif (i-2)/3 == 0:
                    print("3")
                    c3 += blender[i]
                blender.append(blend)
            
            for i in range(0, 40, 3):
                c1 += blender[i]
            for i in range(1, 40, 3):
                c2 += blender[i]
            for i in range(2, 40, 3): 
                c3 += blender[i]
            
            print(c1, c2, c3)
            '''
    
                
        #MMode
        '''
        mouseMode = "up"
        pygame.mouse.set_visible(False)  #hide cursor

        screenBuffer = screen.copy()

        '''
         
            
    
    myClock.tick(60)
    display.flip()
    
print("Shutting down")
quit()

