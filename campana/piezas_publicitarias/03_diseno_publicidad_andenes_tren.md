# Diseño de Publicidad y Señalética en Andenes del Tren Insurgente
## Canal Físico Prioritario: CAN-03 ($80,000 MXN Asignados en I.O.)
**Licenciatura en Ciencias de Datos para Negocios — 5to Semestre (Universidad Rosario Castellanos)**  
**Área:** Mercadotecnia de Proximidad y Comunicación Visual  
**Responsable:** Integrante 3 (Product & Marketing Lead)

---

## 1. Estrategia Territorial por Estación

A diferencia de la publicidad estática que muestra el mismo mensaje en toda la línea, nuestra estrategia aplica **marketing contextual geolocalizado**: el mensaje cambia según la estación donde se encuentra el pasajero y su dirección de viaje.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   ESTRATEGIA DE IMPACTO VISUAL EN EL CORREDOR                          │
└────────────────────────────────────────────────────────────────────────────────────────┘

 [EST-05 / EST-07: Santa Fe y Observatorio]  ──► CAPTACIÓN EN ORIGEN (CDMX)
                                                  "Sal de la burbuja: El fin de semana empieza en tren"

 [EST-04: Lerma]                            ──► CONEXIÓN BIOCULTURAL
                                                  "Despierta a Acatl-Tule y pedalea por las Ciénegas"

 [EST-03: Metepec]                          ──► CULTURA Y ARTESANÍA
                                                  "La tierra que cobra vida: Conoce a Barrotépetl"

 [EST-01: Zinacantepec]                     ──► DESTINO FINAL / NATURALEZA
                                                  "El reino de la escarcha: Despierta a Xinán"
```

---

## 2. Formato 01: Mupi Digital en Andenes de Embarque (1080 x 1920 px)

Ubicado en las mamparas de cristal de los andenes centrales de las estaciones **Santa Fe** y **Observatorio**, impactando a más de 45,000 usuarios diarios en espera del tren.

### Esquema Estructural del Mupi:

```
┌───────────────────────────────────────────────────────┐
│ [LOGOTIPO TREN]             [LOGO GUARDIANES DEL TERR.]│
│                                                       │
│             ¿A DÓNDE VAS ESTE DOMINGO?                │
│                                                       │
│   ┌───────────────────────────────────────────────┐   │
│   │                                               │   │
│   │             [ILUSTRACIÓN VECTORIAL            │   │
│   │             DEL GUARDIÁN XINÁN EN             │   │
│   │              MICROANIMACIÓN 2D]               │   │
│   │                                               │   │
│   │        "El Legendario de Zinacantepec"        │   │
│   │                                               │   │
│   └───────────────────────────────────────────────┘   │
│                                                       │
│    BAJA EN LA SIGUIENTE ESTACIÓN, EXPLORA A PIE       │
│         Y DESBLOQUEA TU COMIDA CON DESCUENTO          │
│                                                       │
│        ┌─────────────┐     ESCANEA Y JUEGA EN VIVO    │
│        │ [CÓDIGO QR] │   • Conexión WiFi libre en andén│
│        │  GIGANTE    │   • Modo Offline rural incluido │
│        │  ANTIFRAUDE │   • Cero comisiones para fondas │
│        └─────────────┘                                │
│                                                       │
│ [SECTUR EDOMEX]    [URC CIENCIA DE DATOS]   [SICT]    │
└───────────────────────────────────────────────────────┘
```

### Especificaciones Técnicas:
* **Resolución:** Full HD Vertical (1080 x 1920 píxeles, 60 fps).
* **Tipografía Principal:** Montserrat ExtraBold (Títulos a 72 pt) y Open Sans SemiBold (Cuerpo a 32 pt) para garantizar legibilidad a más de 4 metros de distancia bajo la iluminación artificial del andén.
* **Cromática:** Contraste reforzado WCAG AAA (Fondo Azul Marino `#090d16`, textos Blanco puro `#ffffff` y acentos Oro `#f59e0b` y Celeste `#38bdf8`).
* **Código QR Inteligente:** Tamaño físico de 25 x 25 cm con URL dinámica UTM (`https://guardianes.mx/qr?origen=est-santafe&medio=mupi-anden`) para medir la atribución exacta de descargas por andén en el pipeline de datos.

---

