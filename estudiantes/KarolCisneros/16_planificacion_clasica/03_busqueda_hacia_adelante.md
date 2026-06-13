---
title: "Búsqueda hacia adelante"
---

| Notebook | Colab |
|---------|:-----:|
| Notebook 02 — Planificación forward | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/16_planificacion_clasica/notebooks/02_planificacion_forward.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |

---

# Búsqueda hacia adelante: GENERIC-SEARCH + STRIPS

> *"There is nothing new under the sun — but there are lots of old things we don't know."*
> — Ambrose Bierce

---

El algoritmo de búsqueda hacia adelante (*forward search*) para planificación es **exactamente** `GENERIC-SEARCH` del módulo 13. No es una analogía — es literalmente el mismo código con tres sustituciones. Esta sección lo demuestra paso a paso.

---

## 1. La conexión con GENERIC-SEARCH

Recordemos el algoritmo genérico de búsqueda del módulo 13:

```
function GENERIC-SEARCH(problema):

    frontera ← {problema.inicio}
    explorado ← ∅
    padre ← {inicio: null}

    while frontera ≠ ∅:
        n ← frontera.pop()

        if problema.es_meta(n):
            return camino(padre, n)

        explorado.add(n)

        for v in problema.vecinos(n):
            if v ∉ explorado ∪ frontera:
                padre[v] ← n
                frontera.push(v)

    return FAILURE
```

Ahora veamos `FORWARD-PLANNING`. Las líneas idénticas están sin resaltar; las tres diferencias están marcadas con `[D1]`, `[D2]`, `[D3]`:

```
function FORWARD-PLANNING(problema):

    frontera ← {problema.s₀}                          # idéntico
    explorado ← ∅                                      # idéntico
    padre ← {s₀: (null, null)}                         # idéntico (+ acción)

    while frontera ≠ ∅:                                # idéntico
        s ← frontera.pop()                             # idéntico

        if problema.meta ⊆ s:                  [D1]   # ← CAMBIO: meta es subconjunto
            return plan(padre, s)                      # idéntico

        explorado.add(s)                               # idéntico

        for a in aplicables(s, problema.acciones): [D2] # ← CAMBIO: filtrar por precondiciones
            v ← aplicar(s, a)                  [D3]    # ← CAMBIO: transición por add/delete
            if v ∉ explorado ∪ frontera:               # idéntico
                padre[v] ← (s, a)                      # idéntico (+ acción)
                frontera.push(v)                       # idéntico

    return FAILURE                                     # idéntico
```

![Forward search vs generic search]({{ '/16_planificacion_clasica/images/06_forward_search_vs_generic.png' | url }})

### Los tres cambios, explicados

> **[D1] — Test de meta**: en búsqueda, `es_meta(n)` compara contra *un* estado. En planificación, la meta es un *subconjunto* de proposiciones. Un estado satisface la meta si $\text{meta} \subseteq s$ — si contiene todas las proposiciones requeridas. Puede contener más, y eso está bien.

> **[D2] — Generación de vecinos**: en búsqueda, `vecinos(n)` devuelve los nodos conectados por aristas. En planificación, no hay aristas predefinidas. En su lugar, `aplicables(s)` filtra las acciones cuyas precondiciones se cumplen en el estado actual. Solo esas acciones generan vecinos.

> **[D3] — Función de transición**: en búsqueda, la transición es implícita (seguir la arista). En planificación, `aplicar(s, a)` calcula el nuevo estado: quita la lista delete, agrega la lista add. La transición es una *operación sobre conjuntos*.

**Todo lo demás es idéntico**: la frontera, el conjunto explorado, el mapa de padres, el bucle principal, la detección de duplicados. El algoritmo de planificación no es un algoritmo nuevo — es búsqueda con un lenguaje más rico para estados y transiciones.

---

## 2. En lenguaje natural

El algoritmo paso a paso:

1. **Empezar**: pon el estado inicial $s_0$ en la frontera. La frontera es la lista de estados pendientes de explorar.

2. **Sacar un estado**: toma un estado $s$ de la frontera. El orden depende de la estructura de datos:
   - **Cola (FIFO)** → BFS — explora por capas, encuentra el plan más corto.
   - **Pila (LIFO)** → DFS — explora en profundidad, usa menos memoria.
   - **Cola de prioridad** → A* — explora los más prometedores primero (sección 4).

3. **Verificar la meta**: ¿el estado $s$ contiene TODAS las proposiciones de la meta? Si sí, reconstruye el plan siguiendo el mapa de padres hacia atrás y termina.

