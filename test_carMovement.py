from time import sleep
import math
#import test_motor

############################# COMMON CODE TO BOTH ######################################

def createMap(mapName):
    for y in range(0, 30):
        line = []
        for x in range(0, 40):
            line.append(0)
        mapName.append(line)


def printMap(mapName):
    for i in mapName:
        print(i)


def initializePosition(mapName):
    mapName[0][0] = 1


def getCurrentPosition(mapName):
    position = []
    for y in range(0, 30):
        for x in range(0, 40):
            if mapName[y][x] == 1:
                position.append(x)
                position.append(y)
                return position


def updatePosition(positions, mapName):
    currentPosition = getCurrentPosition(mapName)
    print(currentPosition)
    currentX = int(currentPosition[0])
    currentY = int(currentPosition[1])
    addingX = int(positions[0])
    addingY = int(positions[1])
    mapName[currentY][currentX] = 0
    mapName[currentY + addingY][currentX + addingX] = 1

########################### COMMON CODE TO BOTH ##########################################


############################# START OF CLIENT MOVEMENT ###################################

#variable that associates one position movement with the time. ex: pass from (0,0) to (0,1)
TIME_SPENT_TO_MOVE = 3

CAR_MAP = []
DROP_OFF_AREA = [0, 0]

def convertPositionsToTime(xVariation):
    return TIME_SPENT_TO_MOVE * int(xVariation)


def decideTurnDirection(movement):
    if movement == 'left':
        #test_motor.turn_left()
        print("era para a esquerda")
    elif movement == 'right':
        #test_motor.turn_right()
        print("era para a direita")
    #else:
        #test_motor.noTurn()

def virtualToRealMovement(direction, turn, xVariation):
    #direction could be forward/backward, and turn could be right/left
    #xVariation number of positions variation 
    #gets the x axis, if it's forward or backward
    if direction == 'forward':
        #gets the y axis, if it's left or right
        #test_motor.forward()
        print("era para a frente")
        decideTurnDirection(turn)
    elif direction == 'backward':
        #test_motor.backward()
        print("era para tras")
        decideTurnDirection(turn)
    sleep(int(convertPositionsToTime(xVariation)))
    test_motor.stop()
    #updatePosition(xVariation, CAR_MAP)


############################# END OF CLIENT MOVEMENT ###################################



############################# START OF SERVER MOVEMENT ###################################

GARAGE_MAP = []


PARKING_SPOTS_STATUS = { 1: "free", 2: "free"}
PARKING_SPOTS_COORDINATES = { 1: [15, 15], 2: [30, 15]}

def getParkingSpotCoordinates(key):
    for coordinates in PARKING_SPOTS_COORDINATES:
        if coordinates == key:
            return PARKING_SPOTS_COORDINATES[coordinates]
    return None


def assignParkingSpot():
    for spot in PARKING_SPOTS_STATUS:
        if PARKING_SPOTS_STATUS[spot] == "free":
            parkingSpot = getParkingSpotCoordinates(spot)
            if parkingSpot != None:
                return parkingSpot
    return None


def calculatePath(initialPoint, finalPoint):
    path = []
    instructions = []
    xDiff = finalPoint[0] - initialPoint[0]
    yDiff = finalPoint[1] - initialPoint[1]
    if xDiff - yDiff > 0:
        #has to go only forward first
        instructions.append(xDiff - yDiff)
        instructions.append(0)
        instructions.append('forward')
        instructions.append('')
        path.append(instructions)
        instructions = []
        instructions.append(xDiff)
        instructions.append(yDiff)
        instructions.append('forward')
        instructions.append('right')
        path.append(instructions)
        return path
    elif xDiff - yDiff == 0:
        #has to go forward and right
        instructions.append(xDiff)
        instructions.append(yDiff)
        instructions.append('forward')
        instructions.append('right')
        path.append(instructions)
        return path
    else:
        return None


