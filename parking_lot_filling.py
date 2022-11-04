import sys

class ParkingLot():
    def __init__(self, length, width):
        self.length = length
        self.width = width

class Spot():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
class Vehicle():
    def __init__(self, id, length, width):
        self.id = id
        self.length = length
        self.width = width
        self.spot = Spot(0, 0)
        self.prevSpots = []

    def rotate(self):
        return Vehicle(self.id, self.width, self.length)

    def freePrevSpots(self):
        self.prevSpots.clear()

class ParkingLotFilling:
    def __init__(self, parkingLot):
        self.parkingLot = parkingLot
        self.occupiedSpots = []
        self.possibleSpots = [Spot(0, 0)]

    def parkVehicles(self, vehicles):
        remainingVehicles = self.orderByArea(vehicles)
        parkedVehicles = []
        while (remainingVehicles.__len__() > 0):
            currentVehicle = remainingVehicles[-1]
            isBacktrack = True
            for spot in self.possibleSpots:
                isParkable, subVehicleIndex = self.canParkVehicle(currentVehicle, spot) 
                if (isParkable):
                    self.parkVehicle(currentVehicle[subVehicleIndex], spot)
                    parkedVehicles.append([currentVehicle, subVehicleIndex])
                    remainingVehicles.remove(currentVehicle)
                    isBacktrack = False
                    break
            if not parkedVehicles:
                return
            if isBacktrack:
                backtrackVehicle, subVehicleIndex = parkedVehicles.pop()
                remainingVehicles.append(backtrackVehicle)
                remainingVehicles[-2][0].freePrevSpots()
                remainingVehicles[-2][1].freePrevSpots()
                self.updateSpotsAfterBacktrack(remainingVehicles[-1][subVehicleIndex])
            # self.printParkedVehicles(parkedVehicles)
        return parkedVehicles
                

    def orderByArea(self, vehicles):
        return sorted(vehicles, key=lambda x: x[0].width * x[0].length, reverse=False)

    def orderByMaxDimension(self, vehicles):
        return sorted(vehicles, key=lambda x: max(x[0].width, x[0].length), reverse=False)

    def canParkVehicle(self, vehicle, spot):
        subVehicleIndex = 0
        canPark = True
        for subVehicle in vehicle:
            if (spot in subVehicle.prevSpots):
                subVehicleIndex = 1
                continue
            if(spot.x + subVehicle.width > self.parkingLot.width):
                subVehicleIndex = 1
                continue
            if(spot.y + subVehicle.length > self.parkingLot.length):
                subVehicleIndex = 1
                continue
            for occupiedSpot in self.occupiedSpots:
                if(occupiedSpot.x >= spot.x and occupiedSpot.x < spot.x + subVehicle.width and occupiedSpot.y >= spot.y and occupiedSpot.y < spot.y + subVehicle.length):
                    subVehicleIndex = 1
                    canPark = False
                    break
            if not canPark:
                continue
            return True, subVehicleIndex
        return False, None

    def parkVehicle(self, subVehicle, spot):
        subVehicle.spot = spot
        subVehicle.prevSpots.append(Spot(spot.x, spot.y))
        self.updateSpotsAfterPark(subVehicle)

    def updateSpotsAfterPark(self, subVehicle):
        for x in range(subVehicle.width):
            for y in range(subVehicle.length):
                self.occupiedSpots.append(Spot(subVehicle.spot.x + x, subVehicle.spot.y + y))
                if Spot(subVehicle.spot.x + x, subVehicle.spot.y + y) in self.possibleSpots:
                    self.possibleSpots.remove(Spot(subVehicle.spot.x + x, subVehicle.spot.y + y))
        if subVehicle.spot.x + subVehicle.width < self.parkingLot.width:
            self.possibleSpots.append(Spot(subVehicle.spot.x + subVehicle.width, subVehicle.spot.y))
        if subVehicle.spot.y + subVehicle.length < self.parkingLot.length:
            self.possibleSpots.append(Spot(subVehicle.spot.x, subVehicle.spot.y + subVehicle.length))
        self.possibleSpots.sort(key=lambda c: (c.y, c.x))
        
    def updateSpotsAfterBacktrack(self, subVehicle):
        for x in range(subVehicle.width):
            for y in range(subVehicle.length):
                    self.occupiedSpots.remove(Spot(subVehicle.spot.x + x, subVehicle.spot.y + y))
        if Spot(subVehicle.spot.x + subVehicle.width, subVehicle.spot.y) in self.possibleSpots:
            self.possibleSpots.remove(Spot(subVehicle.spot.x + subVehicle.width, subVehicle.spot.y))
        if Spot(subVehicle.spot.x, subVehicle.spot.y + subVehicle.length) in self.possibleSpots:
            self.possibleSpots.remove(Spot(subVehicle.spot.x, subVehicle.spot.y + subVehicle.length))
        self.possibleSpots.append(Spot(subVehicle.spot.x, subVehicle.spot.y))
        self.possibleSpots.sort(key=lambda c: (c.y, c.x))
    
    def printParkedVehicles(self, parkedVehicles):
        outputMatrix = [['__' for x in range(parkingLot.width)] for y in range(parkingLot.length)]

        for parkedVehicle in parkedVehicles:
            subVehicle = parkedVehicle[0][parkedVehicle[1]]
            for x in range(subVehicle.width):
                for y in range(subVehicle.length):
                    outputMatrix[subVehicle.spot.y + y][subVehicle.spot.x + x] = str(subVehicle.id)
        for spot in self.possibleSpots:
            outputMatrix[spot.y][spot.x] = 'o'
        for row in outputMatrix:
            print(row)
        print("\n---------------------------------------------------------------------------\n")
     
        

lines = []
parkingLotParams = input();
parkingLot = ParkingLot(int(parkingLotParams.split('\t')[0]), int(parkingLotParams.split('\t')[1]))
parkingLotFilling = ParkingLotFilling(parkingLot)

numOfVehicles = int(input())
vehicles = []
inputVehicleCounter = 0
for line in sys.stdin:
    inputVehicleCounter += 1
    vehicleParams = line.split('\t')
    vehicle = Vehicle(inputVehicleCounter, int(vehicleParams[0]), int(vehicleParams[1]))
    vehicles.append([vehicle, vehicle.rotate()])
    if inputVehicleCounter == numOfVehicles:
        break

parkedVehicles = parkingLotFilling.parkVehicles(vehicles)

outputMatrix = [['_' for x in range(parkingLot.width)] for y in range(parkingLot.length)]
if not parkedVehicles:
    print("No solution")
else:
    for parkedVehicle in parkedVehicles:
        subVehicle = parkedVehicle[0][parkedVehicle[1]]
        for x in range(subVehicle.width):
            for y in range(subVehicle.length):
                outputMatrix[subVehicle.spot.y + y][subVehicle.spot.x + x] = str(subVehicle.id)
    for row in outputMatrix:
        print("\t".join(row), file=sys.stdout)
