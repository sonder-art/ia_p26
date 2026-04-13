---
title: "STRIPS"
---

| Notebook | Colab |
|---------|:-----:|
| Notebook 01 — STRIPS y estados | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/16_planificacion_clasica/notebooks/01_strips_y_estados.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |

---

# STRIPS: el lenguaje de las acciones

> *"The limits of my language mean the limits of my world."*
> — Ludwig Wittgenstein

---

STRIPS (Stanford Research Institute Problem Solver, 1971) es un lenguaje para describir problemas de planificación. Tiene dos ideas simples:

1. **Estados** son conjuntos de proposiciones — hechos verdaderos sobre el mundo.
2. **Acciones** son esquemas con tres partes: qué necesitan para ejecutarse (precondiciones), qué agregan al mundo (lista add), y qué eliminan del mundo (lista delete).

Este lenguaje es tan limpio que sigue siendo la base de los planificadores modernos.

---

## 1. Estados como conjuntos de proposiciones

Un estado es un **conjunto de proposiciones** — hechos que son verdaderos en este momento. Todo lo que **no** está en el conjunto se considera **falso**. Esto se llama la **suposición de mundo cerrado** (*closed-world assumption*).

### Ejemplo: el estado inicial de Blocks World

Recordemos el estado inicial de nuestro ejemplo (los tres bloques sobre la mesa):

```
 ┌───┐  ┌───┐  ┌───┐
 │ A │  │ B │  │ C │
 ═════  ═════  ═════
 mesa   mesa   mesa
```

Este estado se escribe como el siguiente conjunto de proposiciones:

$$s_0 = \{\ \text{On}(A, \text{Mesa}),\ \text{On}(B, \text{Mesa}),\ \text{On}(C, \text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B),\ \text{Clear}(C)\ \}$$

Recorramos cada proposición:

| Proposición | Significado físico |
|---|---|
| $\text{On}(A, \text{Mesa})$ | El bloque A está apoyado sobre la mesa |
| $\text{On}(B, \text{Mesa})$ | El bloque B está apoyado sobre la mesa |
| $\text{On}(C, \text{Mesa})$ | El bloque C está apoyado sobre la mesa |
| $\text{Clear}(A)$ | No hay ningún bloque encima de A — se puede mover |
| $\text{Clear}(B)$ | No hay ningún bloque encima de B — se puede mover |
| $\text{Clear}(C)$ | No hay ningún bloque encima de C — se puede mover |

### Suposición de mundo cerrado

¿Está A sobre B? No aparece $\text{On}(A, B)$ en el conjunto, así que la respuesta es **no**. No necesitamos escribir $\neg \text{On}(A, B)$ — la ausencia de la proposición equivale a su falsedad.

> **Regla**: si una proposición **no está** en el conjunto, es **falsa**. Si **está** en el conjunto, es **verdadera**. No hay proposiciones "desconocidas".

Esto simplifica enormemente la representación. En lugar de escribir $6 + 6 + 3 = 15$ proposiciones (positivas y negativas), solo escribimos las 6 que son verdaderas.

> **Nota sobre la lógica del módulo 3**: las proposiciones STRIPS son los *átomos* del módulo de lógica — hechos simples como $\text{On}(A, B)$. No usamos conectivos lógicos ($\land$, $\lor$, $\neg$) dentro de un estado. Un estado es simplemente un *conjunto* de átomos verdaderos.

---

## 2. Anatomía de una acción STRIPS

Una acción STRIPS tiene cuatro partes:

| Parte | Rol |
|---|---|
| **Nombre** | Identifica la acción, e.g., $\text{MoverDesdeMesa}(B, C)$ |
| **Precondiciones** | Conjunto de proposiciones que **deben ser verdaderas** para ejecutar la acción |
| **Lista Add** | Proposiciones que se **vuelven verdaderas** al ejecutar la acción |
| **Lista Delete** | Proposiciones que **dejan de ser verdaderas** al ejecutar la acción |

### Ejemplo detallado: MoverDesdeMesa(B, C)

Esta acción significa: "mover el bloque B desde la mesa hacia encima del bloque C."

