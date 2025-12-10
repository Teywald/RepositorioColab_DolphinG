import sqlite3
from datetime import datetime
import os
from modulos.config import DB_PATH

def inicializar_bd():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reserva (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            NombreCliente TEXT NOT NULL,
            Documento TEXT,
            NumeroContacto TEXT NOT NULL,
            Correo TEXT,
            Direccion TEXT,
            NumeroPersonas INTEGER NOT NULL,
            FechaLlegada TEXT NOT NULL,
            FechaSalida TEXT NOT NULL,
            Estado INTEGER DEFAULT 0
        );
    """)

    conn.commit()
    conn.close()

def fechas_validas(fecha_llegada, fecha_salida):
    try:
        f1 = datetime.strptime(fecha_llegada, "%Y-%m-%d")
        f2 = datetime.strptime(fecha_salida, "%Y-%m-%d")
        return f1 < f2
    except:
        return False

def disponibilidad_cabana(fecha_llegada, fecha_salida):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Considera sólo reservas no confirmadas (Estado != 1) para disponibilidad
    cursor.execute("""
        SELECT * FROM Reserva
        WHERE Estado != 1
        AND NOT (FechaSalida <= ? OR FechaLlegada >= ?)
    """, (fecha_salida, fecha_llegada))

    conflicto = cursor.fetchone()
    conn.close()

    return conflicto is None

def confirmar_cabana(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE Reserva
        SET Estado = 1
        WHERE Id = ?
    """, (id))
    conn.commit()
    conn.close()


def obtener_reserva_por_id(id_reserva):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reserva WHERE Id = ?", (id_reserva,))
    reserva = cursor.fetchone()
    conn.close()
    return reserva

def buscar_reservas(busqueda):
    conn = sqlite3.connect(DB_PATH)  # ← CORREGIDO
    cursor = conn.cursor()

    query = """
        SELECT *
        FROM Reserva
        WHERE NombreCliente LIKE ? OR Documento LIKE ?
    """

    like = f"%{busqueda}%"
    cursor.execute(query, (like, like))
    resultados = cursor.fetchall()
    
    conn.close()
    return resultados


def crear_reserva(nombre, documento, contacto, correo, direccion, num_personas, fecha_llegada, fecha_salida):
    # 1) Valido campos obligatorios
    if not nombre or not contacto or not num_personas or not fecha_llegada or not fecha_salida:
        print("Error: Los campos obligatorios deben estar completos.")
        return

    # 2) Veo que si sean fechas fechas
    if not fechas_validas(fecha_llegada, fecha_salida):
        print("Error: Las fechas no son válidas.")
        return

    # 3) Veo si hay disponibilidad
    if not disponibilidad_cabana(fecha_llegada, fecha_salida):
        print("Error: La fecha seleccionada ya está ocupada.")

        return

    # Inserto en BD
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Reserva (
            NombreCliente, Documento, NumeroContacto, Correo, 
            Direccion, NumeroPersonas, FechaLlegada, FechaSalida
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nombre, documento, contacto, correo, direccion, num_personas, fecha_llegada, fecha_salida))

    conn.commit()
    conn.close()

    print("Reserva creada.")


def obtener_reservas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Reserva")
    reservas = cursor.fetchall()

    conn.close()
    return reservas

def actualizar_reserva(id_reserva, nuevo_contacto, nueva_fecha_llegada, nueva_fecha_salida, nuevo_num_personas):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1) Verifica si la reserva existe, sino paila
    cursor.execute("SELECT * FROM Reserva WHERE Id = ?", (id_reserva,))
    reserva_original = cursor.fetchone()

    if reserva_original is None:
        print("Error: No existe una reserva con ese ID.")
        conn.close()
        return

    # 2) Valida campos obligatorios
    if not nuevo_contacto or not nueva_fecha_llegada or not nueva_fecha_salida or not nuevo_num_personas:
        print("Error: Todos los campos son obligatorios para actualizar.")
        conn.close()
        return

    # 3) Valida fechas
    if not fechas_validas(nueva_fecha_llegada, nueva_fecha_salida):
        print("Error: Las fechas no son válidas.")
        conn.close()
        return

    # 4) Verifica que la nueva fecha no choque
    cursor.execute("""
        SELECT * FROM Reserva
        WHERE Id != ? 
        AND NOT (FechaSalida < ? OR FechaLlegada > ?)
    """, (id_reserva, nueva_fecha_llegada, nueva_fecha_salida))

    conflicto = cursor.fetchone()

    if conflicto:
        print("Error: Las fechas actualizadas chocan con otra reserva existente.")
        conn.close()
        return

    # 5) Si ta todo bien actualiza
    cursor.execute("""
        UPDATE Reserva
        SET NumeroContacto = ?, 
            FechaLlegada = ?, 
            FechaSalida = ?, 
            NumeroPersonas = ?
        WHERE Id = ?
    """, (nuevo_contacto, nueva_fecha_llegada, nueva_fecha_salida, nuevo_num_personas, id_reserva))

    conn.commit()
    conn.close()

    print("Reserva actualizada.")


def actualizar_reserva_completa(id_reserva, nombre, documento, contacto, correo, direccion, num_personas, fecha_llegada, fecha_salida):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Reserva WHERE Id = ?", (id_reserva,))
    reserva_original = cursor.fetchone()

    if reserva_original is None:
        print("Error: No existe una reserva con ese ID.")
        conn.close()
        return

    # Validaciones básicas
    if not contacto or not num_personas or not fecha_llegada or not fecha_salida:
        print("Error: Campos obligatorios incompletos.")
        conn.close()
        return

    if not fechas_validas(fecha_llegada, fecha_salida):
        print("Error: Las fechas no son válidas.")
        conn.close()
        return

    cursor.execute("""
        UPDATE Reserva
        SET NombreCliente = ?, Documento = ?, NumeroContacto = ?, Correo = ?, Direccion = ?, NumeroPersonas = ?, FechaLlegada = ?, FechaSalida = ?
        WHERE Id = ?
    """, (nombre, documento, contacto, correo, direccion, num_personas, fecha_llegada, fecha_salida, id_reserva))

    conn.commit()
    conn.close()

    print("Reserva actualizada (completa).")



def eliminar_reserva(id_reserva):
    # Eliminación sin interacción por consola para uso desde UI
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Reserva WHERE Id = ?", (id_reserva,))
    conn.commit()
    conn.close()

    print("Reserva eliminada")


def confirmar_reserva_por_id(id_reserva):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE Reserva SET Estado = 1 WHERE Id = ?", (id_reserva,))
    conn.commit()
    conn.close()
    
