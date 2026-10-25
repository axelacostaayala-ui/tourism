# Guardianes del Territorio: App de Turismo Sostenible y Exploración Gamificada

> **Especificación de Producto, Arquitectura Técnica y Mecánicas del MVP**  
> *Proyecto Prototípico de 5to Semestre — Licenciatura en Ciencias de Datos para Negocios (Universidad Rosario Castellanos)*  
> * **Autores:** Kevin Axel Acosta Ayala · Ivan Rafael Mena Fernández  
> * **Fecha de actualización:** 25 de Octubre de 2026

---

## 1. 🎯 Diagnóstico y Problema a Resolver

El turismo en México enfrenta una **falla estructural de distribución**:
* **Hipercentralización y Overtourism:** Un número reducido de enclaves turísticos tradicionales (Cancún/Riviera Maya, CDMX Centro-Roma-Condesa, Los Cabos, Oaxaca Centro, Valle de Bravo) concentran la inversión, el tráfico y los visitantes. Esto genera colapso de servicios públicos, crisis hídricas, gentrificación, encarecimiento del suelo y deterioro ecológico severo.
* **Marginación de Destinos Emergentes:** Cientos de municipios rurales, pueblos mágicos periféricos, cooperativas ecoturísticas y comunidades originarias con un patrimonio cultural, gastronómico y natural de escala mundial permanecen invisibilizados y desprovistos de derrama económica.
* **Falta de Incentivos Reales en Apps Tradicionales:** Aplicaciones como Google Maps, TripAdvisor o Yelp muestran recomendaciones sesgadas por el presupuesto publicitario de grandes cadenas o por la cercanía en automóvil privado, sin ofrecer dinámicas atractivas para dispersar a los viajeros hacia destinos no masivos.

### La Solución: Descentralización Gamificada
Descentralizar el flujo turístico transformando los viajes de fin de semana y vacaciones en una **experiencia de exploración lúdica de colección de personajes (*monster-collecting* estilo Pokémon Go)**, donde el juego premia con mayor valor el descubrimiento de destinos emergentes y recompensa al viajero con **beneficios económicos tangibles en comercios locales afiliados**.

---

## 2. 🎮 Core Gameplay & Ciclo de Usuario (Loop Principal)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           LOOP DE JUEGO PRINCIPAL                               │
└─────────────────────────────────────────────────────────────────────────────────┘
         │
         ▼
[1. Radar de Exploración] ──► Detecta presencia de un "Guardián Dormido" en la zona
         │
         ▼
[2. Misión Territorial]   ──► Recorrer a pie de 1 a 3 Puntos de Interés (POI) comunitarios
         │                    (ej. Mirador natural + Taller de alfarería + Mercado local)
         ▼
[3. Validación Física]    ──► Geofencing (GPS nativo) + Escaneo de Código QR en sitio
         │
         ▼
[4. Despertar del Guardián]► Desbloqueo de Carta Viva 2D coleccionable con microanimación
         │
         ▼
[5. Bendición Económica]  ──► Cupón digital / Descuento para consumir en comercios locales
         │                    (Fondas, artesanos, cooperativas de guías, albergues)
         ▼
