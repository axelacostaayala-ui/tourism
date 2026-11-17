# Kit de Wireframes y Especificación UX/UI del MVP Móvil
## Proyecto: Guardianes del Territorio (Turismo Sostenible y Gamificación)
**Licenciatura en Ciencias de Datos para Negocios — 5to Semestre (Universidad Rosario Castellanos)**  
**Área:** Experiencia de Usuario (UX), Diseño de Interacción (UI) y Mercadotecnia Digital  
**Responsable:** Integrante 3 (Product & Growth / Marketing Lead)

---

## 📱 1. Prototipo Visual Interactivo

Se ha implementado un prototipo funcional e interactivo en formato web responsivo (simulando un chasis de smartphone de alta fidelidad con animaciones fluidas a 60 fps y motor offline-first):

* 🔗 **Archivo local del prototipo:** [campana/prototipo_interactivo_mvp.html](../campana/prototipo_interactivo_mvp.html)
* **Instrucciones para visualizarlo:** Doble clic en el archivo HTML o abrirlo desde cualquier navegador web moderno (Google Chrome, Edge, Safari, Firefox). No requiere conexión a internet ni servidor backend para su demostración.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        ARQUITECTURA DE FLUJOS DEL MVP MÓVIL                            │
└────────────────────────────────────────────────────────────────────────────────────────┘

 [1. Radar de Exploración] ──► [2. Misión POI] ──► [3. Carta Viva 2D] ──► [4. Wallet Cupones]
           │                                                                    │
           ▼                                                                    ▼
 [Pistas en Verso IA]                                                [Canje OTP sin Hardware]
