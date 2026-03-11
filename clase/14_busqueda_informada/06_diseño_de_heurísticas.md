---
title: "Diseño de heurísticas"
---

| Notebook | Colab |
|---------|:-----:|
| Notebook 02 — Búsqueda informada (Greedy, Dijkstra, A\*) | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/14_busqueda_informada/notebooks/02_busqueda_informada.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |
| Notebook 04 — Puzzle de 8 piezas (aplicación) | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/14_busqueda_informada/notebooks/aplicaciones/04_puzzle_8.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |

---

# Diseño de heurísticas: la ingeniería detrás de A\*

> *\"The quality of the heuristic determines the efficiency of A\*.\"*

---

Sabemos que A\* es óptimo con heurísticas admisibles. Pero ¿cómo se **diseña** una heurística admisible? Y una vez que tienes varias opciones, ¿cuál elegir? Este capítulo responde ambas preguntas con técnicas sistemáticas.

---

## 1. La técnica del problema relajado

La forma más rigurosa de construir heurísticas admisibles es el **método del problema relajado**: eliminar restricciones del problema original hasta obtener un problema más fácil cuya solución óptima es calculable de forma exacta o aproximada.

El resultado es automáticamente admisible porque:

$$h_{\text{relajado}}(n) = h^{∗}_{\text{relajado}}(n) \leq h^{∗}(n)$$

Al relajar restricciones, el costo óptimo en el problema relajado nunca puede ser mayor que en el original — hay más caminos disponibles en el relajado.

:::example{title="Problema relajado: el puzzle de 8 piezas"}
El puzzle de 8 piezas es un tablero de 3×3 con fichas numeradas 1-8 y un espacio vacío. Un movimiento: mover una ficha adyacente al espacio vacío.

**Reglas del problema original:**
1. Solo puedes mover fichas adyacentes al espacio vacío.
2. Solo puedes mover al espacio vacío (no a fichas ocupadas).
3. Solo puedes mover una ficha a la vez.

**Relajación 1**: eliminar restricción (1) — las fichas pueden moverse a cualquier posición adyacente, no solo al espacio.

→ En el problema relajado, el costo mínimo para llevar cada ficha a su lugar es exactamente 1 si ya está adyacente a su destino, o más si no. La suma de movimientos mínimos de cada ficha es la **distancia Manhattan** (suma de distancias en fila y columna). Resultado: $h_{\text{Manhattan}}(n) = \sum_i |r_i - r_i^{∗}| + |c_i - c_i^{∗}|$

**Relajación 2**: eliminar restricciones (1) y (2) — cada ficha puede teletransportarse a su posición final en un paso.

→ Solo cuenta cuántas fichas no están en su lugar. Resultado: $h_{\text{misplaced}}(n) = \#\text{ fichas fuera de posición}$
:::

La relajación 1 es estrictamente mejor que la 2 (lo veremos en sección 3), pero ambas son admisibles y se derivan sistemáticamente del mismo principio.

---

## 2. Las dos heurísticas del puzzle de 8 piezas

### Heurística 1: fichas fuera de lugar

$$h_1(n) = \text{número de fichas que no están en su posición final}$$

```
Estado actual:     Estado meta:
  7 2 4              1 2 3
  5 _ 6              4 5 6
  8 3 1              7 8 _

Fichas fuera de lugar: 7, 4, 5, 6, 8, 3, 1 → h1 = 7
(la ficha 2 ya está en su lugar)
```

- **Admisible**: cada ficha descolocada necesita al menos un movimiento.
- **Consistente**: mover una ficha cambia el recuento en ±1 ≤ costo del movimiento (que es 1).

### Heurística 2: distancia Manhattan

$$h_2(n) = \sum_{i=1}^{8} \left( |r_i - r_i^{∗}| + |c_i - c_i^{∗}| \right)$$

