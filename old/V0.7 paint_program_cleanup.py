#Dank Paint Program
#Created by Daniel Liu
#V0.7 - Colour selection improvements
import pygame
from pygame import *
from tkinter import *
import random
pygame.init()
mixer.init()
#font.init()

print('''
You are running Pixel Studios Paint Program V0.7
           Created by Daniel Liu''')

print(pygame.display.Info())

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
#canvasScreen = pygame.Surface((850,650))
dimScreen = pygame.Surface((1200,800), pygame.SRCALPHA)
overlay = pygame.Surface((500,650))
airBrushMask = pygame.Surface((32,32), pygame.SRCALPHA)

#Load assets =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#images
#loading images
backGround1 = pygame.image.load("assets/images/backGround1.png")
icon = pygame.image.load("assets/images/pixelStudios.png")
Xicon = pygame.image.load("assets/images/Xicon.png")
XiconHighlight = pygame.image.load("assets/images/XiconHighlight.png")

pencilToolIcon = pygame.image.load("assets/images/pencilToolIcon.png")
eraserToolIcon = pygame.image.load("assets/images/eraserToolIcon.png")
drawLineToolIcon = pygame.image.load("assets/images/drawLineToolIcon.png")
drawRectToolIcon = pygame.image.load("assets/images/drawRectToolIcon.png")
drawEllipseToolIcon = pygame.image.load("assets/images/drawEllipseToolIcon.png")
drawCirlceToolIcon = pygame.image.load("assets/images/drawCircleToolIcon.png")

#songs
songList = ["Music_1 - SuperMario.ogg", "Music_2 - SuperMarioWorld.ogg", "Music_3 - Kirby.ogg", "Music_4 - StreetFighter.ogg", "Music_5 - PokemonBattle.ogg", "Music_6 - Sonic.ogg", "Music_7 - Megaman.ogg"]

#Load fonts
#posText = font.SysFont("arial", 12)

#initialize window info and set random program name
display.set_icon(icon)

captionList = ["Can I please get a waffle", "Now in 2D!", "Paint Program", "With more than 10,000 lines of code!", "The FUTURE of painting!"] #list of potential quotes
rnd = random.randint(0,len(captionList)-1)
display.set_caption("Pixel Studios - " + captionList[rnd])

#Colours =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
white = (255,255,255)
black = (0,0,0)

sliderC1 = (220,220,220)
sliderC2 = (255,255,0)
sliderX = 500
sliderY = 150

               
colour = black
backGround = white

#Colour slide pos
rpos = sliderX
gpos = sliderX
bpos = sliderX



#overlay window colour
overlayC1 = (40,40,40)

#Tool Box Highlight colours
toolBoxC1 = (170,170,170)
toolBoxC2 = (247,247,173)
toolBoxC3 = (225,225,0)

#Colour box highlight colours
colourBoxC1 = overlayC1
colourBoxC2 = (225,225,0)
#Tool Commands =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
toolType = "pencil" #default tool type

#saving the cordinates of pencil
linePosX, linePosY = 0,0

#Size of brush (min of 1, max of 30)
brushSize = 1

#Blend tool
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
undoList = []
redoList = []


#def undo():
    

#Toggles =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
colourWheelOn = 1
inputToggle = 1
paintToggle = 2
        
#Functions =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
click = False
    
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
    draw.line(screen, colour, (pos1, pos2), (linePosX, linePosY), brushSize*2)
    if ((linePosX - pos1)**2 + (linePosY - pos2)**2)**0.5 != 0 and ((linePosX - pos1)**2 + (linePosY - pos2)**2)**0.5 < brushSize: #make pencil look bumpy if drawing slowly
        draw.line(screen, colour, (pos1, pos2), (linePosX, linePosY), brushSize*2)
        draw.circle(screen, colour,(pos1, pos2), brushSize)
    
def pen():
    if m1 == 0:
        ticks = 0
    else:
        if ((linePosX - pos1)**2 + (linePosY - pos2)**2)**0.5 < 5:
            
            draw.line(screen, colour, (pos1, pos2), (linePosX, linePosY), brushSize*2+2)
            
        elif ((linePosX - pos1)**2 + (linePosY - pos2)**2)**0.5 > 5:
               draw.line(screen, colour, (pos1, pos2), (linePosX, linePosY), brushSize*2-2)

