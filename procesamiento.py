from carga import cargar_telemetria 

total = [
    {'id_sesion': '1', 'servidor': 'SA-BuenosAires', 'jugador_id': 'User_125', 'tipo_partida': 'Competitiva', 'ping_promedio': '49', 'fps_promedio': '75', 'duracion_minutos': '12.0', 'intentos_fallidos': '0', 'reportes_trampa': '1'}, {'id_sesion': '2', 'servidor': 'EU-Frankfurt', 'jugador_id': 'User_132', 'tipo_partida': 'Casual', 'ping_promedio': '185', 'fps_promedio': '75', 'duracion_minutos': '29.0', 'intentos_fallidos': '0', 'reportes_trampa': '1'}, {'id_sesion': '3', 'servidor': 'EU-Frankfurt', 'jugador_id': 'User_325', 'tipo_partida': 'Casual', 'ping_promedio': '201', 'fps_promedio': '30', 'duracion_minutos': '40.8', 'intentos_fallidos': '1', 'reportes_trampa': '0'}
]

def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    total_sesiones = len(sesiones)
    
    ping_promedio = 0
    ping_total = 0
    
    duracion_promedio = 0
    duracion_total = 0
    
    partidas_totales = 0
    porcentaje_competitivas = 0
    
    acumulador = {}
    
    for sesion in sesiones:
        ping_total += int(sesion['ping_promedio'])
        ping_promedio = round(ping_total / total_sesiones, 2)

        duracion_total += float(sesion['duracion_minutos'])
        duracion_promedio = round(duracion_total / total_sesiones, 2)
        
        if (sesion['tipo_partida'] == 'Competitiva' or sesion['tipo_partida'] == 'Torneo'):
            partidas_totales += 1
        
        porcentaje_competitivas = round(partidas_totales/total_sesiones * 100, 2)
            
            
        servidor = sesion['servidor']
        # print (servidor)
        datos = acumulador.get(servidor, {'cantidad':0, 'ping_promedio':0, 'fps_promedio':0})
        # print (datos)
        datos['cantidad'] += 1
        datos['ping_promedio'] += int(sesion['ping_promedio'])
        datos['fps_promedio'] += int(sesion['fps_promedio'])
        acumulador[servidor] = datos
        # print (acumulador)
        
        for servidor, datos in acumulador.items():
            datos['ping_promedio'] = round(datos['ping_promedio'] / datos['cantidad'], 2)       
            datos['fps_promedio'] = round(datos['fps_promedio'] / datos['cantidad'], 2)
            
        acumulador[servidor] = datos
            
    print (acumulador)           
        


    # print (f"Total de sesiones: {ping_total}")
    # print (f"Ping promedio: {ping_promedio}")
    # print (f"Duración promedio: {duracion_promedio}")
    # print (f"Total de partidas: {partidas_totales}")
    # print (f"Porcentaje de partidas competitivas: {porcentaje_competitivas}%")
    


#falta que retorne los datos en un diccionario y ordenar

calcular_estadisticas_globales(total)

def clasificar_incidentes(sesiones: list[dict]) -> tuple[dict, list[dict]]:
    
    
    pass