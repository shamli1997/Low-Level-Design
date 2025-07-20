# 🅿️ Parking Lot System - Low Level Design (LLD)

## 🧠 Problem Understanding
Design a Parking Lot system that handles different vehicle types, entry/exit, real-time display updates, payment, and extensible parking strategies.

---

## ✅ Functional Requirements
- Vehicle enters → assign appropriate spot
- Vehicle exits → calculate fee & mark spot free
- Real-time display of free spots by type
- Support multiple floors and entry/exit panels
- Support different vehicle types: Bike, Car, Truck

---

## 🎭 Actors and Use Cases

| Actor            | Responsibilities                              |
|------------------|-----------------------------------------------|
| Vehicle          | Enters and exits parking lot                  |
| Admin            | Adds/removes panels and spots                 |
| Parking Attendant| Issues ticket                                 |
| Display Board    | Shows live available spot counts              |
| Payment Service  | Handles cash/credit payments                  |

---

## 🔩 Class Design + Relationships

### ✅ ParkingLot (Composition)
- Composition: Contains EntrancePanel, ExitPanel, DisplayBoard, ParkingSpots
- `Map<ParkingSpotEnum, List<ParkingSpot>> freeSpots`
- `Map<ParkingSpotEnum, List<ParkingSpot>> occupiedSpots`

### 🪧 DisplayBoard (Observer)
- Shows current available spots
- `update(event)` method to react to ParkingEvent (ENTRY/EXIT)

### 🚗 Vehicle (Abstract)
- `Car`, `Bike`, `Truck` extend it
- Each has a supported spot type enum

### 🅿️ ParkingSpot (Abstract)
- `CompactSpot`, `MiniSpot`, `LargeSpot`
- Has `id`, `floor`, `isFree`, `amount` (per hour)

### 🎟️ ParkingTicket
- Unique ID
- Vehicle, Spot, Timestamp

### 👨‍🔧 ParkingService (Singleton)
- Main engine of the system
- Handles `entry()`, `exit()`
- Maintains observers

### 💸 PaymentService
- Handles card & cash payments
- Uses `PaymentMethod` interface → OCP safe

### 📊 DisplayService (Observer)
- Updates `DisplayBoard`
- Called by `ParkingService` on entry/exit

### 🧠 Strategy Pattern
Used in `ParkingService` to find spot:
- `NearestFirstStrategy`
- `FarthestFirstStrategy`
- Interface-based → easy to extend

---

## 💡 Design Patterns

| Pattern    | Usage                                              |
|------------|----------------------------------------------------|
| Singleton  | `ParkingService` & `DisplayService`                |
| Strategy   | For selecting best-fit Parking Spot                |
| Observer   | Notify display board on entry/exit                 |

---

## ❗ Design Evolution + Optimizations

### 🛑 Naive:
- `List<ParkingSpot>` → Searching each time is O(n)

### ⚙️ Optimized:
- `Map<ParkingSpotEnum, List<ParkingSpot>>`
- Further:
  - Maintain separate `freeSpots` and `occupiedSpots`
  - Fetch nearest free in O(1) from head of list

---

## 🧱 Class Relationships

| From         | To             | Relationship | Why?                          |
|--------------|----------------|---------------|-------------------------------|
| ParkingLot   | EntrancePanel  | Composition   | Can't exist without lot       |
| ParkingLot   | ParkingSpot    | Composition   | Part of core infra            |
| DisplayBoard | ParkingLot     | Aggregation   | Independent, observable       |
| Vehicle      | ParkingSpotEnum| Aggregation   | Supports flexible mappings    |
| Admin        | ParkingLot     | Aggregation   | External controller           |

---

## 🔐 SOLID Principles

| Principle     | Application                                      |
|---------------|--------------------------------------------------|
| SRP           | Each class has only one responsibility           |
| OCP           | New strategies/vehicle/spot types = extend only |
| LSP           | Polymorphism respected in spot & vehicle classes|
| ISP           | No bloated interfaces                            |
| DIP           | Strategies injected as dependencies              |

---

## 📌 Notes for Interview
- Walk step-by-step: Req → Actors → Class → Relationships → Patterns
- Justify every optimization (time, extensibility, reusability)
- Show thought behind enums vs abstract classes (OCP safe)
- Highlight real-time concerns (observer, singleton)

---

