"""
Modelo de Investigación de Operaciones: Optimización de Presupuesto Publicitario,
Redistribución de Flujos Turísticos y Asignación de Cupones en Comercios Locales.

Proyecto Prototípico - 5to Semestre: Ciencias de Datos para Negocios
Universidad Rosario Castellanos
UCA: Investigación de Operaciones
Autoría: Integrante 2 — Operations Research & Quants (monenri9-svg)

Este script formula y resuelve un modelo de Programación Lineal / Entera Mixta (LP/MILP)
utilizando el solver de alto rendimiento HiGHS (vía scipy.optimize.linprog) para:
1. Asignar de manera óptima el presupuesto de la campaña publicitaria ($250,000 MXN)
   entre los 4 nodos del Corredor 'El Insurgente', 4 canales de difusión y 3 temporadas.
2. Asignar los flujos de visitantes y redención de cupones ('Bendiciones') entre los
   15 comercios locales afiliados, maximizando la derrama económica comunitaria ponderada
   por Rareza Inversa sin rebasar la capacidad de carga de ningún comercio ni ecosistema.
3. Extraer precios sombra (variables duales), holguras y realizar análisis de sensibilidad
   paramétrico sobre el presupuesto y la capacidad de carga comunitaria.
4. Comparar el escenario tradicional (sin optimización / concentrado) frente al escenario
   optimizado sustentable y generar visualizaciones ejecutivas de alta resolución.
"""

import os
import tempfile
os.environ.setdefault("MPLCONFIGDIR", os.path.join(tempfile.gettempdir(), "mpl_cache"))
import pandas as pd
import numpy as np
from scipy.optimize import linprog
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración estética de gráficos
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans, Arial, Helvetica'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROCESSED_DIR = os.path.join(BASE_DIR, "datos", "processed")
KPIS_DIR = os.path.join(BASE_DIR, "campana", "kpis")

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(KPIS_DIR, exist_ok=True)


def cargar_insumos_corredor():
    """Carga los catálogos procesados de estaciones, rareza inversa y comercios afiliados."""
    df_rareza = pd.read_csv(os.path.join(PROCESSED_DIR, "indice_saturacion_rareza_estaciones.csv"))
    df_comercios = pd.read_csv(os.path.join(PROCESSED_DIR, "directorio_comercios_afiliados.csv"))
    cat_file = "catalogo_mexamonsters.csv" if os.path.exists(os.path.join(PROCESSED_DIR, "catalogo_mexamonsters.csv")) else "catalogo_guardianes.csv"
    df_mexamonsters = pd.read_csv(os.path.join(PROCESSED_DIR, cat_file))
    return df_rareza, df_comercios, df_mexamonsters