4. **Expandir**: para cada acción disponible, verifica si sus precondiciones se cumplen en $s$. Si sí, aplica la acción (quita delete, agrega add) y obtén el estado sucesor. Si este sucesor no ha sido explorado ni está en la frontera, agrégalo a la frontera.

5. **Repetir** hasta encontrar la meta o agotar la frontera (no hay plan posible).

### Orden de expansión: ¿quién entra primero a la frontera?

Hay un detalle sutil pero importante. En el paso 4, el algoritmo recorre las acciones aplicables en **algún orden** y va agregando los estados sucesores a la frontera. Ese orden depende de cómo están almacenadas las acciones en la lista `acciones` — es decir, del orden en que fueron generadas al definir el dominio. La primera acción aplicable que se prueba genera el primer sucesor que entra a la frontera, la segunda genera el segundo, etc.

Como BFS usa una cola FIFO (el primero que entra es el primero que sale), **el orden de enumeración de las acciones determina el orden en que se exploran los estados dentro de una misma capa**. Si cambiáramos el orden de la lista de acciones (por ejemplo, poner MoverDesdeMesa(C,B) antes que MoverDesdeMesa(A,B)), los mismos 13 estados se explorarían en un orden diferente.

¿Afecta esto la corrección del algoritmo? **No.** BFS sigue siendo completo y óptimo (en número de pasos) sin importar el orden de enumeración. Todos los estados de la capa $k$ se exploran antes que cualquier estado de la capa $k+1$. Lo único que cambia es *cuál* de los estados dentro de la misma capa se visita primero — pero como todos están a la misma distancia del inicio, el resultado es igualmente óptimo.

> **Contraste con A\***: en A\* (módulo 14), el orden **no** es arbitrario — la cola de prioridad ordena por $f(s) = g(s) + h(s)$. El planificador elige primero el estado más prometedor según la heurística, no el que fue generado primero. Esa es la diferencia entre búsqueda ciega (BFS/DFS) y búsqueda informada (A\*).

---

## 3. Las funciones auxiliares

Antes del pseudocódigo completo, definimos las dos funciones auxiliares que implementan las diferencias [D2] y [D3].

### aplicables(s, acciones) — filtrar acciones por precondiciones [D2]

```
# ── APLICABLES ──────────────────────────────────────────────────────────────
# Recibe un estado s y la lista completa de acciones.
# Devuelve solo las acciones cuyas precondiciones están todas en s.

function APLICABLES(s, acciones):
    resultado ← []                                    # lista vacía de acciones aplicables
    for each a in acciones:                           # recorre TODAS las acciones del dominio
        if a.precondiciones ⊆ s:                      # ¿cada precondición está en el estado?
            resultado.append(a)                       # sí → esta acción se puede ejecutar
    return resultado                                  # devuelve solo las aplicables
```

**Ejemplo**: en el estado $s_0 = \{\text{On}(A,\text{Mesa}), \text{On}(B,\text{Mesa}), \text{On}(C,\text{Mesa}), \text{Clear}(A), \text{Clear}(B), \text{Clear}(C)\}$:

| Acción | Precondiciones | ¿En $s_0$? | ¿Aplicable? |
|---|---|:---:|:---:|
| MoverDesdeMesa(A, B) | {On(A,Mesa), Clear(A), Clear(B)} | Sí, sí, sí | **Sí** ✓ |
| MoverDesdeMesa(B, C) | {On(B,Mesa), Clear(B), Clear(C)} | Sí, sí, sí | **Sí** ✓ |
| Mover(A, B, C) | {On(A,B), Clear(A), Clear(C)} | **No** (On(A,B) falta) | **No** ✗ |
| MoverAMesa(A, B) | {On(A,B), Clear(A)} | **No** (On(A,B) falta) | **No** ✗ |

En $s_0$, las 6 acciones MoverDesdeMesa son aplicables (todos los bloques están en la mesa y libres). Las 12 acciones Mover y MoverAMesa no son aplicables (necesitan que un bloque esté sobre otro bloque).

### aplicar(s, a) — calcular nuevo estado [D3]

```
# ── APLICAR ─────────────────────────────────────────────────────────────────
# Recibe un estado s y una acción a (cuyas precondiciones se cumplen en s).
# Calcula el nuevo estado: quita las proposiciones borradas, agrega las nuevas.

function APLICAR(s, a):
    nuevo ← s − a.delete                             # elimina lo que ya no es cierto
    nuevo ← nuevo ∪ a.add                             # agrega lo que ahora es cierto
    return nuevo                                      # el resto queda igual (mundo cerrado)
```

