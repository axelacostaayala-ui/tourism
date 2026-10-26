"""
Pipeline de Ingesta y Simulación de Big Data: Telemetría de Jugadores
Proyecto Prototípico - 5to Semestre: Ciencias de Datos para Negocios
UCA: Herramientas para el Almacenamiento de Grandes Volúmenes de Datos

Este script simula el flujo de eventos continuos generados por usuarios de
'Guardianes del Territorio' (GPS radar pings, escaneo de QRs en POIs, 
desbloqueos de Cartas Vivas 2D y redención de cupones en comercios locales).
"""

import os
import random
import uuid
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Semilla reproducible
np.random.seed(42)
random.seed(42)

# Rutas de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROCESSED_DIR = os.path.join(BASE_DIR, "datos", "processed")

def cargar_catalogos():
    """Carga los catálogos base del corredor piloto."""
    guardianes_df = pd.read_csv(os.path.join(PROCESSED_DIR, "catalogo_guardianes.csv"))
    pois_df = pd.read_csv(os.path.join(PROCESSED_DIR, "puntos_interes_pois.csv"))
    comercios_df = pd.read_csv(os.path.join(PROCESSED_DIR, "directorio_comercios_afiliados.csv"))
    estaciones_df = pd.read_csv(os.path.join(PROCESSED_DIR, "dataset_estaciones_el_insurgente.csv"))
    return guardianes_df, pois_df, comercios_df, estaciones_df

