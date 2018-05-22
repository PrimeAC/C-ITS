from time import sleep


#variable that associates one position movement with the time. ex: pass from (0,0) to (0,1)
TIME_SPENT_TO_MOVE = 3

GARAGE_MAP = []

CURRENT_X_POSITION = 0
CURRENT_Y_POSITION = 0

def createMap():
    for y in range(0, 30):
        line = []
        for x in range(0, 40):
            line.append(0)
        GARAGE_MAP.append(line)


def printMap():
    for i in GARAGE_MAP:
        print(i)

def initializePosition():
    GARAGE_MAP[0][0] = 1

def getCurrentPosition():
    position = []
    for y in range(0, 30):
        for x in range(0, 40):
            if GARAGE_MAP[y][x] == 1:
                GARAGE_MAP[y][x] = 0
                position.append(x)
                position.append(y)
                return position


def updatePosition(positions):
    currentPosition = getCurrentPosition()
    currentX = int(currentPosition[0])
    currentY = int(currentPosition[1])
    addingX = int(positions[0])
    addingY = int(positions[1])
    GARAGE_MAP[currentY + addingY][currentX + addingX] = 1



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
    sleep(int(convertPositionsToTime(positions)))
  

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

'''
myMovements = []
myPositions = []
myMovements.append(input('forward or backward  '))
myMovements.append(input('right or left  '))

myPositions.append(input('forward or backward positions  '))
myPositions.append(input('right or left positions  '))

virtualToRealMovement(myMovements, myPositions)'''


createMap()
initializePosition()
printMap()

myPositions = []
myPositions.append(input('forward or backward positions  '))
myPositions.append(input('right or left positions  '))
updatePosition(myPositions)
printMap()
myPositions[0] = 4
updatePosition(myPositions)