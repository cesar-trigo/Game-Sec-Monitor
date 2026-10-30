from carga import cargar_telemetria 
import procesamiento
import datetime


ARCHIVO_DE_DATOS = "gamesec_logs.csv"
ARCHIVO_DE_REPORTE = "reporte_gamesec.txt"


sesiones = None
opcion = ""

while opcion != "6":
    print("=" * 41)
    print("    GAMESEC MONITOR - PANEL DE CONTROL")
    print("=" * 41)
    print("1. Cargar y validar dataset")
    print("2. Ver estadísticas globales de servidores")
    print("3. Ver rendimiento por región de servidor")
    print("4. Auditar incidentes de seguridad (Críticos y Sospechosos)")
    print("5. Exportar reporte consolidado (reporte_gamesec.txt)")
    print("6. Salir")
    print("=" * 41)
    opcion = input("Seleccione una opción: ").strip()

    if opcion == "1" or (opcion in ("2", "3", "4", "5") and sesiones is None):
        try:
            sesiones = cargar_telemetria(ARCHIVO_DE_DATOS)
            print(f"Dataset cargado correctamente: {len(sesiones)} sesiones.")
        except (FileNotFoundError, ValueError) as error:
            print(f"Error al cargar el dataset: {error}")
            print()
            continue

    if opcion == "2":
        print("\nRESUMEN GLOBAL OPERATIVO")
        print("-" * procesamiento.ANCHO)
        print("\n".join(procesamiento.formatear_global(sesiones)))

    elif opcion == "3":
        print("\nRENDIMIENTO REGIONAL POR SERVIDOR")
        print("-" * procesamiento.ANCHO)
        print("\n".join(procesamiento.formatear_servidores(sesiones)))

    elif opcion == "4":
        print("\nAUDITORÍA DE SEGURIDAD E INCIDENTES")
        print("-" * procesamiento.ANCHO)
        print("\n".join(procesamiento.formatear_seguridad(sesiones)))

    elif opcion == "5":
        fecha = datetime.date.today().strftime("%d/%m/%Y")
        procesamiento.exportar_reporte(sesiones, ARCHIVO_DE_REPORTE, fecha)
        print(f"Reporte exportado en '{ARCHIVO_DE_REPORTE}'")

    elif opcion == "6":
        print("Saliendo del programa...")

    else:
        print("Opción inválida. Elegí un número del 1 al 6.")

    print()