[6. Canje en Comercio]    ──► Locatario valida cupón con escáner simple o código OTP (Cero costo)
```

---

## 3. ⚖️ Sistema de Rareza Inversa (Incentivo Algorítmico Clave)

Para lograr el mandato del Problema Prototípico (redistribuir los flujos y mitigar la saturación), la app implementa el **Sistema de Rareza Inversa** gobernado por el **Índice de Saturación Turística (IST)** calculado con Ciencia de Datos:

$$\text{Rareza del Guardián} \propto \frac{1}{\text{Saturación y Concentración de Visitantes}}$$

| Tipo de Destino | Nivel de Saturación | Categoría del Guardián | Características Visuales y Lore | Valor de la Bendición (Recompensa) |
| :--- | :--- | :--- | :--- | :--- |
| **Polo Hiperturístico** (Cancún, Centro Histórico saturado, Santa Fe) | **Alta / Crítica** | **Común / "Fatigado"** | Guardián con energía baja, tonos apagados, diseño estándar. | Descuento simbólico (5% o badge digital básico). |
| **Destino de Transición** (Cabecera municipal, ruta intermedia) | **Moderada** | **Raro** | Guardián activo, detalles artesanales visibles. | 10% - 15% de descuento en comercios seleccionados. |
| **Pueblo Emergente / Comunidad Artesanal** (Pueblos de tule, alfarería) | **Baja** | **Épico** | Diseños vibrantes tipo alebrije, animación fluida, efectos de luz. | 20% - 25% de descuento + acceso a experiencias o degustaciones. |
| **Reserva Ecológica / Destino Comunitario Remoto** (Ciénegas, volcanes) | **Mínima / Ociosa** | **Legendario** | Máximo detalle artístico, microanimación compleja, aura mística, historia profunda. | Recompensa de alto valor: Regalo artesanal directo, taller vivencial gratuito o 30%+ descuento en cooperativas. |

---

## 4. 🧭 Corredores Piloto Propuestos (Fase 1)

Para validar el MVP con un clúster regional delimitado de **3 a 4 municipios contiguos**, con **3 a 4 Guardianes** y **15 comercios afiliados**, se definen dos opciones de alto impacto:

### 🏆 Opción Recomendada A: Corredor "El Insurgente" / Valle de Toluca (Edomex)
Aprovecha directamente la infraestructura de transporte masivo rápido y limpio, y los datos ya estructurados en el repositorio:

| Municipio / Estación | Guardián Piloto | Rareza | Lore Cultural e Inspiración | Puntos de Misión Física (POIs) |
| :--- | :--- | :--- | :--- | :--- |
| **1. Zinacantepec** | **Xinán** *(El Guardián de la Escarcha y el Volcán)* | **Legendario** | Inspirado en el coyote de montaña y las nieves sagradas del Volcán Xinantécatl. | 1. Museo Virreinal de San Miguel.<br>2. Pila Bautismal Monolítica.<br>3. Módulo ecoturístico a faldas del volcán. |
| **2. Metepec** | **Barrotépetl** *(El Espíritu Alfarero)* | **Épico** | Espíritu en forma de quimera alada elaborada en barro policromado (Árbol de la Vida). | 1. Capilla del Calvario (Cerro de los Magueyes).<br>2. Taller de alfarería tradicional.<br>3. Mercado Artesanal Municipal. |
| **3. Lerma** | **Acatl-Tule** *(La Ninfa de los Humedales)* | **Épico** | Criatura acuática entrelazada con juncos y aves migratorias de las Ciénegas de Lerma. | 1. Mirador de aves de las Ciénegas de Lerma.<br>2. Templo de Santa Clara.<br>3. Taller de tejido de tule en San Pedro Tultepec. |
| **4. Toluca Centro** | **Mosco Matlatzinca** | **Raro / Común** | Guardián urbano con alas de vitral inspirado en el Cosmovitral. | 1. Cosmovitral Jardín Botánico.<br>2. Los Portales de Toluca.<br>3. Museo del Alfeñique. |

### Red de 15 Comercios Locales Afiliados Piloto (Corredor El Insurgente)
1. **Zinacantepec:** 
   - *Fonda y Barbacoa El Rinconcito Serrano* (15% descuento en consumo familiar).
   - *Panadería Tradicional San Miguel* (Regalo de pan de fiesta en compra mínima).
   - *Cooperativa Ecoturística Raíces del Xinantécatl* (25% descuento en guía local).
2. **Metepec:**
   - *Taller Artesanal Familia Soteno (Árboles de la Vida)* (15% descuento en pieza de barro).
   - *Bar Tradicional 2 de Abril* (Cata cortesía de "La Garañona").
   - *Café Cultural El Cerrojo* (Bebida de cortesía al ordenar alimento).
   - *Fonda Doña Lupe (Gorditas y tlacoyos)* (10% descuento).
3. **Lerma / San Pedro Tultepec:**
   - *Mueblería y Taller de Tule La Laguna* (20% en cestería artesanal).
   - *Restaurante Rincón Mexiquense* (15% en platillos tradicionales de ciénega).
   - *Antojitos Doña Mary (Mercado Municipal Lerma)* (Descuento en consumo).
   - *Bicicletas y Senderismo Humedales Lerma* (2x1 en renta de bicis).
4. **Toluca Centro:**
   - *Chorizos Tradicionales Los Portales (Verde y Rojo)* (10% en embutidos típicos).
   - *Dulcería y Alfeñiques San José* (Bolsa de dulces típicos de cortesía).
   - *Café El Labrador* (15% descuento).
   - *Librería y Espacio Cultural del Nevado* (10% en libros de arte y mapas locales).

*(Alternativa opcional documentada: Clúster Sierra Norte de Puebla: Zacatlán, Chignahuapan, Cuetzalan y Pahuatlán).*

---

## 5. 🤖 Módulos Innovadores de Inteligencia y Experiencia

### A. Chatbot Inteligente: "El Nahual Guía"
Un asistente conversacional liviano integrado en la app con dos propósitos:
1. **Pistas y Acertijos Gamificados:** En lugar de dar indicaciones GPS frías, el Nahual habla con personalidad mística dando pistas en forma de copla o acertijo sobre cómo encontrar a los Guardianes en los puntos de interés.
2. **Divulgador Cultural y Gastronómico:** Responde dudas en tiempo real sobre la historia del pueblo, qué comer, horarios de talleres artesanales y cómo llegar en transporte público sustentable.

### B. Visor de Memoria Histórica ("La Ventana del Tiempo")
* Función de cámara interactiva con filtro superpuesto ligero (sin requerir renderizado 3D complejo):
* Al enfocar un punto clave (el templo, la plaza cívica o el mirador), la pantalla sobrepone una fotografía de archivo histórico o ilustración de cómo era el lugar hace 80 o 100 años (o durante su fundación originaria), comparándolo con el presente mediante una barra deslizadora (*slider* interactivo).

---

## 6. 📱 Definición Técnica del MVP (Prioridad Alto Impacto / Bajo Costo)

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ARQUITECTURA DEL MVP                            │
└────────────────────────────────────────────────────────────────────────┘

  [CLIENTE MÓVIL]
  • Flutter / React Native (iOS / Android)
  • Motor de Animación 2D: Lottie / Skia / Rive (Cartas Vivas fluidas a 60 fps)
  • Almacenamiento Local: SQLite / Hive (Modo Offline-First)
  • Sensores: GPS nativo (Geofencing) + Escáner de Cámara para QR

         │ Sincronización REST / JSON
         ▼
  [BACKEND & APIS]
  • FastAPI (Python 3.10+) ligero y asíncrono
  • PostgreSQL con extensión PostGIS para consultas geoespaciales
  • API Google Maps: Enlace profundo (Deeplinking) hacia rutas peatonales

         │ Ingesta de Eventos
         ▼
  [PIPELINE ANALÍTICO & CIENCIA DE DATOS]
  • Algoritmo de Rareza Inversa (Cálculo del IST con datos de SECTUR/INEGI)
  • Motor de Recomendación de Rutas (Machine Learning)
  • Simulación Monte Carlo de afluencia comunitaria (Modelos Estocásticos)
  • Optimización de asignación de cupones y pauta (Investigación de Operaciones)
```

