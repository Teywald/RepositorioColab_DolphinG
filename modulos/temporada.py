import sqlite3
from modulos.config import DB_PATH
from modulos.CRUD import fechas_validas

def crear_temporada(nombre, fecha_inicio, fecha_fin):

    if not nombre or not fecha_inicio or not fecha_fin:
        print("Error: Los campos obligatorios deben estar completos.")
        return

    if not fechas_validas(fecha_inicio, fecha_fin):
        print("Error: Las fechas no son válidas.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Temporada (Nombre, FechaInicio, FechaFin)
        VALUES (?, ?, ?)
    """, (nombre, fecha_inicio, fecha_fin))

    conn.commit()
    conn.close()
    print("Temporada creada.")


def obtener_temporadas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Temporada")
    temporadas = cursor.fetchall()
    conn.close()
    return temporadas


def actualizar_temporada(id_temporada, nombre, fecha_inicio, fecha_fin):

    if not nombre or not fecha_inicio or not fecha_fin:
        print("Error: Todos los campos son obligatorios.")
        return

    if not fechas_validas(fecha_inicio, fecha_fin):
        print("Error: Fechas inválidas.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Temporada
        SET Nombre = ?, FechaInicio = ?, FechaFin = ?
        WHERE Id = ?
    """, (nombre, fecha_inicio, fecha_fin, id_temporada))

    conn.commit()
    conn.close()
    print("Temporada actualizada.")


def eliminar_temporada(id_temporada):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Temporada WHERE Id = ?", (id_temporada,))
    conn.commit()
    conn.close()

    print("Temporada eliminada.")