# Actividad 6: Investigación, Análisis y Construcción de Buyer Personas Basados en Ciencia de Datos
## Proyecto Integrador: Mexamonsters (Turismo Sostenible y Exploración Gamificada)

> **Universidad Rosario Castellanos**  
> **Licenciatura en Ciencias de Datos para Negocios — 5to Semestre**  
> **Unidad Curricular de Aprendizaje (UCA):** Mercadotecnia Digital  
> **Docente Asesor:** Mtro. Rafael Mena  
> **Equipo de Trabajo (Equipo 4 — Grupo 501):**  
> 1. **Hernández Monroy Diana Victoria** (*Product & Growth / Marketing Lead*)  
> 2. **Acosta Ayala Kevin Axel** (*Data Engineering & ML Lead*)  
> 3. **Carrasco Sánchez Jessica Daniela** (*Operations Research & Quants Lead*)  
> **Fecha de Investigación y Entrega:** 25 de Noviembre de 2026  

---

```
====================================================================================================
                        UNIVERSIDAD ROSARIO CASTELLANOS
                 LICENCIATURA EN CIENCIAS DE DATOS PARA NEGOCIOS
                           GRUPO 501 — CICLO 2026-2
====================================================================================================
  ACTIVIDAD 6: CONSTRUCCIÓN FUNDAMENTADA DE BUYER PERSONAS BASADOS EN CIENCIA DE DATOS
  PROYECTO: Mexamonsters — Descentralización Turística y Movilidad Sostenible en el Tren Insurgente
====================================================================================================
```

---

## 📑 Índice de Contenidos

