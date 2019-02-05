#Dank Paint Program
#Created by Daniel Liu
#V0.5 - display changes and optimizations
import pygame
from pygame import *
import random
pygame.init()
mixer.init()
font.init()

from tkinter import *



screenInfo = pygame.display.Info()
print(screenInfo)

'''
=========== All Commands ===========
leftmouse - draw with selected colour
middlemouse - eye drop
rightmouse - erase
p - toggle paint mode

f - fill screen with selected colour
c - clear screen

s- save drawing
o - open a saved drawing (.png)


+ - increase brush/eraser size
- - decrease brush/eraser size

draw rect
draw circle
draw line

PLanned:
(Ctrl + Z) - Undo
blur tool
spray paint tool
add filters (sepia)
debugging mode (shows the events)
'''

#Screen size
screen = display.set_mode((1200,800))

#Overlay screens
dimScreen = pygame.Surface((1200,800), pygame.SRCALPHA)
overlay = pygame.Surface((500,650))

#Load assets
colourWheel = pygame.image.load("assets/images/colourwheel.png")
icon = pygame.image.load("assets/images/USSR.png")
Xicon = pygame.image.load("assets/images/Xicon.png")
#music_1 = pygame.mixer.music.load("assets/music/music_1.wav")

#initialize window
display.set_icon(icon)
display.set_caption("Pixel Studios")

#Colours =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
white = (255,255,255)
black = (0,0,0)

sliderC1 = (220,220,220)
#sliderC2 =
sliderX = 500
sliderY = 150

colour = black
backGround = white

#Colour slide pos
rpos = sliderX
gpos = sliderX
bpos = sliderX

paletteList = [black]
#Tool Commands =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
toolType = "pencil"
#saving the cordinates of pencil
linePosX, linePosY = 0,0
#Size of brush (min of 1, max of 30)
brushSize = 3
#Blender
blender = 0, 0, 0
c1 = 0
c2 = 0
c3 = 0
ticks = 0
paintBlend = 0, 0, 0
r = 0
g = 0
b = 0

#Undo/redo
screenList = []
flag = 0

#Toggles =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
colourWheelOn = 1
inputToggle = 1
paintToggle = 2
        
#Functions =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

#Reload canvas
def reload():
    screenSave = pygame.image.load("assets/images/backGroundSave.png")
    screen.blit(screenSave, (0,0))

#Delays
def delay_short():
    time.wait(25)

def delay_long():
    time.wait(50)

def delay_longest():
    time.wait(100)

#Tools
def pencil():
    draw.circle(screen, colour,(pos1, pos2), brushSize-2)
    draw.line(screen, colour, (pos1, pos2), (linePosX, linePosY), brushSize*2)

def eraser():
    draw.circle(screen, white,(pos1, pos2), brushSize-2)
    draw.line(screen, white, (pos1, pos2), (linePosX, linePosY), brushSize*2)

def spray():
    rnd1, rnd2 = random.randint(-(brushSize+5), brushSize+5), random.randint(-(brushSize+5), brushSize+5)
    #radius = (((pos1+rnd1) - pos1)**2 + ((pos2+rnd2) - pos2)**2)**0.5
    draw.circle(screen, colour, ((pos1 + rnd1), (pos2 + rnd2)),2)
    #print(radius)



def paintbrush():
    #Paint toggle
    if (pygame.key.get_pressed()[pygame.K_p]):
        delay_long()
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

def drawLine():
    #Save screen
    pygame.image.save(screen, "assets/images/backGroundSave.png")
    print("Input start and end points of line")
    delay_short()

    #Toggle
    inputToggle = 1

    while True:
        for evt in event.get():
                
            if evt.type == QUIT:
                break
                    
        #Mouse input functions in drawLine loop
        m1, m2, m3 = pygame.mouse.get_pressed()
        pos1, pos2 = pygame.mouse.get_pos()
            
        #Getting start point of line
        if m1 == 1 and inputToggle == 1:
            delay_longest()
            lineX1, lineY1 = pos1, pos2
            inputToggle = 2
            print("Start point of line :", lineX1, lineY1)

        #Getting end point of line
        elif inputToggle == 2:
                
            #Save Screen and reload
            reload()

            lineX2, lineY2 = pos1, pos2
            draw.line(screen, colour, (lineX1, lineY1), (lineX2, lineY2), brushSize)
            display.flip()

            if m1 == 1:
                print("End point of line :", lineX2, lineY2)
                print("Drawn line, exiting drawLine loop")
                delay_long()
                break
