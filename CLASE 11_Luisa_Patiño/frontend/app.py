import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:8000/api/conejos/"

def guardar():
    data = {
        "nombre": nombre_var.get(),
        "raza": raza_var.get(),
        "edad": int(edad_var.get()),
        "color": color_var.get()
    }
    response = requests.post(API_URL, json=data)
    if response.status_code == 201:
        messagebox.showinfo("Éxito", "Conejo guardado exitosamente.")
    else:
        messagebox.showerror("Error", "No se pudo guardar.")

def buscar():
    id = id_var.get()
    response = requests.get(API_URL + f"{id}/")
    if response.status_code == 200:
        conejo = response.json()
        nombre_var.set(conejo["nombre"])
        raza_var.set(conejo["raza"])
        edad_var.set(conejo["edad"])
        color_var.set(conejo["color"])
    else:
        messagebox.showerror("Error", "Conejo no encontrado.")

def actualizar():
    id = id_var.get()
    data = {
        "nombre": nombre_var.get(),
        "raza": raza_var.get(),
        "edad": int(edad_var.get()),
        "color": color_var.get()
    }
    response = requests.put(API_URL + f"{id}/actualizar/", json=data)
    if response.status_code == 200:
        messagebox.showinfo("Éxito", "Conejo actualizado.")
    else:
        messagebox.showerror("Error", "Error al actualizar.")

def eliminar():
    id = id_var.get()
    response = requests.delete(API_URL + f"{id}/eliminar/")
    if response.status_code == 204:
        messagebox.showinfo("Éxito", "Conejo eliminado.")
        nombre_var.set("")
        raza_var.set("")
        edad_var.set("")
        color_var.set("")
    else:
        messagebox.showerror("Error", "No se pudo eliminar.")

app = tk.Tk()
app.title("Gestión de Conejos")

id_var = tk.StringVar()
nombre_var = tk.StringVar()
raza_var = tk.StringVar()
edad_var = tk.StringVar()
color_var = tk.StringVar()

tk.Label(app, text="ID").grid(row=0, column=0)
tk.Entry(app, textvariable=id_var).grid(row=0, column=1)

tk.Label(app, text="Nombre").grid(row=1, column=0)
tk.Entry(app, textvariable=nombre_var).grid(row=1, column=1)

tk.Label(app, text="Raza").grid(row=2, column=0)
tk.Entry(app, textvariable=raza_var).grid(row=2, column=1)

tk.Label(app, text="Edad").grid(row=3, column=0)
tk.Entry(app, textvariable=edad_var).grid(row=3, column=1)

tk.Label(app, text="Color").grid(row=4, column=0)
tk.Entry(app, textvariable=color_var).grid(row=4, column=1)

tk.Button(app, text="Guardar", command=guardar).grid(row=5, column=0)
tk.Button(app, text="Buscar", command=buscar).grid(row=5, column=1)
tk.Button(app, text="Actualizar", command=actualizar).grid(row=6, column=0)
tk.Button(app, text="Eliminar", command=eliminar).grid(row=6, column=1)

app.mainloop()
