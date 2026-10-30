# Guardianes del Territorio: Turismo Sostenible y Exploración Gamificada

> **Aplicación móvil de turismo sostenible y exploración lúdica (*monster-collecting*) que descentraliza los flujos de visitantes en México mediante un sistema de rareza inversa y beneficios directos para la economía local.**

Proyecto integrador correspondiente al **Problema Prototípico de 5to Semestre** de la Licenciatura en Ciencias de Datos para Negocios de la **Universidad Rosario Castellanos**.

* **Autores:** Kevin Axel Acosta Ayala · Ivan Rafael Mena Fernández
* **Ciclo:** 2026-2

---

##  1. Visión del Producto y Mecánicas Clave

En México, el turismo masivo se concentra en unos pocos polos saturados provocando *overtourism*, alza de costos y daño ambiental, mientras que los municipios periféricos y pueblos con riqueza comunitaria no reciben derrama económica.

**Guardianes del Territorio** aborda este problema a través de un juego de exploración en el mundo real:
1. **Los Guardianes:** Espíritus protectores inspirados en alebrijes, fauna endémica, nahuales y artesanías de cada localidad.
2. **Mecánica de Desbloqueo Físico:** El viajero activa el radar geolocalizado en la zona, recorre de 1 a 3 Puntos de Interés (miradores, talleres artesanales, mercados) y valida su presencia física mediante GPS + escaneo de Códigos QR en sitio.
3. **Cartas Vivas 2D:** El Guardián despierta en una hermosa carta coleccionable 2D con microanimaciones fluidas (Lottie/Vectorial).
4. **Bendiciones Económicas:** Desbloquear al Guardián otorga un cupón de descuento digital para consumir en comercios locales afiliados (fondas, talleres de artesanos, ecoturismo).
5. **Sistema de Rareza Inversa:** 
   * Polos hiper-turísticos saturados albergan guardianes **Comunes** (con bajas recompensas).
   * Pueblos emergentes y turismo comunitario albergan guardianes **Raros, Épicos y Legendarios** (con los mayores descuentos y prestigio).
6. **Módulos de IA y Memoria Histórica:** 
   * **Chatbot "El Nahual Guía":** Asistente inteligente que da pistas en verso y responde dudas históricas y gastronómicas.
   * **Ventana del Tiempo:** Filtro de cámara ligero que sobrepone fotografías de archivo histórico para ver cómo lucía el lugar hace un siglo.

---

##  2. Arquitectura Técnica del MVP (Bajo Costo / Alto Impacto)

* **Enfoque Visual:** Cartas Vivas 2D con microanimaciones ligeras en Lottie / Rive (descartando 3D y AR compleja para la fase inicial).
* **Modo Offline-First:** Descarga de paquetes de guías locales y validación de logros en almacenamiento local (SQLite/Hive) para operar sin problemas en zonas rurales sin cobertura celular.
* **Integración con Google Maps:** Generación de enlaces directos (*Deeplinking*) para iniciar navegación peatonal hacia los Puntos de Interés.
* **Módulo de Comercio Local Sin Hardware:** Validación de cupones mediante códigos OTP de 4 dígitos o QR dinámico sin necesidad de terminales costosas para el locatario.

---

##  3. Articulación con las 6 Asignaturas (UCAs)

| Materia / UCA | Rol y Aplicación en "Guardianes del Territorio" |
| :--- | :--- |
| **1. Herramientas Big Data** | Ingesta masiva de eventos de juego (GPS, escaneo QR, canjes) y almacenamiento distribuido (PostgreSQL/PostGIS) junto con microdatos DENUE INEGI y aforos oficiales. |
| **2. Minería de Datos** | Detección de patrones temporales de afluencia (identificación de horarios valle) y clustering de municipios por potencial turístico desaprovechado. |
| **3. Machine Learning** | Modelo predictivo del **Índice de Saturación Turística (IST)** que calcula dinámicamente la rareza de los guardianes y motor de recomendación de rutas personalizadas. |
| **4. Modelos Estocásticos** | Simulación **Monte Carlo** para evaluar el riesgo de saturar la capacidad de carga comunitaria de las fondas y talleres locales por el éxito de las bendiciones. |
| **5. Investigación de Operaciones** | Optimización matemática de la asignación del presupuesto de la campaña publicitaria y distribución óptima de cupones para maximizar la derrama local. |
| **6. Mercadotecnia Digital** | Diseño de la campaña publicitaria gamificada, modelado de Buyer Personas, pauta digital (TikTok/Instagram) y dashboard de KPIs (impacto económico y $CO_2$ evitado). |

---

##  4. Estructura del Repositorio

```text
Tourism/
├── README.md                      # Presentación general del proyecto y arquitectura
├── PLAN_DE_ACCION.md              # Cronograma de 16 semanas, backlog y 3 entregas
├── problema prototípico 5to...pdf # Documento oficial de la Universidad
├── docs/                          # Documentación conceptual y técnica
│   ├── PIVOT_APP_GAMIFICADA.md    # Especificación completa del MVP y backlog
│   ├── CONCEPTO_NODOS_VIVOS.md    # Fundamento conceptual y diagnóstico previo
│   └── PROPUESTA_ESTADO_Y_DATOS.md# Análisis comparativo de corredores territoriales
├── datos/                         # Conjuntos de datos y diccionarios
│   ├── raw/                       # Datasets crudos (INEGI, SECTUR, DataTur)
│   └── processed/                 # Datasets limpios (ej. dataset_estaciones_el_insurgente.csv)
├── notebooks/                     # Jupyter Notebooks organizados por UCA
│   ├── 01_big_data_etl/           # Pipelines de ingesta y carga
│   ├── 02_mineria_datos/          # Patrones temporales y clustering
│   ├── 03_machine_learning/       # Algoritmo de rareza inversa y recomendador
│   ├── 04_modelos_estocasticos/   # Simulaciones Monte Carlo de capacidad de carga
│   └── 05_optimizacion_io/        # Optimización matemática de cupones y pauta
├── campana/                       # Recursos de mercadotecnia digital
│   ├── buyer_personas/            # Fichas técnicas de audiencia
│   ├── piezas_publicitarias/      # Guiones para TikTok, copys y diseños de cartas 2D
│   └── kpis/                      # Métricas de retención, canjes y huella ecológica
└── modelos/                       # Modelos entrenados y serializados (.pkl, .joblib)
```

---

##  5. Plan de Entregas Parciales

* **Entrega 1 (Semana 5):** Delimitación del Corredor Piloto, catálogo inicial de Guardianes y comercios, arquitectura Big Data, bases procesadas y wireframes UX.
* **Entrega 2 (Semana 10):** Algoritmo de Machine Learning de Rareza Inversa, prototipo del Chatbot IA, simulaciones estocásticas Monte Carlo y modelo de optimización de Investigación de Operaciones.
* **Entrega 3 (Semana 13):** Prototipo funcional del MVP de la app (modo offline-first), campaña de mercadotecnia digital gamificada y borrador avanzado del Informe Técnico.
* **Entrega Final y Coloquio (Semana 15 - 16):** Informe Técnico definitivo (30-40 páginas), repositorio completo y defensa oral en el Coloquio de la Licenciatura (15 min).
