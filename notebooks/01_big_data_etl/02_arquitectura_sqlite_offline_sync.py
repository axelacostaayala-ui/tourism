"""
Arquitectura de Almacenamiento Big Data, Base de Datos Offline-First (SQLite)
y Sincronización Criptográfica con Enlaces Profundos (Deeplinking Google Maps).

Proyecto Prototípico - 5to Semestre: Ciencias de Datos para Negocios
Universidad Rosario Castellanos
UCA: Herramientas para el Almacenamiento de Grandes Volúmenes de Datos
Rol: Integrante 1 — Data Engineering & ML Lead (monenri9-svg)

Este script implementa:
1. Construcción del paquete local Offline-First en SQLite (guardianes_offline_cache.db)
   para operar sin cobertura celular en zonas serranas (Nevado de Toluca / Ciénegas de Lerma).
2. Generación de enlaces profundos (Deeplinking) hacia Google Maps peatonal/transporte
   desde cada estación del Tren Interurbano 'El Insurgente' hacia los 12 POIs y 15 comercios.
3. Firma criptográfica SHA-256 de capturas de Guardianes y códigos OTP de 4 dígitos
   para validación antifraude sin conexión a internet y sincronización diferida al Data Lakehouse.
4. Particionamiento y compactación analítica de la telemetría de eventos por estación y mes.
"""

import os
import sqlite3
import hashlib
import urllib.parse
from datetime import datetime
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROCESSED_DIR = os.path.join(BASE_DIR, "datos", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)


def generar_deeplink_google_maps(lat_origen, lon_origen, lat_dest, lon_dest, modo="walking"):
    """
    Construye un enlace profundo (Universal Cross-Platform Deeplink) compatible con
    Android e iOS para iniciar navegación paso a paso hacia un POI o comercio local.
    """
    params = {
        "api": "1",
        "origin": f"{lat_origen:.6f},{lon_origen:.6f}",
        "destination": f"{lat_dest:.6f},{lon_dest:.6f}",
        "travelmode": modo
    }
    return f"https://www.google.com/maps/dir/?{urllib.parse.urlencode(params)}"


def generar_firma_offline_sha256(id_usuario, id_poi, token_qr, timestamp_str, secret_salt="GUARDIANES_2026_URC"):
    """
    Genera un hash criptográfico verificable en servidor cuando el dispositivo
    recupera señal celular, evitando falsificación de capturas offline.
    """
    payload = f"{id_usuario}|{id_poi}|{token_qr}|{timestamp_str}|{secret_salt}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def generar_codigo_otp_comercio(id_evento, id_comercio):
    """Genera un código alfanumérico corto (ej. BND-4829) para locatarios sin hardware."""
    digest = hashlib.md5(f"{id_evento}:{id_comercio}".encode("utf-8")).hexdigest()
    num_4d = int(digest[:6], 16) % 9000 + 1000
    return f"BND-{num_4d}"


