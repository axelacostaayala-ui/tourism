# Plan de Acción: Guardianes del Territorio (App de Turismo Sostenible y Exploración Gamificada)

**Nuevo Plan de Acción, Backlog de Producto y Roadmap de Desarrollo**  
*Proyecto Prototípico de 5to Semestre — Licenciatura en Ciencias de Datos para Negocios (Universidad Rosario Castellanos)*  
* **Autores:** Kevin Axel Acosta Ayala · Ivan Rafael Mena Fernández  
* **Evidencia Integradora:** Campaña publicitaria inteligente y sistema de analítica de datos para la redistribución sustentable de los flujos turísticos.

---

## 🎯 1. Visión Estratégica del Pivot

Descentralizar el turismo en México mediante una **aplicación móvil de exploración gamificada (*monster-collecting* estilo Pokémon Go)** basada en **Cartas Vivas 2D**, donde los destinos emergentes albergan a los **Guardianes más raros y valiosos (Sistema de Rareza Inversa)**, recompensando a los viajeros con **Bendiciones (descuentos y beneficios económicos reales)** canjeables en una red de comercios locales y cooperativas comunitarias.

La aplicación y su campaña publicitaria están completamente soportadas por la analítica de datos de las 6 asignaturas del semestre.

---

## 📦 2. Alineación con las 3 Entregas Parciales y la Entrega Final

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CRONOGRAMA DE ENTREGAS                          │
└────────────────────────────────────────────────────────────────────────┘

[Semanas 1 - 5]   ──► ENTREGA 1: Corredor Piloto, Arquitectura Big Data, 
                                 Wireframes de la App y Minería de Datos.
[Semanas 6 - 10]  ──► ENTREGA 2: Algoritmo de Rareza Inversa (ML), Chatbot IA, 
                                 Simulación Monte Carlo y Optimización (IO).
[Semanas 11 - 13] ──► ENTREGA 3: MVP Funcional de la App (Offline-first), 
                                 Campaña de Difusión y Módulo de Comercios.
[Semanas 14 - 16] ──► ENTREGA FINAL: Informe Técnico (30-40 pp), Repositorio 
                                     completo y Defensa en Coloquio (15 min).