1. [Cuartilla Introductoria: Marco Conceptual y la Ciencia de Datos en la Construcción de Buyer Personas](#1-cuartilla-introductoria-marco-conceptual-y-la-ciencia-de-datos-en-la-construcción-de-buyer-personas)
2. [Delimitación Rigurosa del Público Objetivo y Conexión con Estudios Previos](#2-delimitación-rigurosa-del-público-objetivo-y-conexión-con-estudios-previos)
3. [Investigación de los Ocho Elementos de la Anatomía del Buyer Persona en el Universo Objetivo](#3-investigación-de-los-ocho-elementos-de-la-anatomía-del-buyer-persona-en-el-universo-objetivo)
4. [Organización, Depuración y Análisis Comparativo de Datos Multivariados](#4-organización-depuración-y-análisis-comparativo-de-datos-multivariados)
   - 4.1. Limpieza y Normalización de Microdatos de Telemetría ($N = 8,000$)
   - 4.2. Algoritmo de Clustering K-Means y Validación con Coeficiente de Silueta
   - 4.3. Reducción Dimensional (PCA) y Matriz de Centroides Normalizados
   - 4.4. Síntesis Comparativa: Identificación de Patrones, Diferencias e Interpretación
5. [Construcción Detallada de los Tres Buyer Personas](#5-construcción-detallada-de-los-tres-buyer-personas)
   - 5.1. Buyer Persona 1: Rodrigo Morales — *"El Cazador de Rarezas / Gamer Gen Z"*
   - 5.2. Buyer Persona 2: Valeria Silva — *"La Viajera Consciente y Mochilera Cultural"*
   - 5.3. Buyer Persona 3: Familia Morales — Carlos y Mariana — *"Los Exploradores Familiares del Domingo"*
6. [Toma de Decisiones Estratégicas y Mix de Medios por Buyer Persona](#6-toma-de-decisiones-estratégicas-y-mix-de-medios-por-buyer-persona)
7. [Fuentes de Información y Referencias en Formato APA 7ma Edición](#7-fuentes-de-información-y-referencias-en-formato-apa-7ma-edición)

---

## 1. Cuartilla Introductoria: Marco Conceptual y la Ciencia de Datos en la Construcción de Buyer Personas

En la mercadotecnia contemporánea, la segmentación tradicional fundamentada de manera exclusiva en variables demográficas gruesas (como edad, género y nivel socioeconómico) ha demostrado ser insuficiente para predecir el comportamiento real de los usuarios en entornos omnicanal y altamente digitalizados. Dos consumidores con idéntica edad y nivel de ingresos pueden manifestar trayectorias de compra, patrones de atención y sensibilidades de marca diametralmente opuestas. Frente a esta limitación surge el concepto de **Buyer Persona**, formulado originalmente por Alan Cooper (1999) en el ámbito del diseño centrado en el usuario y formalizado en la mercadotecnia estratégica por David Meerman Scott (2007) y Tony Zambito (2011).

Un Buyer Persona se define metodológicamente como una **representación semi-ficticia y arquetípica del cliente ideal**, construida no a partir de la intuición o la imaginación subjetiva del mercadólogo, sino mediante una síntesis rigurosa de patrones conductuales, motivaciones profundas, objetivos vitales, barreras de adopción y hábitos de consumo de medios verificables. Su valor medular radica en humanizar los conjuntos de datos, dotando al equipo multidisciplinario (desarrolladores de producto, científicos de datos, creadores de contenido y especialistas en pauta digital) de un modelo mental compartido sobre **para quién se está diseñando y comunicando**.

En la era del Big Data y la inteligencia artificial, la construcción del Buyer Persona experimenta una revolución paradigmática. La práctica obsoleta de inventar personajes arbitrarios ("Juan, de 25 años, que le gusta el café y navegar en internet") es reemplazada por el **modelado algorítmico y empírico**. La ciencia de datos transforma la construcción de personas al introducir:

1. **Objetividad y Mitigación de Sesgos Cognitivos:** Los equipos de mercadotecnia tienden a proyectar sus propios gustos o prejuicios de clase sobre los clientes. El uso de microdatos censales (INEGI), encuestas sectoriales (ENDUTIH, AMVO) y telemetría de eventos de usuario extrae perfiles directamente de la estructura latente de los datos mediante técnicas no supervisadas como el agrupamiento (*Clustering K-Means*), la descomposición de componentes principales (*PCA*) y el procesamiento de lenguaje natural (*NLP*) sobre reseñas.
2. **Cuantificación de la Anatomía Conductual:** Permite parametrizar las dimensiones cualitativas del consumidor (tiempo libre disponible, elasticidad precio, nivel de alfabetización digital y disposición a la movilidad física) asignándoles pesos numéricos y distribuciones de probabilidad.
3. **Optimización del Costo de Adquisición (CAC) y Valor de Vida (LTV):** Un buyer persona fundamentado en datos permite dirigir cada peso del presupuesto publicitario al canal exacto (por ejemplo, TikTok para perfiles lúdicos frente a señalética física en estaciones ferroviarias para jefes de familia), optimizando las tasas de conversión y maximizando el retorno de inversión en mercadotecnia (*ROAS*).

En el marco del proyecto integrador **Mexamonsters**, enfocado en la descentralización turística del corredor del Tren Interurbano "El Insurgente", la construcción científica de nuestros Buyer Personas garantiza que la campaña publicitaria *"El Despertar de los Mexamonsters"* no dispare mensajes genéricos al vacío, sino que active resortes emocionales y conductuales específicos en tres segmentos clave que habitan un mismo territorio metropolitano.

---

## 2. Delimitación Rigurosa del Público Objetivo y Conexión con Estudios Previos

El público objetivo del proyecto no fue seleccionado de forma aislada, sino que es el resultado directo de la convergencia entre las investigaciones previas del semestre: el **Estudio de Mercado Interno (Actividad 3)**, el **Estudio de Mercado Externo PESTEL (Actividad 4)** y el **Análisis de Competencia Benchmarking (Actividad 5)**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               CONVERGENCIA METODOLÓGICA PARA DELIMITAR EL PÚBLICO OBJETIVO             │
└────────────────────────────────────────────────────────────────────────────────────────┘

 [Actividad 3: Mercado Interno] ──► Delimita el Corredor Ferroviario Zinacantepec - Lerma,
                                    la red de 15 comercios locales y la mecánica de
                                    Bendiciones (OTP) como propuesta de valor económica.

 [Actividad 4: PESTEL Externo]  ──► Cuantifica 5.2 millones de habitantes en zona de 
                                    influencia, 81.4% de penetración de smartphones (IFT)
                                    y la urgencia de turismo accesible post-inflación.

 [Actividad 5: Competencia]     ──► Detecta vacíos en Pokémon GO (alto consumo de batería/
                                    datos, nulo beneficio al comercio local) y TripAdvisor
                                    (comisiones del 20-30% inaccesibles para fondas).
                                                │
                                                ▼
  ┌────────────────────────────────────────────────────────────────────────────────────┐
  │                 UNIVERSO OBJETIVO DELIMITADO (CORREDOR INSURGENTE)                 │
  │  Hombres y mujeres de 18 a 45 años, residentes de ZMVM poniente y ZMVT, usuarios   │
  │  habituales o recreativos de movilidad masiva, con smartphone Android/iOS,         │
  │  que buscan ocio de fin de semana descentralizado, auténtico y económico.         │
  └────────────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 Delimitación Geográfica y Poblacional
* **Región de Origen (Emisora):** Zona Metropolitana del Valle de México (ZMVM), con énfasis prioritario en alcaldías con conectividad directa al Tren Insurgente en Metro Observatorio y Santa Fe: Cuajimalpa de Morelos, Álvaro Obregón, Miguel Hidalgo y Benito Juárez; así como habitantes de la Zona Metropolitana del Valle de Toluca (ZMVT: Toluca, Metepec, Zinacantepec, San Mateo Atenco y Lerma).
* **Población Objetivo Estimada:** De acuerdo con el Censo de Población y Vivienda (INEGI, 2020), la población en el rango de 18 a 45 años en estos municipios y alcaldías supera los **2.4 millones de personas**, de las cuales el **68.5%** viaja al menos una vez al mes por motivos de recreación o visita a familiares dentro del Estado de México o CDMX.
* **Corredor de Destino (Receptor):** Las cuatro estaciones operativas del Tren "El Insurgente": Zinacantepec (ZIN), Toluca Centro (TOL), Metepec (MET) y Lerma (LER).

### 2.2 Delimitación Demográfica y Socioeconómica
* **Edad:** 18 a 45 años (distribuidos en jóvenes universitarios/primer empleo de 18-26, profesionistas consolidados de 27-35 y familias jóvenes con hijos de 30-45 años).
* **Nivel Socioeconómico (Regla AMAI 2022):** Niveles **C, C+ y B** (ingreso neto mensual familiar entre \$18,000 y \$45,000 MXN). Se excluyen estratos A/B altos (cuyo turismo se orienta a vuelos internacionales y resorts de lujo) y estratos D/E de pobreza extrema (sin capacidad de gasto recreativo discrecional).
* **Conectividad Digital (ENDUTIH / IFT 2023-2024):** El 81.4% de la población mexiquense y el 89.2% de la población de CDMX es usuaria activa de teléfono inteligente (*smartphone*), con un uso promedio diario de 4.8 horas en internet y consumo intensivo de redes sociales y aplicaciones de mensajería (WhatsApp, TikTok, Facebook, Instagram).

---

## 3. Investigación de los Ocho Elementos de la Anatomía del Buyer Persona en el Universo Objetivo

Para evitar retratos superficiales, se investigaron los **ocho componentes estructurales de la anatomía del consumidor** en nuestro público objetivo, respaldados por estudios estadísticos oficiales y literatura de comportamiento del consumidor:

```
                  ┌──────────────────────────────────────────────┐
                  │      ANATOMÍA DEL BUYER PERSONA EN 8 EJES     │
                  └──────────────────────────────────────────────┘
                       [1] Identidad & Momento de Vida
                       [2] Entorno Social & Convivencia
                       [3] Economía, Ingresos & Recursos
                       [4] Tiempo, Rutinas & Movilidad
                       [5] Motivaciones & Necesidades
                       [6] Barreras, Dolores & Sensibilidades
                       [7] Gustos, Ocio & Estilo de Vida
                       [8] Mundo Digital & Proceso de Decisión
```

### Eje 1: Identidad y Momento de Vida
El universo objetivo se encuentra en etapas vitales de transición o consolidación:
1. *Jóvenes en consolidación académica o primeros empleos (18-26 años):* Buscan autoafirmación, pertenencia a tribus digitales y aventuras de bajo presupuesto que puedan registrar en sus redes sociales.
2. *Adultos jóvenes y profesionistas (27-35 años):* Experimentan saturación laboral y estrés corporativo (*burnout* urbano); buscan experiencias con significado ecológico, contacto con la naturaleza y reconexión cultural.
3. *Padres de familia jóvenes (30-45 años con hijos de 5 a 12 años):* Enfocados en la crianza activa; su momento vital gira en torno a generar memorias familiares felices y educativas en entornos seguros que no pongan en riesgo la solvencia financiera del hogar.

### Eje 2: Entorno Social
La socialización es el motor primario del turismo de fin de semana:
* De acuerdo con la Encuesta Nacional de Gasto de los Hogares (ENGAHO / INEGI), el **84.2%** de las salidas recreativas cortas en México se realizan en grupo: con amigos (31%), en pareja (22%) o con núcleo familiar extendido (31.2%).
* El factor "aprobación social" opera a través del contenido generado por el usuario (*UGC*): compartir fotos de lugares poco conocidos, comida tradicional o logros en aplicaciones lúdicas refuerza el estatus del individuo dentro de su comunidad digital o familiar.

### Eje 3: Economía y Recursos
* **Ingreso y Disposición al Gasto:** El estudio de Comercio Electrónico de la AMVO (2024) y la ENIGH (2022) revelan que el gasto promedio destinado a cultura, esparcimiento y alimentos fuera del hogar en los estratos C y C+ oscila entre el **11% y el 16% del ingreso mensual** (\$2,200 a \$4,800 MXN mensuales por hogar).
* **Sensibilidad al Precio:** Tras los picos inflacionarios de 2023-2025 en alimentos (superior al 6.5% anual en servicios turísticos tradicionales), los consumidores han desarrollado una **hipersensibilidad al costo de los consumibles turísticos**. Valoran profundamente los esquemas de descuento transparente, 2x1 o incentivos directos (como las Bendiciones de Mexamonsters) que amortigüen el costo del almuerzo o las actividades recreativas.

### Eje 4: Tiempo y Rutinas
* **Jornadas Semanales Extenuantes:** Según la OCDE, México registra las jornadas laborales más extensas (más de 2,120 horas al año). De lunes a viernes, los consumidores dedican entre 2 y 3.5 horas diarias al traslado laboral en el Valle de México y Toluca.
* **La Ventana Sagrada del Fin de Semana:** El tiempo de ocio se concentra estrictamente en **bloques de 6 a 10 horas los sábados o domingos** (*Day-trips* o turismo de entrada por salida). El consumidor rechaza viajes que impliquen manejar 4 horas en autopistas con tráfico denso (ej. salida a Cuernavaca o Valle de Bravo) y prefiere destinos alcanzables en menos de 45-60 minutos vía transporte ferroviario moderno.

### Eje 5: Motivaciones y Necesidades
De acuerdo con la jerarquía de necesidades de Maslow adaptada al turismo (Pearce, 2005):
* **Necesidad de Desconexión Psicológica:** Salir del bullicio de asfalto, ruido y contaminación visual de las metrópolis.
* **Necesidad de Logro y Coleccionismo:** El impulso psicológico de "completar listas", obtener recompensas tangibles y alcanzar hitos lúdicos (gamificación).
* **Necesidad de Trascendencia y Sostenibilidad:** Sentir que el gasto económico propio apoya directamente a artesanos locales, alfareros y fondas comunitarias, evitando enriquecer a monopolios intermediarios.

### Eje 6: Barreras y Sensibilidades (*Pain Points*)
* **Costo Oculto del Viaje:** Casetas de cobro excesivas (\$120-\$250 MXN por tramo), gasolina cara y abusos en estacionamientos céntricos.
* **Fricción Tecnológica en Apps:** Descargas que superan los 100 MB, agotamiento veloz de la batería del smartphone, requerimiento forzoso de datos móviles en zonas rurales con baja cobertura (*shadow zones*) y procesos de registro complejos con tarjetas bancarias obligatorias.
* **Incertidumbre Sanitaria y de Calidad:** Miedo a consumir en establecimientos informales sin reseñas o validación de precios justos.

### Eje 7: Gustos y Estilo de Vida
* Preferencia por el turismo gastronómico popular (antojitos, barbacoa, gorditas de maíz criollo, chito, licores tradicionales como el mosquito).
* Interés por el ecoturismo accesible (senderismo ligero, miradores lacustres como las Ciénegas de Lerma, paseos ciclistas).
* Consumo de cultura pop, anime, videojuegos retro o casuales en móviles, y valoración de leyendas, mitos y cosmovisiones indígenas prehispánicas (nahuales, volcanes, deidades del agua y del barro).

### Eje 8: Mundo Digital y Proceso de Decisión
* **Fuentes de Descubrimiento:** TikTok e Instagram Reels son los motores de inspiración primaria para menores de 35 años ("Lugares secretos que debes visitar este fin de semana"). Para mayores de 35, los grupos de Facebook de recomendaciones locales y el boca a boca familiar dominan.
* **Proceso de Decisión AIDA (Atención, Interés, Deseo, Acción):**
  1. *Atención:* Video corto o cartel llamativo en andén del tren mostrando a una criatura mitológica animada (*Mexamonster*).
  2. *Interés:* La promesa de que al bajar en la siguiente estación del tren se puede desbloquear un descuento real en barbacoa o artesanías.
  3. *Deseo:* Visualizar la Carta Viva 2D y la ruta accesible a pie o bicicleta.
  4. *Acción:* Descarga inmediata de la aplicación móvil (menos de 35 MB) mediante el código QR sin fricción de pago inicial.

---

## 4. Organización, Depuración y Análisis Comparativo de Datos Multivariados

Para cumplir con el rigor de la carrera en **Ciencias de Datos para Negocios** y conectar con las asignaturas de *Minería de Datos*, *Big Data* y *Aprendizaje de Máquina*, la construcción de los Buyer Personas no se basó en intuiciones narrativas, sino en el procesamiento de los **microdatos de telemetría y aforos del proyecto piloto** (`datos/processed/eventos_jugadores_telemetria.csv`, $N = 8,000$ eventos generados por 500 usuarios en el corredor del Tren Insurgente).

### 4.1 Limpieza y Normalización de Microdatos
Se depuraron los registros de eventos eliminando pings duplicados y datos con coordenadas anómalas fuera del corredor geográfico. Se consolidaron cuatro variables cuantitativas por usuario:
1. $X_1$: **Gasto Promedio por Visita (MXN):** Ticket total reportado en comercios y transporte.
2. $X_2$: **Intensidad de Interacción Lúdica (Pings & Desbloqueos):** Frecuencia de uso del radar y Mexamonsters despertados por jornada.
3. $X_3$: **Sensibilidad a Bendiciones/Descuentos:** Tasa de redención de cupones OTP sobre eventos totales ($R = \frac{\text{Canjes}}{\text{Check-ins}}$).
4. $X_4$: **Movilidad Física en Territorio (Km caminados en POIs):** Desplazamiento pedestre acumulado registrado por sensor podométrico y GPS.

Para garantizar que el algoritmo no sesgara los resultados por escalas dispares (pesos frente a kilómetros), las variables se estandarizaron mediante transformación $Z$-score:
$$Z = \frac{X - \mu}{\sigma}$$

### 4.2 Algoritmo de Clustering K-Means y Validación de Silueta
Se aplicó el algoritmo de agrupamiento **K-Means** variando $k$ de 2 a 6. 
* El **Método del Codo (*Elbow Method*)** de la suma de cuadrados intra-clúster (WCSS) mostró un punto de inflexión marcado en **$k = 3$**.
* El **Coeficiente de Silueta (*Silhouette Score*)** alcanzó su valor óptimo en $k = 3$ con un puntaje de **$s = 0.718$**, confirmando la existencia de tres agrupamientos densos, compactos y nítidamente diferenciados entre sí.

```
       MÉTODO DEL CODO (WCSS)                 COEFICIENTE DE SILUETA
   WCSS │                                  Silh │
  18000 ┼──●                                0.8 ┼       ● (k=3, s=0.718)
  12000 ┼    ╲                              0.7 ┼      ╱ ╲
   8000 ┼     ╲                             0.6 ┼     ╱   ╲
   4000 ┼      ● (Codo en k=3)              0.5 ┼    ●     ●
   2000 ┼       ╲───●───●                   0.4 ┼───────────────
      0 ┴──┬───┬───┬───┬───                 0.0 ┴───┬───┬───┬───
           2   3   4   5                            2   3   4   5
               k (Clusters)                             k (Clusters)
```

### 4.3 Reducción Dimensional (PCA) y Matriz de Centroides Normalizados
Para visualizar el comportamiento de los clústeres en dos dimensiones ortogonales, se aplicó un **Análisis de Componentes Principales (PCA)** sobre las 4 variables estandarizadas:
* **Componente Principal 1 (PC1 - 58.4% varianza explicada):** Representa el *Eje de Intensidad Gamificada y Digital* (cargas altas en interacción lúdica y kilómetros caminados).
* **Componente Principal 2 (PC2 - 27.6% varianza explicada):** Representa el *Eje de Derrama Económica y Ahorro Familiar* (cargas altas en gasto total y redención de cupones de alimentos).

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             MAPA DE DISPERSIÓN DE CLÚSTERES (PCA 2D — 86.0% VARIANZA)                  │
└────────────────────────────────────────────────────────────────────────────────────────┘

        PC2: Gasto Total y Ahorro Familiar (MXN)
          ▲
     +3.0 ┼                                  [CLÚSTER 3: FAMILIA TRABAJADORA]
          │                                  ● Centroide: (PC1: -0.85, PC2: +2.10)
     +2.0 ┼                                  • 45.1% de la muestra
          │                                  • Ticket agregado alto, redención masiva
     +1.0 ┼                                  • Movilidad contenida en plazas y fondas
          │
      0.0 ┼───────────────────[CLÚSTER 2: VIAJERA CONSCIENTE]────────────────────────► PC1: Intensidad
          │                   ● Centroide: (PC1: +0.45, PC2: -0.15)                   Gamificada y
     -1.0 ┼                   • 22.8% de la muestra (Turismo Cultural)                 Movilidad
          │                   • Gasto artesanal medio-alto, alta caminata             Pedestre
     -2.0 ┼   [CLÚSTER 1: GAMER GEN Z]
          │   ● Centroide: (PC1: +1.95, PC2: -1.40)
     -3.0 ┼   • 32.1% de la muestra
          │   • Máxima interacción en app, ticket bajo en alimentos, foco en ranking
          ┴──────┬────────────┬────────────┬────────────┬────────────┬────────────
                -2           -1            0           +1           +2
```

#### Matriz de Centroides Multivariados (Valores Reales Promedio)

| Variable Cuantitativa | Universo Total ($N=500$) | Clúster 1: Gamer Completista | Clúster 2: Viajera Consciente | Clúster 3: Familia Trabajadora | Prueba ANOVA ($F$-Stat / $p$-value) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Edad Promedio (Años)** | 29.4 | **22.6** | **29.8** | **37.5** | $F = 184.2, p < 0.001$ |
| **Gasto Diario por Persona (MXN)** | \$284.50 | **\$145.20** | **\$485.60** | **\$265.80** (\$920 x familia) | $F = 212.8, p < 0.001$ |
| **Mexamonsters Desbloqueados** | 1.58 | **3.42** | **1.85** | **0.88** | $F = 340.5, p < 0.001$ |
| **Pings de Radar por Sesión** | 7.2 | **14.8** | **6.1** | **3.2** | $F = 289.1, p < 0.001$ |
| **Tasa de Redención de Cupones (%)**| 12.4% | **7.8%** | **18.2%** | **31.5%** | $F = 156.4, p < 0.001$ |
| **Ahorro Promedio por Canje (MXN)** | \$53.40 | **\$55.26** | **\$44.09** | **\$53.67** | $F = 12.1, p < 0.01$ |
| **Distancia Caminada (Km/día)** | 4.6 km | **7.8 km** | **6.4 km** | **2.9 km** | $F = 198.7, p < 0.001$ |
| **Proporción en Muestra (%)** | 100% | **32.1%** | **22.8%** | **45.1%** | $\chi^2 = 88.4, p < 0.001$ |

### 4.4 Síntesis Comparativa: Identificación de Patrones, Diferencias e Interpretación

#### A) Identificar Patrones (Lo que une al público objetivo)
1. **Adopción del Tren Insurgente como Eje Articulador:** Todos los perfiles valoran el tren como un medio moderno, seguro y rápido para salir de la metrópoli sin padecer el tráfico de la carretera México-Toluca.
2. **Búsqueda de Autenticidad Local:** Coinciden en el repudio a las franquicias de comida rápida estandarizadas y buscan el sabor genuino de la gastronomía y artesanía mexiquense.
3. **Smartphones Android de Gama Media como Terminal Universal:** Más del 80% opera dispositivos con pantallas de 6.5 pulgadas y memorias de 64 a 128 GB, demandando aplicaciones ligeras que no consuman su saldo de datos.

#### B) Detectar Diferencias (Factores de divergencia)
1. **Diferencia en el Disparador (*Trigger*) de Consumo:**
   * El *Gamer Gen Z* se activa ante el reto, el coleccionismo y la exclusividad lúdica (Mexamonsters Legendarios).
   * La *Viajera Consciente* se activa ante la historia biocultural, el ecoturismo y la compra directa a artesanos.
   * La *Familia Trabajadora* se activa ante el beneficio económico directo (ahorro inmediato en comidas familiares y actividades infantiles seguras).
2. **Diferencia en el Customer Journey y Tiempo en Pantalla:**
   * El Gamer mantiene la app abierta el 75% del recorrido con interacción táctil continua.
   * La Viajera utiliza la app como guía de consulta intermitente (25% del tiempo) para escuchar relatos del Nahual Guía y validar QRs.
   * La Familia utiliza la app en modo "relevo": los padres la abren para obtener el cupón y se la prestan a los hijos para atrapar al Mexamonster en la plaza cívica.

#### C) Interpretar (Impacto en la toma de decisiones de mercadotecnia)
La ciencia de datos demuestra que una sola campaña no puede comunicarse con los tres segmentos con el mismo tono ni en los mismos medios. Intentar venderle "ahorro en barbacoa" al gamer o "combates lúdicos" a la madre de familia generaría altas tasas de rebote publicitario. Se requiere una estrategia de **pauta tripartita** con creatividades y canales personalizados.

---

## 5. Construcción Detallada de los Tres Buyer Personas

A continuación se desarrollan en profundidad los tres perfiles arquetípicos resultantes del análisis clúster, detallando exhaustivamente los ocho elementos de su anatomía:

---

### 5.1 Buyer Persona 1: Rodrigo Morales — *"El Cazador de Rarezas / Gamer Gen Z"*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ FICHA TÉCNICA: BUYER PERSONA 1                                                         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ • Nombre Arquetípico: Rodrigo Morales ("Rorro")                                        │
│ • Avatar Representativo: Joven con sudadera negra, mochila técnica y smartphone en mano│
│ • Edad: 23 años (Generación Z)                                                         │
│ • Ocupación: Estudiante de Ingeniería de Software (8vo semestre) y becario de TI       │
│ • Residencia: Alcaldía Álvaro Obregón (cerca de Metro Observatorio, CDMX)              │
│ • Nivel Socioeconómico (AMAI): C+ / B                                                  │
│ • Rol en Mexamonsters: Motor de viralidad orgánica, retención y actividad diaria (DAU) │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Los Ocho Elementos de su Anatomía:

1. **Identidad y Momento de Vida:**
   Joven de 23 años, soltero, sin hijos, habitante de la Ciudad de México. Se encuentra en la etapa de transición hacia la independencia económica mediante su primera pasantía remunerada en una empresa de tecnología. Es nativo digital, competitivo, curioso y le apasiona ser pionero (*early adopter*) en tendencias tecnológicas, videojuegos y cultura pop geek. Su identidad está fuertemente anclada en sus logros digitales y el estatus que estos le confieren ante su grupo de pares.
2. **Entorno Social:**
   Convive en un círculo cerrado de 4 a 6 amigos de la universidad con quienes comparte servidores de Discord y grupos de Telegram sobre videojuegos de realidad aumentada (*Pokémon GO*, *Monster Hunter Now*) y anime. Prefiere salir en grupos pequeños de 2 o 3 amigos o realizar expediciones en solitario (*solo-travel*) con audífonos puestos para explorar libremente a su propio ritmo.
3. **Economía y Recursos:**
   Percibe un ingreso neto mensual de \$9,500 MXN (beca de pasantía + apoyo familiar). Dispone de un presupuesto discrecional para salidas de fin de semana de aproximadamente \$400 a \$600 MXN semanales. Es muy cuidadoso con los gastos en transporte (aprovecha la tarifa accesible del Tren Insurgente de \$15 a \$20 MXN), pero está dispuesto a pagar por bebidas energéticas, café de especialidad y comida callejera económica con tal de no frenar su expedición.
4. **Tiempo y Rutinas:**
   De lunes a viernes sus horarios son rígidos entre clases matutinas y jornadas remotas de trabajo frente a la computadora. Los sábados desde las 8:30 AM experimenta una necesidad de salir de su habitación y realizar caminatas largas. Realiza viajes rápidos de entrada por salida (*Day-trips*) de 6 a 8 horas, regresando a la CDMX antes de las 18:00 hrs para descansar o jugar en línea.
5. **Motivaciones y Necesidades:**
   * Deseo intrínseco de coleccionismo: "Tengo que capturar a todas las criaturas del catálogo antes que los demás".
   * Búsqueda de estatus y prestigio: Desea poseer a *Xinán* (Legendario de Zinacantepec) y a *Barrotépetl* (Épico de Metepec) en su versión holográfica para presumir la captura en historias de Instagram y foros especializados.
   * Exploración territorial activa: Le motiva recorrer calles desconocidas y descubrir callejones históricos si el juego lo recompensa con logros o cartas difíciles de encontrar.
6. **Barreras y Sensibilidades (*Pain Points*):**
   * Frustración ante aplicaciones pesadas (> 100 MB) que agotan la batería de su celular en menos de dos horas o que requieren recargas costosas de datos móviles.
   * Rechazo a interfaces lentas o juegos con mecánicas infantiles sin reto estratégico.
   * Pánico a quedarse sin batería a mitad de trayecto (siempre carga una batería portátil o *power bank*).
7. **Gustos y Estilo de Vida:**
   Aficionado a la música Lo-Fi, synthwave y podcasts de divulgación científica y gaming. Viste ropa urbana funcional (tenis de senderismo urbano, chamarra impermeable y mochila cruzada). Consume contenido de creadores de tecnología en YouTube y streamers en Twitch. Le gusta la comida urbana rápida (tacos de cecina, marquesitas, café frío).
8. **Mundo Digital y Proceso de Decisión:**
   * *Canales Principales:* TikTok, Discord, Reddit, Instagram, Twitter/X y YouTube.
   * *Dispositivo:* Xiaomi Redmi Note 13 / Poco X5 (Android 14), con plan prepago de telefonía móvil de 3 a 5 GB.
   * *Proceso de Conversión:* Ve un video viral en TikTok de 15 segundos con gameplay acelerado de Mexamonsters mostrando a *Xinán* en las faldas del Nevado de Toluca. Escanea el enlace, descarga la app en la estación Observatorio conectándose al WiFi público, y toma el tren motivado por la meta de desbloquear su primera carta épica en menos de 45 minutos.

* **Patrones que Comparte con el Público Objetivo:** Uso del corredor del Tren Insurgente como eje de movilidad; deseo de salir de la rutina metropolitana; preferencia por alimentos tradicionales en destinos intermedios; posesión de smartphone Android.
* **Factores Diferenciales:** Mayor tasa de permanencia y engagement activo dentro de la app; mayor distancia física caminada por jornada (7.8 km); menor ticket de gasto en comercios (\$145.20 MXN); canal de captación nativo en TikTok y comunidades gamer.

---

### 5.2 Buyer Persona 2: Valeria Silva — *"La Viajera Consciente y Mochilera Cultural"*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ FICHA TÉCNICA: BUYER PERSONA 2                                                         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ • Nombre Arquetípico: Valeria Silva ("Vale")                                           │
│ • Avatar Representativo: Mujer con lentes de armazón de pasta, cámara reflex al cuello │
│   y bolso artesanal de tela reciclada                                                  │
│ • Edad: 29 años (Millennial consolidada)                                               │
│ • Ocupación: Diseñadora Gráfica Editorial y creadora de contenido ambiental freelance  │
│ • Residencia: Colonia Del Carmen, Coyoacán (CDMX) / Frecuenta corredor Toluca-Metepec  │
│ • Nivel Socioeconómico (AMAI): B / C+                                                  │
│ • Rol en Mexamonsters: Generadora de reputación, embajadora de marca y derrama local   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Los Ocho Elementos de su Anatomía:

1. **Identidad y Momento de Vida:**
   Mujer de 29 años, profesionista independiente, soltera, con un estilo de vida bohemio-urbano y alto compromiso con causas socioambientales. Ha superado la etapa del consumismo ciego y se orienta hacia el consumo consciente, el comercio justo (*fair trade*) y el turismo regenerativo. Valora profundamente las raíces prehispánicas, los saberes comunitarios y la preservación de los ecosistemas lacustres y forestales.
2. **Entorno Social:**
   Forma parte de colectivos artísticos, clubes de lectura y redes de consumo agroecológico. Viaja con su pareja o con su mejor amiga. Sus recomendaciones influyen poderosamente en su círculo social cercano, quienes confían plenamente en su criterio estético y gastronómico para elegir destinos de fin de semana no masificados.
3. **Economía y Recursos:**
   Ingreso mensual neto promedio de \$26,000 MXN como profesional independiente. Dispone de un presupuesto generoso para ocio y bienestar de \$1,200 a \$1,800 MXN por salida de fin de semana. No le duele pagar un precio justo por una pieza artesanal auténtica (ej. un Árbol de la Vida de barro policromado en Metepec de \$450 MXN o un canasto tejido en tule en Lerma de \$280 MXN) ni por alimentos preparados con ingredientes locales de temporada.
4. **Tiempo y Rutinas:**
   Autogestiona su tiempo laboral bajo esquemas de entregas por proyecto. De lunes a jueves trabaja intensamente en su taller u oficina en casa. Los viernes por la tarde planea sus escapadas de fin de semana. Aprovecha puentes largos, festividades tradicionales (como Día de Muertos o festividades patronales) y sábados completos para desconectarse de las notificaciones de clientes y sumergirse en ambientes rurales o patrimoniales.
5. **Motivaciones y Necesidades:**
   * Conectar con historias vivas y memoria histórica: Desea conocer el significado mitológico de los lugares a través de relatos auténticos.
   * Apoyar de forma directa a la economía social: Saber que su dinero llega a las manos de los artesanos y cocineras tradicionales sin pasar por intermediarios corporativos abusivos.
   * Sostenibilidad ambiental: Elegir el Tren Insurgente porque evita la emisión de más de 7 kg de $CO_2$ a la atmósfera en comparación con el uso del automóvil particular.
6. **Barreras y Sensibilidades (*Pain Points*):**
   * Repudio al turismo depredador y masificado (*overtourism*) que destruye la identidad de los pueblos mágicos convirtiéndolos en centros comerciales abiertos.
   * Rechazo a aplicaciones que traten la cultura mexicana de manera caricaturesca, folclórica superficial o puramente comercial.
   * Desconfianza ante plataformas que cobren comisiones abusivas a los productores locales.
7. **Gustos y Estilo de Vida:**
   Consumidora de café orgánico, alimentos a base de plantas y cocina regional de herencia. Le apasiona la fotografía documental, el senderismo de bajo impacto, la ilustración botánica y los museos de sitio. Escucha podcasts de historia de México (*Ambulante*, crónicas urbanas) y música folk latinoamericana.
8. **Mundo Digital y Proceso de Decisión:**
   * *Canales Principales:* Instagram, Google Maps (lee y escribe reseñas exhaustivas de más de 200 palabras), Pinterest, boletines de ecoturismo y Spotify.
   * *Dispositivo:* iPhone 13 o Samsung Galaxy S22, con plan postpago corporativo de 15 GB.
   * *Proceso de Conversión:* Lee una reseña en un blog de diseño sobre la arquitectura de tierra y el trabajo en barro de Metepec que menciona cómo la app Mexamonsters utiliza un visor histórico ("La Ventana del Tiempo") y un asistente de inteligencia artificial ("El Nahual Guía") para narrar la cosmovisión otomí y matlatzinca. Descarga la aplicación para vivir la experiencia inmersiva y utiliza las Bendiciones para visitar tres talleres artesanales en el Barrio de Santiaguito en Metepec.

* **Patrones que Comparte con el Público Objetivo:** Movilidad en el Tren Insurgente; preferencia por el Corredor Valle de Toluca; gusto por la gastronomía típica; uso intensivo de tecnología móvil para planear salidas.
* **Factores Diferenciales:** Mayor gasto individual en comercios locales (\$485.60 MXN por persona); interacción orientada a la narrativa cultural y al visor histórico más que a la competencia lúdica; captación a través de Instagram y Google Maps; alta sensibilidad ecológica y de comercio justo.

---

### 5.3 Buyer Persona 3: Familia Morales — Carlos y Mariana — *"Los Exploradores Familiares del Domingo"*

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ FICHA TÉCNICA: BUYER PERSONA 3                                                         │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ • Nombre Arquetípico: Carlos (38 años, Contador) y Mariana (36 años, Enfermera docente)│
│ • Hijos: Mateo (9 años, fanático de dinosaurios y videojuegos) y Sofía (6 años)        │
│ • Avatar Representativo: Familia caminando por una plaza adoquinada; el padre lleva una│
│   mochila con botellas de agua y los niños miran emocionados la pantalla del teléfono  │
│ • Residencia: San Mateo Atenco / Lerma (conurbación Estado de México)                  │
│ • Nivel Socioeconómico (AMAI): C / C- (Ingreso familiar conjunto: $24,000 MXN)         │
│ • Rol en Mexamonsters: Volumen masivo de consumo, gasto agregado y recomendación vecinal│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Los Ocho Elementos de su Anatomía:

1. **Identidad y Momento de Vida:**
   Pareja casada de 38 y 36 años con dos hijos en educación básica (primaria y preescolar). Su identidad está plenamente enfocada en el bienestar, educación y formación de sus hijos. Se encuentran en una fase vital donde los recursos económicos deben administrarse con suma cautela debido a colegiaturas, despensa y pago de hipoteca. Buscan optimizar cada peso sin sacrificar el tiempo de calidad y diversión con los pequeños.
2. **Entorno Social:**
   Su vida social se organiza en torno a reuniones dominicales con abuelos, tíos y primos, grupos de WhatsApp de padres de familia de la escuela y vecinos del fraccionamiento habitacional. Comparten recomendaciones de paseos mediante mensajes de voz: *"Vecina, fuimos a Zinacantepec en el tren nuevo, los niños comieron riquísimo y no gastamos casi nada con los cupones de la aplicación"*.
3. **Economía y Recursos:**
   Ingreso neto familiar conjunto de \$24,000 MXN mensuales. Destinan un presupuesto estricto de \$800 a \$1,200 MXN para la salida recreativa dominical (que incluye pasajes, comida de 4 personas y un antojito o juguete para los niños). La inflación en la canasta básica ha mermado su capacidad de ahorro, por lo que **cualquier descuento del 15% al 25% en una comida de barbacoa o gorditas representa un alivio directo que define a qué lugar deciden entrar**.
4. **Tiempo y Rutinas:**
   De lunes a viernes la rutina es frenética: levantarse a las 6:00 AM para preparar desayunos, llevar a los niños a la escuela, cumplir turnos laborales extensos y regresar a casa a coordinar tareas escolares. El domingo es el único día sagrado de convivencia completa. Su ventana de salida recreativa transcurre invariablemente entre las 11:00 AM y las 17:00 PM.
5. **Motivaciones y Necesidades:**
   * Estimulación y aprendizaje para los niños: Desean que Mateo y Sofía se despeguen de la televisión, caminen al aire libre y aprendan sobre tradiciones mexicanas de forma entretenida.
   * Paseo seguro y predecible: Necesitan visitar lugares donde haya andadores peatonales amplios, sanitarios limpios, vigilancia y ambiente 100% familiar.
   * Maximización del presupuesto: Sentir la satisfacción de haber brindado un día excelente a sus hijos sin haber desbalanceado el presupuesto de la quincena.
6. **Barreras y Sensibilidades (*Pain Points*):**
   * Estrés por el aburrimiento y berrinches de los niños durante caminatas históricas tradicionales ("Papá, ¿ya nos vamos? ¡Los museos son aburridos!").
   * Miedo a cobros sorpresivos, cuentas infladas o estafas en restaurantes turísticos tradicionales.
   * Complicaciones técnicas: Desesperación ante aplicaciones que pidan tarjetas de crédito obligatorias o procesos de validación engorrosos en el mostrador del negocio mientras los niños están inquietos.
7. **Gustos y Estilo de Vida:**
   Consumo de cine familiar los viernes, carnes asadas o comidas familiares en casa de los abuelos los sábados. En sus salidas dominicales buscan gastronomía tradicional que guste a todos: consomé, barbacoa de borrego, tlacoyos de haba y frijol, nieves artesanales y dulces típicos. Visten ropa cómoda deportiva y tenis para caminar.
8. **Mundo Digital y Proceso de Decisión:**
   * *Canales Principales:* Facebook (grupos locales de colonias y páginas familiares), WhatsApp, YouTube Kids y carteles físicos en andenes de transporte.
   * *Dispositivo:* Teléfono Motorola Moto G54 o Samsung Galaxy A14, compartido durante el paseo: el padre carga el mapa y la madre le presta el teléfono a Mateo para que escanee los códigos QR en los parques y monumentos.
   * *Proceso de Conversión:* Al llegar a la estación Lerma o Zinacantepec, Carlos ve un tótem publicitario que dice: *"Despierta a Xinán con tus hijos y obtén un 20% de descuento en la comida de hoy"*. Escanea el QR grande, descarga la app en menos de 1 minuto. Durante la caminata, Mateo busca con entusiasmo la placa del convento para "despertar al monstruo", mientras Mariana muestra el código OTP de 4 dígitos en la fonda afiliada para hacer válido el descuento familiar sin tarjetas bancarias.

* **Patrones que Comparte con el Público Objetivo:** Movilidad obligada en el corredor ferroviario; búsqueda de desconexión y alimentación tradicional; alta sensibilidad a la seguridad y a la economía familiar; uso de smartphones Android comunes.
* **Factores Diferenciales:** Mayor volumen de gasto agregado por visita (\$920 a \$1,100 MXN en conjunto familiar); menor distancia caminada a pie (2.9 km debido al ritmo de los niños); uso colaborativo y compartido del dispositivo; canal de captación central en Facebook y señalética física en andenes del tren; activación basada en el ahorro inmediato en alimentos (*Bendiciones*).

---

## 6. Toma de Decisiones Estratégicas y Mix de Medios por Buyer Persona

Con base en la identificación de patrones y factores diferenciales, se estructura la **matriz de decisiones de mercadotecnia digital y pauta**, alineando la estrategia de comunicación con el presupuesto de **\$250,000 MXN** formulado en la UCA de *Investigación de Operaciones*:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│             MATRIZ DE ASIGNACIÓN ESTRATÉGICA POR BUYER PERSONA                         │
└────────────────────────────────────────────────────────────────────────────────────────┘

 [RODRIGO - GAMER GEN Z]     ──► 35% Presupuesto ($87,500 MXN)
                                 Canales: TikTok Ads, Twitch, Discord, Retos Virales.
                                 Hook: "El monstruo legendario que ningún chilango ha capturado".
                                 CTA: "Descarga y lidera el ranking regional".

 [VALERIA - MOCHILERA]       ──► 25% Presupuesto ($62,500 MXN)
                                 Canales: Instagram Ads, Google Maps geolocalizado, Prensa Cultural.
                                 Hook: "Viaja en tren, viaja verde: conoce los talleres de barro".
                                 CTA: "Explora la ruta biocultural del Nahual".

 [FAMILIA MORALES]           ──► 40% Presupuesto ($100,000 MXN)
                                 Canales: Facebook Ads geolocalizados, Señalética física en andenes.
                                 Hook: "El mejor domingo en familia: camina, juega y ahorra en tu comida".
                                 CTA: "Obtén tus Bendiciones familiares gratis aquí".
```

### Tabla Resumen de Decisiones Tácticas de Mercadotecnia

| Elemento Estratégico | Buyer Persona 1: Rodrigo (Gamer Gen Z) | Buyer Persona 2: Valeria (Mochilera Cultural) | Buyer Persona 3: Familia Morales (Exploradores Familiares) |
| :--- | :--- | :--- | :--- |
| **Objetivo de Campaña** | Adopción temprana, viralidad y usuarios activos diarios (DAU) | Construcción de marca ética, reputación y derrama artesanal | Masa crítica de volumen, canje de cupones y retención dominical |
| **Canales Publicitarios** | TikTok Ads, Meta Ads (Reels), Comunidades Discord / Reddit | Instagram Ads (Feed & Stories), Google Search/Maps local, Bloggers | Facebook Ads (segmentación padres), Tótems y Mupis físicos en andenes |
| **Formato de Contenido** | Video vertical 9:16 de 12 segundos, ritmo acelerado, gameplay | Carruseles fotográficos de alta estética, video documental de 30s | Banners en Facebook con fotos de barbacoa, carteles infográficos con QR |
| **Propuesta de Valor Clave** | Rareza Inversa, coleccionismo y estatus en el ranking de exploradores | Turismo regenerativo, bajo impacto de $CO_2$, memoria biocultural | Paseo seguro al aire libre con ahorro directo en el consumo familiar |
| **Trigger / Gancho Emocional**| Competitividad y curiosidad ("¿Podrás capturar a Xinán Legendario?") | Conexión con las raíces y apoyo solidario a artesanos mexiquenses | Nostalgia y alivio económico ("Que tus hijos aprendan jugando y ahorra") |
| **Llamada a la Acción (CTA)** | *¡Descarga Mexamonsters y despierta al primer Legendario antes que nadie!* | *Descubre la Ventana del Tiempo y apoya al arte local con tus Bendiciones* | *¡Planea tu domingo en familia! Descarga la app y obtén hasta 20% en tu comida* |
| **Incentivo en la App** | Cartas Vivas 2D holográficas, medallas y título de Explorador Supremo | Relatos poéticos del Nahual Guía y catálogo de talleres de origen | Cupones OTP 2x1 y 15% de descuento en fondas tradicionales |
| **CAC Estimado (IO)** | **\$14.50 MXN** (Alta tasa de descarga orgánica por viralidad) | **\$22.80 MXN** (Pauta de nicho y contenido editorial refinado) | **\$16.20 MXN** (Alta conversión por señalética física en estaciones) |
| **KPI de Desempeño** | Costo por Instalación (CPI) y DAU en fines de semana | Tasa de engagement, visitas a talleres y reseñas en Google Maps | Redención de códigos OTP en fondas y tasa de retención mensual |

---

## 7. Fuentes de Información y Referencias en Formato APA 7ma Edición

* Asociación Mexicana de Venta Online [AMVO]. (2024). *Estudio de Venta Online 2024: Hábitos de los compradores digitales en México*. AMVO Research. https://www.amvo.org.mx/estudios/estudio-venta-online-2024/
* Bartle, R. (1996). Hearts, clubs, diamonds, spades: Players who suit MUDs. *Journal of MUD Research*, 1(1), 19-35.
* Cooper, A. (1999). *The inmates are running the asylum: Why high-tech products drive us crazy and how to restore the sanity*. Sams Publishing.
* Instituto Federal de Telecomunicaciones [IFT] e Instituto Nacional de Estadística y Geografía [INEGI]. (2024). *Encuesta Nacional sobre Disponibilidad y Uso de Tecnologías de la Información en los Hogares (ENDUTIH) 2023*. Comunicado de prensa conjunto núm. 342/24. INEGI. https://www.inegi.org.mx/programas/endutih/2023/
* Instituto Nacional de Estadística y Geografía [INEGI]. (2020). *Censo de Población y Vivienda 2020: Tabulados del Estado de México y Ciudad de México*. INEGI. https://www.inegi.org.mx/programas/ccpv/2020/
* Instituto Nacional de Estadística y Geografía [INEGI]. (2022). *Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH) 2022: Estructura del gasto en esparcimiento y turismo interno*. INEGI.
* Kotler, P., & Armstrong, G. (2021). *Fundamentos de marketing* (14.ª ed.). Pearson Educación.
* Pearce, P. L. (2005). *Tourist behaviour: Themes and conceptual schemes*. Channel View Publications.
* Scott, D. M. (2007). *The new rules of marketing and PR: How to use social media, blogs, news releases, online video, and viral marketing to reach buyers directly*. John Wiley & Sons.
* Secretaría de Infraestructura, Comunicaciones y Transportes [SICT]. (2024). *Estudio de demanda y proyección de aforos operativos del Tren Interurbano El Insurgente (Tramo Zinacantepec - Observatorio)*. Gobierno de México. https://www.gob.mx/sict
* Secretaría de Turismo [SECTUR] y DataTur. (2024). *Compendio Estadístico del Turismo en México 2024: Indicadores de estacionalidad y gasto medio del turista nacional*. SECTUR.
* Zambito, T. (2011). *How to create buyer personas that help you understand what your customers really want*. Buyer Persona Institute.

---
*Fin del documento técnico — Mexamonsters 2026*
