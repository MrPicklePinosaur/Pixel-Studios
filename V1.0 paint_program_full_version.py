#Pixel Studios Paint Program
#Created by Daniel Liu
#V1.0 - stable version
import pygame
from pygame import *
from tkinter import *
import random
pygame.init()
mixer.init()
font.init()

print(pygame.display.Info())

print('''
               Debugging Mode
You are running Pixel Studios Paint Program V1.0
           Created by Daniel Liu''')


'''
=========== All Commands ===========
leftmouse - draw with selected colour
middlemouse - eye drop
rightmouse - erase


PLanned:
(Ctrl + Z) - Undo
blur tool
debugging mode (shows the events)
'''

#Screen size
screen = display.set_mode((1200,800))

#Surfaces
canvasScreen = pygame.Surface((830,650))
dimScreen = pygame.Surface((1200,800), pygame.SRCALPHA)
overlay = pygame.Surface((500,650))
airBrushMask = pygame.Surface((32,32), pygame.SRCALPHA)
screenShot = screen.subsurface(194,50,830,650)
optionsOverlay = None
shapeScreen = screen.subsurface(0,0,1200,800)

toolBarHighLight = Surface((50,20), pygame.SRCALPHA)
toolBarHighLight.fill((94,155,255,125))
toolBarOptionHighLight = Surface((170,30), pygame.SRCALPHA)
toolBarOptionHighLight.fill((94,155,255,125))


#Load assets =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#images
#loading images
icon = pygame.image.load("assets/images/pixelStudios.png")
Xicon = pygame.image.load("assets/images/Xicon.png")
XiconHighlight = image.load("assets/images/XiconHighlight.png")
sound_mute = image.load("assets/images/sound_mute.png")
sound_low = image.load("assets/images/sound_low.png")
sound_high = image.load("assets/images/sound_high.png")
opacity = image.load("assets/images/opacity.png")

#Define tool collide list, and it's corresponding tool
toolList = ["pencil", "eraser", "drawLine", "drawRect", "drawEllipse", "drawPolyLine",
            "eyedropper", "paintBrush", "artBrush", "spray", "highLighter", "stamp"]

#load tool icons
toolIconList = []
for i in range(len(toolList)):
    toolIconList.append(image.load("assets/images/" + str(toolList[i]) + "ToolIcon.png"))


#backgrounds
rndTheme = random.randint(1,7)
backGroundTheme = image.load("assets/images/backgrounds/backGround" + str(rndTheme) + ".png")
mainBackGround = transform.scale(backGroundTheme, (1200,800))

#stamps
stampList = []
for i in range(12):
    stamp = image.load("assets/images/stamps/stamp" + str(i+1) + ".png")
    stampList.append(transform.scale(stamp, (128,128)))


#songs
songList = ["Music_1 - SuperMario.ogg", "Music_2 - SuperMarioWorld.ogg", "Music_3 - Kirby.ogg", "Music_4 - StreetFighter.ogg",
            "Music_5 - PokemonBattle.ogg", "Music_6 - Sonic.ogg", "Music_7 - Megaman.ogg"]

#Load fonts
arialFont = font.SysFont("Arial",16)
comicFont = font.SysFont("Comic Sans", 16)


#initialize window info and set random program name
display.set_icon(icon)

captionList = ["Can I please get a waffle", "Now in 2D!", "Paint Program", "With more than 100,000 lines of code!",
               "The FUTURE of painting!", "wHEn lIfE giVEs YOu LEmoNS", "Now in 8-bit!", "Pixel Studios - Pixel Studios - ",
               "Now with colour!"] #list of potential quotes
rnd = random.randint(0,len(captionList)-1)
display.set_caption("Pixel Studios - " + captionList[rnd])

#Colours =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
white = (255,255,255)
black = (0,0,0)

themeColours1 = [(53,255,66),(41,160,20),(255,168,208),(204,206,204),(204,206,204),(183, 110, 58),(204,206,204),(204,206,204)] #base colour
themeColours2 = [(165,255,167),(94,188,77),(247,200,221),(234,114,107),(160,160,160),(255,253,170),(87,229,229),(255,253,170)] #light highlight
themeColours3 =  [(4,201,8),(22,119,4),(224,116,164),(255,14,0),(110,110,110),(252,235,47),(33,151,255),(252,235,47)] #dark highlight

sliderC1 = (220,220,220)
sliderC2 = (255,255,0)
sliderX = 500
sliderY = 150
  
colour = black
backGround = white

#current selected colour index
currentColourIndex = 0

#Colour slide pos
rpos = sliderX
gpos = sliderX
bpos = sliderX

#brushSize slider pos
brushSliderPos = 1050

#sound button
soundButtonX = 1149
soundButtonY = 46

#overlay window colours
overlayC1 = (40,40,40)
paletteBoxC1 = (70,70,70)