**Ejemplo**: aplicar MoverDesdeMesa(B, C) a $s_0$:

```
s₀    = { On(A,Mesa), On(B,Mesa), On(C,Mesa), Clear(A), Clear(B), Clear(C) }

Delete = { On(B,Mesa), Clear(C) }
s₀ − Delete = { On(A,Mesa), On(C,Mesa), Clear(A), Clear(B) }

Add = { On(B,C) }
s₁ = { On(A,Mesa), On(C,Mesa), Clear(A), Clear(B) } ∪ { On(B,C) }
   = { On(A,Mesa), On(B,C), On(C,Mesa), Clear(A), Clear(B) }
```

---

## 4. Pseudocódigo completo

Aquí está `FORWARD-PLANNING` con cada línea comentada, las tres diferencias marcadas, y separadores de sección:

```
# ── FORWARD-PLANNING ────────────────────────────────────────────────────────
# Búsqueda hacia adelante: GENERIC-SEARCH con representación STRIPS.
# La estructura de la frontera determina el algoritmo:
#   Cola (FIFO) → BFS — plan más corto
#   Pila (LIFO) → DFS — menos memoria
#   Cola de prioridad → A* — usa heurística (sección 4)

function FORWARD-PLANNING(problema):

    # ── Inicialización ──────────────────────────────────────────────────
    frontera ← new Frontier()                # estructura vacía (Cola para BFS)
    frontera.push(problema.s₀)               # metemos el estado inicial como primer pendiente
    explorado ← empty set                    # conjunto de estados ya procesados — vacío al inicio
    padre ← { problema.s₀: (null, null) }    # mapa: estado → (estado_padre, acción_usada)
                                              # el estado inicial no tiene padre ni acción

    # ── Bucle principal ─────────────────────────────────────────────────
    while frontera is not empty:             # mientras haya estados pendientes de explorar...

        s ← frontera.pop()                   # saca el siguiente estado según la estrategia
                                              #   Cola → el más antiguo (BFS)
                                              #   Pila → el más reciente (DFS)

        # ── Test de meta ─ [D1] ────────────────────────────────────────
        if problema.meta ⊆ s:                # ¿el estado s contiene TODAS las proposiciones meta?
            return reconstruct_plan(padre, s) #   sí → seguir padres hacia atrás = plan completo

        explorado.add(s)                      # marcamos: ya procesamos s, no volver a él

        # ── Expandir ─ [D2] y [D3] ─────────────────────────────────────
        for each a in APLICABLES(s, problema.acciones):   # [D2] solo acciones con pre ⊆ s
            v ← APLICAR(s, a)                              # [D3] nuevo estado: s − delete ∪ add

            if v ∉ explorado and v ∉ frontera:             # ¿es un estado nuevo?
                padre[v] ← (s, a)                          # registramos: "llegué a v desde s con a"
                frontera.push(v)                           # añadimos v a la lista de pendientes

    return FAILURE                           # frontera vacía sin encontrar meta → sin plan
```

**Las tres diferencias sobre `GENERIC-SEARCH`:**

| Cambio | Línea | Qué cambia |
|:------:|---|---|
| `[D1]` | `if problema.meta ⊆ s` | Meta = subconjunto de proposiciones, no un estado fijo |
| `[D2]` | `for a in APLICABLES(s, ...)` | Vecinos = acciones con precondiciones satisfechas |
| `[D3]` | `v ← APLICAR(s, a)` | Transición = operación sobre conjuntos (delete + add) |

---

## 5. Implementación en Python