```

---

## 🧭 2. Especificación Detallada de las Pantallas del MVP

### 📍 Pantalla 1: Radar de Exploración & Asistente IA ("El Nahual Guía")
* **Objetivo:** Orientar al viajero al bajar de la estación del tren ligero sin saturar su pantalla con mapas complejos ni publicidad invasiva.
* **Componentes de Interfaz:**
  1. **Indicador de Estado Offline:** Etiqueta verde persistente en la cabecera (*"Modo Offline Activo"*) que confirma que todos los datos vectoriales y pistas operan desde la memoria local (SQLite/Hive).
  2. **Radar Polar Interactivo:** Retícula concéntrica con barrido giratorio animado (conic-gradient) que sitúa al usuario en el centro y proyecta *blips* pulsantes de los Guardianes dormidos según su distancia geodésica.
  3. **Insignia de Rareza Inversa:** Muestra si el Guardián detectado es *Legendario* (púrpura), *Épico* (rosa) o *Raro* (celeste), calculada por el modelo predictivo de Machine Learning.
  4. **Caja de Pistas del Nahual Guía:** Tarjeta mística con micro-avatar del nahual que despliega coplas líricas y adivinanzas históricas para guiar la búsqueda hacia monumentos o talleres.

---

### 📷 Pantalla 2: Misión Territorial & Validación Antifraude
* **Objetivo:** Garantizar la presencia física del usuario en los Puntos de Interés (POIs) comunitarios mediante un protocolo dual de verificación.
* **Mecánica Antifraude Dual:**
  1. **Geofencing Nativo por Hardware:** La app consulta el sensor GPS nativo del dispositivo y valida que el radio de distancia al POI sea menor a **50 metros**. Si el usuario está lejos, la validación se bloquea para evitar trampas remotas.
  2. **Escáner de Código QR en Sitio:** Visor simulado de cámara con mira y haz láser dinámico. Al encuadrar el código QR ubicado físicamente en la entrada del exconvento, mirador o taller, el sistema registra el evento `POI_QR_SCAN` con sello de tiempo criptográfico.
* **Componentes Visuales:** *Stepper* de misión con estados visuales (Completado en verde, En Progreso en azul) para que el viajero sepa cuántos POIs le faltan para despertar a la criatura (mínimo 1 a 2 POIs).

---

### 🎴 Pantalla 3: Carta Viva 2D Despertada (Coleccionable)
* **Objetivo:** Provocar la gratificación emocional inmediata del jugador (*monster-collecting* de alto impacto estético) y transmitir el valor del patrimonio biocultural.
* **Características de Diseño:**
  1. **Marco Visual por Rareza Inversa:** Acabados degradados según el nivel de saturación turística:
     * **Legendario (Zinacantepec - Xinán):** Bordes violeta místico con resplandor dorado y destellos de escarcha volcánica.
     * **Épico (Metepec - Barrotépetl / Lerma - Acatl-Tule):** Tonos fucsia y esmeralda con motivos de barro y tule.
     * **Raro (Toluca Centro - Mosco):** Tonos cian y azul vitral.
  2. **Efecto de Shimmer & Flotación:** Capa de destello brillante en ángulo de 45° que se desplaza continuamente sobre el arte vectorial del Guardián simulando una carta física holográfica.
  3. **Matriz de Atributos de Impacto:**
     * *IST Rareza:* Valor numérico calculado por el algoritmo de Data Science.
     * *Comunidad:* Porcentaje de retorno local (100% comercio de barrio).
     * *CO₂ Evitado:* Kilogramos de carbono mitigados por haber llegado en tren ligero en lugar de automóvil particular.

---

### 🎟️ Pantalla 4: Wallet de Bendiciones & Módulo de Canje Sin Hardware
* **Objetivo:** Conectar el éxito del juego con la derrama económica en fondas, panaderías y talleres comunitarios sin obligar al artesano a comprar lectores de tarjetas caros ni pagar comisiones bancarias del 3-5%.
* **Flujo de Redención OTP:**
  1. **Cupón Digital Claro:** Título de la recompensa en tipografía legible de alto contraste (ej. *15% de Descuento* o *Pieza de Pan de Fiesta de Cortesía*).
  2. **Código OTP Dinámico:** Código alfanumérico de 4 dígitos generado localmente (ej. `BND-4821` o `MET-3914`) con temporizador regresivo de seguridad de 25 minutos.
  3. **Validación del Locatario (Simulada):** El comerciante sólo necesita que el cliente le dicte el código OTP o se lo muestre en pantalla. El prototipo incluye una ventana modal de recibo donde se demuestra que la comisión es **$0.00 MXN**.

---

### ⏳ Pantalla 5: Visor Histórico ("La Ventana del Tiempo")
* **Objetivo:** Fomentar el turismo cultural profundo y la educación intergeneracional.
* **Mecánica de Interacción:** 
  * Un deslizador horizontal interactivo (*slider*) permite comparar de forma fluida una fotografía del presente (2026) con una postal de archivo histórico (1910) del mismo espacio público (atrio parroquial o plaza cívica), permitiendo al viajero reflexionar sobre la preservación territorial.

---

## 👥 3. Alineación del Diseño UX con los 4 Buyer Personas

| Buyer Persona | Elemento de Diseño Prioritario | Cómo Resuelve su Necesidad en la Interfaz |
| :--- | :--- | :--- |
| **1. Familia Trabajadora** | Wallet clara y contador de ahorro en pesos (\$ MXN) | Visualizan inmediatamente el descuento familiar en barbacoa y antojitos sin trucos ni costos ocultos. |
| **2. Joven Mochilero (Gen Z)** | Cartas Vivas holográficas con microanimaciones fluidas | Satisface el deseo de coleccionismo estético y genera contenido viral listo para compartir en historias de TikTok/Instagram. |
| **3. Turista Cultural** | Visor "Ventana del Tiempo" y lore del Nahual Guía | Ofrece contexto histórico riguroso, citas sobre arquitectura virreinal y memoria comunitaria. |
| **4. Adulto Mayor / Jubilado** | Botones táctiles grandes, alto contraste y código OTP verbal | Evita la frustración con tipografías minúsculas y permite el canje dictando el código verbalmente al panadero sin lidiar con lectores complejos. |

---

## 🎨 4. Guía de Estilos y Sistema de Diseño (Design Tokens)

* **Paleta de Colores Primaria:**
  * Fondo profundo: `#090d16` y `#0f172a` (ahorro de batería en pantallas OLED).
  * Acento de movilidad sustentable: Verde esmeralda `#059669` / `#10b981`.
  * Acento de exploración: Azul ferroviario `#2563eb` y `#38bdf8`.
  * Insignias de Rareza: Legendario `#8b5cf6`, Épico `#ec4899`, Raro `#0284c7`.
* **Tipografía:** Tipografía de sistema nativa sans-serif (`-apple-system`, `Roboto`, `Segoe UI`), optimizada para legibilidad instantánea bajo luz solar directa en andenes y plazas abiertas.
* **Componentes Accesibles:** Altura mínima de zonas táctiles de 44px conforme a las pautas WCAG 2.1 AA.
