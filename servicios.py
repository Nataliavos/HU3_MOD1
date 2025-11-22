from manejo_archivos import inventory, save_inventory_csv, cargar_csv

# Lista para almacenar los productos del inventario
#inventory = []
# Variables para diseño de la tabla
azul = "\033[34m" # color azul
reset = "\033[0m" # reset color
header = f"{azul}{'\nID':<15}{'PRODUCTO':<15}{'PRECIO':<15}{'CANTIDAD':<15}{reset}" # encabezado de tabla
line = f"{'-' * len(header)}" # línea separadora

def generate_new_id():
    # Si el inventario está vacío, el id será 1, si no, será el máximo id + 1
    if not inventory:
        return 1
    return max(int(p["id_product"]) for p in inventory) + 1
    
# ------- AGREGAR PRODUCTO ------
def agregar_producto():

    # Asignamos un ID automático a cada producto
    id_product = generate_new_id()
    
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

    # Imprimimos confirmación y encabezado de tabla
    print("\nProducto ingresado con éxito.")
    print(f"{azul}{header}")
    print(line)

    last_product = inventory[-1] # obtenemos el último producto agregado
    # Imprimimos el último producto agregado
    print(f'{last_product["id_product"]:<15}{last_product["name"]:<15}{last_product["price"]:<15}{last_product["quantity"]:<15}\n')
    

# ------- BUSCAR PRODUCTO ------
def buscar_producto():
    if not inventory:
        print("No hay productos en el inventario.")
        return
    
    print("Buscar producto por:")
    print("1) ID")
    print("2) Nombre")
    
    option = input("Seleccione una opción (1-2): ").strip()
    validate_option_buscar_producto(option)


# ------- EDITAR PRODUCTO ------
def editar_producto():
    # Manejo de errores para asegurar que el ID es un número
    try:
        id_product_editar = int(input("Ingrese el ID del producto a actualizar: "))
    except ValueError:
        print("Error: El ID debe ser un número entero.")
        return

    # Buscamos el producto (usando la función auxiliar) y lo guardamos en una variable
    producto_encontrado = search_product_to(id_product_editar)
    if producto_encontrado is None:
        return
    # si se encuentra el producto: mostramos datos actuales
    print("\n Producto Encontrado:")
    show_product(producto_encontrado)

    print("\n¿Qué Dato deseas Actualizar?")
    print("1) Nombre")
    print("2) Precio")
    print("3) Cantidad")
    print("0) Cancelar")
   
    opcion_editar = input("Seleccione una opción (0-3): ").strip()
    # llamamos a la función para actualizar el dato correspondiente
    update_data(opcion_editar, producto_encontrado)



# ------- ELIMINAR PRODUCTO ------
def eliminar_producto():
    # Manejo de errores para asegurar que el ID es un número
    try:
        id_product_delete = int(input("Ingrese el ID del producto que desea eliminar: "))
    except ValueError:
        print("Error: El ID debe ser un número entero.")
        return
    
    producto_encontrado = search_product_to(id_product_delete)
    if producto_encontrado is None:
        return
    # si se encuentra el producto: mostramos datos actuales
    print("\n Producto Encontrado:")
    show_product(producto_encontrado)
    # confirmamos eliminación
    confirmar_eliminacion(producto_encontrado)


