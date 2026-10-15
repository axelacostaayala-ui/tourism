# Plan de Acción: Nodos Vivos - Utopías Turísticas y Movilidad Social Conectada

**Proyecto Prototípico Integrador - 5to Semestre**  
*Licenciatura en Ciencias de Datos para Negocios — Universidad Rosario Castellanos*  
* **Autores:** Kevin Axel Acosta Ayala · Ivan Rafael Mena Fernández  
* **Evidencia Integradora:** Campaña publicitaria inteligente para la promoción y redistribución sustentable de los flujos turísticos.

---

## 🎯 1. Visión y Objetivos del Proyecto

Diseñar una campaña publicitaria inteligente y un sistema analítico de toma de decisiones para promover **Nodos Vivos: Utopías Turísticas articuladas a redes de transporte masivo** (teleféricos urbanos como Cablebús/Mexicable y trenes de pasajeros). 

El modelo busca democratizar el acceso al turismo de fin de semana para familias trabajadoras y jóvenes, conectando a comunidades marginadas con la derrama económica directa mediante cooperativas vecinales de hospedaje, cultura y gastronomía, mitigando el *overtourism* en enclaves consolidados y reduciendo la huella de carbono a través de la movilidad eléctrica masiva.

---

## 📦 2. Estructura de las 3 Entregas Parciales y la Entrega Final

El plan de trabajo está diseñado para cumplir puntualmente con las **3 entregas previas** y la **entrega final + coloquio**:

```
[Semana 1 - 5]   ──►  ENTREGA 1: Diagnóstico Territorial, Arquitectura Big Data y Minería
[Semana 6 - 10]  ──►  ENTREGA 2: Modelos Predictivos (ML), Estocásticos y Optimización (IO)
[Semana 11 - 13] ──►  ENTREGA 3: Estrategia de Mercadotecnia Digital, Campaña y Validación
[Semana 14 - 16] ──►  ENTREGA FINAL: Informe Técnico (30-40 pp), Repositorio y Coloquio (15 min)
```

---

## 📅 3. Cronograma Detallado y Actividades por Fase

### 📍 FASE 1: Delimitación Territorial, Fuentes y Arquitectura Big Data (Semanas 1 a 3)
* **Materias involucradas:** Herramientas para el Almacenamiento de Grandes Volúmenes de Datos.
* **Actividades clave:**
  - [x] Documentar el concepto integral *Nodos Vivos* en el repositorio (`docs/CONCEPTO_NODOS_VIVOS.md`).
  - [ ] Selección y justificación del Estado / Entorno Territorial (CDMX / Edomex / Corredor Ferroviario - ver `docs/PROPUESTA_ESTADO_Y_DATOS.md`).
  - [ ] Descarga e ingesta de datos de aforos por estación (ADIP / Cablebús / Metro / SICT) y comercios locales (DENUE INEGI).
  - [ ] Diseño conceptual y lógico de la **Arquitectura Big Data**:
    - Capa de ingesta (Batch y Streaming de datos de torniquetes y redes).
    - Capa de almacenamiento escalable (Data Lake / Data Lakehouse particionado por estación y fecha).
    - Solución al incidente crítico: "¿Qué pasa cuando los datos de movilidad y turismo no caben en una sola computadora?".
* **Entregable de la fase:** Esquema de arquitectura Big Data y scripts de descarga de datos.

---

### 📍 FASE 2: Minería de Datos y Descubrimiento de Patrones (Semanas 4 y 5)
* **Materias involucradas:** Minería de Datos, Herramientas de Almacenamiento.
* **Actividades clave:**
  - [ ] Limpieza, normalización y tratamiento de valores atípicos en los aforos de estaciones.
  - [ ] Creación formal del **Diccionario de Datos** de las variables de movilidad, económicas y comunitarias.
  - [ ] Identificación de patrones de afluencia temporal: detección de horas y días valle (fines de semana) con capacidad ociosa para recibir visitantes en estaciones periféricas.
  - [ ] Minería de reglas de asociación (*Apriori* / *FP-Growth*): correlación entre amenidades barriales (mercados, áreas verdes, talleres) y atracción de perfiles de visitantes.
  - [ ] Análisis de sentimiento en redes sociales y búsquedas web sobre los barrios y sistemas de transporte.

---

### 🚀 HITO 1: ENTREGA 1 (Semana 5)
* **Productos a entregar:**
  1. Documento de Diagnóstico y Planteamiento del Problema enfocado en *Nodos Vivos*.
  2. Diagrama y justificación técnica de la Arquitectura de Big Data.
  3. Bases de datos procesadas (`datos/`) y Diccionario de Datos oficial.
  4. Notebook reproducible de Minería de Datos con visualizaciones de patrones temporales y espaciales.

---

### 📍 FASE 3: Modelado Predictivo con Machine Learning (Semanas 6 a 8)
* **Materias involucradas:** Aprendizaje de Máquina.
* **Actividades clave:**
  - [ ] Selección y feature engineering: variables de calendario, estacionalidad, clima, eventos comunitarios y afluencia histórica.
  - [ ] Entrenamiento de modelos de regresión y series de tiempo (Random Forest, XGBoost, Prophet/ARIMA) para predecir afluencia por estación y fecha.
  - [ ] Algoritmo de clustering (K-Means / DBSCAN) para clasificar y rankear estaciones según su potencial de conversión a *Nodo Vivo*.
  - [ ] Evaluación técnica y ética: métricas ($R^2$, RMSE, MAE) y mitigación de sesgos algorítmicos para no invisibilizar comunidades emergentes.

