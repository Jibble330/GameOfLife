import pygame, sys, math, ctypes
import numpy as np
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

#Constants
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLACK = (0, 0, 0)
GREY = (120, 120, 120)
DARK_GREY = (20, 20, 20)
BLUE = (56, 132, 255)
FPS = 60

scroll = 0
tileSize = round(SCREEN_HEIGHT/21.6)
gridSize = 1000
coordinateGrid = []
surroundGrid = []
paused = True
frame = 0
equivilant10px = round(SCREEN_HEIGHT/108)

def tilesX():
    return math.floor(SCREEN_WIDTH/tileSize)

def tilesY():
    return math.floor(SCREEN_HEIGHT/tileSize)

gridOffset = [round((gridSize/2)-(tilesX()/2)), round((gridSize/2)-(tilesY()/2))]

def nextGen(): #Advance to the next generation
    updateList = getUpdate()
    surroundUpdate(updateList)
    for i in updateList:
        y = i[0]
        x = i[1]
        surround = surroundGrid[y][x]
        currentTile = coordinateGrid[y,x]
        if currentTile == 0 and surround == 3:
            coordinateGrid[y,x] = 1
        if currentTile == 1:
            if surround < 2 or surround > 3:
                coordinateGrid[y,x] = 0

def getUpdate():
    location = np.where(coordinateGrid == 1)
    totalUpdate = []
    for i in range(len(location[0])):
        y = location[0][i]
        x = location[1][i]
        totalUpdate.append([y, x])
        totalUpdate.append([y-1,x-1])
        totalUpdate.append([y-1,x])
        totalUpdate.append([y,x-1])
        if y != len(coordinateGrid)-1:
            totalUpdate.append([y+1,x-1])
            totalUpdate.append([y+1,x])
        else:
            totalUpdate.append([0,x-1])
            totalUpdate.append([0,x])
        if x != len(coordinateGrid[y])-1:
            if y != len(coordinateGrid)-1:
                totalUpdate.append([y+1,x+1])
            else: #Loops around if on edge
                totalUpdate.append([0,x+1])
            totalUpdate.append([y-1,x+1])
            totalUpdate.append([y,x+1])
        else:
            if y != len(coordinateGrid)-1:
                totalUpdate.append([y+1,0])
            else: #Loops around if on edge
                totalUpdate.append([0,0])
            totalUpdate.append([y-1,0])
            totalUpdate.append([y,0])
    updateList = []
    [updateList.append(i) for i in totalUpdate if i not in updateList]
    return updateList

def surroundInit():
    for y in range(len(coordinateGrid)):
        baseInside = []
        for x in range(len(coordinateGrid[y])):
            baseInside.append(0)
        surroundGrid.append(baseInside)

def surroundUpdate(updateList):
    for i in updateList:
        y = i[0]
        x = i[1]
        surround = getSurrounding(x, y)
        surroundGrid[y][x] = surround

def getSurrounding(x, y): #Get the number of alive tiles arround 1 tile
    surround = 0
    surround += coordinateGrid[y-1,x-1]
    surround += coordinateGrid[y-1,x]
    surround += coordinateGrid[y,x-1]
    if y != len(coordinateGrid)-1:
        surround += coordinateGrid[y+1,x-1]
        surround += coordinateGrid[y+1,x]
    else:
        surround += coordinateGrid[0,x-1]
        surround += coordinateGrid[0,x]
    if x != len(coordinateGrid[y])-1:
        if y != len(coordinateGrid)-1:
            surround += coordinateGrid[y+1,x+1]
        else: #Loops around if on edge
            surround += coordinateGrid[0,x+1]
        surround += coordinateGrid[y-1,x+1]
        surround += coordinateGrid[y,x+1]
    else:
        if y != len(coordinateGrid)-1:
            surround += coordinateGrid[y+1,0]
        else: #Loops around if on edge
            surround += coordinateGrid[0,0]
        surround += coordinateGrid[y-1,0]
        surround += coordinateGrid[y,0]
    return surround

def renderTiles(offsetX, offsetY):
    for x in range(0-int(offsetX*tileSize), SCREEN_WIDTH+abs(int(offsetX*tileSize)), tileSize):
        for y in range(0-int(offsetY*tileSize), SCREEN_HEIGHT+abs(int(offsetY*tileSize)), tileSize):
            x_coord = int(x/tileSize)
            y_coord = int(y/tileSize)
            rect = pygame.Rect(x+round(offsetX)*tileSize, y+math.floor(offsetY)*tileSize, tileSize, tileSize)
            if getValue(x_coord+gridOffset[0], y_coord+gridOffset[1]) == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, GREY, rect, 1)

def Init(): 
    global coordinateGrid
    print("Initializing...")
    for y in range(gridSize):
        baseRow = []
        for x in range(gridSize):
            baseRow.append(0)
        coordinateGrid.append(baseRow)
    coordinateGrid = np.array(coordinateGrid)

def getValue(x, y):
    realX = x%gridSize
    realY = y%gridSize
    alive = coordinateGrid[realY,realX]
    return alive

def setValue(x, y, value):
    realX = x%gridSize
    realY = y%gridSize
    coordinateGrid[realY,realX] = value