# ------- MOSTRAR ESTADÍSTICAS ------
def calculate_stats():
    if not inventory:
        print("No hay productos en el inventario.")
        return

    # Lambda para subtotal por producto (precio * cantidad)
    subtotal = lambda p: float(p["price"]) * int(p["quantity"])

    # Cantidad total de productos registrados
    cantidad_productos = len(inventory)

    # Unidades totales: suma de todas las cantidades
    unidades_totales = sum(int(p["quantity"]) for p in inventory)

    # Valor total del inventario
    valor_total = sum(subtotal(p) for p in inventory)

    # Producto más caro (por precio unitario)
    producto_mas_caro = max(inventory, key=lambda p: float(p["price"]))

    # Producto con mayor stock (por cantidad)
    producto_mayor_stock = max(inventory, key=lambda p: int(p["quantity"]))

    # === Mostrar resultados ===
    print("\n===== ESTADÍSTICAS DEL INVENTARIO =====")
    print(f"Cantidad total de productos registrados: {cantidad_productos}")
    print(f"Unidades totales en inventario:         {unidades_totales}")
    print(f"Valor total del inventario:            ${valor_total:,.2f}")

    print("\nProducto más caro:")
    print(f"  - ID:     {producto_mas_caro['id_product']}")
    print(f"  - Nombre: {producto_mas_caro['name']}")
    print(f"  - Precio: ${float(producto_mas_caro['price']):,.2f}")

    print("\nProducto con mayor stock:")
    print(f"  - ID:       {producto_mayor_stock['id_product']}")
    print(f"  - Nombre:   {producto_mayor_stock['name']}")
    print(f"  - Cantidad: {int(producto_mayor_stock['quantity'])}")

    print("\n========================================\n")


# ------- CARGAR CSV -------
def load_external_csv():
    """
    Carga productos desde un CSV externo:
      - Pide la ruta al usuario
      - Usa cargar_csv(ruta) para validar y leer productos
      - Pregunta si sobrescribe o fusiona con el inventario actual
      - Aplica la política de fusión por nombre
      - Muestra un resumen al final y guarda el inventario en 'inventory.csv'
    """
    ruta = input("Ingrese la ruta del archivo CSV a cargar (ej: productos.csv): ").strip()

    if not ruta:
        print("Ruta no válida. Operación cancelada.")
        return

    # Cargamos y validamos el archivo CSV externo
    productos_cargados, filas_invalidas = cargar_csv(ruta)

    # Si no hay productos válidos y tampoco filas inválidas, algo grave falló (ya se informó)
    if not productos_cargados and filas_invalidas == 0:
        print("No se cargaron productos desde el archivo.")
        return

    print(f"\nSe encontraron {len(productos_cargados)} productos válidos en el archivo.")
    if filas_invalidas > 0:
        print(f"Se omitieron {filas_invalidas} filas inválidas durante la carga.")

    # Preguntamos si se desea sobrescribir el inventario actual
    while True:
        opcion = input("\n¿Sobrescribir inventario actual? (S/N): ").strip().upper()
        if opcion in ("S", "N"):
            break
        print("Opción no válida. Por favor responda 'S' o 'N'.")

    # Variable para registrar la acción aplicada (para el resumen)
    accion = ""

    if opcion == "S":
        # --- SOBRESCRIBIR INVENTARIO ---
        inventory.clear()  # eliminamos todo el inventario actual

        for prod in productos_cargados:
            nuevo_id = generate_new_id()
            inventory.append({
                "id_product": nuevo_id,
                "name": prod["name"],
                "price": prod["price"],
                "quantity": prod["quantity"],
            })

        accion = "reemplazo completo del inventario"

    else:
        # --- FUSIONAR INVENTARIO ---
        # Política:
        # - Si el nombre ya existe (ignorando mayúsculas/minúsculas):
        #       * sumamos cantidades
        #       * actualizamos el precio al nuevo si es diferente
        # - Si no existe, lo agregamos como producto nuevo
        for prod in productos_cargados:
            nombre_nuevo = prod["name"].lower()

            # Buscamos si ya existe un producto con ese nombre
            existente = next(
                (p for p in inventory if p["name"].lower() == nombre_nuevo),
                None
            )

            if existente is not None:
                # Sumamos cantidades (conversión por si vienen como str desde CSV original)
                existente["quantity"] = int(existente["quantity"]) + int(prod["quantity"])

                # Si el precio es diferente, lo actualizamos al nuevo
                if float(existente["price"]) != float(prod["price"]):
                    existente["price"] = prod["price"]
            else:
                # Si no existe, lo agregamos como un nuevo producto con un ID nuevo
                nuevo_id = generate_new_id()
                inventory.append({
                    "id_product": nuevo_id,
                    "name": prod["name"],
                    "price": prod["price"],
                    "quantity": prod["quantity"],
                })

        accion = "fusión con el inventario existente"

    # Guardamos el inventario actualizado en el CSV principal del sistema
    save_inventory_csv(inventory)

    # Mostramos un resumen final
    print("\nResumen de carga de inventario:")
    print(f" - Productos válidos cargados desde el archivo: {len(productos_cargados)}")
    print(f" - Filas inválidas omitidas: {filas_invalidas}")
    print(f" - Acción aplicada sobre el inventario: {accion}\n")

   

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
        print("Eliminación cancelada.")
        return
    elif opcion_editar == '1':
        inventory.remove(producto_encontrado)
        print("El producto ha sido eliminado.")