```python
from collections import deque, namedtuple


# ── Representación de acciones ──────────────────────────────────────────────
# Una acción STRIPS tiene: nombre, precondiciones, lista add, lista delete.
# Usamos namedtuple para claridad. Los conjuntos son frozenset (inmutables).

Action = namedtuple("Action", ["name", "preconditions", "add_list", "delete_list"])


def is_applicable(state, action):
    """
    Verifica si una acción es aplicable en un estado.

    Args:
        state  : frozenset — conjunto de proposiciones verdaderas
        action : Action   — acción STRIPS con precondiciones

    Returns:
        True si TODAS las precondiciones están en el estado.
    """
    return action.preconditions.issubset(state)   # pre ⊆ state?


def apply_action(state, action):
    """
    Aplica una acción a un estado.

    La fórmula: state' = (state − delete) ∪ add

    Args:
        state  : frozenset — estado actual
        action : Action   — acción aplicable (ya verificada)

    Returns:
        frozenset — nuevo estado después de aplicar la acción
    """
    return (state - action.delete_list) | action.add_list


def get_applicable(state, all_actions):
    """
    Devuelve la lista de acciones aplicables en un estado.

    Recorre TODAS las acciones del dominio y filtra las que
    tienen sus precondiciones satisfechas en el estado actual.
    """
    return [a for a in all_actions if is_applicable(state, a)]


# ── Búsqueda hacia adelante (BFS) ──────────────────────────────────────────

def forward_planning_bfs(initial, goal, all_actions):
    """
    Búsqueda hacia adelante con BFS.

    Args:
        initial     : frozenset — estado inicial (proposiciones verdaderas)
        goal        : frozenset — proposiciones que deben ser verdaderas en la meta
        all_actions : list[Action] — todas las acciones del dominio

    Returns:
        list[Action] — plan (secuencia de acciones) o None si no hay solución
    """
    # ── Inicialización ──────────────────────────────────────────────────
    frontier = deque([initial])                # cola FIFO para BFS
    explored = set()                           # estados ya procesados
    parent = {initial: (None, None)}           # estado → (estado_padre, acción)

    # ── Bucle principal ─────────────────────────────────────────────────
    while frontier:                            # mientras haya estados pendientes...
        s = frontier.popleft()                 # sacar el más antiguo (BFS = FIFO)

        # ── Test de meta [D1] ───────────────────────────────────────────
        if goal.issubset(s):                   # ¿s contiene TODAS las proposiciones meta?
            # Reconstruir el plan siguiendo padres hacia atrás
            plan = []
            current = s
            while parent[current][0] is not None:
                prev_state, action = parent[current]
                plan.append(action)
                current = prev_state
            plan.reverse()                     # invertir: de inicio a meta
            return plan

        explored.add(s)                        # marcar como procesado

        # ── Expandir [D2] y [D3] ────────────────────────────────────────
        for a in get_applicable(s, all_actions):      # [D2] filtrar por precondiciones
            new_state = apply_action(s, a)             # [D3] calcular nuevo estado
            if new_state not in explored and new_state not in frontier:
                parent[new_state] = (s, a)             # registrar cómo llegamos
                frontier.append(new_state)             # agregar a la frontera

    return None                                # no se encontró plan


# ── Definición de Blocks World ──────────────────────────────────────────────

def make_blocks_world_actions():
    """Genera las 18 acciones concretas para Blocks World con 3 bloques."""
    blocks = ["A", "B", "C"]
    actions = []
    for x in blocks:
        for y in blocks:
            if x == y:
                continue
            for z in blocks:
                if z == x or z == y:
                    continue
                # Mover(X, Y, Z): mover X de bloque Y a bloque Z
                actions.append(Action(
                    name=f"Mover({x},{y},{z})",
                    preconditions=frozenset({f"On({x},{y})", f"Clear({x})", f"Clear({z})"}),
                    add_list=frozenset({f"On({x},{z})", f"Clear({y})"}),
                    delete_list=frozenset({f"On({x},{y})", f"Clear({z})"}),
                ))
        for y in blocks:
            if x == y:
                continue
            # MoverAMesa(X, Y): mover X de bloque Y a mesa
            actions.append(Action(
                name=f"MoverAMesa({x},{y})",
                preconditions=frozenset({f"On({x},{y})", f"Clear({x})"}),
                add_list=frozenset({f"On({x},Mesa)", f"Clear({y})"}),
                delete_list=frozenset({f"On({x},{y})"}),
            ))
            # MoverDesdeMesa(X, Y): mover X de mesa a bloque Y
            actions.append(Action(
                name=f"MoverDesdeMesa({x},{y})",
                preconditions=frozenset({f"On({x},Mesa)", f"Clear({x})", f"Clear({y})"}),
                add_list=frozenset({f"On({x},{y})"}),
                delete_list=frozenset({f"On({x},Mesa)", f"Clear({y})"}),
            ))
    return actions


# ── Ejemplo de uso ──────────────────────────────────────────────────────────
if __name__ == '__main__':
    initial = frozenset({
        "On(A,Mesa)", "On(B,Mesa)", "On(C,Mesa)",
        "Clear(A)", "Clear(B)", "Clear(C)"
    })
    goal = frozenset({"On(A,B)", "On(B,C)", "On(C,Mesa)", "Clear(A)"})

    all_actions = make_blocks_world_actions()
    plan = forward_planning_bfs(initial, goal, all_actions)

    print(f"Estado inicial: todos en la mesa")
    print(f"Meta: A sobre B sobre C sobre mesa")
    print(f"Plan encontrado ({len(plan)} pasos):")
    for i, action in enumerate(plan, 1):
        print(f"  Paso {i}: {action.name}")
    # → Plan encontrado (2 pasos):
    # →   Paso 1: MoverDesdeMesa(B,C)
    # →   Paso 2: MoverDesdeMesa(A,B)
```

