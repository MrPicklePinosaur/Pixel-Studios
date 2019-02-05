#Dank Paint Program
#Created by Daniel Liu
#V0.4 - commands overhaul
import pygame
from pygame import *
pygame.init()
#screenWidth, screenHight = display.Info().current_w, display.Info().current_h
#screen = display.set_mode((screenWidth, screenHight),pygame.FULLSCREEN)
screen = display.set_mode((900,600))
display.set_caption("Communist Paint")

#Icon
icon = pygame.image.load("USSR.png")
display.set_icon(icon)


#Colours
white = (255,255,255)
black = (0,0,0)

colour = black
backGround = white

blender = 0, 0, 0
c1 = 0
c2 = 0
c3 = 0

ticks = 0
paintBlend = 0, 0, 0

'''
=========== All Commands ===========
leftmouse - draw with selected colour
middlemouse - eye drop
rightmouse - erase
p - toggle paint mode

f - fill screen with selected colour
c - clear screen
t - toggle colour wheel

s- save drawing
o - open a saved drawing (.png)

l - click twice for startpoint and endpoint to draw line


+ - increase brush/eraser size
- - decrease brush/eraser size

r - draw rect
a - draw circle
l - draw line

PLanned:
(Ctrl + Z) - Undo
import photos
'''

#Toggles
colourWheelOn = 1
inputToggle = 1
paintToggle = 2

#Size of brush (min of 1, max of 30)
brushSize = 3


#Load colour wheel
colourWheel = pygame.image.load("colourwheel.png")

