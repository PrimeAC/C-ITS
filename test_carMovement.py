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