```

---

## 📅 3. Fases y Actividades Detalladas

### 📍 FASE 1: Corredor Piloto, Big Data y Wireframes (Semanas 1 a 5)
* **Objetivo Académico y de Producto:** Delimitar el clúster regional de prueba, diseñar la arquitectura de datos masivos y definir la experiencia de usuario del MVP.
* **Actividades clave:**
  - [x] Documentar el pivot de producto y especificación del juego (`docs/PIVOT_APP_GAMIFICADA.md`).
  - [ ] **Delimitación del Corredor Piloto:** Formalizar el clúster piloto de 3 a 4 municipios contiguos (Corredor *El Insurgente / Valle de Toluca*: Zinacantepec, Toluca Centro, Metepec, Lerma; o Corredor *Sierra Norte de Puebla*).
  - [ ] **Catálogo Piloto:** Estructurar los 4 Guardianes iniciales (*Xinán*, *Barrotépetl*, *Acatl-Tule*, *Mosco*) y el directorio inicial de 15 comercios locales afiliados.
  - [ ] **Arquitectura Big Data (UCA Herramientas de Almacenamiento):**
    - Pipeline de ingesta para telemetría de jugadores (GPS, escaneo de QRs, canjes) y datos oficiales (DataTur, aforos de tren/transporte masivo, DENUE de INEGI).
    - Esquema de base de datos relacional/NoSQL con soporte geoespacial (PostgreSQL + PostGIS).
    - Solución técnica al incidente crítico de almacenamiento de grandes volúmenes.
  - [ ] **Minería de Datos (UCA Minería de Datos):**
    - Análisis exploratorio de datos de turismo y afluencia por municipio.
    - Detección de patrones temporales: identificación de horas valle y temporadas bajas en destinos emergentes.
    - Diccionario de Datos oficial.
  - [ ] **Diseño UX / Wireframes de la App:**
    - Flujo 1: Pantalla de Mapa / Radar con geolocalización nativa.
    - Flujo 2: Vista de Misión territorial y validación de Puntos de Interés (POI).
    - Flujo 3: Carta Viva 2D con microanimaciones (Lottie/SVG).
    - Flujo 4: Bóveda / Álbum de Colección y Wallet de Bendiciones.
* **🚀 HITO 1: ENTREGA 1 (Semana 5)**
  * *Entregables:* Documento de diagnóstico y especificación de producto, arquitectura Big Data, bases de datos procesadas (`datos/processed`), diccionario de datos, notebook de minería y kit de wireframes UX.

---

### 📍 FASE 2: Modelos Predictivos, Chatbot IA y Optimización (Semanas 6 a 10)
* **Objetivo Académico y de Producto:** Desarrollar los algoritmos matemáticos y de machine learning que gobiernan la rareza inversa, el motor de recomendación, el asistente inteligente y el módulo de comercio local.
* **Actividades clave:**
  - [ ] **Machine Learning (UCA Aprendizaje de Máquina):**
    - Modelo predictivo para calcular el **Índice de Saturación Turística (IST)** en tiempo real/semanal.
    - Algoritmo de asignación dinámica de **Rareza Inversa** a los Guardianes en función del IST predicho.
    - Motor de recomendación de rutas personalizadas según las preferencias del jugador.
  - [ ] **Módulo de Inteligencia Artificial (Chatbot "El Nahual Guía"):**
    - Desarrollo del prototipo de chatbot conversacional con NLP para brindar pistas gamificadas en rima y recomendaciones culturales y gastronómicas.
  - [ ] **Modelos Estocásticos (UCA Modelos Estocásticos):**
    - Simulación **Monte Carlo** de la afluencia de jugadores hacia las comunidades receptoras.
    - Evaluación estocástica del riesgo de sobresaturar fondas y talleres comunitarios pequeños, calculando intervalos de confianza al 95%.
  - [ ] **Investigación de Operaciones (UCA Investigación de Operaciones):**
    - Formulación matemática del problema de optimización:
      - *Función objetivo:* Maximizar la derrama económica comunitaria y el número de canjes de cupones.
      - *Restricciones:* Presupuesto publicitario de la campaña, capacidad física máxima de los comercios y cotas de equidad territorial entre municipios.
    - Resolución computacional en Python (`PuLP` o `SciPy`) y análisis de sensibilidad.
  - [ ] **Módulo de Comercio Local (Sin Hardware):**
    - Mecanismo de validación por código OTP de 4 dígitos y QR dinámico de un solo uso.
    - Prototipo de la interfaz web ultraligera (PWA) para el comerciante local.
* **🚀 HITO 2: ENTREGA 2 (Semana 10)**
  * *Entregables:* Notebooks ejecutables de ML con evaluación de modelos ($R^2$, RMSE), script del Chatbot, simulaciones Monte Carlo de capacidad de carga, formulación y solución matemática de IO, y especificación funcional del módulo de comercios.

---

### 📍 FASE 3: MVP Funcional, Campaña Publicitaria y Validación (Semanas 11 a 13)
* **Objetivo Académico y de Producto:** Construir el prototipo funcional de la aplicación (modo offline-first), diseñar la campaña publicitaria inteligente y medir indicadores.
* **Actividades clave:**
  - [ ] **Desarrollo del MVP Móvil (Flutter / React Native):**
    - Implementación del modo *offline-first* (almacenamiento local SQLite/Hive).
    - Integración de Cartas Vivas 2D animadas con Lottie.
    - Lógica de geofencing (GPS) y lector de códigos QR físicos.
    - Integración de enlace directo con Google Maps (*Deeplinking* para iniciar caminata a POIs).
    - Prototipo del visor histórico de cámara ("La Ventana del Tiempo" con filtro sobrepuesto).
  - [ ] **Mercadotecnia Digital (UCA Mercadotecnia Digital):**
    - Estrategia integral de la campaña publicitaria gamificada: *"Despierta a los Guardianes: Redescubre México desde las Vías"*.
    - Perfilado cuantitativo de los **Buyer Personas** (Familias trabajadoras, Mochileros/Jóvenes, Adultos mayores, Turistas culturales).
    - Materiales creativos y pauta digital: videos cortos para TikTok / Instagram Reels y señalética física con QR en andenes de transporte y comercios.
    - Tablero de control (Dashboard) con KPIs: Tasa de conversión, coste de adquisición (CAC), derrama económica en cooperativas y kilogramos de $CO_2$ evitados por viajar en transporte público masivo.
  - [ ] **Borrador del Informe Técnico:** Consolidación de los primeros 18 apartados de la rúbrica oficial.
* **🚀 HITO 3: ENTREGA 3 (Semana 13)**
  * *Entregables:* Código fuente del MVP de la app en GitHub, dossier completo de la campaña publicitaria y piezas creativas, dashboard de KPIs y borrador avanzado del Informe Técnico (80%).

---

### 📍 FASE 4: Consolidación, Informe Técnico y Coloquio (Semanas 14 a 16)
* **Objetivo Académico y de Producto:** Cierre del informe de 30-40 páginas, auditoría del repositorio y preparación de la defensa oral.
* **Actividades clave:**
  - [ ] Redacción final del **Informe Técnico** (30 a 40 páginas, estructurado estrictamente según los 23 apartados oficiales de la Universidad Rosario Castellanos).
  - [ ] Congelamiento y documentación del repositorio de GitHub (código comentado, `requirements.txt`, instrucciones de instalación y datos reproducibles).
  - [ ] **Preparación para el Coloquio:**
    - Presentación visual ejecutiva (máximo 15 minutos).
    - Demostración en vivo de la aplicación móvil (despertar de un Guardián 2D y canje de cupón).
    - Argumentación técnica interdisciplinaria: demostrar cómo los datos, modelos predictivos, simulaciones y optimizaciones sustentan cada decisión de la campaña y del juego.
    - Ensayo de preguntas del sínodo académico.
* **🏆 ENTREGA FINAL Y COLOQUIO (Semanas 15 - 16)**
  * *Entregables Definitivos:* Informe Técnico formal (PDF 30-40 pp), Campaña Publicitaria integral, Repositorio de Productos Técnicos y Defensa oral en el Coloquio.

---

## 🗺️ 4. Roadmap Futuro (Fase 2 - Post-Lanzamiento y Tracción)

Una vez probado y validado el MVP en el corredor piloto:
1. **Cámara con Realidad Aumentada (AR interactiva):** Proyección del Guardián 3D en el entorno físico mediante ARCore / ARKit para tomarse fotos con él.
2. **Filtros Sociales:** Filtros interactivos para TikTok e Instagram con los Guardianes desbloqueados.
3. **Expansión de Corredores Nacionales:** Integración de nuevos clústeres (Ruta Maya, Pueblos Mágicos de Hidalgo, Corredor de Michoacán).
4. **Torneos y Eventos Estacionales:** Eventos de tiempo limitado para festivales tradicionales (Día de Muertos, Feria del Alfeñique, Semana Santa).
