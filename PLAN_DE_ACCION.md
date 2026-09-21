# Plan de Acción: Proyecto Prototípico - Turismo Inteligente Sustentable

Este documento describe el plan de acción, fases, tiempos y actividades propuestas para cumplir con los requerimientos del Problema Prototípico de 5to Semestre de la Licenciatura en Ciencias de Datos para Negocios.

## 🎯 Objetivos del Proyecto
Diseñar y desarrollar una campaña publicitaria inteligente, estratégica y sustentable para un destino turístico en un estado de México (por definir), utilizando la Ciencia de Datos como soporte para la toma de decisiones y la redistribución de los flujos turísticos.

## 📦 Entregables Finales (Antes del Coloquio)
El proyecto exige la entrega de tres componentes principales:
1. **Campaña Publicitaria**: Estrategia integral para promover el estado, segmentada y basada en datos.
2. **Informe Técnico**: Documento de 30 a 40 páginas detallando toda la justificación, modelos y estrategias.
3. **Productos Técnicos**: Bases de datos, código (scripts/notebooks), modelos desarrollados, consultas, diagramas, visualizaciones y resultados de simulaciones/optimización.

---

## 📅 Cronograma y Fases del Proyecto

Se propone un plan estructurado en **6 Fases**, asumiendo una duración típica de 16 semanas para el semestre.

### Fase 1: Preparación, Definición y Arquitectura (Semanas 1 - 3)
**Materias relacionadas:** Herramientas para el Almacenamiento de Grandes Volúmenes de Datos.
- [ ] **Elegir el Estado de la República:** (Pendiente) Analizar 2-3 opciones y decidir en base a disponibilidad de datos.
- [ ] **Estructura del Repositorio:** Configurar este repositorio en GitHub con las carpetas necesarias (`datos/`, `notebooks/`, `docs/`, `modelos/`).
- [ ] **Investigación de Fuentes:** Identificar y listar fuentes de datos útiles (DataTur, INEGI, Sectur, redes sociales, clima, etc.).
- [ ] **Arquitectura Big Data:** Diseñar cómo se van a almacenar y procesar estos datos (considerando que puedan no caber en una sola computadora convencional).
- **Hito:** Estado seleccionado y repositorio configurado con el primer esqueleto de arquitectura.

### Fase 2: Recopilación y Minería de Datos (Semanas 4 - 6)
**Materias relacionadas:** Minería de Datos, Herramientas de Almacenamiento.
- [ ] **Extracción y Limpieza:** Descargar datos históricos y construir los *pipelines* de limpieza.
- [ ] **Diccionario de Datos:** Documentar las variables seleccionadas.
- [ ] **Análisis Exploratorio y Patrones:** Identificar patrones de saturación turística, temporalidad, comportamiento y preferencias.
- [ ] **Insights iniciales:** Responder: ¿Qué destinos están saturados y cuáles tienen potencial subutilizado?
- **Hito:** Entrega del primer *Producto Técnico* (Bases de datos limpias y Diccionario de Datos).

### Fase 3: Modelado Predictivo y Escenarios Estocásticos (Semanas 7 - 9)
**Materias relacionadas:** Aprendizaje de Máquina, Modelos Estocásticos.
- [ ] **Desarrollo de Modelos ML:** Entrenar modelos de predicción de demanda turística o segmentación de turistas (clustering).
- [ ] **Evaluación de Modelos:** Validar los modelos con métricas adecuadas (evitando sobreajuste y considerando sesgos éticos).
- [ ] **Análisis de Incertidumbre:** Generar simulaciones (ej. Monte Carlo) para anticipar demanda bajo escenarios inciertos (clima, economía, etc.).
- [ ] **Intervalos de Confianza:** Estimar rangos probables de afluencia para las campañas.
- **Hito:** *Notebooks* de modelado y simulación listos.

### Fase 4: Optimización y Toma de Decisiones (Semanas 10 - 11)
**Materias relacionadas:** Investigación de Operaciones.
- [ ] **Formulación del Modelo Matemático:** Definir función objetivo (ej. maximizar beneficio económico, minimizar impacto ambiental) y restricciones (capacidad de carga de los destinos, presupuesto).
- [ ] **Resolución:** Implementar código para resolver el problema de optimización sobre cómo distribuir el flujo turístico y asignar presupuesto.
- [ ] **Análisis de Sensibilidad:** Evaluar cómo cambia la decisión óptima si varían las condiciones (ej. aumento de costos).
- **Hito:** Modelo de optimización y resultados de asignación.

### Fase 5: Estrategia de Mercadotecnia y Campaña (Semanas 12 - 13)
**Materias relacionadas:** Mercadotecnia Digital.
- [ ] **Definición del *Buyer Persona*:** Construir los perfiles utilizando los insights de la minería de datos y ML.
- [ ] **Propuesta de Valor y Branding:** Diseñar el mensaje clave y la identidad para redistribuir a los turistas hacia los destinos óptimos.
- [ ] **Selección de Canales y Piezas:** Definir medios (redes, buscadores, etc.) y estructurar las piezas publicitarias.
- [ ] **Indicadores (KPIs):** Definir cómo se medirá el éxito e impacto (comercial, social, ambiental) de la campaña.
- **Hito:** Entrega de la **Campaña Publicitaria**.

### Fase 6: Integración, Informe Técnico y Cierre (Semanas 14 - 16)
**Materias relacionadas:** Integración Interdisciplinaria.
- [ ] **Redacción del Informe Técnico:** Estructurar el documento (30-40 páginas) uniendo el trabajo de todas las materias.
- [ ] **Consolidación de Productos Técnicos:** Asegurar que todo el código esté comentado, funcional y subido al repositorio de GitHub.
- [ ] **Preparación de la Presentación:** Crear los slides para el coloquio, resumiendo hallazgos, articulación del proyecto y defensa.
- [ ] **Ensayo Final:** Preparar la exposición de 15 minutos.
- **Hito:** Entrega del **Informe Técnico** y **Productos Técnicos** finales. Defensa en el coloquio.

---

## 🛠️ Próximos Pasos Inmediatos
1. Discutir y seleccionar el **Estado de México** en el que se enfocará el proyecto.
2. Hacer el primer `commit` de este plan en el repositorio de GitHub y subirlo al servidor remoto.
3. Crear un archivo `README.md` que explique de forma breve de qué trata el repositorio.
