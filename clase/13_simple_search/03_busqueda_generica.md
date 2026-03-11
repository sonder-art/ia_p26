---
title: "Algoritmo genérico de búsqueda"
---

| Notebook | Colab |
|---------|:-----:|
| Notebook 02 — Búsqueda (BFS, DFS e IDDFS en Python) | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/13_simple_search/notebooks/02_busqueda.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |

---

# Algoritmo genérico de búsqueda

> *"A good notation has a subtlety and suggestiveness which at times make it seem almost like a live teacher."*
> — Bertrand Russell

---

Este capítulo presenta la idea central del módulo: existe **un solo algoritmo de búsqueda**. BFS, DFS e IDDFS no son tres algoritmos distintos — son tres instancias del mismo algoritmo, cada una con una estructura de datos diferente para gestionar la frontera.

Entender esto no solo simplifica el aprendizaje; permite *diseñar* nuevos algoritmos cambiando únicamente la frontera.

---

## 1. La observación clave

Sabemos que buscar una solución = encontrar un camino en el grafo del espacio de estados. Para explorar el grafo necesitamos dos estructuras:

| Estructura | Rol |
|---|---|
| **Frontera** (*frontier*) | Nodos descubiertos pero aún no procesados. La "lista de pendientes". |
| **Conjunto explorado** (*explored*) | Nodos completamente procesados. Nunca volvemos aquí. |
| **Mapa de padres** (*parent*) | Registra de dónde vino cada nodo. Permite reconstruir el camino. |

La pregunta es: ¿en qué orden procesamos los nodos de la frontera?

La respuesta determina *completamente* el algoritmo.

---

## 2. El pseudocódigo genérico

**Idea en palabras simples:**

Mantén dos listas: una de nodos *pendientes* (la frontera) y una de nodos *ya vistos* (explorado). Empieza metiendo el nodo inicial a la frontera. Luego repite lo siguiente hasta que no queden pendientes:

1. Saca un nodo de la frontera.
2. Si es la meta, reconstruye el camino y termina.
3. Si no, márcalo como visto y mira a todos sus vecinos. Por cada vecino que no hayas visto todavía y que no esté ya en la lista de pendientes, anota de dónde vino y agrégalo a la lista de pendientes.

Eso es todo. La única pregunta que queda es: **¿cuál nodo sacas primero de la frontera?** Esa decisión define el algoritmo.

```
function GENERIC-SEARCH(problema):

    # ── Inicialización ────────────────────────────────────────────────────
    frontera ← new Frontier()               # estructura de datos vacía — Cola, Pila, etc.
    frontera.push(problema.inicio)          # metemos el nodo de inicio como primer pendiente

    explorado ← empty set                   # conjunto de nodos ya procesados — empieza vacío
    padre ← { problema.inicio: null }       # tabla "llegué a X desde Y"; el inicio no tiene padre

    # ── Bucle principal ───────────────────────────────────────────────────
    while frontera is not empty:            # mientras haya nodos pendientes de explorar...

        nodo ← frontera.pop()              # *** ÚNICA LÍNEA QUE CAMBIA ENTRE ALGORITMOS ***
                                            #   Cola (FIFO) → pop el más ANTIGUO  →  BFS
                                            #   Pila (LIFO) → pop el más RECIENTE →  DFS

        if problema.is_goal(nodo):          # ¿este nodo es la solución que buscamos?
            return reconstruct(padre, nodo) #   sí → seguir padres hacia atrás = camino completo

        explorado.add(nodo)                 # marcamos: ya procesamos este nodo, no volver a él

        for each vecino in problema.neighbors(nodo):  # miramos todos los nodos conectados a nodo

            if vecino not in explorado      # condición 1: ¿ya lo procesamos completamente?
            and vecino not in frontera:     # condición 2: ¿ya está en la lista de pendientes?
                                            #   si pasa ambas condiciones → es nuevo, lo añadimos

                padre[vecino] ← nodo        # registramos: "llegué a vecino viniendo desde nodo"
                frontera.push(vecino)       # añadimos vecino a la lista de pendientes

    return FAILURE                          # vaciamos la frontera sin encontrar meta → sin solución
```

Solo hay **una línea que cambia** entre todos los algoritmos: `frontera.pop()`. Todo lo demás — el bucle, el conjunto explorado, la tabla de padres, la expansión de vecinos — es idéntico.

---

## 3. La interfaz Frontera

Definimos una interfaz abstracta con tres operaciones:

| Operación | Descripción |
|---|---|
| `push(nodo, padre=None)` | Añade un nodo a la frontera. El parámetro `padre` es opcional — lo usan las fronteras que necesitan rastrear profundidad. |
| `pop()` | Elimina y devuelve el nodo a explorar a continuación. **Aquí vive la diferencia entre algoritmos.** |
| `contains(nodo)` | Verifica si un nodo está en la frontera. Necesario para evitar duplicados. |

Con esta interfaz, la tabla de algoritmos es:

| Frontera | Estrategia de `pop()` | Algoritmo resultante |
|---|---|---|
| Cola (FIFO) | El más *antiguo* primero | **BFS** |
| Pila (LIFO) | El más *reciente* primero | **DFS** |
| Pila con límite | El más reciente, hasta prof. $d$ | **DFS con límite** |
| Cola de prioridad (por costo) | El *más barato* primero | Costo uniforme / Dijkstra |
| Cola de prioridad ($g + h$) | El *más prometedor* primero | **A*** |

Los tres últimos los estudiamos en [Módulo 14 — Búsqueda Informada →](../14_busqueda_informada/00_index.md). Por ahora nos concentramos en los dos primeros.

---

## 4. Por qué necesitamos el conjunto explorado: el problema de los ciclos

Considera este grafo de tres nodos con un ciclo:

```
A → B → C → A  (ciclo)
```

Sin conjunto explorado, `BUSQUEDA-GENERICA` desde A produciría:

```
paso 1: procesar A → añadir B a frontera
paso 2: procesar B → añadir C a frontera
paso 3: procesar C → añadir A a frontera  ← !
paso 4: procesar A → añadir B a frontera  ← otra vez
paso 5: procesar B → añadir C a frontera  ← otra vez
... bucle infinito
```

Con el conjunto explorado, en el paso 3 al intentar añadir A, el algoritmo ve que A ya está en `explorado` y simplemente no lo añade. El ciclo queda cortado.

---

## 5. El truco del conjunto sombra para `contains` eficiente

### El problema

Mira esta línea del pseudocódigo:

```
if vecino not in explorado
and vecino not in frontera:   ← ¿cómo sabemos si vecino ya está aquí?
```

Para `explorado` usamos un `set` de Python desde el principio — la verificación es $O(1)$, rápida.

El problema es la **frontera**. Si la implementamos como una cola (`deque`) o una pila (`list`), la pregunta "¿está este nodo ya en la frontera?" requiere recorrer la estructura entera elemento por elemento: $O(n)$. En un grafo con millones de nodos, esta verificación se ejecuta millones de veces. El algoritmo se vuelve inaceptablemente lento.

### La solución: mantener dos estructuras sincronizadas

La idea es simple: además de la cola (que necesitamos para el orden FIFO), mantenemos un `set` paralelo que contiene exactamente los mismos nodos. El `set` no sirve para ordenar — solo para responder "¿está X aquí?" en $O(1)$.

A ese `set` paralelo lo llamamos **conjunto sombra** porque sigue a la cola como una sombra: cada vez que añadimos un nodo a la cola, lo añadimos también al set; cada vez que lo sacamos de la cola, lo quitamos también del set. Siempre contienen los mismos elementos.

```
Cola:    [A, C, D, F]       ← mantiene el ORDEN (quién salió primero)
Set:     {A, C, D, F}       ← responde ¿está X? en O(1)
```

### Implementación

```python
class ColaDeFrontera:
    def __init__(self):
        self.cola = deque()     # mantiene el orden FIFO
        self.miembros = set()   # permite contains en O(1)

    def push(self, nodo, padre=None):
        self.cola.append(nodo)  # añadir a la cola...
        self.miembros.add(nodo) # ...y al set al mismo tiempo → siempre sincronizados

    def pop(self):
        nodo = self.cola.popleft()   # sacar de la cola (el más antiguo)...
        self.miembros.discard(nodo)  # ...y del set al mismo tiempo
        return nodo

    def contains(self, nodo):
        return nodo in self.miembros  # O(1) — consultamos el set, no la cola
```

### La implicación: tiempo vs. memoria

| Enfoque | `contains` | Memoria |
|---|---|---|
| Solo `deque` | $O(n)$ — revisar uno por uno | $n$ nodos |
| `deque` + `set` sombra | $O(1)$ — tabla hash | $2n$ nodos |

Duplicamos el uso de memoria de la frontera a cambio de que cada verificación sea instantánea. En la práctica siempre vale la pena: la frontera ocupa una fracción pequeña de la memoria total, y la ganancia en velocidad es enorme.

---

## 6. Reconstrucción del camino

El mapa `padre` registra, para cada nodo descubierto, desde qué nodo fue alcanzado. Una vez encontrada la meta, seguimos los padres hacia atrás:

```python
def reconstruir_camino(padre, meta):
    camino = []
    nodo = meta
    while nodo is not None:
        camino.append(nodo)
        nodo = padre[nodo]
    camino.reverse()
    return camino
```

Ejemplo con `padre = {A: None, B: A, D: B, F: D}` y meta `F`:

```
F → D → B → A → None
```

Reversed: `[A, B, D, F]` — el camino de inicio a meta.

---

## 7. Implementación Python completa

Esta es la única implementación del algoritmo genérico que usaremos en todo el módulo. BFS, DFS e IDDFS no tendrán su propio loop — solo su propia clase `Frontera`.

