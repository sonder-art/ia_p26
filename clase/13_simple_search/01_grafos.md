---
title: "Grafos: fundamentos"
---

| Notebook | Colab |
|---------|:-----:|
| Notebook 01 — Grafos (práctica de esta sección) | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/13_simple_search/notebooks/01_grafos.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |

---

# Grafos: fundamentos

> *"A mathematician, like a painter or a poet, is a maker of patterns."*
> — G. H. Hardy

---

Los grafos son una de las estructuras más poderosas y ubicuas en ciencias de la computación. Modelan redes sociales, mapas de carreteras, circuitos eléctricos, relaciones en bases de datos, y — como veremos en el módulo — el espacio de posibles acciones de un agente inteligente.

Este capítulo construye el vocabulario formal que necesitamos para hablar con precisión sobre grafos. Nada aquí es difícil; lo importante es que los conceptos queden claros antes de usarlos en algoritmos.

---

## 1. Definición formal

Un **grafo** $G$ es un par $G = (V, E)$ donde:

- $V$ es un conjunto finito de **vértices** (o nodos).
- $E$ es un conjunto de **aristas** (o arcos).

Cómo se definen las aristas depende del tipo de grafo.

---

## 2. Grafos no dirigidos y dirigidos

### Grafo no dirigido

Las aristas son **pares no ordenados** de vértices: $\{u, v\}$ donde $u \neq v$. La arista $\{u, v\}$ y la arista $\{v, u\}$ son la misma arista — la relación es simétrica.

**Ejemplo:** una red de carreteras entre ciudades, donde puedes ir y venir por el mismo camino.

### Grafo dirigido (digrafo)

Las aristas son **pares ordenados**: $(u, v)$. Aquí $(u, v)$ y $(v, u)$ son aristas distintas. Llamamos **arco** a cada par ordenado. La dirección importa.

**Ejemplo:** páginas web con hipervínculos — una página puede enlazar a otra sin que el enlace sea recíproco.

![Grafo no dirigido vs. grafo dirigido]({{ '/13_simple_search/images/01_undirected_vs_directed.png' | url }})

---

## 3. Grafos simples y multigrafos

Un **grafo simple** satisface dos condiciones:

1. **Sin autoloops**: no existe arista de un vértice a sí mismo, es decir, $\{v, v\} \notin E$.
2. **Sin aristas múltiples**: entre dos vértices hay a lo sumo una arista.

Un **multigrafo** relaja estas restricciones: puede haber múltiples aristas entre el mismo par de vértices, y pueden existir autoloops.

:::example{title="¿Por qué nos importa la distinción?"}
En este módulo trabajamos exclusivamente con **grafos simples**. Esta suposición simplifica los algoritmos: no necesitamos rastrear cuántas aristas hay entre dos nodos, ni manejar el caso especial de $u = v$.

La mayoría de los problemas de búsqueda caen naturalmente en esta categoría: entre dos estados hay una transición o no la hay.
:::

![Grafo simple vs. multigrafo]({{ '/13_simple_search/images/02_simple_vs_multigraph.png' | url }})

---

## 4. Vocabulario esencial: recorridos, caminos y ciclos

Dado un grafo $G = (V, E)$ necesitamos hablar sobre secuencias de vértices conectados.

### Recorrido (*walk*)

Una secuencia de vértices $v_0, v_1, v_2, \ldots, v_k$ tal que cada par consecutivo $(v_i, v_{i+1})$ es una arista. **Puede repetir vértices y aristas.**

### Camino (*path*)

Un recorrido donde **ningún vértice se repite**. Formalmente: $v_i \neq v_j$ para todo $i \neq j$.

La **longitud** de un camino es su número de aristas $k$.

### Ciclo (*cycle*)

Un camino $v_0, v_1, \ldots, v_k$ donde además $v_0 = v_k$ (el camino es cerrado). Es decir, empieza y termina en el mismo vértice, y no repite ningún vértice intermedio.

Un grafo **acíclico** no contiene ciclos.

