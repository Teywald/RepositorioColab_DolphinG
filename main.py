from modulos.CRUD import (
    crear_reserva,
    obtener_reservas,
    actualizar_reserva,
    eliminar_reserva
)
from modulos.buscador import buscar_y_mostrar_reserva

from modulos.CRUD import inicializar_bd
inicializar_bd()

def menu():
    print("""
==========================
    SISTEMA DE RESERVAS  
==========================

1. Crear reserva
2. Ver todas las reservas
3. Buscar reserva por ID
4. Actualizar reserva
5. Eliminar reserva
0. Salir

""")


def main():
    while True:
        menu()
        opcion = input("Seleccione una opción: ")


        if opcion == "1":
            print("\n--- CREAR RESERVA ---")
            nombre = input("Nombre del cliente: ")
            documento = input("Documento: ")
            contacto = input("Número de contacto: ")
            correo = input("Correo: ")
            direccion = input("Dirección: ")
            num_personas = input("Número de personas: ")
            fecha_llegada = input("Fecha llegada (YYYY-MM-DD): ")
            fecha_salida = input("Fecha salida (YYYY-MM-DD): ")


            try:
                num_personas = int(num_personas)
            except:
                print("Error: Número de personas inválido.")
                continue

            crear_reserva(nombre, documento, contacto, correo, direccion,
                          num_personas, fecha_llegada, fecha_salida)


        elif opcion == "2":
            print("\n--- TODAS LAS RESERVAS ---\n")
            reservas = obtener_reservas()
            if not reservas:
                print("No hay reservas registradas.\n")
            else:
                for r in reservas:
                    print(f"ID: {r[0]} | Cliente: {r[1]} | Llegada: {r[7]} | Salida: {r[8]}")
                print()


        elif opcion == "3":
            print("\n--- BUSCAR RESERVA ---")
            buscar_y_mostrar_reserva()


        elif opcion == "4":
            print("\n--- ACTUALIZAR RESERVA ---")
            try:
                id_res = int(input("ID de la reserva a actualizar: "))
            except:
                print("Error: ID inválido.")
                continue

            nuevo_contacto = input("Nuevo número de contacto: ")
            nueva_fecha_llegada = input("Nueva fecha llegada (YYYY-MM-DD): ")
            nueva_fecha_salida = input("Nueva fecha salida (YYYY-MM-DD): ")

            nuevo_num_personas = input("Nuevo número de personas: ")

            try:
                nuevo_num_personas = int(nuevo_num_personas)
            except:
                print("Error: Número de personas inválido.")
                continue

            actualizar_reserva(id_res, nuevo_contacto, nueva_fecha_llegada,
                               nueva_fecha_salida, nuevo_num_personas)


        elif opcion == "5":
            print("\n--- ELIMINAR RESERVA ---")
            try:
                id_res = int(input("ID de la reserva a eliminar: "))
            except:
                print("Error: ID inválido.")
                continue

            eliminar_reserva(id_res)

        # -------------------------------
        # 0. SALIR
        # -------------------------------
        elif opcion == "0":
            print("\nSaliendo del sistema... ")
            break

        else:
            print("Opción no válida. Intente de nuevo.\n")


if __name__ == "__main__":
    main()
