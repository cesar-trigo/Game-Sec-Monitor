import csv 


def cargar_telemetria(ruta_archivo: str) -> list:
    telemetria = []

    with open(ruta_archivo, 'r') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv) 
        
        for fila in lector_csv:
            # modificar tipo de datos de salida 
            telemetria.append(fila)

    return telemetria

# agregar si la lista da error

print(cargar_telemetria('gamesec_logs.csv'))