![Recorrido, camino y ciclo en un grafo]({{ '/13_simple_search/images/04_walk_path_cycle.png' | url }})

:::example{title="¿Por qué importa la diferencia?"}
Cuando buscamos un camino entre dos nodos, queremos un *path* (sin repeticiones), no solo un recorrido. Los algoritmos de búsqueda que veremos en los módulos siguientes necesitan llevar un conjunto de nodos visitados precisamente para evitar convertir un path en un walk infinito.
:::

---

## 5. Conectividad

### Grafos no dirigidos

Un grafo no dirigido es **conexo** si existe un camino entre todo par de vértices $u, v \in V$.

Si no es conexo, sus **componentes conexas** son los subgrafos conexos maximales — los grupos de nodos que sí están conectados entre sí.

### Grafos dirigidos

La noción de conectividad se bifurca:

- **Fuertemente conexo**: existe un camino dirigido de $u$ a $v$ **y** de $v$ a $u$ para todo par $u, v$.
- **Débilmente conexo**: el grafo subyacente no dirigido (ignorar direcciones) es conexo.

---

## 6. Árboles: grafos especiales

Un **árbol** es un grafo no dirigido que es simultáneamente:

- **Conexo**: existe un camino entre todo par de nodos.
- **Acíclico**: no contiene ciclos.

Estas dos condiciones son equivalentes a $|E| = |V| - 1$.

Los árboles aparecen constantemente en búsqueda porque los algoritmos BFS y DFS generan naturalmente un **árbol de búsqueda** — la estructura que registra cómo se exploraron los nodos.

:::example{title="Árbol de búsqueda vs. grafo del espacio de estados"}
Es importante distinguir dos objetos diferentes:

- **Grafo del espacio de estados**: el grafo de entrada que representa el problema (puede tener ciclos, múltiples caminos, etc.).
- **Árbol de búsqueda**: la estructura que el algoritmo *construye* mientras explora. Es un árbol porque cada nodo tiene exactamente un padre (el nodo desde el que fue descubierto).

El mismo grafo de entrada genera árboles de búsqueda distintos según el algoritmo (BFS vs. DFS). Un nodo del espacio de estados puede aparecer múltiples veces en el árbol de búsqueda si el grafo tiene ciclos.
:::

![El árbol como grafo especial]({{ '/13_simple_search/images/05_tree_special_case.png' | url }})

---

## 7. Grado de un vértice

### Grafos no dirigidos

El **grado** de un vértice $v$, denotado $\deg(v)$, es el número de aristas incidentes a $v$.

**Ejemplo concreto:** considera el triángulo $A - B - C - A$ (tres vértices, tres aristas).

| Vértice | Aristas incidentes | Grado |
|---|---|---|
| $A$ | $\{A,B\},\{A,C\}$ | 2 |
| $B$ | $\{A,B\},\{B,C\}$ | 2 |
| $C$ | $\{A,C\},\{B,C\}$ | 2 |

Suma de grados: $2 + 2 + 2 = 6 = 2 \times 3 = 2|E|$.

**¿Por qué siempre vale $\sum_{v \in V} \deg(v) = 2|E|$?**

Esta es una igualdad **exacta** — no una cota ni una aproximación — y vale para **cualquier grafo no dirigido**, sin importar si es conexo, disperso o denso.

El argumento es de doble conteo: imagina que "distribuyes" cada arista entre sus dos extremos, dando medio punto a cada uno. La suma total de puntos es $|E|$ (una por arista). Pero esa misma suma vista por vértices es $\frac{1}{2}\sum_{v} \deg(v)$, porque el grado de $v$ cuenta cuántas aristas le tocaron. Igualando: $\frac{1}{2}\sum_{v} \deg(v) = |E|$, es decir:

$$\sum_{v \in V} \deg(v) = 2|E|$$

O dicho sin fracciones: cada arista $\{u,v\}$ contribuye $+1$ al grado de $u$ y $+1$ al grado de $v$ — exactamente 2 en total. No hay margen de error porque cada arista tiene **exactamente** dos extremos, ni más ni menos (estamos en un grafo simple).

