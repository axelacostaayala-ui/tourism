# Estrategia de Campaña Publicitaria y Mix de Medios
## Proyecto: Guardianes del Territorio (Turismo Sostenible y Gamificación)
**Licenciatura en Ciencias de Datos para Negocios — 5to Semestre (Universidad Rosario Castellanos)**  
**UCA:** Mercadotecnia Digital e Investigación de Operaciones  
**Responsable:** Integrante 3 (Product & Growth / Marketing Lead)

---

## 🎯 1. Concepto Creativo Central

> **"Despierta a los Guardianes: Tu Tren a las Leyendas Vivas"**

La campaña busca transformar la percepción del viaje en el Tren Interurbano "El Insurgente", pasando de un simple medio de transporte suburbano a una **puerta de entrada a una aventura cultural gamificada en el mundo real**. 

A diferencia de las campañas turísticas convencionales que promocionan fotos genéricas de monumentos, nuestra narrativa posiciona al viajero como un **explorador activo** que rescata la memoria y apoya directamente a los guardianes humanos del territorio: artesanos, cocineras tradicionales y cuidadores ambientales.

---

## 💰 2. Presupuesto Óptimo y Mix de Canales (Articulación con I.O.)

La asignación del presupuesto trimestral de **$250,000.00 MXN** está matemáticamente optimizada por el modelo de Programación Lineal de Investigación de Operaciones (`notebooks/05_optimizacion_io/01_optimizacion_presupuesto_y_flujos.py`) para maximizar la derrama en destinos emergentes respetando la capacidad de carga de las fondas y talleres:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               DISTRIBUCIÓN DEL PRESUPUESTO PUBLICITARIO ($250,000 MXN)                 │
└────────────────────────────────────────────────────────────────────────────────────────┘

 [CAN-01] TikTok & Instagram Reels ──► 38% ($95,000 MXN)  ──► Gen Z & Jóvenes Mochileros
 [CAN-03] Señalética en Andenes    ──► 32% ($80,000 MXN)  ──► Familias & Adultos Mayores
 [CAN-04] Micro-influencers Locales ──► 18% ($45,000 MXN) ──► Audiencia Multisegmento
 [CAN-02] Google Search & Maps      ──► 12% ($30,000 MXN) ──► Turistas Culturales (Alta Intención)
```

### Métricas de Costo y Conversión Proyectadas por Canal:
| Canal Publicitario | Inversión Trimestral | CAC Efectivo Promedio | Visitantes Estimados con Canje | Derrama Directa Generada | Retorno de Inversión Social (S-ROI) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **CAN-01: TikTok & Reels** | $95,000 MXN | $16.50 MXN | ~5,750 jóvenes | $1,265,000 MXN | 13.3x |
| **CAN-03: Andenes Tren** | $80,000 MXN | $14.20 MXN | ~5,630 familias/adultos | $1,745,000 MXN | 21.8x |
| **CAN-04: Micro-influencers**| $45,000 MXN | $18.80 MXN | ~2,390 exploradores | $693,000 MXN | 15.4x |
| **CAN-02: Google Search** | $30,000 MXN | $22.40 MXN | ~1,340 culturales | $562,000 MXN | 18.7x |
| **Totales Consolidados** | **$250,000 MXN** | **$16.53 MXN** | **~15,110 visitantes** | **$4,265,000 MXN** | **17.1x de Derrama Neta** |

---

## 🔄 3. Embudo de Conversión (Funnel de Mercadotecnia)

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                           EMBUDO DE CONVERSIÓN INTEGRADO                                │
└─────────────────────────────────────────────────────────────────────────────────────────┘
  ▼
[TOFU: Descubrimiento / Atracción]
  • Contenido viral en TikTok/Reels ("Cosas que no sabías que podías hacer en tren").
  • Mupis y tótems luminosos en andenes de Observatorio y Santa Fe.
  • Métrica: Alcance (3.2M impresiones) y CTR (> 2.8%).
  ▼
[MOFU: Interés y Consideración]
  • Descarga de la app en estaciones vía WiFi libre o QR directo.
  • Apertura del mapa y consulta de las pistas líricas de "El Nahual Guía".
  • Métrica: Tasa de instalación (Install Rate > 18%) y activación de geolocalización.
  ▼
[BOFU: Acción Territorial y Retención]
  • Descenso en estaciones emergentes (Zinacantepec, Metepec, Lerma).
  • Escaneo de código QR en monumentos/talleres y despertar de la Carta Viva 2D.
  • Canje del cupón (Bendición) mediante código OTP en las 15 fondas y cooperativas.
  • Métrica: Tasa de canje de cupones (> 35% de jugadores activos) y ticket de ahorro.
```

---

## 📅 4. Calendario de Despliegue por Temporadas

1. **Fase 1: Temporada Valle (Septiembre – Octubre):**  
   * Enfoque: Activación con bono de desestacionalización ($\theta = 1.30$). Pauta agresiva en universitarios (CAN-01) y adultos mayores (CAN-03) entre semana y fines de semana para reactivar la ocupación ociosa en comercios tradicionales.
2. **Fase 2: Temporada Media (Mayo – Junio):**  
   * Enfoque: Difusión hacia familias trabajadoras antes del receso escolar, destacando las Ciénegas de Lerma y los talleres de barro de Metepec como opciones recreativas de proximidad.
3. **Fase 3: Temporada Alta Controlada (Noviembre – Diciembre):**  
   * Enfoque: Regulación de aforos y derivación inteligente mediante **Rareza Inversa**. La app orienta a los turistas hacia Zinacantepec (*Xinán*) para evitar la congestión en Toluca Centro durante la Feria del Alfeñique y compras decembrinas.
