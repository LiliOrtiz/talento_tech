import sqlite3  # motor de bases de datos relacionles
import funciones
from colorama import Fore, init

init(autoreset=True)

def crear_conexion():
    conexion = None
    try:
        conexion = sqlite3.connect("inventario.db")
           
    except sqlite3.Error as e:       
        print(Fore.RED + "¡UPS! Hubo un error inesperado en la conexion 😨 )", e)    
    return conexion

def crear_tabla(conexion):
    sql_crear_tabla = """
                   CREATE TABLE IF NOT EXISTS productos (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nombre TEXT NOT NULL,
                   descripcion TEXT,
                   cantidad INTEGER NOT NULL CHECK(cantidad > 1),
                   precio REAL NOT NULL,
                   categoria TEXT
                    )
                """
    # CREACION DE TABLA
    try:
        cursor = conexion.cursor()
        cursor.execute(sql_crear_tabla)
        
    except sqlite3.Error as e:
        print(Fore.RED + "Hubo un error al crear la tabla", e)

def agregar_producto(conexion, producto):    
    sql_agregar = """INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) VALUES (?,?,?,?,?)"""
    try:
        cursor = conexion.cursor()
        cursor.execute(sql_agregar, producto)
        print(Fore.GREEN +"\n✅ ¡Producto agregado con éxito! :) ")
        conexion.commit()
    except sqlite3.Error as e:
        print(Fore.RED +"Error al agregar producto: ", e)
 

def mostrar_productos(conexion):
    sql_mostrar = """SELECT id, nombre, descripcion, cantidad, precio, 
    categoria FROM productos"""
    try:
        cursor = conexion.cursor()
        cursor.execute(sql_mostrar)

        productos = cursor.fetchall()

        if not productos:
            print(Fore.YELLOW+ "[INFO] No hay PRODUCTOS "
            "registrados en la base de datos.")
        else:
            print(Fore.GREEN + "\n=== Lista de Productos ===")
            for product in productos:
                print(
                    Fore.WHITE +
                    f"ID: {product[0]}, Nombre: {product[1]}, Descripcion: {product[2]}, Cantidad: {product[3]}, Precio: {product[4]}, Categoria: {product[5]}" )
        
    except sqlite3.Error as e:
        print(Fore.RED +"Error al mostrar producto: ", e)
    
def buscar_productos(conexion):
    sql_ID = "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?"
    sql_nombre = "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE nombre = ?"

    try:
        cursor = conexion.cursor()

        print("1. Busqueda por ID")
        print("2. Busqueda por nombre")
        opcion = funciones.pedir_texto("Seleccioná una opción: ")

        if opcion == "1":
            id_busqueda = funciones.pedir_texto("Ingresá el ID del producto a buscar: ")
            cursor.execute(sql_ID,id_busqueda)    
            productos = cursor.fetchall()

            if not productos:
                print(Fore.YELLOW + "[INFO] No se encontraron productos con ese ID.")

            else:
                print(
                    Fore.GREEN + f"\nProducto ENCONTRADO")
                for product in productos:
                    print(
                        Fore.WHITE
                        + f"ID: {product[0]}, Nombre: {product[1]}, Descripcion: {product[2]}, Cantidad: {product[3]}, Precio: {product[4]}, Categoria: {product[5]}" )
                    
        elif opcion == "2":
            nombre_busqueda = funciones.pedir_texto("Ingresá el nombre del producto a buscar: ").capitalize()
            cursor.execute(sql_nombre, (nombre_busqueda,))
            productos = cursor.fetchall()

            if not productos:
                print(Fore.YELLOW + "[INFO] No se encontraron productos con ese nombre.")

            else:
                print(
                    Fore.GREEN + f"\nProducto ENCONTRADO")
                for product in productos:
                    print(
                        Fore.WHITE
                        + f"ID: {product[0]}, Nombre: {product[1]}, Descripcion: {product[2]}, Cantidad: {product[3]}, Precio: {product[4]}, Categoria: {product[5]}" )
                    
        else:
            print(Fore.RED + "[ERROR] Opción no válida.")

    except sqlite3.Error as e:
        print(
            Fore.RED + f"[ERROR] Ocurrió un problema al consultar la base de datos: {e}"
        )
  
