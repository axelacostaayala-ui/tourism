# Plan de Acción: Mexamonsters (App de Turismo Sostenible y Exploración Gamificada)

**Plan de Acción, Backlog de Producto y Roadmap de Desarrollo**  
*Proyecto Prototípico de 5to Semestre — Licenciatura en Ciencias de Datos para Negocios (Universidad Rosario Castellanos)*  
* **Equipo de Alumnos:**
  * **Miembro 1:** Hernández Monroy Diana Victoria (*Product & Growth / Marketing Lead*)
  * **Miembro 2:** Acosta Ayala Kevin Axel (*Data Engineering & ML Lead*)
  * **Miembro 3:** Carrasco Sánchez Jessica Daniela (*Operations Research & Quants Lead*)
* **Docente Asesor:** Rafael Mena
* **Grupo:** 501  
* **Evidencia Integradora:** Campaña publicitaria inteligente, Estudio de Mercado y sistema de analítica de datos para la redistribución sustentable de los flujos turísticos.

---

## 🎯 1. Visión Estratégica del Proyecto

Descentralizar el turismo en México mediante una **aplicación móvil de exploración gamificada (*monster-collecting* estilo Pokémon Go)** basada en **Cartas Vivas 2D**, donde los destinos emergentes albergan a los **Mexamonsters más raros y valiosos (Sistema de Rareza Inversa)**, recompensando a los viajeros con **Bendiciones (descuentos y beneficios económicos reales)** canjeables en una red de comercios locales y cooperativas comunitarias.

La aplicación y su campaña publicitaria están completamente soportadas por la analítica de datos de las 6 asignaturas del semestre.

---

## 🗓️ 2. Alineación con las 3 Entregas Parciales y la Entrega Final

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CRONOGRAMA DE ENTREGAS                          │
└────────────────────────────────────────────────────────────────────────┘

[Semanas 1 - 5]   ──► ENTREGA 1: Corredor Piloto, Arquitectura Big Data, 
                                 Wireframes de la App y Minería de Datos.
[Semanas 6 - 10]  ──► ENTREGA 2: Algoritmo de Rareza Inversa (ML), Chatbot IA, 
                                 Simulación Monte Carlo y Optimización (IO).
[Semanas 11 - 13] ──► ENTREGA 3: MVP Funcional de la App (Offline-first), 
                                 Estudio de Mercado, Campaña de Difusión y Comercios.
[Semanas 14 - 16] ──► ENTREGA FINAL: Informe Técnico (30-40 pp), Repositorio 
                                     completo y Defensa en Coloquio (15 min).
