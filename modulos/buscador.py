from modulos.CRUD import buscar_reserva


DB_PATH = "database/dolphin_green.db"


def mostrar_reserva_formateada(reserva):
    """
    Recibe una tupla con los datos de la reserva y la imprime formateada.
    """
    (
        id_reserva,
        nombre,
        documento,
        contacto,
        correo,
        direccion,
        num_personas,
        fecha_llegada,
        fecha_salida
    ) = reserva

    print("\n======= DETALLE DE LA RESERVA =======")
    print(f"ID Reserva:      {id_reserva}")
    print(f"Cliente:         {nombre}")
    print(f"Documento:       {documento}")
    print(f"Contacto:        {contacto}")
    print(f"Correo:          {correo}")
    print(f"Dirección:       {direccion}")
    print(f"Personas:        {num_personas}")
    print(f"Fecha Llegada:   {fecha_llegada}")
    print(f"Fecha Salida:    {fecha_salida}")
    print("=====================================\n")


def buscar_y_mostrar_reserva():
    """
    Función principal para HU03:
    Permite ingresar un ID, verificarlo y mostrar detalladamente la reserva.
    """
    try:
        id_reserva = int(input("Ingrese el ID de la reserva que desea consultar: "))
    except ValueError:
        print("Error: El ID debe ser un número entero.")
        return

    reserva = buscar_reserva(id_reserva)

    if reserva is None:
        print(f"No existe ninguna reserva con el ID {id_reserva}.")
        return

    mostrar_reserva_formateada(reserva)
    print("Información desplegada.\n")
