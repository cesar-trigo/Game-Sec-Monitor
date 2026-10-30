import csv 


def cargar_telemetria(ruta_archivo: str) -> list:
    telemetria = []

    with open(ruta_archivo, 'r') as archivo_csv:
        lector_csv = csv.DictReader(archivo_csv) 
        
        for fila in lector_csv:
            fila["id_sesion"] = int(fila["id_sesion"])
            fila["ping_promedio"] = int(fila["ping_promedio"])
            fila["fps_promedio"] = int(fila["fps_promedio"])
            fila["duracion_minutos"] = float(fila["duracion_minutos"])
            fila["intentos_fallidos"] = int(fila["intentos_fallidos"])
            fila["reportes_trampa"] = int(fila["reportes_trampa"])
            telemetria.append(fila)

    if len(telemetria) == 0:
        raise ValueError("El archivo no contiene registros")

    return telemetria

