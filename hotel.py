"""Hotel module for the reservation system."""
import json
import os


class Hotel:
    """Represents a hotel with rooms that can be reserved."""

    DATA_FILE = "hotels.json"

    def __init__(self, hotel_id, name, location, rooms):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms

    def to_dict(self):
        """Convert hotel to dictionary."""
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "rooms": self.rooms,
        }

    @classmethod
    def _load_hotels(cls):
        """Load hotels from JSON file."""
        if not os.path.exists(cls.DATA_FILE):
            return []
        with open(cls.DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def _save_hotels(cls, hotels):
        """Save hotels list to JSON file."""
        with open(cls.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(hotels, f, indent=2)

    @classmethod
    def create_hotel(cls, name, location, rooms):
        """Create a new hotel and save it."""
        hotels = cls._load_hotels()
        hotel_id = max((h["hotel_id"] for h in hotels), default=0) + 1
        hotel = cls(hotel_id, name, location, rooms)
        hotels.append(hotel.to_dict())
        cls._save_hotels(hotels)
        return hotel

    @classmethod
    def delete_hotel(cls, hotel_id):
        """Delete a hotel by ID."""
        hotels = cls._load_hotels()
        hotels = [h for h in hotels if h["hotel_id"] != hotel_id]
        cls._save_hotels(hotels)
        return True

    @classmethod
    def display_hotel(cls, hotel_id):
        """Display hotel information."""
        hotels = cls._load_hotels()
        for h in hotels:
            if h["hotel_id"] == hotel_id:
                print(f"Hotel: {h['name']}, Location: {h['location']}, "
                      f"Rooms: {h['rooms']}")
                return h
        return None

    @classmethod
    def modify_hotel(cls, hotel_id, **kwargs):
        """Modify hotel attributes."""
        hotels = cls._load_hotels()
        for h in hotels:
            if h["hotel_id"] == hotel_id:
                for key, value in kwargs.items():
                    if key in ("name", "location", "rooms"):
                        h[key] = value
                cls._save_hotels(hotels)
                return h
        return None

    @classmethod
    def reserve_room(cls, hotel_id):
        """Decrement available rooms for a hotel."""
        hotels = cls._load_hotels()
        for h in hotels:
            if h["hotel_id"] == hotel_id:
                h["rooms"] -= 1
                cls._save_hotels(hotels)
                return True
        return False

    @classmethod
    def cancel_reservation(cls, hotel_id):
        """Increment available rooms for a hotel."""
        hotels = cls._load_hotels()
        for h in hotels:
            if h["hotel_id"] == hotel_id:
                h["rooms"] += 1
                cls._save_hotels(hotels)
                return True
        return False
