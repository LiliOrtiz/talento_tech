import funciones, base_de_datos
from colorama import Fore, init

init(autoreset=True)

opcion = 0
productos=[] #BORRARBLE

con = base_de_datos.crear_conexion()
base_de_datos.crear_tabla(con)


while opcion != 6:
    funciones.menu_de_inicio()

    opcion = funciones.menu_inicio_opciones("\nSeleccione una opción: ")

    #SALIR
    if opcion == 6:
        print("saliendo del programa")
        con.close()
        break    

    #OPCIÓN 1: AGREGAR PRODUCTOS
    elif opcion == 1:
        print(Fore.CYAN +"▬▬▬Agregar producto▬▬▬")

        nombre = funciones.pedir_texto("Ingrese nombre del producto: ").capitalize()
        descripcion = input("Ingrese la descripción del producto: ")
        cantidad = funciones.verifica_digito("Ingrese la cantidad del producto: ")
        precio = funciones.verifica_digito("Ingrese el precio del producto:")
        categoria = input ("Ingrese la categoria del producto:")

        if not descripcion:
            descripcion = "Sin descripción"
        if not categoria:
            categoria = "Sin categoría"

        datos_del_producto = (nombre, descripcion, cantidad, precio, categoria)

        base_de_datos.agregar_producto(con, datos_del_producto)        
        print("\n✅ ¡Producto agregado con éxito! :) ")             
                        
    
    elif opcion == 2:
        base_de_datos.mostrar_productos(con)

    elif opcion == 3:
        base_de_datos.actualizar_producto(con)

    elif opcion == 4:
        base_de_datos.buscar_productos(con)
    
    elif opcion == 5:
        base_de_datos.eliminar_productos(con)