import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from PIL import Image, ImageTk
import threading
from utils import rutas


class Inventario(tk.Frame):
    db_name = 'database.db'

    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.cargar_sucursales()
        self.articulos_combobox()
        self.cargar_articulos()
        self.timer_articulos = None

    def widgets(self):
        #================================== Tabla de Artículos ==================================#
        canvas_articulos = tk.LabelFrame(self, text="Articulos", bg="#c9dbe1", font="Arial 16 bold")
        canvas_articulos.place(x=300, y=10, width=780, height=580)

        # Treeview como tabla
        self.tree = ttk.Treeview(canvas_articulos, columns=("Articulo", "Precio", "Costo", "Codigo", "Stock", "Sucursal"), show="headings")
        self.tree.heading("Articulo", text="Artículo")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Costo", text="Costo")
        self.tree.heading("Codigo", text="Código")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Sucursal", text="Sucursal")

        self.tree.column("Articulo", width=150)
        self.tree.column("Precio", width=80)
        self.tree.column("Costo", width=80)
        self.tree.column("Codigo", width=120)
        self.tree.column("Stock", width=60)
        self.tree.column("Sucursal", width=120)

        self.tree.pack(fill="both", expand=True)

        #============================== Buscar ==============================#
        lblframe_buscar = LabelFrame(self, text="Buscar", bg="#c9dbe1", font="Arial 14 bold")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)

        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="Arial 12")
        self.comboboxbuscar.place(x=5, y=5, width=260, height=40)
        self.comboboxbuscar.bind("<<ComboboxSelected>>", self.on_combobox_select)
        self.comboboxbuscar.bind("<KeyRelease>", self.filtrar_articulos)

        #=========================== Selección =============================#
        lblframe_seleccion = LabelFrame(self, text="Selección", bg="#c9dbe1", font="Arial 14 bold")
        lblframe_seleccion.place(x=10, y=95, width=280, height=190)

        self.label1 = tk.Label(lblframe_seleccion, text="Articulo:", font="Arial 14", bg="#c9dbe1")
        self.label1.place(x=5, y=5)

        self.label2 = tk.Label(lblframe_seleccion, text="Precio:", font="Arial 14", bg="#c9dbe1")
        self.label2.place(x=5, y=40)

        self.label3 = tk.Label(lblframe_seleccion, text="Costo:", font="Arial 14", bg="#c9dbe1")
        self.label3.place(x=5, y=70)

        self.label4 = tk.Label(lblframe_seleccion, text="Stock:", font="Arial 14", bg="#c9dbe1")
        self.label4.place(x=5, y=100)

        self.label5 = tk.Label(lblframe_seleccion, text="Sucursal:", font="Arial 14", bg="#c9dbe1")
        self.label5.place(x=5, y=130)

        #=========================== Botones ==============================#
        lblframe_botones = LabelFrame(self, text="Opciones", bg="#c9dbe1", font="Arial 14 bold")
        lblframe_botones.place(x=10, y=290, width=280, height=300)

        tk.Button(lblframe_botones, text="Agregar", font="Arial 14 bold", bg="white", command=self.agregar_articulos).place(x=20, y=20, width=180, height=40)
        tk.Button(lblframe_botones, text="Editar", font="Arial 14 bold", bg="white",command=self.editar_articulos).place(x=20, y=80, width=180, height=40)
        tk.Button(lblframe_botones, text="Eliminar", font="Arial 14 bold", bg="white", command=self.eliminar_articulos).place(x=20, y=140, width=180, height=40)

        #============================== Imágenes en Botones ==============================#
        self.imagen_agregar = Image.open(rutas("imagenes/agregarUsuario.png"))
        imagen_agregar = self.imagen_agregar.resize((50,50))
        imagen_agregar = ImageTk.PhotoImage(imagen_agregar)

        self.imagen_actualizar = Image.open(rutas("imagenes/actualizarUsuario.png"))
        imagen_actualizar = self.imagen_actualizar.resize((50,50))
        imagen_actualizar = ImageTk.PhotoImage(imagen_actualizar)

        self.imagen_eliminar = Image.open(rutas("imagenes/eliminarUsuario.png"))
        imagen_eliminar = self.imagen_eliminar.resize((50,50))
        imagen_eliminar = ImageTk.PhotoImage(imagen_eliminar)

        tk.Button(lblframe_botones, image=imagen_agregar, command=self.agregar_articulos, bg="#c9dbe1", borderwidth=0).place(x=20, y=20, width=50, height=50)
        tk.Button(lblframe_botones, image=imagen_actualizar, command=self.editar_articulos, bg="#c9dbe1", borderwidth=0).place(x=20, y=80, width=50, height=50)
        tk.Button(lblframe_botones, image=imagen_eliminar, command=self.eliminar_articulos, bg="#c9dbe1", borderwidth=0).place(x=20, y=140, width=50, height=50)

    def cargar_sucursales(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM sucursales")
            self.sucursales = [sucursal[0] for sucursal in cursor.fetchall()]
            conn.close()
        except sqlite3.Error as e:
            print("Error al cargar sucursales:", e)
            self.sucursales = []

    def articulos_combobox(self):
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.cur.execute("SELECT DISTINCT articulo FROM articulos")
        self.articulos = [row[0] for row in self.cur.fetchall()]
        self.comboboxbuscar['values'] = self.articulos

    def agregar_articulos(self):
        top = tk.Toplevel(self)
        top.title("Agregar Articulo")
        top.geometry("700x400+200+50")
        top.config(bg="#c9dbe1")
        top.resizable(False, False)
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()        # Entradas
        campos = [("Codigo", 20), ("Articulo", 60), ("Precio", 100), ("Costo", 140), ("Stock", 180)]
        entradas = {}

        for nombre, y in campos:
            tk.Label(top, text=f"{nombre}: ", font="Arial 12 bold", bg="#c9dbe1").place(x=20, y=y, height=25, width=80)
            entrada = ttk.Entry(top, font="Arial 12 bold")
            entrada.place(x=120, y=y, width=250, height=25)
            entradas[nombre.lower()] = entrada
            
        # Combobox para sucursal
        tk.Label(top, text="Sucursal: ", font="Arial 12 bold", bg="#c9dbe1").place(x=20, y=220, height=25, width=80)
        combo_sucursal = ttk.Combobox(top, font="Arial 12 bold", state="readonly", values=self.sucursales)
        combo_sucursal.place(x=120, y=220, width=250, height=25)
        if self.sucursales:
            combo_sucursal.set(self.sucursales[0])
        entradas["sucursal"] = combo_sucursal

        def guardar():
            datos = {k: v.get() for k, v in entradas.items()}

            if not all(datos.values()):
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            try:
                datos["precio"] = float(datos["precio"])
                datos["costo"] = float(datos["costo"])
                datos["stock"] = int(datos["stock"])
            except ValueError:
                messagebox.showerror("Error", "Precio, costo y stock deben ser números")
                return

            try:
                self.cur.execute("""
                    INSERT INTO articulos (articulo, precio, costo, codigo, stock, sucursal)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (datos["articulo"], datos["precio"], datos["costo"],
                     datos["codigo"], datos["stock"], datos["sucursal"])
                )
                self.con.commit()
                messagebox.showinfo("Éxito", "Artículo agregado correctamente")
                top.destroy()
                self.cargar_articulos()
            except sqlite3.Error as e:
                print("Error al agregar artículo:", e)
                messagebox.showerror("Error", "Error al agregar artículo")

        tk.Button(top, text="Guardar", font="Arial 12 bold", command=guardar).place(x=50, y=300, width=150, height=40)
        tk.Button(top, text="Cancelar", font="Arial 12 bold", command=top.destroy).place(x=300, y=300, width=150, height=40)

    def cargar_articulos(self, filtro=None, categoria=None):
        self.after(0, self._cargar_articulos, filtro, categoria)

    def _cargar_articulos(self, filtro=None, categoria=None):
        self.tree.delete(*self.tree.get_children())
        query = "SELECT * FROM articulos"
        params = []

        if filtro:
            query += " WHERE articulo LIKE ? OR codigo LIKE ?"
            params.extend((f'%{filtro}%', f'%{filtro}%'))

        self.cur.execute(query, params)
        articulos = self.cur.fetchall()

        for _, articulo, precio, costo, codigo, stock, sucursal in articulos:
            self.tree.insert("", "end", values=(articulo, f"${precio:.2f}", f"${costo:.2f}", codigo, stock, sucursal))

    def on_combobox_select(self, event):
        self.actualizar_label()

    def actualizar_label(self, event=None):
        valor = self.comboboxbuscar.get().strip()

        try:
            self.cur.execute("""
                SELECT articulo, precio, costo, stock, sucursal 
                FROM articulos 
                WHERE articulo = ? OR codigo = ?
            """, (valor, valor))
            resultado = self.cur.fetchone()

            if resultado:
                articulo, precio, costo, stock, sucursal = resultado
                self.label1.config(text=f"Articulo: {articulo}")
                self.label2.config(text=f"Precio: {precio}")
                self.label3.config(text=f"Costo: {costo}")
                self.label4.config(text=f"Stock: {stock}")
                self.label5.config(text=f"Sucursal: {sucursal}")
            else:
                for label in [self.label1, self.label2, self.label3, self.label4, self.label5]:
                    label.config(text="No encontrado")

        except sqlite3.Error as e:
            print("Error al buscar artículo:", e)
            messagebox.showerror("Error", "Error al buscar artículo")

    def filtrar_articulos(self, event):
        if self.timer_articulos:
            self.after_cancel(self.timer_articulos)

        self.timer_articulos = self.after(300, self._filter_articulos)


    def _filter_articulos(self):
        typed = self.comboboxbuscar.get().strip()

        if not typed:
            self.comboboxbuscar['values'] = self.articulos
            self.cargar_articulos()
            return

        try:
            self.cur.execute("""
            SELECT DISTINCT articulo FROM articulos
            WHERE articulo LIKE ? OR codigo LIKE ?
            """, (f'%{typed}%', f'%{typed}%'))

            resultados = self.cur.fetchall()
            data = [row[0] for row in resultados]

            if data:
                self.comboboxbuscar['values'] = data
            else:
                self.comboboxbuscar['values'] = ['No se encontraron resultados']

            self.comboboxbuscar.event_generate('<Down>')
            self.cargar_articulos(filtro=typed)

        except sqlite3.Error as e:
            print("Error en filtro:", e)
            messagebox.showerror("Error", "No se pudo filtrar los artículos")
            
    def editar_articulos(self):
        selected_item = self.comboboxbuscar.get()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un artículo")
            return 

        self.cur.execute("SELECT articulo,precio,costo,codigo,stock,sucursal FROM articulos WHERE articulo = ?", (selected_item,))
        resultado = self.cur.fetchone()
        
        if not resultado:
            messagebox.showerror("Error", "No se encontró el artículo")
            return
        
        top = tk.Toplevel(self)
        top.title("Editar Articulo")
        top.geometry("700x400+200+50")
        top.config(bg="#c9dbe1")
        top.resizable(False, False)
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()
        
        (articulo, precio, costo, codigo , stock, sucursal) = resultado
        
        tk.Label(top,text="Articulo: ",font="arial 12 bold ",bg="#c9dbe1").place(x=20,y= 20, width=80,height=25)
        entry_articulo = ttk.Entry(top,font="arial 12 bold")
        entry_articulo.place(x=120,y=20 ,width=250,height=30)
        entry_articulo.insert(0,articulo)
        
        tk.Label(top,text="Precio: ",font="arial 12 bold ",bg="#c9dbe1").place(x=20,y= 60, width=80,height=25)
        entry_precio = ttk.Entry(top,font="arial 12 bold")
        entry_precio.place(x=120,y=60 ,width=250,height=30)
        entry_precio.insert(0,precio)
        
        tk.Label(top,text="Costo: ",font="arial 12 bold ",bg="#c9dbe1").place(x=20,y= 100, width=80,height=25)
        entry_costo = ttk.Entry(top,font="arial 12 bold")
        entry_costo.place(x=120,y=100 ,width=250,height=30)
        entry_costo.insert(0,costo)
        
        tk.Label(top,text="Codigo: ",font="arial 12 bold ",bg="#c9dbe1").place(x=20,y= 140, width=80,height=25)
        entry_codigo = ttk.Entry(top,font="arial 12 bold")
        entry_codigo.place(x=120,y=140 ,width=250,height=30)
        entry_codigo.insert(0,codigo)
        
        tk.Label(top,text="Stock: ",font="arial 12 bold ",bg="#c9dbe1").place(x=20,y= 180, width=80,height=25)
        entry_stock = ttk.Entry(top,font="arial 12 bold")
        entry_stock.place(x=120,y=180 ,width=250,height=30)
        entry_stock.insert(0,stock)
        
        tk.Label(top, text="Sucursal: ", font="arial 12 bold", bg="#c9dbe1").place(x=20, y=220, width=80, height=25)
        combo_sucursal = ttk.Combobox(top, font="arial 12 bold", state="readonly", values=self.sucursales)
        combo_sucursal.place(x=120, y=220, width=250, height=30)
        if sucursal in self.sucursales:
            combo_sucursal.set(sucursal)
        elif self.sucursales:
            combo_sucursal.set(self.sucursales[0])
        entry_sucursal = combo_sucursal
        
        def guardar():
            nuevo_articulo = entry_articulo.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            codigo = entry_codigo.get()
            stock = entry_stock.get()
            sucursal = entry_sucursal.get()
            
            if not nuevo_articulo or not precio or not costo or not codigo or not stock or not sucursal:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return 
            
            try:
                precio = float(precio)
                costo = float(costo)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Los campos precio, costo y stock deben ser numericos")
                
                
            self.cur.execute(
            "UPDATE articulos SET articulo = ?, precio = ?, costo = ?, codigo = ?, stock = ?, sucursal = ? WHERE articulo = ? OR codigo = ?",
            (nuevo_articulo, precio, costo, codigo, stock, sucursal, selected_item, selected_item))
            self.con.commit()
            
            self.articulos_combobox()
            self.after(0,lambda: self.cargar_articulos(filtro=nuevo_articulo))
            
            top.destroy()
            messagebox.showinfo("Exito","Articulo editado exitosamente")
            
        btn_guardar  = tk.Button(top, text="Guardar", command=guardar,font="arial 12 bold")
        btn_guardar.place(x=260,y=300,width=150, height=40)
    
    def eliminar_articulos(self):
        valor = self.comboboxbuscar.get().strip()

        if not valor:
            messagebox.showwarning("Advertencia", "Por favor escribe el nombre o código del artículo que deseas eliminar.")
            return

        try:
            # Buscar el artículo por nombre o código
            self.cur.execute("SELECT articulo, codigo FROM articulos WHERE articulo = ? OR codigo = ?", (valor, valor))
            resultado = self.cur.fetchone()

            if not resultado:
                messagebox.showerror("Error", "No se encontró ningún artículo con ese nombre o código.")
                return

            articulo, codigo = resultado

        # Confirmación del usuario
            respuesta = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar el artículo '{articulo}'?")
            if not respuesta:
                return

        # Eliminar de la base de datos
            self.cur.execute("DELETE FROM articulos WHERE articulo = ? AND codigo = ?", (articulo, codigo))
            self.con.commit()

        # Mostrar éxito
            messagebox.showinfo("Éxito", "Artículo eliminado correctamente")

        # Limpiar etiquetas
            for label in [self.label1, self.label2, self.label3, self.label4, self.label5]:
                label.config(text="")

        # Actualizar Combobox y tabla
            self.articulos_combobox()
            self.comboboxbuscar['values'] = self.articulos
            self.comboboxbuscar.set("")
            self.cargar_articulos()

        except Exception as e:
            print("Error al eliminar:", e)
            messagebox.showerror("Error", "No se pudo eliminar el artículo")


