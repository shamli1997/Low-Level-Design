# 🛫 Flight Booking System - Low Level Design (LLD)

Design and implement a simplified, extensible Flight Booking System that models real-world airline reservation functionality, while applying clean OOP, SOLID principles, and Design Patterns.

---

## ✅ Functional Requirements

* Customers can search flights by source, destination, and date.
* Customers can book and cancel tickets.
* Admins can add and cancel flights.
* The system manages aircrafts and their seats.
* Prevent overbooking.

---

## 🎭 Actors (Use Case Diagram)

| Actor        | Responsibilities                              |
| ------------ | --------------------------------------------- |
| **Customer** | Search, reserve, cancel seats                 |
| **Admin**    | Add/remove flights                            |
| **System**   | Store/manage flights, aircraft, booking logic |

---

## 🧱 Class Design

### 👥 User (Abstract)

* Fields: `id`, `name`, `email`, `system`
* Shared superclass for Customer and Admin
* ✅ Use inheritance, not interface (shared data and similar behavior)

### 👤 Customer extends User

* Methods:

  * `bookSeat(flight, seat)`
  * `cancelBooking(flight)`

### 👨‍✈️ Admin extends User

* Methods:

  * `addFlight(flight)`
  * `cancelFlight(flight)`

### 🧠 System

* Manages all flights and booking operations
* Fields: `List<Flight>`
* Methods:

  * `fetchFlights(src, dest, date)`
  * `bookSeat(flight, seat)`
  * `addFlight(flight)`
  * `cancelFlight(flight)`

### ✈️ Flight

* Fields: `date`, `source`, `destination`, `startTime`, `endTime`, `aircraft`
* Methods:

  * `cancelForCustomer(customer)`
* ✅ Composition with Aircraft

### 🛩️ Aircraft

* Fields: `Map<seat_id, Seat>`
* Methods:

  * `bookSeat(seat, customer)`
  * `addSeat(seat)`
* ✅ Aggregation with Seat

### 💺 Seat

* Fields: `id`, `type` (Regular, ExtraLegRoom, EmergencyExit), `customer`

---

## 🔁 Relationships

| Class                 | Relationship | Justification                       |
| --------------------- | ------------ | ----------------------------------- |
| Flight → Aircraft     | Composition  | Flight can't exist without Aircraft |
| Aircraft → Seats      | Aggregation  | Seats reusable/swappable            |
| Customer/Admin → User | Inheritance  | Common structure & behavior         |
| User ↔ System         | Association  | Pass system reference to users      |

---

## 🧠 Design Patterns

| Pattern         | Purpose                                                        |
| --------------- | -------------------------------------------------------------- |
| **Strategy**    | Different booking strategies (e.g., cheapest, front-row first) |
| **Factory**     | For dynamic creation of Seats by type                          |
| **Composition** | Flight contains Aircraft, Aircraft has Seats                   |
| **Singleton**   | Optional: One system instance shared across users              |

---

## 🔧 Optimizations Made

| Iteration | Before                             | Problem      | Optimized To                         |
| --------- | ---------------------------------- | ------------ | ------------------------------------ |
| 1         | List of seats in Aircraft          | Slow lookup  | Map\<seat\_id, Seat>                 |
| 2         | Booking in Flight                  | Violates SRP | Move to Aircraft class               |
| 3         | Duplicate fields in Customer/Admin | Redundant    | Abstract User class                  |
| 4         | Enum if/else logic for seat type   | Breaks OCP   | Used factory/abstract class for Seat |

---

## 📏 SOLID Principles Applied

| Principle | Application                                                      |
| --------- | ---------------------------------------------------------------- |
| SRP       | Clear separation: System for orchestration, Aircraft for booking |
| OCP       | Add new Seat types without modifying logic                       |
| LSP       | Customer/Admin substitutable via User                            |
| ISP       | Role-specific minimal methods                                    |
| DIP       | System logic depends on abstractions                             |

---

## 🔐 Locking Strategy

### ✅ Optimistic Locking

* Read version → update → check version → commit
* Suitable for low contention (like most bookings)

### ❌ Pessimistic Locking

* Locks resource before access
* Safer but higher latency

✅ In this design, optimistic locking is better suited as bookings are less likely to conflict.

---

## 🧪 Sample Flow

```python
# Customer books a seat
customer.bookSeat(flight, seat)

# Admin adds a new flight
admin.system.addFlight(flight)
```

---

## 📌 Summary for Interviews

* Started with use case → actors → class diagrams
* Focused on **composition** (Flight → Aircraft → Seats)
* Applied **Strategy Pattern** for flexible booking rules
* Used **Factory** to abstract seat creation
* Designed for **scalability** and **extensibility**
* Clean application of all **SOLID** principles
* Explained **optimistic vs. pessimistic** locking trade-offs

---

> “Think in abstractions. Design in composition. Code with intention.”

---
