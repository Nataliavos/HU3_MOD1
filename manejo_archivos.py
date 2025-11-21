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



def save_inventory_csv(inventory: list[dict]):
    try:
        with open('inventory.csv', 'w', newline='', encoding='utf-8') as file:
            if inventory:
                fieldnames = inventory[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(inventory)
    except Exception as e:
        print(f"Error al guardar inventario como CSV: {e}")