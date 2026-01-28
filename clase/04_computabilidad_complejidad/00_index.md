---
title: "Computabilidad y Complejidad"
---

# Computabilidad y Complejidad

Los límites fundamentales de lo que podemos computar y cuán rápido.

## Contenido

1. [Introducción](01_intro.md) — Las tres grandes preguntas
2. [Algoritmos y Máquinas de Turing](02_algoritmos_turing.md) — El modelo fundamental
3. [Computabilidad vs Decidibilidad](03_computabilidad_decidibilidad.md) — ¿Qué podemos resolver?
4. [Límites: El Halting Problem](04_limites_halting.md) — ¿Qué NO podemos resolver?
5. [Gödel y la Conexión](05_godel_conexion.md) — Límites lógicos y computacionales
6. [Complejidad y Big-O](06_complejidad_big_o.md) — ¿Cuán rápido?
7. [Clases: P, NP y BPP](07_p_np_bpp.md) — Jerarquía de dificultad
8. [Síntesis Final](08_sintesis.md) — El mapa completo

## Preguntas Centrales

Este módulo responde tres preguntas fundamentales sobre la computación:

### 1. ¿Qué podemos computar?
**Respuesta:** Todo lo que una Máquina de Turing puede hacer (Church-Turing Thesis)

### 2. ¿Qué NO podemos computar?
**Respuesta:** Hay problemas indecidibles (ej: Halting Problem) e incluso no computables

### 3. ¿Qué tan rápido podemos computar?
**Respuesta:** Depende de la clase de complejidad (P, NP, etc.)

## Conexiones

Este módulo conecta con:
- **Lógica** — Teoremas de Gödel usan ideas similares a Halting
- **SAT (del módulo anterior)** — Es NP-completo, conecta computabilidad con complejidad
- **Agentes** — Define los límites de lo que un agente puede hacer o decidir

## Roadmap Visual

```
¿Qué es computable?
        ↓
Máquinas de Turing (modelo)
        ↓
    ┌───────────────────┐
    │                   │
Computabilidad    Decidibilidad
    │                   │
    └─────────┬─────────┘
              ↓
    ¿Hay límites? → Halting Problem
              ↓
    Gödel: límites lógicos también
              ↓
    De "¿se puede?" a "¿cuán rápido?"
              ↓
        Big-O & Complejidad
              ↓
        P, NP, BPP
              ↓
        P vs NP: el problema del millón
```

## Objetivos de Aprendizaje

Al finalizar este módulo, podrás:

- ✓ Explicar qué es una Máquina de Turing y por qué importa
- ✓ Distinguir entre computabilidad y decidibilidad
- ✓ Demostrar que el Halting Problem es indecidible
- ✓ Conectar los teoremas de Gödel con límites computacionales
- ✓ Usar notación Big-O para analizar algoritmos
- ✓ Clasificar problemas en P, NP o NP-completo
- ✓ Explicar la importancia de P vs NP
- ✓ Entender que hay límites fundamentales en lo que podemos computar

---

**Siguiente:** [Introducción →](01_intro.md)
