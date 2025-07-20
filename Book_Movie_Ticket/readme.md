# 🎬 Movie Ticket Booking System (BookMyShow LLD)

A scalable, thread-safe simulation of a movie booking system in Python, complete with support for cities, theatres, shows, seat categories, and concurrency-safe booking logic (with Optimistic Locking).

---

## 🧠 Problem Statement
Design a system like BookMyShow that supports:
- Multiple cities, movies, theatres, shows, screens
- Tiered seat categories (Silver, Gold, Platinum)
- Real-time booking with thread safety
- Optimistic Locking to avoid overbooking

---

## ✅ Functional Requirements
- Users can book seats for specific shows in a city.
- Seats must not be double-booked.
- Movies and shows are city-specific.

---

## ❌ Non-Functional Requirements
- Highly concurrent seat booking.
- Avoid stale data updates (Optimistic Locking).
- Extensible for new features: payments, UI, etc.

---

## 🧑‍💻 Actors (Use Cases)
| Actor            | Responsibilities                                 |
|------------------|--------------------------------------------------|
| User             | Searches and books seats                        |
| MovieController  | Manages all movie-related data                  |
| TheatreController| Manages theatres and shows                      |
| Booking Service  | Validates seat, performs thread-safe booking    |
| Payment Service  | Placeholder for future payment implementation   |

---

## 🧱 Class Design Notes

### 🎞️ Movie
- `movie_id`, `name`, `duration`
- Maintained centrally by `MovieController`

### 🏟️ Theatre
- Has `screens` and `shows`
- Is city-specific
- Composition relationship with `Show`, `Screen`

### 🖥️ Screen
- Holds a list of `Seat` objects

### 💺 Seat
- `seat_id`, `category` (Silver, Gold, Platinum)
- Not tied to user directly, tied via Show's booked_seat_ids

### 📅 Show
- Contains booked seats, `version` field for optimistic locking
- Uses internal lock (`threading.Lock`) for critical section
- Composition relationship with Movie and Screen

### 🛒 Booking
- Holds Show and list of booked Seats
- Could be extended with payment and user info

---

## 🔐 Optimistic Locking: Why?
- We want to avoid race conditions where two users book the same seat.
- Optimistic Locking assumes minimal conflict and only checks version before commit.

### ✅ How It Works:
- Version number is read before booking.
- Booking only proceeds if version hasn’t changed.
- Version is incremented only after booking is successful.

### ❌ When It Fails:
- Another thread booked in between your read and write → version mismatch.
- Safer and less heavy than Pessimistic Locking (`synchronized` blocks or full locks).

---
### 🤔 Why Not Pessimistic Locking?

- Pessimistic Locking uses a heavy-handed approach by locking the resource until the operation completes.

- It guarantees no concurrent modification but can lead to performance bottlenecks and thread contention.

- In high-read, low-write scenarios (like ticket bookings), Optimistic Locking is preferred for better performance and user experience.

## ⚙️ Flow of Booking (create_booking)
1. Fetch movie by city and name
2. Find matching theatre and show
3. Try to book seat (using optimistic lock)
4. Return Booking confirmation or error

---

## 🧩 Design Patterns Used
| Pattern              | Purpose                                                 |
|----------------------|----------------------------------------------------------|
| Singleton (implicit) | Shared controller objects (MovieController, etc.)       |
| Composition          | Theatres → Screens → Seats; Shows include Movie & Screen|
| Optimistic Locking   | Ensures concurrency-safe booking without lock overhead  |

---

## ✅ SOLID Principles Applied
| Principle   | How it’s followed                                      |
|-------------|--------------------------------------------------------|
| SRP         | Classes do one thing (e.g., MovieController vs TheatreController) |
| OCP         | Add new seat categories, cities, without breaking existing code  |
| LSP         | Not directly used but class hierarchies follow correct substitution |
| ISP         | Clean, minimal interfaces via class methods            |
| DIP         | Controllers depend on Models, not concrete implementations |

---

## 🚀 Future Optimizations
- Integrate Payment and Refund flows
- Add seat pricing per category
- Use Redis or SQL for persistence
- Add retry strategy for version conflict failures
- Add `PessimisticLocking` fallback where contention is very high

---

## 🧪 Sample Run
```python
app = BookMyShow()
app.create_booking(City.BANGALORE, "BAAHUBALI", 30)
app.create_booking(City.BANGALORE, "BAAHUBALI", 30)  # Should fail
```

---

## 📌 Summary for Interviews
- Built core classes first: Movie, Theatre, Screen, Show, Seat
- Used `Composition` to keep logical ownership clear
- Used `Optimistic Locking` in `Show` to prevent overbooking
- Controllers followed clean modular structure
- Followed SOLID + thread-safe practices from ground-up

---

