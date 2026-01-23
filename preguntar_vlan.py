while True:
    vlan = int(input("Ingrese el número de VLAN (0 para salir): "))

    if vlan == 0:
        print("Programa finalizado.")
        break

    if vlan >= 1 and vlan <= 1005:
        print("VLAN 1 a 1005 pertenece a rango NORMAL\n")
    elif vlan >= 1006 and vlan <= 4094:
        print("VLAN 1006 a 4094 es 2de rango EXTENDIDO\n")
    else:
        print("No corresponde a una VLAN válida\n")