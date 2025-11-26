# API Taller Mecánico

Backend en Django + Django REST Framework + PostgreSQL para gestionar clientes, vehículos,
mecánicos, servicios y órdenes de reparación de un taller mecánico.

## Requisitos

- Python 3.11+
- PostgreSQL 14+
- pip / virtualenv

## Instalación

```bash
git clone <URL_DEL_REPO>
cd taller_mecanico_backend

python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows

pip install -r requirements.txt

# Configura la base de datos en taller_mecanico_api/settings.py

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