---

## 6. Traza paso a paso: BFS en Blocks World

Vamos a ejecutar `FORWARD-PLANNING` con BFS (cola FIFO) en nuestro ejemplo. Estado inicial: A, B, C en la mesa. Meta: A sobre B, B sobre C, C en la mesa.

Para hacer la traza legible, usamos esta notación abreviada para los estados:

| Notación | Significado | Visual |
|---|---|---|
| `A, B, C` | Los tres bloques en la mesa | `A  B  C` (mesa) |
| `A/B, C` | A sobre B, C en la mesa | A encima de B, C solo |
| `A/B/C` | Torre: A sobre B sobre C sobre la mesa | Torre de 3 |

La barra `/` significa "encima de": `A/B` = A está encima de B. Todos los bloques que no están sobre otro bloque están sobre la mesa.

### Traza completa

Ejecutamos el algoritmo línea por línea. En cada paso mostramos: el estado sacado de la frontera, el test de meta, las acciones aplicables, los estados que generan, y el estado de la frontera y el conjunto de explorados.

---

**Paso 1** — Sacar: `A, B, C` (estado inicial — los tres en la mesa)

$$s = \{\ \text{On}(A,\text{Mesa}),\ \text{On}(B,\text{Mesa}),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B),\ \text{Clear}(C)\ \}$$

- **Meta** $\subseteq s$? Necesitamos $\text{On}(A,B) \in s$ — **no está** → No es meta.
- **Aplicables**: todos los bloques están en la mesa y libres → solo las 6 acciones MoverDesdeMesa:

| Acción | Resultado | ¿Nuevo? |
|---|---|:---:|
| MoverDesdeMesa(A,B) | `A/B, C` | **Nuevo** → frontera |
| MoverDesdeMesa(A,C) | `B, A/C` | **Nuevo** → frontera |
| MoverDesdeMesa(B,A) | `B/A, C` | **Nuevo** → frontera |
| MoverDesdeMesa(B,C) | `A, B/C` | **Nuevo** → frontera |
| MoverDesdeMesa(C,A) | `C/A, B` | **Nuevo** → frontera |
| MoverDesdeMesa(C,B) | `A, C/B` | **Nuevo** → frontera |

- **Frontera** (6): los 6 estados con un bloque sobre otro.
- **Explorados** (1): `{A, B, C}`

---

**Paso 2** — Sacar: `A/B, C` (A sobre B, C en la mesa)

> **¿Por qué sale `A/B, C` y no otro estado?** En el paso 1, las 6 acciones MoverDesdeMesa se recorrieron en el orden de la lista de acciones. La primera aplicable fue MoverDesdeMesa(A,B), así que `A/B, C` fue el primer sucesor en entrar a la cola FIFO, y por lo tanto es el primero en salir. Si las acciones estuvieran en otro orden — por ejemplo, si MoverDesdeMesa(C,B) fuera la primera — saldría otro estado aquí. Pero el resultado final del BFS sería el mismo: plan óptimo de 2 pasos.

$$s = \{\ \text{On}(A,B),\ \text{On}(B,\text{Mesa}),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(C)\ \}$$

- **Meta** $\subseteq s$? $\text{On}(B,C) \notin s$ → No.
- **Aplicables** (3): Clear(A) y Clear(C) → podemos mover A (está encima) o subir C a A.

| Acción | ¿Por qué aplicable? | Resultado | ¿Nuevo? |
|---|---|---|:---:|
| Mover(A,B,C) | On(A,B)✓ Clear(A)✓ Clear(C)✓ | `B, A/C` | En frontera |
| MoverAMesa(A,B) | On(A,B)✓ Clear(A)✓ | `A, B, C` | Explorado |
| MoverDesdeMesa(C,A) | On(C,Mesa)✓ Clear(C)✓ Clear(A)✓ | `C/A/B` — torre | **Nuevo** → frontera |

