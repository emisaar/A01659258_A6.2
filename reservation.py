"""Reservation module for the reservation system."""
import json
import os

from customer import Customer
from hotel import Hotel


class Reservation:
    """Represents a reservation linking a customer to a hotel."""

    DATA_FILE = "reservations.json"

    def __init__(self, reservation_id, customer_id, hotel_id):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id

    def to_dict(self):
        """Convert reservation to dictionary."""
        return {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
        }

    @classmethod
    def _load_reservations(cls):
        """Load reservations from JSON file."""
        if not os.path.exists(cls.DATA_FILE):
            return []
        try:
            with open(cls.DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    @classmethod
    def _save_reservations(cls, reservations):
        """Save reservations list to JSON file."""
        with open(cls.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(reservations, f, indent=2)

    @classmethod
    def create_reservation(cls, customer_id, hotel_id):
        """Create a reservation after validating customer and hotel."""
        customer = Customer.display_customer(customer_id)
        if not customer:
            return None
        hotel = Hotel.display_hotel(hotel_id)
        if not hotel:
            return None
        Hotel.reserve_room(hotel_id)
        reservations = cls._load_reservations()
        reservation_id = max(
            (r["reservation_id"] for r in reservations), default=0
        ) + 1
        reservation = cls(reservation_id, customer_id, hotel_id)
        reservations.append(reservation.to_dict())
        cls._save_reservations(reservations)
        return reservation

    @classmethod
    def cancel_reservation(cls, reservation_id):
        """Cancel a reservation and free the room."""
        reservations = cls._load_reservations()
        target = None
        for r in reservations:
            if r["reservation_id"] == reservation_id:
                target = r
                break
        if not target:
            return False
        Hotel.cancel_reservation(target["hotel_id"])
        reservations = [
            r for r in reservations
            if r["reservation_id"] != reservation_id
        ]
        cls._save_reservations(reservations)
        return True
