import sqlite3
import shutil
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox,filedialog
from PIL import Image, ImageTk
import os
import sys
from utils import rutas


class Configuraciones(tk.Frame):
    db_name = 'database.db'
    def __init__(self, padre):
        super().__init__(padre)

        self.widgets()

    def widgets(self):
        frame = tk.LabelFrame(self, text="Configuración", bg="#c9dbe1", font="sans 30 bold", labelanchor="n")
        frame.place(x=0, y=0, width=1100, height=600)

        imagen_sucursal = Image.open(rutas("imagenes/sucursales.png")).resize((100, 100))
        imagen_tk = ImageTk.PhotoImage(imagen_sucursal)

        self.btn_sucursal = Button(frame, fg="black", text="Sucursal", font="sans 16 bold", command=self.crear_sucursal)
        self.btn_sucursal.config(image=imagen_tk, compound=TOP, padx=10)
        self.btn_sucursal.image = imagen_tk
        self.btn_sucursal.place(x=150, y=50, width=250, height=150)

        imagen_miEmpresa = Image.open(rutas("imagenes/empresa.png")).resize((100, 100))
        imagen_miEmpresa = ImageTk.PhotoImage(imagen_miEmpresa)        
        
        self.btn_miEmpresa = Button(frame, fg="black", text="Mi empresa", font="sans 16 bold", command=self.ver_mi_empresa)
        self.btn_miEmpresa.config(image=imagen_miEmpresa, compound=TOP, padx=10)
        self.btn_miEmpresa.image = imagen_miEmpresa
        self.btn_miEmpresa.place(x=450, y=50, width=250, height=150)

        imagen_copiaSeguridad = Image.open(rutas("imagenes/guardardb.png")).resize((100, 100))
        imagen_copiaSeguridad = ImageTk.PhotoImage(imagen_copiaSeguridad)

        self.btn_copiaSeguridad = Button(frame, fg="black", text="Copia de seguridad DB", font="sans 16 bold", command=self.copia_seguridad_db)
        self.btn_copiaSeguridad.config(image=imagen_copiaSeguridad, compound=TOP, padx=10)
        self.btn_copiaSeguridad.image = imagen_copiaSeguridad
        self.btn_copiaSeguridad.place(x=750, y=50, width=250, height=150)

        imagen_RestaurarDB = Image.open(rutas("imagenes/cargardb.png")).resize((100, 100))
        imagen_RestaurarDB = ImageTk.PhotoImage(imagen_RestaurarDB)

        self.btn_RestaurarDB = Button(frame, fg="black", text="Restaurar DB", font="sans 16 bold",command=self.restaurar_db)
        self.btn_RestaurarDB.config(image=imagen_RestaurarDB, compound=TOP, padx=10)
        self.btn_RestaurarDB.image = imagen_RestaurarDB
        self.btn_RestaurarDB.place(x=450, y=250, width=250, height=150)

    def crear_sucursal(self):
        top = tk.Toplevel(self)
        top.title("Sucursales")
        top.geometry("400x500+200+100")
        top.config(bg="#c9dbe1")
        top.resizable(False, False)
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        imagen_guardar = Image.open(rutas("imagenes/guardar.png")).resize((30, 30))
        imagen_guardar = ImageTk.PhotoImage(imagen_guardar)

        imagen_eliminar = Image.open(rutas("imagenes/eliminar.png")).resize((30, 30))
        imagen_eliminar = ImageTk.PhotoImage(imagen_eliminar)

        labelframe = tk.LabelFrame(top, text="Crear Sucursales", font="sans 16 bold", bg="#c9dbe1", bd=2,
                                   relief="groove", labelanchor="n")
        labelframe.place(x=20, y=20, width=360, height=450)

        lbl_nombre = tk.Label(labelframe, text="Nombre:", font="sans 12 bold", bg="#c9dbe1")
        lbl_nombre.place(x=20, y=40)

        self.entry_nombre = tk.Entry(labelframe, font="sans 12", width=25)
        self.entry_nombre.place(x=100, y=40, height=30)

        btn_guardar = tk.Button(labelframe, text="Guardar", compound=tk.LEFT, padx=10, font="sans 10 bold",
                                bg="white", command=lambda: self.guardar_y_actualizar(self.entry_nombre.get()))
        btn_guardar.config(image=imagen_guardar)
        btn_guardar.image = imagen_guardar
        btn_guardar.place(x=30, y=90, width=130, height=40)

        btn_eliminar = tk.Button(labelframe, text="Eliminar", compound=tk.LEFT, padx=10, font="sans 10 bold",
                                 bg="white", relief="raised", command= self.eliminar_sucursal_seleccionada)
        btn_eliminar.config(image=imagen_eliminar)
        btn_eliminar.image = imagen_eliminar
        btn_eliminar.place(x=200, y=90, width=130, height=40)

        scrol_y = ttk.Scrollbar(labelframe, orient=VERTICAL)
        scrol_y.place(x=315, y=150, height=240)

        self.tre = ttk.Treeview(labelframe, yscrollcommand=scrol_y.set,
                                columns=("ID", "Nombre"), show="headings", height=10)
        self.tre.place(x=20, y=150, width=300, height=240)

        scrol_y.config(command=self.tre.yview)

        self.tre.heading("ID", text="ID")
        self.tre.heading("Nombre", text="Nombre")

        self.tre.column("ID", width=50, anchor="center")
        self.tre.column("Nombre", width=250, anchor="center")

        self.actualizar_treeview()

    def agregar_sucursal(self, nombre):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sucursales (nombre) VALUES (?)", (nombre,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Sucursal creada exitosamente.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al crear la sucursal: {e}")

    def mostrar_sucursales(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sucursales")
            rows = cursor.fetchall()
            conn.close()
            for row in rows:
                self.tre.insert("", "end", values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al mostrar las sucursales: {e}")

    def actualizar_treeview(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
        self.mostrar_sucursales()

    def guardar_y_actualizar(self, nombre):
        if not nombre.strip():
            messagebox.showwarning("Campo vacío", "El nombre de la sucursal no puede estar vacío.")
            return
        self.agregar_sucursal(nombre)
        self.entry_nombre.delete(0, END)
        self.actualizar_treeview()

    def eliminar_sucursal(self, sucursal_id, nombre):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()  # Create cursor here
            cursor.execute("DELETE FROM sucursales WHERE id = ?", (sucursal_id,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", f"Sucursal '{nombre}' eliminada exitosamente.") # Added success message
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al eliminar la sucursal: {e}")
            return
        self.actualizar_treeview()

    def eliminar_sucursal_seleccionada(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una sucursal para eliminar.")
            return

        item = self.tre.item(seleccion[0])
        sucursal_id = item['values'][0]
        nombre = item['values'][1]

        confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la sucursal '{nombre}'?")
        if confirmar:
            self.eliminar_sucursal(sucursal_id, nombre)

    def copia_seguridad_db(self):
        try:
            ruta_destino = filedialog.asksaveasfilename(
                defaultextension=".db",
                filetypes=[("Database files", "*.db")],
                title="Guardar copia de seguridad"
        )
            if ruta_destino:
                shutil.copy(self.db_name, ruta_destino)
                messagebox.showinfo("Éxito", "Copia de seguridad creada exitosamente.")
            else:
                messagebox.showwarning("Advertencia", "No se seleccionó una ruta para guardar la copia de seguridad.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la copia de seguridad: {e}")
    
    def restaurar_db(self):
        try:
            ruta_origen = filedialog.askopenfilename(
                filetypes=[("Database files", "*.db")],
                title="Seleccionar base de datos para restaurar"
            )
            if ruta_origen:
                confirmacion = messagebox.askyesno("Confirmar restauración", "¿Estás seguro de que deseas restaurar esta copia? Esto sobrescribirá la base de datos actual.")
                if confirmacion:
                    shutil.copy(ruta_origen, "basedatos.db")
                    messagebox.showinfo("Éxito", "Base de datos restaurada exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al restaurar la base de datos: {e}")
    
    def ver_mi_empresa(self):
        top = tk.Toplevel(self)
        top.title("Actualizar Información de la Empresa")
        top.geometry("450x500+200+100")
        top.config(bg="#c9dbe1")
        top.resizable(False, False)
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        self.imagen_guardar = Image.open(rutas("imagenes/guardar.png"))
        imagen_guardar = self.imagen_guardar.resize((30,30))
        imagen_guardar = ImageTk.PhotoImage(imagen_guardar)

        frame = tk.LabelFrame(top, text="Información empresa", font="sans 30 bold", bg="#c9dbe1")
        frame.place(x=20, y=20, width=410, height=450)

        label_nombre = tk.Label(frame, text="Nombre de la Empresa:", font="sans 14 bold", bg="#c9dbe1")
        label_nombre.place(x=10, y = 5)
        self.entry_nombre = ttk.Entry(frame, font="sans 14 bold")
        self.entry_nombre.place(x=10, y=30,width=300,height=40)
        
        label_direccion = tk.Label(frame, text="Dirección:", font="sans 14 bold", bg="#c9dbe1")
        label_direccion.place(x=10, y = 70 )
        self.entry_direccion = ttk.Entry(frame, font="sans 14 bold")
        self.entry_direccion.place(x=10, y=100,width=300,height=40)
        
        label_telefono = tk.Label(frame, text="Teléfono", font="sans 14 bold", bg="#c9dbe1")
        label_telefono.place(x=10, y = 150)
        self.entry_telefono = ttk.Entry(frame, font="sans 14 bold")
        self.entry_telefono.place(x=10, y=180,width=300,height=40)
        
        label_email = tk.Label(frame, text="Correo", font="sans 14 bold", bg="#c9dbe1")
        label_email.place(x=10, y = 230)
        self.entry_email = ttk.Entry(frame, font="sans 14 bold")
        self.entry_email.place(x=10, y=260,width=300,height=40)        
        self.btn_guardar = Button(frame, text="Guardar", font="sans 12 bold", command=self.guardar_info_empresa)
        self.btn_guardar.config(image=imagen_guardar, compound=LEFT, padx=10)
        self.btn_guardar.config(image=imagen_guardar)
        self.btn_guardar.image = imagen_guardar
        self.btn_guardar.place(x=150, y=320, width=200, height=40)
        
        # Cargar información existente
        self.cargar_info_empresa()

        # Cargar información de la empresa al abrir la ventana
        self.cargar_info_empresa()

    def guardar_info_empresa(self):
        try:
            nombre = self.entry_nombre.get()
            direccion = self.entry_direccion.get()
            telefono = self.entry_telefono.get()
            email = self.entry_email.get()
            
            if not nombre or not direccion or not telefono or not email:
                messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
                return
                
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            
            # Crear la tabla si no existe
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS empresa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    direccion TEXT,
                    telefono TEXT,
                    email TEXT
                )
            """)
            
            # Verificar si ya existe información
            cursor.execute("SELECT COUNT(*) FROM empresa")
            count = cursor.fetchone()[0]
            
            if count > 0:
                # Actualizar información existente
                cursor.execute("""
                    UPDATE empresa SET 
                    nombre = ?, 
                    direccion = ?, 
                    telefono = ?, 
                    email = ? 
                    WHERE id = 1
                """, (nombre, direccion, telefono, email))
            else:
                # Insertar nueva información
                cursor.execute("""
                    INSERT INTO empresa (nombre, direccion, telefono, email)
                    VALUES (?, ?, ?, ?)
                """, (nombre, direccion, telefono, email))
            
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Información de la empresa guardada correctamente")
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al guardar la información: {e}")

    def cargar_info_empresa(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, direccion, telefono, email FROM empresa WHERE id = 1")
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                self.entry_nombre.delete(0, END)
                self.entry_direccion.delete(0, END)
                self.entry_telefono.delete(0, END)
                self.entry_email.delete(0, END)
                
                self.entry_nombre.insert(0, resultado[0])
                self.entry_direccion.insert(0, resultado[1])
                self.entry_telefono.insert(0, resultado[2])
                self.entry_email.insert(0, resultado[3])
                
        except sqlite3.Error as e:
            print(f"Error al cargar la información de la empresa: {e}")

    def obtener_info_empresa(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, direccion, telefono, email FROM empresa WHERE id = 1")
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                return {
                    "nombre": resultado[0],
                    "direccion": resultado[1],
                    "telefono": resultado[2],
                    "email": resultado[3]
                }
            return None
            
        except sqlite3.Error as e:
            print(f"Error al obtener la información de la empresa: {e}")
            return None