def drawRect():
    #Save screen
    pygame.image.save(screen, "assets/images/backGroundSave.png")
    print("Input start and end points of Rect")
    delay_short()

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
            delay_longest()
            rectX1, rectY1 = pos1, pos2
            inputToggle = 2
            print("Start point of rect :", rectX1, rectY1)

        #Getting end point of line
        elif inputToggle == 2:
                
            #Save Screen and reload
            reload()

            rectX2, rectY2 = pos1, pos2
            draw.rect(screen, colour, (rectX1, rectY1, (rectX2 - rectX1), (rectY2 - rectY1)), brushSize)
            display.flip()

            if m1 == 1:
                print("End point of rect :", rectX2, rectY2)
                print("Drawn rect, exiting drawRect loop")
                delay_long()
                break

def drawCircle():
    #Save screen
    pygame.image.save(screen, "assets/images/backGroundSave.png")
    print("Input center and radius points of circle")
    delay_short()

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
            delay_longest()
            circX1, circY1 = pos1, pos2
            inputToggle = 2
            print("center of circle :", circX1, circY1)

        #Getting end point of line
        elif inputToggle == 2:
                
            #Save Screen and reload
            reload()

            circX2, circY2 = pos1, pos2
            if (circX2 - circX1) == 0:
                circX1 += 1
            draw.circle(screen, colour, (circX1, circY1), abs(int((((circY2 - circY1)**2 + (circX2 - circX1)**2))**0.5)))
            display.flip()

            if m1 == 1:
                print("End point of circle :", circX2, circY2)
                print("Drawn circle, exiting drawCirc loop")
                delay_long()
                break

'''
def fill():
    baseColour = screen.get_at(pos1,pos2)
    for i in range(
'''
 
def refreshSlider(c): #Refresh sliders
    if c == r:
        for i in range(0,256):
            rSlider = draw.rect(screen, (i,0,0), (sliderX+i ,sliderY, 1, 20))
    elif c == g:
        for i in range(0,256):
            gSlider = draw.rect(screen, (0,i,0), (sliderX+i ,sliderY+30, 1, 20))
    elif c == b:
        for i in range(0,256):
            bSlider = draw.rect(screen, (0,0,i), (sliderX+i ,sliderY+60, 1, 20))


def drawSlide(c): #Draw sliders
    if c == r:
        draw.rect(screen, sliderC1, (rpos, sliderY, 10, 20))
    elif c == g:
        draw.rect(screen, sliderC1, (gpos, sliderY+30, 10, 20))
    elif c == b:
        draw.rect(screen, sliderC1, (bpos, sliderY+60, 10, 20))

def initSliders():
    for i in range(0,256): #Draw colour sliders
        draw.rect(screen, (i,0,0), (sliderX+i ,sliderY, 1, 20))
        draw.rect(screen, (0,i,0), (sliderX+i ,sliderY+30, 1, 20))
        draw.rect(screen, (0,0,i), (sliderX+i ,sliderY+60, 1, 20))
    
    draw.rect(screen, sliderC1, (rpos, sliderY, 10, 20))
    draw.rect(screen, sliderC1, (gpos, sliderY+30, 10, 20))
    draw.rect(screen, sliderC1, (bpos, sliderY+60, 10, 20))

