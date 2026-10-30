from carga import cargar_telemetria 



def sacar_promedio(unidad, total):
    return round(unidad/total, 2)

def sacar_porcentaje(parte, total):
    return round(parte * 100 / total, 2)


def calcular_estadisticas_globales(sesiones: list[dict]) -> dict:
    total_sesiones = len(sesiones)
    ping_total = 0
    duracion_total = 0
    partidas_totales = 0
    
    for sesion in sesiones:
        ping_total += sesion['ping_promedio']
        duracion_total += sesion['duracion_minutos']
        
        if sesion['tipo_partida'] in ('Competitiva', 'Torneo'):
            partidas_totales += 1
        
    ping_promedio = sacar_promedio(ping_total, total_sesiones)
    duracion_promedio = sacar_promedio(duracion_total, total_sesiones)
    porcentaje_competitivas = sacar_promedio(partidas_totales * 100, total_sesiones)
  
    estadisticas_globales = {
        'total_sesiones': total_sesiones,
        'ping_promedio': ping_promedio,
        'duracion_promedio': duracion_promedio,
        'porcentaje_competitivas': porcentaje_competitivas,
    }
    
    return estadisticas_globales
        

            
def analizar_por_servidor(sesiones: list[dict]) -> dict:    
    
    acumulador = {}
    
    for sesion in sesiones:    
        servidor = sesion['servidor']
        
        datos = acumulador.get(servidor, {'cantidad':0, 'ping_promedio':0, 'fps_promedio':0})
        
        datos['cantidad'] += 1
        datos['ping_promedio'] += (sesion['ping_promedio'])
        datos['fps_promedio'] += (sesion['fps_promedio'])       
        acumulador[servidor] = datos

        
    for servidor, datos in acumulador.items():
        datos['ping_promedio'] = sacar_promedio(datos['ping_promedio'], datos['cantidad'])       
        datos['fps_promedio'] = sacar_promedio(datos['fps_promedio'], datos['cantidad'])
        
    
    return acumulador    




def clasificar_incidentes(sesiones: list[dict]) -> tuple[dict, list[dict]]:
    resumen_frecuencias = {'Normal': 0, 'Sospechoso': 0, 'Crítico': 0}
    critico = []
    
    for sesion in sesiones:
        
        if sesion['reportes_trampa'] >= 3 or sesion['intentos_fallidos'] >= 4:

            critico.append({
                'id_sesion': sesion['id_sesion'],
                'jugador_id': sesion['jugador_id'],
                'servidor': sesion['servidor'],
                'motivo': f'Exceso de reportes por trampa ({sesion['reportes_trampa']}) e intentos fallidos ({sesion['intentos_fallidos']})'
            })
            resumen_frecuencias['Crítico'] += 1
        elif sesion['ping_promedio'] > 200 and sesion['intentos_fallidos'] >= 2 or sesion['reportes_trampa'] == 2:
            resumen_frecuencias['Sospechoso'] += 1
        else:
            resumen_frecuencias['Normal'] += 1
            
    return (resumen_frecuencias, critico)


ANCHO = 70


def formatear_global(sesiones: list[dict]) -> list[str]:
    estadisticas = calcular_estadisticas_globales(sesiones)
    
    return [
        f"Total de sesiones procesadas: {estadisticas['total_sesiones']}",
        f"Ping promedio global: {estadisticas['ping_promedio']:.2f} ms",
        f"Duración media de partida: {estadisticas['duracion_promedio']:.2f} min",
        f"Partidas de alta competencia (Ranked/Torneo): {estadisticas['porcentaje_competitivas']:.2f}%",
    ]


def formatear_servidores(sesiones: list[dict]) -> list[str]:
    por_servidor = analizar_por_servidor(sesiones)
    
    lineas = [f"{'Servidor':<18} │ {'Sesiones':<8} │ {'Ping Promedio':<13} │ FPS Promedio"]
    lineas.append("-" * ANCHO)

    for servidor, datos in por_servidor.items():
        ping = f"{datos['ping_promedio']:.2f} ms"
        fps = f"{datos['fps_promedio']:.2f} fps"
        lineas.append(f"{servidor:<18} │ {datos['cantidad']:<8} │ {ping:<13} │ {fps}")

    return lineas


def formatear_seguridad(sesiones: list[dict]) -> list[str]:
    resumen, criticos = clasificar_incidentes(sesiones)
    total = len(sesiones)

    normales = resumen['Normal']
    sospechosos = resumen['Sospechoso']
    cant_criticos = resumen['Crítico']

    lineas = [
        "Distribución de estados de seguridad:",
        f"  • Normales:    {normales:>3} sesiones ({sacar_porcentaje(normales, total):>5.2f}%)",
        f"  • Sospechosos: {sospechosos:>3} sesiones ({sacar_porcentaje(sospechosos, total):>5.2f}%)",
        f"  • Críticos:    {cant_criticos:>3} sesiones ({sacar_porcentaje(cant_criticos, total):>5.2f}%)",
        "",
        "Detalle de Sesiones Críticas Detectadas:",
    ]

    for critico in criticos:
        lineas.append(
            f"  [!] Sesión #{critico['id_sesion']}  │ Jugador: {critico['jugador_id']} │ Servidor: {critico['servidor']}"
        )
        lineas.append(f"      Motivo: {critico['motivo']}")

    return lineas


def exportar_reporte(sesiones: list[dict], ruta_salida: str = 'reporte_gamesec.txt',
                     fecha: str = '') -> None:

    lineas = ["=" * ANCHO,
              "REPORTE DE AUDITORÍA Y TELEMETRÍA — GAMESEC".center(ANCHO),
              "=" * ANCHO,
              f"Fecha de generación: {fecha}",
              "",
              "[1] RESUMEN GLOBAL OPERATIVO",
              "-" * ANCHO]
    lineas += formatear_global(sesiones)

    lineas += ["", "[2] RENDIMIENTO REGIONAL POR SERVIDOR", "-" * ANCHO]
    lineas += formatear_servidores(sesiones)

    lineas += ["", "[3] AUDITORÍA DE SEGURIDAD E INCIDENTES", "-" * ANCHO]
    lineas += formatear_seguridad(sesiones)

    lineas += ["", "=" * ANCHO,
               "FIN DEL REPORTE GAMESEC".center(ANCHO),
               "=" * ANCHO]

    with open(ruta_salida, "w", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")
