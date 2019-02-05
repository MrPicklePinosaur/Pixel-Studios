#Dank Paint Program
#Created by Daniel Liu
#V0.6 - many fixes and improvements
import pygame
from pygame import *
from tkinter import *
import random
pygame.init()
mixer.init()
#font.init()

print('''
You are running Pixel Studios Paint Program V0.6
           Created by Daniel Liu''')

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
canvasScreen = pygame.Surface((850,650))
dimScreen = pygame.Surface((1200,800), pygame.SRCALPHA)
overlay = pygame.Surface((500,650))

#Load assets
#images
backGround1 = pygame.image.load("assets/images/backGround1.png")
icon = pygame.image.load("assets/images/USSR.png")
Xicon = pygame.image.load("assets/images/Xicon.png")
XiconHighlight = pygame.image.load("assets/images/XiconHighlight.png")


#tool icons
pencilToolIcon = pygame.image.load("assets/images/pencilToolIcon.png")
paintToolIcon = pygame.image.load("assets/images/paintToolIcon.png")

#sounds
pygame.mixer.music.load("assets/music/music_1.mp3")
#click = 
#initialize window
display.set_icon(icon)
#set random program name
captionList = ["Pixel Studios - ", "Pixel Studios - ", "Pixel Studios - "]
rnd = random.randint(0,len(captionList)-1)
display.set_caption(captionList[rnd])

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

#Colours in palette and their location
paletteList = [black]
palettePosList = [(409,290,32,32)]

#overlay window colour
overlayC1 = 40,40,40
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
undoList = []
redoList = []
#screen.subsurface(canvas).copy()
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


def drawShape(n): #draw basic shapes (start point and end point)
    #Save screen
    pygame.image.save(screen, "assets/images/backGroundSave.png")
    print("Input start and end points of shape")

    #Toggle
    inputToggle = 1

    while True:
        
        click = False
        for evt in event.get():
                
            if evt.type == QUIT:
                break

            if evt.type == MOUSEBUTTONDOWN:
                click = True
            
        #Mouse input functions in loop
        m1, m2, m3 = pygame.mouse.get_pressed()
        pos1, pos2 = pygame.mouse.get_pos()
            
        #Getting start point of line
        if click and inputToggle == 1:
            shapeX1, shapeY1 = pos1, pos2
            inputToggle = 2
            print("Start point of shape:", shapeX1, shapeY1)
            delay_longest()
            
        #Getting end point of line
        elif inputToggle == 2:
                
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
                
            display.flip()

            if click:
                print("End point of shape :", shapeX2, shapeY2)
                print("Drawn shape, exiting drawShape loop")
                toolType = "pencil"
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
canvasCollide = Rect(175,50,850,650)
rSliderCollide = Rect(sliderX,sliderY,255,20)
gSliderCollide = Rect(sliderX,sliderY+30,255,20)
bSliderCollide = Rect(sliderX,sliderY+60,255,20)
overlayCollide = Rect(350, 100, 500 ,650)
XiconCollide = Rect(810,110,32,32)
addColourCollide = Rect(665,240,40,20)
delColourCollide = Rect(715,240,40,20)
#Draw Screen =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
screen.fill((200,200,200)) #Draw background
canvasScreen.fill((white))
canvasScreen.blit(canvasScreen, (175,50))
screen.blit(backGround1, (0,0))

draw.rect(screen, white, (canvasCollide)) #Draw canvas

colourPalette = draw.rect(screen, black, (100,700,50,50))

#draw tool icons
screen.blit(pencilToolIcon, (50,50))
screen.blit(paintToolIcon, (50,150))
'''
pencilButton
paintButton
eraserButton
lineButton
rectButton
eyedropperButton
'''
#Play music
mixer.music.play()



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
        if evt.type == MOUSEBUTTONDOWN:
            click = True

    
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
        if toolType == "drawLine":
            drawShape("line")
        elif toolType == "drawRect":
            drawShape("rect")
        elif toolType == "drawCircle":
            drawShape("circle")
            
        '''
        elif toolType == "undo":
            undo()
        elif toolType == "redo":
            redo()
        '''
    #Update line pos
    linePosX, linePosY = pos1, pos2
    
    
    #Colour Palette
    if colourPalette.collidepoint(pygame.mouse.get_pos()) and click:

        #Save screen
        pygame.image.save(screen, "assets/images/backGroundSave.png")
        screenSave = pygame.image.load("assets/images/backGroundSave.png")
        
        #Dim the screen and draw overlay menu
        dimScreen.fill((0,0,0,128))
        overlay.fill((overlayC1))
        screen.blit(dimScreen, (0,0))
        screen.blit(overlay, (350, 100))
        screen.blit(Xicon, (810,110))
        
        draw.rect(screen, (255,255,0), addColourCollide) #Button to make add colour
        draw.rect(screen, (255,255,0), delColourCollide)
        #screen.set_clip(overlayCollide)

        #Refresh palette list
        paletteX = 0
        paletteY = 0

        for i in range(len(paletteList)):
            paletteX += 1
            if paletteX > 8:
                paletteX = 1
                paletteY += 1
            draw.rect(screen, paletteList[i], (359 + paletteX*50, 290 + paletteY*50, 32, 32))
                    
        initSliders()
        #Colour palette loop
        while True:
            
            click = False
            for evt in event.get():
                
                #Mouse input functions in loop
                m1, m2, m3 = pygame.mouse.get_pressed()
                pos1, pos2 = pygame.mouse.get_pos()

                if evt.type == QUIT:
                    running = False
                
                if evt.type == MOUSEBUTTONDOWN and m1 == 1:
                    click = True
                
            #Refresh icons
            draw.rect(screen, overlayC1, XiconCollide)
            screen.blit(Xicon, (810,110))

            #Colour slider
            #Refresh colour box
            draw.rect(screen, (r,g,b), (sliderX-90,sliderY,80,80))
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


            #add the selected colour to the palette if clicked
            if addColourCollide.collidepoint(pygame.mouse.get_pos()) and click:
                paletteList.append((r,g,b))
                #add colour to palette list
                paletteX += 1
                if paletteX > 8:
                    paletteX = 1
                    paletteY += 1
                draw.rect(screen, paletteList[-1], (359 + paletteX*50, 290 + paletteY*50, 32, 32))
                #add pos of square to list
                palettePosList.append((359 + paletteX*50, 290 + paletteY*50, 32, 32))
                

            #Using a colour

            
            #Reset parameters
            screen.set_clip(None)
            
            #if the close icon is highlighted, give feedback
            if XiconCollide.collidepoint(pygame.mouse.get_pos()):
                screen.blit(XiconHighlight, (810,110))
                #if the close icon is clicked, close window
                if click:
                    screen.blit(screenSave, (0,0))
                    delay_longest()
                    #drawing palette on main screen
                    #Refresh palette list
                    paletteX = 0
                    paletteY = 0
                    for i in range(len(paletteList)):
                        paletteX += 1
                        if paletteX > 6:
                            paletteX = 1
                            paletteY += 1
                        draw.rect(screen, paletteList[i], (1022 + paletteX*23, 500 + paletteY*23, 16, 16))
                    break
                
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
        canvasScreen.fill(colour)
        delay_short()
        print("Screen was filled in with", colour)

    #Clear screen
    if (pygame.key.get_pressed()[pygame.K_c]):
        canvasScreen.fill(white)
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

