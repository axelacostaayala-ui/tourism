# Base de Datos de Estacionalidad y Temporadas Turísticas en México

> **Compendio Estadístico del Turismo en México (CETM 2024 - SECTUR / DataTur)**  
> *Proyecto Prototípico de 5to Semestre — Licenciatura en Ciencias de Datos para Negocios (Universidad Rosario Castellanos)*  
> * **UCA:** Herramientas para el Almacenamiento de Grandes Volúmenes de Datos (Big Data) & Minería de Datos  
> * **Archivo de Base de Datos:** [`datos/processed/turismo_mexico_temporadas.db`](../datos/processed/turismo_mexico_temporadas.db)  
> * **Fecha de procesamiento:** Noviembre 2026

---

## 1. 🎯 Propósito y Alcance del Procesamiento

A partir de la carpeta oficial **CETM2024** (Compendio Estadístico del Turismo en México 2024, emitido por la Secretaría de Turismo Federal y DataTur), se diseñó un pipeline automatizado en Python para:
1. Ingestar, limpiar y normalizar **30 años de registros mensuales (1995 - 2024)** de indicadores turísticos de todo el país.
2. Resolver inconsistencias históricas de unidades estadísticas (escalas de personas vs. miles de personas y normalización de porcentajes).
3. Almacenar los datos en una **Base de Datos Relacional SQLite** estructurada y optimizada para consultas analíticas.
4. Exportar tablas maestras en formato **CSV estándar** para su procesamiento directo en Python, SQL, R o herramientas BI.
5. Cuantificar el **Índice de Estacionalidad Base 100** y determinar de forma rigurosa los tres picos de **Temporada Alta** en México frente a los periodos de **Temporada Baja (Valle)**.

---

## 2. 🗄️ Arquitectura de la Base de Datos (`turismo_mexico_temporadas.db`)

La base de datos contiene cuatro tablas relacionales con granularidad mensual:

```
┌────────────────────────────────────────────────────────────────────────┐
│             BASE DE DATOS: turismo_mexico_temporadas.db                │
└────────────────────────────────────────────────────────────────────────┘
                                    │
    ┌───────────────────────────────┼───────────────────────────────┐
    ▼                               ▼                               ▼
[temporadas_mensuales_nacional] [estacionalidad_promedio_mensual] [afluencia_aeropuertos_mensual]
• anio (1995-2024)              • mes (1 - 12)                    • anio (2010-2024)
• mes (1 - 12)                  • nombre_mes                      • mes (1 - 12)
• fecha (YYYY-MM-01)            • ocupacion_hotelera_promedio     • aeropuerto (Cancún, CDMX,
• ocupacion_hotelera_pct        • indice_estacional_ocupacion       Los Cabos, Toluca, etc.)
• turistas_hoteles_total_miles    (Base 100)                      • entidad_federativa
• turistas_nacionales_miles     • tipo_temporada_anual            • tipo_destino (Playa, Urbano)
• turistas_extranjeros_miles    • turistas_nacionales_promedio    • pasajeros_llegada
• pasajeros_aereos_total        • turistas_extranjeros_promedio
• pasajeros_cruceros            • pasajeros_aereos_promedio
• clasificacion_temporada
```

### Descripción de las Tablas:

1. **`temporadas_mensuales_nacional` (360 registros):**  
   Serie de tiempo mensual histórica ininterrumpida de 1995 a 2024. Contiene ocupación hotelera en 70 centros del país, arribo de turistas a cuartos de hotel desglosados por nacionales y extranjeros, llegadas de vuelos y pasajeros a aeropuertos, cruceristas y gasto de divisas.
2. **`estacionalidad_promedio_mensual` (12 registros):**  
   Perfil estructural de los 12 meses del año calculado sobre la última década consolidada (excluyendo la anomalía atípica de confinamiento de 2020 para no sesgar la estacionalidad real). Incluye el **Índice Estacional Base 100** y la etiqueta de clasificación de temporada (*Alta*, *Media*, *Baja*).
3. **`afluencia_aeropuertos_mensual` (1,896 registros):**  
   Serie mensual 2010–2024 de pasajeros llegados a los 11 principales aeropuertos y nodos de conexión del país: *Cancún, CDMX AICM, Guadalajara, Monterrey, Tijuana, Puerto Vallarta, Los Cabos, Mérida, Oaxaca, Acapulco y Toluca*.
4. **`visitantes_inah_cultural_mensual` (180 registros):**  
   Registro mensual de visitas registradas en museos y zonas arqueológicas protegidas por el INAH.

---

## 3. 📊 Matriz de Estacionalidad y Clasificación de Temporadas en México