def parametrizar_modelo(df_rareza, df_comercios):
    """
    Define los conjuntos, índices y parámetros técnicos y económicos del modelo de IO
    alimentados por los datos reales del corredor Tren Interurbano 'El Insurgente'.
    """
    # 1. Nodos turísticos receptores del corredor (Valle de Toluca)
    nodos = ["EST-01", "EST-02", "EST-03", "EST-04"]
    nombres_nodos = {
        "EST-01": "Zinacantepec (Xinán - Legendario)",
        "EST-02": "Toluca Centro (Mosco - Raro)",
        "EST-03": "Metepec (Barrotépetl - Épico)",
        "EST-04": "Lerma (Acatl-Tule - Épico)"
    }
    nombres_cortos = {
        "EST-01": "Zinacantepec",
        "EST-02": "Toluca Centro",
        "EST-03": "Metepec",
        "EST-04": "Lerma"
    }

    # Índice de Saturación Turística (IST) y ponderador de prioridad por Rareza Inversa
    ist_map = dict(zip(df_rareza["id_estacion"], df_rareza["indice_saturacion_ist"]))
    # Factor de prioridad social/descentralización: premia destinos con menor IST
    prioridad_nodo = {
        "EST-01": 1.35,  # Zinacantepec (IST 0.212 - Mayor prioridad comunitaria)
        "EST-04": 1.25,  # Lerma / San Pedro Tultepec (IST 0.312 - Humedales y artesanía tule)
        "EST-03": 1.20,  # Metepec talleres barriales (IST 0.307 - Alfarería tradicional)
        "EST-02": 1.00   # Toluca Centro (IST 0.300 - Cabecera urbana consolidada)
    }

    # Capacidad de carga turística mensual sostenible por nodo (visitantes con canje en comercios)
    capacidad_nodo_mensual = {
        "EST-01": 1650,  # Restricción ambiental por cercanía a Parque Nacional Xinantécatl
        "EST-02": 2400,  # Mayor infraestructura urbana en Los Portales / Centro
        "EST-03": 1950,  # Capacidad de talleres familiares y Cerro de los Magueyes
        "EST-04": 1500   # Ecosistema sensible (Sitio Ramsar Ciénegas de Lerma)
    }

    # 2. Canales de difusión publicitaria (j in J)
    canales = ["CAN-01", "CAN-02", "CAN-03", "CAN-04"]
    info_canales = {
        "CAN-01": {
            "nombre": "TikTok & Instagram Reels",
            "segmento_principal": "Joven Mochilero / Familia Joven",
            "cac_base_mxn": 18.50,  # Costo de adquisición por visitante activo con canje
            "cota_min_pct": 0.20,
            "cota_max_pct": 0.40
        },
        "CAN-02": {
            "nombre": "Google Maps & Search Geolocalizado",
            "segmento_principal": "Turista Cultural / Viajero Regional",
            "cac_base_mxn": 22.00,
            "cota_min_pct": 0.15,
            "cota_max_pct": 0.35
        },
        "CAN-03": {
            "nombre": "Señalética QR en Andenes 'El Insurgente'",
            "segmento_principal": "Familia Trabajadora / Adulto Mayor",
            "cac_base_mxn": 14.00,  # Alta conversión in-transit de usuarios del tren
            "cota_min_pct": 0.22,   # Garantiza inclusión de grupos no digitalizados
            "cota_max_pct": 0.38
        },
        "CAN-04": {
            "nombre": "Micro-Influencers de Cultura y Gastronomía",
            "segmento_principal": "Multisegmento / Exploradores",
            "cac_base_mxn": 20.50,
            "cota_min_pct": 0.12,
            "cota_max_pct": 0.30
        }
    }

    # 3. Temporadas de intervención (t in T) basadas en hallazgos del CETM 2024
    temporadas = ["TEMP-VALLE", "TEMP-MEDIA", "TEMP-ALTA"]
    info_temporadas = {
        "TEMP-VALLE": {
            "nombre": "Temporada Baja / Valle (Sep-Oct)",
            "factor_eficacia_cac": 1.12,  # Cuesta 12% más atraer visitantes en valle, pero es prioritario
            "bono_desestacionalizacion": 1.30,  # Premio en función objetivo por activar meses valle
            "cota_min_presupuesto": 0.40  # Mínimo 40% del presupuesto para romper estacionalidad
        },
        "TEMP-MEDIA": {
            "nombre": "Temporada Media (May-Jun)",
            "factor_eficacia_cac": 1.00,
            "bono_desestacionalizacion": 1.10,
            "cota_min_presupuesto": 0.30
        },
        "TEMP-ALTA": {
            "nombre": "Temporada Alta Controlada (Nov-Dic)",
            "factor_eficacia_cac": 0.88,  # Alta demanda natural
            "bono_desestacionalizacion": 0.90,  # Menor peso para no saturar picos
            "cota_min_presupuesto": 0.15
        }
    }

    # 4. Parametrización microeconómica de los 15 comercios locales afiliados (k in K)
    # Basado en categoría: ticket promedio, descuento otorgado, derrama neta y capacidad mensual
    params_categoria = {
        "Gastronomía Tradicional": {"ticket_mxn": 320.0, "subsidio_cup_mxn": 45.0, "cap_mensual": 480, "min_mensual": 90},
        "Alimentos y Bebidas":     {"ticket_mxn": 180.0, "subsidio_cup_mxn": 25.0, "cap_mensual": 520, "min_mensual": 100},
        "Ecoturismo y Guías":      {"ticket_mxn": 450.0, "subsidio_cup_mxn": 85.0, "cap_mensual": 260, "min_mensual": 55},
        "Artesanías y Alfarería":  {"ticket_mxn": 410.0, "subsidio_cup_mxn": 60.0, "cap_mensual": 310, "min_mensual": 65},
        "Gastronomía y Bebidas":   {"ticket_mxn": 290.0, "subsidio_cup_mxn": 38.0, "cap_mensual": 420, "min_mensual": 80},
        "Cafetería y Cultura":     {"ticket_mxn": 210.0, "subsidio_cup_mxn": 30.0, "cap_mensual": 450, "min_mensual": 85},
        "Artesanías y Muebles":    {"ticket_mxn": 520.0, "subsidio_cup_mxn": 95.0, "cap_mensual": 220, "min_mensual": 50},
        "Ecoturismo y Movilidad":  {"ticket_mxn": 260.0, "subsidio_cup_mxn": 50.0, "cap_mensual": 340, "min_mensual": 70},
        "Gastronomía y Embutidos": {"ticket_mxn": 310.0, "subsidio_cup_mxn": 32.0, "cap_mensual": 550, "min_mensual": 110},
        "Dulces Tradicionales":    {"ticket_mxn": 195.0, "subsidio_cup_mxn": 25.0, "cap_mensual": 580, "min_mensual": 110}
    }

    comercios_lista = []
    for _, row in df_comercios.iterrows():
        cat = row["categoria"]
        p_cat = params_categoria.get(cat, {"ticket_mxn": 250.0, "subsidio_cup_mxn": 35.0, "cap_mensual": 400, "min_mensual": 75})
        est_id = row["id_estacion"]
        ticket = p_cat["ticket_mxn"]
        descuento = p_cat["subsidio_cup_mxn"]
        derrama_neta = ticket - descuento  # Ingreso líquido directo retenido por el locatario por canje

        # Emisiones de CO2 evitadas por visitante (kg CO2) al usar Tren El Insurgente vs auto
        # Distancias más largas desde CDMX ahorran más kg de CO2 por viaje redondo
        co2_evitado_kg = {"EST-01": 8.4, "EST-02": 7.6, "EST-03": 7.1, "EST-04": 6.2}.get(est_id, 7.0)

        comercios_lista.append({
            "id_comercio": row["id_comercio"],
            "nombre_comercio": row["nombre_comercio"],
            "categoria": cat,
            "municipio": row["municipio"],
            "id_estacion": est_id,
            "ticket_promedio_mxn": ticket,
            "descuento_otorgado_mxn": descuento,
            "derrama_neta_unitaria_mxn": derrama_neta,
            "capacidad_mensual_max": p_cat["cap_mensual"],
            "demanda_minima_garantizada": p_cat["min_mensual"],
            "co2_evitado_por_visita_kg": co2_evitado_kg,
            "ponderador_rareza_nodo": prioridad_nodo[est_id],
            "ist_nodo": ist_map[est_id]
        })

    df_com_params = pd.DataFrame(comercios_lista)
    return {
        "nodos": nodos,
        "nombres_nodos": nombres_nodos,
        "nombres_cortos": nombres_cortos,
        "prioridad_nodo": prioridad_nodo,
        "capacidad_nodo_mensual": capacidad_nodo_mensual,
        "canales": canales,
        "info_canales": info_canales,
        "temporadas": temporadas,
        "info_temporadas": info_temporadas,
        "df_com_params": df_com_params
    }


