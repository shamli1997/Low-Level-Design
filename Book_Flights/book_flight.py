'''
========================USE CASE DIAGRAM================
Customer
===========
1. Reserve a Ticket
2. Select Seats
3. Fetch Flights for a date (src, dst)
4. Cancel Reservation

Seats
==========
1. Regular
2. ExtralegRoom
3. EmergencyExit

Admin
=============
1. Add Flights
2. Cancel Flights

System
==============
1. Fetch all the flights
2. Book seat for customer
3. Cancels seat
========================CLASS DIAGRAM================
User
==========
String id;
String name;
String email
System system;
Customer extends User
===========
x String id;
x String name;
x String email;
x System system; instance of system (to book the tickets)

Boolean bookSeat(Flight flight, Seat seat [])
Boolean cancelBooking(Flight flight)
------------------------------------------------------
Admin extends User
=============
x String id;
x String name;
x String email
x System system;
See these are redundant so we'll make a class User and these 2 will extend this class
Why not Interface as User? We use Intreface when we have same function but 2 different classes implementing it differently, 
here things are seperated out they have same data members but different functionality, behaviour is also same, Admin is a User
------------------------------------------------------

System
============
Flight: List<Flight>
fetchFlights (src, dest, date): List<Flight>
bookSeat(Aircraft, Seat): bool
addFlight(Flight flight): bool
cancelFlight(Flight flight): bool
------------------------------------------------------
User
============
System system

Customer extends User
Admin extends User
------------------------------------------------------
Flight
============
Date date;
Aircraft aircarft;
startTime: Time
endTime: Time
source: String
destination: String

cancelForCustomer(Customer customer): bool
------------------------------------------------------
Aircraft
==============
Map<id, Seat>Seats
id:string
bookSeat(Seat, Customer): bool
addSeat(Seat)
------------------------------------------------------
Seat
==============
type: Seat
id: String
customer: Customer

seat belongs to an Aircraft, An aircraft has n number of seats

'''
# ✈️ Flight Booking System - Python (with Design Patterns)

from typing import List, Dict
from datetime import datetime
from enum import Enum

# ------------------ ENUMS ------------------
class SeatType(Enum):
    REGULAR = "Regular"
    EXTRA_LEGROOM = "ExtraLegRoom"
    EMERGENCY_EXIT = "EmergencyExit"

# ------------------ MODELS ------------------
class Seat:
    def __init__(self, seat_id: str, seat_type: SeatType):
        self.seat_id = seat_id
        self.seat_type = seat_type
        self.customer = None  # Assigned when booked

class Aircraft:
    def __init__(self, aircraft_id: str):
        self.aircraft_id = aircraft_id
        self.seats: Dict[str, Seat] = {}

    def add_seat(self, seat: Seat):
        self.seats[seat.seat_id] = seat

    def book_seat(self, seat_id: str, customer):
        seat = self.seats.get(seat_id)
        if seat and seat.customer is None:
            seat.customer = customer
            return True
        return False

class Flight:
    def __init__(self, flight_id: str, date: datetime, aircraft: Aircraft, start_time: str, end_time: str, src: str, dst: str):
        self.flight_id = flight_id
        self.date = date
        self.aircraft = aircraft
        self.start_time = start_time
        self.end_time = end_time
        self.src = src
        self.dst = dst

    def cancel_for_customer(self, customer):
        for seat in self.aircraft.seats.values():
            if seat.customer == customer:
                seat.customer = None
                return True
        return False

# ------------------ SYSTEM ------------------
class FlightSystem:
    def __init__(self):
        self.flights: List[Flight] = []

    def add_flight(self, flight: Flight):
        self.flights.append(flight)
        return True

    def cancel_flight(self, flight: Flight):
        if flight in self.flights:
            self.flights.remove(flight)
            return True
        return False

    def fetch_flights(self, src: str, dst: str, date: datetime):
        return [f for f in self.flights if f.src == src and f.dst == dst and f.date.date() == date.date()]

    def book_seat(self, flight: Flight, seat_id: str, customer):
        return flight.aircraft.book_seat(seat_id, customer)

# ------------------ USERS ------------------
class User:
    def __init__(self, user_id: str, name: str, email: str, system: FlightSystem):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.system = system

class Customer(User):
    def book_seat(self, flight: Flight, seat_id: str):
        return self.system.book_seat(flight, seat_id, self)

    def cancel_booking(self, flight: Flight):
        return flight.cancel_for_customer(self)

class Admin(User):
    def add_flight(self, flight: Flight):
        return self.system.add_flight(flight)

    def cancel_flight(self, flight: Flight):
        return self.system.cancel_flight(flight)

# ------------------ DEMO ------------------
if __name__ == "__main__":
    system = FlightSystem()

    # Admin setup
    admin = Admin("admin1", "Admin", "admin@example.com", system)

    aircraft = Aircraft("A1")
    for i in range(1, 6):
        aircraft.add_seat(Seat(f"S{i}", SeatType.REGULAR))

    flight = Flight("F1001", datetime(2025, 7, 20), aircraft, "10:00", "12:00", "DEL", "BLR")
    admin.add_flight(flight)

    # Customer booking
    customer = Customer("cust1", "John Doe", "john@example.com", system)
    if customer.book_seat(flight, "S1"):
        print("Seat S1 booked successfully!")

    if not customer.book_seat(flight, "S1"):
        print("Seat S1 already booked!")

    if customer.cancel_booking(flight):
        print("Booking cancelled.")

    if customer.book_seat(flight, "S1"):
        print("Seat S1 rebooked successfully!")
