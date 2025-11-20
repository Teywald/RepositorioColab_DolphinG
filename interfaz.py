from datetime import datetime
import sqlite3
import tkinter as tk
from tkinter import ttk
import os
from modulos.CRUD import *

DB_PATH = os.path.join(os.environ["LOCALAPPDATA"], "dolphin_green.db")

# ---------------- Backend ----------------
def calcular_noches(entrada, salida):
    try:
        fecha1 = datetime.strptime(entrada, "%Y-%m-%d")
        fecha2 = datetime.strptime(salida, "%Y-%m-%d")
        return (fecha2 - fecha1).days
    except:
        return "-"


# ---------------- Aplicación ----------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.configurar_ventana()
        self.configurar_grid()
        self.configurar_estilos()

        # Panel lateral (Para crear el panel izquierdo)
        self.crear_panel_lateral()

        # Contenedor principal de la reserva (a la derecha)
        self.contenedor = ttk.Frame(self)
        self.contenedor.grid(row=0, column=1, sticky="NS", padx=10, pady=10)

        # Cargar pantalla por defecto
        self.pantalla_crear_reserva()


    # Configuracion de la ventana GUI 
    def configurar_ventana(self):
        self.geometry('900x600')  #Tamaño en pixeles
        self.configure(bg='#F9F5F1')    #Color del fondo
        self.title('Dolphin Green')     #Nombr
        self.iconbitmap('icon.ico')    #Icono APP
    

    def configurar_grid(self):
        # Panel izquierdo
        self.columnconfigure(0, weight=0, minsize=120) #Panel lateral mas ancho
        # Área principal
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
    

    def configurar_estilos(self):
        #Creamos un objeto estilo para aplicar estilo :) a la ventada de grid 
        estilos = ttk.Style()
        estilos.theme_use('clam')
        
        #Estilos para la ventana principal 
        estilos.configure('.', background='#F9F5F1')
        estilos.configure('TButton', background="#CCCABA")
        #Estilo para color(fondo) del boton
        estilos.map('TButton', background=[('active', "#A8A177")])
        #Estilo para cuando pose el mouse por encima
        estilos.configure('BG.TFrame', background='#F9F5F1') #foregroud = 'white')
        
        #Estilos para el panel del lateral izquierdo
        estilos.configure('Lateral.TFrame', background="#BDB699")
        estilos.configure('Lateral.TLabel', background='#BDB699', foreground='white')
        estilos.configure('Lateral.TButton', background="#CCCABA", foreground='white')
        estilos.map('Lateral.TButton', background=[('active', '#A8A177')])



    # Panel lateral izquierdo
    def crear_panel_lateral(self):
        #Crear panel lateral
        self.panel = ttk.Frame(self, style='Lateral.TFrame')
        self.panel.grid(row=0, column=0, sticky="NS", padx=0, pady=0)

        #Nombre y estilo del panel lateral
        ttk.Label(
            self.panel,
            text="COTIZACIONES",
            font=("Segoe UI", 18, "bold"),
            style='Lateral.TLabel'
        ).pack(pady=40)

        #Boton para crear reserva 
        ttk.Button(
            self.panel,
            text="Crear Reserva",
            command=self.pantalla_crear_reserva,
            style='Lateral.TButton'
        ).pack(fill="x", padx=20, pady=10)

        #Boton para buscar reserva
        ttk.Button(
            self.panel,
            text="Reservas",
            command=self.pantalla_reserva,
            style='Lateral.TButton'
        ).pack(fill="x", padx=20, pady=10)
        
        """Aqui seguira luego, calendario, repositorio historico de las
        cotizaciones y demas funcionalidades que ameriten"""


    #Para limpiar la pantalla cuando cambie entre apartados del lateral
    def limpiar_pantalla(self):
        for widget in self.contenedor.winfo_children():
            widget.destroy()


    #Pantalla de configuracion de la reserva
    def pantalla_crear_reserva(self):
        self.limpiar_pantalla()
        
        self.frame_datos = ttk.Frame(self.contenedor, style='BG.TFrame')
        self.frame_datos.grid(row=0, column=0, padx=20, pady=20)

        #Titulo y estilos
        ttk.Label(
            self.frame_datos,
            text="Crear Reserva",
            font=('Segoe UI', 25, 'bold'),
            background='#F9F5F1'
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # Variables
        self.nombre_cliente = tk.StringVar()
        self.cedula = tk.IntVar()
        self.telefono = tk.StringVar()
        self.correo = tk.StringVar()
        self.direccion = tk.StringVar()
        self.num_personas = tk.IntVar()
        self.fecha_ent = tk.StringVar()
        self.fecha_sal = tk.StringVar()
        self.noches_var = tk.StringVar(value="-")

        # Nombre y caja de texto de nombre
        ttk.Label(self.frame_datos, text="Nombre Cliente").grid(row=1, column=0, sticky='W')
        ttk.Entry(self.frame_datos, textvariable=self.nombre_cliente).grid(row=1, column=1)

        # Cedula y caja de texto
        ttk.Label(self.frame_datos, text="Cédula").grid(row=2, column=0, sticky='W')
        ttk.Entry(self.frame_datos, textvariable=self.cedula).grid(row=2, column=1)

        # Teléfono...
        ttk.Label(self.frame_datos, text="Teléfono").grid(row=3, column=0, sticky='W')
        ttk.Entry(self.frame_datos, textvariable=self.telefono).grid(row=3, column=1)

        # Correo...
        ttk.Label(self.frame_datos, text="Correo").grid(row=4, column=0, sticky='W')
        ttk.Entry(self.frame_datos, textvariable=self.correo).grid(row=4, column=1)
        
        # Direccion...
        ttk.Label(self.frame_datos, text="Direccion").grid(row=5, column=0, sticky='W')
        ttk.Entry(self.frame_datos, textvariable=self.direccion).grid(row=5, column=1)

        # Número de personas...
        ttk.Label(self.frame_datos, text="Número de Personas").grid(row=6, column=0, sticky='W')
        ttk.Entry(self.frame_datos, textvariable=self.num_personas).grid(row=6, column=1)

        # Fecha entrada...
        ttk.Label(self.frame_datos, text="Fecha Entrada (YYYY-MM-DD)").grid(row=7, column=0, sticky='W')
        ttk.Entry(self.frame_datos, textvariable=self.fecha_ent).grid(row=7, column=1)

        # Fecha salida...
        ttk.Label(self.frame_datos, text="Fecha Salida (YYYY-MM-DD)").grid(row=8, column=0, sticky='W')
        ttk.Entry(self.frame_datos, textvariable=self.fecha_sal).grid(row=8, column=1)

        # Noches...
        ttk.Label(self.frame_datos, text="Noches:").grid(row=9, column=0, sticky="W")
        ttk.Label(self.frame_datos, textvariable=self.noches_var,
                  font=("Segoe UI", 18, "bold")).grid(row=9, column=1, sticky="W")
        
        # Boton Crear Reserva
        ttk.Button(
            self.frame_datos,
            text="Crear Reserva",
            command=lambda: crear_reserva(self.nombre_cliente.get(), self.cedula.get(), self.telefono.get(), self.correo.get(), self.direccion.get(), self.num_personas.get(), self.fecha_ent.get(), self.fecha_sal.get())
        ).grid(row=10, column=1, columnspan=2, pady=20)
        
        # Botón calcular
        ttk.Button(
            self.frame_datos,
            text="Calcular Noches",
            command=self.actualizar_noches
        ).grid(row=11, column=0, columnspan=1, pady=20)

    # Pantalla de Reservas
    def pantalla_reserva(self):

        self.limpiar_pantalla()

        # Marco principal de la pantalla
        frame = ttk.Frame(self.contenedor, style='BG.TFrame')
        frame.grid(row=0, column=0, padx=20, pady=20)

        ttk.Label(
            frame,
            text="Buscar Reserva",
            font=("Segoe UI", 20),
            background="#F9F5F1"
        ).grid(row=0, column=0, pady=20, columnspan=3)

        # ---------------------- BUSQUEDA ----------------------
        self.busqueda = tk.StringVar()

        ttk.Label(frame, text="Búsqueda").grid(row=1, column=0, sticky="W")
        ttk.Entry(frame, textvariable=self.busqueda, width=30).grid(row=1, column=1, padx=5)

        # ---------------------- TABLA -------------------------
        columnas = ("Id", "Cliente", "Documento", "Contacto", "Correo", "Direccion",
                    "Personas", "FechaLlegada", "FechaSalida")

        self.tree = ttk.Treeview(frame, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.grid(row=2, column=0, columnspan=3, pady=10)

        #Funcion Cargar
        def cargar_datos(filtro=""):
            # limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            if filtro == "":
                cursor.execute("SELECT * FROM Reserva")
            else:
                cursor.execute("""
                    SELECT * FROM Reserva
                    WHERE NombreCliente LIKE ? OR Documento LIKE ?
                """, (f"%{filtro}%", f"%{filtro}%"))

            filas = cursor.fetchall()

            for fila in filas:
                self.tree.insert("", "end", values=fila + ("Eliminar",))

            conn.close()

        # Botón buscar (ya conoce cargar_datos)
        ttk.Button(
            frame,
            text="Buscar",
            command=lambda: cargar_datos(self.busqueda.get())
        ).grid(row=1, column=2, padx=10)

        # Cargar todas las reservas al abrir pantalla
        cargar_datos("")

    # -------------------------------------------------
    # BACKEND UI
    def actualizar_noches(self):
        entrada = self.fecha_ent.get()
        salida = self.fecha_sal.get()
        self.noches_var.set(calcular_noches(entrada, salida))


# ---------------------------------------------------------
if __name__ == '__main__':
    app = App()
    app.mainloop()
