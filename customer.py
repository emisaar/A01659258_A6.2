"""Customer module for the reservation system."""
import json
import os


class Customer:
    """Represents a customer who can make reservations."""

    DATA_FILE = "customers.json"

    def __init__(self, customer_id, name, surname, email):
        self.customer_id = customer_id
        self.name = name
        self.surname = surname
        self.email = email

    def to_dict(self):
        """Convert customer to dictionary."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
        }

    @classmethod
    def _load_customers(cls):
        """Load customers from JSON file."""
        if not os.path.exists(cls.DATA_FILE):
            return []
        try:
            with open(cls.DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    @classmethod
    def _save_customers(cls, customers):
        """Save customers list to JSON file."""
        with open(cls.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(customers, f, indent=2)

    @classmethod
    def create_customer(cls, name, surname, email):
        """Create a new customer and save it."""
        if not name or not surname or not email:
            print("Error: name, surname and email are required.")
            return None
        customers = cls._load_customers()
        customer_id = max(
            (c["customer_id"] for c in customers), default=0
        ) + 1
        customer = cls(customer_id, name, surname, email)
        customers.append(customer.to_dict())
        cls._save_customers(customers)
        return customer

    @classmethod
    def delete_customer(cls, customer_id):
        """Delete a customer by ID."""
        customers = cls._load_customers()
        original_len = len(customers)
        customers = [
            c for c in customers if c["customer_id"] != customer_id
        ]
        if len(customers) == original_len:
            print(f"Error: Customer {customer_id} not found.")
            return False
        cls._save_customers(customers)
        return True

    @classmethod
    def display_customer(cls, customer_id):
        """Display customer information."""
        customers = cls._load_customers()
        for c in customers:
            if c["customer_id"] == customer_id:
                print(f"Customer: {c['name']} {c['surname']}, "
                      f"Email: {c['email']}")
                return c
        return None

    @classmethod
    def modify_customer(cls, customer_id, **kwargs):
        """Modify customer attributes."""
        customers = cls._load_customers()
        for c in customers:
            if c["customer_id"] == customer_id:
                for key, value in kwargs.items():
                    if key in ("name", "surname", "email"):
                        c[key] = value
                cls._save_customers(customers)
                return c
        return None
