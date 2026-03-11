---
title: "Heurísticas h(n)"
---

| Notebook | Colab |
|---------|:-----:|
| Notebook 02 — Búsqueda informada (Greedy, Dijkstra, A\*) | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/14_busqueda_informada/notebooks/02_busqueda_informada.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |

---

# Heurísticas $h(n)$: guiar la búsqueda con conocimiento

> *"A heuristic is a technique that seeks good enough solutions at the cost of completeness, accuracy, or precision."*

---

Dijkstra y A\* pueden guiar la búsqueda hacia la meta si tienen una estimación de cuánto falta. Esa estimación es la **función heurística** $h(n)$. Este capítulo define qué es, qué propiedades debe cumplir, y qué ocurre cuando esas propiedades se violan.

---

## 1. ¿Qué es $h(n)$?

$$h(n) = \text{estimación del costo mínimo desde el nodo } n \text{ hasta la meta más cercana}$$

**$h(n)$ es conocimiento del dominio**, no algo que calcule automáticamente el algoritmo. El diseñador del algoritmo decide cómo calcularla. Esto es lo que hace a la búsqueda "informada": el algoritmo *sabe algo* sobre la estructura del problema.

Ejemplos concretos:

| Problema | $h(n)$ | Intuición |
|---|---|---|
| Navegación en cuadrícula 4-conexa | Distancia Manhattan $= \|r_n - r_G\| + \|c_n - c_G\|$ | Nunca podemos hacer menos pasos que la distancia "de taxi" |
| Navegación en mapa de carreteras | Distancia en línea recta (Euclidiana) | Nunca podemos ir más rápido que en línea recta |
| Puzzle de 8 piezas | Número de fichas fuera de su lugar | Cada ficha descolocada necesita al menos un movimiento |
| Sin información | $h(n) = 0$ para todo $n$ | No sabemos nada → el algoritmo se comporta como Dijkstra |

---

## 2. Admisibilidad: nunca sobreestimar

La propiedad más importante que debe cumplir $h(n)$:

$$\boxed{h(n) \leq h^{∗}(n) \quad \forall n}$$

donde $h^{∗}(n)$ es el **costo real óptimo** desde $n$ hasta la meta.

Una heurística **admisible** nunca exagera lo que falta. Es optimista — puede subestimar, pero no sobreestimar.

**¿Por qué importa esto?** Si $h$ sobreestima, A\* podría "penalizar" injustamente nodos que son parte del camino óptimo, y saltarse la solución óptima por buscar una que *parece* más barata según $h$.

:::example{title="Comprobando admisibilidad: distancia Manhattan en cuadrícula"}
En una cuadrícula 4-conexa con paredes, el camino real desde $(r_n, c_n)$ hasta $(r_G, c_G)$ nunca puede ser más corto que la distancia Manhattan $|r_n - r_G| + |c_n - c_G|$, porque:

- Cada movimiento solo cambia una coordenada en ±1.
- Las paredes solo pueden forzar **rodeos** (caminos más largos, nunca más cortos).

Por tanto: $h_{\text{Manhattan}}(n) \leq h^{∗}(n)$ siempre → **admisible**.
:::

:::example{title="Heurística inadmisible — qué pasa"}
Supón que usamos $h(n) = \text{Manhattan}(n, \text{meta}) \times 2$. Esta heurística **sobreestima**.

Consecuencia: A\* puede rechazar el camino óptimo porque $f = g + h$ parece demasiado alto, y devolver un camino subóptimo. El algoritmo termina rápido pero la solución es incorrecta.

Moraleja: con heurística inadmisible pierdes la garantía de optimalidad.
:::

---

## 3. Consistencia (monotonicidad): la propiedad más fuerte

La **consistencia** (también llamada monotonicidad) es más restrictiva que la admisibilidad:

$$\boxed{h(n) \leq \text{costo}(n, n') + h(n') \quad \forall \text{ arista } (n, n')}$$

Esto es la **desigualdad triangular**: la estimación desde $n$ no puede superar el costo de ir a $n'$ más la estimación desde $n'$.

```
        n
       / \
      c   h(n) ≤?
     /
    n'
     \
      h(n')

Consistencia exige: h(n) ≤ c(n,n') + h(n')
```

**Intuición: los valores de $h$ no pueden dar saltos bruscos.** Si estoy en $n$ y doy un paso a $n'$, mi estimación del costo restante debería cambiar *suavemente* — no puede caer de golpe más de lo que costó el paso. Formalmente: $h(n) - h(n') \leq \text{costo}(n, n')$.

Otra forma de verlo: si la estimación desde $n$ pudiera ser mucho mayor que el costo del paso más la estimación desde $n'$, significaría que $h$ "inventa" dificultad donde no la hay — y A\* podría confundirse pensando que $n$ es un nodo muy difícil de continuar, cuando en realidad llegar a $n'$ es barato.

**Relación entre consistencia y admisibilidad:**

> Consistencia $\Rightarrow$ Admisibilidad (pero no al revés)

Una heurística consistente es siempre admisible. Pero **una heurística admisible puede no ser consistente**: puede subestimar correctamente el costo total desde cada nodo, pero hacerlo de forma "irregular" — subiendo y bajando entre nodos adyacentes de manera inconsistente con los costos de las aristas.

**¿Por qué importa la consistencia?** Con una heurística consistente, los valores $f(n) = g(n) + h(n)$ son **monótonamente no decrecientes** a lo largo de cualquier camino. Esto significa que la primera vez que A\* expande un nodo, ha encontrado el camino óptimo hasta él — nunca necesitamos reabrir un nodo del conjunto `explorado`.

Sin consistencia (solo admisibilidad), A\* todavía encuentra la solución óptima, pero podría necesitar reabrir nodos ya explorados al descubrir caminos más baratos. La implementación se complica: en lugar de un conjunto `explorado` definitivo, habría que comparar costos al reinsertar.

:::example{title="Comprobando consistencia: distancia Manhattan"}
Para la distancia Manhattan en cuadrícula 4-conexa:

- Cada movimiento cambia exactamente una coordenada en ±1.
- Si nos movemos de $n = (r, c)$ a $n' = (r+1, c)$ (un paso abajo), entonces:
  - $\text{costo}(n, n') = 1$
  - $h(n') = |r+1 - r_G| + |c - c_G|$
  - $h(n) = |r - r_G| + |c - c_G|$
  - La diferencia $h(n) - h(n') \leq 1 = \text{costo}(n, n')$ por la desigualdad triangular de valores absolutos.

Por tanto Manhattan es **consistente** (y por tanto admisible).
:::

:::example{title="Contraejemplo: admisible pero NO consistente"}
Construimos una heurística admisible que viola la consistencia en un grafo de 3 nodos:

```
Grafo:
  S ──1── A ──1── Meta

h* (costo real óptimo):
  h*(S) = 2,  h*(A) = 1,  h*(Meta) = 0

Heurística h (admisible: h ≤ h* en todo nodo):
  h(S) = 2,  h(A) = 0,  h(Meta) = 0
```

**¿Es admisible?** Sí: $h(S)=2 \leq h^{∗}(S)=2$, $h(A)=0 \leq h^{∗}(A)=1$, $h(\text{Meta})=0$. Nunca sobreestima.

**¿Es consistente?** Comprobamos la arista $S \to A$:

$$h(S) \leq \text{costo}(S, A) + h(A) \quad \Rightarrow \quad 2 \leq 1 + 0 = 1 \quad \text{¡FALSO!}$$

La consistencia falla porque $h$ cae bruscamente de 2 a 0 al pasar de $S$ a $A$, pero el paso solo cuesta 1. Es como si la heurística dijera «desde $S$ hay mucho que caminar, pero desde $A$ ya estás prácticamente ahí» — cuando en realidad solo se dio un paso de costo 1.

**Consecuencia práctica**: A\* con esta $h$ podría expandir $A$ con $f(A) = g(A) + h(A) = 1 + 0 = 1$ y marcarlo como explorado. Pero luego, al llegar a Meta desde $A$ con $g(\text{Meta})=2$, el valor $f=2$ es mayor que $f(A)=1$ previo. Los valores de $f$ no son monótonos → el conjunto `explorado` no es fiable sin reapertura.
:::

---

## 4. El espectro de calidad de $h$

La calidad de la heurística determina directamente cuántos nodos expande A\*:

```
Calidad de h(n)                  Comportamiento de A*
─────────────────────────────────────────────────────────────────
h(n) = 0 para todo n    →  Dijkstra puro: expande en todas
                            direcciones, O(b^d) nodos

h(n) = buena estimación  →  A* enfocado: mucho menos que O(b^d),
admisible y consistente     solo las "zonas prometedoras"

h(n) = h*(n) exacta     →  A* perfecto: expande solo los nodos
(imposible en práctica)     del camino óptimo, O(d) nodos

h(n) > h*(n) en algún n →  A* inadmisible: rápido pero puede
(sobreestima)               devolver solución subóptima
```

![Espectro de calidad de la heurística]({{ '/14_busqueda_informada/images/03_heuristic_spectrum.png' | url }})

El problema: S y G están en la misma columna con una pared horizontal entre ellos. $h_{\text{Manhattan}}(S, G) = 17$, pero el camino real requiere rodear la pared: $h^{∗}(S) = 35$ (más del doble). Cuatro heurísticas, misma solución óptima:

| Heurística | Nodos expandidos | Forma visible |
|---|:---:|---|
| $h = 0$ (Dijkstra) | 452 | Inundación rectangular — sin dirección |
| $h = \frac{h_M}{2}$ (débil) | 435 | Cruz ancha — ligero sesgo hacia abajo |
| $h = h_M$ (Manhattan) | 284 | Columna hacia abajo + cruz en la pared |
| $h = h^{∗}$ (exacta) | 171 | Corredor en L — izquierda, abajo, derecha |

**La clave**: Manhattan dice «baja recto 17 pasos» pero la pared lo obliga a desviarse. A\* con Manhattan sigue esa intuición equivocada hasta chocar. A\* con $h^{∗}$ sabe desde el primer paso que debe ir izquierda.

---

## 5. Tres heurísticas concretas para estudiar

### Distancia Manhattan (cuadrícula 4-conexa)

$$h(n) = |r_n - r_G| + |c_n - c_G|$$

- **Admisible**: cada paso cambia una coordenada en ±1, así que el número mínimo de pasos es la suma de diferencias absolutas.
- **Consistente**: la desigualdad triangular se cumple por la propiedad de los valores absolutos.
- **Uso**: laberintos, mapas de cuadrícula, puzzles de deslizamiento.

### Distancia Euclidiana (mapa 2D)

$$h(n) = \sqrt{(x_n - x_G)^2 + (y_n - y_G)^2}$$

- **Admisible**: la línea recta es siempre el camino más corto posible.
- **Consistente**: se hereda de la desigualdad triangular geométrica.
- **Uso**: navegación en mapas, robótica, GPS.

### Fichas fuera de lugar (puzzle de 8 piezas)

$$h(n) = \text{número de fichas que no están en su posición final}$$

- **Admisible**: cada ficha descolocada requiere al menos un movimiento.
- **Consistente**: mover una ficha cambia el recuento en a lo sumo ±1 = costo del movimiento.
- **Uso**: benchmark clásico de A\*. Dominada por Manhattan (ver capítulo 06).

---

## 6. Recordatorio: la notación de complejidad

Como en el módulo anterior, usamos:

| Símbolo | Significado | Nota |
|:-------:|-------------|------|
| $b$ | Factor de ramificación **máximo** | Peor caso; en grafos uniformes = promedio |
| $d$ | Profundidad de la solución óptima | Número de aristas en el camino mínimo |
| $m$ | Profundidad máxima del grafo | Puede ser $\gg d$ |

Para A\* añadimos:
- $b^{∗}$ — **factor de ramificación efectivo**: si A\* expande $N$ nodos encontrando solución a profundidad $d$, entonces $b^{∗} \approx N^{1/d}$. Un buen indicador de la calidad de $h$: $b^{∗} = 1$ es perfecto, $b^{∗} = b$ es Dijkstra.

---

**Siguiente:** [Greedy best-first →](03_greedy.md)