### Estrategia Offline-First para Zonas Rurales:
1. El usuario puede pulsar "Descargar Guía de la Región" mientras tiene WiFi o datos en la estación de tren o en su casa.
2. Todo el mapa del clúster, los artes vectoriales de los Guardianes, las pistas y las coordenadas de los POIs quedan guardados en memoria local.
3. La validación GPS + QR no requiere conexión a internet activa.
4. Las bendiciones y logros se registran localmente con una firma criptográfica hash simple y se sincronizan en cuanto el teléfono recupera señal celular.

---

## 7. 🏪 Módulo de Comercio Local (Sin Hardware Costoso)

Para garantizar la adopción de fondas, artesanos y cooperativas sin barreras tecnológicas:
* **Método 1 (QR Dinámico del Usuario):** El usuario muestra la pantalla de su cupón con un código QR que contiene el ID de la bendición y un token de vigencia.
* **Método 2 (Código Alfanumérico OTP de 4 Dígitos):** Para locatarios sin lector de QR, la app muestra un código simple (ej. `BND-4821`). El comerciante solo lo verifica o lo anota en su lista diaria.
* **Portal Locatario Web Ultraligero (PWA):** Una página web accesible desde cualquier celular básico de gama baja donde el comerciante inicia sesión con su número de teléfono y puede ver los cupones canjeados del día y su saldo acumulado de retribución comunitaria.

---

## 8. 📋 Backlog de Producto y Wireframes del Flujo de Usuario

```
[Flujo 1: Radar]       [Flujo 2: Misión POI]      [Flujo 3: Carta 2D]      [Flujo 4: Wallet]
┌────────────────┐     ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│  MAPA / RADAR  │     │ VALIDACIÓN POI │     │  CARTA VIVA 2D │     │   BENDICIÓN    │
│                │     │                │     │                │     │                │
│ [o] Guardián   │────►│ Escanear QR    │────►│  "¡Despierto!" │────►│ Cupón 20% OFF  │
│  a 400m        │     │ en Taller de   │     │  ★ ★ ★ ÉPICO   │     │ Taller Soteno  │
│ [Pista Nahual] │     │ Barro          │     │ (Microanimado) │     │ [Usar Cupón]   │
└────────────────┘     └────────────────┘     └────────────────┘     └────────────────┘
```