def Update():
    global frame
    global paused
    global sliderBack
    global sliderOutline
    global slider
    if paused:
        pause1 = pygame.Rect(SCREEN_WIDTH-equivilant10px*5, equivilant10px*3, equivilant10px*2, equivilant10px*6)
        pause2 = pygame.Rect(SCREEN_WIDTH-equivilant10px*8, equivilant10px*3, equivilant10px*2, equivilant10px*6)
        pygame.draw.rect(screen, DARK_GREY, pause1)
        pygame.draw.rect(screen, DARK_GREY, pause2)
    sliderBack = pygame.Rect(SCREEN_WIDTH-equivilant10px*26, SCREEN_HEIGHT-equivilant10px*4, equivilant10px*22, equivilant10px*2)
    sliderOutline = pygame.Rect((SCREEN_WIDTH-equivilant10px*26)-2, (SCREEN_HEIGHT-equivilant10px*4)-2, (equivilant10px*22)+4, (equivilant10px*2)+4)
    slider = pygame.Rect(sliderPos, (SCREEN_HEIGHT-equivilant10px*4)+1, (equivilant10px*2)-2, (equivilant10px*2)-2)
    pygame.draw.rect(screen, WHITE, sliderBack)
    pygame.draw.rect(screen, DARK_GREY, sliderOutline, 2)
    pygame.draw.rect(screen, DARK_GREY, slider)
    pygame.display.flip()

def main():
    global tileSize
    global screen
    global clock
    global frame
    global paused
    global speed
    global sliderPos
    print("Starting...")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Conway's Game of Life")
    clock = pygame.time.Clock()
    Init()
    surroundInit()
    sliderMove = False
    sliderPos = round(equivilant10px*3.3)+SCREEN_WIDTH-equivilant10px*26
    speed = 2
    while True:
        #Frame counter -->
        frame += 1
        #Get events -->
        if sliderMove:
            mousePos = pygame.mouse.get_pos()
            if mousePos[0] > SCREEN_WIDTH-equivilant10px*25 and mousePos[0] < SCREEN_WIDTH-equivilant10px*5:
                sliderPos = mousePos[0]-equivilant10px
                speed = ((mousePos[0]-(SCREEN_WIDTH-equivilant10px*25))/(equivilant10px*3.33))
            elif mousePos[0] > SCREEN_WIDTH-equivilant10px*25:
                sliderPos = SCREEN_WIDTH-equivilant10px*6
                speed = ((sliderPos-(SCREEN_WIDTH-equivilant10px*26))/(equivilant10px*3.33))
            elif mousePos[0] < SCREEN_WIDTH-equivilant10px*5:
                sliderPos = (SCREEN_WIDTH-equivilant10px*26)+1
                speed = ((sliderPos-(SCREEN_WIDTH-equivilant10px*26))/(equivilant10px*3.33))
        
        for event in pygame.event.get():
            #Get key events -->
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Exiting...")
                    sys.exit()
                #Toggle pause -->
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                 #Move left
                elif event.key == pygame.K_LEFT:
                    for x in range(int(1.8*tilesX())):
                        screen.fill(WHITE)
                        renderTiles(x/1.8, 0)
                        Update()
                        clock.tick(1.8*tilesX())
                    gridOffset[0] -= tilesX()
                #Move right
                elif event.key == pygame.K_RIGHT:
                    for x in range(int(1.8*tilesX())):
                        screen.fill(WHITE)
                        renderTiles(x/-1.8, 0)
                        Update()
                        clock.tick(1.8*tilesX())
                    gridOffset[0] += tilesX()
                #Move down
                elif event.key == pygame.K_DOWN:
                    for y in range(int(1.8*tilesY())):
                        screen.fill(WHITE)
                        renderTiles(0, y/-1.8)
                        Update()
                        clock.tick(1.8*tilesY())
                    gridOffset[1] += tilesY()
                #Move up
                elif event.key == pygame.K_UP:
                    for y in range(int(1.8*tilesY())):
                        screen.fill(WHITE)
                        renderTiles(0, y/1.8)
                        Update()
                        clock.tick(1.8*tilesY())
                    gridOffset[1] -= tilesY()
            #Toggle squares -->
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousePos = pygame.mouse.get_pos() # get the mouse posistion
                    if sliderBack.collidepoint(mousePos):
                        sliderMove = True
                    else:
                        if paused:
                            mouse_x, mouse_y = event.pos
                            mouseXCoord = math.floor(mouse_x/tileSize)
                            mouseYCoord = math.floor(mouse_y/tileSize)
                            setValue(mouseXCoord+gridOffset[0], mouseYCoord+gridOffset[1], 1 - getValue(mouseXCoord+gridOffset[0], mouseYCoord+gridOffset[1]))
            
            elif event.type == pygame.MOUSEBUTTONUP:
                sliderMove = False
            #Zoom -->
            elif event.type == pygame.MOUSEWHEEL:
                global scroll
                if scroll < 15 and event.y == -1:
                    scroll -= event.y
                    gridOffset[0] -= round(tilesX()/20)
                    gridOffset[1] -= round(tilesY()/20)
                if scroll > -5 and event.y == 1:
                    scroll -= event.y
                    gridOffset[0] += round(tilesX()/20)
                    gridOffset[1] += round(tilesY()/20)
                tileSize = round(SCREEN_HEIGHT/(21.6*((scroll+10)/10)))
        if not paused and frame%round(FPS/speed) == 0:
            nextGen()
        #Render next frame -->
        screen.fill(WHITE)
        renderTiles(0, 0)
        Update()
        clock.tick(FPS)
main()
