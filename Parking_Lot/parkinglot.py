'''
Parking lot
==============
There should be composition realtionship because 1, 2, 3, 4 can't exist without PL

1. Entrances
2. Exits
3. Global Displays
4. Parking spots
    1. Mini - Bike
    2. Compact - Cars
    3. Large - Trucks
System
==============
1. Generate Ticktes
2. Updating Display Board
3. Manage Payments
4. Handle Parking Strategies

Admin
===============
1. Add/ Remove Entrances and Exits

Parking Attendant
=================
1. Create Parking Ticket

================CLASS DIAGRAM================
ParkingLot
===========
name;
List<EntrancePanel> entrances;
List<ExitPanel> exits;
DisplayBoard displayboard;
x List<ParkingSpot> parkingspot;
x Map <ParkingSpotEnum, List<ParkingSpot>> parkingspots;
Map <ParkingSpotEnum, List<ParkingSpot>> freeParkingspots;
Map <ParkingSpotEnum, List<ParkingSpot>> occupiedParkingspots;
Composition realtionship
----------------------------
EntrancePanel
-------------
name
-----------------------------
ExitPanel
-------------
name
----------------------------
ParkingSpot
1. ENUM : Can violate Open closed principal. How? we'll have if else statements liek if compact do this and so on
if we add one more type then we will modify the class 
2. Abstract Classes: Here if new parking spot comes in we just extend the parking spot abstract class we
wont be changing the class logic. like the abst class will have cost(), and the extended classes will have its own implementations
abstract ParkingSpot
--------------------
int id;
int floorNum;
int amount;
boolean isFree;

CompactParkingSpot extends ParkingSpot;
MiniParkingSpot extends ParkingSpot;
LargeParkingSpot extends ParkingSpot;
--------------------------------------

DisplayBoard
--------------
Redundant these 3
x int freeCompactSpots
x int freeMiniSpots
x int largeSpots
instead do this
Map <ParkingSpotEnum, int> freeParkingSpots
--------------------------------------

Vehicle
---------
int id;
ParkingSpotEnum supportedParkingSpot;
------------
Car extends Vehicle;
MotorBike extends Vehicle;
Truck extends Vehicle;
-----------------------------------------
ParkingTicket
=============
String id;
Vehicle vehicle;
ParkingSpot parkingSpot;
LocalDateTime timestamp;
--------------------------------------
Account
==============
string name;
string email;
string password;

Admin extends Account
===============
ParkingLot parkinglot;
------------------------------------
ParkingAttendant extends Account
===============
ParkingService parkingservice;

ParkingSpotService
=======================
Mini, Compact, Large create--ParkingSpot(int floorName);
this will be a redundant code
How to improve?
ParkingSpot create(ParkingSPotEnum parkingSPotEnum, int floorNum){}
we can check if it is a compact and create a CompactParkingSPot class
if enum is compact we create that type of class what if we have a mapper that if we have this enum type give me object of that class

ParkingSpotEnum
========================
Compact(Compact.class)
Mini(Mini.Class)
Large(Large.class)
public Class getParkingSpot()

DisplayService implements Observer
===========================
DisplayBoard displayboard;
x changeMiniSPot(int change);
x changeCompactSPot(int change);
x changeLargeSPot(int change);

here also redundant code so use the previous ENUM

x change(ParkingSpotEnum parkingSpotEnum, int change){
    freeSpotsupdate(parkingSpotEnum);
}
public void update(ParkingEvent event){}

If 5 vehicles enter this service will be called 5 times so we should make it Singleton

PaymentService
=============================
void acceptCash(amount);
void acceptCreditCard(CardNum, cvv, amount);
---------------------------------------------
abstract PaymentMethod
=====================
abstract boolean intiatePayemnet(int amount)
------------------------
Cash extends PaymentMethod;
CreditCard extends PaymentMethod;
---------------------------------------------
ParkingService -> make it singleton whenever entry exit happen changes made to same PL
========================
ParkingLot parkinglot;
ParkingTicket entry (Vehicle vehicle);
void exit (ParkingTicket parkingTicket, Vehicle vehicle)
List<Observer> observers;

public void addObserver(Observer observer);
public void notifyAllObservers(ParkingEvent parkingEvent);
x ParkingTicket nearestFirstEntry(Vehicle vehicle)
x ParkingTicket farthestFirstEntry(Vehicle vehicle)
--------------------------------------------------
if another strategy comes in we will violate open/closed principle
these strategies are decided at runtime so we'll use Strategy Design Pattern here

Interface Strategy
-------------------------
findParkingSpot(ParkingSpotEnum parkingSpotEnum)
----------------------------------
1. NearestFirstStrategy implements Strategy -> intsnce of ParkingLot
2. FarthestFirstSTrategy implements Strategy -> intsnce of ParkingLot

If I have to find Nearst PS of type Mini
- iterate over the parking spots available and find - O(n)
- optimized : separate list of mini, compact, large map of these-> O(n / 3)
- further optimization: Store the sorted list (Nearest spot-> first ele in list, farthest spot -> last ele in list)- O(1)
- but if the first PS is occupied and second one also it brings back the complexity to O(n)
- to solve this we can maintain the list of occupied ps amd free ps separately

Entry                           |           Exit
- Strategy & Vehicle            | - Validation
- Issue Parking Ticket          | - Payment
- Changing Display board        | - Change on displayBoard
------------------------------------------------
Figuring out which type of Parking Spot we want?

Bike -> Mini, Car -> Compact
There is no vehicle to spot mapping we dont want to use switch statment
- add ParkingSpotEnum in the Vehicle class
------------------------------------------------
Observer Design Pattern
========================
Entry - log , update display service
Exit - log, update display service
these are observer of parking service
List of observer, pass event to these observers and these will update themselves (displayservice)

ENUM ParkingEventType
=====================
ENTRY 
EXIT
-------------------------------
ParkingEvent
===========
ParkingEventType
ParkingSpotType
Vehicle

Interface Observer
=================
void update(ParkingEvent event)


'''
'''
# 🅿️ Parking Lot Low-Level Design (LLD)

## Overview
A modular and scalable parking lot system designed using Object-Oriented Design principles and real-world patterns like Strategy, Composition, Singleton, and Factory.

---

## Python Implementation (Single File)

'''
from abc import ABC, abstractmethod
from collections import defaultdict
import uuid
from datetime import datetime

