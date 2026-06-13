---
title: "Redes Bayesianas"
---

# Redes Bayesianas

> *"Probability theory is nothing but common sense reduced to calculation."*
> — Pierre-Simon Laplace

Las redes Bayesianas son una de las herramientas más poderosas de la inteligencia artificial para razonar bajo incertidumbre. Combinan dos ideas fundamentales: la **teoría de probabilidad** (módulo 05) y los **grafos dirigidos** (que ya conoces de estructuras de datos).

La pregunta central es: **¿cómo representamos y calculamos probabilidades en sistemas con muchas variables interconectadas?**

## Contenido

| Sección | Tema | Idea clave |
|:------:|------|-----------|
| 10.1 | [De Probabilidades a Grafos](01_probabilidad_y_grafos.md) | Factorizar la conjunta usando un grafo dirigido |
| 10.2 | [Queries y Tablas de Probabilidad](02_queries_y_tablas.md) | CPTs, variables ocultas, evidencia y consultas |
| 10.3 | [Inferencia por Enumeración](03_inferencia_fuerza_bruta.md) | Fuerza bruta: sumar sobre todas las combinaciones |
| 10.4 | [Independencia y Markov Blanket](04_independencia_y_markov.md) | Leer independencias del grafo para simplificar |
| 10.5 | [Eliminación de Variables](05_eliminacion_de_variables.md) | Algoritmo eficiente: empujar sumas dentro de productos |

## Objetivos de aprendizaje

Al terminar este módulo podrás:

1. **Traducir** entre una distribución conjunta factorizada y un grafo dirigido (y viceversa)
2. **Especificar** una red Bayesiana completa con su estructura y tablas condicionales (CPTs)
3. **Formular** queries probabilísticos identificando variables de consulta, evidencia y ocultas
4. **Calcular** probabilidades por enumeración (fuerza bruta) y analizar su complejidad
5. **Identificar** independencias condicionales usando las tres estructuras canónicas y d-separación
6. **Aplicar** el algoritmo de eliminación de variables paso a paso

## Prerrequisitos

Este módulo asume que ya conoces:

| Concepto | Módulo |
|----------|--------|
| Probabilidad condicional $P(A \mid B)$ | [05 — Probabilidad](../05_probabilidad/06_condicional_marginal.md) |
| Teorema de Bayes | [05 — Probabilidad](../05_probabilidad/08_bayes.md) |
| Regla del producto y de la suma | [05 — Probabilidad](../05_probabilidad/07_reglas_probabilidad.md) |
| Independencia | [05 — Probabilidad](../05_probabilidad/06_condicional_marginal.md) |

## Mapa Conceptual

```
PROBABILIDAD CONJUNTA P(X₁, X₂, ..., Xₙ)
         │
         │ "Es exponencial... ¿cómo factorizarla?"
         │
    ┌────▼────┐
    │  GRAFO  │ ← Cada nodo = variable
    │  (DAG)  │ ← Cada flecha = dependencia directa
    └────┬────┘
         │
    ┌────▼────────────────┐
    │  TABLAS (CPTs)      │ ← Cada nodo tiene P(nodo | padres)
    │  + ESTRUCTURA       │
    └────┬────────────────┘
         │
         │ "¿Cómo responder preguntas?"
         │
    ┌────▼────────────────┐
    │  INFERENCIA         │
    │  ├─ Enumeración     │ ← Fuerza bruta (exponencial)
    │  └─ Eliminación     │ ← Más eficiente (usa independencias)
    └────┬────────────────┘
         │
    ┌────▼────────────────┐
    │  INDEPENDENCIA       │
    │  ├─ Cadena           │
    │  ├─ Bifurcación      │
    │  └─ Colisionador     │
    │  → d-separación      │
    │  → Markov blanket    │
    └─────────────────────┘
```

---

**Siguiente:** [De Probabilidades a Grafos →](01_probabilidad_y_grafos.md)
