---
title: "Lecturas: Lógica"
---

# Lecturas: Lógica

Material de lectura para el módulo de Lógica.

## Lectura Principal

:::pdf{src="{{ '/03_logica/lecturas_logica.pdf' | url }}" height="800px"}
:::

## Contenido del PDF

El PDF incluye el **Capítulo 7: Logical Agents** de *Artificial Intelligence: A Modern Approach* (Russell & Norvig):

| Sección | Tema | Páginas aprox. |
|---------|------|----------------|
| 7.1 | Knowledge-Based Agents | 210-213 |
| 7.2 | The Wumpus World | 213-218 |
| 7.3 | Logic | 218-222 |
| 7.4 | Propositional Logic: A Very Simple Logic | 222-233 |
| 7.5 | Propositional Theorem Proving | 233-253 |

## Guía de Lectura

### Lectura Esencial (obligatoria)

1. **7.1 Knowledge-Based Agents** — Qué es un agente basado en conocimiento, el ciclo TELL/ASK
2. **7.2 The Wumpus World** — El entorno de ejemplo, PEAS
3. **7.3 Logic** — Sintaxis vs semántica, entailment
4. **7.4 Propositional Logic** — Sintaxis, semántica, tablas de verdad

### Lectura Recomendada

5. **7.5.1-7.5.2** — Inferencia y pruebas, prueba por resolución
6. **7.5.3** — Cláusulas de Horn y forward/backward chaining

### Lectura Opcional (para profundizar)

7. **7.5.4** — Model checking eficiente (DPLL, WalkSAT)
8. **7.6** — Agentes basados en lógica proposicional (si está en tu versión)

## Preguntas para Guiar la Lectura

Mientras lees, intenta responder:

1. ¿Por qué un Simple Reflex Agent no funciona para Wumpus World?
2. ¿Cuál es la diferencia entre sintaxis y semántica?
3. ¿Por qué $P \rightarrow Q$ es verdadero cuando $P$ es falso?
4. ¿Qué significa que una fórmula sea válida vs satisfacible?
5. ¿Por qué es importante la forma CNF?
6. ¿Qué ventaja tienen las cláusulas de Horn?
7. ¿Cómo funciona la resolución y por qué es completa?

## Recursos Adicionales

### Videos

- [Stanford CS221 - Logic](https://www.youtube.com/watch?v=HBxh1xOKq3w) — Introducción a lógica en IA
- [MIT 6.034 - Logic](https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/) — Clase completa de Patrick Winston

### Herramientas

- [SAT Competition](http://www.satcompetition.org/) — Competencia anual de SAT solvers
- [MiniSat](http://minisat.se/) — SAT solver minimalista para aprender
- [Z3 Theorem Prover](https://github.com/Z3Prover/z3) — SMT solver de Microsoft

### Práctica

- [Logic Gym](https://www.logicgym.com/) — Ejercicios interactivos de lógica
- [Wumpus World Simulator](https://github.com/topics/wumpus-world) — Implementaciones para practicar