# ENUM Simulation
class ParkingSpotEnum:
    COMPACT = 'COMPACT'
    MINI = 'MINI'
    LARGE = 'LARGE'


# ----------- VEHICLE --------------
class Vehicle(ABC):
    def __init__(self, vehicle_id):
        self.id = vehicle_id

    @abstractmethod
    def get_supported_spot(self):
        pass

class Car(Vehicle):
    def get_supported_spot(self):
        return ParkingSpotEnum.COMPACT

class Motorbike(Vehicle):
    def get_supported_spot(self):
        return ParkingSpotEnum.MINI

class Truck(Vehicle):
    def get_supported_spot(self):
        return ParkingSpotEnum.LARGE


# ----------- PARKING SPOT --------------
class ParkingSpot(ABC):
    def __init__(self, spot_id, floor_num, amount):
        self.id = spot_id
        self.floor_num = floor_num
        self.amount = amount
        self.is_free = True

class CompactParkingSpot(ParkingSpot):
    pass

class MiniParkingSpot(ParkingSpot):
    pass

class LargeParkingSpot(ParkingSpot):
    pass


# ----------- TICKET --------------
class ParkingTicket:
    def __init__(self, vehicle, parking_spot):
        self.id = str(uuid.uuid4())
        self.vehicle = vehicle
        self.parking_spot = parking_spot
        self.timestamp = datetime.now()


# ----------- ACCOUNT --------------
class Account:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class Admin(Account):
    def __init__(self, name, email, password, parking_lot):
        super().__init__(name, email, password)
        self.parking_lot = parking_lot

class ParkingAttendant(Account):
    def __init__(self, name, email, password, parking_service):
        super().__init__(name, email, password)
        self.parking_service = parking_service


# ----------- DISPLAY BOARD --------------
class DisplayBoard:
    def __init__(self):
        self.free_spots = defaultdict(int)

    def change(self, spot_type, delta):
        self.free_spots[spot_type] += delta


