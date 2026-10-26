# Asignación de Roles y Plan de Trabajo para 3 Integrantes

**Proyecto Prototípico — 5to Semestre: Ciencias de Datos para Negocios**  
*Universidad Rosario Castellanos*  
* **Proyecto:** *Guardianes del Territorio: Turismo Sostenible y Exploración Gamificada*  
* **Corredor Piloto:** Tren Interurbano "El Insurgente" (Edomex - CDMX)  

---

## 👥 1. Perfiles y Distribución de Responsabilidades

Para equilibrar la carga de trabajo y asegurar que las **6 asignaturas (UCAs)** y los **entregables** queden cubiertos con excelencia, el equipo se organiza en tres roles complementarios:

```
┌─────────────────────────────────┐   ┌─────────────────────────────────┐   ┌─────────────────────────────────┐
│           INTEGRANTE 1          │   │           INTEGRANTE 2          │   │           INTEGRANTE 3          │
│   Data Engineering & ML Lead    │   │  Operations Research & Quants   │   │  Product & Growth/Marketing     │
├─────────────────────────────────┤   ├─────────────────────────────────┤   ├─────────────────────────────────┤
│• Big Data & Pipeline ETL        │   │• Minería de Datos & Clustering  │   │• Diseño UX/UI & Prototipo App   │
│• Modelos Predictivos (ML)       │   │• Modelos Estocásticos (Monte    │   │• Mercadotecnia Digital & Pauta  │
│• Chatbot IA "El Nahual Guía"    │   │  Carlo y Capacidad de Carga)    │   │• Alianzas Locales & Comercios   │
│• Arquitectura Offline-First     │   │• Optimización Matemática (IO)   │   │• Informe Técnico & Coloquio     │
│  (SQLite/PostGIS)               │   │• Análisis de Sensibilidad       │   │• Dashboard de KPIs de Impacto   │
└─────────────────────────────────┘   └─────────────────────────────────┘   └─────────────────────────────────┘
```

---

## 📅 2. Matriz de Actividades por Entrega y Fase

---

### 🚀 ENTREGA 1 (Semanas 1 a 5): Diagnóstico, Big Data, Minería y Wireframes

| Integrante | Rol Principal | Actividades Específicas a Realizar | Entregable Concreto |
| :--- | :--- | :--- | :--- |
| **Integrante 1** | *Data Engineering & ML* | • Configurar base de datos local y estructura de ingesta (`datos/raw/` y `datos/processed/`).<br>• Diseñar el diagrama de Arquitectura Big Data para eventos masivos de telemetría de jugadores.<br>• Implementar y documentar el pipeline de almacenamiento offline-first (SQLite para móviles sin señal). | Script de ingesta Big Data (`01_generador_ingesta_eventos.py`) + Capítulo de Arquitectura de Almacenamiento para el informe. |
| **Integrante 2** | *OR & Minería* | • Ejecutar la limpieza y análisis exploratorio (EDA) de los aforos de estaciones del Tren Insurgente.<br>• Calcular y formalizar matemáticamente el **Índice de Saturación Turística (IST)**.<br>• Elaborar el **Diccionario de Datos** oficial de estaciones, POIs y comercios.<br>• Generar gráficas de capacidad ociosa en fines de semana. | Notebook de Minería de Datos ejecutado (`01_algoritmo_rareza_inversa_eda.py`) + Documento del Diccionario de Datos. |
| **Integrante 3** | *Product & Marketing* | • Redactar el capítulo de Introducción, Justificación y Planteamiento del Problema (*overtourism* vs marginación).<br>• Diseñar los wireframes UX de las 4 pantallas clave del MVP (Radar, Misión POI, Carta Viva 2D y Wallet de Cupones).<br>• Definir el lore cultural de los 4 Guardianes y fichas de los 15 comercios afiliados piloto. | Kit de Wireframes (Figma o esquemas visuales) + Capítulo de Diagnóstico y Contexto del Territorio para el informe. |

---

### 🚀 ENTREGA 2 (Semanas 6 a 10): Modelos Predictivos, Simulación y Optimización

| Integrante | Rol Principal | Actividades Específicas a Realizar | Entregable Concreto |
| :--- | :--- | :--- | :--- |
| **Integrante 1** | *Data Engineering & ML* | • Entrenar y comparar modelos de Machine Learning (Random Forest, XGBoost) para predecir afluencia y demanda turística semanal.<br>• Programar el prototipo del **Chatbot IA ("El Nahual Guía")** con procesamiento de lenguaje natural (NLP) para generar pistas en rima y recomendaciones.<br>• Validar métricas predictivas ($R^2$, RMSE, MAE) evitando sobreajuste. | Notebook de Machine Learning (`03_machine_learning/`) + Código funcional del Chatbot + Capítulo técnico de ML. |
| **Integrante 2** | *OR & Minería* | • Diseñar y ejecutar la **Simulación Monte Carlo** (10,000 iteraciones) para modelar la variabilidad en la adopción de la app y evaluar el riesgo de saturar fondas/talleres comunitarios.<br>• Formular el modelo de **Investigación de Operaciones** (programación lineal/entera en Python con `PuLP`) para maximizar la derrama local respetando restricciones de presupuesto y aforo.<br>• Realizar análisis de sensibilidad y dualidad. | Notebook de Modelos Estocásticos (`04_modelos_estocasticos/`) + Notebook de Optimización Matemática (`05_optimizacion_io/`) + Capítulos técnicos de Estocásticos e IO. |
| **Integrante 3** | *Product & Marketing* | • Diseñar el **Módulo de Comercios Locales Sin Hardware**: flujo de canje por código OTP de 4 dígitos y QR dinámico.<br>• Construir los 4 **Buyer Personas** cuantificados con base en la segmentación de datos.<br>• Redactar la propuesta de valor y el sistema de incentivos comerciales de las Bendiciones. | Fichas técnicas de Buyer Personas + Especificación del Módulo de Comercios + Capítulo de Mercadotecnia y Estrategia Comercial. |