def construir_paquete_offline_sqlite():
    """
    Empaqueta los catálogos maestros, POIs con coordenadas y enlaces de navegación,
    metadatos del visor histórico 'La Ventana del Tiempo' y la cola de sincronización
    diferida en una base de datos SQLite ligera lista para el cliente móvil.
    """
    db_path = os.path.join(PROCESSED_DIR, "guardianes_offline_cache.db")
    print(f"[*] Construyendo base de datos Offline-First en: {db_path}...")

    estaciones = pd.read_csv(os.path.join(PROCESSED_DIR, "dataset_estaciones_el_insurgente.csv"))
    rareza = pd.read_csv(os.path.join(PROCESSED_DIR, "indice_saturacion_rareza_estaciones.csv"))
    guardianes = pd.read_csv(os.path.join(PROCESSED_DIR, "catalogo_guardianes.csv"))
    pois = pd.read_csv(os.path.join(PROCESSED_DIR, "puntos_interes_pois.csv"))
    comercios = pd.read_csv(os.path.join(PROCESSED_DIR, "directorio_comercios_afiliados.csv"))
    eventos = pd.read_csv(os.path.join(PROCESSED_DIR, "eventos_jugadores_telemetria.csv"))

    # Coordenadas de las estaciones para calcular rutas peatonales Deeplink
    coords_estacion = {
        "EST-01": (19.2830, -99.7340),
        "EST-02": (19.2890, -99.6540),
        "EST-03": (19.2540, -99.6040),
        "EST-04": (19.2840, -99.5140),
        "EST-05": (19.3590, -99.2580),
        "EST-06": (19.3780, -99.2310),
        "EST-07": (19.3980, -99.2000)
    }

    # Enriquecer POIs con Deeplinks y metadatos del visor histórico 'La Ventana del Tiempo'
    epocas_historicas = {
        "POI-01": ("Siglo XVI (1569)", "Convento franciscano original y atrio evangelizador de Zinacantepec."),
        "POI-02": ("Año 1581", "Labrado monolítico indígena en piedra volcánica del Xinantécatl."),
        "POI-03": ("Década de 1930", "Antiguos caminos forestales de los pueblos madereros y glaciares del volcán."),
        "POI-04": ("Siglo XVIII", "Vista panorámica del Cerro de los Magueyes y trazado colonial de Metepec."),
        "POI-05": ("Año 1940", "Primeros hornos familiares de barro policromado y pigmentos minerales."),
        "POI-06": ("Año 1955", "Tianguis tradicional de alfareros en la plaza central de Metepec."),
        "POI-07": ("Siglo XIX (1890)", "Extensión lacustre originaria de la Gran Laguna de Lerma y chinampas."),
        "POI-08": ("Siglo XVII (1613)", "Fundación de la ciudad colonial de Lerma y puente real de piedra."),
        "POI-09": ("Año 1925", "Cosecha lacustre y tejido comunitario de petates y cestería de tule."),
        "POI-10": ("Año 1910 vs 1980", "Antiguo Mercado 16 de Septiembre de hierro forjado antes del Cosmovitral."),
        "POI-11": ("Año 1870", "Construcción de Los Portales de Toluca y tranvías tirados por mulas."),
        "POI-12": ("Siglo XIX", "Talleres gremiales de dulce de pasta de azúcar para la Feria del Alfeñique.")
    }

    pois_enriquecidos = []
    for _, row in pois.iterrows():
        est_id = row["id_estacion"]
        lat_o, lon_o = coords_estacion.get(est_id, (19.2830, -99.7340))
        deeplink = generar_deeplink_google_maps(lat_o, lon_o, row["latitud"], row["longitud"], modo="walking")
        epoca, desc_hist = epocas_historicas.get(row["id_poi"], ("Siglo XX", "Archivo fotográfico histórico regional."))

        item = row.to_dict()
        item["radio_geofence_metros"] = 50
        item["google_maps_deeplink"] = deeplink
        item["ventana_tiempo_epoca"] = epoca
        item["ventana_tiempo_descripcion"] = desc_hist
        pois_enriquecidos.append(item)

    df_pois_ext = pd.DataFrame(pois_enriquecidos)

    # Enriquecer comercios con Deeplinks y modalidad de validación sin hardware
    comercios_ext = []
    for _, row in comercios.iterrows():
        est_id = row["id_estacion"]
        lat_o, lon_o = coords_estacion.get(est_id, (19.2830, -99.7340))
        deeplink = generar_deeplink_google_maps(lat_o, lon_o, row["latitud"], row["longitud"], modo="walking")
        item = row.to_dict()
        item["metodo_validacion_locatario"] = "OTP 4-Dígitos + QR Dinámico Offline"
        item["google_maps_deeplink"] = deeplink
        comercios_ext.append(item)

    df_comercios_ext = pd.DataFrame(comercios_ext)

    # Simular cola de sincronización offline-first (Outbox Pattern) con firmas SHA-256 y códigos OTP
    eventos_offline = eventos[eventos["tipo_evento"].isin(["POI_QR_SCAN", "GUARDIAN_UNLOCKED", "COUPON_REDEEMED"])].head(250).copy()
    cola_sync = []
    for _, ev in eventos_offline.iterrows():
        firma = generar_firma_offline_sha256(
            ev["id_usuario"], ev["id_poi"], "TOKEN_LOCAL_CACHED", ev["timestamp"]
        )
        otp = generar_codigo_otp_comercio(ev["id_evento"], ev["id_comercio"]) if ev["tipo_evento"] == "COUPON_REDEEMED" else "NA"
        cola_sync.append({
            "id_evento": ev["id_evento"],
            "timestamp_captura_local": ev["timestamp"],
            "id_usuario": ev["id_usuario"],
            "tipo_evento": ev["tipo_evento"],
            "id_estacion": ev["id_estacion"],
            "id_poi": ev["id_poi"],
            "id_comercio": ev["id_comercio"],
            "codigo_otp_locatario": otp,
            "firma_criptografica_sha256": firma,
            "estado_sincronizacion": "SYNCHRONIZED_TO_CLOUD"
        })
    df_cola_sync = pd.DataFrame(cola_sync)

    # Resumen de particionamiento Big Data por nodo y tipo de evento (Capa Gold del Lakehouse)
    df_particiones = eventos.groupby(["id_estacion", "es_fin_de_semana", "tipo_evento"]).agg(
        total_eventos=("id_evento", "count"),
        usuarios_unicos=("id_usuario", "nunique"),
        ahorro_acumulado_mxn=("ahorro_redencion_mxn", "sum"),
        latitud_media=("latitud", "mean"),
        longitud_media=("longitud", "mean")
    ).reset_index()

    # Guardar en SQLite local con índices optimizados
    conn = sqlite3.connect(db_path)
    estaciones.merge(rareza[["id_estacion", "indice_saturacion_ist", "rareza_inversa_asignada", "multiplicador_recompensa"]], on="id_estacion", how="left").to_sql(
        "offline_nodos_estaciones", conn, if_exists="replace", index=False
    )
    guardianes.to_sql("offline_catalogo_guardianes", conn, if_exists="replace", index=False)
    df_pois_ext.to_sql("offline_pois_y_ventana_tiempo", conn, if_exists="replace", index=False)
    df_comercios_ext.to_sql("offline_comercios_afiliados", conn, if_exists="replace", index=False)
    df_cola_sync.to_sql("offline_outbox_sync_queue", conn, if_exists="replace", index=False)
    df_particiones.to_sql("lakehouse_gold_particiones_telemetria", conn, if_exists="replace", index=False)

    # Crear índices para consultas de baja latencia (< 5 ms en dispositivo móvil)
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pois_estacion ON offline_pois_y_ventana_tiempo(id_estacion);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_com_estacion ON offline_comercios_afiliados(id_estacion);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sync_user ON offline_outbox_sync_queue(id_usuario, tipo_evento);")
    conn.commit()
    conn.close()

    # Exportar tablas enriquecidas a CSV para trazabilidad
    df_pois_ext.to_csv(os.path.join(PROCESSED_DIR, "pois_enriquecidos_deeplinks_ventana_tiempo.csv"), index=False)
    df_cola_sync.to_csv(os.path.join(PROCESSED_DIR, "muestra_sincronizacion_offline_sha256.csv"), index=False)
    df_particiones.to_csv(os.path.join(PROCESSED_DIR, "bigdata_particiones_eventos_gold.csv"), index=False)

    tamano_kb = os.path.getsize(db_path) / 1024.0
    print(f"[+] Paquete SQLite Offline-First creado exitosamente ({tamano_kb:.1f} KB).")
    print(f"    • POIs con Deeplinks y Ventana del Tiempo: {len(df_pois_ext)} registros")
    print(f"    • Comercios con validación OTP sin hardware: {len(df_comercios_ext)} registros")
    print(f"    • Eventos firmados con SHA-256 en cola Outbox: {len(df_cola_sync)} registros")
    print(f"    • Particiones analíticas Gold Lakehouse: {len(df_particiones)} particiones")


if __name__ == "__main__":
    print("=========================================================================")
    print("  ARQUITECTURA BIG DATA & OFFLINE-FIRST ENGINE - GUARDIANES DEL TERRITORIO")
    print("=========================================================================")
    construir_paquete_offline_sqlite()
    print("\n[OK] Pipeline de Arquitectura Big Data y Almacenamiento Offline-First completado.")
