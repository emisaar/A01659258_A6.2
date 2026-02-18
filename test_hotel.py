"""Tests for the Hotel class."""
import os
import tempfile
import unittest

from hotel import Hotel


class TestHotel(unittest.TestCase):
    """Test cases for Hotel class."""

    def setUp(self):
        """Set up temp file for hotel data."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "hotels.json")
        self._original_data_file = Hotel.DATA_FILE
        Hotel.DATA_FILE = self.temp_file

    def tearDown(self):
        """Clean up temp files."""
        Hotel.DATA_FILE = self._original_data_file
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    # Positive tests

    def test_create_hotel(self):
        """Test creating a hotel."""
        hotel = Hotel.create_hotel("Emporio", "Acapulco", 100)
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.name, "Emporio")
        self.assertEqual(hotel.location, "Acapulco")
        self.assertEqual(hotel.rooms, 100)

    def test_delete_hotel(self):
        """Test deleting a hotel."""
        Hotel.create_hotel("Emporio", "Acapulco", 100)
        self.assertTrue(Hotel.delete_hotel(1))
        self.assertIsNone(Hotel.display_hotel(1))

    def test_display_hotel(self):
        """Test displaying hotel info."""
        Hotel.create_hotel("Emporio", "Acapulco", 100)
        result = Hotel.display_hotel(1)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Emporio")

    def test_modify_hotel(self):
        """Test modifying hotel attributes."""
        Hotel.create_hotel("Emporio", "Acapulco", 100)
        result = Hotel.modify_hotel(1, name="Updated", rooms=50)
        self.assertEqual(result["name"], "Updated")
        self.assertEqual(result["rooms"], 50)

    def test_reserve_room(self):
        """Test reserving a room."""
        Hotel.create_hotel("Emporio", "Acapulco", 2)
        self.assertTrue(Hotel.reserve_room(1))
        info = Hotel.display_hotel(1)
        self.assertEqual(info["rooms"], 1)

    def test_cancel_reservation(self):
        """Test cancelling a reservation increments rooms."""
        Hotel.create_hotel("Emporio", "Acapulco", 5)
        Hotel.reserve_room(1)
        Hotel.cancel_reservation(1)
        info = Hotel.display_hotel(1)
        self.assertEqual(info["rooms"], 5)

    # Negative tests

    def test_create_hotel_invalid_name(self):
        """Test creating hotel with empty name."""
        result = Hotel.create_hotel("", "Acapulco", 10)
        self.assertIsNone(result)

    def test_delete_nonexistent_hotel(self):
        """Test deleting a hotel that doesn't exist."""
        self.assertFalse(Hotel.delete_hotel(999))

    def test_display_nonexistent_hotel(self):
        """Test displaying a hotel that doesn't exist."""
        result = Hotel.display_hotel(999)
        self.assertIsNone(result)

    def test_modify_nonexistent_hotel(self):
        """Test modifying a hotel that doesn't exist."""
        result = Hotel.modify_hotel(999, name="X")
        self.assertIsNone(result)

    def test_cancel_reservation_nonexistent(self):
        """Test cancelling reservation for nonexistent hotel."""
        self.assertFalse(Hotel.cancel_reservation(999))

    def test_reserve_room_no_availability(self):
        """Test reserving when no rooms available."""
        Hotel.create_hotel("Emporio", "Acapulco", 1)
        Hotel.reserve_room(1)
        self.assertFalse(Hotel.reserve_room(1))

    def test_load_corrupted_file(self):
        """Test loading a corrupted JSON file."""
        with open(self.temp_file, "w", encoding="utf-8") as f:
            f.write("not valid json{{{")
        hotels = Hotel._load_hotels()
        self.assertEqual(hotels, [])


if __name__ == "__main__":
    unittest.main()
