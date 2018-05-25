############################# START OF SERVER MOVEMENT ###################################

GARAGE_MAP = []

DROP_OFF_AREA = [0, 0]
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
        return calculateLeavingPath(initialPoint, DROP_OFF_AREA)

############################# END OF SERVER MOVEMENT ###################################
