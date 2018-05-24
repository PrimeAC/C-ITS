from time import sleep
import math
import test_motor

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

def convertPositionsToTime(positions):
    totalPositions = int(positions[0]) + int(positions[1])
    print("calculei que vou andar " + str(totalPositions))
    return TIME_SPENT_TO_MOVE * totalPositions


def decideTurnDirection(movement, positions):
    if movement == 'left':
        test_motor.turn_left()
        print("era para a esquerda")
    elif movement == 'right':
        test_motor.turn_right()
        print("era para a direita")
  

def virtualToRealMovement(direction, turn, positionx, positiony, duration):
    #receives two arrays with two positions
    #the first array is [forward/backward, right/left]
    #the second array is [forward/backward number of positions, right/left number of positions] 
    #gets the x axis, if it's forward or backward
    if direction == 'forward':
        #gets the y axis, if it's left or right
        test_motor.forward()
        print("era para a frente")
        decideTurnDirection(turn, positionx)
    elif direction == 'backward':
        test_motor.backward()
        print("era para tras")
        decideTurnDirection(turn, positiony)
    #sleep(int(convertPositionsToTime(positions)))
    sleep(float(duration))
    test_motor.stop()
    #updatePosition(positiony, CAR_MAP)


############################# END OF CLIENT MOVEMENT ###################################



############################# START OF SERVER MOVEMENT ###################################

GARAGE_MAP = []

PARKING_SPOT_1 = [15,15]
PARKING_SPOT_2 = [30,15]


def assignParkingSpot():
    if GARAGE_MAP[PARKING_SPOT_1[1]][PARKING_SPOT_1[0]] == 0:
        print('lugar 1 livre')
        GARAGE_MAP[PARKING_SPOT_1[1]][PARKING_SPOT_1[0]] = 1
        createPath(PARKING_SPOT_1)
    elif GARAGE_MAP[PARKING_SPOT_2[1]][PARKING_SPOT_2[0]] == 0:
        print('lugar 2 livre')
        GARAGE_MAP[PARKING_SPOT_2[1]][PARKING_SPOT_2[0]] = 1
        createPath(PARKING_SPOT_2)
    else:
        print('sem lugares disponiveis')


def turn(path, highest, parkingSpot):
    print('segundo')
    isFirst = True
    for x in range(0,parkingSpot + 1 ,5):
        if isFirst == False:
            coordinates = []
            coordinates.append(x + highest)
            coordinates.append(x + highest)
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
    elif yDiff < 0:
        print('preciso de virar para a esquerda')
    else:
        print('diff do y e zero')


def decideMovement(path):
    #the x increases from the left to the right
    #the y increases from up to down
    #path is list with all the coordinates from start to end, ex: [[0, 1], [0, 4], ...]
    #movements its the list to send to the car and positions is the number of positions that the client has to travel
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
            movements.append('backwards')
            decideTurn(nextY - currentY)
        elif nextX - currentX > 0:
            #need to move forward
            print('mover para a frente')
            movements.append('forward')
            decideTurn(nextY - currentY)
        print("positions " + str(positions))
        updatePosition(positions, GARAGE_MAP)
        updatePath(path)

############################# END OF CLIENT MOVEMENT ###################################