def resolver_modelo_io(params, presupuesto_total=250000.0, factor_capacidad=1.0):
    """
    Construye y resuelve el problema de Programación Lineal (LP) con el método HiGHS.

    Variables de decisión:
      1. x[i, j, t] >= 0: Presupuesto publicitario (MXN) asignado al nodo i, canal j, temporada t
         Total variables x: 4 nodos * 4 canales * 3 temporadas = 48 variables.
      2. y[k, t] >= 0: Número de visitantes con cupón redimido en el comercio k en la temporada t
         Total variables y: 15 comercios * 3 temporadas = 45 variables.
    Total variables de decisión: 93 variables continuas/enteras.
    """
    nodos = params["nodos"]
    canales = params["canales"]
    temporadas = params["temporadas"]
    info_canales = params["info_canales"]
    info_temporadas = params["info_temporadas"]
    capacidad_nodo = params["capacidad_nodo_mensual"]
    df_com = params["df_com_params"]
    comercios = df_com["id_comercio"].tolist()

    # Mapear índices de variables
    idx_x = {}
    curr = 0
    for i in nodos:
        for j in canales:
            for t in temporadas:
                idx_x[(i, j, t)] = curr
                curr += 1

    idx_y = {}
    for k in comercios:
        for t in temporadas:
            idx_y[(k, t)] = curr
            curr += 1

    n_vars = curr

    # -------------------------------------------------------------------------
    # FUNCIÓN OBJETIVO: Maximizar Derrama Económica Ponderada por Rareza Inversa
    # y Desestacionalización + Valoración Ecológica de CO2 Evitado.
    # En linprog se minimiza, por lo que multiplicamos por -1.
    # -------------------------------------------------------------------------
    c = np.zeros(n_vars)

    # Pequeño costo de fricción administrativa sobre x para evitar gasto ocioso sin conversión
    for (i, j, t), pos in idx_x.items():
        c[pos] = 0.001

    for _, row in df_com.iterrows():
        k = row["id_comercio"]
        derrama = row["derrama_neta_unitaria_mxn"]
        w_rareza = row["ponderador_rareza_nodo"]
        co2_kg = row["co2_evitado_por_visita_kg"]
        bono_ambiental_mxn = co2_kg * 1.50  # Precio social sombra del carbono ($1.50 MXN / kg CO2)

        for t in temporadas:
            w_temp = info_temporadas[t]["bono_desestacionalizacion"]
            beneficio_unitario = (derrama * w_rareza * w_temp) + bono_ambiental_mxn
            c[idx_y[(k, t)]] = -beneficio_unitario

    # -------------------------------------------------------------------------
    # RESTRICCIONES DE DESIGUALDAD (A_ub * v <= b_ub)
    # -------------------------------------------------------------------------
    A_ub = []
    b_ub = []
    nombres_restricciones = []

    # R1. Presupuesto Total Disponible de la Campaña: sum(x_{i,j,t}) <= B_total
    row_r1 = np.zeros(n_vars)
    for pos in idx_x.values():
        row_r1[pos] = 1.0
    A_ub.append(row_r1)
    b_ub.append(presupuesto_total)
    nombres_restricciones.append("R1_Presupuesto_Total_Campana")

    # R2. Conversión Publicitaria a Flujo de Visitantes por Nodo y Temporada:
    # sum_{k in K_i} y_{k,t} - sum_{j in J} (1 / CAC_{i,j,t}) * x_{i,j,t} <= 0
    for i in nodos:
        comercios_i = df_com[df_com["id_estacion"] == i]["id_comercio"].tolist()
        for t in temporadas:
            row_conv = np.zeros(n_vars)
            for k in comercios_i:
                row_conv[idx_y[(k, t)]] = 1.0
            for j in canales:
                # Ajuste de eficiencia de conversión por afinidad nodo-canal
                afinidad = 1.0
                if i == "EST-01" and j in ["CAN-01", "CAN-04"]:
                    afinidad = 0.90  # Mayor tracción en redes para aventura en volcán
                elif i == "EST-03" and j in ["CAN-01", "CAN-02"]:
                    afinidad = 0.92  # Alta búsqueda en Maps/Reels para Pueblo Mágico Metepec
                elif i == "EST-04" and j in ["CAN-03", "CAN-04"]:
                    afinidad = 0.91  # Excelente respuesta en tren y nicho ecoturístico
                elif i == "EST-02" and j == "CAN-03":
                    afinidad = 0.88  # Alto flujo en estación Toluca Centro

                cac_efectivo = info_canales[j]["cac_base_mxn"] * info_temporadas[t]["factor_eficacia_cac"] * afinidad
                tasa_conversion = 1.0 / cac_efectivo
                row_conv[idx_x[(i, j, t)]] = -tasa_conversion

            A_ub.append(row_conv)
            b_ub.append(0.0)
            nombres_restricciones.append(f"R2_Conversion_Publicitaria_{i}_{t}")

    # R3. Capacidad de Carga Ecosistémica y Urbana por Destino y Temporada:
    # sum_{k in K_i} y_{k,t} <= Capacidad_Nodo_i * factor_capacidad
    for i in nodos:
        comercios_i = df_com[df_com["id_estacion"] == i]["id_comercio"].tolist()
        cap_max_i = capacidad_nodo[i] * factor_capacidad
        for t in temporadas:
            # En temporada alta se restringe un 15% adicional la capacidad disponible para la campaña
            # porque ya existe flujo turístico basal que ocupa parte del destino
            factor_estacional_cap = 0.85 if t == "TEMP-ALTA" else (1.05 if t == "TEMP-VALLE" else 1.0)
            row_cap_nodo = np.zeros(n_vars)
            for k in comercios_i:
                row_cap_nodo[idx_y[(k, t)]] = 1.0
            A_ub.append(row_cap_nodo)
            b_ub.append(cap_max_i * factor_estacional_cap)
            nombres_restricciones.append(f"R3_Capacidad_Carga_Nodo_{i}_{t}")

    # R4. Equidad Territorial entre Municipios (Cota Mínima >= 20% y Cota Máxima <= 32% del Presupuesto)
    for i in nodos:
        # Cota máxima: sum_{j,t} x_{i,j,t} <= 0.32 * B_total
        row_eq_max = np.zeros(n_vars)
        for j in canales:
            for t in temporadas:
                row_eq_max[idx_x[(i, j, t)]] = 1.0
        A_ub.append(row_eq_max)
        b_ub.append(0.32 * presupuesto_total)
        nombres_restricciones.append(f"R4_Equidad_Max_Nodo_{i}")

        # Cota mínima: -sum_{j,t} x_{i,j,t} <= -0.20 * B_total
        row_eq_min = -row_eq_max.copy()
        A_ub.append(row_eq_min)
        b_ub.append(-0.20 * presupuesto_total)
        nombres_restricciones.append(f"R4_Equidad_Min_Nodo_{i}")

    # R5. Diversificación Estratégica por Canal de Difusión (Cota Mínima y Máxima)
    for j in canales:
        c_min = info_canales[j]["cota_min_pct"]
        c_max = info_canales[j]["cota_max_pct"]
        row_can_max = np.zeros(n_vars)
        for i in nodos:
            for t in temporadas:
                row_can_max[idx_x[(i, j, t)]] = 1.0
        A_ub.append(row_can_max)
        b_ub.append(c_max * presupuesto_total)
        nombres_restricciones.append(f"R5_Canal_Max_{j}")

        row_can_min = -row_can_max.copy()
        A_ub.append(row_can_min)
        b_ub.append(-c_min * presupuesto_total)
        nombres_restricciones.append(f"R5_Canal_Min_{j}")

    # R6. Priorización Contracíclica por Temporada (Impulso a Temporada Valle y Media)
    for t in temporadas:
        t_min = info_temporadas[t]["cota_min_presupuesto"]
        row_temp_min = np.zeros(n_vars)
        for i in nodos:
            for j in canales:
                row_temp_min[idx_x[(i, j, t)]] = -1.0
        A_ub.append(row_temp_min)
        b_ub.append(-t_min * presupuesto_total)
        nombres_restricciones.append(f"R6_Temporada_Min_{t}")

    # -------------------------------------------------------------------------
    # COTAS INDIVIDUALES DE VARIABLES (Bounds):
    # - Capacidad de Carga Física de cada Comercio Local Afiliado (y_{k,t} <= Cap_k)
    # - Demanda Mínima Garantizada para cada Locatario (y_{k,t} >= Min_k)
    # -------------------------------------------------------------------------
    bounds = []
    for _ in range(len(idx_x)):
        bounds.append((0.0, None))

    # Escalar el piso mínimo si el presupuesto evaluado en sensibilidad es muy bajo
    escala_piso = min(1.0, presupuesto_total / 200000.0) * min(1.0, factor_capacidad)
    for _, row in df_com.iterrows():
        cap_k = row["capacidad_mensual_max"] * factor_capacidad
        min_k = row["demanda_minima_garantizada"] * escala_piso
        for t in temporadas:
            bounds.append((min_k, cap_k))

    # Resolver con HiGHS
    res = linprog(
        c=c,
        A_ub=np.array(A_ub),
        b_ub=np.array(b_ub),
        bounds=bounds,
        method="highs"
    )

    return res, idx_x, idx_y, nombres_restricciones, A_ub, b_ub


