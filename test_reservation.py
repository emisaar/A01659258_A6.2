"""Tests for the Reservation class."""
import os
import tempfile
import unittest

from customer import Customer
from hotel import Hotel
from reservation import Reservation


class TestReservation(unittest.TestCase):
    """Test cases for Reservation class."""

    def setUp(self):
        """Set up temp files for all data."""
        self.temp_dir = tempfile.mkdtemp()
        self._orig_hotel = Hotel.DATA_FILE
        self._orig_customer = Customer.DATA_FILE
        self._orig_reservation = Reservation.DATA_FILE
        Hotel.DATA_FILE = os.path.join(self.temp_dir, "hotels.json")
        Customer.DATA_FILE = os.path.join(self.temp_dir, "customers.json")
        Reservation.DATA_FILE = os.path.join(
            self.temp_dir, "reservations.json"
        )

    def tearDown(self):
        """Clean up temp files."""
        Hotel.DATA_FILE = self._orig_hotel
        Customer.DATA_FILE = self._orig_customer
        Reservation.DATA_FILE = self._orig_reservation
        for fname in ("hotels.json", "customers.json", "reservations.json"):
            path = os.path.join(self.temp_dir, fname)
            if os.path.exists(path):
                os.remove(path)

    # Positive tests

    def test_create_reservation(self):
        """Test creating a reservation."""
        Customer.create_customer("Rosalina", "Smith", "rosalina@test.com")
        Hotel.create_hotel("Emporio", "Acapulco", 5)
        res = Reservation.create_reservation(1, 1)
        self.assertIsNotNone(res)
        self.assertEqual(res.customer_id, 1)
        self.assertEqual(res.hotel_id, 1)
        info = Hotel.display_hotel(1)
        self.assertEqual(info["rooms"], 4)

    def test_cancel_reservation(self):
        """Test cancelling a reservation restores the room."""
        Customer.create_customer("Rosalina", "Smith", "rosalina@test.com")
        Hotel.create_hotel("Emporio", "Acapulco", 5)
        Reservation.create_reservation(1, 1)
        self.assertTrue(Reservation.cancel_reservation(1))
        info = Hotel.display_hotel(1)
        self.assertEqual(info["rooms"], 5)

    # Negative tests

    def test_create_reservation_nonexistent_customer(self):
        """Test reservation with nonexistent customer."""
        Hotel.create_hotel("Emporio", "Acapulco", 5)
        result = Reservation.create_reservation(999, 1)
        self.assertIsNone(result)

    def test_cancel_nonexistent_reservation(self):
        """Test cancelling a reservation that doesn't exist."""
        self.assertFalse(Reservation.cancel_reservation(999))

    def test_load_corrupted_file(self):
        """Test loading a corrupted reservations file."""
        with open(Reservation.DATA_FILE, "w", encoding="utf-8") as f:
            f.write("not valid json")
        reservations = Reservation._load_reservations()
        self.assertEqual(reservations, [])


if __name__ == "__main__":
    unittest.main()