# ----------- PAYMENT STRATEGY --------------
class PaymentMethod(ABC):
    @abstractmethod
    def initiate_payment(self, amount):
        pass

class Cash(PaymentMethod):
    def initiate_payment(self, amount):
        return True

class CreditCard(PaymentMethod):
    def initiate_payment(self, amount):
        return True


# ----------- STRATEGY PATTERN --------------
class ParkingStrategy(ABC):
    @abstractmethod
    def find_parking_spot(self, spot_type):
        pass

class NearestFirstStrategy(ParkingStrategy):
    def __init__(self, parking_lot):
        self.parking_lot = parking_lot

    def find_parking_spot(self, spot_type):
        for spot in self.parking_lot.free_parking_spots[spot_type]:
            if spot.is_free:
                return spot
        return None


# ----------- SERVICES --------------
class ParkingSpotService:
    @staticmethod
    def create(spot_enum, spot_id, floor_num, amount):
        if spot_enum == ParkingSpotEnum.COMPACT:
            return CompactParkingSpot(spot_id, floor_num, amount)
        elif spot_enum == ParkingSpotEnum.MINI:
            return MiniParkingSpot(spot_id, floor_num, amount)
        elif spot_enum == ParkingSpotEnum.LARGE:
            return LargeParkingSpot(spot_id, floor_num, amount)


class ParkingService:
    def __init__(self, parking_lot):
        self.parking_lot = parking_lot
        self.strategy = NearestFirstStrategy(parking_lot)

    def entry(self, vehicle):
        spot_type = vehicle.get_supported_spot()
        spot = self.strategy.find_parking_spot(spot_type)
        if not spot:
            print("No available spot.")
            return None
        spot.is_free = False
        self.parking_lot.display_board.change(spot_type, -1)
        self.parking_lot.occupied_parking_spots[spot_type].append(spot)
        self.parking_lot.free_parking_spots[spot_type].remove(spot)
        return ParkingTicket(vehicle, spot)

    def exit(self, ticket, payment_method):
        if payment_method.initiate_payment(ticket.parking_spot.amount):
            spot_type = ticket.vehicle.get_supported_spot()
            ticket.parking_spot.is_free = True
            self.parking_lot.occupied_parking_spots[spot_type].remove(ticket.parking_spot)
            self.parking_lot.free_parking_spots[spot_type].append(ticket.parking_spot)
            self.parking_lot.display_board.change(spot_type, 1)
            print("Payment successful. Thank you!")


# ----------- PARKING LOT (Composition Root) --------------
class ParkingLot:
    def __init__(self, name):
        self.name = name
        self.entrances = []
        self.exits = []
        self.display_board = DisplayBoard()
        self.free_parking_spots = defaultdict(list)
        self.occupied_parking_spots = defaultdict(list)

    def add_parking_spot(self, spot_enum, spot):
        self.free_parking_spots[spot_enum].append(spot)
        self.display_board.change(spot_enum, 1)

def main():
    # Setup
    lot = ParkingLot("MyLot")
    service = ParkingService(lot)

    # Add spots
    for i in range(2):
        lot.add_parking_spot(ParkingSpotEnum.MINI, ParkingSpotService.create(ParkingSpotEnum.MINI, f"M{i}", 1, 10))
        lot.add_parking_spot(ParkingSpotEnum.COMPACT, ParkingSpotService.create(ParkingSpotEnum.COMPACT, f"C{i}", 1, 20))
        lot.add_parking_spot(ParkingSpotEnum.LARGE, ParkingSpotService.create(ParkingSpotEnum.LARGE, f"L{i}", 1, 30))

    # Vehicle Entry
    bike = Motorbike("Bike001")
    car = Car("Car001")
    truck = Truck("Truck001")

    ticket1 = service.entry(bike)
    ticket2 = service.entry(car)
    ticket3 = service.entry(truck)

    # Vehicle Exit
    service.exit(ticket1, Cash())
    service.exit(ticket2, CreditCard())
    service.exit(ticket3, CreditCard())


if __name__ == "__main__":
    main()

