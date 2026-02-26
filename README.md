# churn-3001e-mvp

MVP de predicción de churn orientado a operación: pipeline reproducible + ranking Top-N (N=10/25) + explicabilidad (SHAP).
Proyecto de innovación (Maestría en Inteligencia Artificial, UNIR).

**Equipo 3001E:**  
- JP: René Javier Pereira Moreno  
- RV: Ramón González Vázquez  
- JZ: José Ángel Zúniga Turcios  

## Contexto y enfoque
El churn en servicios de suscripción reduce ingresos y exige acciones preventivas. Este proyecto propone pasar de retención reactiva a preventiva mediante un ranking Top-N basado en riesgo de churn, con explicaciones por cliente usando SHAP.

**Dataset de validación (reproducibilidad):** Telco Customer Churn (Blastchar, 2018).  
**Contexto real (requisitos/interfaz objetivo):** NOVANET (sin integración productiva en este MVP).

## Objetivo del MVP
- Estimar probabilidad de churn por cliente.
- Generar ranking priorizado Top-N alineado a capacidad operativa (N=10 y N=25).
- Reportar métricas operativas: Recall@N y Precision@N / Lift@N.
- Entregar explicaciones globales y locales (SHAP) para soporte a decisiones.
- Exportar resultados en formatos operativos (CSV/Excel).

## Alcance y no-alcance
**Incluye:** pipeline reproducible, control de data leakage, baseline por reglas, modelo ML, métricas Top-N, SHAP y exportación.  
**No incluye (trabajo futuro):** integración con CRM/dashboard, automatización productiva, NLP en tickets/WhatsApp, señales QoS avanzadas.

## Estructura del repositorio
- `/data/` datos (no subir datos sensibles)
- `/notebooks/` notebooks del pipeline end-to-end
- `/src/` utilidades (métricas, helpers, exportación)
- `/outputs/` ranking Top-N (CSV/Excel), métricas y figuras
- `/docs/` bitácora Lean, evidencia, decisiones por sprint

## Cómo ejecutar (reproducible)
1. Recomendado: Python 3.10.
2. Instalar dependencias:
   - `pip install -r requirements.txt`
3. Ejecutar notebooks en `/notebooks/` en el orden definido (S1→S4).

## Salidas esperadas
- `outputs/topN_N10.csv` / `outputs/topN_N25.csv` (o Excel equivalente).
- Tabla de métricas: Recall@10/25 y Precision/Lift@10/25.
- Figuras SHAP: global (importancia) + local (explicación por cliente Top-N).

## Trazabilidad con Jira (Scrum + Lean aplicado)
Las historias PB-01…PB-12 se gestionan en Jira (proyecto **Churn-3001E**).  
Cada historia se evidencia con: enlaces a commits, notebooks/artefactos y registro en bitácora Lean (Build-Measure-Learn) por sprint.
