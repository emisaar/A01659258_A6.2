# A01659258_A6.2

Sistema de reservaciones de hotel implementado en Python con persistencia en archivos JSON.

## Estructura

| Archivo | Descripcion |
|---------|-------------|
| `hotel.py` | Clase Hotel - CRUD de hoteles |
| `customer.py` | Clase Customer - CRUD de clientes |
| `reservation.py` | Clase Reservation - Crear y cancelar reservaciones |
| `test_hotel.py` | Tests unitarios para Hotel |
| `test_customer.py` | Tests unitarios para Customer |
| `test_reservation.py` | Tests unitarios para Reservation |
| `generate_results.sh` | Script para generar evidencia de resultados |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install pytest pytest-cov flake8 pylint
```

## Ejecucion

```bash
# Tests
python -m pytest test_hotel.py test_customer.py test_reservation.py -v

# Cobertura
python -m pytest --cov=hotel --cov=customer --cov=reservation --cov-report=term-missing

# Flake8
flake8 hotel.py customer.py reservation.py test_hotel.py test_customer.py test_reservation.py

# Pylint
pylint hotel.py customer.py reservation.py

# Generar resultados
bash generate_results.sh
```