- **Frontera** (6): se quitó `A/B, C` y se agregó `C/A/B` (torre).
- **Explorados** (2): `{A,B,C}` y `{A/B, C}`

> **Observación**: MoverAMesa(A,B) devuelve al estado inicial — ya explorado, se descarta. Mover(A,B,C) genera `B, A/C` que ya está en la frontera — también se descarta. Solo `C/A/B` (torre C sobre A sobre B) es nuevo.

---

**Paso 3** — Sacar: `B, A/C` (A sobre C, B en la mesa)

$$s = \{\ \text{On}(A,C),\ \text{On}(B,\text{Mesa}),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\ \}$$

- **Meta** $\subseteq s$? $\text{On}(A,B) \notin s$ → No.
- **Aplicables** (3):

| Acción | Resultado | ¿Nuevo? |
|---|---|:---:|
| Mover(A,C,B) | `A/B, C` | Explorado |
| MoverAMesa(A,C) | `A, B, C` | Explorado |
| MoverDesdeMesa(B,A) | `B/A/C` — torre | **Nuevo** → frontera |

- **Frontera** (6): se quitó `B, A/C` y se agregó `B/A/C` (torre).
- **Explorados** (3)

---

**Paso 4** — Sacar: `B/A, C` (B sobre A, C en la mesa)

$$s = \{\ \text{On}(A,\text{Mesa}),\ \text{On}(B,A),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(B),\ \text{Clear}(C)\ \}$$

- **Meta** $\subseteq s$? $\text{On}(A,B) \notin s$ → No.
- **Aplicables** (3):

| Acción | Resultado | ¿Nuevo? |
|---|---|:---:|
| Mover(B,A,C) | `A, B/C` | En frontera |
| MoverAMesa(B,A) | `A, B, C` | Explorado |
| MoverDesdeMesa(C,B) | `C/B/A` — torre | **Nuevo** → frontera |

- **Frontera** (6): se quitó `B/A, C` y se agregó `C/B/A` (torre).
- **Explorados** (4)

---

**Paso 5** — Sacar: `A, B/C` (B sobre C, A en la mesa)

$$s = \{\ \text{On}(A,\text{Mesa}),\ \text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\ \}$$

- **Meta** $\subseteq s$? $\text{On}(A,B) \notin s$ → No. (Tiene $\text{On}(B,C)$ y $\text{On}(C,\text{Mesa})$ y $\text{Clear}(A)$, pero falta $\text{On}(A,B)$.)
- **Aplicables** (3):

| Acción | Resultado | ¿Nuevo? |
|---|---|:---:|
| MoverDesdeMesa(A,B) | `A/B/C` — ¡torre meta! | **Nuevo** → frontera |
| Mover(B,C,A) | `B/A, C` | Explorado |
| MoverAMesa(B,C) | `A, B, C` | Explorado |

- **Frontera** (6): se quitó `A, B/C` y se agregó **`A/B/C`** (¡la torre meta!).
- **Explorados** (5)

> **Observación importante**: ¡en este paso se genera el estado meta `A/B/C`! Se agrega a la frontera, pero BFS no lo saca todavía — hay estados pendientes que entraron antes. BFS es FIFO: primero salen `C/A`, `A/C/B`, `C/A/B`, `B/A/C`, `C/B/A`, y **luego** `A/B/C`.

---

**Paso 6** — Sacar: `C/A, B` (C sobre A, B en la mesa)

$$s = \{\ \text{On}(A,\text{Mesa}),\ \text{On}(B,\text{Mesa}),\ \text{On}(C,A),\ \text{Clear}(B),\ \text{Clear}(C)\ \}$$

- **Meta** $\subseteq s$? No.
- **Aplicables** (3):

| Acción | Resultado | ¿Nuevo? |
|---|---|:---:|
| MoverDesdeMesa(B,C) | `B/C/A` — torre | **Nuevo** → frontera |
| Mover(C,A,B) | `A, C/B` | En frontera |
| MoverAMesa(C,A) | `A, B, C` | Explorado |

- **Frontera** (6): se quitó `C/A, B` y se agregó `B/C/A` (torre).
- **Explorados** (6)

---

**Paso 7** — Sacar: `A, C/B` (C sobre B, A en la mesa)

$$s = \{\ \text{On}(A,\text{Mesa}),\ \text{On}(B,\text{Mesa}),\ \text{On}(C,B),\ \text{Clear}(A),\ \text{Clear}(C)\ \}$$