#Tool Box Highlight colours
toolBoxC1 = themeColours1[rndTheme-1] #(55, 255, 0)
toolBoxC2 = themeColours2[rndTheme-1]#(255,253,170)
toolBoxC3 = themeColours3[rndTheme-1]#(252,235,47)

#Colour box highlight colours
colourBoxC1 = overlayC1
colourBoxC2 = themeColours3[rndTheme-1] #(225,225,0)

#highlighter
ro, go, bo = 0,0,0

#Tool Commands =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
pos1, pos2 = 0,0

toolType = "pencil" #default tool type

#saving the cordinates of older pos
oldPos1, oldPos2 = 0,0

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

undoToggle1 = False
undoToggle2 = False

#polyline
polyLineList = []

#Tool bar
numberOfTools = None
toolBarList = ["File", "Edit"]

#stamp
selectedStamp = 0


#Toggles =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
colourWheelOn = 1
inputToggle = 1
paintToggle = 2
fillToggle = brushSize
snapToggle = 1
optionToggle = False


#Functions =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
click = False
keyClick = False
    
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

def mousePosBox():
    
    #Mouse Position box
    screen.set_clip(None)
    draw.rect(screen, (40,40,40), (194,700,80,30))
    #Display mouse position
    #show no position if mouse is outside canvas
    if canvasCollide.collidepoint(mouse.get_pos()):
        mx, my = str(pos1 - 194), str(pos2 - 50)
    else:
        mx, my = str("---"), str("---")
        
    mouseTextX, mouseTextY = arialFont.render("X:" + mx, False, white), arialFont.render("Y:" + my, False, white)
    screen.blit(mouseTextX, (194,700)) #draw text on screen
    screen.blit(mouseTextY, (234,700))
    
#Tools
def pencil():
    draw.line(screen, colour, (pos1, pos2), (oldPos1, oldPos2), 2)

def spray():
    for i in range(4):
        #define random points in a square
        rnd1, rnd2 = random.randint(-(brushSize+20), brushSize+20), random.randint(-(brushSize+20), brushSize+20)
        #check to see if thos points are in the spray circle, if they are, draw them
        if ((rnd1)**2 +(rnd2)**2)**0.5 <= (brushSize+20):
            draw.rect(screen, colour, ((pos1 + rnd1), (pos2 + rnd2), 2, 2))


def brush(n):
    #Find the distance from each point
    distanceX = pos1 - oldPos1
    distanceY = pos2 - oldPos2
    distance = int((distanceX**2 + distanceY**2)*0.5)
    #Draw circles going to each point
    for i in range(0,distance-1):
        h = int(oldPos1 + i*distanceX/distance)
        k = int(oldPos2 + i*distanceY/distance)
        #transparent brush
        if n == "highLighter":
            highLighterMask = Surface((40,40),SRCALPHA) #reset transparent surface
            highLighterMask.fill((255,255,255,0))
            draw.circle(highLighterMask, (ro,go,bo,5), (20,20), brushSize+4) #draw transparent strokes
            screen.blit(highLighterMask, (h-20,k-20))
                
        elif n == "paintBrush":
            draw.circle(screen, colour, (h,k), brushSize+2)
            
        elif n == "artBrush": #chang size depending on speed
            if distance == 0:
                draw.circle(screen, colour, (h,k), brushSize+6)
            if distance < 100:
                draw.circle(screen, colour, (h,k), brushSize+5)
            elif distance < 200:
                draw.circle(screen, colour, (h,k), brushSize+4)
            elif distance < 300:
                draw.circle(screen, colour, (h,k), brushSize+3)
            else:
                draw.circle(screen, colour, (h,k), brushSize+2)
                
            #print(((pos1-oldPos1)**2 + (pos2-oldPos1)**2)**0.5)

        elif n == "eraser":
            draw.circle(screen, white, (h,k), brushSize+2)
    
def eyedropper():
        colour = screen.get_at((pos1, pos2)) #pick colour mouse is hovered over
        delay_short()
        print("Colour was changed to", colour)
        
