import sqlite3
from config import DB_PATH

def obtener_parametros_servicios():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ParametrosCotizacion")
    parametrosCotizacion = cursor.fetchall()

    conn.close()
    return parametrosCotizacion

def actualizar_parametros_servicios(id_parametros_cotizacion, valor_noche_cabana_temp_alta, valor_noche_cabana_temp_baja, valor_cocinera, valor_aux_cocina, deposito):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1) Verifica si la reserva existe, sino paila
    cursor.execute("SELECT * FROM ParametrosCotizacion WHERE Id = ?", (id_parametros_cotizacion,))
    parametros_cotizacion_original = cursor.fetchone()

    if parametros_cotizacion_original is None:
        print("Error: No existe una reserva con ese ID.")
        conn.close()
        return

    # 2) Valida campos obligatorios
    if not valor_noche_cabana_temp_alta or not valor_noche_cabana_temp_baja or not valor_cocinera or not valor_aux_cocina or not deposito:
        print("Error: Todos los campos son obligatorios para actualizar.")
        conn.close()
        return

    # 3) Si ta todo bien actualiza
    cursor.execute("""
        UPDATE ParametrosCotizacion
        SET ValorNocheCabanaTempAlta = ?,
        ValorNocheCabanaTempBaja = ?,
        ValorCocinera = ?,
        ValorAuxCocina = ?,
        Deposito = ?
        WHERE Id = ?
    """, (valor_noche_cabana_temp_alta, valor_noche_cabana_temp_baja, valor_cocinera, valor_aux_cocina, deposito, id_parametros_cotizacion))

    conn.commit()
    conn.close()

    print("Paramteros actualizados.")