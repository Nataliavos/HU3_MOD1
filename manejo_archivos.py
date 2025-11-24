import os
import csv

def load_inventory_csv() -> list[dict]:
     try:
         with open('inventory.csv', 'r', encoding='utf-8') as file:
             reader = csv.DictReader(file)
             inventory = list(reader)
     except Exception as e:
         inventory = []
     return inventory

inventory = load_inventory_csv()



def save_inventory_csv(inventory: list[dict], ruta: str = 'inventory.csv') -> None:
    try:
        with open(ruta, 'w', newline='', encoding='utf-8') as file:
            if inventory:
                fieldnames = inventory[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(inventory)

        print(f"Inventario actualizado correctamente en '{ruta}'")
    except Exception as e:
        print(f"Error al guardar inventario como CSV: {e}")


def cargar_csv(ruta):
    """
    Lee un archivo CSV externo y devuelve:
        (productos_validos, filas_invalidas)

    El archivo debe tener **exactamente** este encabezado (en este orden):

        name,price,quantity

    Ejemplo de archivo válido:
        name,price,quantity
        Lapicero,1.2,10
        Cuaderno,3.5,5
        Borrador,0.8,20
    """

    if not os.path.exists(ruta):
        print("Error: el archivo no existe.")
        return [], 0

    productos = []
    filas_invalidas = 0

    with open(ruta, mode="r", encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)

        encabezados_esperados = ["name", "price", "quantity"]

        # Validación estricta del encabezado
        if lector.fieldnames != encabezados_esperados:
            print("Error: el archivo debe tener el encabezado exactamente: 'name,price,quantity'.")
            print(f"Encabezados encontrados: {lector.fieldnames}")
            return [], 0

        # Procesar filas
        for numero_fila, fila in enumerate(lector, start=2):  # start=2 porque la fila 1 es el encabezado
            try:
                name = (fila["name"] or "").strip()
                price_str = (fila["price"] or "").strip()
                quantity_str = (fila["quantity"] or "").strip()

                if not name:
                    raise ValueError("Nombre vacío")

                # Convertir tipos
                price = float(price_str)
                quantity = int(quantity_str)

                if price < 0:
                    raise ValueError("Precio negativo")
                if quantity <= 0:
                    raise ValueError("Cantidad debe ser mayor que 0")

                productos.append({
                    "name": name,
                    "price": price,
                    "quantity": quantity,
                })

            except Exception as e:
                filas_invalidas += 1
                print(f"  ⚠ Fila {numero_fila} inválida ({e}). Datos: {fila}")
                continue

    return productos, filas_invalidas