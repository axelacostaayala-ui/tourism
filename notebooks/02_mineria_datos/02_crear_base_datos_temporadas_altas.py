"""
Generador de Base de Datos y Análisis de Estacionalidad / Temporadas Altas de Turismo en México
Compendio Estadístico del Turismo en México (CETM 2024 - SECTUR / DataTur)
UCA: Herramientas para el Almacenamiento de Grandes Volúmenes de Datos & Minería de Datos

Este script procesa los archivos oficiales del CETM2024 y genera:
1. Base de datos SQLite unificada: datos/processed/turismo_mexico_temporadas.db
2. Archivos CSV limpios para hojas de cálculo, SQL y Python
3. Gráficas analíticas de temporadas altas, medias y bajas en México
"""

import os
import sqlite3
import datetime
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CETM_DIR = os.path.join(BASE_DIR, "CETM2024")
PROCESSED_DIR = os.path.join(BASE_DIR, "datos", "processed")
KPIS_DIR = os.path.join(BASE_DIR, "campana", "kpis")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(KPIS_DIR, exist_ok=True)

# Nombres de meses en español
NOMBRES_MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def extraer_resumen_mensual_nacional():
    """
    Extrae la serie temporal mensual de 1995 a 2024 del archivo 1_2.xlsx (Resumen Mensual).
    Normaliza unidades estadísticas para garantizar continuidad y comparabilidad histórica.
    """
    file_path = os.path.join(CETM_DIR, "1_2.xlsx")
    print(f"[*] Procesando {file_path}...")
    wb = openpyxl.load_workbook(file_path, data_only=True)
    
    registros = []
    
    for sheet in wb.sheetnames:
        try:
            anio = int(sheet)
        except ValueError:
            continue
            
        ws = wb[sheet]
        
        # Localizar fila y columnas de fechas
        date_cols = {}
        for r in range(1, 6):
            for c in range(1, 25):
                val = ws.cell(r, c).value
                if isinstance(val, (datetime.datetime, datetime.date)):
                    date_cols[c] = val.month
            if len(date_cols) >= 12:
                break
                
        if len(date_cols) < 12:
            continue
            
        # Mapear filas por indicador
        mapa_filas = {}
        for r in range(4, ws.max_row + 1):
            c1 = ws.cell(r, 1).value
            c2 = ws.cell(r, 2).value
            c3 = ws.cell(r, 3).value
            texto = f"{c1 or ''} {c2 or ''} {c3 or ''}".strip().lower()
            
            if 'visitantes internacionales a méxico' in texto and 'gasto' not in texto and 'número' not in texto and 'al exterior' not in texto:
                if 'visitantes_internacionales_miles' not in mapa_filas:
                    mapa_filas['visitantes_internacionales_miles'] = r
            elif 'turistas internacionales' in texto and 'gasto' not in texto and 'al exterior' not in texto and 'visitantes' not in texto:
                if 'turistas_internacionales_miles' not in mapa_filas:
                    mapa_filas['turistas_internacionales_miles'] = r
            elif 'excursionistas internacionales' in texto and 'gasto' not in texto and 'al exterior' not in texto:
                if 'excursionistas_internacionales_miles' not in mapa_filas:
                    mapa_filas['excursionistas_internacionales_miles'] = r
            elif 'porcentaje de ocupación' in texto:
                if 'ocupacion_hotelera_pct' not in mapa_filas:
                    mapa_filas['ocupacion_hotelera_pct'] = r
            elif 'llegada de turistas' in texto and 'vuelos' not in texto and 'pasajeros' not in texto:
                if 'turistas_hoteles_total_miles' not in mapa_filas:
                    mapa_filas['turistas_hoteles_total_miles'] = r
            elif 'nacionales' in texto and 'turistas_hoteles_total_miles' in mapa_filas and 'vuelos' not in texto and 'pasajeros' not in texto:
                if 'turistas_hoteles_nacionales_miles' not in mapa_filas:
                    mapa_filas['turistas_hoteles_nacionales_miles'] = r
            elif 'extranjeros' in texto and 'turistas_hoteles_total_miles' in mapa_filas and 'vuelos' not in texto and 'pasajeros' not in texto:
                if 'turistas_hoteles_extranjeros_miles' not in mapa_filas:
                    mapa_filas['turistas_hoteles_extranjeros_miles'] = r
            elif 'llegada de vuelos a los aeropuertos' in texto:
                if 'vuelos_aeropuertos_total' not in mapa_filas:
                    mapa_filas['vuelos_aeropuertos_total'] = r
            elif 'llegada de pasajeros a los aeropuertos' in texto:
                if 'pasajeros_aereos_total' not in mapa_filas:
                    mapa_filas['pasajeros_aereos_total'] = r
            elif 'pasajeros en crucero' in texto:
                if 'pasajeros_cruceros' not in mapa_filas:
                    mapa_filas['pasajeros_cruceros'] = r
            elif 'visitantes internacionales a méxico' in texto and 'gasto' in texto and 'al exterior' not in texto:
                if 'gasto_visitantes_millones_usd' not in mapa_filas:
                    mapa_filas['gasto_visitantes_millones_usd'] = r
                
        # Extraer valores para cada mes
        for col, mes in sorted(date_cols.items(), key=lambda x: x[1]):
            rec = {
                "anio": anio,
                "mes": mes,
                "fecha": f"{anio}-{mes:02d}-01",
                "nombre_mes": NOMBRES_MESES[mes],
                "trimestre": f"T{(mes-1)//3 + 1}"
            }
            for ind, r_idx in mapa_filas.items():
                val = ws.cell(r_idx, col).value
                if isinstance(val, (int, float)):
                    # Normalizar ocupación si viene en decimal (0.60) a porcentaje (60.0)
                    if ind == 'ocupacion_hotelera_pct' and val <= 1.0:
                        val = val * 100.0
                    # Normalizar turistas en hoteles a Miles de personas
                    elif 'hoteles' in ind and val > 100000:
                        val = val / 1000.0
                    rec[ind] = round(float(val), 3)
                else:
                    rec[ind] = None
                    
            registros.append(rec)
            
    df_nacional = pd.DataFrame(registros)
    df_nacional = df_nacional.sort_values(by=["anio", "mes"]).reset_index(drop=True)
    
    # Calcular clasificación de temporada basada en percentiles de ocupación hotelera
    p33 = df_nacional['ocupacion_hotelera_pct'].quantile(0.33)
    p66 = df_nacional['ocupacion_hotelera_pct'].quantile(0.66)
    
    def clasificar(pct):
        if pd.isna(pct):
            return "Sin Dato"
        if pct >= p66:
            return "Temporada Alta (Peak)"
        elif pct >= p33:
            return "Temporada Media"
        else:
            return "Temporada Baja (Valle)"
            
    df_nacional['clasificacion_temporada'] = df_nacional['ocupacion_hotelera_pct'].apply(clasificar)
    print(f"[+] Resumen Nacional mensual procesado: {len(df_nacional)} registros (1995-2024).")
    return df_nacional

