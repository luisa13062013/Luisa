# Proyecto Final

Este es un proyecto en Django + Django REST Framework que implementa una API REST para la gestión de **autores** y **libros**, usando arquitectura **Modelo - Vista - Controlador (MVC/MDC)** y buenas prácticas de separación por apps.

---

## 📁 Estructura del proyecto

```
PROYECTO_LUISA/
├── backend/
│   ├── api/
│   │   ├── urls.py             # Ruteo global para ViewSets
│   ├── autores/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── libros/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── settings.py
│   └── urls.py                 # URL general del proyecto
├── db.sqlite3
├── manage.py
└── frontend/ (opcional)
```

---

## 🚀 Instalación

1. **Clona el proyecto o descomprime el ZIP**

```bash
cd PROYECTO_LUISA
```

2. **Crea un entorno virtual** (opcional pero recomendado)

```bash
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate
```

3. **Instala dependencias**

```bash
pip install -r requirements.txt
```

4. **Aplica migraciones**

```bash
python manage.py migrate
```

5. **Corre el servidor**

```bash
python manage.py runserver
```

Abre tu navegador en `http://127.0.0.1:8000/api/autores/` o `http://127.0.0.1:8000/api/libros/`

---

## 🧪 Endpoints disponibles

* `GET /api/autores/` → Lista todos los autores
* `POST /api/autores/` → Crea un autor
* `GET /api/libros/` → Lista todos los libros
* `POST /api/libros/` → Crea un libro

Usa herramientas como **Postman** o el navegador para hacer pruebas.

---

## ⚙️ Tecnologías usadas

* Python 3.x
* Django 5.x
* Django REST Framework

---

## 📌 Notas importantes

* Sigue arquitectura limpia por apps (MVC)
* Los modelos, vistas, y serializadores están separados para `autores` y `libros`
* Puedes agregar autenticación si lo deseas
* El proyecto es para fines educativos

---

## 👨‍💻 Autor

Luisa Patiño

---
