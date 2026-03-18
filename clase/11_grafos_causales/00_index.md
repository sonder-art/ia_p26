---
title: "Grafos Causales"
---

# Grafos Causales

> *"Correlation is not causation but it sure is a hint."*
> — Edward Tufte

Hasta ahora hemos aprendido a representar distribuciones de probabilidad con grafos dirigidos y a calcular consultas probabilísticas. Pero hay una pregunta que la probabilidad sola **no puede responder**: **¿qué pasaría si intervenimos?**

La pregunta central de este módulo es: **¿cuál es la diferencia entre observar que algo ocurre y hacer que ocurra?**

## Contenido

| Sección | Tema | Idea clave |
|:------:|------|-----------|
| 11.1 | [Estructuras Causales](01_estructuras_causales.md) | Las tres estructuras (fork, chain, collider) y la paradoja de Simpson |
| 11.2 | [Causalidad y el Operador do](02_do_y_causalidad.md) | Intervenciones, cirugía de grafos, fórmula de ajuste y RCTs |

## Objetivos de aprendizaje

Al terminar este módulo podrás:

1. **Distinguir** entre correlación y causalidad usando grafos dirigidos
2. **Identificar** las tres estructuras causales fundamentales (fork, chain, collider) y su efecto sobre las correlaciones observadas
3. **Explicar** la paradoja de Simpson y resolverla con razonamiento causal
4. **Diferenciar** entre observar $P(Y \mid X)$ e intervenir $P(Y \mid do(X))$
5. **Aplicar** la cirugía de grafos y la fórmula de ajuste para calcular efectos causales
6. **Describir** por qué los experimentos aleatorizados (RCTs) eliminan el sesgo de confusión

## Prerrequisitos

Este módulo asume que ya conoces:

| Concepto | Módulo |
|----------|--------|
| Probabilidad condicional $P(A \mid B)$ | [05 — Probabilidad](../05_probabilidad/06_condicional_marginal.md) |
| Teorema de Bayes | [05 — Probabilidad](../05_probabilidad/08_bayes.md) |
| Regla del producto y de la suma | [05 — Probabilidad](../05_probabilidad/07_reglas_probabilidad.md) |

## Mapa Conceptual

```
"¿Correlación o causalidad?"
         │
         │ "Necesitamos un lenguaje formal"
         │
    ┌────▼──────────────────┐
    │  GRAFOS CAUSALES      │ ← Nodos = variables
    │  (DAGs)               │ ← Flechas = causa directa
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │  TRES ESTRUCTURAS     │
    │  ├─ Fork (confounding)│ ← Causa común crea correlación espuria
    │  ├─ Chain (mediación) │ ← Causa indirecta a través de un mediador
    │  └─ Collider (sesgo)  │ ← Condicionar crea correlación falsa
    └────┬──────────────────┘
         │
         │ "Observar ≠ Intervenir"
         │
    ┌────▼──────────────────┐
    │  OPERADOR do()        │
    │  ├─ Cirugía de grafos │ ← Cortar flechas entrantes
    │  └─ Fórmula de ajuste │ ← P(Y|do(X)) con datos observacionales
    └────┬──────────────────┘
         │
    ┌────▼──────────────────┐
    │  RCT                  │ ← La aleatorización implementa
    │  (Experimento         │    cirugía de grafos físicamente
    │   aleatorizado)       │
    └───────────────────────┘
```

---

**Siguiente:** [Estructuras Causales →](01_estructuras_causales.md)
