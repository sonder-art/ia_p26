---
title: "¿Qué es planificar?"
---

| Notebook | Colab |
|---------|:-----:|
| Notebook 01 — STRIPS y estados | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/16_planificacion_clasica/notebooks/01_strips_y_estados.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |

---

# ¿Qué es planificar?

> *"Plans are worthless, but planning is everything."*
> — Dwight D. Eisenhower

---

## 1. Intuición: la mudanza

Imagina que te mudas de departamento.

**En búsqueda (módulo 13)**, alguien te entrega un mapa de la ciudad con todas las calles dibujadas. Tu trabajo es encontrar la ruta más corta del departamento viejo al nuevo. El mapa ya existe — los nodos (esquinas) y las aristas (calles) están dados. Solo tienes que recorrerlo.

**En planificación**, nadie te da un mapa. En su lugar tienes:

- Una descripción de **dónde estás ahora**: cajas sin empacar, muebles en el departamento viejo, camión vacío estacionado afuera.
- Una descripción de **dónde quieres terminar**: cajas en el departamento nuevo, muebles colocados, departamento viejo vacío, llaves devueltas.
- Una lista de **cosas que puedes hacer**: empacar una caja, cargar una caja al camión, manejar el camión al nuevo departamento, descargar, acomodar muebles, devolver llaves…

Tu trabajo es combinar esas acciones en un **plan** — una secuencia ordenada que te lleve del estado actual al estado meta. Nadie te dice cuántas acciones necesitas ni en qué orden van. Tú "construyes el mapa" razonando: *¿qué puedo hacer ahora? ¿qué cambia si lo hago? ¿me acerca a la meta?*

---

## 2. La diferencia fundamental

En los módulos 13 y 14, el **espacio de estados es explícito**: te dan un grafo con nodos y aristas. En el módulo 15, el espacio de estados también es explícito — es el árbol de juego, donde cada nodo es una configuración del tablero.

En planificación, el **espacio de estados es implícito**. No te dan los nodos ni las aristas. Te dan:

1. Un **lenguaje para describir estados** — conjuntos de proposiciones (hechos verdaderos sobre el mundo).
2. Un **lenguaje para describir acciones** — esquemas con precondiciones y efectos que generan nuevos estados.

El algoritmo de búsqueda **genera** el grafo conforme explora, aplicando acciones cuyos precondiciones se cumplen en el estado actual.

| | Búsqueda (módulos 13–14) | Adversarial (módulo 15) | Planificación (módulo 16) |
|---|---|---|---|
| **Estados** | Nodos explícitos del grafo | Configuraciones del juego | **Conjuntos de proposiciones** |
| **Transiciones** | Aristas del grafo | Turnos + acciones del juego | **Acciones STRIPS** (precondiciones → efectos) |
| **Grafo** | Dado de antemano | Dado (árbol de juego) | **Generado** conforme se busca |
| **Meta** | Un estado específico | Ganar el juego | **Subconjunto de proposiciones** (estado parcial) |
| **Algoritmo** | BFS / DFS / A* | Minimax / alpha-beta | **BFS / DFS / A*  (¡el mismo!)** |

![Búsqueda vs Planificación]({{ '/16_planificacion_clasica/images/01_search_vs_planning.png' | url }})

**Cómo leer la figura:**

- **Panel izquierdo** (Búsqueda): un grafo completo con todos sus nodos y aristas dibujados. El algoritmo solo necesita recorrerlo.
- **Panel derecho** (Planificación): algunos nodos ya fueron descubiertos (verde); otros aún son "?" — no existen hasta que una acción STRIPS los genere. Las aristas se crean cuando una acción es aplicable.

---

## 3. La observación clave

> **Planificación hacia adelante (forward planning) ES `GENERIC-SEARCH` del módulo 13.**

El algoritmo es literalmente el mismo: frontera, conjunto explorado, mapa de padres, bucle principal. Solo cambian **tres líneas**:

| Cambio | En `GENERIC-SEARCH` (mod 13) | En `FORWARD-PLANNING` (mod 16) |
|:------:|---|---|
| **[D1]** Meta | `problema.es_meta(n)` | `problema.meta ⊆ s` — la meta es un *subconjunto* de proposiciones |
| **[D2]** Vecinos | `problema.vecinos(n)` | `aplicables(s)` — acciones cuyas precondiciones se cumplen |
| **[D3]** Transición | implícita (seguir arista) | `aplicar(s, a)` — quitar lista delete, agregar lista add |

Todo lo demás — la frontera, el conjunto explorado, el bucle `while frontera ≠ ∅`, la reconstrucción del camino — es **idéntico**. Desarrollaremos esto en detalle en la sección 3.

---

## 4. ¿Por qué necesitamos un lenguaje nuevo?

¿Por qué no simplemente enumerar todos los estados posibles y construir el grafo explícitamente?

Porque la enumeración explota. Considera un robot que puede estar en 10 habitaciones, con 5 objetos que pueden estar en cualquier habitación o en la mano del robot. El número de estados posibles es del orden de $10 \times 11^5 \approx 1{,}600{,}000$. Con 50 objetos: $10 \times 11^{50} \approx 10^{52}$. Enumerar esos estados es imposible.

El lenguaje de proposiciones y acciones permite describir esos $10^{52}$ estados **de forma compacta**: un conjunto de hechos verdaderos. Y las acciones STRIPS permiten generar transiciones **bajo demanda**: solo calculas los vecinos de un estado cuando lo necesitas.

---

## 5. El ejemplo que usaremos: Blocks World

Para entender planificación necesitamos un ejemplo concreto que sea lo suficientemente pequeño para trazar completamente y lo suficientemente rico para mostrar los conceptos. Usaremos **Blocks World** (mundo de bloques) con tres bloques: **A**, **B** y **C**.

### Las reglas

- Hay una **mesa** y **tres bloques** etiquetados A, B, C.
- Cada bloque puede estar **sobre la mesa** o **sobre otro bloque**.
- Solo puedes mover un bloque si **no tiene nada encima** (está "clear").
- La mesa puede sostener cualquier cantidad de bloques simultáneamente.
- Solo puedes mover **un bloque a la vez**.

### Estado inicial y estado meta

![Blocks World: estado inicial y meta]({{ '/16_planificacion_clasica/images/02_blocks_world_initial_goal.png' | url }})

**Estado inicial** — los tres bloques están sobre la mesa, sin ninguno apilado:

```
 ┌───┐  ┌───┐  ┌───┐
 │ A │  │ B │  │ C │
 ═════  ═════  ═════
 mesa   mesa   mesa
```

Escrito como conjunto de proposiciones:

$$\{\ \text{On}(A, \text{Mesa}),\ \text{On}(B, \text{Mesa}),\ \text{On}(C, \text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B),\ \text{Clear}(C)\ \}$$

Cada proposición es un **hecho verdadero** sobre el mundo:
- $\text{On}(A, \text{Mesa})$: "el bloque A está sobre la mesa"
- $\text{Clear}(A)$: "no hay nada encima del bloque A"

**Estado meta** — los tres bloques apilados A sobre B sobre C sobre la mesa:

```
 ┌───┐
 │ A │
 ├───┤
 │ B │
 ├───┤
 │ C │
 ═════
 mesa
```

Escrito como conjunto de proposiciones:

$$\{\ \text{On}(A, B),\ \text{On}(B, C),\ \text{On}(C, \text{Mesa}),\ \text{Clear}(A)\ \}$$

Observa que la meta **no** especifica todo el estado — solo las proposiciones que nos importan. Un estado satisface la meta si **contiene** todas las proposiciones de la meta (puede contener más). Esta es la diferencia [D1]: en búsqueda la meta es *un* estado; en planificación es un *subconjunto* de proposiciones.

### ¿Cuántos estados tiene este problema?

Con solo 3 bloques, el espacio de estados tiene aproximadamente **13 estados alcanzables**. Es lo suficientemente pequeño para dibujarlo completo — lo haremos en la siguiente sección. Es el análogo del árbol de Nim(1,2) con 12 nodos del módulo 15: pequeño para trazar, grande para ser no trivial.

---

**Siguiente:** [STRIPS →](02_strips.md)