def estructurar_resultados(res, params, idx_x, idx_y, nombres_restricciones, b_ub):
    """Extrae las tablas de solución óptima, métricas de impacto y precios sombra."""
    df_com = params["df_com_params"]
    info_canales = params["info_canales"]
    info_temporadas = params["info_temporadas"]
    nombres_cortos = params["nombres_cortos"]

    # 1. Tabla de asignación óptima de presupuesto x[i, j, t]
    filas_x = []
    for (i, j, t), pos in idx_x.items():
        monto = res.x[pos]
        filas_x.append({
            "id_estacion": i,
            "destino": nombres_cortos[i],
            "id_canal": j,
            "nombre_canal": info_canales[j]["nombre"],
            "id_temporada": t,
            "nombre_temporada": info_temporadas[t]["nombre"],
            "presupuesto_asignado_mxn": round(float(monto), 2)
        })
    df_sol_presupuesto = pd.DataFrame(filas_x)

    # 2. Tabla de flujos de visitantes y derrama por comercio y[k, t]
    filas_y = []
    for _, row in df_com.iterrows():
        k = row["id_comercio"]
        for t in params["temporadas"]:
            pos = idx_y[(k, t)]
            visitas = res.x[pos]
            gasto_bruto = visitas * row["ticket_promedio_mxn"]
            descuento_total = visitas * row["descuento_otorgado_mxn"]
            derrama_neta = visitas * row["derrama_neta_unitaria_mxn"]
            co2_evitado = visitas * row["co2_evitado_por_visita_kg"]
            cap_max = row["capacidad_mensual_max"]
            uso_capacidad_pct = (visitas / cap_max) * 100.0

            filas_y.append({
                "id_comercio": k,
                "nombre_comercio": row["nombre_comercio"],
                "categoria": row["categoria"],
                "id_estacion": row["id_estacion"],
                "municipio": row["municipio"],
                "id_temporada": t,
                "nombre_temporada": info_temporadas[t]["nombre"],
                "visitantes_cupon_optimo": round(float(visitas), 1),
                "capacidad_maxima_mensual": cap_max,
                "utilizacion_capacidad_pct": round(float(uso_capacidad_pct), 1),
                "gasto_bruto_turistas_mxn": round(float(gasto_bruto), 2),
                "ahorro_descuentos_turistas_mxn": round(float(descuento_total), 2),
                "derrama_neta_comercio_mxn": round(float(derrama_neta), 2),
                "co2_evitado_kg": round(float(co2_evitado), 2)
            })
    df_sol_comercios = pd.DataFrame(filas_y)

    # 3. Tabla de Precios Sombra (Dualidad) y Holguras de las Restricciones Estructurales
    marginals = res.ineqlin.marginals
    slacks = res.ineqlin.residual
    filas_dual = []
    for nombre_r, rhs, dual_val, slack_val in zip(nombres_restricciones, b_ub, marginals, slacks):
        # Como linprog minimiza -Z, el precio sombra de maximización es -dual_val
        precio_sombra_max = -float(dual_val) if abs(dual_val) > 1e-7 else 0.0
        filas_dual.append({
            "restriccion": nombre_r,
            "cota_derecha_rhs": round(float(rhs), 2),
            "holgura_slack": round(float(slack_val), 2),
            "estado_restriccion": "Activa (Saturada)" if abs(slack_val) < 1e-4 else "Con Holgura",
            "precio_sombra_marginal": round(precio_sombra_max, 4)
        })
    df_dualidad = pd.DataFrame(filas_dual)

    return df_sol_presupuesto, df_sol_comercios, df_dualidad