def drawShape(n): #draw basic shapes (start point and end point)
    #Resest parameters
    snapCollide = None
    snapToggle = 1
    polyLineList = []
    while True:
        
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
                #add point to polyline list
                if n == "polyLine" and len(polyLineList) == 0:
                    polyLineList.append((shapeX1,shapeY1))
                    snapCollide = (shapeX1-10,shapeY1-10,20,20)
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
                
            
            #Save Screen and reload
            reload()
            shapeX2, shapeY2 = pos1, pos2
            #Determines which shape to draw (depending on selected tool)
            if n == "line":
                draw.line(screen, colour, (shapeX1, shapeY1), (shapeX2, shapeY2), brushSize)
            elif n == "rect":
                #Draw square if shift is held
                if (pygame.key.get_pressed()[pygame.K_LSHIFT]) or (pygame.key.get_pressed()[pygame.K_RSHIFT]):
                        #Draw in 2nd and 4th quadrant if shapeX2 and shapeY2 are there
                        if (shapeX2-shapeX1 >= 0 and shapeY2-shapeY1 >= 0) or (shapeX2-shapeX1 <= 0 and shapeY2-shapeY1 <= 0):
                            parameters = Rect(shapeX1, shapeY1, (shapeX2 - shapeX1), (shapeX2 - shapeX1))
                        #Draw in 1st and 3rd quadrant if shapeX2 and shapeY2 are there
                        else:
                            parameters = Rect(shapeX1, shapeY1, -(shapeX1 - shapeX2), (shapeX1 - shapeX2))
                    
                    
                else: #draw normal rect
                    parameters = Rect(shapeX1, shapeY1, (shapeX2 - shapeX1), (shapeY2 - shapeY1))

                parameters.normalize()
                
                #draw rectangle
                draw.rect(screen, colour, (parameters[0], parameters[1], parameters[2], brushSize+1)) #top left to top right
                draw.rect(screen, colour, (parameters[0], parameters[1]+parameters[3], parameters[2], brushSize+1)) #bottom left to bottom right
                draw.rect(screen, colour, (parameters[0], parameters[1], brushSize+1, parameters[3])) #top left to bottom left
                draw.rect(screen, colour, (parameters[0]+parameters[2]-brushSize-1, parameters[1], brushSize+1, parameters[3])) #Top right to bottom right

                if fillToggle == 0: #fill rect if fillToggle is 0
                    draw.rect(screen, colour, parameters)
                
            elif n == "ellipse":
                #If shift is pressed, draw circle
                if (pygame.key.get_pressed()[pygame.K_LSHIFT]) or (pygame.key.get_pressed()[pygame.K_RSHIFT]):
                    try:
                        #Draw in 2nd and 4th quadrant if shapeX2 and shapeY2 are there
                        if (shapeX2-shapeX1 >= 0 and shapeY2-shapeY1 >= 0) or (shapeX2-shapeX1 <= 0 and shapeY2-shapeY1 <= 0):
                            parameters = Rect(shapeX1, shapeY1, (shapeX2 - shapeX1), (shapeX2 - shapeX1))
                        #Draw in 1st and 3rd quadrant if shapeX2 and shapeY2 are there
                        else:
                            parameters = Rect(shapeX1, shapeY1, -(shapeX1 - shapeX2), (shapeX1 - shapeX2))
                    
                        parameters.normalize()
                        draw.ellipse(screen, colour, parameters,fillToggle)
                    except:
                        pass
                #Draw normal ellipse
                else:
                    try:
                        parameters = Rect(shapeX1, shapeY1, (shapeX2 - shapeX1), (shapeY2 - shapeY1))
                        parameters.normalize()
                        draw.ellipse(screen, colour, parameters,fillToggle)
                    except:
                        pass
                
            elif n == "polyLine":
                #Draw the polyLine
                for i in range(1,len(polyLineList)):
                    if len(polyLineList) == 2:
                        draw.line(screen, colour, polyLineList[0], (shapeX2,shapeY2), brushSize)
                    else:
                        draw.line(screen, colour, polyLineList[-1], (shapeX2,shapeY2), brushSize)
                
                #Check for snap
                if Rect(snapCollide).collidepoint(mouse.get_pos()) and len(polyLineList) > 2:
                    reload()
                    draw.line(screen, colour, polyLineList[-1], polyLineList[0], brushSize)
                    if inputToggle == 2:
                        snapToggle = 2

            #Break loop
            if inputToggle == 2:
                break

            mousePosBox()
            screen.set_clip(canvasCollide)
            display.flip()

        #add endpoint to list
        if n == "polyLine":
            polyLineList.append((shapeX2,shapeY2))
                        
        #check to see if polygon is drawn
        if n == "polyLine" and snapToggle == 2:
            undoList.append(screenShot.copy())
            break

        #Break loop if not polyLine
        if n != "polyLine":
            undoList.append(screenShot.copy())
            break


def stamp():
    stamp = transform.scale(stampList[selectedStamp], (brushSize*30, brushSize*30))
    if click: #draw stamp
        screen.blit(stamp, ((pos1-brushSize*15, pos2-brushSize*15)))
        
def undo():
    if len(undoList) < 3: #make sure there is still undos to be made
        pass
    else:
        screen.blit(undoList[-2], (194,50)) #blit the undo screen
        if len(undoList) != 2 and len(undoList) != 1:
            redoList.append(undoList[-2]) #move blitted screen into redo list and remove from undo list
            del undoList[-2]
    print("Undo")

def redo():
    if len(redoList) < 3: #make sure there are still redos to be made
        pass
    else:
        screen.blit(redoList[-2], (194,50))
        undoList.append(redoList[-2]) #move blitted screen into undo list and remove from redo list
        del redoList[-2]
    print("Redo")
    
def save():
    try:
        #opens window for user to choose file
        fname = filedialog.asksaveasfilename(defaultextension=".png")
        #save drawing
        pygame.image.save(screenShot, fname)
        print("Drawing was saved as", fname)
    except: #if no name is entered, do nothing
        print("Unable to save", fname)

