class ParkingLot():
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Vehicle():
    def __init__(self, id, length, width):
        self.id = id
        self.length = length
        self.width = width

    def rotate(self):
        return(Vehicle(self.id, self.width, self.length))

class ParkingLotFilling:
    def __init__(self, parking_lot):
        self.parking_lot = parking_lot

    def fill(self, vehicles):
        for vehicle in vehicles:
            self.parking_lot.park(vehicle)

lines = []
with open("sample_input.txt") as f:
    lines = [line.rstrip() for line in f]

parking_lot = ParkingLot(int(lines[0].split('\t')[0]), int(lines[0].split('\t')[1]))
parking_lot_filling = ParkingLotFilling(parking_lot)

vehicles = []
numOfVehicles = int(lines[1])
print(numOfVehicles)
for i in range(2, numOfVehicles+2):
    vehicle = Vehicle(i-1, int(lines[i].split('\t')[0]), int(lines[i].split('\t')[1]))
    vehicles.append(vehicle)
    vehicles.append(vehicle.rotate())

for vehicle in vehicles:
    print(vehicle.id, vehicle.length, vehicle.width)