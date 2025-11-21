from manejo_archivos import inventory, save_inventory_csv

# Lista para almacenar los productos del inventario
#inventory = []
# Variables para diseño de la tabla
azul = "\033[34m" # color azul
reset = "\033[0m" # reset color
header = f"{azul}{'\nID':<15}{'PRODUCTO':<15}{'PRECIO':<15}{'CANTIDAD':<15}{reset}" # encabezado de tabla
line = f"{'-' * len(header)}" # línea separadora

# ------- AGREGAR PRODUCTO ------
def agregar_producto():

    # Asignamos un ID automático a cada producto
    id_product = len(inventory) + 1
    
    # Solicitamos nombre del producto y validamos que no esté vacío
    name = input("Ingrese nombre del producto: ")
    while name == "":
        name = input("Ingrese un nombre válido: ")

    # Solicitamos precio y validamos que sea numérico, mayor o igual a 0 y no esté vacío
    price = input("Ingrese precio: ")

    while not price.replace('.', '', 1).isnumeric() or float(price) < 0 or price == "":
        price = input("Ingrese un precio válido: ")
    # Si es válido convertimos a float
    price = float(price)

    # Solicitamos cantidad y validamos que sea numérico, mayor a 0 y no esté vacío
    quantity = input("Ingrese cantidad: ")

    while not quantity.isnumeric() or int(quantity) <= 0 or quantity == "":
        quantity = input("Ingrese una cantidad válida: ")
    # Si es válido convertimos a int
    quantity = int(quantity)

    # Agregamos el producto al inventario
    inventory.append({"id_product" : id_product, "name" : name, "price" : price, "quantity" : quantity})

    # Guardamos el inventario actualizado en el archivo CSV
    save_inventory_csv(inventory)

    # Imprimimos confirmación y encabezado de tabla
    print("\nProducto ingresado con éxito.")
    print(f"{azul}{header}")
    print(line)

    last_product = inventory[-1] # obtenemos el último producto agregado
    # Imprimimos el último producto agregado
    print(f'{last_product["id_product"]:<15}{last_product["name"]:<15}{last_product["price"]:<15}{last_product["quantity"]:<15}\n')
    

# ------- EDITAR PRODUCTO ------
def editar_producto():

    
    # Manejo de errores para asegurar que el ID es un número
    try:
        id_product_editar = int(input("Ingrese el ID del producto a actualizar: "))
    except ValueError:
        print("Error: El ID debe ser un número entero.")
        return

    # 1. Buscar el paciente (usando la función auxiliar)
   
    producto_encontrado = None

    for pro in inventory:
        if int(pro["id_product"]) == id_product_editar:
            producto_encontrado = pro
            break
        
    # si no se encuentra el paciente,regresar al menú principal
    if producto_encontrado is None:
        print(f"No se encontró ningún producto con ID {id_product_editar}")
        return
    
    show_product(producto_encontrado)

    print("\n¿Qué Dato deseas Actualizar?")
    print("1) Nombre")
    print("2) Precio")
    print("3) Cantidad")
    print("0) Cancelar")
   
    opcion_editar = input("Seleccione una opción (0-3): ").strip()

    if opcion_editar == '0':
        print("Edición cancelada.")
        return
    
    # --- Actualizar Nombre ---
    elif opcion_editar == '1':

        nuevo_nombre = (input(f"Nombre actual: {producto_encontrado['name']}. Ingrese el nuevo nombre: "))
        producto_encontrado['name'] = nuevo_nombre

        # Guardamos el inventario actualizado en el archivo CSV
        save_inventory_csv(inventory)
      
        print("\nNombre actualizado correctamente.")
        show_product(producto_encontrado)

    # --- Actualizar Precio ---
    elif opcion_editar == '2':
        while True:
            nuevo_precio = input(f"Precio actual: {producto_encontrado['price']}. Ingrese el nuevo precio: ")
            if not nuevo_precio.replace('.', '', 1).isnumeric() or float(nuevo_precio) < 0 or nuevo_precio == "":
                print("Ingrese un precio válido.")
            else:
                producto_encontrado['price'] = float(nuevo_precio)

                # Guardamos el inventario actualizado en el archivo CSV
                save_inventory_csv(inventory)
              
                print("Precio actualizado correctamente.")
                print("\n Producto Encontrado. Datos Actuales:")
                show_product(producto_encontrado)
                break

    # --- Actualizar Cantidad ---
    elif opcion_editar == '3':
        while True:
            nueva_cantidad = input(f"Cantidad actual: {producto_encontrado['quantity']}. Ingrese la nueva cantidad: ")
            if not nueva_cantidad.isnumeric() or int(nueva_cantidad) <= 0 or nueva_cantidad == "":
                print("Ingrese una cantidad válida.")
            else:
                producto_encontrado['quantity'] = int(nueva_cantidad)

                # Guardamos el inventario actualizado en el archivo CSV
                save_inventory_csv(inventory)
              
                print("\nCantidad actualizada correctamente.")
                show_product(producto_encontrado)
                break

    else:
        print("Error, opción no válida.")


# ------- ELIMINAR PRODUCTO ------
def eliminar_producto():
    try:
        id_product_delete = input("Ingrese el ID del producto que desea eliminar: ")
    except ValueError:
        print("Error: El ID debe ser un número entero.")
        return

    # 1. Buscar el producto (usando la función auxiliar)
    producto_encontrado = None

    show_all_products(inventory)  # Depuración: Mostrar el inventario cargado

    for p in inventory:
        if p["id_product"] == id_product_delete:
            producto_encontrado = p
            break
        
    # si no se encuentra el paciente,regresar al menú principal
    if producto_encontrado is None:
        print(f"No se encontró ningún producto con ID {id_product_delete}")
        return
    
    # 2. Mostrar datos actuales del producto
    print("\n Producto Encontrado. Datos Actuales:")
    show_product(producto_encontrado)
    confirmar_eliminacion(producto_encontrado)


# ------- LISTAR PRODUCTOS ------
def listar_productos():
    if not inventory:
        print("No hay productos en el inventario.")
        return

    print(f"{azul}{header}")
    print(line)
    for producto in inventory:
        print(f'{producto["id_product"]:<15}{producto["name"]:<15}{producto["price"]:<15}{producto["quantity"]:<15}')


# ------- FUNCIONES AUXILIARES ------
    
# Mostrar un producto en formato tabla
def show_product(producto):
    print(f"{azul}{header}")
    print(line)
    print(f'{producto["id_product"]:<15}{producto["name"]:<15}{producto["price"]:<15}{producto["quantity"]:<15}\n')

# Mostrar todos los productos en formato tabla
def show_all_products(inventory):
    print(f"{azul}{header}")
    print(line)
    for producto in inventory:
        print(f'{producto["id_product"]:<15}{producto["name"]:<15}{producto["price"]:<15}{producto["quantity"]:<15}')

# Confirmar eliminación de un producto
def confirmar_eliminacion(producto_encontrado):
    print("\n¿Seguro que desea eliminar este producto?")
   
    opcion_editar = input("1) Sí, eliminar \n0) Cancelar").strip()

    while not opcion_editar in ['0', '1']:
        print("Error, opción no válida.")
        opcion_editar = input("1) Sí, eliminar \n0) Cancelar").strip()

    if opcion_editar == '0':
        print("Edición cancelada.")
        return
    elif opcion_editar == '1':
        inventory.remove(producto_encontrado)
        # Guardamos el inventario actualizado en el archivo CSV
        save_inventory_csv(inventory)
        print("El producto ha sido eliminado.")