def eraser():
    draw.line(screen, white, (pos1, pos2), (linePosX, linePosY), brushSize*2)
    if ((linePosX - pos1)**2 + (linePosY - pos2)**2)**0.5 != 0 and ((linePosX - pos1)**2 + (linePosY - pos2)**2)**0.5 < brushSize: #make pencil look bumpy if drawing slowly
        draw.line(screen, white, (pos1, pos2), (linePosX, linePosY), brushSize*2)
        draw.circle(screen, white,(pos1, pos2), brushSize)

def spray():
    rnd1, rnd2 = random.randint(-(brushSize+5), brushSize+5), random.randint(-(brushSize+5), brushSize+5)
    #radius = (((pos1+rnd1) - pos1)**2 + ((pos2+rnd2) - pos2)**2)**0.5
    #draw.circle(screen, colour, ((pos1 + rnd1), (pos2 + rnd2)),2)
    draw.rect(screen, colour, ((pos1 + rnd1), (pos2 + rnd2), 2, 2))


def paintbrush(): #broken
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
            Pass #Do nothing
        else:
            colour = tuple(colour)
            #dont keep increaasing the colour if its close to being invalid
            if paintBlend[0] <= 0 or paintBlend[1] <= 0 or paintBlend[2] <= 0 or paintBlend[0] >= 255 or paintBlend[1] >= 255 or paintBlend[2] >= 255:
                Pass #do nothing
                
            draw.circle(screen, (paintBlend[0] + ticks, paintBlend[1] + ticks, paintBlend[2] + ticks),(pos1, pos2), brushSize)
            print("Painting in", colour, "with a brush size of", brushSize, "and blending for", ticks)
            ticks += 1

def eyedropper():
        colour = screen.get_at((pos1, pos2))
        delay_short()
        print("Colour was changed to", colour)
        
def drawShape(n): #draw basic shapes (start point and end point)

    #Save screen
    pygame.image.save(screen, "assets/images/backGroundSave.png")

    #Toggle
    inputToggle = 1

    #First loop, get start point of shape
    print("Input start point of", n)
    while True:
        
        click = False
        for evt in event.get():
            
            #Mouse input functions in loop
            m1, m2, m3 = pygame.mouse.get_pressed()
            pos1, pos2 = pygame.mouse.get_pos()

            if evt.type == MOUSEBUTTONDOWN and m1 == 1:
                click = True
            
            
        #Getting start point of line
        if click:
            shapeX1, shapeY1 = pos1, pos2
            print("Start point of", n, ":", shapeX1, shapeY1)
            break
            
        
    #Second loop, get end point of shape
    print("Input end point of", n)
    while True:
        
        click = False
        for evt in event.get():
            
            #Mouse input functions in loop
            m1, m2, m3 = pygame.mouse.get_pressed()
            pos1, pos2 = pygame.mouse.get_pos()
            
            if evt.type == MOUSEBUTTONDOWN and m1 == 1:
                click = True

            #Break loop if the mouse is no longer being held down
            if evt.type == MOUSEBUTTONUP:
                print("End point of", n, ":", shapeX2, shapeY2)
                print("Drawn", n, "exiting draw" + n, "loop")
                inputToggle = 2

        #Break loop
        if inputToggle == 2:
            break
        
        #Save Screen and reload
        reload()

        shapeX2, shapeY2 = pos1, pos2

        #Determines which shape to draw (depending on selected tool)
        if n == "line":
            draw.line(screen, colour, (shapeX1, shapeY1), (shapeX2, shapeY2), brushSize)
        elif n == "rect":
            draw.rect(screen, colour, (shapeX1, shapeY1, (shapeX2 - shapeX1), (shapeY2 - shapeY1)), brushSize)
        elif n == "circle":
            if (shapeX2 - shapeX1) == 0:
                shapeX1 += 1
            draw.circle(screen, colour, (shapeX1, shapeY1), abs(int((((shapeY2 - shapeY1)**2 + (shapeX2 - shapeX1)**2))**0.5)))
        elif n == "ellipse":
            parameters = Rect(shapeX1, shapeY1, (shapeX2 - shapeX1), (shapeY2 - shapeY1))
            parameters.normalize()
            draw.ellipse(screen, colour, parameters)
                
        display.flip()


        

