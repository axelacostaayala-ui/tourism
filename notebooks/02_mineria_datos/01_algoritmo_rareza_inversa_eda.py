"""
Algoritmo de Rareza Inversa y Análisis Exploratorio de Patrones Turísticos (EDA)
Proyecto Prototípico - 5to Semestre: Ciencias de Datos para Negocios
UCA: Minería de Datos y Aprendizaje de Máquina

Este script ejecuta:
1. Cálculo formal del Índice de Saturación Turística (IST) por estación/municipio.
2. Ejecución del Algoritmo de Rareza Inversa para determinar la categoría de cada Guardián.
3. Análisis de patrones temporales de afluencia (Días laborales vs Fines de semana).
4. Métricas de derrama económica en comercios locales por redención de bendiciones.
5. Generación de gráficos ejecutivos de KPIs y mapa interactivo geoespacial (Folium).
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium

# Configuración visual de gráficos
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROCESSED_DIR = os.path.join(BASE_DIR, "datos", "processed")
KPIS_DIR = os.path.join(BASE_DIR, "campana", "kpis")
CAMPANA_DIR = os.path.join(BASE_DIR, "campana")

os.makedirs(KPIS_DIR, exist_ok=True)

def cargar_datos():
    """Carga los datasets limpios del corredor y la telemetría."""
    estaciones = pd.read_csv(os.path.join(PROCESSED_DIR, "dataset_estaciones_el_insurgente.csv"))
    guardianes = pd.read_csv(os.path.join(PROCESSED_DIR, "catalogo_guardianes.csv"))
    pois = pd.read_csv(os.path.join(PROCESSED_DIR, "puntos_interes_pois.csv"))
    comercios = pd.read_csv(os.path.join(PROCESSED_DIR, "directorio_comercios_afiliados.csv"))
    eventos = pd.read_csv(os.path.join(PROCESSED_DIR, "eventos_jugadores_telemetria.csv"))
    return estaciones, guardianes, pois, comercios, eventos

def calcular_indice_saturacion_y_rareza(estaciones_df):
    """
    Calcula el Índice de Saturación Turística (IST) normalizado entre 0 y 1.
    Aplica el Algoritmo de Rareza Inversa:
      - IST < 0.35  -> Legendario
      - 0.35 <= IST < 0.60 -> Épico
      - 0.60 <= IST < 0.85 -> Raro
      - IST >= 0.85 -> Común / Fatigado
    """
    # Capacidades de diseño nominal diario por estación (estimación técnica SICT)
    capacidades_diseno = {
        "EST-01": 20000, # Zinacantepec
        "EST-02": 25000, # Toluca Centro
        "EST-03": 22000, # Metepec
        "EST-04": 20000, # Lerma
        "EST-05": 30000, # Santa Fe
        "EST-06": 20000, # Vasco de Quiroga
        "EST-07": 65000  # Observatorio
    }
    
    # Afluencia promedio estimada actual/proyectada (punto medio del rango registrado)
    afluencias_base = {
        "EST-01": 4250,
        "EST-02": 7500,
        "EST-03": 6750,
        "EST-04": 6250,
        "EST-05": 22500,
        "EST-06": 15000,
        "EST-07": 61500
    }
    
    resultados = []
    for _, row in estaciones_df.iterrows():
        e_id = row["id_estacion"]
        nombre = row["nombre_estacion"]
        capacidad = capacidades_diseno.get(e_id, 25000)
        afluencia = afluencias_base.get(e_id, 8000)
        
        # Fórmula del IST
        ist = round(afluencia / capacidad, 3)
        
        # Algoritmo de Rareza Inversa
        if ist < 0.35:
            rareza = "Legendario"
            color = "#ffd700" # Oro
            factor_multiplicador = 3.0
        elif ist < 0.60:
            rareza = "Épico"
            color = "#a335ee" # Púrpura
            factor_multiplicador = 2.0
        elif ist < 0.85:
            rareza = "Raro"
            color = "#0070dd" # Azul
            factor_multiplicador = 1.4
        else:
            rareza = "Común / Fatigado"
            color = "#9d9d9d" # Gris
            factor_multiplicador = 1.0
            
        resultados.append({
            "id_estacion": e_id,
            "nombre_estacion": nombre,
            "entidad": row["entidad"],
            "municipio_alcaldia": row["municipio_alcaldia"],
            "afluencia_diaria": afluencia,
            "capacidad_diseno": capacidad,
            "indice_saturacion_ist": ist,
            "rareza_inversa_asignada": rareza,
            "color_hex": color,
            "multiplicador_recompensa": factor_multiplicador
        })
        
    df_rareza = pd.DataFrame(resultados)
    output_path = os.path.join(PROCESSED_DIR, "indice_saturacion_rareza_estaciones.csv")
    df_rareza.to_csv(output_path, index=False)
    print(f"[+] Índice de Saturación y Rareza Inversa calculado:\n{df_rareza[['nombre_estacion', 'indice_saturacion_ist', 'rareza_inversa_asignada']]}")
    return df_rareza

def generar_visualizaciones(df_rareza, df_eventos, df_comercios):
    """Genera las 3 figuras de KPIs para la Entrega 1 y la campaña."""
    print("[*] Generando figuras de análisis de minería de datos...")
    
    # FIGURA 1: Índice de Saturación y Rareza Inversa
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.bar(df_rareza["nombre_estacion"], df_rareza["indice_saturacion_ist"], 
                  color=df_rareza["color_hex"], edgecolor="#333333", width=0.55)
    
    ax.axhline(0.35, color="#ffd700", linestyle="--", alpha=0.7, label="Umbral Legendario (<0.35)")
    ax.axhline(0.60, color="#a335ee", linestyle="--", alpha=0.7, label="Umbral Épico (<0.60)")
    ax.axhline(0.85, color="#0070dd", linestyle="--", alpha=0.7, label="Umbral Raro (<0.85)")
    
    ax.set_title("Índice de Saturación Turística (IST) y Asignación de Rareza Inversa\nTren Interurbano 'El Insurgente'", 
                 fontsize=13, fontweight='bold', pad=15)
    ax.set_ylabel("Índice de Saturación (0 = Ocioso, 1 = Límite de Capacidad)", fontsize=10)
    ax.set_ylim(0, 1.1)
    
    for bar, rareza in zip(bars, df_rareza["rareza_inversa_asignada"]):
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.03, f"{yval:.2f}\n({rareza})", 
                ha='center', va='bottom', fontsize=8.5, fontweight='bold')
        
    ax.legend(loc="upper left", frameon=True)
    plt.xticks(rotation=20, ha='right', fontsize=9.5)
    plt.tight_layout()
    fig1_path = os.path.join(KPIS_DIR, "fig1_indice_saturacion_y_rarezas.png")
    plt.savefig(fig1_path, dpi=300)
    plt.close()
    print(f"    [v] Guardada: {fig1_path}")
    
    # FIGURA 2: Patrón Temporal de Eventos (Entre semana vs Fin de semana)
    fig, ax = plt.subplots(figsize=(10, 5))
    conteo_eventos = df_eventos.groupby(["id_estacion", "es_fin_de_semana"]).size().unstack().fillna(0)
    conteo_eventos.rename(columns={False: "Días Laborales (Lun-Vie)", True: "Fin de Semana (Sáb-Dom)"}, inplace=True)
    
    estaciones_map = dict(zip(df_rareza["id_estacion"], df_rareza["nombre_estacion"]))
    conteo_eventos.index = [estaciones_map.get(idx, idx) for idx in conteo_eventos.index]
    
    conteo_eventos.plot(kind="bar", ax=ax, color=["#34495e", "#27ae60"], width=0.6, edgecolor="#222222")
    ax.set_title("Distribución de Actividad de Jugadores: Laboral vs Fin de Semana\nDemostración de Capacidad Ociosa en Destinos Emergentes", 
                 fontsize=12, fontweight='bold', pad=12)
    ax.set_ylabel("Total de Interacciones Registradas", fontsize=10)
    ax.set_xlabel("Estación del Corredor", fontsize=10)
    plt.xticks(rotation=15, ha='right')
    plt.tight_layout()
    fig2_path = os.path.join(KPIS_DIR, "fig2_patron_temporal_afluencia.png")
    plt.savefig(fig2_path, dpi=300)
    plt.close()
    print(f"    [v] Guardada: {fig2_path}")
    
    # FIGURA 3: Derrama Económica por Categoría de Comercio Afiliado
    canjes = df_eventos[df_eventos["tipo_evento"] == "COUPON_REDEEMED"]
    ahorro_total = canjes["ahorro_redencion_mxn"].sum()
    derrama_estimada = ahorro_total * 4.5 # Estimando ticket promedio 4.5x el descuento obtenido
    
    # Merge con la categoría del comercio
    canjes_com = canjes.merge(df_comercios[["id_comercio", "categoria"]], on="id_comercio", how="left")
    derrama_por_cat = canjes_com.groupby("categoria")["ahorro_redencion_mxn"].sum()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    colores_pie = ["#e67e22", "#2ecc71", "#9b59b6", "#3498db", "#1abc9c"]
    derrama_por_cat.plot(kind="pie", ax=ax, autopct='%1.1f%%', colors=colores_pie, 
                         startangle=140, textprops={'fontsize': 10, 'weight': 'bold'})
    ax.set_ylabel("")
    ax.set_title(f"Distribución de Beneficios Económicos en Comercios Locales\nDerrama Total Estimada: ${derrama_estimada:,.2f} MXN (Ahorro Turistas: ${ahorro_total:,.2f} MXN)", 
                 fontsize=11, fontweight='bold', pad=12)
    plt.tight_layout()
    fig3_path = os.path.join(KPIS_DIR, "fig3_derrama_economica_comercios.png")
    plt.savefig(fig3_path, dpi=300)
    plt.close()
    print(f"    [v] Guardada: {fig3_path}")

def crear_mapa_interactivo(df_estaciones, df_pois, df_comercios):
    """Construye un mapa interactivo en HTML con Folium mostrando el corredor, POIs y comercios."""
    print("[*] Construyendo mapa interactivo del corredor 'Guardianes del Territorio'...")
    # Coordenadas centro: Valle de Toluca - CDMX
    mapa = folium.Map(location=[19.28, -99.60], zoom_start=11, tiles="OpenStreetMap")
    
    # Coordenadas aproximadas de las estaciones del Tren Interurbano
    coords_estaciones = {
        "EST-01": [19.2830, -99.7340],
        "EST-02": [19.2890, -99.6540],
        "EST-03": [19.2540, -99.6040],
        "EST-04": [19.2840, -99.5140],
        "EST-05": [19.3590, -99.2580],
        "EST-06": [19.3780, -99.2310],
        "EST-07": [19.3980, -99.2000]
    }
    
    # Trazar la línea del tren
    puntos_linea = list(coords_estaciones.values())
    folium.PolyLine(puntos_linea, color="#e74c3c", weight=5, opacity=0.8, tooltip="Tren Interurbano 'El Insurgente'").add_to(mapa)
    
    # Grupo de capas
    capa_estaciones = folium.FeatureGroup(name="Estaciones del Tren").add_to(mapa)
    capa_pois = folium.FeatureGroup(name="Puntos de Interés (Misiones POI)").add_to(mapa)
    capa_comercios = folium.FeatureGroup(name="Comercios Locales Afiliados (Bendiciones)").add_to(mapa)
    
    # Añadir estaciones
    for _, row in df_estaciones.iterrows():
        e_id = row["id_estacion"]
        if e_id in coords_estaciones:
            coord = coords_estaciones[e_id]
            html_pop = f"""
            <div style="font-family: Arial; width: 220px;">
                <h4 style="color: #c0392b; margin-bottom: 4px;">🚆 Estación {row['nombre_estacion']}</h4>
                <b>Municipio:</b> {row['municipio_alcaldia']}<br>
                <b>Tipo:</b> {row['tipo_estacion']}<br>
                <b>Afluencia:</b> {row['afluencia_diaria_pasajeros']}
            </div>
            """
            folium.Marker(
                location=coord,
                popup=folium.Popup(html_pop, max_width=250),
                tooltip=f"Estación {row['nombre_estacion']}",
                icon=folium.Icon(color="red", icon="subway", prefix="fa")
            ).add_to(capa_estaciones)
            
    # Añadir POIs de misiones
    for _, row in df_pois.iterrows():
        html_poi = f"""
        <div style="font-family: Arial; width: 220px;">
            <h4 style="color: #2980b9; margin-bottom: 4px;">📍 POI: {row['nombre_poi']}</h4>
            <b>Guardián:</b> {row['id_guardian']}<br>
            <b>Tipo:</b> {row['tipo_poi']}<br>
            <b>Misión:</b> {row['requerimiento_mision']}
        </div>
        """
        folium.CircleMarker(
            location=[row["latitud"], row["longitud"]],
            radius=6,
            color="#2980b9",
            fill=True,
            fill_color="#3498db",
            fill_opacity=0.9,
            popup=folium.Popup(html_poi, max_width=250),
            tooltip=row["nombre_poi"]
        ).add_to(capa_pois)
        
    # Añadir Comercios Locales
    for _, row in df_comercios.iterrows():
        html_com = f"""
        <div style="font-family: Arial; width: 240px;">
            <h4 style="color: #27ae60; margin-bottom: 4px;">🏪 {row['nombre_comercio']}</h4>
            <b>Categoría:</b> {row['categoria']}<br>
            <b>Oferta:</b> <span style="color:#e67e22; font-weight:bold;">{row['descuento_oferta']}</span><br>
            <b>Contacto:</b> {row['responsable_contacto']}
        </div>
        """
        folium.CircleMarker(
            location=[row["latitud"], row["longitud"]],
            radius=7,
            color="#27ae60",
            fill=True,
            fill_color="#2ecc71",
            fill_opacity=0.9,
            popup=folium.Popup(html_com, max_width=260),
            tooltip=f"Comercio: {row['nombre_comercio']}"
        ).add_to(capa_comercios)
        
    folium.LayerControl().add_to(mapa)
    mapa_html_path = os.path.join(CAMPANA_DIR, "mapa_interactivo_corredor_guardianes.html")
    mapa.save(mapa_html_path)
    print(f"[+] Mapa interactivo generado con éxito en:\n    {mapa_html_path}")

def main():
    print("=============================================================")
    print("    GUARDIANES DEL TERRITORIO - PIPELINE DE MINERÍA EDA      ")
    print("=============================================================")
    estaciones, guardianes, pois, comercios, eventos = cargar_datos()
    df_rareza = calcular_indice_saturacion_y_rareza(estaciones)
    generar_visualizaciones(df_rareza, eventos, comercios)
    crear_mapa_interactivo(estaciones, pois, comercios)
    print("\n[OK] Pipeline de Minería y EDA completado con éxito.")

if __name__ == "__main__":
    main()