- **Meta** $\subseteq s$? No.
- **Aplicables** (3):

| Acción | Resultado | ¿Nuevo? |
|---|---|:---:|
| MoverDesdeMesa(A,C) | `A/C/B` — torre | **Nuevo** → frontera |
| Mover(C,B,A) | `C/A, B` | Explorado |
| MoverAMesa(C,B) | `A, B, C` | Explorado |

- **Frontera** (6): se quitó `A, C/B` y se agregó `A/C/B` (torre). La frontera ahora contiene solo torres.
- **Explorados** (7) — todos los estados de "2 bloques en mesa" ya están explorados.

---

> **Patrón**: los pasos 2–7 exploró los 6 estados con un bloque sobre otro (capa 1 del BFS). Cada uno generó exactamente una torre nueva. Ahora la frontera tiene las 6 torres. BFS pasa a la capa 2.

---

**Paso 8** — Sacar: `C/A/B` — torre C (arriba), A (medio), B (abajo)

$$s = \{\ \text{On}(A,B),\ \text{On}(B,\text{Mesa}),\ \text{On}(C,A),\ \text{Clear}(C)\ \}$$

- **Meta** $\subseteq s$? $\text{On}(B,C) \notin s$ → No.
- **Aplicables** (1): solo C está libre (Clear), y C está sobre A (no sobre mesa).

| Acción | Resultado | ¿Nuevo? |
|---|---|:---:|
| MoverAMesa(C,A) | `A/B, C` | Explorado |

Ningún estado nuevo. La frontera se reduce.

- **Frontera** (5): 5 torres restantes (incluyendo `A/B/C`, la meta).
- **Explorados** (8)

---

**Paso 9** — Sacar: `B/A/C` — torre B (arriba), A (medio), C (abajo)

$$s = \{\ \text{On}(A,C),\ \text{On}(B,A),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(B)\ \}$$

- **Meta** $\subseteq s$? $\text{On}(A,B) \notin s$ → No.
- **Aplicables** (1): solo B está libre.

| Acción | Resultado | ¿Nuevo? |
|---|---|:---:|
| MoverAMesa(B,A) | `B, A/C` | Explorado |

Ningún estado nuevo.

- **Frontera** (4): 4 torres restantes.
- **Explorados** (9)

---

**Paso 10** — Sacar: `C/B/A` — torre C (arriba), B (medio), A (abajo)

$$s = \{\ \text{On}(A,\text{Mesa}),\ \text{On}(B,A),\ \text{On}(C,B),\ \text{Clear}(C)\ \}$$

- **Meta** $\subseteq s$? $\text{On}(A,B) \notin s$ → No.
- **Aplicables** (1): solo C está libre.

| Acción | Resultado | ¿Nuevo? |
|---|---|:---:|
| MoverAMesa(C,B) | `B/A, C` | Explorado |

Ningún estado nuevo.

- **Frontera** (3): `A/B/C` (¡la meta!), `B/C/A`, `A/C/B`.
- **Explorados** (10)

> **Patrón de las torres**: en los pasos 8–10, cada torre tiene solo 1 acción aplicable (mover el bloque de arriba a la mesa), y esa acción siempre devuelve a un estado ya explorado. Las torres son "callejones sin salida" para BFS — no generan estados nuevos.

---

**Paso 11** — Sacar: `A/B/C` — torre A (arriba), B (medio), C (abajo)

$$s = \{\ \text{On}(A,B),\ \text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A)\ \}$$

- **Meta** $\subseteq s$?
  - $\text{On}(A,B) \in s$? **Sí** ✓
  - $\text{On}(B,C) \in s$? **Sí** ✓
  - $\text{On}(C,\text{Mesa}) \in s$? **Sí** ✓
  - $\text{Clear}(A) \in s$? **Sí** ✓
  - Todas presentes → **¡SÍ! META ALCANZADA** ✓

**Plan encontrado en 11 pasos de BFS**, explorando 10 estados. Quedan 2 estados en la frontera sin explorar (`B/C/A` y `A/C/B`).

---

### Resumen de la traza

| Capa BFS | Estados explorados | ¿Qué son? |
|:---:|---|---|
| 0 | `A,B,C` (paso 1) | Todos en la mesa — 1 estado |
| 1 | `A/B,C` ... `A,C/B` (pasos 2–7) | Un bloque sobre otro — 6 estados |
| 2 | `C/A/B`, `B/A/C`, `C/B/A`, **`A/B/C`** (pasos 8–11) | Torres de 3 — exploró 4 de 6 |