def generar_telemetria_eventos(n_usuarios=500, n_eventos=8000):
    """
    Simula eventos de telemetría de jugadores a lo largo de un mes (30 días).
    Refleja picos de exploración turística en fines de semana (sábado y domingo).
    """
    print(f"[*] Iniciando generación de {n_eventos} eventos de telemetría para {n_usuarios} jugadores...")
    guardianes_df, pois_df, comercios_df, estaciones_df = cargar_catalogos()
    
    # Generar IDs de usuarios y perfiles
    perfiles = ["Familia Trabajadora", "Joven Mochilero", "Adulto Mayor", "Turista Cultural"]
    prob_perfiles = [0.40, 0.35, 0.10, 0.15]
    
    usuarios_db = {}
    for i in range(1, n_usuarios + 1):
        u_id = f"USR-{i:04d}"
        usuarios_db[u_id] = {
            "perfil": np.random.choice(perfiles, p=prob_perfiles),
            "dispositivo": np.random.choice(["Android", "iOS"], p=[0.78, 0.22])
        }
    
    # Fechas simuladas: Septiembre - Octubre 2026
    fecha_inicio = datetime(2026, 9, 20, 6, 0, 0)
    
    eventos = []
    tipos_evento = ["RADAR_PING", "POI_CHECKIN_GPS", "POI_QR_SCAN", "GUARDIAN_UNLOCKED", "COUPON_REDEEMED"]
    
    for _ in range(n_eventos):
        u_id = random.choice(list(usuarios_db.keys()))
        perfil = usuarios_db[u_id]["perfil"]
        
        # Simular distribución temporal: mayor probabilidad en fines de semana
        dia_offset = random.randint(0, 29)
        fecha_base = fecha_inicio + timedelta(days=dia_offset)
        es_fin_de_semana = fecha_base.weekday() in [5, 6] # Sábado=5, Domingo=6
        
        if es_fin_de_semana:
            hora = int(np.random.normal(loc=13, scale=3)) # Pico al mediodía/tarde
        else:
            hora = int(np.random.normal(loc=17, scale=2)) # Horas de salida laboral
            
        hora = max(7, min(21, hora))
        minuto = random.randint(0, 59)
        segundo = random.randint(0, 59)
        timestamp = fecha_base.replace(hour=hora, minute=minuto, second=segundo)
        
        # Selección de nodo/municipio: en fin de semana viajan más a destinos emergentes
        if es_fin_de_semana:
            # Metepec, Zinacantepec y Lerma ganan peso
            id_estacion = np.random.choice(["EST-01", "EST-02", "EST-03", "EST-04", "EST-05"], 
                                           p=[0.25, 0.20, 0.30, 0.20, 0.05])
        else:
            # Entre semana predomina tránsito en Toluca y Santa Fe
            id_estacion = np.random.choice(["EST-01", "EST-02", "EST-03", "EST-04", "EST-05"], 
                                           p=[0.10, 0.35, 0.15, 0.15, 0.25])
            
        # Filtrar POIs y Comercios de esa estación
        pois_sub = pois_df[pois_df["id_estacion"] == id_estacion]
        comercios_sub = comercios_df[comercios_df["id_estacion"] == id_estacion]
        
        # Seleccionar tipo de evento coherente
        tipo_ev = np.random.choice(tipos_evento, p=[0.45, 0.25, 0.15, 0.10, 0.05])
        
        poi_id = None
        poi_nombre = None
        comercio_id = None
        comercio_nombre = None
        lat = None
        lon = None
        monto_ahorro_mxn = 0.0
        
        if len(pois_sub) > 0 and tipo_ev in ["POI_CHECKIN_GPS", "POI_QR_SCAN", "GUARDIAN_UNLOCKED"]:
            poi_row = pois_sub.sample(1).iloc[0]
            poi_id = poi_row["id_poi"]
            poi_nombre = poi_row["nombre_poi"]
            # Añadir pequeña perturbación GPS realista (~10-20 metros)
            lat = round(poi_row["latitud"] + np.random.normal(0, 0.00015), 6)
            lon = round(poi_row["longitud"] + np.random.normal(0, 0.00015), 6)
            
        elif len(comercios_sub) > 0 and tipo_ev == "COUPON_REDEEMED":
            com_row = comercios_sub.sample(1).iloc[0]
            comercio_id = com_row["id_comercio"]
            comercio_nombre = com_row["nombre_comercio"]
            lat = com_row["latitud"]
            lon = com_row["longitud"]
            # Estimación del descuento obtenido en pesos (entre 25 y 120 MXN)
            monto_ahorro_mxn = round(float(np.random.uniform(25.0, 110.0)), 2)
        else:
            # Radar ping en cercanía de la estación
            est_row = estaciones_df[estaciones_df["id_estacion"] == id_estacion].iloc[0]
            lat = 19.28 + np.random.uniform(-0.02, 0.02)
            lon = -99.60 + np.random.uniform(-0.10, 0.10)
            
        eventos.append({
            "id_evento": str(uuid.uuid4())[:13],
            "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "dia_semana": timestamp.strftime("%A"),
            "es_fin_de_semana": es_fin_de_semana,
            "id_usuario": u_id,
            "perfil_usuario": perfil,
            "tipo_evento": tipo_ev,
            "id_estacion": id_estacion,
            "id_poi": poi_id if poi_id else "NA",
            "nombre_poi": poi_nombre if poi_nombre else "NA",
            "id_comercio": comercio_id if comercio_id else "NA",
            "nombre_comercio": comercio_nombre if comercio_nombre else "NA",
            "latitud": lat,
            "longitud": lon,
            "ahorro_redencion_mxn": monto_ahorro_mxn
        })
        
    df_eventos = pd.DataFrame(eventos)
    df_eventos.sort_values(by="timestamp", inplace=True)
    
    # Guardar en processed
    output_path = os.path.join(PROCESSED_DIR, "eventos_jugadores_telemetria.csv")
    df_eventos.to_csv(output_path, index=False)
    print(f"[+] Dataset de eventos generado exitosamente:")
    print(f"    Total registros: {len(df_eventos)}")
    print(f"    Ruta de guardado: {output_path}")
    print(f"\nResumen de eventos por tipo:\n{df_eventos['tipo_evento'].value_counts()}")
    return df_eventos

if __name__ == "__main__":
    generar_telemetria_eventos()