```
  Acción: MoverDesdeMesa(B, C)
  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  │  Precondiciones:  { On(B, Mesa), Clear(B), Clear(C) }       │
  │                     ↑              ↑          ↑              │
  │                     B está en      nada       nada           │
  │                     la mesa        sobre B    sobre C        │
  │                                                              │
  │  Lista Add:       { On(B, C) }                               │
  │                     ↑                                        │
  │                     ahora B está sobre C                     │
  │                                                              │
  │  Lista Delete:    { On(B, Mesa), Clear(C) }                  │
  │                     ↑              ↑                         │
  │                     B ya no está   C ya no está              │
  │                     en la mesa     libre (B está encima)     │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
```

![Anatomía de una acción STRIPS]({{ '/16_planificacion_clasica/images/03_strips_action_anatomy.png' | url }})

**Cómo leer la figura:**

- **Caja azul (Precondiciones)**: lo que debe ser verdadero *antes* de ejecutar la acción. Si alguna precondición falta del estado actual, la acción **no se puede ejecutar**.
- **Caja verde (Lista Add)**: lo que se vuelve verdadero *después* de ejecutar la acción. Estas proposiciones se agregan al estado.
- **Caja roja (Lista Delete)**: lo que deja de ser verdadero. Estas proposiciones se eliminan del estado.

**¿Por qué tres partes?** Porque el mundo cambia de forma precisa:
- Las precondiciones garantizan que la acción tiene sentido físicamente (no puedes mover B si algo está encima).
- La lista add captura lo nuevo (B ahora está sobre C).
- La lista delete captura lo que ya no es cierto (B ya no está en la mesa, C ya no está libre).

> **¿Por qué necesitamos $\text{On}(B, \text{Mesa})$ en las precondiciones?**
> Uno podría pensar que basta con $\text{Clear}(B)$ y $\text{Clear}(C)$: si B está libre, se puede mover sin importar *dónde* esté. Físicamente eso es cierto — pero en STRIPS las precondiciones no solo verifican si la acción es *posible*, sino que aseguran que la **lista delete** va a limpiar la proposición correcta.
>
> La lista delete de $\text{MoverDesdeMesa}(B, C)$ elimina $\text{On}(B, \text{Mesa})$. Si B estuviera en realidad sobre A (no sobre la mesa), pasarían dos cosas malas:
> 1. La lista delete intenta eliminar $\text{On}(B, \text{Mesa})$ que no existe — inofensivo pero incorrecto.
> 2. $\text{On}(B, A)$ **sobrevive** porque nadie la elimina. El estado resultante dice que B está sobre A **y** sobre C al mismo tiempo — un estado inconsistente.
>
> STRIPS no tiene un verificador de consistencia — confía en que las definiciones de las acciones mantengan estados válidos. La precondición $\text{On}(B, \text{Mesa})$ garantiza que la acción solo se ejecute en el contexto correcto para que su lista delete haga la limpieza adecuada.

---

## 3. Aplicar una acción: transición de estado paso a paso

Veamos exactamente qué pasa cuando aplicamos $\text{MoverDesdeMesa}(B, C)$ al estado inicial.

### Paso 1 — Verificar precondiciones

¿Están todas las precondiciones en el estado actual?

| Precondición | ¿Está en $s_0$? |
|---|:---:|
| $\text{On}(B, \text{Mesa})$ | **Sí** ✓ |
| $\text{Clear}(B)$ | **Sí** ✓ |
| $\text{Clear}(C)$ | **Sí** ✓ |

Todas presentes → la acción **es aplicable**.

### Paso 2 — Eliminar la lista delete

Quitamos del estado las proposiciones de la lista delete:

$$s_0 - \text{Delete} = \{\ \text{On}(A, \text{Mesa}),\ \cancel{\text{On}(B, \text{Mesa})},\ \text{On}(C, \text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B),\ \cancel{\text{Clear}(C)}\ \}$$

