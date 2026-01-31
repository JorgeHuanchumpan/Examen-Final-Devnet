import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "e50ec2be-7549-474ª-9ª2c-d4dbe28da1ae"

def geocoding (location, key):
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key})
    replydata = requests.get(url)
    json_status = replydata.status_code
    json_data = replydata.json()

    if json_status == 200 and len(json_data["hits"]) !=0:
        json_data = requests.get(url).json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        
        if "country" in json_data["hits"][0]:
            country = json_data["hits"][0]["country"]
        else:
            country=""
        if "state" in json_data["hits"][0]:
            state = json_data["hits"][0]["state"]
        else:
            state=""
        if len(state) !=0 and len(country) !=0:
            new_loc = name + ", " + state + ", " + country
        elif len(state) !=0:
            new_loc = name + ", " + country
        else:
            new_loc = name
        print("URL de la API de Geocodificación para " + new_loc +" (Tipo de Ubicación: " + value + ")\n" + url)
    else:
        lat="null"
        lng="null"
        new_loc=location
        if json_status != 200:
            print("Estado de la API de Geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])
    return json_status,lat,lng,new_loc

while True:
    print("\n--------------------------------------------------")
    print("DESARROLLO ACITIVDAD 2 ---------------------------")
    print("EXAMEN CISCO DEVNET 23-01-2026--------------------")
    print("Jorge Huanchumpan---------------------------------")
    print("--------------------------------------------------")
    print("Instrucciones: Seleccione una forma de transporte:")
    print("--------------------------------------------------")
    print("automovil, bicicleta, caminar") 
    print("--------------------------------------------------")
    print("De lo contrario para salir presione la tecla v")
    print("--------------------------------------------------")
    

    perfiles_validos = {
        "automovil": "car",
        "bicicleta": "bike",
        "caminar": "foot"
    }
    
    entrada_usuario = input("SELECCIONE SOLO 1 PERFIL DE VEHICULO: ").lower()
    
    
    if entrada_usuario == "quit" or entrada_usuario == "v":
        break
    elif entrada_usuario in perfiles_validos:
        vehicle = perfiles_validos[entrada_usuario]
    else:
        vehicle = "car"
        print("No se ingresó un perfil de vehículo válido. Usando el perfil de auto (car).")

    loc1 = input("Ubicación de Inicio: ")
    if loc1 == "quit" or loc1 == "v":
        break
    orig = geocoding(loc1, key)
    
    loc2 = input("Destino: ")
    if loc2 == "quit" or loc2 == "v":
        break
    dest = geocoding(loc2, key)
    
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op="&point="+str(orig[1])+"%2C"+str(orig[2])
        dp="&point="+str(dest[1])+"%2C"+str(dest[2])
        
        
        paths_url = route_url + urllib.parse.urlencode({"key":key, "vehicle":vehicle, "locale":"es"}) + op + dp
        
        paths_status = requests.get(paths_url).status_code
        paths_data = requests.get(paths_url).json()
        print("Estado de la API de Rutas: " + str(paths_status) + "\nURL de la API de Rutas:\n" + paths_url)
        print("=================================================")
       
        print("Instrucciones desde " + orig[3] + " hasta " + dest[3] + " en " + entrada_usuario)
        print("=================================================")
        
        if paths_status == 200:
            miles = (paths_data["paths"][0]["distance"])/1000/1.61
            km = (paths_data["paths"][0]["distance"])/1000
            sec = int(paths_data["paths"][0]["time"]/1000%60)
            min = int(paths_data["paths"][0]["time"]/1000/60%60)
            hr = int(paths_data["paths"][0]["time"]/1000/60/60)
            print("Distancia Recorrida: {0:.1f} millas / {1:.1f} km".format(miles, km))
            print("Duración del Viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                distance = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ({1:.1f} km / {2:.1f} millas)".format(path, distance/1000, distance/1000/1.61))
            print("=================================================")
        else:
            print("Mensaje de error: " + paths_data["message"])

            print("*************************************************")