### Épicas e Historias de Usuario (Fase 1 - MVP):

#### ÉPICA 1: Exploración Territorial y Radar de Guardianes
* **HU-1.1:** *Como viajero*, quiero ver un mapa estilizado con el radar de mi ubicación para identificar si hay guardianes dormidos a mi alrededor.
* **HU-1.2:** *Como viajero*, quiero recibir pistas temáticas del "Nahual Guía" sobre la ubicación de los puntos de interés para orientar mi recorrido a pie.
* **HU-1.3:** *Como viajero en zona rural sin señal*, quiero que la aplicación funcione en modo offline para no interrumpir mi juego si pierdo conexión celular.

#### ÉPICA 2: Misiones y Validación Antifraude
* **HU-2.1:** *Como viajero*, quiero validar mi visita a un POI escaneando un código QR físico en el sitio para registrar mi avance de misión.
* **HU-2.2:** *Como sistema*, quiero verificar por Geofencing (GPS nativo) que el usuario esté en un radio de 50 metros del POI para evitar capturas fraudulentas a distancia.

#### ÉPICA 3: Colección y Cartas Vivas 2D
* **HU-3.1:** *Como jugador*, quiero desbloquear una Carta Viva 2D animada con los atributos, elemento cultural y rareza del Guardián tras completar la misión.
* **HU-3.2:** *Como coleccionista*, quiero acceder a mi Álbum/Bóveda digital donde pueda consultar todos mis guardianes ordenados por región, rareza y fecha de despertar.

#### ÉPICA 4: Recompensas Comunitarias y Wallet de Bendiciones
* **HU-4.1:** *Como usuario*, quiero recibir un cupón digital asociado al Guardián desbloqueado para canjearlo en negocios locales de la comunidad.
* **HU-4.2:** *Como comerciante local*, quiero un mecanismo simple (código de 4 dígitos o escaneo de pantalla) para validar el descuento del cliente sin requerir terminales ni pagar comisiones bancarias.

#### ÉPICA 5: Experiencia Histórica
* **HU-5.1:** *Como viajero cultural*, quiero activar el visor "Ventana del Tiempo" para comparar la vista actual de un monumento histórico con su fotografía histórica de principios del siglo XX.

---

## 9. 🚀 Roadmap Futuro (Fase 2 - Post-Tracción)
Una vez validada la tracción en el corredor piloto:
1. **Cámara con Realidad Aumentada (AR):** Visualización del Guardián proyectado en el entorno físico mediante ARCore / ARKit.
2. **Filtros para Redes Sociales:** Filtros interactivos en TikTok e Instagram para lucir al Guardián despertado y viralizar las visitas comunitarias.
3. **Torneos Estacionales de Exploración:** Competencias regionales durante puentes vacacionales y festivales tradicionales (ej. Día de Muertos, Festival del Alfeñique).

---

## 10. 🎓 Articulación Estricta con el Problema Prototípico (5to Semestre)

Para cumplir al 100% con la rúbrica de la Universidad Rosario Castellanos, la app es la herramienta central evaluada por las 6 asignaturas:

1. **Big Data:** Arquitectura de ingesta de eventos de jugadores (GPS, escaneos, canjes) y almacenamiento distribuido particionado por región y temporalidad.
2. **Minería de Datos:** Clustering de municipios por potencial turístico y reglas de asociación entre perfiles de jugadores y tipos de comercios visitados.
3. **Machine Learning:** Modelo predictivo del Índice de Saturación Turística (IST) para fijar dinámicamente la rareza de los guardianes y motor de recomendación de misiones.
4. **Modelos Estocásticos:** Simulación Monte Carlo para calcular el impacto de las bendiciones sobre la capacidad de carga de las fondas y talleres locales, evitando desabasto.
5. **Investigación de Operaciones:** Modelo matemático de optimización para la asignación del presupuesto de difusión de la campaña y balanceo óptimo de flujos hacia los comercios.
6. **Mercadotecnia Digital:** Diseño integral de la campaña publicitaria gamificada, embudo de conversión, pauta digital y cuadro de mando de KPIs turísticos, económicos y de reducción de $CO_2$.