Resultado intermedio: $\{\ \text{On}(A, \text{Mesa}),\ \text{On}(C, \text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\ \}$

### Paso 3 — Agregar la lista add

Agregamos las proposiciones de la lista add:

$$s_1 = \{\ \text{On}(A, \text{Mesa}),\ \text{On}(C, \text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\ \} \cup \{\ \text{On}(B, C)\ \}$$

### Resultado: estado $s_1$

$$s_1 = \{\ \text{On}(A, \text{Mesa}),\ \text{On}(B, C),\ \text{On}(C, \text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\ \}$$

Visualmente:

```
          ┌───┐
 ┌───┐    │ B │
 │ A │    ├───┤
 │   │    │ C │
 ═════    ═════
 mesa     mesa
```

![Transición de estado]({{ '/16_planificacion_clasica/images/04_state_transition.png' | url }})

**Cómo leer la figura:**

- **Panel izquierdo (ANTES)**: el estado $s_0$ con las proposiciones listadas. Las proposiciones que van a desaparecer están en rojo con tachado.
- **Panel central (ACCIÓN)**: la acción aplicada, con las listas delete (rojo) y add (verde) explícitas.
- **Panel derecho (DESPUÉS)**: el estado $s_1$ resultante. La proposición nueva $\text{On}(B, C)$ aparece en verde.

### La fórmula general

Para cualquier estado $s$ y acción $a$ cuyas precondiciones se cumplan:

$$s' = (s - \text{Delete}(a)) \cup \text{Add}(a)$$

En palabras: **quita lo que ya no es cierto, agrega lo que ahora es cierto, deja todo lo demás igual**.

---

## 4. Los tres esquemas de acción para Blocks World

Un **esquema de acción** es una plantilla parametrizada. Los parámetros (X, Y, Z) se reemplazan por bloques concretos (A, B, C) para obtener **acciones concretas** (ground actions).

### Esquema 1: Mover(X, Y, Z)

*Mover el bloque X desde el bloque Y hacia el bloque Z.*

```
Mover(X, Y, Z)

  Precondiciones:  { On(X, Y), Clear(X), Clear(Z) }
                     ↑          ↑          ↑
                     X está     nada       nada
                     sobre Y    sobre X    sobre Z

  Lista Add:       { On(X, Z), Clear(Y) }
                     ↑          ↑
                     X ahora    Y queda
                     sobre Z    libre

  Lista Delete:    { On(X, Y), Clear(Z) }
                     ↑          ↑
                     X ya no    Z ya no
                     sobre Y    está libre
```

**Restricción**: X, Y y Z deben ser bloques diferentes. Y y Z **no** pueden ser Mesa (para eso están los otros esquemas).

> **¿Por qué no necesitamos $\text{On}(Y, \text{Mesa})$ ni $\text{On}(Z, \text{Mesa})$ en las precondiciones?** Porque la acción no mueve ni a Y ni a Z — solo mueve a X. Lo único que le importa de Y es que X está encima (para eliminar $\text{On}(X, Y)$ y liberar Y). Lo único que le importa de Z es que está libre (para poner X encima). Dónde descansa Y (¿en la mesa? ¿sobre otro bloque?) y dónde descansa Z son irrelevantes — la acción no toca esas relaciones. En STRIPS, cada proposición en las precondiciones existe porque la lista add o la lista delete la necesita. Si la acción no modifica una relación, no necesita verificarla.

### Esquema 2: MoverAMesa(X, Y)

*Mover el bloque X desde el bloque Y hacia la mesa.*

```
MoverAMesa(X, Y)

  Precondiciones:  { On(X, Y), Clear(X) }
                     ↑          ↑
                     X está     nada
                     sobre Y    sobre X

  Lista Add:       { On(X, Mesa), Clear(Y) }
                     ↑             ↑
                     X ahora       Y queda
                     en la mesa    libre

  Lista Delete:    { On(X, Y) }
                     ↑
                     X ya no está sobre Y
```

**Nota**: no necesitamos $\text{Clear}(\text{Mesa})$ como precondición porque la mesa siempre puede sostener más bloques. Tampoco eliminamos $\text{Clear}(\text{Mesa})$ porque la mesa nunca se "llena".

### Esquema 3: MoverDesdeMesa(X, Z)

*Mover el bloque X desde la mesa hacia encima del bloque Z.*

```
MoverDesdeMesa(X, Z)

  Precondiciones:  { On(X, Mesa), Clear(X), Clear(Z) }
                     ↑              ↑          ↑
                     X está en      nada       nada
                     la mesa        sobre X    sobre Z

  Lista Add:       { On(X, Z) }
                     ↑
                     X ahora sobre Z

  Lista Delete:    { On(X, Mesa), Clear(Z) }
                     ↑              ↑
                     X ya no en     Z ya no
                     la mesa        está libre
```

### ¿Por qué tres esquemas y no uno solo?

Una pregunta natural: si un bloque libre se puede mover sin importar dónde esté (en la mesa o sobre otro bloque), ¿por qué no tener un solo esquema genérico $\text{Move}(X, \text{Destino})$ con una precondición tipo "B está en la mesa **o** B está sobre algún bloque"?

La razón es una **limitación del lenguaje STRIPS**: las precondiciones son una **conjunción** (un conjunto de proposiciones que deben ser **todas** verdaderas). No existe la disyunción (OR) en las precondiciones. No podemos escribir $\text{On}(B, \text{Mesa}) \lor \text{On}(B, A)$ como precondición.

Los tres esquemas son la forma en que STRIPS resuelve esta limitación: **enumera cada caso como una acción separada**. Cuando el planificador hace búsqueda hacia adelante, prueba las 18 acciones concretas contra el estado actual, y las precondiciones filtran automáticamente cuáles aplican:

- Si B está en la mesa → $\text{MoverDesdeMesa}(B, C)$ es aplicable, $\text{Mover}(B, A, C)$ no lo es.
- Si B está sobre A → $\text{Mover}(B, A, C)$ es aplicable, $\text{MoverDesdeMesa}(B, C)$ no lo es.

El planificador no necesita "saber" cuál usar — prueba todas y la física (las precondiciones) filtra las incorrectas.

> **Nota**: el lenguaje **ADL** (Action Description Language, Pednault 1989) extiende STRIPS con precondiciones disyuntivas, negación, efectos condicionales y cuantificadores. En ADL *sí* podríamos escribir un solo esquema genérico. Pero STRIPS, por su simplicidad, sigue siendo la base pedagógica y práctica de la planificación clásica.

---

## 5. Todas las acciones concretas para 3 bloques

Con bloques A, B, C, cada esquema se instancia reemplazando los parámetros por todas las combinaciones válidas. Listamos **cada una** — no saltamos ninguna:

### Instancias de Mover(X, Y, Z) — mover de bloque a bloque

| Acción | Precondiciones | Add | Delete |
|---|---|---|---|
| Mover(A, B, C) | {On(A,B), Clear(A), Clear(C)} | {On(A,C), Clear(B)} | {On(A,B), Clear(C)} |
| Mover(A, C, B) | {On(A,C), Clear(A), Clear(B)} | {On(A,B), Clear(C)} | {On(A,C), Clear(B)} |
| Mover(B, A, C) | {On(B,A), Clear(B), Clear(C)} | {On(B,C), Clear(A)} | {On(B,A), Clear(C)} |
| Mover(B, C, A) | {On(B,C), Clear(B), Clear(A)} | {On(B,A), Clear(C)} | {On(B,C), Clear(A)} |
| Mover(C, A, B) | {On(C,A), Clear(C), Clear(B)} | {On(C,B), Clear(A)} | {On(C,A), Clear(B)} |
| Mover(C, B, A) | {On(C,B), Clear(C), Clear(A)} | {On(C,A), Clear(B)} | {On(C,B), Clear(A)} |

**6 acciones** (3 bloques × 2 posibles soportes distintos).

### Instancias de MoverAMesa(X, Y) — mover de bloque a mesa

| Acción | Precondiciones | Add | Delete |
|---|---|---|---|
| MoverAMesa(A, B) | {On(A,B), Clear(A)} | {On(A,Mesa), Clear(B)} | {On(A,B)} |
| MoverAMesa(A, C) | {On(A,C), Clear(A)} | {On(A,Mesa), Clear(C)} | {On(A,C)} |
| MoverAMesa(B, A) | {On(B,A), Clear(B)} | {On(B,Mesa), Clear(A)} | {On(B,A)} |
| MoverAMesa(B, C) | {On(B,C), Clear(B)} | {On(B,Mesa), Clear(C)} | {On(B,C)} |
| MoverAMesa(C, A) | {On(C,A), Clear(C)} | {On(C,Mesa), Clear(A)} | {On(C,A)} |
| MoverAMesa(C, B) | {On(C,B), Clear(C)} | {On(C,Mesa), Clear(B)} | {On(C,B)} |

**6 acciones** (3 bloques × 2 posibles soportes).

### Instancias de MoverDesdeMesa(X, Z) — mover de mesa a bloque

| Acción | Precondiciones | Add | Delete |
|---|---|---|---|
| MoverDesdeMesa(A, B) | {On(A,Mesa), Clear(A), Clear(B)} | {On(A,B)} | {On(A,Mesa), Clear(B)} |
| MoverDesdeMesa(A, C) | {On(A,Mesa), Clear(A), Clear(C)} | {On(A,C)} | {On(A,Mesa), Clear(C)} |
| MoverDesdeMesa(B, A) | {On(B,Mesa), Clear(B), Clear(A)} | {On(B,A)} | {On(B,Mesa), Clear(A)} |
| MoverDesdeMesa(B, C) | {On(B,Mesa), Clear(B), Clear(C)} | {On(B,C)} | {On(B,Mesa), Clear(C)} |
| MoverDesdeMesa(C, A) | {On(C,Mesa), Clear(C), Clear(A)} | {On(C,A)} | {On(C,Mesa), Clear(A)} |
| MoverDesdeMesa(C, B) | {On(C,Mesa), Clear(C), Clear(B)} | {On(C,B)} | {On(C,Mesa), Clear(B)} |

**6 acciones** (3 bloques × 2 posibles destinos).

**Total: 18 acciones concretas** (6 + 6 + 6). No todas son aplicables en un estado dado — solo las que tienen sus precondiciones satisfechas. En el estado inicial $s_0$, donde los 3 bloques están en la mesa:

- ¿Mover(A, B, C)? Necesita On(A, B) — **no está** → no aplicable.
- ¿MoverAMesa(A, B)? Necesita On(A, B) — **no está** → no aplicable.
- ¿MoverDesdeMesa(A, B)? Necesita On(A, Mesa) ✓, Clear(A) ✓, Clear(B) ✓ → **aplicable**.

En $s_0$, solo las 6 acciones MoverDesdeMesa son aplicables (cualquier bloque puede ir sobre cualquier otro bloque, todos están en la mesa y libres).

---

## 6. El espacio de estados completo

Partiendo del estado inicial $s_0$ y aplicando todas las acciones posibles de forma sistemática (BFS), obtenemos el **espacio de estados completo**: todos los estados alcanzables y todas las transiciones entre ellos.

![Espacio de estados completo de Blocks World]({{ '/16_planificacion_clasica/images/05_blocks_world_state_space.png' | url }})

### Cómo leer la figura

- **Cada nodo** es un estado — muestra la configuración física de los bloques (rectángulos de colores apilados sobre la mesa).
- **Cada arista** conecta dos estados que difieren por una sola acción STRIPS. Las aristas son **bidireccionales**: si puedes ir de $s_i$ a $s_j$ con $\text{MoverDesdeMesa}(B, C)$, puedes volver con $\text{MoverAMesa}(B, C)$.
- El nodo con **borde verde punteado** es el estado inicial: A, B, C todos en la mesa.
- El nodo con **borde naranja punteado** es el estado meta: A sobre B sobre C sobre la mesa.
- Los nodos están organizados por **número de bloques en la mesa**: arriba (3 en mesa), medio (2 en mesa), abajo (1 en mesa = torre de 3).

### Estructura del espacio

| Bloques en mesa | Configuraciones | Descripción |
|:---:|:---:|---|
| 3 | 1 | Todos en la mesa (estado inicial) |
| 2 | 6 | Un bloque sobre otro, el tercero en la mesa |
| 1 | 6 | Torre de 3 bloques (6 permutaciones) |
| **Total** | **13** | |

El espacio es pequeño — **13 estados y 15 aristas** (transiciones bidireccionales). Es el análogo del árbol de Nim(1,2) con 12 nodos del módulo 15: lo suficientemente pequeño para visualizarlo completo, lo suficientemente rico para mostrar todos los conceptos.

---

**Siguiente:** [Búsqueda hacia adelante →](03_busqueda_hacia_adelante.md)
