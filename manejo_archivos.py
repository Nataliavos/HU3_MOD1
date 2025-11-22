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


def cargar_csv(ruta: str) -> tuple[list[dict], int]:
    """
    Lee un archivo CSV externo con encabezado: nombre,precio,cantidad
    Valida cada fila y devuelve:
      - una lista de productos válidos con estructura: {"name", "price", "quantity"}
      - la cantidad de filas inválidas que fueron omitidas
    """
    productos: list[dict] = []
    filas_invalidas = 0

    try:
        with open(ruta, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Validamos que el archivo tenga encabezados
            if reader.fieldnames is None:
                print("Error: el archivo no tiene encabezado.")
                return [], 0

            # Normalizamos encabezados a minúsculas y sin espacios
            headers_normalizados = [h.strip().lower() for h in reader.fieldnames]
            encabezado_esperado = ["nombre", "precio", "cantidad"]

            # Validamos que el encabezado sea exactamente nombre,precio,cantidad
            if headers_normalizados != encabezado_esperado:
                print("Error: el archivo debe tener el encabezado exactamente: 'nombre,precio,cantidad'.")
                return [], 0

            # Recorremos las filas de datos
            for fila in reader:
                try:
                    # Extraemos campos y validamos que no estén vacíos
                    nombre = (fila.get("nombre") or "").strip()
                    precio_str = (fila.get("precio") or "").strip()
                    cantidad_str = (fila.get("cantidad") or "").strip()

                    if not nombre or not precio_str or not cantidad_str:
                        filas_invalidas += 1
                        continue

                    # Convertimos a tipos numéricos
                    precio = float(precio_str)
                    cantidad = int(cantidad_str)

                    # Validamos que no sean negativos
                    if precio < 0 or cantidad < 0:
                        filas_invalidas += 1
                        continue

                    # Si todo está bien, agregamos el producto en el formato interno
                    productos.append({
                        "name": nombre,
                        "price": precio,
                        "quantity": cantidad,
                    })

                except ValueError:
                    # Error en la conversión numérica de esta fila → la omitimos
                    filas_invalidas += 1
                    continue

        return productos, filas_invalidas

    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{ruta}'.")
    except UnicodeDecodeError:
        print(f"Error: no se pudo leer el archivo '{ruta}' por un problema de codificación (UTF-8 esperado).")
    except Exception as e:
        print(f"Error inesperado al cargar el archivo CSV: {e}")

    # Si hubo algún error grave, devolvemos listas vacías
    return [], 0