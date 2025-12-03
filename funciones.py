from colorama import Fore, Back, init

init(autoreset=True)



def menu_de_inicio():
    print("\n=== GESTION DE PRODUCTOS ===" \
    "\n1. Registrar producto" \
    "\n2. Mostrar productos" \
    "\n3. Actualizar producto" \
    "\n4. Buscar producto" \
    "\n5. Eliminar producto" \
    "\n6. Salir del programa")

def mensaje_vacio():
    print(Fore.RED + "Esta información no puede quedar vacia o ingresar valores incorrectos")

def pedir_texto(texto):
    dato = input(texto).strip()
    while not dato:
        mensaje_vacio()
        dato = input(texto).strip()
    return dato

def menu_inicio_opciones(msje_pedir):    
    numero = input(msje_pedir).strip()

    # Validar que sea dígito
    while not numero.isdigit():
        mensaje_vacio()
        numero = input(msje_pedir).strip()

    numero = int(numero)

    # Validar rango del menú
    while numero < 1 or numero > 6:
        print("\nDebe ingresar una opción del 1 al 6 !")
        numero = input(msje_pedir).strip()

        while not numero.isdigit():
            mensaje_vacio()
            numero = input(msje_pedir).strip()

        numero = int(numero)

    return int(numero)

def verifica_digito(digito):
    numero = input(digito).strip()
    while not numero.isdigit():
        mensaje_vacio()
        numero = input(digito).strip()
    return int(numero)