```

---

## 👥 3. Organización y Asignación para 3 Integrantes

Para ejecutar cada fase de manera coordinada y sin cuellos de botella, las responsabilidades se dividen en 3 roles especializados:
* **Miembro 1 — Hernández Monroy Diana Victoria (Product & Marketing Lead):** Wireframes UX/UI de la app, Cartas Vivas 2D, lore de Mexamonsters, módulo de comercios locales, Estudios de Mercado (Interno y PESTEL), Buyer Personas, campaña publicitaria y maquetación del Informe Técnico.
* **Miembro 2 — Acosta Ayala Kevin Axel (Data Engineering & ML Lead):** Big Data, pipelines ETL, modelos predictivos de afluencia, base de datos offline-first y Chatbot IA ("El Nahual Guía").
* **Miembro 3 — Carrasco Sánchez Jessica Daniela (Operations Research & Quants):** Minería de datos, simulación Monte Carlo de capacidad de carga, optimización matemática (IO en Python/PuLP) y métricas de impacto ecológico ($CO_2$).

> Consulta la matriz completa de tareas por semana y entregables individuales en [docs/ASIGNACION_ROLES_Y_ACTIVIDADES.md](docs/ASIGNACION_ROLES_Y_ACTIVIDADES.md).

---

## 🚀 4. Fases y Actividades Detalladas

### 📌 FASE 1: Corredor Piloto, Big Data y Wireframes (Semanas 1 a 5)
* **Objetivo Académico y de Producto:** Delimitar el clúster regional de prueba, diseñar la arquitectura de datos masivos y definir la experiencia de usuario del MVP.
* **Actividades clave:**
  - [x] Documentar el pivot de producto y especificación del juego (`docs/PIVOT_APP_GAMIFICADA.md`).
  - [x] **Delimitación del Corredor Piloto:** Formalizar el clúster piloto en el Corredor *El Insurgente / Valle de Toluca* (Zinacantepec, Toluca Centro, Metepec, Lerma).
  - [x] **Catálogo Piloto:** Estructurar los 4 Mexamonsters iniciales (*Xinán*, *Barrotépetl*, *Acatl-Tule*, *Mosco Matlatzinca*) y el directorio inicial de 15 comercios locales afiliados.
  - [x] **Arquitectura Big Data (UCA Herramientas de Almacenamiento):**
    - Pipeline de ingesta para telemetría de jugadores (GPS, escaneo de QRs, desbloqueo de Mexamonsters, canjes) y datos oficiales (DataTur, aforos de tren/transporte masivo, DENUE de INEGI).
    - Base de datos relacional SQLite de temporadas turísticas nacionales 1995-2024 (`turismo_mexico_temporadas.db`).
  - [x] **Minería de Datos (UCA Minería de Datos):**
    - Análisis exploratorio de datos de turismo y afluencia por municipio (`01_algoritmo_rareza_inversa_eda.py`).
    - Detección de patrones temporales: identificación de horas valle y fines de semana ociosos en destinos emergentes.
    - Mapa interactivo Folium del corredor (`campana/mapa_interactivo_corredor_mexamonsters.html`).
  - [ ] **Diseño UX / Wireframes de la App:**
    - Flujo 1: Pantalla de Mapa / Radar con geolocalización nativa de Mexamonsters.
    - Flujo 2: Vista de Misión territorial y validación de Puntos de Interés (POI).
    - Flujo 3: Carta Viva 2D de Mexamonsters con microanimaciones (Lottie / Rive).
    - Flujo 4: Bóveda / Álbum de Colección y Wallet de Bendiciones Económicas.
* **🏁 HITO 1: ENTREGA 1 (Semana 5)**
  * *Entregables:* Documento de diagnóstico y especificación de producto, arquitectura Big Data, bases de datos procesadas (`datos/processed`), diccionario de datos, notebook de minería y kit de wireframes UX.

---

### 📌 FASE 2: Modelos Predictivos, Chatbot IA y Optimización (Semanas 6 a 10)
* **Objetivo Académico y de Producto:** Desarrollar los algoritmos matemáticos y de machine learning que gobiernan la rareza inversa, el motor de recomendación, el asistente inteligente y el módulo de comercio local.
* **Actividades clave:**
  - [ ] **Machine Learning (UCA Aprendizaje de Máquina):**
    - Modelo predictivo para calcular el **Índice de Saturación Turística (IST)** en tiempo real/semanal.
    - Algoritmo de asignación dinámica de **Rareza Inversa** a los Mexamonsters en función del IST predicho.
    - Motor de recomendación de rutas personalizadas según las preferencias del jugador.
  - [ ] **Módulo de Inteligencia Artificial (Chatbot "El Nahual Guía"):**
    - Desarrollo del prototipo de chatbot conversacional con NLP para brindar pistas gamificadas en rima sobre la ubicación de Mexamonsters y recomendaciones culturales y gastronómicas.
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
* **🏁 HITO 2: ENTREGA 2 (Semana 10)**
  * *Entregables:* Notebooks ejecutables de ML con evaluación de modelos ($R^2$, RMSE), script del Chatbot, simulaciones Monte Carlo de capacidad de carga, formulación y solución matemática de IO, y especificación funcional del módulo de comercios.

---

### 📌 FASE 3: MVP Funcional, Estudio de Mercado y Campaña (Semanas 11 a 13)
* **Objetivo Académico y de Producto:** Construir el prototipo funcional de la aplicación (modo offline-first), consolidar el Estudio de Mercado y diseñar la campaña publicitaria inteligente.
* **Actividades clave:**
  - [ ] **Desarrollo del MVP Móvil (Flutter / React Native):**
    - Implementación del modo *offline-first* (almacenamiento local SQLite/Hive).
    - Integración de Cartas Vivas 2D animadas de Mexamonsters.
    - Lógica de geofencing (GPS) y lector de códigos QR físicos.
    - Integración de enlace directo con Google Maps (*Deeplinking* para iniciar caminata a POIs).
    - Prototipo del visor histórico de cámara ("La Ventana del Tiempo" con filtro sobrepuesto).
  - [x] **Mercadotecnia Digital (UCA Mercadotecnia Digital):**
    - **Estudios de Mercado Integrales (Actividad 3 y 5):**
      - *Estudio Interno y de Oferta (Actividad 3):* Oferta, Territorio, Periodo, Matriz Schwartz 2×2, Expansión y Criterios de Transición (`docs/ESTUDIO_DE_MERCADO_MEXAMONSTERS.md`).
      - *Estudio Externo PESTEL (Actividad 3):* Diagnóstico del macroentorno (Político, Económico, Social, Tecnológico, Ecológico y Legal) con decisiones estratégicas data-driven (`docs/ESTUDIO_DE_MERCADO_EXTERNO_PESTEL.md`).
      - *Benchmarking de Competencia (Actividad 5):* Análisis exhaustivo de competidores directos, indirectos y sustitutos, matriz paramétrica y factores diferenciales radicales (`docs/BENCHMARKING_MERCADO_COMPETENCIA.md`).
    - Perfilado cuantitativo de los **3 Buyer Personas** (`campana/buyer_personas/`):
      1. *Explorador Completista (Gamers & Geeks)*: Adopción y viralidad.
      2. *Turista Consciente / Mochilero*: Sostenibilidad y ticket cultural.
      3. *Familias Jóvenes*: Volumen de gasto familiar y retención.
    - Plan de campaña en 4 fases: Prelanzamiento (S1-S4), Lanzamiento *"El Despertar de los Mexamonsters"* (S5-S6), Sostenimiento con Eventos Leyenda (S7-S20) y Postlanzamiento (S21-S24).
    - Tablero de control (Dashboard) con KPIs: Tasa de conversión, coste de adquisición (CAC), derrama económica en comercios locales y $CO_2$ evitado por viajar en tren.
  - [ ] **Borrador del Informe Técnico:** Consolidación de los primeros apartados de la rúbrica oficial.
* **🏁 HITO 3: ENTREGA 3 (Semana 13)**
  * *Entregables:* Código fuente del MVP de la app en GitHub, Estudio de Mercado y dossier completo de campaña publicitaria, dashboard de KPIs y borrador avanzado del Informe Técnico (80%).

---

### 📌 FASE 4: Consolidación, Informe Técnico y Coloquio (Semanas 14 a 16)
* **Objetivo Académico y de Producto:** Cierre del informe de 30-40 páginas, auditoría del repositorio y preparación de la defensa oral.
* **Actividades clave:**
  - [ ] Ensamble definitivo del Informe Técnico con formato institucional y normas APA 7ma edición.
  - [ ] Auditoría de reproducibilidad de todos los scripts (`datos/`, `notebooks/`, `modelos/`).
  - [ ] Diseño de las diapositivas ejecutivas para la presentación final ante el sínodo.
  - [ ] Ensayo cronometrado de la defensa oral (15 minutos: 5 min Técnico, 5 min Cuantitativo, 5 min Comercial/Impacto).
* **🏆 HITO FINAL: COLOQUIO (Semanas 15 - 16)**
  * *Entregables:* Informe Técnico final empastado/PDF, repositorio GitHub impecable con licencia libre y presentación exitosa ante el comité evaluador.
