"""Tests for the Customer class."""
import os
import tempfile
import unittest

from customer import Customer


class TestCustomer(unittest.TestCase):
    """Test cases for Customer class."""

    def setUp(self):
        """Set up temp file for customer data."""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, "customers.json")
        self._original_data_file = Customer.DATA_FILE
        Customer.DATA_FILE = self.temp_file

    def tearDown(self):
        """Clean up temp files."""
        Customer.DATA_FILE = self._original_data_file
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    # Positive tests

    def test_create_customer(self):
        """Test creating a customer."""
        customer = Customer.create_customer("Rosalina", "Smith", "rosalina@test.com")
        self.assertIsNotNone(customer)
        self.assertEqual(customer.name, "Rosalina")
        self.assertEqual(customer.surname, "Smith")
        self.assertEqual(customer.email, "rosalina@test.com")

    def test_delete_customer(self):
        """Test deleting a customer."""
        Customer.create_customer("Rosalina", "Smith", "rosalina@test.com")
        self.assertTrue(Customer.delete_customer(1))
        self.assertIsNone(Customer.display_customer(1))

    def test_display_customer(self):
        """Test displaying customer info."""
        Customer.create_customer("Rosalina", "Smith", "rosalina@test.com")
        result = Customer.display_customer(1)
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Rosalina")

    def test_modify_customer(self):
        """Test modifying customer attributes."""
        Customer.create_customer("Rosalina", "Smith", "rosalina@test.com")
        result = Customer.modify_customer(1, name="Jana",
                                          surname="Ruiz",
                                          email="jana@test.com")
        self.assertEqual(result["name"], "Jana")
        self.assertEqual(result["surname"], "Ruiz")
        self.assertEqual(result["email"], "jana@test.com")


    # Negative tests

    def test_create_customer_invalid_name(self):
        """Test creating customer with empty name."""
        result = Customer.create_customer("", "Smith", "a@test.com")
        self.assertIsNone(result)

    def test_delete_nonexistent_customer(self):
        """Test deleting a customer that doesn't exist."""
        self.assertFalse(Customer.delete_customer(999))

    def test_display_nonexistent_customer(self):
        """Test displaying a customer that doesn't exist."""
        result = Customer.display_customer(999)
        self.assertIsNone(result)

    def test_modify_nonexistent_customer(self):
        """Test modifying a customer that doesn't exist."""
        result = Customer.modify_customer(999, name="X")
        self.assertIsNone(result)

    def test_load_corrupted_file(self):
        """Test loading a corrupted JSON file."""
        with open(self.temp_file, "w", encoding="utf-8") as f:
            f.write("invalid json")
        customers = Customer._load_customers()
        self.assertEqual(customers, [])


if __name__ == "__main__":
    unittest.main()