def load():
    try:
        #opens window for user to choose file
        fname = filedialog.asksaveasfilename(defaultextension=".png")
        drawing = pygame.image.load(fname)
        #draws chosen file on screen
        screen.blit(transform.scale(drawing, (830,650)), (194,50))
        delay_short()
        print(drawingName, "was loaded")
    #If program crashes, display message 
    except:
        print("Unable to open", str(fname))

def clear():
    draw.rect(screen, white, canvasCollide)
    undoList.append(screenShot.copy())
    print("Screen was cleared")
    
def fill():
    draw.rect(screen, colour, canvasCollide)
    undoList.append(screenShot.copy())
    print("Screen was filled with", colour)
    
#other functions
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
canvasCollide = Rect(194,50,830,650)
rSliderCollide = Rect(sliderX,sliderY,255,20)
gSliderCollide = Rect(sliderX,sliderY+30,255,20)
bSliderCollide = Rect(sliderX,sliderY+60,255,20)
overlayCollide = Rect(350, 100, 500 ,650)
XiconCollide = Rect(810,110,32,32)
addColourCollide = Rect(665,240,40,20)
delColourCollide = Rect(715,240,40,20)
volumeSliderCollide = Rect(1039,52,100,20)
        
toolBoxX = 20
toolBoxY = 55
toolBoxGap = 90

#Tool bar collidepoints
toolBarCollideList = []
for i in range(len(toolBarList)):
    toolBarCollideList.append(Rect(i*50,0,50,20))

#tool bar options
toolBarOptionsList = []

#Stamp collide
stampCollideList = []
stampHighLightList = []
stampX = 0
stampY = 0
for i in range(len(stampList)+1):
    stampX += 1
    if stampX > 3:
        stampY += 1
        stampX = 1
    stampCollideList.append((222+stampX*158,150+stampY*148))
    stampHighLightList.append(Rect(222+stampX*158,150+stampY*148,128,128))

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

#tooltip discriptions
toolTipX = [130,130,130,200,200,230,130,230,230,130,200,230]
toolTipDiscrip = ["Cannot change size","Standard Eraser","Hold to draw a line","Hold SHIFT to draw square", "Hold SHIFT to draw circle","Draw lines until a polygon is formed"
                  ,"Picks colour","A thick brush that draws smoothly","An artistic brush that changes in size","Spray paint effect","Draws over normal paint", "Select the stamp in the stamp menu"]

#Colours in palette and their location
paletteColourList = [(0,0,0)]
palettePosList = [Rect(409,290,32,32)]
palettePosListMini = [Rect(1047,500,16,16)]
paletteHighlightList = [Rect(408,289,34,34)]
paletteHighlightListMini = [Rect(1046,499,18,18)]
selectedColour = paletteColourList[0]
selectedColourPos = paletteHighlightList[0]
indexPaletteMini = 0



#Draw Screen =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
screen.fill((200,200,200)) #Draw background
screen.blit(mainBackGround, (0,0))

#draw.rect(screen, white, (canvasCollide))
canvasScreen.fill(white)

#Draw colour palette
draw.rect(screen, themeColours1[rndTheme-1], (1035,398,154,304)) #Draw colour picker highlight
draw.rect(screen, paletteBoxC1, (1037, 400, 150, 300)) #redraw colour picker box
draw.rect(screen, paletteColourList[0], palettePosListMini[0])

#Tool info box
draw.rect(screen, themeColours1[rndTheme-1], (1035,208,154,174))
draw.rect(screen, paletteBoxC1, (1037, 210, 150, 170))

#draw tool selection boxes
#Drawing background of box
for i in range(len(toolCollideList)):
    draw.rect(screen, toolBoxC1, toolCollideList[i])

toolIconX = 0
toolIconY = 0
#draw tool icons
for i in range(0,len(toolList)):
    screen.blit(toolIconList[i], (toolBoxX+toolBoxGap*toolIconX,toolBoxY+toolBoxGap*toolIconY))
    toolIconY += 1
    #Make new row of tools
    if toolIconY > 6:
        toolIconY = 0
        toolIconX = 1
        

#Draw highlights
for i in range(0,len(toolCollideList)):
    if i < 7:
        draw.rect(screen, toolBoxC1, (toolBoxX-5,toolBoxY-5+i*toolBoxGap,74,74),5)
    else: #Draw new column of highlights
        draw.rect(screen, toolBoxC1, (toolBoxX-5+toolBoxGap,toolBoxY-5+(i-7)*toolBoxGap,74,74),5)
        
#draw hightlight for selected tool
i = toolList.index(toolType)
draw.rect(screen, toolBoxC3, (toolBoxX-5,toolBoxY-5+i*toolBoxGap,74,74),5)

#draw highlight for selected colour
draw.rect(screen, colourBoxC2, paletteHighlightListMini[0])
draw.rect(screen, paletteColourList[0], palettePosListMini[0])