---

### 📍 FASE 4: Incertidumbre Estocástica y Optimización Matemática (Semanas 9 y 10)
* **Materias involucradas:** Modelos Estocásticos para la Toma de Decisiones, Investigación de Operaciones.
* **Actividades clave:**
  - [ ] **Modelos Estocásticos (Incidente Crítico):**
    - Simulación **Monte Carlo** para evaluar escenarios de adopción de la campaña (pesimista, moderado, optimista).
    - Cálculo del riesgo de rebasar la capacidad de carga comunitaria (sobresaturación en albergues vecinales o transporte).
    - Intervalos de confianza al 90% y 95% para la afluencia esperada.
  - [ ] **Investigación de Operaciones:**
    - Formulación matemática del problema de optimización:
      - **Función Objetivo:** Maximizar la derrama económica local y el impacto de la campaña.
      - **Restricciones:** Presupuesto publicitario total, capacidad máxima de carga por estación/Utopía, cotas de equidad territorial entre nodos.
    - Implementación y resolución computacional en Python (`PuLP` / `SciPy.optimize`).
    - Análisis de sensibilidad y precios sombra de las restricciones.

---

### 🚀 HITO 2: ENTREGA 2 (Semana 10)
* **Productos a entregar:**
  1. Notebooks de Machine Learning con modelos predictivos y comparativa de métricas.
  2. Notebook de Modelos Estocásticos con simulaciones Monte Carlo y curvas de riesgo.
  3. Formulación matemática formal, código y reporte de resultados de Investigación de Operaciones.
  4. Capítulo técnico de integración de modelos predictivos y prescriptivos.

---

### 📍 FASE 5: Estrategia de Mercadotecnia Digital y Campaña Publicitaria (Semanas 11 a 13)
* **Materias involucradas:** Mercadotecnia Digital, Integración Interdisciplinaria.
* **Actividades clave:**
  - [ ] Caracterización cuantitativa de los **4 Buyer Personas** sustentada en los clusters obtenidos:
    - *Familias trabajadoras*, *Jóvenes y mochileros*, *Adultos mayores*, *Viajeros internacionales*.
  - [ ] Desarrollo de la campaña: **"Pueblea en Cablebús / Tren: Redescubre tu Ciudad en las Alturas"**:
    - Definición de branding, identidad visual, eslogan y propuesta de valor.
    - Diseño de mockups y piezas publicitarias para TikTok, Instagram Reels y módulos físicos en CETRAMs.
    - Estructura del **Pase Integrado Multimodal** (Transporte + Utopía + Descuentos en Mercado de Sabores).
  - [ ] Asignación de pauta publicitaria basada estrictamente en la solución óptima de Investigación de Operaciones.
  - [ ] Matriz de KPIs e indicadores de desempeño: alcance, tasa de interacción, afluencia generada por nodo, derrama económica capturada por cooperativas y emisiones de $CO_2$ evitadas.

---

### 🚀 HITO 3: ENTREGA 3 (Semana 13)
* **Productos a entregar:**
  1. Dossier completo de la Campaña Publicitaria Inteligente (*branding*, piezas, canales, pauta).
  2. Fichas técnicas de los Buyer Personas y mapa de experiencia del usuario (Customer Journey).
  3. Cuadro de mando / Dashboard de indicadores (KPIs comerciales, comunitarios y ambientales).
  4. Primer borrador consolidado del Informe Técnico (80% de avance).

---

### 📍 FASE 6: Consolidación, Informe Técnico y Coloquio (Semanas 14 a 16)
* **Materias involucradas:** Articulación integral de las 6 UCAs.
* **Actividades clave:**
  - [ ] Edición final del **Informe Técnico** (extensión sugerida: 30 a 40 páginas, cumpliendo los 23 apartados oficiales de la rúbrica).
  - [ ] Limpieza, documentación y congelamiento del código en el repositorio GitHub (README interactivo, requerimientos `requirements.txt`).
  - [ ] Diseño de la presentación ejecutiva para el **Coloquio de la Licenciatura**:
    - Máximo 15 minutos de exposición.
    - Guión de defensa técnica que evidencie cómo los datos alimentan la campaña publicitaria sin tratar las materias como islas separadas.
  - [ ] Ensayos cronometrados de la exposición en equipo y simulación de preguntas del sínodo.

---

### 🏆 ENTREGA FINAL Y COLOQUIO (Semanas 15 - 16)
* **Entregables:**
  1. **Informe Técnico Final** (PDF formal 30-40 páginas).
  2. **Campaña Publicitaria Integral** (carpeta digital con materiales gráficos, audiovisuales y estrategia).
  3. **Repositorio de Productos Técnicos** (datos limpios, notebooks, modelos, simulaciones).
  4. **Defensa en el Coloquio** (15 minutos de presentación oral y sesión de preguntas).

---

## 🛠️ Resumen de Herramientas Tecnológicas

* **Lenguaje:** Python 3.10+
* **Big Data & Procesamiento:** Pandas, PySpark / Polars, DuckDB, SQLAlchemy.
* **Minería y Machine Learning:** Scikit-Learn, MLxtend (Apriori), XGBoost, LightGBM, Statsmodels.
* **Modelos Estocásticos y Optimización:** NumPy, SciPy, PuLP, SimPy.
* **Visualización y Geoespacial:** Matplotlib, Seaborn, Folium, GeoPandas, Plotly.
* **Control de Versiones y Documentación:** Git, GitHub, Markdown, LaTeX.
