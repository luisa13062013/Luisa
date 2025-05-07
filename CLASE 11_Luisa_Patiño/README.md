# Proyecto Editorial Andina - Conejos 🐇

Este proyecto contiene una aplicación de escritorio y un backend Django para registrar, buscar, actualizar y eliminar registros de conejos.

## Estructura

- **backend/** → Proyecto Django con modelo Conejo y API CRUD.
- **frontend/** → Interfaz Tkinter conectada al backend.
- **README.md** → Instrucciones de uso.

## Cómo correr

### 1. Backend

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### 2. Frontend

```bash
cd frontend
python app.py
```

Asegúrate de tener el backend corriendo antes de abrir el frontend.

