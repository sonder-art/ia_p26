---
title: "Optimización"
---
:::exam{id="EX-05" title="Parcial de Optimización" date="2026-02-23" points="10" duration="20 minutos"}
Examen sobre optimización, incluyendo formulación, paisaje, algoritmos y ejemplos en Python. Todo lo que vimos en el módulo en clase, incluyendo la tarea.
:::
# Optimización

En IA, casi todo se reduce a optimizar: minimizar una pérdida, maximizar una utilidad, encontrar los mejores parámetros. Entrenar una red neuronal es resolver un problema de optimización. Ajustar una regresión es resolver un problema de optimización. Incluso elegir la mejor jugada en un juego puede verse como optimización.

Este módulo enseña el **lenguaje** de la optimización — cómo formular problemas, entender el paisaje de soluciones, y usar herramientas computacionales para resolverlos.

## Convenciones rápidas (notas vs SciPy)

- **Notas (matemáticas)**: solemos escribir desigualdades como \(g(x) \le 0\).
- **SciPy (`minimize`)**: una restricción `"ineq"` significa `fun(x) >= 0`.
- **SciPy (`linprog`, `milp`)**: solo **minimizan**. Si tu problema es de **maximización**, niega el objetivo.
- **No negatividad / cotas**: cuando puedas, ponlas como `bounds` (en lugar de inventar restricciones extra).

## Flujo de trabajo: lee y haz

El módulo alterna entre **lectura** (notas) y **práctica** (notebooks). Sigue este orden:

| Paso | Actividad | Material |
|:----:|-----------|----------|
| 1 | **Lee** 7.1: Formulación + regularización | [Notas](01_formulacion.md) |
| 2 | **Haz** Función objetivo + producción (LP) | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/07_optimization/notebooks/01_formulacion_y_paisaje.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> (formulación + LP) |
| 3 | **Lee** 7.2: Paisaje + convexidad + opt. entera | [Notas](02_paisaje_y_conceptos.md) |
| 4 | **Haz** Visualiza 1D, 2D, cuerdas de convexidad | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/07_optimization/notebooks/01_formulacion_y_paisaje.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> (paisajes + convexidad) |
| 5 | **Lee** 7.3: GD + convergencia + SGD | [Notas](03_algoritmos.md) (primera mitad) |
| 6 | **Haz** GD, learning rates, SGD vs batch | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/07_optimization/notebooks/02_algoritmos_y_codigo.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> (GD + SGD) |
| 7 | **Lee** 7.3: Newton/BFGS + Lagrange + Simplex | [Notas](03_algoritmos.md) (segunda mitad) |
| 8 | **Haz** Rosenbrock vs L-BFGS-B, Lagrange, `linprog` | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/07_optimization/notebooks/02_algoritmos_y_codigo.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> (2º orden + restricciones + LP) |
| 9 | **Lee** 7.3: IP + SA + GA + comparación | [Notas](03_algoritmos.md) (tercio final) |
| 10 | **Haz** IP/MIP, SA, GA, comparación | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/07_optimization/notebooks/02_algoritmos_y_codigo.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> (entera + metaheurísticas) |
| 11 | **Lee** 7.4: scipy reference + autodiff | [Notas](04_ejemplos_python.md) |
| 12 | **Haz** Autodiff + capstone | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/07_optimization/notebooks/02_algoritmos_y_codigo.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> (autodiff + cierre) |

## Materiales

| Tipo | Archivo | Descripción |
|:----:|---------|-------------|
| Notas | [7.1 Formulación](01_formulacion.md) | Objetivo, variables, restricciones, regularización |
| Notas | [7.2 Paisaje y conceptos](02_paisaje_y_conceptos.md) | Mínimos, puntos silla, convexidad, opt. entera |
| Notas | [7.3 Algoritmos](03_algoritmos.md) | GD, SGD, Newton, Lagrange, simplex, SA, GA, comparación |
| Notas | [7.4 scipy reference](04_ejemplos_python.md) | Cheat sheet de scipy.optimize (8 patrones) + autodiff |
| Notebook | [NB1: Formulación y paisaje](notebooks/01_formulacion_y_paisaje.ipynb) | Interactivo: formula y visualiza |
| Notebook | [NB2: Algoritmos y código](notebooks/02_algoritmos_y_codigo.ipynb) | Interactivo: GD, SGD, scipy, LP, autodiff |
| Tarea | [NB3: Tarea optimización](notebooks/03_tarea_optimizacion.ipynb) | 5 problemas (LP, QP, IP, black-box, MIP) — 20 pts, entrega 23 feb |
| Lab | [lab_optimization.py](lab_optimization.py) | Genera todas las visualizaciones |

## Cómo correr el lab (para imágenes)

```bash
cd clase/07_optimization
python lab_optimization.py
```

## Objetivos de aprendizaje

Al terminar este módulo podrás:

1. **Formular** un problema de optimización: identificar objetivo $f(x)$, variables de decisión $x$, y restricciones.
2. **Distinguir** entre mínimos locales, globales, puntos silla, y entender por qué importa.
3. **Explicar** qué es convexidad y por qué simplifica la optimización ("todo mínimo local es global").
4. **Describir** intuitivamente cómo funcionan descenso de gradiente, SGD, métodos de segundo orden, multiplicadores de Lagrange y el método simplex.
5. **Resolver** problemas de optimización en Python usando `scipy.optimize`.
6. **Conectar** estos conceptos con el entrenamiento de modelos de ML (regularización, autodiff, SGD/Adam).
7. **Decidir** qué algoritmo usar según las propiedades del problema (gradiente, convexidad, discreto).
8. **Implementar** metaheurísticas (SA, GA) para funciones sin gradiente.

---

**Siguiente:** [Formulación matemática →](01_formulacion.md)
