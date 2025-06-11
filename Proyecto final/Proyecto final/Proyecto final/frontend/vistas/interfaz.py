import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import requests
from controladores.autor_controlador import ComunicacionAutor
from controladores.libro_controlador import ComunicacionLibro
from modelos.autor_modelo import Autor
from modelos.libro_modelo import Libro
from vistas.tabla import Tabla

class Interfaz:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Gestión de Biblioteca")
        self.ventana.geometry("900x600")
        self.ventana.resizable(True, True)

        # URL base de la API
        self.API_URL = 'http://localhost:8000/api'

        # Variable para controlar respaldos automáticos
        self.respaldos_activos = False
        self.hilo_respaldo = None

        # Inicializar controladores
        self.autor_controlador = ComunicacionAutor(self.ventana)
        self.libro_controlador = ComunicacionLibro(self.ventana)

        # Inicializar modelos
        self.autor_modelo = Autor(self.ventana)
        self.libro_modelo = Libro(self.ventana)

        # 🟩 Scroll general
        contenedor_scroll = ttk.Frame(self.ventana)
        contenedor_scroll.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(contenedor_scroll)
        scrollbar = ttk.Scrollbar(contenedor_scroll, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Crear secciones en el frame con scroll
        self.crear_seccion_autores(self.scroll_frame)
        self.crear_seccion_libros(self.scroll_frame)

        # Iniciar respaldos automáticos
        self.iniciar_respaldos_automaticos()

    def crear_seccion_autores(self, parent):
        self.frame_autores = ttk.LabelFrame(parent, text="Autores")
        self.frame_autores.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        frame_form_autor = ttk.LabelFrame(self.frame_autores, text="Datos del Autor", padding=10)
        frame_form_autor.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame_form_autor, text="ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_id_autor = ttk.Entry(frame_form_autor, textvariable=self.autor_modelo.id, width=20)
        self.entry_id_autor.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form_autor, text="Nombre:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form_autor, textvariable=self.autor_modelo.nombre, width=20).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form_autor, text="Edad:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form_autor, textvariable=self.autor_modelo.edad, width=20).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_form_autor, text="Nacionalidad:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form_autor, textvariable=self.autor_modelo.nacionalidad, width=20).grid(row=3, column=1, padx=5, pady=5)

        frame_botones_autor = ttk.Frame(frame_form_autor)
        frame_botones_autor.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(frame_botones_autor, text="Guardar", command=self.guardar_autor).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_autor, text="Actualizar", command=self.actualizar_autor).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_autor, text="Eliminar", command=self.eliminar_autor).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_autor, text="Consultar", command=self.consultar_autor).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_autor, text="Consultar Todos", command=self.consultar_todos_autores).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_autor, text="Limpiar", command=self.limpiar_autor).pack(side=tk.LEFT, padx=5)

        frame_tabla_autor = ttk.LabelFrame(self.frame_autores, text="Lista de Autores", padding=10)
        frame_tabla_autor.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tabla_autores = None
        self.crear_tabla_autores(frame_tabla_autor)

    def crear_seccion_libros(self, parent):
        self.frame_libros = ttk.LabelFrame(parent, text="Libros")
        self.frame_libros.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        frame_form_libro = ttk.LabelFrame(self.frame_libros, text="Datos del Libro", padding=10)
        frame_form_libro.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame_form_libro, text="ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_id_libro = ttk.Entry(frame_form_libro, textvariable=self.libro_modelo.id, width=20)
        self.entry_id_libro.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form_libro, text="Título:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form_libro, textvariable=self.libro_modelo.titulo, width=20).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form_libro, text="Género:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form_libro, textvariable=self.libro_modelo.genero, width=20).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_form_libro, text="Páginas:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form_libro, textvariable=self.libro_modelo.paginas, width=20).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_form_libro, text="Año Publicación:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame_form_libro, textvariable=self.libro_modelo.año_publicacion, width=20).grid(row=1, column=3, padx=5, pady=5)

        frame_botones_libro = ttk.Frame(frame_form_libro)
        frame_botones_libro.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(frame_botones_libro, text="Guardar", command=self.guardar_libro).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_libro, text="Actualizar", command=self.actualizar_libro).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_libro, text="Eliminar", command=self.eliminar_libro).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_libro, text="Consultar", command=self.consultar_libro).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_libro, text="Consultar Todos", command=self.consultar_todos_libros).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones_libro, text="Limpiar", command=self.limpiar_libro).pack(side=tk.LEFT, padx=5)

        frame_tabla_libro = ttk.LabelFrame(self.frame_libros, text="Lista de Libros", padding=10)
        frame_tabla_libro.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.tabla_libros = None
        self.crear_tabla_libros(frame_tabla_libro)

    def crear_tabla_autores(self, parent):
        titulos = ["ID", "Nombre", "Edad", "Nacionalidad"]
        columnas = ["id", "nombre", "edad", "nacionalidad"]
        data = []
        self.tabla_autores = Tabla(parent, titulos, columnas, data)
        self.tabla_autores.tabla.pack(fill=tk.BOTH, expand=True)
        self.tabla_autores.tabla.bind("<<TreeviewSelect>>", self.seleccionar_autor)

    def crear_tabla_libros(self, parent):
        titulos = ["ID", "Título", "Género", "Páginas", "Año Publicación"]
        columnas = ["id", "titulo", "genero", "paginas", "año_publicacion"]
        data = []
        self.tabla_libros = Tabla(parent, titulos, columnas, data)
        self.tabla_libros.tabla.pack(fill=tk.BOTH, expand=True)

        
        # Bind para seleccionar fila
        self.tabla_libros.tabla.bind("<<TreeviewSelect>>", self.seleccionar_libro)
        
    # Métodos para Autores
    def guardar_autor(self):
        try:
            resultado = self.autor_controlador.guardar(
                self.autor_modelo.nombre.get(),
                self.autor_modelo.edad.get(),
                self.autor_modelo.nacionalidad.get()
            )
            if resultado and resultado.status_code == 201:
                messagebox.showinfo("Éxito", "Autor guardado correctamente")
                self.limpiar_autor()
                self.consultar_todos_autores()
            else:
                messagebox.showerror("Error", "Error al guardar el autor")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            
    def actualizar_autor(self):
        try:
            if not self.autor_modelo.id.get():
                messagebox.showwarning("Advertencia", "Debe seleccionar un autor para actualizar")
                return
                
            resultado = self.autor_controlador.actualizar(
                self.autor_modelo.id.get(),
                self.autor_modelo.nombre.get(),
                self.autor_modelo.edad.get(),
                self.autor_modelo.nacionalidad.get()
            )
            if resultado and resultado.status_code == 200:
                messagebox.showinfo("Éxito", "Autor actualizado correctamente")
                self.limpiar_autor()
                self.consultar_todos_autores()
            else:
                messagebox.showerror("Error", "Error al actualizar el autor")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            
    def eliminar_autor(self):
        try:
            if not self.autor_modelo.id.get():
                messagebox.showwarning("Advertencia", "Debe seleccionar un autor para eliminar")
                return
                
            respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este autor?")
            if respuesta:
                resultado = self.autor_controlador.eliminar(self.autor_modelo.id.get())
                if resultado == 204:
                    messagebox.showinfo("Éxito", "Autor eliminado correctamente")
                    self.limpiar_autor()
                    self.consultar_todos_autores()
                else:
                    messagebox.showerror("Error", "Error al eliminar el autor")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            
    def consultar_autor(self):
        try:
            if not self.autor_modelo.id.get():
                messagebox.showwarning("Advertencia", "Debe ingresar un ID para consultar")
                return
                
            resultado = self.autor_controlador.consultar(self.autor_modelo.id.get())
            if resultado:
                self.autor_modelo.nombre.set(resultado.get('nombre', ''))
                self.autor_modelo.edad.set(resultado.get('edad', 0))
                self.autor_modelo.nacionalidad.set(resultado.get('nacionalidad', ''))
            else:
                messagebox.showinfo("Info", "Autor no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            
    def consultar_todos_autores(self):
        try:
            resultado = self.autor_controlador.consultar_todo('', '', '')
            if resultado:
                data = []
                for autor in resultado:
                    data.append([
                        autor.get('id', ''),
                        autor.get('nombre', ''),
                        autor.get('edad', ''),
                        autor.get('nacionalidad', '')
                    ])
                self.tabla_autores.refrescar(data)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            
    def seleccionar_autor(self, event):
        selection = self.tabla_autores.tabla.selection()
        if selection:
            item = self.tabla_autores.tabla.item(selection[0])
            values = item['values']
            if values:
                self.autor_modelo.id.set(values[0])
                self.autor_modelo.nombre.set(values[1])
                self.autor_modelo.edad.set(values[2])
                self.autor_modelo.nacionalidad.set(values[3])
                
    def limpiar_autor(self):
        self.autor_modelo.id.set('')
        self.autor_modelo.nombre.set('')
        self.autor_modelo.edad.set(0)
        self.autor_modelo.nacionalidad.set('')
        
    # Métodos para Libros
    def guardar_libro(self):
        try:
            resultado = self.libro_controlador.guardar(
                self.libro_modelo.titulo.get(),
                self.libro_modelo.genero.get(),
                self.libro_modelo.paginas.get(),
                self.libro_modelo.año_publicacion.get()
            )
            if resultado and resultado.status_code == 201:
                messagebox.showinfo("Éxito", "Libro guardado correctamente")
                self.limpiar_libro()
                self.consultar_todos_libros()
            else:
                messagebox.showerror("Error", "Error al guardar el libro")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            
    def actualizar_libro(self):
        try:
            if not self.libro_modelo.id.get():
                messagebox.showwarning("Advertencia", "Debe seleccionar un libro para actualizar")
                return
                
            resultado = self.libro_controlador.actualizar(
                self.libro_modelo.id.get(),
                self.libro_modelo.titulo.get(),
                self.libro_modelo.genero.get(),
                self.libro_modelo.paginas.get(),
                self.libro_modelo.año_publicacion.get()
            )
            if resultado and resultado.status_code == 200:
                messagebox.showinfo("Éxito", "Libro actualizado correctamente")
                self.limpiar_libro()
                self.consultar_todos_libros()
            else:
                messagebox.showerror("Error", "Error al actualizar el libro")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            
    def eliminar_libro(self):
        try:
            if not self.libro_modelo.id.get():
                messagebox.showwarning("Advertencia", "Debe seleccionar un libro para eliminar")
                return
                
            respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este libro?")
            if respuesta:
                resultado = self.libro_controlador.eliminar(self.libro_modelo.id.get())
                if resultado == 204:
                    messagebox.showinfo("Éxito", "Libro eliminado correctamente")
                    self.limpiar_libro()
                    self.consultar_todos_libros()
                else:
                    messagebox.showerror("Error", "Error al eliminar el libro")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            
    def consultar_libro(self):
        try:
            if not self.libro_modelo.id.get():
                messagebox.showwarning("Advertencia", "Debe ingresar un ID para consultar")
                return
                
            resultado = self.libro_controlador.consultar(self.libro_modelo.id.get())
            if resultado:
                self.libro_modelo.titulo.set(resultado.get('titulo', ''))
                self.libro_modelo.genero.set(resultado.get('genero', ''))
                self.libro_modelo.paginas.set(resultado.get('paginas', 0))
                self.libro_modelo.año_publicacion.set(resultado.get('año_publicacion', 0))
            else:
                messagebox.showinfo("Info", "Libro no encontrado")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            
    def consultar_todos_libros(self):
        try:
            resultado = self.libro_controlador.consultar_todo('', '', '', '')
            if resultado:
                data = []
                for libro in resultado:
                    data.append([
                        libro.get('id', ''),
                        libro.get('titulo', ''),
                        libro.get('genero', ''),
                        libro.get('paginas', ''),
                        libro.get('año_publicacion', '')
                    ])
                self.tabla_libros.refrescar(data)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            
    def seleccionar_libro(self, event):
        selection = self.tabla_libros.tabla.selection()
        if selection:
            item = self.tabla_libros.tabla.item(selection[0])
            values = item['values']
            if values:
                self.libro_modelo.id.set(values[0])
                self.libro_modelo.titulo.set(values[1])
                self.libro_modelo.genero.set(values[2])
                self.libro_modelo.paginas.set(values[3])
                self.libro_modelo.año_publicacion.set(values[4])
                
    def limpiar_libro(self):
        self.libro_modelo.id.set('')
        self.libro_modelo.titulo.set('')
        self.libro_modelo.genero.set('')
        self.libro_modelo.paginas.set(0)
        self.libro_modelo.año_publicacion.set(0)
        
    def iniciar_respaldos_automaticos(self):
        self.respaldos_activos = True
        self.hilo_respaldo = threading.Thread(target=self.respaldos_automaticos, daemon=True)
        self.hilo_respaldo.start()
        print("Respaldos automáticos iniciados (cada 60 segundos)")
        
    def respaldos_automaticos(self):        
        while self.respaldos_activos:
            try:
                # Obtener autores y guardar en archivo
                r_autores = requests.get(f"{self.API_URL}/autores/")
                if r_autores.status_code == 200:
                    with open("respaldo_autores.txt", "w", encoding="utf-8") as f:
                        for a in r_autores.json():
                            f.write(f"ID: {a['id']}\n")
                            f.write(f"Nombre: {a['nombre']}\n")
                            f.write(f"Nacionalidad: {a['nacionalidad'].capitalize()}\n")
                            f.write(f"Edad: {a['edad']}\n\n")

                # Obtener libros y guardar en archivo
                r_libros = requests.get(f"{self.API_URL}/libros/")
                if r_libros.status_code == 200:
                    with open("respaldo_libros.txt", "w", encoding="utf-8") as f:
                        for l in r_libros.json():
                            f.write(f"ID: {l['id']}\n")
                            f.write(f"Título: {l['titulo']}\n")
                            f.write(f"Género: {l['genero']}\n")
                            f.write(f"Páginas: {l['paginas']}\n")
                            f.write(f"Año: {l['año_publicacion']}\n\n")

                print("Respaldo automático realizado.")
                
            except Exception as e:
                print(f"Error en respaldo automático: {e}")
                
            # Esperar 60 segundos antes del próximo respaldo
            for i in range(60):
                if not self.respaldos_activos:
                    break
                time.sleep(1)
        
    def mostrar_interfaz(self):
        self.ventana.mainloop()