#Draw toolbar
draw.rect(screen, (220,220,220), (0,0,1200,20))

#Music
volume = 0.75
#play music
mixer.music.load("assets/music/" + songList[rndTheme-1])
mixer.music.play(-1)
print("Now playing", songList[rndTheme-1])

screen.blit(canvasScreen, (194,50))
#screen.blit(canvasBackGround, (194,50))

#add first and second screen to undo list and first screen to redo list
undoList.append(screenShot.copy())
undoList.append(screenShot.copy()) #placeholder
redoList.append(screenShot.copy())

#Draw volume slider
draw.rect(screen, themeColours1[rndTheme-1], (1037,50,104,24))
#refresh slider
for i in range(100):
    draw.rect(screen, (i*2,i*2,i*2), (1039+i,52,1,20))
#refresh slider box
draw.rect(screen, sliderC1, (1039+(volume*100),52,10,20))
screen.blit(sound_high, (soundButtonX,soundButtonY))

#draw muse psition box
mousePosBox()



#Running loops =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#Main Loop
running = True
while running:

    click = False
    keyClick = False
    for evt in event.get():

        #Finds out which mouse button is being pressed and where the mouse is
        m1, m2, m3 = pygame.mouse.get_pressed()
        pos1, pos2 = pygame.mouse.get_pos()
    
        if evt.type == QUIT:
            running = False

        #Determines if mouse is being clicked
        if evt.type == MOUSEBUTTONDOWN and m1 == 1:
            click = True

        #Determines if key being clicked
        if evt.type == KEYDOWN:
            keyClick = True
            
        #Check for canvas changes
        if canvasCollide.collidepoint(pygame.mouse.get_pos()):
            if evt.type == MOUSEBUTTONDOWN and (m1 == 1 or m3 == 1):
                undoToggle1 = True
            
            if undoToggle1 == True and evt.type == MOUSEBUTTONUP:
                undoToggle2 = True

    #Check for undo append
    if undoToggle1 == True and undoToggle2 == True:
        undoList.append(screenShot.copy())
        undoToggle1, undoToggle2 = False, False
            
    #song volume slider
    #refresh highlight
    if volumeSliderCollide.collidepoint(mouse.get_pos()):
        draw.rect(screen, themeColours1[rndTheme-1], (1037,50,104,24))
        #refresh slider
        for i in range(100):
            draw.rect(screen, (i*2,i*2,i*2), (1039+i,52,1,20))
        #refresh slider box
        draw.rect(screen, sliderC1, (1039+(volume*100),52,10,20))
        #Changing volume
        if m1 == 1:
            volume = (pos1-1039)/100

        mixer.music.set_volume(volume) #set volume

        #Volume icon
        mainBackGroundMask = (mainBackGround.subsurface((soundButtonX-8,soundButtonY,40,32)))
        screen.blit(mainBackGroundMask, (soundButtonX-8,soundButtonY))

        if volume == 0:
            screen.blit(sound_mute, (soundButtonX,soundButtonY))
        elif volume <= 0.5:
            screen.blit(sound_low, (soundButtonX,soundButtonY))
        else:
            screen.blit(sound_high, (soundButtonX,soundButtonY))



        
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
        if toolTickList[i] > 150:
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

                    #Determine which toolTip to display
                    draw.rect(screen,black, (pos1, pos2, toolTipX[i], 60)) #draw tooltip box
                    screen.blit(comicFont.render(toolList[i], False, (255,255,0)), (pos1+5, pos2+5)) #print tool name
                    screen.blit(comicFont.render(toolTipDiscrip[i], False, (255,255,255)), (pos1+5, pos2+25))

                    
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
                
    #Refresh tool box highlight
    toolBoxHighlight()




    #Using tools
    #If mouse is on canvas, enable editing mode
    if canvasCollide.collidepoint(pygame.mouse.get_pos()):
        mousePosBox()

        screen.set_clip(canvasCollide)
        #If mouse 1 is being pressed, use primary tools
        if m1 == 1:
            #Tools
            if toolType == "pencil":
                pencil()
            elif toolType == "paintbrush":
                paint()
            elif toolType == "eraser":
                brush("eraser")
            elif toolType == "eyedropper":
                colour = screen.get_at((pos1, pos2))
                delay_short()
            elif toolType == "spray":
                spray()
            elif toolType == "highLighter":
                brush("highLighter")
            elif toolType == "paintBrush":
                brush("paintBrush")
            elif toolType == "artBrush":
                brush("artBrush")
        
        #If middle mouse is being pressed, use eye dropper tool
        #Eye-dropper tool
        elif m2 == 1:
            colour = screen.get_at((pos1, pos2))
            delay_short()
            print("Colour was changed to", colour)
            
        #If right mouse is being pressed, use eraser tool
        elif m3 == 1:
            brush("eraser")

        #Other tools
        if toolType == "drawLine":
            drawShape("line")
            toolType = "pencil" #Reset tool type
        elif toolType == "drawRect":
            drawShape("rect")
            toolType = "pencil" 
        elif toolType == "drawEllipse":
            drawShape("ellipse")
            toolType = "pencil" 
        elif toolType == "drawPolyLine":
            drawShape("polyLine")
            toolType = "pencil"
        elif toolType == "stamp":
            stamp()

        
        #Reset screen clip
        screen.set_clip(None)

        
    #Colour Palette
    if Rect(1048,285,128,20).collidepoint(pygame.mouse.get_pos()) and click: #open colour picker window if palette butoon is clicked

        #Save screen
        pygame.image.save(screen, "assets/images/backGroundSave.png")
        screenSave = pygame.image.load("assets/images/backGroundSave.png")
        
        #Dim the screen and draw overlay menu
        dimScreen.fill((0,0,0,128))
        overlay.fill((overlayC1))
        screen.blit(dimScreen, (0,0))
        draw.rect(screen, themeColours1[rndTheme-1], (348,98,504,654))
        screen.blit(overlay, (350, 100))
        screen.blit(Xicon, (810,110))
        
        draw.rect(screen, (255,255,0), addColourCollide) #Button to add colour
        addButtonFont = comicFont.render("add", False, black)
        screen.blit(addButtonFont, (673,245))

        draw.rect(screen, (255,255,0), delColourCollide) #Button to delete a colour
        delButtonFont = comicFont.render("del", False, black)
        screen.blit(delButtonFont, (725, 245))
                    
        #Refresh palette list
        paletteX = 0
        paletteY = 0

        paletteXMini = 0 #need new variables as the small palette picker has 6 columns instead of 8
        paletteYMini = 0

        #draw the colours
        for i in range(len(paletteColourList)):
            paletteX += 1
            if paletteX > 8:
                paletteX = 1
                paletteY += 1
            draw.rect(screen, paletteColourList[i], (359 + paletteX*50, 290 + paletteY*50, 32, 32))

        #count the colours in the mini colour picker
        for i in range(len(palettePosListMini)):
            paletteXMini += 1
            if paletteXMini > 6:
                paletteXMini = 1
                paletteYMini += 1
                    
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
                palettePosList.append(Rect(359 + paletteX*50, 290 + paletteY*50, 32, 32))
                #add highlight pos of colour square to list
                paletteHighlightList.append(Rect(358 + paletteX*50, 289 + paletteY*50, 34, 34))
                
                #add mini colour box pos to list
                paletteXMini += 1
                if paletteXMini > 6:
                    paletteXMini = 1
                    paletteYMini += 1
                palettePosListMini.append(Rect(1024 + paletteXMini*23, 500 + paletteYMini*23, 16, 16))
                #add highlight pos of mini colour square to list
                paletteHighlightListMini.append(Rect(1023 + paletteXMini*23, 499 + paletteYMini*23, 18,18))

                
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
    
                
            #if the close icon is hovered over, highlight
            if XiconCollide.collidepoint(pygame.mouse.get_pos()):
                screen.blit(XiconHighlight, (810,110))
                #if the close icon is clicked, close window
                if click:
                    screen.blit(screenSave, (0,0))
                    delay_longest()
                    
                    #drawing palette on main screen
                    #Refresh palette list
                    draw.rect(screen, paletteBoxC1, (1037, 400, 150, 300)) #redraw colour picker box
                    #Update current colour
                    colour = paletteColourList[currentColourIndex]
                    ro,go,bo = paletteColourList[currentColourIndex]
                    break

                
            #Reset parameters
            screen.set_clip(None)
            
            display.flip()




    #Stamp menu (350,100,500,650)
    #Draw stamp button
    #open stamp menu
    if Rect(1048,315,128,20).collidepoint(mouse.get_pos()) and click:
        #Save screen
        pygame.image.save(screen, "assets/images/backGroundSave.png")
        screenSave = pygame.image.load("assets/images/backGroundSave.png")
        
        #Dim the screen and draw overlay menu
        dimScreen.fill((0,0,0,128))
        overlay.fill((overlayC1))
        screen.blit(dimScreen, (0,0))
        draw.rect(screen, themeColours1[rndTheme-1], (348,98,504,654))
        screen.blit(overlay, (350, 100))
        screen.blit(Xicon, (810,110))

        #Draw the background and draw stamp previews
        for i in range(len(stampList)):
                screen.blit((transform.scale(opacity, (128,128))), stampCollideList[i])
                screen.blit(stampList[i], stampCollideList[i])
                
        #Stamp loop
        while True:

            click = False
            for evt in event.get():

                #FInds out which mouse button is being pressed and where the mouse is
                m1, m2, m3 = pygame.mouse.get_pressed()
                pos1, pos2 = pygame.mouse.get_pos()
                            

                #Determines if mouse is being clicked
                if evt.type == MOUSEBUTTONDOWN and m1 == 1:
                    click = True

            #Refresh X icon
            draw.rect(screen, overlayC1, XiconCollide)
            screen.blit(Xicon, (810,110))

            #Refresh stamp highlights
            for i in range(len(stampList)):
                draw.rect(screen, overlayC1, stampHighLightList[i],4)
                #check if mouse is hovering over stamp
                if stampHighLightList[i].collidepoint(mouse.get_pos()):
                    draw.rect(screen, themeColours1[rndTheme-1], stampHighLightList[i],4)
                    if click: #set selected stamp
                        selectedStamp = i

            #Draw highlight around selected stamp
            draw.rect(screen, themeColours2[rndTheme-1], stampHighLightList[selectedStamp],4)
            
            #if the close icon is hovered over, highlight
            if XiconCollide.collidepoint(pygame.mouse.get_pos()):
                screen.blit(XiconHighlight, (810,110))
                #if the close icon is clicked, close window
                if click:
                    reload()
                    delay_longest()
                    break
                
            display.flip()
        
        
    #colour box and current stamp box
    draw.rect(screen, white, (1055,428,44,44))
    draw.rect(screen, colour, (1057,430,40,40))

    draw.rect(screen, white, (1127,428,44,44))
    screen.blit(transform.scale(opacity, (40,40)), (1129,430)) #draw background of current stamp box
    screen.blit(transform.scale(stampList[selectedStamp], (40,40)), (1129,430)) #draw current stamp preview

    #Pop-up window menus
    #Colour palette Menu button
    draw.rect(screen, (255,255,0), (1048,285,128,20))
    screen.blit(comicFont.render("Edit Colours", False, black), (1055,288))

    #Stamp Menu button
    draw.rect(screen, (255,255,0), (1048,315,128,20))
    screen.blit(comicFont.render("Select Stamps", False, black), (1055,318))

    #Toggle FillToggle switch
    draw.rect(screen, (255,255,0), (1048,345,128,20))
    #Draw button depending on toggle
    if fillToggle == brushSize:
        screen.blit(comicFont.render("FillToggle : OFF", False, black), (1055,348))
    elif fillToggle == 0:
        screen.blit(comicFont.render("FillToggle : ON", False, black), (1055,348))


    #Changing brush sizes
    #Draw "brush size" text
    screen.blit(comicFont.render("Brush Size:", False, white), (1050, 220))

    #Refresh brushSize slider box
    draw.rect(screen, themeColours2[rndTheme-1], (1048,238,128,24))
    draw.rect(screen, (240,240,240), (1050,240,124,20))

    #refresh brushSize sliders
    draw.rect(screen, sliderC1, (brushSliderPos,240,10,20))
    draw.rect(screen, paletteBoxC1, (1176,240,10,20))
    
    #moving brushSize Slider
    if Rect(1050,240,124,20).collidepoint(mouse.get_pos()) and m1 == 1:
        brushSliderPos = pos1

    #Update brushSize
    brushSize = int((brushSliderPos - 1050)/12.4) + 1
    


    #MINI PALETTE
    #Check to see if any of the colour in Mini colour picker are being hovered over
    for i in range(len(palettePosListMini)):
        #Reset colour box highlights
        draw.rect(screen, paletteBoxC1, paletteHighlightListMini[i])
        if palettePosListMini[i].collidepoint(pygame.mouse.get_pos()):
            #Highlight mini colour box if hovered over
            draw.rect(screen, paletteColourList[i], paletteHighlightListMini[i])
            #set the colour if colour box is clicked
            if click:
                colour = paletteColourList[i]
                ro, go, bo = paletteColourList[i]
                currentColourIndex = i
                indexPaletteMini = i


    #Draw the highlights on the selected colour
    if currentColourIndex != None:
        draw.rect(screen, colourBoxC2, paletteHighlightListMini[indexPaletteMini])

    #Refresh all the colour boxes
    for i in range(len(paletteColourList)):
        draw.rect(screen, paletteColourList[i], palettePosListMini[i])



    #ToolBar
    #Refresh ToolBar
    draw.rect(screen, (220,220,220), (0,0,1200,20))
    for i in range(len(toolBarList)):
        #Refresh toolbar tool names
        toolBarText = comicFont.render(str(toolBarList[i]), False, black)
        screen.blit(toolBarText, (i*50+7,7))

    #Check to see if any of the tool bar is being hovered over
    for i in range(len(toolBarList)):
        if toolBarCollideList[i].collidepoint(mouse.get_pos()):
            screen.blit(toolBarHighLight, (i*50,0))
            #open options if clicked
            if click:
                #Set option box size
                if i == 0:
                    numberOfTools = 2
                elif i == 1:
                    numberOfTools = 4

                #Save screen
                pygame.image.save(screen, "assets/images/backGroundSave.png")
                canvasMask = screenShot.copy()
                
                #reset option collide list
                toolBarOptionsList = []
                #set collides for tools, depending on the column its in
                if i == 0:
                    for n in range(0,2):
                        toolBarOptionsList.append(Rect(0,20+n*30,170,30))
                        
                elif i == 1:
                    for n in range(0,4):
                        toolBarOptionsList.append(Rect(50,20+n*30,170,30))
                        
                while True:

                    click = False
                    for evt in event.get():

                        #FInds out which mouse button is being pressed and where the mouse is
                        m1, m2, m3 = pygame.mouse.get_pressed()
                        pos1, pos2 = pygame.mouse.get_pos()
                            
                        #Determines if mouse is being clicked
                        if evt.type == MOUSEBUTTONDOWN and m1 == 1:
                            click = True

                    #Refresh Option window
                    draw.rect(screen, (245,245,245), (i*50,20,170,30*numberOfTools))

                    #Draw option names
                    if i == 0:
                        screen.blit(comicFont.render("Save    CTRL + S", False, black), (10,30))
                        screen.blit(comicFont.render("Open    CTRL + O", False, black), (10,60))
                    if i == 1:
                        screen.blit(comicFont.render("Undo    CTRL + Z", False, black), (60,30))
                        screen.blit(comicFont.render("Redo    CTRL + SHIFT + Z", False, black), (60,60))
                        screen.blit(comicFont.render("Clear Screen    CTRL + C", False, black), (60,90))
                        screen.blit(comicFont.render("Fill Screen    CTRL + F", False, black), (60,120))

                    #draw highligts
                    for n in range(len(toolBarOptionsList)):
                        if toolBarOptionsList[n].collidepoint(mouse.get_pos()):
                            screen.blit(toolBarOptionHighLight, toolBarOptionsList[n])
                            
                    #save screen with options open
                    canvasMaskAlt = screen.subsurface(Rect(i*50,20,170,30*numberOfTools)).copy()
                        
                    #update screen (as there is an overlap)
                    screen.blit(canvasMask, (194,50))
                                
                    #check to see if tools are being hovered over
                    for n in range(len(toolBarOptionsList)):
                        if toolBarOptionsList[n].collidepoint(mouse.get_pos()) and click: #if click, perform the option
                            #using grid system to determine which option is chosen
                            if i == 0 and n == 0: #column 1, row 1 : save
                                save()
                            elif i == 0 and n == 1: #column 1, row 2 : load
                                load()
                            elif i == 1 and n == 0: #column 2, row 1 : undo
                                undo()
                            elif i == 1 and n == 1: #column 2, row 2 : redo
                                redo()
                            elif i == 1 and n == 2: #column 2, row 3 : clear screen
                                clear()
                            elif i == 1 and n == 3: #column 2, row 4 : fill screen with selected colour
                                fill()

                    #save and draw updated screen
                    canvasMask = screenShot.copy()
                    screen.blit(canvasMask, (194,50))

                    #save and draw options menu again
                    #canvasMaskAlt = screen.copy()
                    screen.blit(canvasMaskAlt, (i*50,20))
                    
                    #break loop if anywhere else but window is cicked
                    if not Rect(i*50,20,170,30*numberOfTools).collidepoint(mouse.get_pos()) and click:
                        #reset screen
                        reload()
                        screen.blit(canvasMask, (194,50))
                        break
                    
        
                    display.flip()
        
        
    #Toggle shape fill/unfill
    if Rect(1048,345,128,20).collidepoint(mouse.get_pos()) and click:
        #Make shape Unfilled
        if fillToggle == 0:
            fillToggle = brushSize
            ("fillToggle off")
        #Make shape flled
        elif fillToggle != 0:
            fillToggle = 0
            print("fillToggle on")

    #update fillToggle
    if fillToggle != 0:
        fillToggle = brushSize


    '''
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



    #Keyboard shortcuts
    #Shortcuts that use control
    if (pygame.key.get_pressed()[pygame.K_LCTRL]) or (pygame.key.get_pressed()[pygame.K_RCTRL]):
        #Save (CTRL + S)
        if (pygame.key.get_pressed()[pygame.K_s]) and keyClick:
            save()
        #Load (CTRL + O)
        elif (pygame.key.get_pressed()[pygame.K_o]) and keyClick:
            load()
        #redo (CTRL + SHIFT + Z)
        elif (pygame.key.get_pressed()[pygame.K_LSHIFT]) or (pygame.key.get_pressed()[pygame.K_RSHIFT]):
            if (pygame.key.get_pressed()[pygame.K_z]) and keyClick:
                redo()
        #Undo (CTRL + Z)
        elif (pygame.key.get_pressed()[pygame.K_z]) and keyClick:
            undo()
        #Clear screen (CTRL + C)
        elif (pygame.key.get_pressed()[pygame.K_c]) and keyClick:
            clear()
        #Fill screen (CTRL + F)
        elif (pygame.key.get_pressed()[pygame.K_f]) and keyClick:
            fill()

            
    #Update old pos
    oldPos1, oldPos2 = pos1, pos2

    mousePosBox()
    screen.set_clip(None)
    display.flip()
    
    
print("Shutting down")
quit()