'''
def fill(): #check all surrounding pixels, if they are the same, convert colour
    baseColour = screen.get_at(pos1,pos2)
    for i in range(
'''
 
def refreshSlider(): #Refresh colour sliders
        for i in range(0,256):
            rSlider = draw.rect(screen, (i,0,0), (sliderX+i ,sliderY, 1, 20))
            gSlider = draw.rect(screen, (0,i,0), (sliderX+i ,sliderY+30, 1, 20))
            bSlider = draw.rect(screen, (0,0,i), (sliderX+i ,sliderY+60, 1, 20))


def drawSlide(): #Draw sliders
        draw.rect(screen, sliderC1, (rpos, sliderY, 10, 20))
        draw.rect(screen, sliderC1, (gpos, sliderY+30, 10, 20))
        draw.rect(screen, sliderC1, (bpos, sliderY+60, 10, 20))

def initSliders():
    for i in range(0,256): #Draw colour sliders
        draw.rect(screen, (i,0,0), (sliderX+i ,sliderY, 1, 20))
        draw.rect(screen, (0,i,0), (sliderX+i ,sliderY+30, 1, 20))
        draw.rect(screen, (0,0,i), (sliderX+i ,sliderY+60, 1, 20))
    
    draw.rect(screen, sliderC1, (rpos, sliderY, 10, 20))
    draw.rect(screen, sliderC1, (gpos, sliderY+30, 10, 20))
    draw.rect(screen, sliderC1, (bpos, sliderY+60, 10, 20))

def hoverTimer(): #waits, and then sends a siginal (used for tooltips)
    ticks += 1
    if ticks > 300:
        print("yee")

def toolBoxHighlight():
    #draw hightlight for selected tool
    i = toolList.index(toolType)
    if i < 7:
        draw.rect(screen, toolBoxC3, (toolBoxX-5,toolBoxY-5+i*toolBoxGap,74,74),5)
    else: #Draw new column of highlights
        draw.rect(screen, toolBoxC3, (toolBoxX-5+toolBoxGap,toolBoxY-5+(i-7)*toolBoxGap,74,74),5)
        
#Defining collide points =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
canvasCollide = Rect(194,50,831,650)
rSliderCollide = Rect(sliderX,sliderY,255,20)
gSliderCollide = Rect(sliderX,sliderY+30,255,20)
bSliderCollide = Rect(sliderX,sliderY+60,255,20)
overlayCollide = Rect(350, 100, 500 ,650)
XiconCollide = Rect(810,110,32,32)
addColourCollide = Rect(665,240,40,20)
delColourCollide = Rect(715,240,40,20)

toolBoxX = 20
toolBoxY = 55
toolBoxGap = 90

#Define tool collide list, and it's corresponding tool
toolList = ["pencil", "eraser", "drawLine", "drawRect", "drawEllipse", "drawCircle", "eyedropper", "spray"]

toolCollideList = []
for i in range(len(toolList)):
    if i < 7:
        toolCollideList.append(Rect(toolBoxX, toolBoxY+i*toolBoxGap,64,64))
    else: #add new column of tools
        toolCollideList.append(Rect(toolBoxX+toolBoxGap, toolBoxY+(i-7)*toolBoxGap,64,64))
        

        
#ToolTip for each tool
toolTickList = []
for i in range(len(toolList)):
    toolTickList.append(0)


#Colours in palette and their location
paletteColourList = [(0,0,0)]
palettePosList = [Rect(409,290,32,32)]
palettePosListMini = []
paletteHighlightList = [Rect(408, 289, 34, 34)]
selectedColour = paletteColourList[0]
selectedColourPos = paletteHighlightList[0]
#Draw Screen =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
screen.fill((200,200,200)) #Draw background
screen.blit(backGround1, (0,0))

draw.rect(screen, white, (canvasCollide))

