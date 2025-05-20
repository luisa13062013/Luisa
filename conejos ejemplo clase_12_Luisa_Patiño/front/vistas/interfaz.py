import tkinter as tk
from tkinter import ttk, messagebox
from modelos.conejo import Conejo

class InterfazConejos:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Gestión de Conejos")
        self.ventana.geometry("800x800")
        self.ventana.configure(bg="#ffe6f0")

        self.conejos = {}
        self.contador_id = 1

        self.entradas = {}
        campos = ["ID", "Nombre", "Raza", "Color", "Edad"]

        for i, campo in enumerate(campos):
            lbl = tk.Label(self.ventana, text=campo, bg="#ffe6f0", fg="black", font=("Arial", 12, "bold"))
            lbl.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            entrada = tk.Entry(self.ventana, font=("Arial", 12))
            entrada.grid(row=i, column=1, padx=10, pady=5)
            self.entradas[campo] = entrada

        botones = [
            ("Registrar", self.registrar_conejo),
            ("Consultar por ID", self.consultar_por_id),
            ("Consultar todos", self.consultar_todos),
            ("Actualizar", self.actualizar_conejo),
            ("Eliminar", self.eliminar_conejo),
            ("Limpiar", self.limpiar_campos)
        ]

        for i, (texto, funcion) in enumerate(botones):
            btn = tk.Button(self.ventana, text=texto, command=funcion, font=("Arial", 12), bg="#ffb6c1", fg="black")
            btn.grid(row=6 + i, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        columnas = ("ID", "Nombre", "Raza", "Color", "Edad")
        self.tabla = ttk.Treeview(self.ventana, columns=columnas, show="headings", height=15)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor=tk.CENTER)

        self.tabla.grid(row=0, column=2, rowspan=12, padx=10, pady=10, sticky="nsew")

        self.ventana.grid_columnconfigure(2, weight=1)
        self.ventana.grid_rowconfigure(12, weight=1)

        self.ventana.mainloop()

    def registrar_conejo(self):
        try:
            nombre = self.entradas["Nombre"].get()
            raza = self.entradas["Raza"].get()
            color = self.entradas["Color"].get()
            edad = int(self.entradas["Edad"].get())

            conejo = Conejo(nombre, raza, color, edad)
            self.conejos[self.contador_id] = conejo
            self.contador_id += 1

            messagebox.showinfo("Registrado", "Conejo registrado correctamente")
            self.limpiar_campos()
            self.actualizar_tabla()
        except ValueError:
            messagebox.showerror("Error", "Edad inválida")

    def consultar_por_id(self):
        try:
            id_conejo = int(self.entradas["ID"].get())
            conejo = self.conejos.get(id_conejo)
            if conejo:
                self.entradas["Nombre"].delete(0, tk.END)
                self.entradas["Nombre"].insert(0, conejo.nombre)
                self.entradas["Raza"].delete(0, tk.END)
                self.entradas["Raza"].insert(0, conejo.raza)
                self.entradas["Color"].delete(0, tk.END)
                self.entradas["Color"].insert(0, conejo.color)
                self.entradas["Edad"].delete(0, tk.END)
                self.entradas["Edad"].insert(0, conejo.edad)
                self.actualizar_tabla([(id_conejo, conejo)])
            else:
                messagebox.showwarning("No encontrado", "No hay conejo con ese ID")
        except ValueError:
            messagebox.showerror("Error", "ID inválido")

    def consultar_todos(self):
        self.actualizar_tabla()

    def actualizar_conejo(self):
        try:
            id_conejo = int(self.entradas["ID"].get())
            if id_conejo in self.conejos:
                nombre = self.entradas["Nombre"].get()
                raza = self.entradas["Raza"].get()
                color = self.entradas["Color"].get()
                edad = int(self.entradas["Edad"].get())

                self.conejos[id_conejo] = Conejo(nombre, raza, color, edad)
                messagebox.showinfo("Actualizado", "Conejo actualizado correctamente")
                self.actualizar_tabla()
            else:
                messagebox.showwarning("No encontrado", "No existe un conejo con ese ID")
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos")

    def eliminar_conejo(self):
        try:
            id_conejo = int(self.entradas["ID"].get())
            if id_conejo in self.conejos:
                del self.conejos[id_conejo]
                messagebox.showinfo("Eliminado", "Conejo eliminado")
                self.limpiar_campos()
                self.actualizar_tabla()
            else:
                messagebox.showwarning("No encontrado", "ID no existe")
        except ValueError:
            messagebox.showerror("Error", "ID inválido")

    def limpiar_campos(self):
        for campo in self.entradas.values():
            campo.delete(0, tk.END)
        self.actualizar_tabla()

    def actualizar_tabla(self, lista=None):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        if lista is None:
            lista = self.conejos.items()

        for id_c, conejo in lista:
            self.tabla.insert("", "end", values=(
                id_c,
                conejo.nombre,
                conejo.raza,
                conejo.color,
                conejo.edad
            ))