```python
from collections import deque

# ── Interfaz abstracta ────────────────────────────────────────────────────

class Frontera:
    """Interfaz abstracta. Cada subclase implementa una estrategia distinta."""

    def push(self, nodo, padre=None):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def contains(self, nodo):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError


# ── Funciones de búsqueda ─────────────────────────────────────────────────

def busqueda_generica(problema, frontera):
    """
    Algoritmo genérico de búsqueda.
    El algoritmo específico (BFS, DFS, etc.) está determinado únicamente
    por la clase `frontera` que se pasa como argumento.
    """
    inicio = problema.inicio
    frontera.push(inicio)
    explorado = set()
    padre = {inicio: None}

    while not frontera.is_empty():
        nodo = frontera.pop()

        if problema.es_meta(nodo):
            return reconstruir_camino(padre, nodo)

        explorado.add(nodo)

        for vecino in problema.vecinos(nodo):
            if vecino not in explorado and not frontera.contains(vecino):
                padre[vecino] = nodo
                frontera.push(vecino, padre=nodo)

    return None  # FALLO: no se encontró solución


def reconstruir_camino(padre, meta):
    """Reconstruye el camino desde el inicio hasta la meta usando el mapa de padres."""
    camino = []
    nodo = meta
    while nodo is not None:
        camino.append(nodo)
        nodo = padre[nodo]
    camino.reverse()
    return camino
```

---

## Resumen visual

```
                        busqueda_generica(problema, frontera)
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                  │
           ColaDeFrontera     PilaDeFrontera    PilaConLimite
               (FIFO)             (LIFO)          (LIFO + d)
                    │                 │                  │
                  BFS               DFS             DFS limitado
                                                         │
                                                      IDDFS
                                               (loop sobre DFS limitado)
```

En los próximos capítulos veremos exactamente cómo se implementa cada frontera y qué consecuencias tiene cada elección en términos de completitud, optimalidad y complejidad.

---

## Notación de complejidad — referencia para todo el módulo

Los capítulos siguientes analizan la complejidad de BFS, DFS e IDDFS usando tres parámetros. Se definen aquí una vez y se usan de forma consistente en todo el módulo:

| Símbolo | Nombre | Significado | Ejemplo |
|:-------:|--------|-------------|---------|
| $b$ | **Factor de ramificación** (*branching factor*) | **Número máximo** de vecinos de cualquier nodo — cuántas opciones hay como máximo en cada paso | En una cuadrícula: $b = 4$ (exacto, todos los nodos tienen 4 vecinos). En ajedrez: $b \approx 35$ (promedio usado como estimación del máximo práctico). |
| $d$ | **Profundidad de la solución** (*depth of solution*) | Número de aristas en el camino más corto desde el inicio hasta la meta | Si la solución es `A→B→D→F`, entonces $d = 3$. |
| $m$ | **Profundidad máxima del grafo** (*maximum depth*) | La rama más larga posible del grafo. Puede ser mucho mayor que $d$ o incluso infinito. | Un grafo con ciclos sin conjunto explorado tendría $m = \infty$. |

:::example{title="¿$b$ es el máximo o el promedio? ¿Importa para Big-O?"}

Depende de lo que quieras garantizar:

| Usando $b$ como... | $O(b^d)$ significa... | Válido como... |
|---|---|---|
| **máximo** de vecinos | cota superior garantizada — nunca explorarás más nodos | análisis de **peor caso** ✓ |
| **promedio** de vecinos | número esperado de nodos — estimación práctica | análisis de **caso promedio** |

**Cuando el grafo es uniforme** (todos los nodos tienen el mismo número de vecinos, como una cuadrícula 4-conexa o un árbol binario), máximo = promedio y la distinción desaparece.

**Cuando el grafo es irregular** (algunos nodos tienen 2 vecinos, otros tienen 20), hay dos opciones:
- Usar $b = b_{max}$ → Big-O es una cota de peor caso, pero puede sobreestimar mucho si la mayoría de nodos tienen pocos vecinos.
- Usar $b = b_{avg}$ → Big-O es una estimación más realista, pero ya no es un peor caso garantizado.

En los análisis de este módulo usamos $b = b_{max}$ para que las cotas $O(b^d)$, $O(b^m)$ y $O(bd)$ sean garantías válidas en el peor caso. Cuando un ejercicio dice "la cuadrícula tiene $b=4$" o "ajedrez tiene $b=35$" está usando el máximo práctico (o el exacto en grafos regulares).
:::

**¿Por qué importa la diferencia entre $d$ y $m$?**

- $d$ es la profundidad donde *vive la solución* — cuántos pasos mínimos se necesitan.
- $m$ es lo más profundo que puede ir el algoritmo *en el peor caso*.
- BFS e IDDFS garantizan explorar solo hasta $d$ — nunca más profundo de lo necesario.
- DFS puede bajar hasta $m$, que puede ser arbitrariamente mayor que $d$.

Esta diferencia explica directamente por qué el espacio de BFS es $O(b^d)$ (controlado por la solución) mientras que el tiempo de DFS puede ser $O(b^m)$ (controlado por la profundidad máxima).

---

**Siguiente:** [Búsqueda en amplitud (BFS) →](04_bfs.md)