#Draw colour palette
colourPalette = draw.rect(screen, black, (100,700,50,50)) #button to open colour picker
draw.rect(screen, (70,70,70), (1037, 400, 150, 300)) #redraw colour picker box

#draw tool selection boxes
#Drawing background of box
for i in range(len(toolCollideList)):
    draw.rect(screen, toolBoxC1, toolCollideList[i])

#draw tool icons
screen.blit(pencilToolIcon, (toolBoxX,toolBoxY))
screen.blit(eraserToolIcon, (toolBoxX,toolBoxY+toolBoxGap))
screen.blit(drawLineToolIcon, (toolBoxX,toolBoxY+toolBoxGap*2))
screen.blit(drawRectToolIcon, (toolBoxX,toolBoxY+toolBoxGap*3))
screen.blit(drawEllipseToolIcon, (toolBoxX,toolBoxY+toolBoxGap*4))

#Draw highlights
for i in range(0,len(toolCollideList)):
    if i < 7:
        draw.rect(screen, toolBoxC1, (toolBoxX-5,toolBoxY-5+i*toolBoxGap,74,74),5)
    else: #Draw new column of highlights
        draw.rect(screen, toolBoxC1, (toolBoxX-5+toolBoxGap,toolBoxY-5+(i-7)*toolBoxGap,74,74),5)
        
#draw hightlight for selected tool
i = toolList.index(toolType)
draw.rect(screen, toolBoxC3, (toolBoxX-5,toolBoxY-5+i*toolBoxGap,74,74),5)


#Music
volume = 0.75

