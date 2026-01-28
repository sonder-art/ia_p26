---
title: "Probabilidad: Razonamiento bajo Incertidumbre"
---

# Probabilidad: Razonamiento bajo Incertidumbre

¿Cómo razonamos cuando no tenemos certeza absoluta?

## Contenido

| Sección | Tema | Descripción |
|---------|------|-------------|
| [01](01_intro.md) | Introducción | ¿Por qué necesitamos probabilidad? El problema del razonamiento plausible |
| [02](02_robot_desiderata.md) | El Robot Pensante | Los desiderata de Jaynes: qué queremos de un sistema de razonamiento |
| [03](03_probabilidad_como_logica.md) | Probabilidad como Lógica Extendida | La conexión profunda entre lógica y probabilidad |
| [04](04_interpretaciones.md) | Interpretaciones de Probabilidad | Frecuentista vs Bayesiano vs Jaynes |
| [05](05_conceptos_basicos.md) | Conceptos Básicos | Espacio muestral, eventos, medidas de probabilidad |
| [06](06_condicional_marginal.md) | Probabilidad Condicional y Marginal | P(A\|B), marginalización, independencia |
| [07](07_reglas_probabilidad.md) | Las Reglas de Probabilidad | Regla del producto y suma; Jaynes vs Kolmogorov |
| [08](08_bayes.md) | Teorema de Bayes | La joya de la corona: actualización de creencias |
| [09](09_esperanza_momentos.md) | Esperanza y Momentos | Valores esperados, varianza, covarianza |

## Tarea

| [10](10_tarea_probabilidad.md) | Tarea de Probabilidad | Ejercicios de probabilidad, conceptos, y álgebra booleana (20 pts, entrega: 4 feb) |

## Lecturas

- [Lecturas de Probabilidad (PDF)](lecturas_probabilidad.pdf) — E.T. Jaynes, Capítulos 1-2

## Idea Central

> "La teoría de probabilidad no es más que sentido común reducido a cálculo."
> — Pierre-Simon Laplace

En esta sección exploraremos la probabilidad desde la perspectiva de **E.T. Jaynes**, quien argumenta que:

1. La probabilidad es una **extensión de la lógica** para manejar incertidumbre
2. Las reglas de probabilidad no son arbitrarias — son las **únicas** reglas consistentes
3. Toda probabilidad es **condicional** en información de fondo

Este enfoque unifica las visiones "frecuentista" y "bayesiana" bajo un marco más fundamental.

---

## Mapa Conceptual

```
LÓGICA DEDUCTIVA          RAZONAMIENTO PLAUSIBLE
     │                            │
  Certeza                    Incertidumbre
  (T/F)                      (grados 0-1)
     │                            │
     └──────────┬─────────────────┘
                │
        ┌───────▼───────┐
        │  DESIDERATA   │
        │  (requisitos) │
        └───────┬───────┘
                │
        ┌───────▼───────┐
        │   REGLAS DE   │
        │ PROBABILIDAD  │
        └───────┬───────┘
                │
        ┌───────▼───────┐
        │    BAYES      │
        │   THEOREM     │
        └───────────────┘
```

---

**Siguiente:** [Introducción →](01_intro.md)
