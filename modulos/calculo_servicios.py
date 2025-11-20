from modulos.CRUD import buscar_reserva
from datetime import datetime
import locale

# --- CONFIGURACIÓN Y COSTOS ---
COSTO_COCINERA_DIA = 150000 
COSTO_AUXILIAR_DIA = 100000

# --- CONFIGURACIÓN DE LOCALIZACIÓN ---
try:
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
except locale.Error:
    pass


# --- FUNCIONES DE UTILIDAD ---

def calcular_dias_reserva(fecha_llegada_str, fecha_salida_str):
    try:
        llegada = datetime.strptime(fecha_llegada_str, '%Y-%m-%d')
        salida = datetime.strptime(fecha_salida_str, '%Y-%m-%d')
        dias = (salida - llegada).days
        return dias if dias > 0 else 1
    except:
        return 1

# --- FUNCIONES DE DESPLIEGUE ---

def mostrar_reserva_formateada(reserva):
    (
        id_reserva,
        nombre,
        documento,
        contacto,
        correo,
        direccion,
        num_personas,
        fecha_llegada,
        fecha_salida,
        *resto_datos 
    ) = reserva 

    print("\n======= DETALLE DE LA RESERVA =======")
    print(f"ID Reserva:        {id_reserva}")
    print(f"Cliente:           {nombre}")
    print(f"Personas:          {num_personas}")
    print(f"Fecha Llegada:     {fecha_llegada}")
    print(f"Fecha Salida:      {fecha_salida}")
    print("=====================================\n")

def mostrar_desglose_servicios(servicios):
    total_servicios = sum(servicios.values())
    
    print("\n========= DESGLOSE DE SERVICIOS CALCULADOS =========")
    for servicio, valor in servicios.items():
        valor_formateado = locale.format_string("%.0f", valor, grouping=True)
        print(f"- {servicio:<20}: $ {valor_formateado}")
    
    print("--------------------------------------------------")
    total_formateado = locale.format_string("%.0f", total_servicios, grouping=True)
    print(f"TOTAL SERVICIOS ADICIONALES: $ {total_formateado}")
    print("==================================================\n")


# --- LÓGICA DE CÁLCULO ---

def calcular_servicios(reserva):
    try:
        num_personas = reserva[6]
        fecha_llegada = reserva[7]
        fecha_salida = reserva[8]
    except IndexError:
        print("Error: Estructura de reserva incorrecta.")
        return {}


    servicios = {}
    dias_reserva = calcular_dias_reserva(fecha_llegada, fecha_salida)

    print("--- Verificación de Reglas de Negocio para Servicios ---")

    # Regla Cocinera: 
    if num_personas >= 1:
        costo_cocinera = COSTO_COCINERA_DIA * dias_reserva
        servicios["Cocinera"] = costo_cocinera
        print(f"-> Cocinera: APLICA. Costo: $ {costo_cocinera:,.0f}")
    else:
        servicios["Cocinera"] = 0
        print(f"-> Cocinera: NO APLICA (Estadía corta)")


    # Regla Auxiliar:
    if num_personas >= 14:
        costo_auxiliar = COSTO_AUXILIAR_DIA * dias_reserva
        servicios["Auxiliar de Cocina"] = costo_auxiliar
        print(f"-> Auxiliar: APLICA. Costo: $ {costo_auxiliar:,.0f}")
    else:
        servicios["Auxiliar de Cocina"] = 0
        print(f"-> Auxiliar: NO APLICA (Menos de 14 personas)")
        
    return servicios

# --- FUNCIÓN PRINCIPAL ---

def ejecutar_calculo_servicios():
    try:
        id_reserva = int(input("\nIngrese el ID de la reserva para calcular servicios: "))
    except ValueError:
        print("Error: El ID debe ser un número entero.")
        return

    # 1. Busca la reserva 
    reserva = buscar_reserva(id_reserva)

    if reserva is None:
        print(f"No existe ninguna reserva con el ID {id_reserva}.")
        return

    # 2. Muestra la información básica
    mostrar_reserva_formateada(reserva)

    # 3. Calcula los servicios
    servicios_calculados = calcular_servicios(reserva)

    # 4. Muestra el desglose
    mostrar_desglose_servicios(servicios_calculados)
    
    print("Cálculo automático de servicios completado.\n")