### Grafos dirigidos

- **Grado de entrada** (*in-degree*) $\deg^+(v)$: número de arcos que llegan a $v$.
- **Grado de salida** (*out-degree*) $\deg^-(v)$: número de arcos que salen de $v$.

El grado de salida determina cuántas opciones tiene un agente desde el estado $v$ — esto es el **factor de ramificación** (*branching factor*), que reaparecerá en el análisis de complejidad de BFS, DFS e IDDFS.

---

## 8. Representaciones en Python

¿Cómo guardamos un grafo en memoria? Hay dos representaciones estándar.

### 8.1 Lista de adyacencia

Para cada vértice, guardamos la lista de sus vecinos. En Python, lo más natural es un diccionario de listas:

```python
# Grafo dirigido: 0→1, 0→2, 1→3, 2→3, 3→4
graph = {
    0: [1, 2],
    1: [3],
    2: [3],
    3: [4],
    4: [],
}
```

Para un grafo **no dirigido**, cada arista aparece en ambas listas:

```python
# Grafo no dirigido: {0,1}, {1,2}, {2,3}
graph = {
    0: [1],
    1: [0, 2],
    2: [1, 3],
    3: [2],
}
```

### 8.2 Matriz de adyacencia

Una matriz $A$ de tamaño $|V| \times |V|$ donde $A[i][j] = 1$ si existe la arista $(i, j)$ y $0$ si no.

```python
import numpy as np

# El mismo grafo dirigido de 5 nodos
A = np.array([
    [0, 1, 1, 0, 0],   # nodo 0
    [0, 0, 0, 1, 0],   # nodo 1
    [0, 0, 0, 1, 0],   # nodo 2
    [0, 0, 0, 0, 1],   # nodo 3
    [0, 0, 0, 0, 0],   # nodo 4
])
```

![Lista de adyacencia vs. matriz de adyacencia]({{ '/13_simple_search/images/03_adjacency_representations.png' | url }})

### 8.3 ¿Cuál usar?

| Operación | Lista de adyacencia | Matriz de adyacencia |
|---|---|---|
| Espacio | $O(V + E)$ | $O(V^2)$ |
| Verificar si $(u,v) \in E$ | $O(\deg(u))$ | $O(1)$ |
| Iterar vecinos de $u$ | $O(\deg(u))$ | $O(V)$ |
| Añadir arista | $O(1)$ | $O(1)$ |

**Regla práctica:**

- **Grafo disperso** ($|E| \ll V^2$): usa lista de adyacencia. La mayoría de los problemas de IA caen aquí — el espacio de estados tiene muchos nodos pero cada uno tiene pocos vecinos.
- **Grafo denso** ($|E| \approx V^2$): la matriz puede ser más eficiente para consultas de aristas.

:::example{title="¿Por qué la lista es mejor para búsqueda?"}
En BFS y DFS, la operación crítica es **iterar sobre los vecinos de un nodo**. Con lista de adyacencia esto toma $O(\deg(u))$, que es proporcional a cuántos vecinos hay. Con matriz, toma $O(V)$ aunque el nodo tenga solo 3 vecinos — tenemos que revisar todas las columnas.

Para grafos dispersos (los típicos en búsqueda), la lista de adyacencia es estrictamente mejor.
:::

---

## Resumen

| Concepto | Definición rápida |
|---|---|
| Grafo $G = (V, E)$ | Conjunto de vértices y aristas |
| No dirigido / Dirigido | Aristas simétricas / asimétricas |
| Grafo simple | Sin autoloops, sin aristas múltiples |
| Recorrido | Secuencia de nodos (puede repetir) |
| Camino | Recorrido sin repeticiones |
| Ciclo | Camino cerrado |
| Grafo conexo | Camino entre todo par de nodos |
| Árbol | Conexo + acíclico, $|E| = |V| - 1$ |
| Grado | Número de aristas incidentes |

---

**Siguiente:** [Espacio de estados →](02_espacio_de_estados.md)