def ejecutar_analisis_sensibilidad(params):
    """
    Evalúa la sensibilidad del modelo ante variaciones en:
    1. Presupuesto Total Publicitario ($150k a $400k MXN).
    2. Factor de Capacidad de Carga Comunitaria (0.70x a 1.30x).
    """
    escenarios_sens = []
    presupuestos = [150000, 200000, 250000, 300000, 350000, 400000]
    factores_cap = [0.80, 1.00, 1.20]

    for f_cap in factores_cap:
        for b_tot in presupuestos:
            res_s, idx_x_s, idx_y_s, nombres_r, _, b_rhs = resolver_modelo_io(
                params, presupuesto_total=b_tot, factor_capacidad=f_cap
            )
            if res_s.success:
                _, df_com_s, df_dual_s = estructurar_resultados(
                    res_s, params, idx_x_s, idx_y_s, nombres_r, b_rhs
                )
                derrama_total = df_com_s["derrama_neta_comercio_mxn"].sum()
                gasto_bruto = df_com_s["gasto_bruto_turistas_mxn"].sum()
                visitas_totales = df_com_s["visitantes_cupon_optimo"].sum()
                co2_total = df_com_s["co2_evitado_kg"].sum()
                roas_social = derrama_total / b_tot
                dual_presupuesto = df_dual_s.loc[
                    df_dual_s["restriccion"] == "R1_Presupuesto_Total_Campana", "precio_sombra_marginal"
                ].values[0]

                escenarios_sens.append({
                    "presupuesto_campana_mxn": b_tot,
                    "factor_capacidad_carga": f_cap,
                    "etiqueta_capacidad": f"Capacidad {int(f_cap*100)}%",
                    "visitantes_canalizados": round(visitas_totales, 0),
                    "gasto_bruto_turistas_mxn": round(gasto_bruto, 2),
                    "derrama_neta_comunitaria_mxn": round(derrama_total, 2),
                    "roas_comunitario_neto": round(roas_social, 2),
                    "co2_evitado_total_kg": round(co2_total, 1),
                    "precio_sombra_presupuesto": round(dual_presupuesto, 4)
                })

    return pd.DataFrame(escenarios_sens)


def comparar_escenarios_tradicional_vs_optimizado(df_sol_presupuesto, df_sol_comercios, params):
    """
    Compara la estrategia de asignación tradicional (concentrada en el polo urbano Toluca
    y en Temporada Alta sin restricciones de capacidad local) frente a la solución óptima
    del modelo de Investigación de Operaciones.
    """
    # Escenario Optimizado (Solución IO)
    por_nodo_opt = df_sol_comercios.groupby(["id_estacion", "municipio"]).agg(
        visitas_optimizadas=("visitantes_cupon_optimo", "sum"),
        derrama_optimizada_mxn=("derrama_neta_comercio_mxn", "sum"),
        co2_optimizado_kg=("co2_evitado_kg", "sum"),
        uso_cap_promedio_opt=("utilizacion_capacidad_pct", "mean")
    ).reset_index()

    pres_nodo_opt = df_sol_presupuesto.groupby("id_estacion")["presupuesto_asignado_mxn"].sum().reset_index()
    por_nodo_opt = por_nodo_opt.merge(pres_nodo_opt, on="id_estacion")

    # Escenario Tradicional Inercial (Sin IO: 55% en Toluca Centro, 25% Metepec, 10% Lerma, 10% Zinacantepec,
    # concentrado 65% en Temporada Alta, generando saturación en centros urbanos y subutilización en periferias)
    pesos_trad = {"EST-01": 0.10, "EST-02": 0.55, "EST-03": 0.23, "EST-04": 0.12}
    cac_tradicional_promedio = 22.80  # Menor eficiencia por saturación de pauta en temporada alta

    comparativa = []
    for _, row in por_nodo_opt.iterrows():
        est = row["id_estacion"]
        p_trad = 250000.0 * pesos_trad[est]
        visitas_trad = p_trad / cac_tradicional_promedio
        # En el escenario tradicional, parte de la demanda en Toluca rebasa capacidad de comercios locales (desperdicio/fuga)
        factor_retencion_local = 0.72 if est == "EST-02" else 0.90
        derrama_unit_media = (
            params["df_com_params"][params["df_com_params"]["id_estacion"] == est]["derrama_neta_unitaria_mxn"].mean()
        )
        derrama_trad = visitas_trad * factor_retencion_local * derrama_unit_media
        cap_trimestral_nodo = params["capacidad_nodo_mensual"][est] * 3.0
        uso_cap_trad = (visitas_trad / cap_trimestral_nodo) * 100.0

        comparativa.append({
            "id_estacion": est,
            "municipio": row["municipio"],
            "presupuesto_tradicional_mxn": round(p_trad, 2),
            "presupuesto_optimizado_mxn": round(row["presupuesto_asignado_mxn"], 2),
            "visitas_tradicional": round(visitas_trad, 0),
            "visitas_optimizadas": round(row["visitas_optimizadas"], 0),
            "derrama_tradicional_mxn": round(derrama_trad, 2),
            "derrama_optimizada_mxn": round(row["derrama_optimizada_mxn"], 2),
            "saturacion_tradicional_pct": round(uso_cap_trad, 1),
            "saturacion_optimizada_pct": round(row["uso_cap_promedio_opt"], 1),
            "co2_optimizado_kg": round(row["co2_optimizado_kg"], 1)
        })

    return pd.DataFrame(comparativa)


