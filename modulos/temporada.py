import sqlite3

DB_PATH = "database/dolphin_green.db"

from CRUD import fechas_validas

def crear_temporada(nombre, fecha_inicio, fecha_fin):
    # 1) Valido campos obligatorios
    if not nombre or not fecha_inicio or not fecha_fin:
        print("Error: Los campos obligatorios deben estar completos.")
        return

    # 2) Veo que si sean fechas fechas
    if not fechas_validas(fecha_inicio, fecha_fin):
        print("Error: Las fechas no son válidas.")
        return

    # Inserto en BD
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Temporada (
            Id, Nombre, FechaInicio, FechaFin
        ) VALUES (?, ?, ?)
    """, (nombre, fecha_inicio, fecha_fin))

    conn.commit()
    conn.close()

    print("Temporada creada.")
    
def obtener_temporadas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Temporada")
    temporada = cursor.fetchall()

    conn.close()
    return temporada

def actualizar_temporada(id_temporada, nuevo_nombre, nueva_fecha_inicio, nueva_fecha_fin):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1) Verifica si la temporada existe, sino paila
    cursor.execute("SELECT * FROM Reserva WHERE Id = ?", (id_temporada,))
    temporada_original = cursor.fetchone()

    if temporada_original is None:
        print("Error: No existe una temporada con ese ID.")
        conn.close()
        return

    # 2) Valida campos obligatorios
    if not nuevo_nombre or not nueva_fecha_inicio or not nueva_fecha_fin:
        print("Error: Todos los campos son obligatorios para actualizar.")
        conn.close()
        return

    # 3) Valida fechas
    if not fechas_validas(nueva_fecha_inicio, nueva_fecha_fin):
        print("Error: Las fechas no son válidas.")
        conn.close()
        return

    # 4) Si ta todo bien actualiza
    cursor.execute("""
        UPDATE Reserva
        SET Nombre = ?,
            FechaInicio = ?,
            FechaFin = ?
        WHERE Id = ?
    """, (nuevo_nombre, nueva_fecha_inicio, nueva_fecha_fin))

    conn.commit()
    conn.close()

    print("Temporada actualizada.")

def elimar_temporada(id_temporada):
    confirm = input(f"¿Seguro que deseas eliminar la temporada {id_temporada}? (s/n): ")

    if confirm.lower() != "s":
        print("Operación cancelada.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Temporada WHERE Id = ?", (id_temporada,))
    conn.commit()
    conn.close()

    print("Temporada eliminada    ")