#Running loops =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#Main Loop
running = True
while running:

    click = False
    for evt in event.get():

        #FInds out which mouse button is being pressed and where the mouse is
        m1, m2, m3 = pygame.mouse.get_pressed()
        pos1, pos2 = pygame.mouse.get_pos()
    
        if evt.type == QUIT:
            running = False

        #Determines if mouse is being clicked
        if evt.type == MOUSEBUTTONDOWN and m1 == 1:
            click = True
        
    #Checks if there is music playing
    if mixer.music.get_busy() == False:
        #play a random song if there is no music
        rndSong = random.randint(0,len(songList)-1)
        mixer.music.load("assets/music/" + songList[rndSong])
        mixer.music.set_volume(volume) #set volume
        mixer.music.play()
        print("Now playing", songList[rndSong])



    #Switching tools and displaying tool feedback
    #check to see if any tool buttons are being hovered over and display tool tips
    for i in range(len(toolCollideList)):
        #Reset highlights
        if i < 7:
            draw.rect(screen, toolBoxC1, (toolBoxX-5,toolBoxY-5+i*toolBoxGap,74,74),5)
        else: #Draw new column of highlights
            draw.rect(screen, toolBoxC1, (toolBoxX-5+toolBoxGap,toolBoxY-5+(i-7)*toolBoxGap,74,74),5)
            
        if toolCollideList[i].collidepoint(pygame.mouse.get_pos()):
            #highlight box if it is being hovered over
            if i < 7:
                draw.rect(screen, toolBoxC2, (toolBoxX-5,toolBoxY-5+i*toolBoxGap,74,74),5)
            else: #Draw new column of highlights
                draw.rect(screen, toolBoxC2, (toolBoxX-5+toolBoxGap,toolBoxY-5+(i-7)*toolBoxGap,74,74),5)

            
            #finds how long the icon was hovered on for, for each of the icons
            toolTickList[i] += 1
         
            #Switch tools if clicked
            if click:
                toolType = toolList[i]

        #if the icon is not being hovered over, reset ticks
        else:
            toolTickList[i] = 0

        #Tool tips for each tool
        if toolTickList[i] > 350:
            #Save screen
            pygame.image.save(screen, "assets/images/backGroundSave.png")
            
            while True:
                for evt in event.get():

                    #FInds out which mouse button is being pressed and where the mouse is
                    m1, m2, m3 = pygame.mouse.get_pressed()
                    pos1, pos2 = pygame.mouse.get_pos()

                    #Determines if mouse is being clicked
                    if evt.type == MOUSEBUTTONDOWN and m1 == 1:
                        click = True

                #Draw tooltip if mouse is still on tool box
                if toolCollideList[i].collidepoint(pygame.mouse.get_pos()):
                    reload()
                    #Refresh tool box highlight
                    toolBoxHighlight()
                    draw.rect(screen,black, (pos1, pos2, 100, 40))
                    #If the tool is clicked, break loop and reset timer
                    if click:
                        toolType = toolList[i]
                        reload()
                        toolBoxHighlight()
                        toolTickList[i] = 0
                        break
                    
                #if mouse isn't on tool box, break loop
                else:
                    reload()
                    toolTickList[i] = 0
                    break
                
                display.flip()
                
    #print(toolTickList)

    #Refresh tool box highlight
    toolBoxHighlight()


    #Using tools
    #If mouse is on canvas, enable editing mode
    if canvasCollide.collidepoint(pygame.mouse.get_pos()):
        screen.set_clip(canvasCollide)

        #If mouse 1 is being pressed, use primary tools
        if m1 == 1:
            #Tools
            if toolType == "pencil":
                pencil()
            elif toolType == "paintbrush":
                paint()
            elif toolType == "eraser":
                eraser()
            elif toolType == "eyedropper":
                colour = screen.get_at((pos1, pos2))
                delay_short()
                print("Colour was changed to", colour)
            elif toolType == "spray":
                spray()
        
        #If middle mouse is being pressed, use eye dropper tool
        #Eye-dropper tool
        elif m2 == 1:
            colour = screen.get_at((pos1, pos2))
            delay_short()
            print("Colour was changed to", colour)
            
        #If right mouse is being pressed, use eraser tool
        elif m3 == 1:
            eraser()


        #Other tools
        else:
            if toolType == "drawLine":
                drawShape("line")
                toolType = "pencil" #Reset tool type
            elif toolType == "drawRect":
                drawShape("rect")
                toolType = "pencil" #Reset tool type
            elif toolType == "drawCircle":
                drawShape("circle")
                toolType = "pencil" #Reset tool type
            elif toolType == "drawEllipse":
                drawShape("ellipse")
                toolType = "pencil" #Reset tool type
            
        
        '''
        elif toolType == "undo":
            undo()
        elif toolType == "redo":
            redo()
        '''




    #Colour Palette
    if colourPalette.collidepoint(pygame.mouse.get_pos()) and click: #open colour picker window if palette butoon is clicked

        #Save screen
        pygame.image.save(screen, "assets/images/backGroundSave.png")
        screenSave = pygame.image.load("assets/images/backGroundSave.png")
        
        #Dim the screen and draw overlay menu
        dimScreen.fill((0,0,0,128))
        overlay.fill((overlayC1))
        screen.blit(dimScreen, (0,0))
        screen.blit(overlay, (350, 100))
        screen.blit(Xicon, (810,110))
        
        draw.rect(screen, (255,255,0), addColourCollide) #Button to add colour
        draw.rect(screen, (255,255,0), delColourCollide) #Button to delete a colour

        #Refresh palette list
        paletteX = 0
        paletteY = 0

        #draw the colours
        for i in range(len(paletteColourList)):
            paletteX += 1
            if paletteX > 8:
                paletteX = 1
                paletteY += 1
            draw.rect(screen, paletteColourList[i], (359 + paletteX*50, 290 + paletteY*50, 32, 32))
                    
        initSliders()
        #Colour palette loop
        while True:
            
            click = False
            for evt in event.get():
                
                #Mouse input functions in loop
                m1, m2, m3 = pygame.mouse.get_pressed()
                pos1, pos2 = pygame.mouse.get_pos()
                
                if evt.type == MOUSEBUTTONDOWN and m1 == 1:
                    click = True

                    
            #Refresh X icon
            draw.rect(screen, overlayC1, XiconCollide)
            screen.blit(Xicon, (810,110))


            #Colour slider
            #Update colour box to match current colour
            draw.rect(screen, (r,g,b), (sliderX-90,sliderY,80,80))
            draw.rect(screen, white , (sliderX-90,sliderY, 80, 80), 5)

            #add the selected colour to the palette if add colour button is clicked
            if addColourCollide.collidepoint(pygame.mouse.get_pos()) and click:
                #add a new colour
                paletteColourList.append(selectedColour)
                #add colour pos to palette list
                paletteX += 1
                if paletteX > 8:
                    paletteX = 1
                    paletteY += 1
                #add pos of colour square to list
                palettePosList.append(Rect(359 + paletteX*50, 290 + paletteY*50, 32, 32))
                #add highlight pos of colour square to list
                paletteHighlightList.append(Rect(358 + paletteX*50, 289 + paletteY*50, 34, 34))

                
            #Check to see if any of the colour are being hovered over
            for i in range(len(paletteHighlightList)):
                #Reset colour box highlights
                draw.rect(screen, colourBoxC1, paletteHighlightList[i])
                if palettePosList[i].collidepoint(pygame.mouse.get_pos()):
                    draw.rect(screen, paletteColourList[i], paletteHighlightList[i])
                    #Select the colour box
                    if click:
                        selectedColourPos = paletteHighlightList[i]
                        selectedColour = paletteColourList[i]
                        #Update r,g,b values to the selected colour
                        r,g,b = selectedColour
                        rpos, gpos, bpos = r + sliderX, g + sliderX, b + sliderX
                        refreshSlider()
                        drawSlide()                    


            #Draw highlight for selected colour box
            i = paletteHighlightList.index(selectedColourPos)
            draw.rect(screen, colourBoxC2, paletteHighlightList[i])
            
            #Refresh all colour boxes
            for i in range(len(paletteColourList)):
                draw.rect(screen, paletteColourList[i], palettePosList[i])

            
            #Using colour sliders
            if rSliderCollide.collidepoint(pygame.mouse.get_pos()) and m1 == 1:
                r = pos1 - sliderX
                screen.set_clip(rSliderCollide)
                #Update Red slider
                rpos = pos1
                refreshSlider()
                drawSlide()
            elif gSliderCollide.collidepoint(pygame.mouse.get_pos()) and m1 == 1:
                g = pos1 - sliderX
                screen.set_clip(gSliderCollide)
                #Update Green slider
                gpos = pos1
                refreshSlider()
                drawSlide()
            elif bSliderCollide.collidepoint(pygame.mouse.get_pos()) and m1 == 1:
                b = pos1 - sliderX
                screen.set_clip(bSliderCollide)
                #Update Blue slider
                bpos = pos1
                refreshSlider()
                drawSlide()

            #Update the selected colour
            i = paletteHighlightList.index(selectedColourPos)
            paletteColourList[i] = r,g,b
            selectedColour = paletteColourList[i]
            
            #Delete the selected colour if button is pressed
            '''
            if delColourCollide.collidepoint(pygame.mouse.get_pos()) and click:
                i = palettePosList.index(selectedColourPos)
                selectedColour, selectedColourPos = paletteColourList[1], palettePosList[1]
                del paletteColourList[i]
                del palettePosList[i]
                del paletteHighlightList[-1]
            '''
    
                
            #if the close icon is highlighted, give feedback
            if XiconCollide.collidepoint(pygame.mouse.get_pos()):
                screen.blit(XiconHighlight, (810,110))
                #if the close icon is clicked, close window
                if click:
                    screen.blit(screenSave, (0,0))
                    delay_longest()
                    #drawing palette on main screen
                    #Refresh palette list
                    draw.rect(screen, (70,70,70), (1037, 400, 150, 300)) #redraw colour picker box
                    
                    paletteX = 0
                    paletteY = 0
                    for i in range(len(paletteColourList)):
                        paletteX += 1
                        if paletteX > 6:
                            paletteX = 1
                            paletteY += 1
                        draw.rect(screen, paletteColourList[i], (1024 + paletteX*23, 500 + paletteY*23, 16, 16))
                    break

                
            #Reset parameters
            screen.set_clip(None)
            
            display.flip()
    





        

    #Changing brush sizes
    if (pygame.key.get_pressed()[pygame.K_EQUALS]):
        brushSize += 1
        if brushSize > 10:
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
    #Mouse Position box
    
    #Reset parameters
    screen.set_clip(None)

    #Update line pos
    linePosX, linePosY = pos1, pos2
    
    display.flip()
    
print("Shutting down")
quit()