#Defining collide points =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
canvasCollide = Rect(200,50,850,650)
rSliderCollide = Rect(sliderX,sliderY,255,20)
gSliderCollide = Rect(sliderX,sliderY+30,255,20)
bSliderCollide = Rect(sliderX,sliderY+60,255,20)
overlayCollide = Rect(350, 100, 500 ,650)
XiconCollide = Rect(810,110,32,32)
addColourCollide = Rect(715,240,40,20)
#Draw Screen =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
screen.fill((200,200,200)) #Draw background

draw.rect(screen, white, (canvasCollide)) #Draw canvas

colourPalette = draw.rect(screen, black, (100,700,50,50))

'''
pencilButton
paintButton
eraserButton
lineButton
rectButton
eyedropperButton
'''


#mixer.music.play(1, 0)


#Running loops =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#Main Loop
running = True
while running:
    for evt in event.get():
            
        if evt.type == QUIT:
            running = False
    
        
    #FInds out which mouse button is being pressed and where the mouse is
    m1, m2, m3 = pygame.mouse.get_pressed()
    pos1, pos2 = pygame.mouse.get_pos()

    #Changing Tools


    
    #If left mouse is being pressed on canvas, draw
    if canvasCollide.collidepoint(pygame.mouse.get_pos()):
        screen.set_clip(canvasCollide)
        
        if m1 == 1:
            #Tools
            if toolType == "pencil":
                pencil()
                print("Drawing with pencil in", colour, "with a brush size of", brushSize)
            elif toolType == "paintbrush": #kinda broken
                paint()
                print("Drawing with paintbrush in", colour, "with a brush size of", brushSize)
            elif toolType == "eraser":
                eraser()
                print("Erasing with brush size of", brushSize)
            elif toolType == "eyedropper":
                eyedropper()
                print("colour was changed to", colour)
            elif toolType == "spray":
                spray()
                print("spray painting with a radius of", brushSize + 5)
            
            
        #If middle mouse is being pressed, change colour to the clour under mouse
        #Eye-dropper tool
        if m2 == 1:
            colour = screen.get_at((pos1, pos2))
            delay_short()
            print("Colour was changed to", colour)
            
            
        #If right mouse is being pressed, erase
        if m3 == 1:
            eraser()
            print("Erasing with brush size of", brushSize)
            
        #Other tools
        elif toolType == "drawLine":
            drawLine()
        elif toolType == "drawRect":
            drawRect()
        elif toolType == "drawCircle":
            drawCircle()
        '''
        elif toolType == "undo":
            undo()
        elif toolType == "redo":
            redo()
        '''
        #Update line pos
        linePosX, linePosY = pos1, pos2

    
    #Colour Palette
    if colourPalette.collidepoint(pygame.mouse.get_pos()) and m1 == 1:

        #Save screen
        pygame.image.save(screen, "assets/images/backGroundSave.png")
        screenSave = pygame.image.load("assets/images/backGroundSave.png")
        
        #Dim the screen and draw overlay menu
        dimScreen.fill((0,0,0,128))
        overlay.fill((40,40,40))
        screen.blit(dimScreen, (0,0))
        screen.blit(overlay, (350, 100))
        screen.blit(Xicon, (810,110))
        draw.rect(screen, (255,255,0), addColourCollide)
        #screen.set_clip(overlayCollide)

        initSliders()
        
        #Colour palette loop
        while True:
           
            for evt in event.get():
                
                if evt.type == QUIT:
                    break

            #Mouse input functions in loop
            m1, m2, m3 = pygame.mouse.get_pressed()
            pos1, pos2 = pygame.mouse.get_pos()
            
            #Colour slider
            #Refresh colour box
            draw.rect(screen, colour, (sliderX-90,sliderY,80,80))
            draw.rect(screen, white , (sliderX-90,sliderY, 80, 80), 5)
    
    
            #Using colour sliders
            if rSliderCollide.collidepoint(pygame.mouse.get_pos()) and m1 == 1:
                r = pos1 - sliderX
                screen.set_clip(rSliderCollide)
                #Update Red slider
                rpos = pos1
                refreshSlider(r)
                drawSlide(r)
            elif gSliderCollide.collidepoint(pygame.mouse.get_pos()) and m1 == 1:
                g = pos1 - sliderX
                screen.set_clip(gSliderCollide)
                #Update Green slider
                gpos = pos1
                refreshSlider(g)
                drawSlide(g)
            elif bSliderCollide.collidepoint(pygame.mouse.get_pos()) and m1 == 1:
                b = pos1 - sliderX
                screen.set_clip(bSliderCollide)
                #Update Blue slider
                bpos = pos1
                refreshSlider(b)
                drawSlide(b)
            #Set the selected colour
            colour = (r,g,b)
            #add the selected colour to the palette if there isn't a duplicate colour and ckicked
            if addColourCollide.collidepoint(pygame.mouse.get_pos()) and m1 == 1:
                paletteList.append(colour)
                print(paletteList)

            
            #Reset parameters
            screen.set_clip(None)
            
            #if the close icon is clicked, close window
            if XiconCollide.collidepoint(pygame.mouse.get_pos()) and m1 == 1:
                screen.blit(screenSave, (0,0))
                delay_longest()
                break
                

            display.flip()
    
        
        

    #Changing brush sizes
    if (pygame.key.get_pressed()[pygame.K_EQUALS]):
        brushSize += 1
        if brushSize > 20:
            brushSize -= 1
        print("Brush size was changed to", brushSize)
        delay_short()
    elif (pygame.key.get_pressed()[pygame.K_MINUS]):
        brushSize -= 1
        if brushSize < 2:
            brushSize += 1
        print("Brush size was changed to", brushSize)
        delay_short()


    #Screen fill the selected colour
    if (pygame.key.get_pressed()[pygame.K_f]):
        draw.rect(screen, colour, canvasCollide)
        delay_short()
        print("Screen was filled in with", colour)

    #Clear screen
    if (pygame.key.get_pressed()[pygame.K_c]):
        draw.rect(screen, white, canvasCollide)
        delay_short()
        print("Screen was cleared")


    #Save drawing
    if (pygame.key.get_pressed()[pygame.K_s]):
        try:
            fname = filedialog.asksaveasfilename(defaultextension=".png")
            #pygame.image.save(screen.subsurface(canvasCollide), "assets/screen/", name)
            pygame.image.save(screen.subsurface(canvasCollide), "assets/screen/" + fname)
            print("Drawing was saved as", "assets/screen/" + fname)
        except:
            print("Unable to save", fname)

    #Open saved drawing
    elif (pygame.key.get_pressed()[pygame.K_o]):
        drawingName = input("Enter the file name --> ")
        #check to see if file exists
        try:
            #fname = filedialog.asksaveasfilename(defaultextension=".png")
            drawing = pygame.image.load("assets/screen/" + drawingName + ".png")
            screen.blit(drawing, (0,0))
            delay_short()
            print(drawingName + ".png was loaded")
        #If program crashes, display message 
        except:
            print("Unable to open assets/screen/" + drawingName + ".png")
        
    




                    
            
            
    #Blend
    elif (pygame.key.get_pressed()[pygame.K_b]):
        delay_long()
        
        blender = 0, 0, 0
    
        for i in range(0, 10):
            for n in range(0,10):
                blend = screen.get_at((pos1 - 5 + i, pos2 - 5 + n))
                print(blend)
                blender = (blender[0] + blend[0], blender[1] + blend[1], blender[2] + blend[2])
                

        
        blender = (blender[0]//100, blender[1]//100, blender[2]//100)
        print(blender)
        colour = blender
        
    
    '''
    arialFont = font.SysFont("Arial",40)
    comicFont = font.SysFont("Comic Sans MS",30)

    myText1 = arialFont.render("Blobfefe", True, (0,255,0))
    #Turns the text into a picture
    
    '''         
        #MMode
    '''
        mouseMode = "up"
        pygame.mouse.set_visible(False)  #hide cursor

        screenBuffer = screen.copy()

    '''
         
            
    #Reset parameters
    screen.set_clip(None)

    
    display.flip()
    
print("Shutting down")
quit()