A partir del análisis cuantitativo de la base de datos, el comportamiento anual del turismo en México se distribuye de la siguiente manera:

| Mes | Nombre Mes | Ocupación Hotelera Promedio | Índice Estacional (Base 100) | Tipo de Temporada | Turistas en Hoteles (Miles) | Pasajeros Aéreos Promedio | Dinámica Turística Principal |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | Enero | 52.13% | 93.10 | **Temporada Baja** | 5,436.5 | 4,785,682 | Resaca post-fiestas; turismo internacional activo pero baja el doméstico. |
| **2** | Febrero | 57.10% | 101.98 | **Temporada Media** | 5,280.6 | 4,312,773 | Primer puente festivo nacional (Constitución) y turismo extranjero invernal. |
| **3** | **Marzo** | **59.20%** | **105.73** | **Temporada Alta (Peak)** | **6,425.2** | **5,139,406** | **Pico 1: Semana Santa / Spring Break y puente de Benito Juárez.** |
| **4** | **Abril** | **58.29%** | **104.10** | **Temporada Alta (Peak)** | **6,458.9** | **4,987,573** | **Pico 1 (cont.): Semana de Pascua y vacaciones escolares primaverales.** |
| **5** | Mayo | 54.77% | 97.82 | **Temporada Media** | 6,234.6 | 5,046,498 | Puentes de mayo (Día del Trabajo, Batalla de Puebla); actividad laboral plena. |
| **6** | Junio | 54.52% | 97.37 | **Temporada Media** | 5,945.4 | 5,133,810 | Cierre de ciclo escolar; valle previo a las vacaciones de verano. |
| **7** | **Julio** | **62.37%** | **111.39** | **Temporada Alta (Peak Máximo)**| **7,418.5** | **5,857,027** | **Pico 2: Temporada más alta del año en México por vacaciones de verano.** |
| **8** | Agosto | 56.33% | 100.60 | **Temporada Media-Alta**| 6,641.1 | 5,408,888 | Segunda mitad del verano; fuerte flujo de regreso escolar. |
| **9** | **Septiembre**| **48.33%** | **86.31** | **Temporada Baja (Valle Mínimo)**| **5,397.3** | **4,498,130** | **Mes de menor afluencia turística en México (temporada de lluvias y ciclones).** |
| **10**| Octubre | 52.70% | 94.12 | **Temporada Baja** | 6,021.6 | 5,033,016 | Recuperación gradual; turismo de congresos y convenciones. |
| **11**| **Noviembre** | **59.08%** | **105.51** | **Temporada Alta (Peak)** | **6,476.5** | **5,296,705** | **Pico 3: Día de Muertos, Festival del Globo, Buen Fin y puente de Revolución.**|
| **12**| **Diciembre** | **57.10%** | **101.98** | **Temporada Alta (Peak Aéreo)** | **6,820.7** | **5,887,677** | **Pico 3 (cont.): Fiestas decembrinas y máximo histórico en vuelos y cruceros.**|

---

## 4. 🔍 Los 3 Grandes Picos de Temporada Alta y Hallazgos Analíticos

### 1. Pico 1: Primavera / Semana Santa y Pascua (Marzo - Abril)
* **Ocupación promedio:** 58.7% - 59.2%.
* **Volumen:** Supera los 6.4 millones de turistas en hoteles por mes.
* **Característica:** Coincide con el periodo de *Spring Break* internacional y las vacaciones masivas del sistema educativo nacional (SEP). Los destinos de playa y pueblos mágicos cercanos a las grandes metrópolis experimentan saturación crítica.

### 2. Pico 2: Vacaciones de Verano (Julio - Agosto) — *El Máximo Nacional*
* **Ocupación promedio:** **62.37% en Julio** (Índice Estacional 111.39, el valor más alto del calendario).
* **Volumen:** **7.41 millones de turistas** y 5.85 millones de pasajeros aéreos.
* **Característica:** Es la temporada de mayor derrama económica familiar del turismo doméstico mexicano. Prácticamente todo el país presenta alta ocupación debido a la duración extendida del receso escolar.

### 3. Pico 3: Otoño-Invierno y Fin de Año (Noviembre - Diciembre)
* **Volumen:** Diciembre registra el récord anual en pasajeros de avión (**5.88 millones**) y cruceristas (**>700,000 pasajeros**).
* **Característica:** Concentra festividades de alto arraigo identitario (Día de Muertos en noviembre) y el retorno de la diáspora mexicana de EE.UU. junto con turistas extranjeros que huyen de las nevadas de Norteamérica hacia las costas mexicanas.

