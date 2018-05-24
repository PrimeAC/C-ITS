from time import sleep
import math

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
        #left()
        print("era para a esquerda")
    elif movement == 'right':
        #right()
        print("era para a direita")
  

def virtualToRealMovement(movements, positions):
    #receives two arrays with two positions
    #the first array is [forward/backward, right/left]
    #the second array is [forward/backward number of positions, right/left number of positions] 
    #gets the x axis, if it's forward or backward
    if movements[0] == 'forward': 
        #gets the y axis, if it's left or right
        #forward()
        print("era para a frente")
        decideTurnDirection(movements[1], positions)
    else:
        #backward()
        print("era para tras")
        decideTurnDirection(movements[1], positions)
    sleep(int(convertPositionsToTime(positions)))
    updatePosition(positions, CAR_MAP)


############################# END OF CLIENT MOVEMENT ###################################



############################# START OF SERVER MOVEMENT ###################################

GARAGE_MAP = []


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




'''
myMovements = []
myPositions = []
myMovements.append(input('forward or backward  '))
myMovements.append(input('right or left  '))

myPositions.append(input('forward or backward positions  '))
myPositions.append(input('right or left positions  '))

virtualToRealMovement(myMovements, myPositions)'''

'''
createMap(CAR_MAP)
initializePosition(CAR_MAP)
printMap(CAR_MAP)
print('-------------------------------------------------')
createMap(GARAGE_MAP)
printMap(GARAGE_MAP)

myPositions = []
myPositions.append(input('forward or backward positions  '))
myPositions.append(input('right or left positions  '))
updatePosition(myPositions, CAR_MAP)
printMap(CAR_MAP)
myPositions[0] = 4
updatePosition(myPositions, CAR_MAP)
print('-------------------------------------------------')
printMap(CAR_MAP)
'''

'''
createMap(GARAGE_MAP)
initializePosition(GARAGE_MAP)
printMap(GARAGE_MAP)

path = [[3,0], [6,0], [9,3], [12,6], [15,9]]

decideMovement(path)
printMap(GARAGE_MAP)
printPath(path)
decideMovement(path)
printMap(GARAGE_MAP)
printPath(path)
decideMovement(path)
printMap(GARAGE_MAP)
printPath(path)
decideMovement(path)
printMap(GARAGE_MAP)
decideMovement(path)
printMap(GARAGE_MAP)
decideMovement(path)
printMap(GARAGE_MAP)
decideMovement(path)
printMap(GARAGE_MAP)
'''