##  3. Formato 02: Tótem Físico Interactivo de Salida (Vestíbulo de Estaciones)

Instalado en los torniquetes de salida de las estaciones intermedias (**Zinacantepec, Toluca Centro, Metepec y Lerma**), orientado al viajero que acaba de descender del vagón y busca opciones de comida, cultura y transporte local.

### Especificaciones de Mensaje por Vestíbulo:

#### A. Vestíbulo Estación Zinacantepec (EST-01):
* **Titular Principal:** *"¡Bienvenido al Territorio del Xinantécatl!"*
* **Llamado de Acción Gamificado:**  
  *"Xinán duerme a 340 metros de esta salida. Camina hacia el Museo Virreinal de San Miguel, escanea la Pila Bautismal y despierta al Guardián Legendario."*
* **Incentivo Local:**  
  *"Al despertar a Xinán, recibe un 15% de descuento directo en barbacoa tradicional de hoyo en 'El Rinconcito Serrano' y pan de fiesta en Panadería San Miguel."*
* **Integración de Movilidad Sustentable:** Indicador de pasos a pie (8 min) y ruta de combis locales con tarifa oficial de $12 MXN.

#### B. Vestíbulo Estación Metepec (EST-03):
* **Titular Principal:** *"Tierra de Barro y Árboles de la Vida"*
* **Llamado de Acción Gamificado:**  
  *"Barrotépetl te espera en el Cerro de los Magueyes. Sigue las pistas del Nahual Guía y visita los talleres tradicionales de la Familia Soteno."*
* **Incentivo Local:**  
  *"Bendición activa: 20% en piezas artesanales de barro policromado o degustación tradicional de 'La Garañona' en el Bar 2 de Abril."*

#### C. Vestíbulo Estación Lerma (EST-04):
* **Titular Principal:** *"Santuario de Aves y Humedales"*
* **Llamado de Acción Gamificado:**  
  *"La Ninfa Acatl-Tule protege las Ciénegas de Lerma. Desbloquea la ruta ecoturística en bicicleta."*
* **Incentivo Local:**  
  *"Bendición activa: 2x1 en renta de bicicletas ecológicas y 20% en cestería artesanal de tule en San Pedro Tultepec."*

---

##  4. Formato 03: Dovelas y Paneles Interiores de Vagones (45 x 28 cm)

Ubicados a la altura de la vista de los pasajeros sentados en los vagones eléctricos de *El Insurgente*:

### Texto del Panel Interior (Lectura Rápida en Trayecto):
```text
┌───────────────────────────────────────────────────────────────────┐
│    MIENTRAS LLEGAS A TU DESTINO...                                │
│                                                                   │
│ ¿Sabías que viajar en este tren evita 7.6 kg de CO₂ frente a un   │
│ coche particular y que en la próxima parada puedes desbloquear un │
│ Guardián cultural que te invita la botana?                        │
│                                                                   │
│ 1. Abre tu cámara y escanea el código del asiento.                │
│ 2. Activa tu radar (funciona sin consumir tus datos).             │
│ 3. Convierte tu viaje en una aventura comunitaria.                │
│                                                                   │
│ [QR DESCARGA RÁPIDA]        GUARDIANES DEL TERRITORIO             │
│                             La app que descentraliza el turismo   │
└───────────────────────────────────────────────────────────────────┘
```

---

##  5. Criterios de Accesibilidad Universal y Señalética Inclusiva

1. **Inclusión para Adultos Mayores (Buyer Persona 04):**  
   * Los tótems físicos incluyen tipografía de gran cuerpo (mínimo 24 pt en instrucciones) y alto contraste cromático para pasajeros con baja agudeza visual.
   * La altura del código QR está calibrada a **1.20 metros del suelo**, facilitando su escaneo para personas en silla de ruedas o niños sin necesidad de inclinarse o estirarse.
2. **QR Sonoro y Asistido:**  
   * Al escanear el código, las personas con discapacidad visual acceden automáticamente a una audiodescripción en voz de "El Nahual Guía" que narra las instrucciones de orientación hacia el centro histórico o plaza comunitaria.
3. **Resistencia y Mantenimiento:**  
   * Impresión en vinil polimérico mate antirreflejante de 180 micras con laminado protector UV antigraffiti, garantizando una vida útil superior a 24 meses sin degradación visual en andenes exteriores.