#Draw background
screen.fill(backGround)


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

    #PAINT BRUSH - kinda broken
    #Paint toggle
    if (pygame.key.get_pressed()[pygame.K_p]):
        time.wait(50)
        ticks = 0
        paintToggle = 3 - paintToggle
        if paintToggle == 1:
            print("Paint mode on")
        elif paintToggle == 2:
            print("Paint mode off")
        
    if m1 == 1 and paintToggle == 1:
        paintBlend = screen.get_at((pos1,pos2))
        #If mouse is on colour wheel, don't draw
        if colourWheel.get_rect().collidepoint(pygame.mouse.get_pos()) and colourWheelOn == 1:
            brushSize += 0 #Do nothing
        else:
            colour = tuple(colour)
            #dont keep increaasing the colour if its close to being invalid
            if paintBlend[0] <= 0 or paintBlend[1] <= 0 or paintBlend[2] <= 0 or paintBlend[0] >= 255 or paintBlend[1] >= 255 or paintBlend[2] >= 255:
                brushSize += 0 #do nothing
            
                
            
            
            draw.circle(screen, (paintBlend[0] + ticks, paintBlend[1] + ticks, paintBlend[2] + ticks),(pos1, pos2), brushSize)
            print("Painting in", colour, "with a brush size of", brushSize, "and blending for", ticks)
            ticks += 1

                
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
        time.delay(100)
        #If colour wheel is off 
        if colourWheelOn == 2:
            draw.rect(screen, backGround, (0, 0, 220, 220))
            time.delay(25)
            print("Colour wheel has been turned off")
        #If colour wheel is on
        elif colourWheelOn == 1:
            screen.blit(colourWheel, (0,0))
            time.delay(25)
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
        time.wait(25)
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
        drawing = pygame.image.load(drawingName + ".png")
        screen.blit(drawing, (0,0))
        time.wait(25)
        print(drawingName + ".png was loaded")
        
    #Open image
    elif (pygame.key.get_pressed()[pygame.K_q]):
        drawingName = input("Enter the file name --> ")
        x = int(input("Enter x value of picture"))
        y = int(input("Enter x value of picture"))
        drawing = pygame.image.load(drawingName)
        screen.blit(drawing, (x,y))
        time.wait(25)
        print(drawingName + ".png was loaded")
        
    #Draw line
    elif (pygame.key.get_pressed()[pygame.K_l]):
        pygame.image.save(screen, "backGroundSave.png")
        print("Input start and end points of line")
        time.wait(25)

        #Toggle
        inputToggle = 1

        while True:
            for evt in event.get():
                
                if evt.type == QUIT:
                    running = False
                    

            #Mouse input functions in drawLine loop
            m1, m2, m3 = pygame.mouse.get_pressed()
            pos1, pos2 = pygame.mouse.get_pos()
            
            #Getting start point of line
            if m1 == 1 and inputToggle == 1:
                time.delay(100)
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
                    time.delay(100)
                    print("End point of line :", lineX2, lineY2)
                    print("Drawn line, exiting drawLine loop")
                    time.delay(100)
                    break

            #If x is clicked anytime, exit drawLine loop
            elif (pygame.key.get_pressed()[pygame.K_x]):
                print("Exiting drawLine loop")
                break

    #Draw rect
    elif (pygame.key.get_pressed()[pygame.K_r]):
        pygame.image.save(screen, "backGroundSave.png")
        print("Input start and end points of Rect")
        time.wait(25)

        #Toggle
        inputToggle = 1

        while True:
            for evt in event.get():
                
                if evt.type == QUIT:
                    running = False
                    

            #Mouse input functions in drawRect loop
            m1, m2, m3 = pygame.mouse.get_pressed()
            pos1, pos2 = pygame.mouse.get_pos()
            
            #Getting start point of line
            if m1 == 1 and inputToggle == 1:
                time.delay(100)
                rectX1, rectY1 = pos1, pos2
                inputToggle = 2
                print("Start point of rect :", rectX1, rectY1)

            #Getting end point of line
            elif inputToggle == 2:
                
                #Save Screen and reload
                screenSave = pygame.image.load("backGroundSave.png")
                screen.blit(screenSave, (0,0))

                rectX2, rectY2 = pos1, pos2
                draw.rect(screen, colour, (rectX1, rectY1, (rectX2 - rectX1), (rectY2 - rectY1)), brushSize)
                display.flip()

                if m1 == 1:
                    time.delay(100)
                    print("End point of rect :", rectX2, rectY2)
                    print("Drawn rect, exiting drawRect loop")
                    time.delay(100)
                    break

            #If x is clicked anytime, exit drawRect loop
            elif (pygame.key.get_pressed()[pygame.K_x]):
                print("Exiting drawRect loop")
                break

    #Draw circle
    elif (pygame.key.get_pressed()[pygame.K_a]):
        pygame.image.save(screen, "backGroundSave.png")
        print("Input center and radius points of circle")
        time.wait(25)

        #Toggle
        inputToggle = 1

        while True:
            for evt in event.get():
                
                if evt.type == QUIT:
                    running = False
                    

            #Mouse input functions in drawCirc loop
            m1, m2, m3 = pygame.mouse.get_pressed()
            pos1, pos2 = pygame.mouse.get_pos()
            
            #Getting start point of line
            if m1 == 1 and inputToggle == 1:
                time.delay(100)
                circX1, circY1 = pos1, pos2
                inputToggle = 2
                print("center of circle :", circX1, circY1)

            #Getting end point of line
            elif inputToggle == 2:
                
                #Save Screen and reload
                screenSave = pygame.image.load("backGroundSave.png")
                screen.blit(screenSave, (0,0))

                circX2, circY2 = pos1, pos2
                if (circX2 - circX1) == 0:
                    circX1 += 1
                draw.circle(screen, colour, (circX1, circY1), abs(int((((circY2 - circY1)**2 + (circX2 - circX1)**2))**0.5)))
                display.flip()

                if m1 == 1:
                    time.delay(100)
                    print("End point of rect :", circX2, circY2)
                    print("Drawn rect, exiting drawCirc loop")
                    time.delay(100)
                    break

            #If x is clicked anytime, exit drawCirc loop
            elif (pygame.key.get_pressed()[pygame.K_x]):
                print("Exiting drawCirc loop")
                break



            

            
            
                    
                    
                    
            
            
    #Blend
    elif (pygame.key.get_pressed()[pygame.K_b]):
        time.wait(50)
        
        blender = 0, 0, 0
    
        for i in range(0, 10):
            for n in range(0,10):
                blend = screen.get_at((pos1 - 5 + i, pos2 - 5 + n))
                print(blend)
                blender = (blender[0] + blend[0], blender[1] + blend[1], blender[2] + blend[2])
                

        
        blender = (blender[0]//100, blender[1]//100, blender[2]//100)
        print(blender)
        colour = blender
        
    

            
            
   
    
                
        #MMode
    '''
        mouseMode = "up"
        pygame.mouse.set_visible(False)  #hide cursor

        screenBuffer = screen.copy()

    '''
         
            
    
    
    display.flip()
    
print("Shutting down")
quit()

