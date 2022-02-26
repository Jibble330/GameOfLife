import pygame, sys, math

#Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
BLACK = (0, 0, 0)
GREY = (120, 120, 120)
FPS = 30

gridSize = 50
screenSize = 200
coordinateGrid = []
surroundGrid = []
frame = 0
squaresX = math.floor(SCREEN_WIDTH/gridSize)
squaresY = math.floor(SCREEN_HEIGHT/gridSize)
gridOffset = [round((screenSize/2)-(squaresX/2)), round((screenSize/2)-(squaresY/2))]

def nextGen(): #Advance to the next generation
    surroundUpdate()
    for y in range(len(coordinateGrid)):
        for x in range(len(coordinateGrid[y])):
            surround = surroundGrid[y][x]
            currentBlock = coordinateGrid[y][x]
            if currentBlock == 0 and surround == 3:
                coordinateGrid[y][x] = 1
            if currentBlock == 1:
                if surround < 2 or surround > 3:
                    coordinateGrid[y][x] = 0

def surroundInit():
    for y in range(len(coordinateGrid)):
        baseInside = []
        for x in range(len(coordinateGrid[y])):
            baseInside.append(0)
        surroundGrid.append(baseInside)
    surroundUpdate()

def surroundUpdate(): #Hugely ineficient way to get surrounding tiles for each tile
    for y in range(len(coordinateGrid)):
        for x in range(len(coordinateGrid[y])):
            surround = getSurrounding(x, y)
            surroundGrid[y][x] = surround

def getSurrounding(x, y): #Get the number of alive tiles arround 1 tile
    surround = 0
    surround += coordinateGrid[y-1][x-1]
    surround += coordinateGrid[y-1][x]
    surround += coordinateGrid[y][x-1]
    if y != len(coordinateGrid)-1:
        surround += coordinateGrid[y+1][x-1]
        surround += coordinateGrid[y+1][x]
    else:
        surround += coordinateGrid[0][x-1]
        surround += coordinateGrid[0][x]
    if x != len(coordinateGrid[y])-1:
        if y != len(coordinateGrid)-1:
            surround += coordinateGrid[y+1][x+1]
        else: #Loops around if on edge
            surround += coordinateGrid[0][x+1]
        surround += coordinateGrid[y-1][x+1]
        surround += coordinateGrid[y][x+1]
    else:
        if y != len(coordinateGrid)-1:
            surround += coordinateGrid[y+1][0]
        else: #Loops around if on edge
            surround += coordinateGrid[0][0]
        surround += coordinateGrid[y-1][0]
        surround += coordinateGrid[y][0]
    return surround

def renderTiles(offsetX, offsetY):
    for x in range(0-int(offsetX*gridSize), SCREEN_WIDTH+abs(int(offsetX*gridSize)), gridSize):
        for y in range(0-int(offsetY*gridSize), SCREEN_HEIGHT+abs(int(offsetY*gridSize)), gridSize):
            x_coord = int(x/gridSize)
            y_coord = int(y/gridSize)
            rect = pygame.Rect(x+math.ceil(offsetX)*gridSize, y+math.floor(offsetY)*gridSize, gridSize, gridSize)
            if getValue(x_coord+gridOffset[0], y_coord+gridOffset[1]) == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, GREY, rect, 1)

def Init(gridSize):
    print("Initializing...")
    for y in range(gridSize):
        baseRow = []
        for x in range(gridSize):
            baseRow.append(0)
        coordinateGrid.append(baseRow)

def getValue(x, y):
    realX = x%screenSize
    realY = y%screenSize
    alive = coordinateGrid[realY][realX]
    return alive

def setValue(x, y, alive):
    realX = x%screenSize
    realY = y%screenSize
    coordinateGrid[realY][realX] = alive

def main():
    paused = True
    Init(screenSize)
    ICON = pygame.image.load('game-of-life.ico')
    pygame.display.set_icon(ICON)
    surroundInit()
    print("Starting...")
    pygame.init()
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    #screen_rect = screen.get_rect()

    pygame.display.set_caption("Conway's Game of Life")

    # - objects -

    # - mainloop -
    global clock
    clock = pygame.time.Clock()

    while True:
        # - events
        global frame
        frame += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_LEFT:
                    for x in range(int(1.5*squaresX)):
                        screen.fill(WHITE)
                        renderTiles(x/1.5, 0)
                        pygame.display.flip()
                        clock.tick(45)
                    gridOffset[0] -= squaresX
                elif event.key == pygame.K_RIGHT:
                    for x in range(int(1.5*squaresX)):
                        screen.fill(WHITE)
                        renderTiles(x/-1.5, 0)
                        pygame.display.flip()
                        clock.tick(45)
                    gridOffset[0] += squaresX
                elif event.key == pygame.K_DOWN:
                    for y in range(int(1.5*squaresY)):
                        screen.fill(WHITE)
                        renderTiles(0, y/-1.5)
                        pygame.display.flip()
                        clock.tick(45)
                    gridOffset[1] += squaresY
                elif event.key == pygame.K_UP:
                    for y in range(int(1.5*squaresY)):
                        screen.fill(WHITE)
                        renderTiles(0, y/1.5)
                        pygame.display.flip()
                        clock.tick(45)
                    gridOffset[1] -= squaresY
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if paused:
                        mouse_x, mouse_y = event.pos
                        mouseXCoord = math.floor(mouse_x/gridSize)
                        mouseYCoord = math.floor(mouse_y/gridSize)
                        setValue(mouseXCoord+gridOffset[0], mouseYCoord+gridOffset[1], 1 - getValue(mouseXCoord+gridOffset[0], mouseYCoord+gridOffset[1]))
        # - updates (without draws) -
        if not paused and frame%7 == 0:
            nextGen()

        screen.fill(WHITE)
        renderTiles(0, 0)
        pygame.display.flip()
        clock.tick(FPS)
main()