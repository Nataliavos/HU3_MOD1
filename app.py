from servicios import agregar_producto, editar_producto, listar_productos, eliminar_producto
from manejo_archivos import inventory, load_inventory_csv, save_inventory_csv


while True:
    # mostramos el menú de opciones
    print("------- GESTIÓN DE PRODUCTOS -------")
    print("1) Agregar Producto\n2) Mostrar Productos \n3) Buscar Producto\n4) Editar Producto\n5) Eliminar Producto\n6) Mostrar Estadísticas \n7) Cargar CSV \n8) Salir")

    # solicitamos la opción al usuario
    option=input("\nIngresa una opción ->").strip()

    # validamos que la entrada sea numérica y esté dentro del rango de opciones
    if not option.isnumeric() or option not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        print("Por favor ingrese una opción válida.")
        continue # volvemos a pedir el dato

    # convertimos la entrada a entero
    option = int(option)

    # usamos match para las opciones del menú. Definimos las funciones fuera del match para mayor claridad.
    # ejecutamos la función correspondiente según la opción seleccionada
    match option:
        
        case 1:
            agregar_producto()
        case 2:
            listar_productos()
        case 3:
            buscar_producto()
        case 4:
            editar_producto()
        case 5:
            eliminar_producto()
        case 6:
            calculate_stats()
        case 7:
            upload_inventory_csv()
        case 8:
            print("¡Hasta la próxima!")
            break # salimos del bucle y terminamos el programa