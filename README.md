# Nodos Vivos: Utopías Turísticas y Movilidad Social Conectada

> **Modelo integral de turismo accesible y comunitario articulado a redes de transporte masivo en desarrollo.**

Proyecto integrador correspondiente al **Problema Prototípico de 5to Semestre** de la Licenciatura en Ciencias de Datos para Negocios de la **Universidad Rosario Castellanos**.

* **Autores:** Kevin Axel Acosta Ayala · Ivan Rafael Mena Fernández
* **Fecha:** Septiembre - Octubre 2026

---

## 📖 Resumen Ejecutivo

En México, el turismo tradicional se concentra en enclaves consolidados y de alto costo, generando saturación ambiental (*overtourism*) y excluyendo a familias trabajadoras del acceso al descanso digno, mientras comunidades periféricas y barriales con alto valor cultural permanecen marginadas de la derrama económica.

**Nodos Vivos** es una propuesta basada en Ciencia de Datos que aprovecha la expansión gubernamental de **sistemas de transporte público masivo y eléctrico** (teleféricos urbanos como Cablebús y Mexicable, y trenes de pasajeros) para convertir las estaciones periféricas en **destinos culturales y comunitarios planificados**.

Cada estación nodal integra tres pilares:
1. 🏡 **Hospedaje Comunitario Accesible:** Albergues y hospedajes vecinales cooperativos de bajo costo.
2. 🎭 **Espacio Utopía:** Infraestructura pública abierta para talleres artísticos, foros culturales al aire libre y deporte.
3. 🌽 **Mercado de Sabores y Oficios:** Puntos de venta directa para cocineras tradicionales y artesanos sin intermediarios.

Todo esto articulado mediante un **Pase Integrado** y la campaña publicitaria inteligente **"Pueblea en Cablebús / Tren"**.

---

## 🧠 Articulación con las 6 Asignaturas (UCAs)

El proyecto demuestra una cadena de valor analítica integral donde cada disciplina alimenta a la siguiente:

```
[Herramientas Big Data] 
       ▼ (Aforos masivos, microdatos comerciales DENUE)
[Minería de Datos] 
       ▼ (Patrones temporales en horas valle, reglas de asociación, sentimiento)
[Aprendizaje de Máquina] 
       ▼ (Predicción de afluencia, recomendador de rutas y clustering de nodos)
[Modelos Estocásticos] 
       ▼ (Simulación Monte Carlo de riesgos y capacidad de carga comunitaria)
[Investigación de Operaciones] 
       ▼ (Optimización matemática del presupuesto y balanceo de flujos)
[Mercadotecnia Digital] 
       ► Campaña "Pueblea en Cablebús/Tren", Buyer Personas y KPIs de impacto
```

1. **Herramientas para el Almacenamiento de Grandes Volúmenes de Datos:** Arquitectura escalable de ingesta y almacenamiento distribuido para registros de validación en torniquetes, aforos y datos geoespaciales.
2. **Minería de Datos:** Identificación de patrones de viaje en fines de semana, capacidad ociosa en estaciones y correlación de atractivos barriales.
3. **Aprendizaje de Máquina:** Modelos predictivos de demanda turística y algoritmos de recomendación de rutas sustentables.
4. **Modelos Estocásticos para la Toma de Decisiones:** Simulación Monte Carlo ante variabilidad de demanda y modelado del riesgo de saturación comunitaria.
5. **Investigación de Operaciones:** Modelo de programación lineal/entera para la asignación óptima del presupuesto publicitario maximizando el beneficio comunitario bajo restricciones de aforo.
6. **Mercadotecnia Digital:** Diseño integral de la campaña *"Pueblea en Cablebús/Tren"*, segmentación cuantitativa de Buyer Personas, pase multimodal y monitoreo de impacto socioambiental.

---

## 🗂️ Estructura del Repositorio

```text
Tourism/
├── README.md                      # Presentación general del proyecto
├── PLAN_DE_ACCION.md              # Cronograma de 16 semanas, fases y 3 entregas
├── problema prototípico 5to...pdf # Documento oficial de la Universidad
├── docs/                          # Documentación conceptual y técnica
│   ├── CONCEPTO_NODOS_VIVOS.md    # Propuesta conceptual y diagnósticos
│   └── PROPUESTA_ESTADO_Y_DATOS.md# Análisis comparativo de estados y fuentes
├── datos/                         # Conjuntos de datos y diccionarios
│   ├── raw/                       # Datos originales descargados (DataTur, ADIP, INEGI)
│   └── processed/                 # Datos limpios y procesados
├── notebooks/                     # Jupyter Notebooks organizados por materia
│   ├── 01_big_data_etl/           # Pipelines de ingesta y transformación
│   ├── 02_mineria_datos/          # EDA, reglas de asociación y series de tiempo
│   ├── 03_machine_learning/       # Modelos predictivos y clustering
│   ├── 04_modelos_estocasticos/   # Simulaciones Monte Carlo de capacidad
│   └── 05_optimizacion_io/        # Modelos matemáticos de asignación de presupuesto
├── campana/                       # Recursos de mercadotecnia digital
│   ├── buyer_personas/            # Perfiles y customer journeys
│   ├── piezas_publicitarias/      # Mockups, copys y diseños para TikTok/Instagram
│   └── kpis/                      # Tableros e indicadores de impacto
└── modelos/                       # Modelos entrenados y serializados (.pkl, .joblib)
```

---

## 📦 Plan de Entregas Parciales

* **Entrega 1 (Semana 5):** Diagnóstico territorial, arquitectura Big Data, bases de datos limpias y minería de patrones de movilidad.
* **Entrega 2 (Semana 10):** Modelos de Machine Learning predictivos, simulaciones estocásticas Monte Carlo y modelo de optimización matemática de asignación de recursos.
* **Entrega 3 (Semana 13):** Campaña publicitaria *"Pueblea en Cablebús/Tren"*, Buyer Personas cuantitativos, plan de medios y borrador del Informe Técnico.
* **Entrega Final y Coloquio (Semana 15 - 16):** Informe Técnico definitivo (30-40 páginas), repositorio completo con código reproducible y defensa oral en el Coloquio (15 min).

Para consultar el desglose semanal detallado, revisa [PLAN_DE_ACCION.md](PLAN_DE_ACCION.md).
