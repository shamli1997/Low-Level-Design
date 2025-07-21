# 📅 Calendar System (LLD in Python)
# Use Cases:
# 1. Users can create/edit/delete events
# 2. Invite users to events
# 3. Events can be recurring
# 4. Check conflicts
# 5. List daily/weekly/monthly agenda

from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# -------------------- Models --------------------
class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name
        self.calendar = Calendar(self)

class Event:
    def __init__(self, title: str, start: datetime, end: datetime, owner: User, recurrence: str = None):
        self.title = title
        self.start = start
        self.end = end
        self.owner = owner
        self.participants = [owner]
        self.recurrence = recurrence  # e.g. "DAILY", "WEEKLY", None

    def add_participant(self, user: User):
        if user not in self.participants:
            self.participants.append(user)

    def remove_participant(self, user: User):
        if user in self.participants:
            self.participants.remove(user)

# -------------------- Calendar --------------------
class Calendar:
    def __init__(self, user: User):
        self.user = user
        self.events = []  # List[Event]

    def create_event(self, event: Event):
        if self.has_conflict(event):
            print("❌ Conflict Detected. Event not added.")
            return False
        self.events.append(event)
        print(f"✅ Event '{event.title}' added to calendar of {self.user.name}")
        return True

    def delete_event(self, event: Event):
        if event in self.events:
            self.events.remove(event)
            print(f"🗑️ Event '{event.title}' deleted from calendar")

    def has_conflict(self, new_event: Event):
        for event in self.events:
            if not (new_event.end <= event.start or new_event.start >= event.end):
                return True
        return False

    def list_events(self, period: str = "DAILY"):
        now = datetime.now()
        if period == "DAILY":
            window_end = now + timedelta(days=1)
        elif period == "WEEKLY":
            window_end = now + timedelta(weeks=1)
        elif period == "MONTHLY":
            window_end = now + timedelta(days=30)
        else:
            print("Unknown period.")
            return

        print(f"\n📅 {period} agenda for {self.user.name}:")
        for event in self.events:
            if now <= event.start <= window_end:
                print(f"- {event.title}: {event.start.strftime('%Y-%m-%d %H:%M')}")

# -------------------- Recurrence Strategy (Decorator-like) --------------------
class RecurrenceStrategy(ABC):
    @abstractmethod
    def get_next_occurrence(self, event: Event):
        pass

class DailyRecurrence(RecurrenceStrategy):
    def get_next_occurrence(self, event: Event):
        return Event(event.title, event.start + timedelta(days=1), event.end + timedelta(days=1), event.owner, event.recurrence)

class WeeklyRecurrence(RecurrenceStrategy):
    def get_next_occurrence(self, event: Event):
        return Event(event.title, event.start + timedelta(weeks=1), event.end + timedelta(weeks=1), event.owner, event.recurrence)

# -------------------- Recurrence Factory --------------------
class RecurrenceFactory:
    def get_strategy(self, recurrence: str):
        if recurrence == "DAILY":
            return DailyRecurrence()
        elif recurrence == "WEEKLY":
            return WeeklyRecurrence()
        else:
            return None

# -------------------- Usage --------------------
if __name__ == "__main__":
    alice = User("U1", "Alice")
    bob = User("U2", "Bob")

    now = datetime.now()
    meeting = Event("Team Sync", now + timedelta(hours=2), now + timedelta(hours=3), alice, recurrence="DAILY")

    alice.calendar.create_event(meeting)
    meeting.add_participant(bob)

    alice.calendar.list_events("DAILY")

    # Add recurring next instance
    strategy = RecurrenceFactory().get_strategy(meeting.recurrence)
    if strategy:
        next_event = strategy.get_next_occurrence(meeting)
        alice.calendar.create_event(next_event)
        alice.calendar.list_events("WEEKLY")