```
Estado actual:     Estado meta:
  7 2 4              1 2 3
  5 _ 6              4 5 6
  8 3 1              7 8 _

Manhattan por ficha:
  Ficha 7: (0,0)→(2,0): |0-2|+|0-0| = 2
  Ficha 2: (0,1)→(0,1): 0 (en su lugar)
  Ficha 4: (0,2)→(1,0): |0-1|+|2-0| = 3
  Ficha 5: (1,0)→(1,1): 1
  Ficha 6: (1,2)→(1,2): 0
  Ficha 8: (2,0)→(2,1): 1
  Ficha 3: (2,1)→(0,2): 2+1 = 3
  Ficha 1: (2,2)→(0,0): 2+2 = 4

h2 = 2+0+3+1+0+1+3+4 = 14
```

- **Admisible**: en el problema original, cada movimiento avanza una ficha como máximo 1 casilla en Manhattan; llegar a su destino requiere al menos la distancia Manhattan de pasos.
- **Consistente**: cada movimiento cambia la suma Manhattan en ±1 ≤ costo del movimiento.

**Comparación**: $h_2 = 14 > h_1 = 7$ para el mismo estado. $h_2$ domina a $h_1$.

![Efecto de la calidad de la heurística en el puzzle de 8 piezas]({{ '/14_busqueda_informada/images/08_heuristic_quality_effect.png' | url }})

---

## 3. Dominancia: elegir la heurística más informativa

Una heurística $h_a$ **domina** a $h_b$ si $h_a(n) \geq h_b(n)$ para todo $n$, con al menos alguna desigualdad estricta, y ambas son admisibles.

**Si $h_a$ domina a $h_b$, siempre es mejor usar $h_a$.**

Demostración: si $h_a(n) \geq h_b(n)$ para todo $n$, entonces cualquier nodo que A\* expande con $h_a$ también lo expande con $h_b$, pero no al revés. A\* con $h_a$ nunca explora más nodos, y típicamente explora muchos menos.

En el puzzle de 8 piezas:

| Heurística | Promedio de nodos expandidos (profundidad 20) |
|---|:---:|
| $h_1$ (fichas fuera de lugar) | ~73.000 |
| $h_2$ (Manhattan) | ~1.200 |
| $h_3$ (lineal conflict, ver abajo) | ~500 |

La diferencia es de 2 órdenes de magnitud — con la misma garantía de optimalidad.

---

## 4. El truco del máximo

Si tienes múltiples heurísticas admisibles $h_1, h_2, \ldots, h_k$ y ninguna domina completamente a las demás, puedes combinarlas:

$$h(n) = \max(h_1(n), h_2(n), \ldots, h_k(n))$$

Esta heurística combinada es:
- **Admisible**: el máximo de subestimaciones es también una subestimación.
- **No peor que ninguna individual**: domina a cada $h_i$ por definición del máximo.
- **Fácil de implementar**: solo calcula todas y toma el mayor.

:::example{title="Truco del máximo en el puzzle de 8 piezas"}
Para el estado del ejemplo anterior:
$$h(n) = \max(h_1=7, h_2=14) = 14$$

La heurística combinada es automáticamente tan buena como la mejor heurística individual, en cualquier estado.
:::

El costo adicional es calcular todas las heurísticas en cada estado — que a menudo vale la pena si las heurísticas son rápidas de calcular pero informativas.

---

## 5. Más allá de Manhattan: conflicto lineal

La **heurística de conflicto lineal** mejora Manhattan considerando fichas que están en la fila o columna correcta pero en orden incorrecto.

```
Estado:    1 3 2  ←  fila meta
Meta:      1 2 3

Las fichas 3 y 2 están en la fila correcta pero en orden invertido.
Para ordenarlas, una debe salir de la fila, hacer movimientos verticales, y regresar.
Costo adicional mínimo: 2 movimientos.

h_LC(n) = h_Manhattan(n) + 2 × (número de conflictos lineales)
```

Esta heurística sigue siendo admisible (los 2 movimientos adicionales son un mínimo real) y reduce significativamente los nodos expandidos.

---

## 6. Bases de datos de patrones

Para problemas más grandes (como el puzzle de 15 piezas), incluso Manhattan es insuficiente. La técnica de **bases de datos de patrones** (pattern databases) precomputa el costo óptimo para resolver subproblemas.