---

### 🚀 ENTREGA 3 (Semanas 11 a 13): Prototipo de App, Campaña y Tablero de KPIs

| Integrante | Rol Principal | Actividades Específicas a Realizar | Entregable Concreto |
| :--- | :--- | :--- | :--- |
| **Integrante 1** | *Data Engineering & ML* | • Integrar el prototipo funcional móvil o web interactivo (Flutter / React Native o Streamlit demo) conectando la lectura de QRs y el radar de ubicación.<br>• Configurar el enlace profundo (*Deeplinking*) hacia Google Maps para guiar al usuario a los POIs.<br>• Programar el prototipo ligero del visor de fotos históricas ("La Ventana del Tiempo"). | Prototipo interactivo funcional del MVP de la app + Repositorio con código fuente estructurado. |
| **Integrante 2** | *OR & Minería* | • Integrar los resultados de los modelos predictivos y de optimización en un pipeline de datos único.<br>• Calcular métricas ambientales: estimación de kilogramos de $CO_2$ evitados por usar el Tren Insurgente frente al automóvil particular.<br>• Apoyar la consolidación y pruebas de reproducibilidad de todo el código del proyecto. | Script de métricas ecológicas y económicas consolidadas + Pruebas unitarias de notebooks. |
| **Integrante 3** | *Product & Marketing* | • Diseñar los materiales de la campaña publicitaria gamificada: guiones para videos de TikTok/Reels y mockups de señalética en andenes de tren.<br>• Construir el **Dashboard de KPIs** de impacto (tasa de conversión, CAC estimado, derrama económica neta capturada por cooperativas).<br>• Ensamblar el **primer borrador completo del Informe Técnico** (30 a 40 páginas, integrando los aportes de los 3 integrantes). | Dossier de Campaña Publicitaria (piezas gráficas/copys) + Dashboard de KPIs + Borrador al 80% del Informe Técnico. |

---

### 🏆 ENTREGA FINAL Y COLOQUIO (Semanas 14 a 16): Consolidación y Defensa Oral

| Integrante | Tareas de Cierre del Informe | Rol en la Presentación del Coloquio (15 min) |
| :--- | :--- | :--- |
| **Integrante 1** | Pulir los capítulos de Big Data, Machine Learning, Chatbot y reproducibilidad del repositorio GitHub. | **Defensa Técnica (5 min):** Explica la arquitectura de datos, el algoritmo de rareza inversa, el modelo predictivo de afluencia y la demostración en vivo de la app. |
| **Integrante 2** | Pulir los capítulos de Minería de Datos, Simulación Monte Carlo de riesgos y Modelo de Optimización de Investigación de Operaciones. | **Defensa Cuantitativa y Matemática (5 min):** Explica cómo se cuantificó la incertidumbre, cómo la optimización matemática asigna recursos sin saturar a los pueblos y el impacto ambiental ($CO_2$). |
| **Integrante 3** | Revisión de estilo APA 7ma edición, formato final del documento PDF (30-40 pp) y ensamblado de las diapositivas ejecutivas. | **Defensa Estratégica y Comercial (5 min):** Abre con el planteamiento del problema, presenta la campaña publicitaria, los Buyer Personas, la derrama en comercios locales y cierra con conclusiones. |

---

## 🛠️ 3. Acuerdos de Trabajo y Buenas Prácticas del Equipo

1. **Control de Versiones en Git:**
   * Cada integrante trabaja en una rama propia (ej. `feature/mineria-datos`, `feature/wireframes`, `feature/big-data`) y se integran mediante Pull Requests a `main`.
2. **Reunión Semanal de Sincronización (Standup de 20 minutos):**
   * ¿Qué completé esta semana?
   * ¿Qué voy a realizar en la siguiente?
   * ¿Tengo algún bloqueo que requiera apoyo de mis compañeros?
3. **Mantenimiento del Repositorio:**
   * Todo script debe incluir comentarios y referencias a las fuentes oficiales (SICT, INEGI, DataTur).
   * Los notebooks deben ejecutarse de arriba a abajo sin errores (`Restart & Run All`).