def extraer_pasajeros_aeropuertos():
    """
    Extrae la afluencia mensual por aeropuerto para destinos turísticos y metropolitanos (7_13.xlsx).
    """
    file_path = os.path.join(CETM_DIR, "7_13.xlsx")
    print(f"[*] Procesando {file_path}...")
    wb = openpyxl.load_workbook(file_path, data_only=True)
    
    destinos_clave = {
        'cancún': ('Cancún (Sol y Playa)', 'Quintana Roo', 'Playa'),
        'los cabos': ('Los Cabos (Sol y Playa)', 'Baja California Sur', 'Playa'),
        'puerto vallarta': ('Puerto Vallarta (Sol y Playa)', 'Jalisco', 'Playa'),
        'ciudad de méxico': ('CDMX AICM (Urbano/Negocios)', 'Ciudad de México', 'Urbano'),
        'guadalajara': ('Guadalajara (Urbano/Cultural)', 'Jalisco', 'Urbano'),
        'monterrey': ('Monterrey (Urbano/Industrial)', 'Nuevo León', 'Urbano'),
        'tijuana': ('Tijuana (Fronterizo/Urbano)', 'Baja California', 'Fronterizo'),
        'mérida': ('Mérida (Cultural/Península)', 'Yucatán', 'Cultural'),
        'oaxaca': ('Oaxaca (Cultural/Pueblos)', 'Oaxaca', 'Cultural'),
        'acapulco': ('Acapulco (Playa Tradicional)', 'Guerrero', 'Playa'),
        'toluca': ('Toluca (Corredor Insurgente)', 'Estado de México', 'Corredor')
    }
    
    registros = []
    
    for sheet in wb.sheetnames:
        try:
            anio = int(sheet)
        except ValueError:
            continue
        if anio < 2010: # Periodo consolidado 2010-2024
            continue
            
        ws = wb[sheet]
        date_cols = {}
        for c in range(1, 20):
            val = ws.cell(3, c).value
            if isinstance(val, (datetime.datetime, datetime.date)):
                date_cols[c] = val.month
        if len(date_cols) < 12:
            continue
            
        for r in range(4, ws.max_row + 1):
            c3 = ws.cell(r, 3).value
            c2 = ws.cell(r, 2).value
            nombre_raw = str(c3 or c2 or '').strip()
            
            for clave, (nombre_std, estado, tipo_destino) in destinos_clave.items():
                if clave in nombre_raw.lower():
                    # Verificar que sea la fila de total y no un subtipo
                    val_check = ws.cell(r, list(date_cols.keys())[0]).value
                    if isinstance(val_check, (int, float)):
                        for col, mes in date_cols.items():
                            val = ws.cell(r, col).value
                            if isinstance(val, (int, float)):
                                registros.append({
                                    "anio": anio,
                                    "mes": mes,
                                    "fecha": f"{anio}-{mes:02d}-01",
                                    "nombre_mes": NOMBRES_MESES[mes],
                                    "aeropuerto": nombre_std,
                                    "entidad_federativa": estado,
                                    "tipo_destino": tipo_destino,
                                    "pasajeros_llegada": int(val)
                                })
                    break
                    
    df_ap = pd.DataFrame(registros)
    df_ap = df_ap.drop_duplicates(subset=["anio", "mes", "aeropuerto"])
    df_ap = df_ap.sort_values(by=["aeropuerto", "anio", "mes"]).reset_index(drop=True)
    print(f"[+] Aeropuertos procesados: {len(df_ap)} registros ({df_ap['aeropuerto'].nunique()} aeropuertos).")
    return df_ap

