#!/bin/bash
# Script to generate test results for the Reservation System project.
# Usage: source venv/bin/activate && bash generate_results.sh

OUTPUT_DIR="results"
mkdir -p "$OUTPUT_DIR"

echo "Generating hotel test results..."
{
  echo "========================================="
  echo "Hotel Class - Test Results"
  echo "========================================="
  echo ""
  echo "--- Unit Tests ---"
  python -m pytest test_hotel.py -v 2>&1
  echo ""
  echo "--- Code Coverage ---"
  python -m pytest test_hotel.py --cov=hotel --cov-report=term-missing 2>&1
  echo ""
  echo "--- Flake8 ---"
  flake8 hotel.py test_hotel.py 2>&1 || echo "(no issues found)"
  echo ""
  echo "--- Pylint ---"
  pylint hotel.py 2>&1
} > "$OUTPUT_DIR/hotel_tests.txt"

echo "Generating customer test results..."
{
  echo "========================================="
  echo "Customer Class - Test Results"
  echo "========================================="
  echo ""
  echo "--- Unit Tests ---"
  python -m pytest test_customer.py -v 2>&1
  echo ""
  echo "--- Code Coverage ---"
  python -m pytest test_customer.py --cov=customer --cov-report=term-missing 2>&1
  echo ""
  echo "--- Flake8 ---"
  flake8 customer.py test_customer.py 2>&1 || echo "(no issues found)"
  echo ""
  echo "--- Pylint ---"
  pylint customer.py 2>&1
} > "$OUTPUT_DIR/customer_tests.txt"

echo "Generating reservation test results..."
{
  echo "========================================="
  echo "Reservation Class - Test Results"
  echo "========================================="
  echo ""
  echo "--- Unit Tests ---"
  python -m pytest test_reservation.py -v 2>&1
  echo ""
  echo "--- Code Coverage ---"
  python -m pytest test_reservation.py --cov=reservation --cov-report=term-missing 2>&1
  echo ""
  echo "--- Flake8 ---"
  flake8 hotel.py customer.py reservation.py test_hotel.py test_customer.py test_reservation.py 2>&1 || echo "(no issues found)"
  echo ""
  echo "--- Pylint ---"
  pylint hotel.py customer.py reservation.py 2>&1
} > "$OUTPUT_DIR/reservation_tests.txt"

echo "Done. Results saved in $OUTPUT_DIR/"
