# 📅 Calendar System (LLD in Python)

A flexible calendar management system supporting event creation, updates, deletions, and multi-user event access. This design follows SOLID principles and uses design patterns like Strategy, Factory, and Composition for flexibility and scalability.

---

## 🧠 Problem Statement
Design a calendar system that supports:
- Creating and updating calendar events
- Managing recurring events (daily, weekly, monthly)
- Sharing events between users
- Searching/filtering events

---

## ✅ Functional Requirements
- Users can create, update, delete calendar events.
- Support for recurring events using strategies.
- Users can view events they are invited to.
- Events can have reminders and descriptions.

---

## ❌ Non-Functional Requirements
- Scalable for multiple users
- Easy to extend with new recurrence types or notification logic
- Clean, modular architecture

---

## 🧑‍💻 Actors (Use Cases)
| Actor    | Responsibilities                            |
|----------|---------------------------------------------|
| User     | Creates, views, edits, deletes events       |
| Calendar | Stores events and interacts with strategies |
| Event    | Represents a calendar event                 |
| Strategy | Determines recurrence logic                 |
| Factory  | Creates recurrence strategy dynamically     |

---

## 🧱 Class Design Notes

### 👤 User
- Holds a user_id and name
- Has its own calendar (composition)

### 🗓️ Calendar
- Composed of multiple events
- Can add, update, delete events
- Can search by date

### 📌 Event
- `event_id`, `title`, `start_time`, `end_time`, `participants`
- Can use a recurrence strategy

### 🔁 RecurrenceStrategy (Interface)
- Implemented by Daily, Weekly, Monthly
- Used for generating next occurrences

### 🏭 RecurrenceFactory
- Returns the correct recurrence strategy
- Allows extensibility for new rules

---

## 🔁 Relationships
| Class A          | ↔️ Relationship | Class B             | Justification                               |
|------------------|----------------|----------------------|----------------------------------------------|
| User             | Composition    | Calendar             | Each user owns a calendar                    |
| Calendar         | Aggregation    | Event                | Events belong to calendar                    |
| Event            | Composition    | RecurrenceStrategy   | Strategy used internally for recurrence      |
| RecurrenceFactory| Uses           | RecurrenceStrategy   | Dynamically returns appropriate strategy     |

---

## 🔐 Design Patterns Used
| Pattern            | Purpose                                                              |
|--------------------|-----------------------------------------------------------------------|
| Strategy           | Handle different recurrence logics via interchangeable strategies    |
| Factory            | Create recurrence strategies based on string identifier              |
| Composition        | Calendar has Events, User has Calendar                               |

---

## ✅ SOLID Principles Applied
| Principle | Application                                                                 |
|-----------|-----------------------------------------------------------------------------|
| SRP       | Each class has a single responsibility (Calendar manages events, Strategy handles recurrence) |
| OCP       | New recurrence strategies can be added without touching existing ones       |
| LSP       | Each strategy can be replaced without breaking the system                  |
| ISP       | Interfaces like `RecurrenceStrategy` are minimal and specific               |
| DIP       | High-level modules depend on abstractions (strategy interface)              |

---

## UML Diagram:

                  +--------------------+
                  |      User          |
                  +--------------------+
                  | - user_id: str     |
                  | - name: str        |
                  | - calendar: Calendar |
                  +--------------------+
                            |
                            | Composition
                            v
                  +--------------------+
                  |     Calendar       |
                  +--------------------+
                  | - user: User       |
                  | - events: List[Event] |
                  +--------------------+
                  | +create_event()    |
                  | +delete_event()    |
                  | +has_conflict()    |
                  | +list_events()     |
                  +--------------------+
                            |
                            | Aggregation
                            v
                  +--------------------+
                  |      Event         |
                  +--------------------+
                  | - title: str       |
                  | - start: datetime  |
                  | - end: datetime    |
                  | - owner: User      |
                  | - participants: [] |
                  | - recurrence: str  |
                  +--------------------+
                  | +add_participant() |
                  | +remove_participant() |
                  +--------------------+
                            |
                            | Composition
                            v
         +----------------------------+
         |   RecurrenceStrategy (ABC) |
         +----------------------------+
         | +get_next_occurrence()     |
         +----------------------------+
                ^           ^
                |           |
      +----------------+ +----------------+
      | DailyRecurrence| | WeeklyRecurrence|
      +----------------+ +----------------+

        +-------------------------+
        |   RecurrenceFactory     |
        +-------------------------+
        | +get_strategy(recurrence:str) |
        +-------------------------+


## 🧪 Sample Run
```python
user = User("u123", "Alice")
calendar = user.calendar

start = datetime.now()
end = start + timedelta(hours=1)
event = Event("e101", "Team Sync", start, end, ["Alice", "Bob"], DailyRecurrence())
calendar.add_event(event)
calendar.list_events()
```

---

## 📌 Summary
- Followed clean OOP architecture: `User → Calendar → Event`
- Used Strategy Pattern to handle recurrence
- Factory provides decoupling for recurrence logic
- System is modular, extensible, and cleanly structured

---
