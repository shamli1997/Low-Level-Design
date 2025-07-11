# Movie Ticket Booking System - Full Python Code with Optimistic Locking

from enum import Enum
from typing import List, Dict
import threading

# ----------------------------- Enums -----------------------------
class City(Enum):
    BANGALORE = "Bangalore"
    DELHI = "Delhi"

class SeatCategory(Enum):
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"

# ----------------------------- Models -----------------------------
class Movie:
    def __init__(self, movie_id, name, duration_minutes):
        self.movie_id = movie_id
        self.movie_name = name
        self.movie_duration = duration_minutes

class Seat:
    def __init__(self, seat_id, category: SeatCategory):
        self.seat_id = seat_id
        self.seat_category = category

class Screen:
    def __init__(self, screen_id, seats):
        self.screen_id = screen_id
        self.seats = seats  # List of Seat objects

class Show:
    def __init__(self, show_id, movie: Movie, screen: Screen, start_time):
        self.show_id = show_id
        self.movie = movie
        self.screen = screen
        self.start_time = start_time  # e.g., 14 for 2PM
        self.booked_seat_ids = set()
        self.version = 0  # For optimistic locking
        self.lock = threading.Lock()

    def is_seat_available(self, seat_id):
        return seat_id not in self.booked_seat_ids

    def book_seat(self, seat_id):
        with self.lock:
            current_version = self.version
            if not self.is_seat_available(seat_id):
                return False
            # simulate optimistic check
            if current_version != self.version:
                return False
            self.booked_seat_ids.add(seat_id)
            self.version += 1
            return True

class Theatre:
    def __init__(self, theatre_id, city: City, screens: List[Screen], shows: List[Show]):
        self.theatre_id = theatre_id
        self.city = city
        self.screens = screens
        self.shows = shows

# ----------------------------- Controllers -----------------------------
class MovieController:
    def __init__(self):
        self.city_movies: Dict[City, List[Movie]] = {}
        self.all_movies: List[Movie] = []

    def add_movie(self, movie: Movie, city: City):
        self.all_movies.append(movie)
        self.city_movies.setdefault(city, []).append(movie)

    def get_movie_by_name(self, name):
        return next((m for m in self.all_movies if m.movie_name == name), None)

    def get_movies_by_city(self, city: City):
        return self.city_movies.get(city, [])

class TheatreController:
    def __init__(self):
        self.city_theatres: Dict[City, List[Theatre]] = {}
        self.all_theatres: List[Theatre] = []

    def add_theatre(self, theatre: Theatre, city: City):
        self.all_theatres.append(theatre)
        self.city_theatres.setdefault(city, []).append(theatre)

    def get_shows_by_movie_and_city(self, movie: Movie, city: City):
        result = {}
        for theatre in self.city_theatres.get(city, []):
            movie_shows = [show for show in theatre.shows if show.movie.movie_id == movie.movie_id]
            if movie_shows:
                result[theatre] = movie_shows
        return result

# ----------------------------- Booking -----------------------------
class Booking:
    def __init__(self, show: Show, seats: List[Seat]):
        self.show = show
        self.seats = seats

# ----------------------------- Payment -----------------------------
class Payment:
    def __init__(self, payment_id):
        self.payment_id = payment_id

# ----------------------------- BookMyShow Main -----------------------------
class BookMyShow:
    def __init__(self):
        self.movie_controller = MovieController()
        self.theatre_controller = TheatreController()
        self.initialize()

    def initialize(self):
        self.create_movies()
        self.create_theatres()

    def create_movies(self):
        avengers = Movie(1, "AVENGERS", 128)
        baahubali = Movie(2, "BAAHUBALI", 180)

        for city in City:
            self.movie_controller.add_movie(avengers, city)
            self.movie_controller.add_movie(baahubali, city)

    def create_theatres(self):
        avenger = self.movie_controller.get_movie_by_name("AVENGERS")
        baahubali = self.movie_controller.get_movie_by_name("BAAHUBALI")

        inox = Theatre(1, City.BANGALORE, self.create_screens(), [])
        pvr = Theatre(2, City.DELHI, self.create_screens(), [])

        inox.shows.append(self.create_show(1, inox.screens[0], avenger, 8))
        inox.shows.append(self.create_show(2, inox.screens[0], baahubali, 16))

        pvr.shows.append(self.create_show(3, pvr.screens[0], avenger, 13))
        pvr.shows.append(self.create_show(4, pvr.screens[0], baahubali, 20))

        self.theatre_controller.add_theatre(inox, City.BANGALORE)
        self.theatre_controller.add_theatre(pvr, City.DELHI)

    def create_screens(self):
        return [Screen(1, self.create_seats())]

    def create_seats(self):
        seats = []
        for i in range(40):
            seats.append(Seat(i, SeatCategory.SILVER))
        for i in range(40, 70):
            seats.append(Seat(i, SeatCategory.GOLD))
        for i in range(70, 100):
            seats.append(Seat(i, SeatCategory.PLATINUM))
        return seats

    def create_show(self, show_id, screen, movie, time):
        return Show(show_id, movie, screen, time)

    def create_booking(self, city: City, movie_name: str, seat_id: int):
        movies = self.movie_controller.get_movies_by_city(city)
        movie = next((m for m in movies if m.movie_name == movie_name), None)
        if not movie:
            print("Movie not found")
            return

        theatre_shows = self.theatre_controller.get_shows_by_movie_and_city(movie, city)
        if not theatre_shows:
            print("No shows found")
            return

        theatre, shows = next(iter(theatre_shows.items()))
        show = shows[0]

        if show.book_seat(seat_id):
            booked_seat = next(seat for seat in show.screen.seats if seat.seat_id == seat_id)
            booking = Booking(show, [booked_seat])
            print(f"BOOKING SUCCESSFUL: Seat {seat_id} for '{movie_name}' at {theatre.city.value}")
        else:
            print("Seat already booked or version conflict. Try again.")

# ----------------------------- Main Driver -----------------------------
if __name__ == "__main__":
    app = BookMyShow()
    app.create_booking(City.BANGALORE, "BAAHUBALI", 30)
    app.create_booking(City.BANGALORE, "BAAHUBALI", 30)  # should fail (already booked or version conflict)