### 4. La Temporada Baja Estructural: El "Valle de Septiembre"
* **Septiembre registra apenas 48.33% de ocupación hotelera** y un índice estacional de **86.31** (13.7% por debajo del promedio anual).
* **Causas identificadas en los datos:** Inicio del ciclo escolar, gastos familiares de colegiaturas/útiles y pico histórico de lluvias y fenómenos meteorológicos en costas del Golfo y Pacífico.

---

## 5. ⚖️ Asimetría de Mercados: Turismo Nacional vs. Extranjero

Uno de los aportes más valiosos de la base de datos es la evidencia cuantitativa de que **el turismo nacional y el internacional tienen calendarios opuestos**:

```
                       ASIMETRÍA ESTACIONAL EN MÉXICO
                       
  (Llegadas a Hoteles)
         ▲
         │          ┌─────────┐   ◄─── TURISMO NACIONAL (Pico en JULIO: 5.80M)
         │         /           \
         │  ┌─────┘             └─────┐
         │ /                           \       ┌─────┐
         │/                             \_____/       \
         ├─────────────────────────────────────────────┤
         │\     ┌─────┐                         ┌─────/   ◄─── TURISMO EXTRANJERO (Pico en DIC-MAR: 1.76M)
         │ \___/       \_______________________/
         └─────────────────────────────────────────────►
           Ene Feb Mar Abr May Jun Jul Ago Sep Oct Nov Dic
```

* **Turistas Extranjeros:** Prefieren los meses fríos de Norteamérica y Europa (**Diciembre a Marzo**), concentrándose fuertemente en centros de sol y playa de Quintana Roo, Los Cabos y Puerto Vallarta.
* **Turistas Nacionales:** Se movilizan masivamente en periodos escolares (**Julio-Agosto y Semana Santa**), visitando tanto playas como ciudades coloniales, balnearios y destinos de naturaleza.

---

## 6. 📈 Gráficas Generadas en Alta Resolución

Los gráficos analíticos generados por el pipeline se encuentran en [`campana/kpis/`](../campana/kpis/):
1. **[`fig4_estacionalidad_temporadas_mexico.png`](../campana/kpis/fig4_estacionalidad_temporadas_mexico.png):**  
   Panel 2x2 que muestra:
   - *Subplot 1:* Ocupación hotelera mensual con barras clasificadas en semáforo (Rojo = Alta, Naranja = Media, Verde = Baja).
   - *Subplot 2:* Curvas comparativas de turistas nacionales vs. extranjeros evidenciando la asimetría de picos.
   - *Subplot 3:* Volumen mensual de pasajeros en aeropuertos del país (millones de personas).
   - *Subplot 4:* Pasajeros de cruceros marítimos (concentración extrema en invierno).
2. **[`fig5_heatmap_estacionalidad_mexico.png`](../campana/kpis/fig5_heatmap_estacionalidad_mexico.png):**  
   Mapa de calor mensual año por año (2014 a 2024) que confirma la consistencia histórica del ciclo estacional en México y la recuperación post-pandemia.
3. **[`fig6_temporadas_playa_vs_ciudades.png`](../campana/kpis/fig6_temporadas_playa_vs_ciudades.png):**  
   Comparativa de índices estacionales relativos (Base 100) entre aeropuertos de sol y playa (*Cancún, Los Cabos, Puerto Vallarta*) y metrópolis del interior (*CDMX, Guadalajara, Monterrey*).

---

## 7. 💻 Ejemplos de Consultas SQL Útiles

Puedes consultar la base de datos directamente con Python o con cualquier cliente de SQLite:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("datos/processed/turismo_mexico_temporadas.db")

# 1. Consultar los meses de Temporada Alta ordenados por índice estacional
query_temporadas = """
SELECT mes, nombre_mes, ocupacion_hotelera_promedio, indice_estacional_ocupacion_base100, tipo_temporada_anual
FROM estacionalidad_promedio_mensual
WHERE tipo_temporada_anual = 'Temporada Alta (Peak)'
ORDER BY indice_estacional_ocupacion_base100 DESC;
"""
print(pd.read_sql(query_temporadas, conn))

# 2. Consultar la afluencia en aeropuertos durante el pico de verano (Julio) en 2024
query_aeropuertos = """
SELECT aeropuerto, entidad_federativa, tipo_destino, pasajeros_llegada
FROM afluencia_aeropuertos_mensual
WHERE anio = 2024 AND mes = 7
ORDER BY pasajeros_llegada DESC;
"""
print(pd.read_sql(query_aeropuertos, conn))

conn.close()
```