**Idea**: resolver el subproblema de solo las fichas 1-4 desde cualquier configuración. Almacenar estos costos en una tabla. Al buscar, consultar la tabla — el costo del subproblema es una heurística admisible para el problema completo (resolver el subconjunto no puede ser más caro que resolverlo todo).

| Técnica | Espacio precomputado | Calidad de $h$ |
|---|---|---|
| Manhattan | 0 (fórmula directa) | Buena |
| Conflicto lineal | 0 (fórmula directa) | Mejor |
| Pattern DB (fichas 1-7) | ~$10^6$ entradas | Excelente |
| Pattern DB (fichas 1-15) | ~$10^{10}$ entradas | Perfecta para el subprob. |

El tradeoff: más memoria precomputada → mejor heurística → menos expansiones en tiempo de búsqueda.

![Problema relajado en el puzzle de 8 piezas]({{ '/14_busqueda_informada/images/09_relaxed_problem_8puzzle.png' | url }})

---

## 7. El tradeoff cómputo-expansión

Cada evaluación de $h$ tiene un costo computacional. No sirve de nada tener una heurística perfecta si calcularla tarda más que expandir todos los nodos.

El criterio de decisión:

$$\text{usar } h \text{ si: } \underbrace{\text{ahorro en expansiones} \times \text{costo por expansión}}_{\text{ahorro total}} > \underbrace{\text{costo extra por evaluar } h}_{\text{costo extra}}$$

**Regla práctica**:
- Heurísticas de fórmula cerrada (Manhattan, Euclidiana): coste $O(1)$ → casi siempre vale la pena.
- Heurísticas iterativas (resolver un subproblema en línea): puede que no valga la pena.
- Pattern databases: el costo de consulta es $O(1)$ (lookup en tabla) → muy eficiente una vez precomputadas.

---

## 8. Cómo diseñar tu propia heurística

Para cualquier problema nuevo, sigue estos pasos:

1. **Identifica las restricciones** que hacen difícil el problema (adyacencia, capacidad, orden...).
2. **Elimina algunas** para obtener un problema más fácil pero relacionado.
3. **Calcula el costo óptimo en el problema relajado** — esa es tu heurística.
4. **Verifica admisibilidad**: ¿el costo del problema relajado es siempre ≤ costo del original?
5. **Compara con otras heurísticas**: usa el truco del máximo o elige la dominante.
6. **Mide** el factor de ramificación efectivo $b^{∗}$ en instancias representativas.

:::example{title="Diseño de heurística: problema del viajante (TSP)"}
Problema: visitar $n$ ciudades con costo mínimo.

**Restricción original**: cada ciudad exactamente una vez, formar un ciclo.

**Relajación**: eliminar la restricción de que sea un ciclo → solo exigir que sea un árbol que conecte todas las ciudades.

**Resultado**: el **árbol de expansión mínimo** (MST) de las ciudades no visitadas es una heurística admisible — un tour siempre tiene costo ≥ MST de las ciudades (porque el tour es un grafo más restringido que un árbol).

Esta heurística hace que A\* sea competitivo en instancias medianas de TSP.
:::

---

## 9. Resumen: propiedades y técnicas

| Propiedad / Técnica | Descripción | Garantía |
|---|---|---|
| **Admisibilidad** $h \leq h^{∗}$ | Nunca sobreestima | A\* es óptimo |
| **Consistencia** $h(n) \leq c + h(n')$ | Desigualdad triangular | No reapertura de nodos |
| **Problema relajado** | Eliminar restricciones | Heurística admisible automática |
| **Dominancia** $h_a \geq h_b$ | Siempre preferir $h_a$ | Nunca más expansiones |
| **Truco del máximo** $\max(h_1, h_2, \ldots)$ | Combinar heurísticas | Domina a todas las individuales |
| **Pattern databases** | Subproblemas precomputados | Heurísticas muy informativas |

> **Mensaje central**: la búsqueda informada es tan buena como la heurística que se usa. Invertir tiempo en diseñar una buena heurística puede reducir el tiempo de búsqueda en órdenes de magnitud — con la misma garantía de optimalidad.

---

**Siguiente:** [Branch & Bound e IDA\* →](07_branch_and_bound_e_ida_estrella.md)