def extraer_visitantes_culturales_inah():
    """
    Extrae la afluencia mensual nacional a museos y zonas arqueológicas del INAH (12_5.xlsx).
    """
    file_path = os.path.join(CETM_DIR, "12_5.xlsx")
    print(f"[*] Procesando {file_path}...")
    wb = openpyxl.load_workbook(file_path, data_only=True)
    
    registros = []
    
    for sheet in wb.sheetnames:
        try:
            anio = int(sheet)
        except ValueError:
            continue
        if anio < 2010:
            continue
            
        ws = wb[sheet]
        date_cols = {}
        for r in range(1, 8):
            for c in range(1, 20):
                val = ws.cell(r, c).value
                if isinstance(val, (datetime.datetime, datetime.date)):
                    date_cols[c] = val.month
            if len(date_cols) >= 12:
                break
        if len(date_cols) < 12:
            continue
            
        for r in range(4, 15):
            c4 = str(ws.cell(r, 4).value or ws.cell(r, 3).value or '').strip()
            if 'total de visitantes' in c4.lower() and 'nacionales' not in c4.lower() and 'internacionales' not in c4.lower():
                for col, mes in date_cols.items():
                    val = ws.cell(r, col).value
                    if isinstance(val, (int, float)):
                        registros.append({
                            "anio": anio,
                            "mes": mes,
                            "fecha": f"{anio}-{mes:02d}-01",
                            "nombre_mes": NOMBRES_MESES[mes],
                            "visitantes_inah_total": int(val)
                        })
                break
                
    df_inah = pd.DataFrame(registros)
    df_inah = df_inah.sort_values(by=["anio", "mes"]).reset_index(drop=True)
    print(f"[+] Visitas INAH procesadas: {len(df_inah)} registros.")
    return df_inah