def generar_visualizaciones_io(df_sol_presupuesto, df_sol_comercios, df_sensibilidad, df_comparativa):
    """Genera 3 figuras de alta resolución en campana/kpis/ para el informe y coloquio."""
    print("[*] Generando gráficas de Investigación de Operaciones...")

    # -------------------------------------------------------------------------
    # FIGURA 7: Asignación Óptima del Presupuesto por Destino, Canal y Temporada
    # -------------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Subplot 1: Presupuesto por Destino y Canal (Barras apiladas)
    piv_canal = df_sol_presupuesto.pivot_table(
        index="destino", columns="nombre_canal", values="presupuesto_asignado_mxn", aggfunc="sum"
    )
    # Ordenar por prioridad
    orden_destinos = ["Zinacantepec", "Lerma", "Metepec", "Toluca Centro"]
    piv_canal = piv_canal.reindex([d for d in orden_destinos if d in piv_canal.index])

    colores_canales = ["#2980b9", "#27ae60", "#e67e22", "#8e44ad"]
    piv_canal.plot(kind="bar", stacked=True, ax=axes[0], color=colores_canales, edgecolor="#222222", width=0.58)
    axes[0].set_title(
        "1. Asignación Óptima del Presupuesto por Destino y Canal\n(Equidad Territorial: Cota 20% - 32% por Municipio)",
        fontsize=11, fontweight="bold", pad=12
    )
    axes[0].set_ylabel("Presupuesto Asignado ($ MXN)", fontsize=10)
    axes[0].set_xlabel("Nodo / Municipio del Corredor", fontsize=10)
    axes[0].tick_params(axis="x", rotation=15)
    axes[0].legend(title="Canal de Difusión", fontsize=8.5, title_fontsize=9, loc="upper left", frameon=True)

    # Etiquetas de total por barra
    totales_nodo = piv_canal.sum(axis=1)
    for idx, total in enumerate(totales_nodo):
        axes[0].text(idx, total + 1500, f"${total:,.0f}\n({total/2500:.1f}%)", ha="center", va="bottom", fontsize=9, fontweight="bold")
    axes[0].set_ylim(0, max(totales_nodo) * 1.38)

    # Subplot 2: Presupuesto por Temporada y Destino (Estrategia Contracíclica)
    piv_temp = df_sol_presupuesto.pivot_table(
        index="nombre_temporada", columns="destino", values="presupuesto_asignado_mxn", aggfunc="sum"
    )
    orden_temp = [
        "Temporada Baja / Valle (Sep-Oct)",
        "Temporada Media (May-Jun)",
        "Temporada Alta Controlada (Nov-Dic)"
    ]
    piv_temp = piv_temp.reindex([t for t in orden_temp if t in piv_temp.index])

    colores_nodos = ["#f39c12", "#16a085", "#9b59b6", "#34495e"]
    piv_temp.plot(kind="bar", stacked=True, ax=axes[1], color=colores_nodos, edgecolor="#222222", width=0.55)
    axes[1].set_title(
        "2. Distribución Temporal Contracíclica del Presupuesto\n(Priorización en Temporada Valle para Aplanar Estacionalidad)",
        fontsize=11, fontweight="bold", pad=12
    )
    axes[1].set_ylabel("Presupuesto Asignado ($ MXN)", fontsize=10)
    axes[1].set_xlabel("Temporada de Intervención", fontsize=10)
    axes[1].tick_params(axis="x", rotation=12)
    axes[1].legend(title="Destino Receptor", fontsize=8.5, title_fontsize=9, loc="upper right")

    totales_temp = piv_temp.sum(axis=1)
    for idx, total in enumerate(totales_temp):
        axes[1].text(idx, total + 1800, f"${total:,.0f}\n({total/2500:.1f}%)", ha="center", va="bottom", fontsize=9, fontweight="bold")
    axes[1].set_ylim(0, max(totales_temp) * 1.18)

    plt.suptitle(
        "INVESTIGACIÓN DE OPERACIONES: OPTIMIZACIÓN DEL PRESUPUESTO PUBLICITARIO ($250,000 MXN)\nCorredor Tren Interurbano 'El Insurgente' — Mexamonsters",
        fontsize=13, fontweight="bold", y=1.01
    )
    plt.tight_layout()
    fig7_path = os.path.join(KPIS_DIR, "fig7_io_asignacion_optima_presupuesto.png")
    plt.savefig(fig7_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"    [v] Guardada: {fig7_path}")

    # -------------------------------------------------------------------------
    # FIGURA 8: Flujo Óptimo de Cupones y Capacidad de Carga en los 15 Comercios
    # -------------------------------------------------------------------------
    resumen_com = df_sol_comercios.groupby(["id_comercio", "nombre_comercio", "municipio", "categoria"]).agg(
        visitas_trimestre=("visitantes_cupon_optimo", "sum"),
        cap_trimestre=("capacidad_maxima_mensual", "sum"),
        derrama_trimestre=("derrama_neta_comercio_mxn", "sum"),
        uso_cap_pct=("utilizacion_capacidad_pct", "mean")
    ).reset_index()

    resumen_com = resumen_com.sort_values(by="derrama_trimestre", ascending=True)
    etiquetas_y = [f"{r['id_comercio']} | {r['nombre_comercio'][:28]} ({r['municipio'][:6]}.)" for _, r in resumen_com.iterrows()]

    fig, axes = plt.subplots(1, 2, figsize=(16, 7.5), sharey=True)

    # Subplot 1: Visitantes Canalizados vs Capacidad de Carga Trimestral
    y_pos = np.arange(len(resumen_com))
    axes[0].barh(y_pos, resumen_com["cap_trimestre"], color="#ecf0f1", edgecolor="#95a5a6", height=0.68, label="Capacidad de Carga Máxima Sostenible")
    axes[0].barh(y_pos, resumen_com["visitas_trimestre"], color="#2ecc71", edgecolor="#27ae60", height=0.48, label="Flujo Óptimo Asignado (Visitantes con Cupón)")
    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels(etiquetas_y, fontsize=9)
    axes[0].set_xlabel("Visitantes con Cupón Redimido (Trimestre)", fontsize=10)
    axes[0].set_title(
        "1. Flujo de Visitantes vs. Límite de Capacidad de Carga\n(Cero Sobresaturación en Fondas, Talleres y Ecoturismo)",
        fontsize=11, fontweight="bold", pad=10
    )
    axes[0].legend(loc="lower right", frameon=True, fontsize=8.5)

    for idx, (_, r) in enumerate(resumen_com.iterrows()):
        axes[0].text(
            r["visitas_trimestre"] + 15, idx,
            f"{int(r['visitas_trimestre'])}/{int(r['cap_trimestre'])} ({r['uso_cap_pct']:.0f}%)",
            va="center", fontsize=8, fontweight="bold", color="#1e8449"
        )
    axes[0].set_xlim(0, max(resumen_com["cap_trimestre"]) * 1.22)

    # Subplot 2: Derrama Económica Neta Generada por Comercio ($ MXN)
    colores_mun = {
        "Zinacantepec": "#f39c12",
        "Metepec": "#9b59b6",
        "Lerma": "#16a085",
        "Toluca de Lerdo": "#3498db"
    }
    c_bars = [colores_mun.get(m, "#34495e") for m in resumen_com["municipio"]]
    axes[1].barh(y_pos, resumen_com["derrama_trimestre"] / 1000.0, color=c_bars, edgecolor="#222222", height=0.58)
    axes[1].set_xlabel("Derrama Económica Neta Retenida (Miles de $ MXN)", fontsize=10)
    axes[1].set_title(
        "2. Derrama Económica Neta Capturada por Comercio Local\n(Descontando el Valor del Cupón Otorgado al Viajero)",
        fontsize=11, fontweight="bold", pad=10
    )

    for idx, val in enumerate(resumen_com["derrama_trimestre"] / 1000.0):
        axes[1].text(val + 5, idx, f"${val:,.1f}k MXN", va="center", fontsize=8.5, fontweight="bold")
    axes[1].set_xlim(0, max(resumen_com["derrama_trimestre"] / 1000.0) * 1.22)

    plt.suptitle(
        "ASIGNACIÓN ÓPTIMA DE FLUJOS Y DERRAMA COMUNITARIA EN LOS 15 COMERCIOS AFILIADOS\nSolución de Programación Lineal — Respeto Estricto a la Capacidad de Carga Local",
        fontsize=13, fontweight="bold", y=1.01
    )
    plt.tight_layout()
    fig8_path = os.path.join(KPIS_DIR, "fig8_io_flujos_y_capacidad_comercios.png")
    plt.savefig(fig8_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"    [v] Guardada: {fig8_path}")

    # -------------------------------------------------------------------------
    # FIGURA 9: Análisis de Sensibilidad Paramétrico y Comparativa de Escenarios
    # -------------------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(15, 5.8))

    # Subplot 1: Curvas de Sensibilidad (Presupuesto vs Derrama bajo 3 niveles de Capacidad)
    colores_cap = {"Capacidad 80%": "#e74c3c", "Capacidad 100%": "#2980b9", "Capacidad 120%": "#27ae60"}
    for etiq, grp in df_sensibilidad.groupby("etiqueta_capacidad"):
        axes[0].plot(
            grp["presupuesto_campana_mxn"] / 1000.0,
            grp["derrama_neta_comunitaria_mxn"] / 1e6,
            marker="o", linewidth=2.4, label=etiq, color=colores_cap.get(etiq, "#333333")
        )

    axes[0].axvline(250, color="#7f8c8d", linestyle="--", linewidth=1.3, label="Presupuesto Base ($250k)")
    axes[0].set_title(
        "1. Análisis de Sensibilidad: Presupuesto vs. Derrama Neta\n(Efecto de Saturación de Capacidad de Carga a Altos Presupuestos)",
        fontsize=11, fontweight="bold", pad=12
    )
    axes[0].set_xlabel("Presupuesto de Campaña Publicitaria (Miles de $ MXN)", fontsize=10)
    axes[0].set_ylabel("Derrama Neta Comunitaria (Millones de $ MXN)", fontsize=10)
    axes[0].legend(title="Escenario de Capacidad", frameon=True)

    # Subplot 2: Comparativa Escenario Inercial (Tradicional) vs. Optimizado Sustentable (IO)
    x_idx = np.arange(len(df_comparativa))
    width = 0.36
    axes[1].bar(
        x_idx - width/2, df_comparativa["derrama_tradicional_mxn"] / 1000.0,
        width=width, color="#95a5a6", edgecolor="#222222", label="Escenario Tradicional (Concentrado en Toluca)"
    )
    axes[1].bar(
        x_idx + width/2, df_comparativa["derrama_optimizada_mxn"] / 1000.0,
        width=width, color="#27ae60", edgecolor="#222222", label="Escenario Optimizado IO (Redistribución Sustentable)"
    )

    axes[1].set_xticks(x_idx)
    axes[1].set_xticklabels(df_comparativa["municipio"], fontsize=9.5)
    axes[1].set_ylabel("Derrama Económica Neta (Miles de $ MXN)", fontsize=10)
    axes[1].set_title(
        "2. Impacto Redistributivo: Tradicional vs. Modelo de Optimización\n(Incremento de Beneficios en Zinacantepec, Lerma y Metepec)",
        fontsize=11, fontweight="bold", pad=12
    )
    axes[1].legend(loc="upper right", frameon=True)

    for i, r in df_comparativa.iterrows():
        axes[1].text(i - width/2, r["derrama_tradicional_mxn"]/1000.0 + 18, f"${r['derrama_tradicional_mxn']/1000.0:,.0f}k", ha="center", fontsize=8)
        axes[1].text(i + width/2, r["derrama_optimizada_mxn"]/1000.0 + 18, f"${r['derrama_optimizada_mxn']/1000.0:,.0f}k", ha="center", fontsize=8, fontweight="bold", color="#1e8449")
    axes[1].set_ylim(0, max(df_comparativa["derrama_tradicional_mxn"].max(), df_comparativa["derrama_optimizada_mxn"].max()) / 1000.0 * 1.22)

    plt.suptitle(
        "ANÁLISIS DE SENSIBILIDAD Y COMPARACIÓN DE ESCENARIOS DE TOMA DE DECISIONES",
        fontsize=13, fontweight="bold", y=1.01
    )
    plt.tight_layout()
    fig9_path = os.path.join(KPIS_DIR, "fig9_io_sensibilidad_y_comparativa.png")
    plt.savefig(fig9_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"    [v] Guardada: {fig9_path}")


