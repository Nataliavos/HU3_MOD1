from Moodle.Historias_usuario.Mod1_semana3.app import Inventory
import csv
import permanencia_archivos as pa

all_products = []

# convertir productos a csv
def convert_product_to_csv(listofproduct):
    file = open("products.csv", "w")
    file.write("")
    file.close()
    for p in listofproduct:
        f = open("products.csv", "a")
        f.write(f"{p.id},{p.name},{p.price},{p.quant}\n")
        f.close()

# convertir csv a lista de producto
def convert_csv_to_product_list():
    all_products = []