def actualizar_producto(conexion):
    sql_1 = "SELECT * FROM productos WHERE id = ?"
    sql_2 = "UPDATE productos SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? WHERE id = ?"

    cursor = conexion.cursor()

    try:
        id_producto = funciones.verifica_digito("Ingrese el ID del producto a actualizar: ")

        cursor.execute(sql_1, (id_producto,))
        producto = cursor.fetchone()
        if not producto:
            print(Fore.YELLOW + "[INFO] No se encontró un producto con ese ID.")           
            
        
        print(Fore.CYAN + "\n=== Datos actuales del producto ===")
        print(Fore.WHITE +
              f"Nombre: {producto[1]}\n"
              f"Descripción: {producto[2]}\n"
              f"Cantidad: {producto[3]}\n"
              f"Precio: {producto[4]}\n"
              f"Categoría: {producto[5]}\n")

        print(Fore.GREEN + "Dejá vacío el campo que NO quieras modificar.\n")

        #Pedir nuevos datos (vacío = mantener)
        nuevo_nombre = input("Nuevo nombre: ").strip()
        nuevo_descripcion = input("Nueva descripción: ").strip()
        nuevo_cantidad = input("Nueva cantidad: ").strip()
        nuevo_precio = input("Nuevo precio: ").strip()
        nuevo_categoria = input("Nueva categoría: ").strip()

        #Reemplazar solo si se ingresó algo
        nombre_final = nuevo_nombre.capitalize() if nuevo_nombre else producto[1]
        descripcion_final = nuevo_descripcion if nuevo_descripcion else producto[2]
        cantidad_final = int(nuevo_cantidad) if nuevo_cantidad.isdigit() else producto[3]
        precio_final = float(nuevo_precio) if nuevo_precio.replace('.', '', 1).isdigit() else producto[4]
        categoria_final = nuevo_categoria if nuevo_categoria else producto[5]

        #Actualizar en la base
        sql_actualizar = sql_2

        cursor.execute(sql_actualizar, (
            nombre_final,
            descripcion_final,
            cantidad_final,
            precio_final,
            categoria_final,
            id_producto
        ))

        conexion.commit()
        print(Fore.GREEN + "\n✔ ¡Producto actualizado con éxito!")

    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] Ocurrió un problema al actualizar: {e}")

def eliminar_productos(conexion):
    sql = "DELETE FROM productos WHERE id = ?"
    sql_ID = "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?"
    
    try:
        cursor = conexion.cursor()
        id_producto = funciones.verifica_digito("Ingrese el ID del producto a eliminar: ")

        cursor.execute(sql_ID, (id_producto,))
        productos = cursor.fetchall()

        if not productos:
            print(Fore.YELLOW + "[INFO] No se encontraron productos con ese ID.")
            return

        print(Fore.GREEN + f"\nProducto ENCONTRADO")
        for product in productos:
            print(
                Fore.WHITE +
                f"ID: {product[0]}, Nombre: {product[1]}, Descripcion: {product[2]}, "
                f"Cantidad: {product[3]}, Precio: {product[4]}, Categoria: {product[5]}"
            )

        print("\n¿Está seguro que quiere eliminar este producto?")
        print("1 - SI")
        print("2 - NO")
        op = funciones.verifica_digito("Seleccione una opción: ")

        if op == 1:
            cursor.execute(sql, (id_producto,)) 
            conexion.commit()
            print(Fore.GREEN + "\n✔ ¡Producto eliminado con éxito!")
        else:
            print("Producto no eliminado")
            return  # vuelve al menú

    except sqlite3.Error as e:
        print(Fore.RED + f"[ERROR] Ocurrió un problema al eliminar: {e}")