def construir_base_datos_sqlite(df_nacional, df_aeropuertos, df_inah):
    """
    Genera la base de datos relacional SQLite y exporta tablas a CSV.
    """
    db_path = os.path.join(PROCESSED_DIR, "turismo_mexico_temporadas.db")
    print(f"[*] Construyendo base de datos SQLite en: {db_path}...")
    
    # Calcular tabla agregada de estacionalidad promedio por mes (1 a 12)
    # Excluimos 2020 para evitar la distorsión atípica de la pandemia en la estacionalidad estructural
    df_sin_pandemia = df_nacional[(df_nacional['anio'] >= 2010) & (df_nacional['anio'] != 2020)]
    
    estacionalidad = df_sin_pandemia.groupby('mes').agg(
        nombre_mes=('nombre_mes', 'first'),
        ocupacion_hotelera_promedio=('ocupacion_hotelera_pct', 'mean'),
        ocupacion_hotelera_min=('ocupacion_hotelera_pct', 'min'),
        ocupacion_hotelera_max=('ocupacion_hotelera_pct', 'max'),
        turistas_internacionales_promedio_miles=('turistas_internacionales_miles', 'mean'),
        turistas_nacionales_hoteles_promedio_miles=('turistas_hoteles_nacionales_miles', 'mean'),
        turistas_extranjeros_hoteles_promedio_miles=('turistas_hoteles_extranjeros_miles', 'mean'),
        turistas_totales_hoteles_promedio_miles=('turistas_hoteles_total_miles', 'mean'),
        pasajeros_aereos_promedio=('pasajeros_aereos_total', 'mean'),
        pasajeros_cruceros_promedio=('pasajeros_cruceros', 'mean')
    ).reset_index()
    
    # Calcular índice estacional (Base 100 = promedio anual de los 12 meses)
    prom_gral_ocup = estacionalidad['ocupacion_hotelera_promedio'].mean()
    prom_gral_turistas = estacionalidad['turistas_totales_hoteles_promedio_miles'].mean()
    
    estacionalidad['indice_estacional_ocupacion_base100'] = round(
        (estacionalidad['ocupacion_hotelera_promedio'] / prom_gral_ocup) * 100, 2
    )
    estacionalidad['indice_estacional_turistas_base100'] = round(
        (estacionalidad['turistas_totales_hoteles_promedio_miles'] / prom_gral_turistas) * 100, 2
    )
    
    def calificar_mes(indice):
        if indice >= 104.0:
            return "Temporada Alta (Peak)"
        elif indice >= 96.0:
            return "Temporada Media"
        else:
            return "Temporada Baja (Valle)"
            
    estacionalidad['tipo_temporada_anual'] = estacionalidad['indice_estacional_ocupacion_base100'].apply(calificar_mes)
    
    # Guardar en SQLite
    conn = sqlite3.connect(db_path)
    df_nacional.to_sql("temporadas_mensuales_nacional", conn, if_exists="replace", index=False)
    estacionalidad.to_sql("estacionalidad_promedio_mensual", conn, if_exists="replace", index=False)
    df_aeropuertos.to_sql("afluencia_aeropuertos_mensual", conn, if_exists="replace", index=False)
    df_inah.to_sql("visitantes_inah_cultural_mensual", conn, if_exists="replace", index=False)
    conn.close()
    
    # Exportar a CSV
    df_nacional.to_csv(os.path.join(PROCESSED_DIR, "temporadas_mensuales_nacional_1995_2024.csv"), index=False)
    estacionalidad.to_csv(os.path.join(PROCESSED_DIR, "estacionalidad_promedio_mensual_mexico.csv"), index=False)
    df_aeropuertos.to_csv(os.path.join(PROCESSED_DIR, "afluencia_aeropuertos_mensual_2010_2024.csv"), index=False)
    
    print(f"[+] Base de datos SQLite y archivos CSV creados exitosamente.")
    return estacionalidad