def get_product_by_id(id_product: int) -> dict | None:

    producto_encontrado = None

    for pe in inventory:
        if int(pe["id_product"]) == id_product:
            producto_encontrado = pe
            break

    if producto_encontrado is None:
        print(f"No se encontró ningún producto con ID {id_product}")
        return

    print("\n Producto Encontrado")
    show_product(producto_encontrado)


def get_product_by_name(name: str) -> list[dict]:
    productos_encontrados = []

    for pe in inventory:
        if pe["name"].lower() == name.lower():
            productos_encontrados.append(pe)

    if not productos_encontrados:
        print(f"No se encontró ningún producto con nombre {name}")
        return

    print(f"\n Productos Encontrados con nombre '{name}':")
    for producto in productos_encontrados:
        show_product(producto)


def validate_option_buscar_producto(option: str):
    if option not in ['1', '2']:
        print("Opción no válida.")
        return
    elif option == '1':
        try:
           id_product_buscar = int(input("Ingrese el ID del producto a buscar: "))
        except ValueError:
           print("Error: El ID debe ser un número entero.")
           return
        get_product_by_id(id_product_buscar)

    elif option == '2':
        nombre_buscar = input("Ingrese el nombre del producto a buscar: ").strip().lower()
        get_product_by_name(nombre_buscar)

# Buscar producto para editar o eliminar
def search_product_to(id_product: int) -> dict | None:
    for p in inventory:
        if int(p["id_product"]) == id_product:
            return p # retornamos el producto encontrado
        
    # si no se encuentra el paciente,regresar al menú principal
    print(f"No se encontró ningún producto con ID {id_product}")
    return None
    
def update_data(opcion, producto):
    if opcion == '0':
        print("Edición cancelada.")
        return
    # --- Actualizar Nombre ---
    elif opcion == '1':
        update_name(producto)
    # --- Actualizar Precio ---
    elif opcion == '2':
        update_price(producto)
    # --- Actualizar Cantidad ---
    elif opcion == '3':
        update_quantity(producto)
    else:
        print("Error, opción no válida.")

def update_name(product):
    nuevo_nombre = (input(f"Nombre actual: {product['name']}. Ingrese el nuevo nombre: "))
    product['name'] = nuevo_nombre
      
    print("\nNombre actualizado correctamente.")
    show_product(product)

def update_price(product):
    while True:
            nuevo_precio = input(f"Precio actual: {product['price']}. Ingrese el nuevo precio: ")
            if not nuevo_precio.replace('.', '', 1).isnumeric() or float(nuevo_precio) < 0 or nuevo_precio == "":
                print("Ingrese un precio válido.")
            else:
                product['price'] = float(nuevo_precio)
              
                print("Precio actualizado correctamente.")
                print("\n Producto Encontrado:")
                show_product(product)
                break

def update_quantity(product):
    while True:
            nueva_cantidad = input(f"Cantidad actual: {product['quantity']}. Ingrese la nueva cantidad: ")
            if not nueva_cantidad.isnumeric() or int(nueva_cantidad) <= 0 or nueva_cantidad == "":
                print("Ingrese una cantidad válida.")
            else:
                product['quantity'] = int(nueva_cantidad)
              
                print("\nCantidad actualizada correctamente.")
                show_product(product)
                break