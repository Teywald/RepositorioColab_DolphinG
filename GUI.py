import customtkinter as ctk
import tkinter.ttk as ttk
from CTkTable import CTkTable
import os
import sqlite3
from modulos.config import DB_PATH
from modulos.CRUD import *
from modulos.servicios import *

# Apariencia
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    
    def __init__(self):        
        super().__init__()

        self.title("Dolphin Green")     # Nombre
        self.geometry("900x600")        # Tamaño APP
        self.iconbitmap('icon.ico')     # Icono APP

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- BARRA LATERAL ---
        self.barra_lateral = ctk.CTkFrame(self, height=600 , width=200, corner_radius=0)
        self.barra_lateral.grid(row=0, column=0, sticky="nsw")

        self.barra_lateral_label = ctk.CTkLabel(self.barra_lateral, text="Menu", font=("", 20))
        self.barra_lateral_label.pack(padx=20, pady=(20, 10))

        # Botones
        self.boton_reserva = ctk.CTkButton(
            self.barra_lateral, text="Reservas",
            command=lambda: self.show_frame("reservas")
        )
        self.boton_reserva.pack(padx=20, pady=10)

        self.boton_calendario = ctk.CTkButton(
            self.barra_lateral, text="Calendario",
            command=lambda: self.show_frame("calendario")
        )
        self.boton_calendario.pack(padx=20, pady=10)

        self.boton_servicio = ctk.CTkButton(
            self.barra_lateral, text="Servicios",
            command=lambda: self.show_frame("servicios")
        )
        self.boton_servicio.pack(padx=20, pady=10)
        
        self.boton_temporada = ctk.CTkButton(
            self.barra_lateral, text="Temporadas",
            command=lambda: self.show_frame("temporadas")
        )
        self.boton_temporada.pack(padx=20, pady=10)

        # --- AREA PRINCIPAL ---
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Diccionario de pantallas
        self.pantallas = {
            "reservas": self.crear_pantalla_reservas,
            "calendario": self.crear_pantalla_calendario,
            "servicios": self.crear_pantalla_servicios,
            "temporadas": self.crear_pantalla_temporadas,
            "crear_reserva": self.crear_pantalla_crear_reserva,
            "editar_reserva": self.crear_pantalla_editar_reserva,
            "editar_servicios": self.crear_pantalla_editar_servicios
        }

        # Mostrar frame por defecto
        self.show_frame("reservas")


    # --- CREACIÓN DE PANTALLAS ----
    # --- PANTALLA RESERVAS ---
    def crear_pantalla_reservas(self):

        frame = ctk.CTkFrame(self.main)
        frame.pack(fill="both", expand=True)

        ctk.CTkLabel(frame, text="Reservas", font=("", 24)).pack(pady=20)

        # --- BUSQUEDA ---
        search_frame = ctk.CTkFrame(frame, fg_color="transparent")
        search_frame.pack(pady=10)

        self.busqueda = ctk.StringVar()

        ctk.CTkLabel(search_frame, text="Buscar:").pack(side="left", padx=5)
        entry_buscar = ctk.CTkEntry(search_frame, textvariable=self.busqueda, width=200)
        entry_buscar.pack(side="left", padx=5)

        btn_buscar = ctk.CTkButton(search_frame, text="Buscar", command=self.actualizar_tabla_reservas)
        btn_buscar.pack(side="left", padx=5)

        # --- TABLA INICIAL ---
        self.reservas_actuales = obtener_reservas()     # ahora guardamos las reservas vigentes

        self.headers = [
            "Cliente", "Documento", "Contacto",
            "Correo", "Dirección", "# Personas",
            "Llegada", "Salida", "Confirmar", "Editar", "Eliminar"
        ]

        self.tabla_reservas = CTkTable(
            frame,
            values=self.construir_tabla(self.reservas_actuales),
            header_color="gray20",
            colors=["gray15", "gray25"],
            hover_color="gray30",
            corner_radius=8,
        )

        self.tabla_reservas.pack(padx=20, pady=20, fill="both", expand=True)

        # --- BOTON CREAR ---
        self.boton_crear_reserva = ctk.CTkButton(
            frame, text="Nueva Reserva",
            command=lambda: self.show_frame("crear_reserva")
        )
        self.boton_crear_reserva.pack(padx=20, pady=10, side="right")

        return frame
    
    def crear_pantalla_crear_reserva(self):
        
        frame = ctk.CTkFrame(self.main)
        frame.pack(fill="both", expand=True)
        
        boton_volver = ctk.CTkButton(
            frame,
            text="Volver",
            fg_color="gray",
            hover_color="#555555",
            command=lambda: self.show_frame("reservas")
        )
        boton_volver.pack(anchor="nw", padx=20, pady=20)

        # --- CONTENEDOR CENTRADO ---
        contenedor = ctk.CTkFrame(frame, fg_color="transparent")
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        # TITULO
        ctk.CTkLabel(contenedor, text="Crear Reserva", font=("", 24)).grid(
            row=0, column=0, columnspan=2, pady=20
        )

        # -------- VARIABLES --------
        self.nombre_cliente = ctk.StringVar()
        self.cedula = ctk.StringVar()
        self.telefono = ctk.StringVar()
        self.correo = ctk.StringVar()
        self.direccion = ctk.StringVar()
        self.num_personas = ctk.StringVar()
        self.fecha_ent = ctk.StringVar()
        self.fecha_sal = ctk.StringVar()
        self.noches_var = ctk.StringVar(value="-")

        # -------- FORMULARIO --------
        campos = [
            ("Nombre Cliente", self.nombre_cliente),
            ("Cédula", self.cedula),
            ("Teléfono", self.telefono),
            ("Correo", self.correo),
            ("Dirección", self.direccion),
            ("Número de Personas", self.num_personas),
            ("Fecha Entrada (YYYY-MM-DD)", self.fecha_ent),
            ("Fecha Salida (YYYY-MM-DD)", self.fecha_sal)
        ]

        fila = 1
        for texto, variable in campos:
            ctk.CTkLabel(contenedor, text=texto).grid(row=fila, column=0, sticky="w", pady=5, padx=10)
            ctk.CTkEntry(contenedor, textvariable=variable, width=220).grid(row=fila, column=1, pady=5)
            fila += 1

        # BOTÓN CREAR
        ctk.CTkButton(
            contenedor,
            text="Crear Reserva",
            command=lambda: crear_reserva(self.nombre_cliente.get(), self.cedula.get(), self.telefono.get(), self.correo.get(), self.direccion.get(), self.num_personas.get(), self.fecha_ent.get(), self.fecha_sal.get())
        ).grid(row=fila, column=0, columnspan=2, pady=20)

        return frame

    def crear_pantalla_editar_reserva(self):
        frame = ctk.CTkFrame(self.main)
        frame.pack(fill="both", expand=True)
        
        boton_volver = ctk.CTkButton(
            frame,
            text="Volver",
            fg_color="gray",
            hover_color="#555555",
            command=lambda: self.show_frame("reservas")
        )
        boton_volver.pack(anchor="nw", padx=20, pady=20)

        # --- CONTENEDOR CENTRADO ---
        contenedor = ctk.CTkFrame(frame, fg_color="transparent")
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        # TITULO
        ctk.CTkLabel(contenedor, text="Crear Reserva", font=("", 24)).grid(
            row=0, column=0, columnspan=2, pady=20
        )

        # -------- VARIABLES --------
        self.nombre_cliente = ctk.StringVar()
        self.cedula = ctk.StringVar()
        self.telefono = ctk.StringVar()
        self.correo = ctk.StringVar()
        self.direccion = ctk.StringVar()
        self.num_personas = ctk.StringVar()
        self.fecha_ent = ctk.StringVar()
        self.fecha_sal = ctk.StringVar()
        self.noches_var = ctk.StringVar(value="-")

        # -------- FORMULARIO --------
        campos = [
            ("Nombre Cliente", self.nombre_cliente),
            ("Cédula", self.cedula),
            ("Teléfono", self.telefono),
            ("Correo", self.correo),
            ("Dirección", self.direccion),
            ("Número de Personas", self.num_personas),
            ("Fecha Entrada (YYYY-MM-DD)", self.fecha_ent),
            ("Fecha Salida (YYYY-MM-DD)", self.fecha_sal)
        ]

        fila = 1
        for texto, variable in campos:
            ctk.CTkLabel(contenedor, text=texto).grid(row=fila, column=0, sticky="w", pady=5, padx=10)
            ctk.CTkEntry(contenedor, textvariable=variable, width=220).grid(row=fila, column=1, pady=5)
            fila += 1

        # BOTÓN CREAR
        ctk.CTkButton(
            contenedor,
            text="Crear Reserva",
            command=lambda: crear_reserva(self.nombre_cliente.get(), self.cedula.get(), self.telefono.get(), self.correo.get(), self.direccion.get(), self.num_personas.get(), self.fecha_ent.get(), self.fecha_sal.get())
        ).grid(row=fila, column=0, columnspan=2, pady=20)

        return frame

    def crear_pantalla_calendario(self):
        frame = ctk.CTkFrame(self.main)
        ctk.CTkLabel(frame, text="Calendario", font=("", 24)).pack(pady=20)
        return frame

    def crear_pantalla_servicios(self):
        frame = ctk.CTkFrame(self.main)
        frame.pack(fill="both", expand=True)

        ctk.CTkLabel(frame, text="Servicios", font=("", 24)).pack(pady=20)
            
        servicios = obtener_parametros_servicios()

        # Encabezados
        headers = [
            "Valor Noche Temp Alta", "Valor Noche Temp Baja", "Valor Cocinera", "Valor Auxiliar Cocina", "Deposito"
        ]
        
        data = [headers] + [list(r)[1:] for r in servicios]

        # Tabla reservas
        table = CTkTable(
            frame,
            values=data,
            header_color="gray20",
            colors=["gray15", "gray25"],
            hover_color="gray30",
            corner_radius=8,
            
        )

        table.pack(padx=20, pady=20, fill="both", expand=True)  # importante
        
        # Frame para botón
        botones = ctk.CTkFrame(frame, fg_color="transparent")
        botones.pack(fill="x")
        
        self.boton_crear_reserva = ctk.CTkButton(frame, text="Editar", command=lambda: self.show_frame("editar_servicios"))
        self.boton_crear_reserva.pack(padx=20, pady=10, side="right")

        return frame

    def crear_pantalla_editar_servicios(self):
        frame = ctk.CTkFrame(self.main)
        frame.pack(fill="both", expand=True)
        
        boton_volver = ctk.CTkButton(
            frame,
            text="Volver",
            fg_color="gray",
            hover_color="#555555",
            command=lambda: self.show_frame("servicios")
        )
        boton_volver.pack(anchor="nw", padx=20, pady=20)
        
        # --- OBTENER DATOS DE LA BD ---
        parametros = obtener_parametros_servicios()
        if parametros:
            parametros = parametros[0]  # (id, v_alta, v_baja, cocinera, aux, deposito)
            self.id_param = parametros[0]
        else:
            parametros = (None, "", "", "", "", "")
            self.id_param = None

        # --- CONTENEDOR CENTRADO ---
        contenedor = ctk.CTkFrame(frame, fg_color="transparent")
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        # TITULO
        ctk.CTkLabel(contenedor, text="Editar Parámetros", font=("", 24)).grid(
            row=0, column=0, columnspan=2, pady=20
        )

        # -------- VARIABLES --------
        self.valor_noche_temp_alta = ctk.StringVar(value=parametros[1])
        self.valor_noche_temp_baja = ctk.StringVar(value=parametros[2])
        self.valor_cocinera = ctk.StringVar(value=parametros[3])
        self.valor_aux_cocina = ctk.StringVar(value=parametros[4])
        self.deposito = ctk.StringVar(value=parametros[5])

        # -------- FORMULARIO --------
        campos = [
            ("Valor Noche Temp Alta", self.valor_noche_temp_alta),
            ("Valor Noche Temp Baja", self.valor_noche_temp_baja),
            ("Valor Cocinera", self.valor_cocinera),
            ("Valor Aux Cocina", self.valor_aux_cocina),
            ("Depósito", self.deposito),
        ]

        fila = 1
        for texto, variable in campos:
            ctk.CTkLabel(contenedor, text=texto).grid(row=fila, column=0, sticky="w", pady=5, padx=10)
            ctk.CTkEntry(contenedor, textvariable=variable, width=220).grid(row=fila, column=1, pady=5)
            fila += 1

        # BOTÓN GUARDAR
        ctk.CTkButton(
            contenedor,
            text="Guardar Cambios",
            command=lambda: actualizar_parametros_servicios(
                self.id_param,
                self.valor_noche_temp_alta.get(),
                self.valor_noche_temp_baja.get(),
                self.valor_cocinera.get(),
                self.valor_aux_cocina.get(),
                self.deposito.get()
            )
        ).grid(row=fila, column=0, columnspan=2, pady=20)

        return frame

    def crear_pantalla_temporadas(self):
        frame = ctk.CTkFrame(self.main)
        ctk.CTkLabel(frame, text="Administración de Temporadas", font=("", 24)).pack(pady=20)
        return frame


    # --- FUNCIÓN PARA CAMBIAR PANTALLAS ---

    def show_frame(self, frame_name):
        # Borrar contenido anterior del main
        for widget in self.main.winfo_children():
            widget.destroy()

        # Crear nueva pantalla desde la función
        frame = self.pantallas[frame_name]()
        frame.pack(fill="both", expand=True)
    
    # Actulizar tabla reservas
    def construir_tabla(self, reservas):
        data = [self.headers]

        for r in reservas:
            fila = list(r)[1:-1]  # quitar ID
            fila += ["Confirmar", "Editar", "Eliminar"]
            data.append(fila)

        return data

    
    def actualizar_tabla_reservas(self):
        busq = self.busqueda.get().strip()

        if busq:
            self.reservas_actuales = buscar_reservas(busq)
        else:
            self.reservas_actuales = obtener_reservas()

        data = self.construir_tabla(self.reservas_actuales)

        self.tabla_reservas.configure(values=data)

app = App()
app.mainloop()