def calculateLeavingPath(initialPoint, finalPoint):
    path = []
    instructions = []
    xDiff = finalPoint[0] - initialPoint[0]
    yDiff = finalPoint[1] - initialPoint[1]
    if xDiff - yDiff < 0:
        #has to go only forward first
        instructions.append(initialPoint + (xDiff - yDiff))
        instructions.append(initialPoint + (xDiff - yDiff))
        instructions.append('backward')
        instructions.append('right')
        path.append(instructions)
        instructions = []
        instructions.append(initialPoint + xDiff)
        instructions.append(0)
        instructions.append('backward')
        instructions.append('')
        path.append(instructions)
        return path
    elif xDiff - yDiff == 0:
        #has to go forward and right
        instructions.append(initialPoint + xDiff)
        instructions.append(initialPoint + yDiff)
        instructions.append('backward')
        instructions.append('right')
        path.append(instructions)
        return path
    else:
        return None


def pathFinder(initialPoint):
    #initialPoint is an array with the x and y values, like [0, 0]
    if initialPoint[0] == 0 and initialPoint[1] == 0:
        #means that is parking, because its on the drop off area
        parkingSpot = assignParkingSpot()
        if parkingSpot != None:
            return calculatePath(initialPoint, parkingSpot)
        else:
            return None
    else:
        #means that is leaving
        return calculatePath(initialPoint, DROP_OFF_AREA)






























def turn(path, highest, parkingSpot):
    print('segundo')
    isFirst = True
    for x in range(0,parkingSpot + 1 ,5):
        if isFirst == False:
            coordinates = []
            coordinates.append(x + highest)
            coordinates.append(x)
            path.append(coordinates)
            print(path)
        else:
            isFirst = False
    return path
        

def createPath(parkingSpot):
    #parking spot is the coordinates of de assigned parking spot
    isFirst = True
    path = []
    print(parkingSpot)
    currentPosition = getCurrentPosition(GARAGE_MAP)
    xDiff = parkingSpot[0] - currentPosition[0]
    yDiff = parkingSpot[1] - currentPosition[1]
    if xDiff - yDiff > 0:
        print('entrei')
        for x in range(0,(xDiff - yDiff)+1,5):
            print('entrei for')
            #will send the car move forward until xDiff = yDiff
            if isFirst == False:
                coordinates = []
                coordinates.append(x)
                coordinates.append(0)
                path.append(coordinates)
                print(path)
                print(x == (xDiff - yDiff))
                if x == (xDiff - yDiff):
                    path = turn(path, x, parkingSpot[1])
            else:
                isFirst = False
    elif xDiff - yDiff == 0:
        #needs to turn
        path = turn(path, 0, parkingSpot[1])


def updatePath(path):
    if len(path) > 0:        
        del path[0]


def printPath(path):
    for coordinates in path:
        print(coordinates) 


def decideTurn(yDiff):
    if yDiff > 0:
        print('preciso de virar para a direita')
        return 'right'
    elif yDiff < 0:
        print('preciso de virar para a esquerda')
        return 'left'
    else:
        print('diff do y e zero')
        return ''


def decideMovement(path):
    #the x increases from the left to the right
    #the y increases from up to down
    #path is list with all the coordinates from start to end, ex: [[0, 1], [0, 4], ...]
    #movements is the list to send to the car and positions is the number of positions that the client has to travel
    if len(path) > 0:
        movements = []
        positions = []
        currentPosition = getCurrentPosition(GARAGE_MAP)
        print("minha posicao atual " + str(currentPosition))
        currentX = currentPosition[0]
        currentY = currentPosition[1]
        nextX = path[0][0]
        nextY = path[0][1]
        positions.append(int(math.fabs(nextX - currentX)))
        positions.append(int(math.fabs(nextY - currentY)))
        if nextX - currentX < 0:
            #need to move backwards
            print('mover para tras')
            movements.append('backward')
            movements.append(decideTurn(nextY - currentY))
        elif nextX - currentX > 0:
            #need to move forward
            print('mover para a frente')
            movements.append('forward')
            movements.append(decideTurn(nextY - currentY))
        print("positions " + str(positions))
        updatePosition(positions, GARAGE_MAP)
        updatePath(path)
    else:
        print('path esta vazio')

############################# END OF SERVER MOVEMENT ###################################

