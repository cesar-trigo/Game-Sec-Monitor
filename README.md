# GameSec Monitor

Telemetría de servidores de videojuegos y detección de incidentes con Python.

**Universidad Nacional de Hurlingham — Instituto de Tecnología e Ingeniería**
Taller de Programación I — Ciclo Lectivo 2026
Trabajo Práctico Integrador

## Integrantes

| Nombre y apellido | DNI | Carrera |
|---|---|---|
| (completar) | (completar) | (completar) |
| (completar) | (completar) | (completar) |
| (completar) | (completar) | (completar) |

## Descripción

Herramienta de consola que procesa un archivo de telemetría de servidores de un
videojuego online (`gamesec_logs.csv`), calcula métricas operativas y clasifica
automáticamente las sesiones como **Normal**, **Sospechosa** o **Crítica** mediante
un motor de reglas heurísticas. Además, genera un reporte consolidado en texto.

## Requisitos

- Python 3.10 o superior.
- Solo biblioteca estándar de Python. No se usan librerías externas (sin Pandas ni NumPy).

## Cómo ejecutarlo

Desde la carpeta del proyecto, con `gamesec_logs.csv` en la misma carpeta:

```
python main.py
```

## Estructura del proyecto

| Archivo | Responsabilidad |
|---|---|
| `main.py` | Punto de entrada. Muestra el menú, coordina las llamadas a los otros módulos y dispara la exportación del reporte. |
| `carga.py` | Lectura del CSV con `csv.DictReader`, conversión de tipos y validación. |
| `procesamiento.py` | Estadísticas globales, agrupación por servidor, clasificación de incidentes y armado del reporte. |
| `gamesec_logs.csv` | Dataset de entrada (150 sesiones). |
| `reporte_gamesec.txt` | Reporte generado por el programa (opción 5 del menú). |

## Menú

| Opción | Acción |
|---|---|
| 1 | Cargar y validar el dataset |
| 2 | Ver estadísticas globales |
| 3 | Ver rendimiento por región de servidor |
| 4 | Auditar incidentes de seguridad |
| 5 | Exportar el reporte consolidado |
| 6 | Salir |

Si se elige cualquier opción de la 2 a la 5 sin haber cargado el dataset, el programa lo carga automáticamente.

## Funciones principales

| Función | Módulo | Qué hace |
|---|---|---|
| `cargar_telemetria(ruta_archivo)` | `carga.py` | Lee el CSV y devuelve una lista de diccionarios con los tipos convertidos. |
| `calcular_estadisticas_globales(sesiones)` | `procesamiento.py` | Devuelve total de sesiones, ping promedio, duración promedio y porcentaje de partidas competitivas. |
| `analizar_por_servidor(sesiones)` | `procesamiento.py` | Agrupa por servidor con un diccionario acumulador y calcula cantidad, ping y FPS promedio. |
| `clasificar_incidentes(sesiones)` | `procesamiento.py` | Devuelve el resumen de frecuencias y la lista de sesiones críticas. |
| `exportar_reporte(sesiones, ruta_salida, fecha, conclusiones)` | `procesamiento.py` | Escribe el reporte en un archivo de texto. |

## Reglas de clasificación

1. **Crítico:** `reportes_trampa >= 3` o `intentos_fallidos >= 4`.
2. **Sospechoso:** si no es crítico y cumple `(ping_promedio > 200 y intentos_fallidos >= 2)` o `reportes_trampa == 2`.
3. **Normal:** cualquier otra sesión.

## Dataset

Columnas de `gamesec_logs.csv`: `id_sesion`, `servidor`, `jugador_id`, `tipo_partida`,
`ping_promedio`, `fps_promedio`, `duracion_minutos`, `intentos_fallidos`, `reportes_trampa`.