def generar_graficas_temporadas(df_nacional, estacionalidad, df_aeropuertos):
    """
    Genera 3 figuras ejecutivas de alta resolución para visualizar las temporadas altas en México.
    """
    print("[*] Generando visualizaciones de temporadas altas...")
    
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    # -------------------------------------------------------------
    # FIGURA 1: Los 3 Picos de Temporada Alta en México (Panel 2x2)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    
    # Subplot 1: Ocupación Hotelera e Índice Estacional
    colores_barras = [
        '#e74c3c' if t == "Temporada Alta (Peak)" else '#f39c12' if t == "Temporada Media" else '#27ae60'
        for t in estacionalidad['tipo_temporada_anual']
    ]
    bars = axes[0, 0].bar(estacionalidad['nombre_mes'], estacionalidad['ocupacion_hotelera_promedio'], 
                           color=colores_barras, edgecolor='#333333', width=0.6)
    media_ocup = estacionalidad['ocupacion_hotelera_promedio'].mean()
    axes[0, 0].axhline(media_ocup, color='#2980b9', 
                       linestyle='--', linewidth=1.5, label=f"Media Anual: {media_ocup:.1f}%")
    axes[0, 0].set_title("1. Porcentaje de Ocupación Hotelera Promedio por Mes\n(Rojo: Temporada Alta, Naranja: Media, Verde: Baja)", 
                         fontsize=11, fontweight='bold', pad=10)
    axes[0, 0].set_ylabel("Ocupación Hotelera (%)", fontsize=10)
    axes[0, 0].set_ylim(40, 70)
    axes[0, 0].tick_params(axis='x', rotation=35)
    axes[0, 0].legend(loc="lower right")
    
    for bar in bars:
        yval = bar.get_height()
        axes[0, 0].text(bar.get_x() + bar.get_width()/2, yval + 0.6, f"{yval:.1f}%", 
                        ha='center', va='bottom', fontsize=8.5, fontweight='bold')
        
    # Subplot 2: Turistas Nacionales vs Extranjeros en Hoteles (Asimetría Estacional)
    axes[0, 1].plot(estacionalidad['nombre_mes'], estacionalidad['turistas_nacionales_hoteles_promedio_miles'] / 1000.0, 
                    marker='o', linewidth=2.5, color='#2980b9', label='Turistas Nacionales (Pico Verano: Julio/Agosto)')
    axes[0, 1].plot(estacionalidad['nombre_mes'], estacionalidad['turistas_extranjeros_hoteles_promedio_miles'] / 1000.0, 
                    marker='s', linewidth=2.5, color='#e67e22', label='Turistas Extranjeros (Pico Invierno: Dic-Mar)')
    axes[0, 1].set_title("2. Asimetría de Mercados: Nacional vs Extranjero\n(Comportamiento Estacional Diferenciado)", 
                         fontsize=11, fontweight='bold', pad=10)
    axes[0, 1].set_ylabel("Millones de Turistas en Hoteles", fontsize=10)
    axes[0, 1].tick_params(axis='x', rotation=35)
    axes[0, 1].legend(loc="upper left")
    
    # Subplot 3: Llegada de Pasajeros Aéreos a Aeropuertos del País
    axes[1, 0].bar(estacionalidad['nombre_mes'], estacionalidad['pasajeros_aereos_promedio'] / 1e6, 
                   color='#8e44ad', edgecolor='#333333', width=0.55)
    axes[1, 0].set_title("3. Pasajeros Aéreos Mensuales en México (Millones)\n(Máximos en Diciembre, Julio y Marzo)", 
                         fontsize=11, fontweight='bold', pad=10)
    axes[1, 0].set_ylabel("Millones de Pasajeros", fontsize=10)
    axes[1, 0].set_ylim(3, 8)
    axes[1, 0].tick_params(axis='x', rotation=35)
    
    for bar in axes[1, 0].patches:
        yval = bar.get_height()
        axes[1, 0].text(bar.get_x() + bar.get_width()/2, yval + 0.08, f"{yval:.2f}M", 
                        ha='center', va='bottom', fontsize=8.5, fontweight='bold')
        
    # Subplot 4: Pasajeros en Cruceros (Temporada de Invierno)
    axes[1, 1].bar(estacionalidad['nombre_mes'], estacionalidad['pasajeros_cruceros_promedio'] / 1e3, 
                   color='#16a085', edgecolor='#333333', width=0.55)
    axes[1, 1].set_title("4. Pasajeros en Cruceros Marítimos (Miles)\n(Fuerte Concentración en Invierno: Noviembre a Abril)", 
                         fontsize=11, fontweight='bold', pad=10)
    axes[1, 1].set_ylabel("Miles de Cruceristas", fontsize=10)
    axes[1, 1].tick_params(axis='x', rotation=35)
    
    for bar in axes[1, 1].patches:
        yval = bar.get_height()
        axes[1, 1].text(bar.get_x() + bar.get_width()/2, yval + 10, f"{int(yval)}k", 
                        ha='center', va='bottom', fontsize=8.5, fontweight='bold')
        
    plt.suptitle("ANÁLISIS DE TEMPORADAS TURÍSTICAS EN MÉXICO (CETM 2024)\nCompendio Estadístico de Turismo - SECTUR / DataTur", 
                 fontsize=14, fontweight='bold', y=0.99)
    plt.tight_layout()
    fig1_path = os.path.join(KPIS_DIR, "fig4_estacionalidad_temporadas_mexico.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"    [v] Guardada: {fig1_path}")
    
    # -------------------------------------------------------------
    # FIGURA 2: Heatmap Histórico de Ocupación Mensual (2014-2024)
    # -------------------------------------------------------------
    df_reciente = df_nacional[df_nacional['anio'] >= 2014].copy()
    matriz_ocupacion = df_reciente.pivot(index='anio', columns='mes', values='ocupacion_hotelera_pct')
    matriz_ocupacion.columns = [NOMBRES_MESES[m] for m in matriz_ocupacion.columns]
    
    fig, ax = plt.subplots(figsize=(14, 7))
    sns.heatmap(matriz_ocupacion, annot=True, fmt=".1f", cmap="YlOrRd", cbar_kws={'label': 'Ocupación Hotelera (%)'}, 
                linewidths=0.5, ax=ax)
    ax.set_title("MAPA DE CALOR: ESTACIONALIDAD Y TEMPORADAS ALTAS EN MÉXICO (2014 - 2024)\n(Identificación de picos vacacionales y caída durante contingencia 2020)", 
                 fontsize=12, fontweight='bold', pad=15)
    ax.set_xlabel("Mes del Año", fontsize=10)
    ax.set_ylabel("Año", fontsize=10)
    plt.tight_layout()
    fig2_path = os.path.join(KPIS_DIR, "fig5_heatmap_estacionalidad_mexico.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"    [v] Guardada: {fig2_path}")
    
    # -------------------------------------------------------------
    # FIGURA 3: Comparativa de Temporadas Altas: Destinos de Playa vs Ciudades
    # -------------------------------------------------------------
    df_ap_recent = df_aeropuertos[(df_aeropuertos['anio'] >= 2018) & (df_aeropuertos['anio'] != 2020)].copy()
    ap_estac = df_ap_recent.groupby(['aeropuerto', 'mes', 'nombre_mes', 'tipo_destino'])['pasajeros_llegada'].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(13, 6))
    destinos_muestra = [
        ('Cancún (Sol y Playa)', '#e74c3c', '-'),
        ('Los Cabos (Sol y Playa)', '#e67e22', '-'),
        ('Puerto Vallarta (Sol y Playa)', '#f1c40f', '-'),
        ('CDMX AICM (Urbano/Negocios)', '#2980b9', '--'),
        ('Guadalajara (Urbano/Cultural)', '#27ae60', '--'),
        ('Monterrey (Urbano/Industrial)', '#8e44ad', '--')
    ]
    
    for dest, color, estilo in destinos_muestra:
        sub = ap_estac[ap_estac['aeropuerto'] == dest].sort_values(by='mes')
        if not sub.empty:
            base100 = (sub['pasajeros_llegada'] / sub['pasajeros_llegada'].mean()) * 100
            ax.plot(sub['nombre_mes'], base100, marker='o', label=dest, color=color, linestyle=estilo, linewidth=2.2)
            
    ax.axhline(100, color='gray', linestyle=':', label='Media Anual del Destino (100)')
    ax.set_title("COMPARATIVA ESTACIONAL: DESTINOS DE PLAYA vs. CENTROS URBANOS\n(Índice Base 100: >100 indica temporada alta del destino)", 
                 fontsize=12, fontweight='bold', pad=15)
    ax.set_ylabel("Índice Estacional Relativo (Base 100)", fontsize=10)
    ax.set_xlabel("Mes", fontsize=10)
    ax.tick_params(axis='x', rotation=30)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), frameon=True)
    plt.tight_layout()
    fig3_path = os.path.join(KPIS_DIR, "fig6_temporadas_playa_vs_ciudades.png")
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"    [v] Guardada: {fig3_path}")

def main():
    print("==================================================================")
    print("  BASE DE DATOS Y ANÁLISIS DE TEMPORADAS TURÍSTICAS EN MÉXICO     ")
    print("==================================================================")
    df_nacional = extraer_resumen_mensual_nacional()
    df_aeropuertos = extraer_pasajeros_aeropuertos()
    df_inah = extraer_visitantes_culturales_inah()
    
    estacionalidad = construir_base_datos_sqlite(df_nacional, df_aeropuertos, df_inah)
    generar_graficas_temporadas(df_nacional, estacionalidad, df_aeropuertos)
    
    print("\n[OK] Base de datos y gráficas de temporadas turísticas generadas exitosamente.")

if __name__ == "__main__":
    main()
