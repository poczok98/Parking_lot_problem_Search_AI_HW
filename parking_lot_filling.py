import time

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

class Segment():
    def __init__(self, x, y, w):
        self.x = x
        self.y = y
        self.w = w

class ParkingLotFilling:
    def __init__(self, parking_lot):
        self.parking_lot = parking_lot
        self.freeSpots = []
        for x in range(parking_lot.width):
            for y in range(parking_lot.length):
                self.freeSpots.append(Spot(x, y))
        self.freeSpots.sort(key=lambda c: (c.x, c.y))
        self.occupiedSpots = []

    def parkVehicles(self, vehicles):
        remainingVehicles = self.orderByMaxDimension(vehicles)
        parkedVehicles = []
        startTime = time.time_ns() // 1_000_000
        currAlgorithmTime = 0.0
        while (remainingVehicles.__len__() > 0):
            currentVehicle = remainingVehicles[-1]
            isBacktrack = True
            for spot in self.freeSpots:
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
            currAlgorithmTime = time.time_ns() // 1_000_000 - startTime
            self.printParkedVehicles(parkedVehicles)
        
        print("Algorithm time: ", currAlgorithmTime)
        return parkedVehicles
                

    def orderByArea(self, vehicles):
        return sorted(vehicles, key=lambda x: x[0].width * x[0].length, reverse=False)

    def orderByMaxDimension(self, vehicles):
        return sorted(vehicles, key=lambda x: max(x[0].width, x[0].length), reverse=False)

    def canParkVehicle(self, vehicle, spot):
        i = 0
        canPark = True
        for subVehicle in vehicle:
            if (spot in subVehicle.prevSpots):
                i = 1
                continue
            if(spot.x + subVehicle.width > self.parking_lot.width):
                i = 1
                continue
            if(spot.y + subVehicle.length > self.parking_lot.length):
                i = 1
                continue
            for occupiedSpot in self.occupiedSpots:
                if(occupiedSpot.x >= spot.x and occupiedSpot.x < spot.x + subVehicle.width and occupiedSpot.y >= spot.y and occupiedSpot.y < spot.y + subVehicle.length):
                    i = 1
                    canPark = False
                    break
            if not canPark:
                continue
            return True, i
        return False, 0

    def parkVehicle(self, subVehicle, spot):
        subVehicle.spot = spot
        subVehicle.prevSpots.append(Spot(spot.x, spot.y))
        self.updateSpotsAfterPark(subVehicle)

    def updateSpotsAfterPark(self, subVehicle):
        for x in range(subVehicle.width):
            for y in range(subVehicle.length):
                self.freeSpots.remove(Spot(subVehicle.spot.x + x, subVehicle.spot.y + y))
                self.occupiedSpots.append(Spot(subVehicle.spot.x + x, subVehicle.spot.y + y))

        self.freeSpots.sort(key=lambda c: (c.x, c.y))
        
    def updateSpotsAfterBacktrack(self, subVehicle):
        for x in range(subVehicle.width):
            for y in range(subVehicle.length):
                    self.freeSpots.append(Spot(subVehicle.spot.x + x, subVehicle.spot.y + y))
                    self.occupiedSpots.remove(Spot(subVehicle.spot.x + x, subVehicle.spot.y + y))

        self.freeSpots.sort(key=lambda c: (c.x, c.y))
    
    def printParkedVehicles(self, parkedVehicles):
        outputMatrix = [['__' for x in range(parking_lot.width)] for y in range(parking_lot.length)]

        for parkedVehicle in parkedVehicles:
            subVehicle = parkedVehicle[0][parkedVehicle[1]]
            for x in range(subVehicle.width):
                for y in range(subVehicle.length):
                    outputMatrix[subVehicle.spot.y + y][subVehicle.spot.x + x] = str(subVehicle.id)
        for row in outputMatrix:
            print(row)
        print("\n---------------------------------------------------------------------------\n")
     
        

lines = []
with open("sample_input_16_20.txt") as f:
# with open("sample_input_pdf.txt") as f:
    lines = [line.rstrip() for line in f]
f.close()

parking_lot = ParkingLot(int(lines[0].split('\t')[0]), int(lines[0].split('\t')[1]))
parking_lot_filling = ParkingLotFilling(parking_lot)

vehicles = []
numOfVehicles = int(lines[1])
for i in range(2, numOfVehicles+2):
    vehicle = Vehicle(i-1, int(lines[i].split('\t')[0]), int(lines[i].split('\t')[1]))
    vehicles.append([vehicle, vehicle.rotate()])

parkedVehicles = parking_lot_filling.parkVehicles(vehicles)

outputMatrix = [['_' for x in range(parking_lot.width)] for y in range(parking_lot.length)]
if not parkedVehicles:
    print("No solution")
else:
    for parkedVehicle in parkedVehicles:
        subVehicle = parkedVehicle[0][parkedVehicle[1]]
        for x in range(subVehicle.width):
            for y in range(subVehicle.length):
                outputMatrix[subVehicle.spot.y + y][subVehicle.spot.x + x] = str(subVehicle.id)
    # with open("output.txt", "w") as f:
    with open("output_16_20.txt", "w") as f:
        for line in outputMatrix:
            f.write("\t".join(line))
            f.write("\n")
    f.close()
