# 📚 Proyecto Final - Editorial Andina S.A.S.

Este proyecto es una aplicación de gestión de autores y libros desarrollada con arquitectura **MVC**, utilizando **Django** como backend y **Tkinter** como frontend, todo en Python.

---

### ⚙️ Requisitos

Instala las dependencias usando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### 🗂️ Estructura del Proyecto

```
Proyecto final/
├── backend/
│   ├── autor/         # CRUD para autores
│   ├── libro/         # CRUD para libros
│   └── editorial/     # Configuración general del proyecto Django
├── frontend/
│   ├── vistas/        # Interfaces gráficas en Tkinter
│   ├── controladores/ # Lógica entre frontend y backend
│   └── modelos/       # Comunicación con la API REST
├── respaldo_autores.txt
├── respaldo_libros.txt
└── requirements.txt
```

---

### 🖥️ Ejecución

1. Ejecuta el servidor Django desde la carpeta `backend`:

```bash
cd backend
python manage.py runserver
```

2. Ejecuta la interfaz gráfica desde la carpeta `frontend`:

```bash
cd ../frontend
python main.py
```

---

### 🔁 Funcionalidades

- **Autores**
  - Crear, consultar, actualizar y eliminar autores.
- **Libros**
  - Crear, consultar, actualizar y eliminar libros.
- **Respaldo automático**
  - Guardado automático de los datos de autores y libros cada minuto en archivos `.txt`.

---

### 🧠 Arquitectura Usada

- **Modelo (Modelos/)**: Gestiona las solicitudes a la API REST.
- **Vista (Vistas/)**: Interfaz gráfica en Tkinter.
- **Controlador (Controladores/)**: Conecta la lógica de la vista con el backend.