BFS exploró **10 estados** antes de encontrar la meta. El espacio completo tiene 13 estados — BFS no necesitó explorarlos todos.

### Reconstrucción del plan

Seguimos el mapa de padres desde el estado meta hacia atrás:

```
A/B/C   ← llegué con MoverDesdeMesa(A,B) desde...
A, B/C  ← llegué con MoverDesdeMesa(B,C) desde...
A, B, C ← estado inicial (sin padre)
```

Invertimos: **Plan = [MoverDesdeMesa(B,C), MoverDesdeMesa(A,B)]**

### Verificación del plan paso a paso

**Paso 1: MoverDesdeMesa(B, C)**

```
Estado:  { On(A,Mesa), On(B,Mesa), On(C,Mesa), Clear(A), Clear(B), Clear(C) }
Pre:     { On(B,Mesa) ✓, Clear(B) ✓, Clear(C) ✓ } → aplicable
Delete:  { On(B,Mesa), Clear(C) }
Add:     { On(B,C) }
Después: { On(A,Mesa), On(B,C), On(C,Mesa), Clear(A), Clear(B) }
```

Visualmente:

```
          ┌───┐
 ┌───┐    │ B │
 │ A │    ├───┤
 │   │    │ C │
 ═════    ═════
```

**Paso 2: MoverDesdeMesa(A, B)**

```
Estado:  { On(A,Mesa), On(B,C), On(C,Mesa), Clear(A), Clear(B) }
Pre:     { On(A,Mesa) ✓, Clear(A) ✓, Clear(B) ✓ } → aplicable
Delete:  { On(A,Mesa), Clear(B) }
Add:     { On(A,B) }
Después: { On(A,B), On(B,C), On(C,Mesa), Clear(A) }
```

Visualmente:

```
 ┌───┐
 │ A │
 ├───┤
 │ B │
 ├───┤
 │ C │
 ═════
```

**Verificación de la meta**: ¿$\{\text{On}(A,B), \text{On}(B,C), \text{On}(C,\text{Mesa}), \text{Clear}(A)\} \subseteq s_2$? **Sí** ✓

![Plan encontrado]({{ '/16_planificacion_clasica/images/08_plan_found.png' | url }})

**Cómo leer la figura:** cada panel muestra un estado (bloques coloreados). Las flechas naranjas entre paneles indican la acción aplicada. El primer panel tiene borde verde (estado inicial), el último tiene borde naranja (meta alcanzada).

![Traza de búsqueda hacia adelante]({{ '/16_planificacion_clasica/images/07_forward_search_trace.png' | url }})

**Cómo leer la figura de traza:** cada nodo muestra la configuración de bloques. Los números (1), (2), ... indican el orden de exploración BFS. El camino verde es la solución encontrada.

---

## 7. Propiedades

| Propiedad | Valor | Condición |
|---|---|---|
| **Completo** | Sí | Espacio de estados finito + conjunto explorado |
| **Óptimo** | Sí (BFS) | Si todas las acciones tienen el mismo costo |
| **Tiempo** | $O(b^d)$ | $b$ = acciones aplicables por estado, $d$ = longitud del plan |
| **Espacio** | $O(b^d)$ | Almacena toda la frontera (igual que BFS del módulo 13) |

Comparación con los algoritmos de módulos anteriores:

| Algoritmo | Módulo | Tiempo | Espacio | Completo | Óptimo |
|---|:---:|---|---|:---:|:---:|
| BFS | 13 | $O(b^d)$ | $O(b^d)$ | Sí | Sí (sin pesos) |
| A* | 14 | $O(b^d)$ | $O(b^d)$ | Sí | Sí |
| Minimax | 15 | $O(b^m)$ | $O(b \cdot m)$ | Sí | Sí* |
| **Forward BFS** | **16** | $O(b^d)$ | $O(b^d)$ | **Sí** | **Sí** |

Las complejidades son **idénticas** a BFS — porque forward planning con cola FIFO **es** BFS. El factor de ramificación $b$ aquí es el número de acciones aplicables por estado (en Blocks World con 3 bloques, $b \leq 6$).

Para problemas más grandes, $b^d$ crece rápidamente. La siguiente sección muestra cómo usar heurísticas (la misma idea de A* del módulo 14) para reducir los nodos explorados.

---

**Siguiente:** [Heurísticas para planificación →](04_heuristicas_planificacion.md)