def main():
    print("=========================================================================")
    print("  MODELO DE INVESTIGACIÓN DE OPERACIONES - MEXAMONSTERS                  ")
    print("=========================================================================")

    df_rareza, df_comercios, df_mexamonsters = cargar_insumos_corredor()
    params = parametrizar_modelo(df_rareza, df_comercios)

    # Resolver modelo base ($250,000 MXN, Capacidad 100%)
    presupuesto_base = 250000.0
    res, idx_x, idx_y, nombres_r, A_ub, b_ub = resolver_modelo_io(
        params, presupuesto_total=presupuesto_base, factor_capacidad=1.0
    )

    if not res.success:
        raise RuntimeError(f"El modelo de optimización no convergió: {res.message}")

    print(f"[+] Estado del Solver HiGHS: ÓPTIMO ENCONTRADO ({res.message})")

    df_sol_presupuesto, df_sol_comercios, df_dualidad = estructurar_resultados(
        res, params, idx_x, idx_y, nombres_r, b_ub
    )

    # Ejecutar análisis de sensibilidad y comparativa
    df_sensibilidad = ejecutar_analisis_sensibilidad(params)
    df_comparativa = comparar_escenarios_tradicional_vs_optimizado(df_sol_presupuesto, df_sol_comercios, params)

    # Exportar tablas técnicas a datos/processed/
    df_sol_presupuesto.to_csv(os.path.join(PROCESSED_DIR, "io_asignacion_optima_presupuesto.csv"), index=False)
    df_sol_comercios.to_csv(os.path.join(PROCESSED_DIR, "io_flujos_optimos_comercios.csv"), index=False)
    df_dualidad.to_csv(os.path.join(PROCESSED_DIR, "io_precios_sombra_dualidad.csv"), index=False)
    df_sensibilidad.to_csv(os.path.join(PROCESSED_DIR, "io_analisis_sensibilidad.csv"), index=False)
    df_comparativa.to_csv(os.path.join(PROCESSED_DIR, "io_comparativa_escenarios.csv"), index=False)

    # Resumen ejecutivo en consola
    visitas_tot = df_sol_comercios["visitantes_cupon_optimo"].sum()
    gasto_bruto_tot = df_sol_comercios["gasto_bruto_turistas_mxn"].sum()
    ahorro_tot = df_sol_comercios["ahorro_descuentos_turistas_mxn"].sum()
    derrama_neta_tot = df_sol_comercios["derrama_neta_comercio_mxn"].sum()
    co2_tot = df_sol_comercios["co2_evitado_kg"].sum()
    roas_neto = derrama_neta_tot / presupuesto_base

    print("\n--- RESUMEN DE LA SOLUCIÓN ÓPTIMA (TRIMESTRAL) ---")
    print(f"  • Presupuesto Publicitario Invertido : ${presupuesto_base:,.2f} MXN")
    print(f"  • Visitantes con Cupón Canalizados   : {visitas_tot:,.0f} viajeros")
    print(f"  • Gasto Turístico Bruto en Comercios : ${gasto_bruto_tot:,.2f} MXN")
    print(f"  • Ahorro Directo Otorgado al Viajero : ${ahorro_tot:,.2f} MXN")
    print(f"  • Derrama Económica Neta Comunitaria : ${derrama_neta_tot:,.2f} MXN")
    print(f"  • Retorno Social sobre Pauta (ROAS)  : {roas_neto:.2f}x ($ MXN netos por cada $1 de pauta)")
    print(f"  • Emisiones Evitadas (Tren vs Auto)  : {co2_tot:,.1f} kg de CO2 ({co2_tot/1000.0:.2f} toneladas)")

    print("\n--- DISTRIBUCIÓN POR NODO / MUNICIPIO ---")
    print(df_comparativa[[
        "municipio", "presupuesto_optimizado_mxn", "visitas_optimizadas",
        "derrama_tradicional_mxn", "derrama_optimizada_mxn", "saturacion_optimizada_pct"
    ]].to_string(index=False))

    print("\n--- PRECIOS SOMBRA PRINCIPALES (RESTRICCIONES ACTIVAS) ---")
    activas = df_dualidad[df_dualidad["estado_restriccion"] == "Activa (Saturada)"]
    print(activas.to_string(index=False))

    generar_visualizaciones_io(df_sol_presupuesto, df_sol_comercios, df_sensibilidad, df_comparativa)
    print("\n[OK] Pipeline de Investigación de Operaciones finalizado exitosamente.")


if __name__ == "__main__":
    main()
