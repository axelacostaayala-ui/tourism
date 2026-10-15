# Análisis de Opciones Territoriales y Fuentes de Datos (Abierto)

Este documento presenta una comparativa de posibles entidades federativas para implementar el modelo **"Nodos Vivos: Utopías Turísticas y Movilidad Social Conectada"**, evaluando su pertinencia conceptual y la viabilidad de datos abiertos para alimentar los modelos analíticos.

> **Nota:** La elección final del estado se mantiene abierta para decisión del equipo.

---

## 1. Matriz Comparativa de Entidades Candidatas

| Criterio | Opción A: Ciudad de México (CDMX) | Opción B: Estado de México (Edomex) | Opción C: Quintana Roo / Yucatán |
| :--- | :--- | :--- | :--- |
| **Infraestructura de Transporte Masivo** | **Cablebús** (Línea 1 GAM, Línea 2 Iztapalapa, Línea 3 Chapultepec/Vasco de Quiroga) y Metro/Metrobús. | **Mexicable** (Línea 1 Ecatepec, Línea 2 Tlalnepantla) y **Tren Interurbano** (Toluca-Lerma). | **Tren Maya** (Estaciones y paraderos comunitarios). |
| **Alineación con el concepto "Utopías"** | **Excelente:** Las UTOPÍAS ya existen formalmente en Iztapalapa y se expanden como política pública de la CDMX. | **Muy Buena:** Posibilidad de crear Utopías metropolitanas articuladas al Mexicable. | **Buena:** Enfoque en estaciones de bienestar y cooperativas mayas. |
| **Disponibilidad de Datos de Movilidad** | **Masiva y diaria:** Portal de Datos Abiertos de la ADIP (afluencias diarias y horarias por estación). | **Media-Alta:** Estadísticas del SITRAMYTEM y Gobierno del Estado de México. | **En consolidación:** Estadísticas de pasaje de Fonatur / Sedena y DataTur. |
| **Datos Económicos y Comerciales** | **Excelente:** DENUE INEGI con cientos de miles de registros georreferenciados por manzana. | **Excelente:** DENUE INEGI de municipios metropolitanos. | **Alta:** DENUE INEGI y Censos Económicos. |
| **Redistribución Turística** | Descongestiona Reforma/Centro/Roma hacia Iztapalapa y GAM. | Canaliza flujos de la capital hacia corredores culturales periféricos mexiquenses. | Descongestiona Cancún/Tulum hacia pueblos y comunidades intermedias. |

---

## 2. Fuentes de Datos Abiertas Identificadas

Cualquiera que sea la entidad seleccionada, se aprovecharán las siguientes fuentes oficiales y públicas:

### A. Datos de Movilidad y Aforos
* **Portal de Datos Abiertos de la CDMX (ADIP):** Afluencia diaria por estación del Sistema de Movilidad Integrada (Cablebús, Metro, Metrobús, Trolebús).
* **INEGI - Estadística de Transporte Urbano de Pasajeros (ETUP):** Pasajeros transportados, kilómetros recorridos por sistema.
* **Secretaría de Infraestructura, Comunicaciones y Transportes (SICT):** Estadísticas de movimiento ferroviario y de pasajeros.

### B. Datos Económicos y Turísticos
* **INEGI - Directorio Estadístico Nacional de Unidades Económicas (DENUE):** Microdatos de comercios de alimentos y bebidas, talleres de artesanías, hospedajes, cooperativas y servicios recreativos con coordenadas GPS.
* **SECTUR - DataTur:** Ocupación hotelera, llegada de turistas nacionales y extranjeros, derrama económica y estacionalidad trimestral.
* **INEGI - Censos Económicos y Encuesta Nacional de Ingresos y Gastos de los Hogares (ENIGH):** Nivel de gasto de familias trabajadoras en recreación y cultura.

### C. Datos Territoriales y Ambientales
* **INEGI - Marco Geoestadístico Nacional:** Cartografía vectorial (polígonos de colonias, AGEBs y municipios).
* **CONABIO / SEDEMA:** Áreas de valor ambiental, reservas ecológicas y áreas verdes protegidas para calcular capacidades de carga ecosistémica.
* **Google Maps API / OpenStreetMap (Overpass API):** Distancias caminables (isócronas de 5, 10 y 15 minutos) desde las estaciones de transporte hasta los atractivos barriales.

---

## 3. Próximo Paso para la Elección
1. Revisar en equipo si se opta por **CDMX** (por la ventaja de tener ya la infraestructura de Cablebús + Utopías y datasets de afluencia muy detallados) o si se amplía a un **corredor metropolitano (CDMX - Edomex)** o **ferroviario regional**.
2. Una vez confirmado, se descargarán los archivos base correspondientes para iniciar la limpieza en el directorio `datos/`.
