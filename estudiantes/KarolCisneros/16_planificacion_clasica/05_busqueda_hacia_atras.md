---
title: "Búsqueda hacia atrás"
---

| Notebook | Colab |
|---------|:-----:|
| Notebook 02 — Planificación forward | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/16_planificacion_clasica/notebooks/02_planificacion_forward.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |

---

# Búsqueda hacia atrás: del objetivo al inicio

> *"Begin with the end in mind."*
> — Stephen R. Covey

---

Hasta ahora hemos construido planes buscando **hacia adelante**: partimos del estado inicial $s_0$, aplicamos acciones, y avanzamos hasta alcanzar la meta $G$. Esa dirección es natural — imita cómo ejecutamos acciones en el mundo real. Pero no es la única dirección posible.

La **búsqueda hacia atrás** (*backward search* o *regression*) hace exactamente lo contrario: parte de la meta $G$ y pregunta "¿qué acción pudo haber producido esta situación?", retrocediendo paso a paso hasta llegar al estado inicial $s_0$. Al recorrer la cadena de padres desde $s_0$ hacia $G$, las acciones se leen directamente en orden de ejecución.

### El panorama general

Vamos a construir un **árbol de búsqueda donde la raíz es la meta** $G$. Cada nodo del árbol no es un estado completo del mundo, sino un **subobjetivo**: un conjunto de proposiciones que *necesitamos* que sean verdaderas. En cada nodo preguntamos: "¿qué acción, ejecutada justo antes, podría haber producido este subobjetivo?". Cada respuesta genera un nuevo subobjetivo hijo — lo que necesitaba ser verdad *antes* de esa acción.

```
                        G                          ← raíz: la meta
                     ╱     ╲
              acción a₁    acción a₂               ← acciones que producen algo de G
               ╱               ╲
             g₁                 g₂                 ← subobjetivos: ¿qué debe cumplirse antes?
           ╱    ╲                 ╲
       acción a₃  acción a₄     acción a₅
        ╱            ╲               ╲
      g₃              g₄             g₅
       ⋮               ⋮              ⋮
      g_k ⊆ s₀  ← ÉXITO: s₀ ya satisface todo lo que pedimos, no necesitamos más acciones
```

La búsqueda termina cuando encontramos un subobjetivo $g_k$ que está **completamente contenido en $s_0$** — es decir, todo lo que $g_k$ pide ya es verdad en el estado inicial. En ese momento, el camino desde $g_k$ hasta la raíz $G$ nos da el plan: las acciones a lo largo de ese camino, leídas desde $g_k$ hacia $G$, son exactamente las acciones a ejecutar en orden.

Esta sección explica la idea, la formaliza, la ejecuta paso a paso en Blocks World, y la compara con la búsqueda hacia adelante.

---

## 1. La idea — buscar desde la meta

### Analogía: las llaves perdidas

Imagina que perdiste tus llaves. Tienes dos estrategias:

- **Hacia adelante**: reconstruir cada paso desde que te despertaste. "Me levanté, fui a la cocina, preparé café, agarré la mochila..." — son decenas de pasos, la mayoría irrelevantes.
- **Hacia atrás**: empezar por el final. "¿Dónde estuve por última vez que sé que las tenía? En el coche. ¿Qué hice después de bajar del coche? Fui al escritorio. ¿Están en el escritorio?" — pocos pasos, todos relevantes.

La búsqueda hacia atrás funciona igual: en vez de explorar todas las acciones posibles desde el inicio (muchas de las cuales no tienen nada que ver con la meta), empezamos desde lo que queremos lograr y preguntamos "¿qué necesito que sea verdad *justo antes* para que esto se cumpla?"

### Comparación directa

| | Hacia adelante (*forward*) | Hacia atrás (*backward*) |
|---|---|---|
| **Empieza en** | $s_0$ (estado inicial) | $G$ (meta) |
| **Pregunta** | ¿Qué puedo hacer desde aquí? | ¿Qué acción pudo producir esto? |
| **Expande** | Acciones **aplicables** ($\text{Pre}(a) \subseteq s$) | Acciones **relevantes** ($\text{Add}(a) \cap g \neq \emptyset$) |
| **Termina cuando** | $G \subseteq s$ (meta satisfecha) | $g \subseteq s_0$ (subobjetivo en estado inicial) |
| **Dirección** | $s_0 \longrightarrow G$ | $G \longrightarrow s_0$ |

![Forward vs backward search]({{ '/16_planificacion_clasica/images/11_forward_vs_backward.png' | url }})

**Cómo leer la figura:** a la izquierda, la búsqueda forward parte de $s_0$ (los tres bloques en la mesa) y aplica acciones hacia adelante, generando **estados completos** en cada paso hasta alcanzar $G$. A la derecha, la búsqueda backward parte de $G$ (la torre A-B-C) y aplica **regresión** hacia atrás, generando **subobjetivos** (descripciones parciales del mundo) hasta llegar a algo que $s_0$ satisface. Nota la diferencia: los nodos forward son estados completos (cajas con borde sólido), los nodos backward son subobjetivos (cajas con borde punteado).

### Subobjetivos, no estados completos

Hay una diferencia fundamental entre las dos direcciones. En la búsqueda hacia adelante, cada nodo del árbol de búsqueda es un **estado completo**: un conjunto que especifica exactamente qué proposiciones son verdaderas y cuáles no. Por ejemplo, el estado inicial $s_0 = \{\text{On}(A,\text{Mesa}), \text{On}(B,\text{Mesa}), \text{On}(C,\text{Mesa}), \text{Clear}(A), \text{Clear}(B), \text{Clear}(C)\}$ describe todo el mundo.

En la búsqueda hacia atrás, los nodos **no** son estados completos. Son **subobjetivos** — conjuntos parciales de proposiciones que *necesitamos* que sean verdaderas. Un subobjetivo dice "me importa que estas cosas sean ciertas; el resto no me importa".

Por ejemplo, la meta $G = \{\text{On}(A,B), \text{On}(B,C), \text{On}(C,\text{Mesa}), \text{Clear}(A)\}$ especifica 4 proposiciones. No dice nada sobre si $\text{Clear}(B)$ es verdadera o falsa — simplemente no le importa. Eso es un subobjetivo: una descripción **parcial** del mundo.

> **Observación:** Esta distinción es clave. En forward search, sabemos exactamente en qué estado estamos. En backward search, trabajamos con descripciones incompletas — sabemos qué *necesitamos*, pero no el estado completo del mundo. Eso hace que la regresión sea conceptualmente más abstracta, pero también potencialmente más eficiente: al ignorar lo que no importa, podemos evitar explorar estados irrelevantes.

---

## 2. Definición formal — acciones relevantes y regresión

Ya tenemos la intuición: construimos un árbol desde $G$ hacia atrás, y cada nodo es un subobjetivo. Ahora necesitamos formalizar tres cosas:

1. **¿Qué acciones podemos usar en cada paso?** → acciones *relevantes* (contribuyen algo) y *consistentes* (no destruyen nada).
2. **¿Cómo calculamos el nuevo subobjetivo?** → la fórmula de *regresión*.
3. **¿Cuándo terminamos?** → cuando el subobjetivo está contenido en $s_0$.

### 2.1 Subobjetivos (estados parciales)

Un **subobjetivo** es un conjunto $g \subseteq P$ de proposiciones que necesitamos que sean verdaderas. No describe un estado completo del mundo — solo las proposiciones que importan.

- El subobjetivo inicial de la búsqueda hacia atrás es la meta del problema: $g_0 = G$.
- En cada paso, la regresión produce un nuevo subobjetivo $g_{i+1}$ que representa "lo que necesita ser verdad *antes* de ejecutar la acción elegida".
- La búsqueda termina cuando el subobjetivo $g_i$ es un subconjunto del estado inicial: $g_i \subseteq s_0$.

### 2.2 Acción relevante

No todas las acciones sirven para un subobjetivo dado. Solo nos interesan las acciones que **contribuyen** — es decir, que logran al menos una de las proposiciones que necesitamos.

Una acción $a$ es **relevante** para un subobjetivo $g$ si su lista Add contiene al menos una proposición del subobjetivo:

$$\text{Add}(a) \cap g \neq \emptyset$$

En palabras: la acción produce algo que necesitamos. Si una acción no agrega nada de lo que buscamos, no tiene sentido considerarla — sería como buscar las llaves en un cuarto donde nunca entraste.

**Ejemplo.** Subobjetivo $g = \{\text{On}(A,B),\ \text{On}(B,C)\}$. Evaluamos dos acciones:

| Acción | $\text{Add}(a)$ | $\text{Add}(a) \cap g$ | ¿Relevante? |
|---|---|---|:---:|
| MoverDesdeMesa(A,B) | $\{\text{On}(A,B)\}$ | $\{\text{On}(A,B)\} \neq \emptyset$ | **Sí** ✓ |
| MoverDesdeMesa(C,A) | $\{\text{On}(C,A)\}$ | $\emptyset$ | **No** ✗ |

MoverDesdeMesa(A,B) es relevante porque produce $\text{On}(A,B)$, que es algo que necesitamos. MoverDesdeMesa(C,A) produce $\text{On}(C,A)$, que no aparece en nuestro subobjetivo — no nos ayuda.

### 2.3 Acción consistente

Que una acción sea relevante no basta. También necesitamos que **no destruya** nada que necesitamos. Una acción puede agregar algo útil pero al mismo tiempo borrar otra cosa que también era parte de nuestro subobjetivo.

Una acción relevante $a$ es **consistente** con el subobjetivo $g$ si su lista Delete no elimina ninguna proposición del subobjetivo:

$$\text{Del}(a) \cap g = \emptyset$$

En palabras: la acción no destruye nada de lo que necesitamos. Si lo hiciera, sería contraproducente — estaría resolviendo un subproblema mientras crea otro.

**Ejemplo 1 — acción consistente.** Subobjetivo $g = \{\text{On}(A,B),\ \text{On}(B,C),\ \text{Clear}(A)\}$.

Acción MoverDesdeMesa(A,B):
- $\text{Del}(\text{MoverDesdeMesa}(A,B)) = \{\text{On}(A,\text{Mesa}),\ \text{Clear}(B)\}$
- $\text{Del}(a) \cap g = \{\text{On}(A,\text{Mesa}),\ \text{Clear}(B)\} \cap \{\text{On}(A,B),\ \text{On}(B,C),\ \text{Clear}(A)\} = \emptyset$
- Ninguna proposición eliminada está en $g$ → **consistente** ✓

La acción borra $\text{On}(A,\text{Mesa})$ y $\text{Clear}(B)$, pero ninguna de esas dos proposiciones está en nuestro subobjetivo. No nos importa que desaparezcan.

**Ejemplo 2 — acción inconsistente.** Subobjetivo $g = \{\text{On}(A,B),\ \text{Clear}(B)\}$.

Acción MoverDesdeMesa(A,B):
- $\text{Del}(\text{MoverDesdeMesa}(A,B)) = \{\text{On}(A,\text{Mesa}),\ \text{Clear}(B)\}$
- $\text{Del}(a) \cap g = \{\text{Clear}(B)\} \neq \emptyset$
- La acción borra $\text{Clear}(B)$, que está en $g$ → **inconsistente** ✗

Aquí la acción MoverDesdeMesa(A,B) coloca A encima de B, lo cual produce $\text{On}(A,B)$ (bien), pero destruye $\text{Clear}(B)$ (mal). No podemos usarla porque viola nuestro propio subobjetivo — necesitamos que B quede libre, pero la acción lo tapa.

> **Observación:** La condición de consistencia filtra acciones que serían "un paso adelante, un paso atrás". Sin esta condición, la búsqueda podría generar subobjetivos imposibles de satisfacer.

> **¿Y si necesito esa acción inconsistente?** Que una acción sea inconsistente con un subobjetivo *particular* no significa que la búsqueda la descarte para siempre. La consistencia es un filtro **local**: prohíbe usar la acción como paso *inmediatamente anterior* a ese subobjetivo específico. Pero la misma acción puede ser perfectamente relevante y consistente para otro subobjetivo en otra rama del árbol.
>
> Por ejemplo, si $g = \{\text{On}(A,B),\ \text{Clear}(B)\}$ y MoverDesdeMesa(A,B) es inconsistente aquí (borra Clear(B)), eso simplemente indica que esa combinación de requisitos no puede lograrse de golpe con esa acción. El BFS sigue explorando otras ramas, y si existe una solución que usa MoverDesdeMesa(A,B) en otro punto del plan, la encontrará. El algoritmo sigue siendo **completo**: si existe un plan, lo encontrará.

### 2.4 La fórmula de regresión

Ahora viene el corazón de la búsqueda hacia atrás. Dado un subobjetivo $g$ y una acción $a$ que es relevante y consistente, la **regresión** produce un nuevo subobjetivo:

$$\text{regress}(g,\ a) = (g - \text{Add}(a)) \cup \text{Pre}(a)$$

Desglosamos la fórmula en dos pasos:

**Paso 1 — Quitar lo que la acción produce:**

$$g - \text{Add}(a)$$

Eliminamos del subobjetivo las proposiciones que la acción $a$ se encargará de producir. Ya no necesitamos que estén previamente — la acción las creará.

**Paso 2 — Agregar lo que la acción necesita:**

$$(\ldots) \cup \text{Pre}(a)$$

Añadimos las precondiciones de $a$. Ahora necesitamos que estas proposiciones sean verdaderas *antes* de ejecutar $a$ — porque sin ellas, $a$ no puede ejecutarse.

**Resultado:** el nuevo subobjetivo $g' = \text{regress}(g, a)$ responde la pregunta: "¿qué debe ser verdad en el mundo para que, al ejecutar $a$, obtengamos todo lo que $g$ pide?"

### Comparación: aplicar (forward) vs regresar (backward)

La regresión es la **operación espejo** de la aplicación de acciones que usamos en forward search. Recordemos ambas fórmulas lado a lado:

| | **Forward:** aplicar acción | **Backward:** regresar acción |
|---|---|---|
| **Fórmula** | $s' = (s - \text{Del}(a)) \cup \text{Add}(a)$ | $g' = (g - \text{Add}(a)) \cup \text{Pre}(a)$ |
| **Entrada** | Estado completo $s$ | Subobjetivo $g$ |
| **Salida** | Nuevo estado completo $s'$ | Nuevo subobjetivo $g'$ |
| **Paso 1: quitar** | Quitar lo que la acción **destruye** (Del) | Quitar lo que la acción **produce** (Add) |
| **Paso 2: agregar** | Agregar lo que la acción **produce** (Add) | Agregar lo que la acción **requiere** (Pre) |
| **Pregunta** | "¿Cómo queda el mundo *después* de $a$?" | "¿Qué debe ser verdad *antes* de $a$?" |
| **Dirección** | $s \xrightarrow{a} s'$ (avanza hacia $G$) | $g \xleftarrow{a} g'$ (retrocede hacia $s_0$) |

La simetría es casi perfecta: donde forward usa Del y Add, backward usa Add y Pre. La lógica es la misma — en forward quitamos lo que $a$ destruye y agregamos lo que produce; en backward quitamos lo que $a$ ya se encargará de producir y agregamos lo que $a$ necesita para poder ejecutarse.

La siguiente figura muestra ambas operaciones aplicadas a la **misma acción** MoverDesdeMesa(A,B), una desde $s_0$ (forward) y otra desde $G$ (backward). Observa cómo en cada caso se quitan y agregan proposiciones distintas, pero la estructura de los dos pasos es idéntica.

![Aplicar vs regresar]({{ '/16_planificacion_clasica/images/14_apply_vs_regress.png' | url }})

**Cómo leer la figura:** a la izquierda, forward aplica MoverDesdeMesa(A,B) al estado $s_0$ — elimina On(A,Mesa) y Clear(B) (tachados en rojo), luego agrega On(A,B) (marcado en verde). A la derecha, backward regresa la misma acción desde $G$ — elimina On(A,B) del subobjetivo (ya no hace falta pedirlo), luego agrega las precondiciones On(A,Mesa) y Clear(B) (marcados en verde). La misma acción, pero cada dirección quita y agrega cosas diferentes.

En resumen, la regresión responde una pregunta sencilla: **"si quiero que $g$ sea verdad *después* de ejecutar $a$, ¿qué necesita ser verdad *antes*?"**. Lo que $a$ produce (Add) ya no necesito pedirlo — $a$ se encargará. Pero lo que $a$ requiere (Pre), ahora tengo que pedirlo yo.

**Ejemplo completo.** Subobjetivo $g = \{\text{On}(A,B),\ \text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A)\}$. Acción $a = \text{MoverDesdeMesa}(A,B)$:

- $\text{Pre}(a) = \{\text{On}(A,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\}$
- $\text{Add}(a) = \{\text{On}(A,B)\}$
- $\text{Del}(a) = \{\text{On}(A,\text{Mesa}),\ \text{Clear}(B)\}$

Verificamos: ¿relevante? $\text{Add}(a) \cap g = \{\text{On}(A,B)\} \neq \emptyset$ → sí. ¿Consistente? $\text{Del}(a) \cap g = \emptyset$ → sí.

Regresión:

$$\text{regress}(g,\ a) = (\{\text{On}(A,B),\ \text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A)\} - \{\text{On}(A,B)\}) \cup \{\text{On}(A,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\}$$

Paso 1 — quitar $\text{Add}(a)$:

$$\{\text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A)\}$$

Paso 2 — agregar $\text{Pre}(a)$:

$$\{\text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A)\} \cup \{\text{On}(A,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\}$$

$$= \{\text{On}(A,\text{Mesa}),\ \text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\}$$

El nuevo subobjetivo dice: "necesito que A esté en la mesa, B esté sobre C, C esté en la mesa, A esté libre, y B esté libre". Si eso se cumple, entonces puedo ejecutar MoverDesdeMesa(A,B) y obtener el subobjetivo original $g$.

---

## 3. Ejemplo paso a paso — regresión en Blocks World

Usamos el mismo ejemplo de toda la sección: tres bloques todos en la mesa, queremos apilarlos A sobre B sobre C.

- **Estado inicial:** $s_0 = \{\text{On}(A,\text{Mesa}),\ \text{On}(B,\text{Mesa}),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B),\ \text{Clear}(C)\}$
- **Meta:** $G = \{\text{On}(A,B),\ \text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A)\}$

Vamos a construir el árbol de búsqueda hacia atrás. Empezamos con $G$ como raíz, evaluamos qué acciones son relevantes y consistentes, calculamos la regresión para cada una, y repetimos hasta que algún subobjetivo esté contenido en $s_0$.

```
Paso 0:   frontera = { G }     explorado = { }
Paso 1:   expandir G  →  generar g₁, g₂, g₃, ...  (uno por cada acción relevante y consistente)
Paso 2:   expandir g₁ →  generar g₄, g₅, ...
          ...hasta encontrar g_k ⊆ s₀
```

### Paso 1 de regresión

**Subobjetivo actual:** $g_0 = G = \{\text{On}(A,B),\ \text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A)\}$

**Test de terminación:** ¿$g_0 \subseteq s_0$? Necesitamos $\text{On}(A,B) \in s_0$ — no está (A está en la mesa, no sobre B). → No hemos terminado.

Ahora buscamos acciones relevantes y consistentes. Revisemos las 18 acciones del dominio y veamos cuáles pasan ambos filtros.

---

**Acción MoverDesdeMesa(A,B):**

- $\text{Add} = \{\text{On}(A,B)\}$
- $\text{Add} \cap g_0 = \{\text{On}(A,B)\} \neq \emptyset$ → **relevante** ✓
- $\text{Del} = \{\text{On}(A,\text{Mesa}),\ \text{Clear}(B)\}$
- $\text{Del} \cap g_0 = \emptyset$ (ni $\text{On}(A,\text{Mesa})$ ni $\text{Clear}(B)$ están en $g_0$) → **consistente** ✓

Regresión:

$$\text{regress}(g_0,\ \text{MoverDesdeMesa}(A,B)) = (g_0 - \{\text{On}(A,B)\}) \cup \{\text{On}(A,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\}$$

$$= \{\text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A)\} \cup \{\text{On}(A,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\}$$

$$= \{\text{On}(A,\text{Mesa}),\ \text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\}$$

Este es $g_1$. Lo agregamos a la frontera.

---

**Acción MoverDesdeMesa(C,A) — ejemplo de acción NO relevante:**

- $\text{Add} = \{\text{On}(C,A)\}$
- $\text{Add} \cap g_0 = \emptyset$ ($\text{On}(C,A)$ no está en $g_0$) → **no relevante** ✗

No nos interesa. Esta acción coloca C sobre A, que no tiene nada que ver con nuestra meta. Descartada.

---

**Acción MoverDesdeMesa(B,C):**

- $\text{Add} = \{\text{On}(B,C)\}$
- $\text{Add} \cap g_0 = \{\text{On}(B,C)\} \neq \emptyset$ → **relevante** ✓
- $\text{Del} = \{\text{On}(B,\text{Mesa}),\ \text{Clear}(C)\}$
- $\text{Del} \cap g_0 = \emptyset$ (ni $\text{On}(B,\text{Mesa})$ ni $\text{Clear}(C)$ están en $g_0$) → **consistente** ✓

Regresión:

$$\text{regress}(g_0,\ \text{MoverDesdeMesa}(B,C)) = (g_0 - \{\text{On}(B,C)\}) \cup \{\text{On}(B,\text{Mesa}),\ \text{Clear}(B),\ \text{Clear}(C)\}$$

$$= \{\text{On}(A,B),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A)\} \cup \{\text{On}(B,\text{Mesa}),\ \text{Clear}(B),\ \text{Clear}(C)\}$$

$$= \{\text{On}(A,B),\ \text{On}(B,\text{Mesa}),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B),\ \text{Clear}(C)\}$$

Este subobjetivo todavía contiene $\text{On}(A,B)$, que no está en $s_0$. No hemos terminado, pero lo agregamos a la frontera como candidato.

---

**Acción Mover(A,C,B) — ejemplo de acción relevante pero inconsistente:**

- $\text{Add} = \{\text{On}(A,B),\ \text{Clear}(C)\}$
- $\text{Add} \cap g_0 = \{\text{On}(A,B)\} \neq \emptyset$ → **relevante** ✓
- $\text{Del} = \{\text{On}(A,C),\ \text{Clear}(B)\}$
- $\text{Del} \cap g_0 = \emptyset$ (ni $\text{On}(A,C)$ ni $\text{Clear}(B)$ están en $g_0$) → **consistente** ✓

En este caso, Mover(A,C,B) también pasa ambos filtros. Su regresión produce:

$$\text{regress}(g_0,\ \text{Mover}(A,C,B)) = (g_0 - \{\text{On}(A,B),\ \text{Clear}(C)\}) \cup \{\text{On}(A,C),\ \text{Clear}(A),\ \text{Clear}(B)\}$$

$$= \{\text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A)\} \cup \{\text{On}(A,C),\ \text{Clear}(A),\ \text{Clear}(B)\}$$

$$= \{\text{On}(A,C),\ \text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\}$$

Este subobjetivo pide $\text{On}(A,C)$ y $\text{On}(B,C)$ simultáneamente — ¡ambos bloques encima de C! Eso es **físicamente imposible** en Blocks World (C solo tiene espacio para un bloque encima). La búsqueda lo agregará a la frontera, pero nunca podrá llegar a $s_0$ desde ahí. Es un callejón sin salida.

> **Observación:** La regresión no detecta inconsistencias semánticas — puede generar subobjetivos mutuamente excluyentes. La búsqueda los explorará y eventualmente los descartará (nunca llegarán a $s_0$), pero gastará tiempo en ellos. Detectar estas incompatibilidades requiere análisis adicional (como *mutex* en Graphplan), que no cubrimos aquí.

---

Para esta traza, sigamos la rama más directa: elegimos $g_1$ (el resultado de regresar con MoverDesdeMesa(A,B)) como siguiente nodo a expandir.

---

### Paso 2 de regresión

**Subobjetivo actual:** $g_1 = \{\text{On}(A,\text{Mesa}),\ \text{On}(B,C),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\}$

**Test de terminación:** ¿$g_1 \subseteq s_0$? Necesitamos $\text{On}(B,C) \in s_0$ — no está (B está en la mesa, no sobre C). → No hemos terminado.

Buscamos acciones relevantes y consistentes para $g_1$.

---

**Acción MoverDesdeMesa(B,C):**

- $\text{Add} = \{\text{On}(B,C)\}$
- $\text{Add} \cap g_1 = \{\text{On}(B,C)\} \neq \emptyset$ → **relevante** ✓
- $\text{Del} = \{\text{On}(B,\text{Mesa}),\ \text{Clear}(C)\}$
- $\text{Del} \cap g_1 = \emptyset$ (ni $\text{On}(B,\text{Mesa})$ ni $\text{Clear}(C)$ están en $g_1$) → **consistente** ✓

Regresión:

$$\text{regress}(g_1,\ \text{MoverDesdeMesa}(B,C)) = (g_1 - \{\text{On}(B,C)\}) \cup \{\text{On}(B,\text{Mesa}),\ \text{Clear}(B),\ \text{Clear}(C)\}$$

Paso 1 — quitar $\text{Add}$:

$$g_1 - \{\text{On}(B,C)\} = \{\text{On}(A,\text{Mesa}),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\}$$

Paso 2 — agregar $\text{Pre}$:

$$\{\text{On}(A,\text{Mesa}),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B)\} \cup \{\text{On}(B,\text{Mesa}),\ \text{Clear}(B),\ \text{Clear}(C)\}$$

$$= \{\text{On}(A,\text{Mesa}),\ \text{On}(B,\text{Mesa}),\ \text{On}(C,\text{Mesa}),\ \text{Clear}(A),\ \text{Clear}(B),\ \text{Clear}(C)\}$$

Este es $g_2$.

---

**Test de terminación:** ¿$g_2 \subseteq s_0$?

Verifiquemos proposición por proposición:

| Proposición en $g_2$ | ¿Está en $s_0$? |
|---|:---:|
| $\text{On}(A,\text{Mesa})$ | **Sí** ✓ |
| $\text{On}(B,\text{Mesa})$ | **Sí** ✓ |
| $\text{On}(C,\text{Mesa})$ | **Sí** ✓ |
| $\text{Clear}(A)$ | **Sí** ✓ |
| $\text{Clear}(B)$ | **Sí** ✓ |
| $\text{Clear}(C)$ | **Sí** ✓ |

$g_2 = s_0$ — de hecho, el subobjetivo es exactamente el estado inicial. Todas las proposiciones que necesitamos están en $s_0$. **¡Búsqueda terminada!**

---

### Plan reconstruido

La búsqueda hacia atrás encontró la secuencia de regresiones:

$$g_0 = G \xleftarrow{\text{MoverDesdeMesa}(A,B)} g_1 \xleftarrow{\text{MoverDesdeMesa}(B,C)} g_2 = s_0$$

Para reconstruir el plan, seguimos la cadena de padres desde $g_2$ (que coincide con $s_0$) hacia $g_0 = G$:

- `padre[$g_2$] = ($g_1$, MoverDesdeMesa(B,C))` → primera acción a ejecutar desde $s_0$
- `padre[$g_1$] = ($g_0$, MoverDesdeMesa(A,B))` → segunda acción a ejecutar

Las acciones se recolectan en orden de ejecución — no es necesario invertir:

$$\text{Plan} = [\text{MoverDesdeMesa}(B,C),\ \text{MoverDesdeMesa}(A,B)]$$

Primero ponemos B sobre C, luego A sobre B. Es el **mismo plan de 2 pasos** que encontró la búsqueda hacia adelante.

### Verificación rápida

```
Estado inicial: { On(A,Mesa), On(B,Mesa), On(C,Mesa), Clear(A), Clear(B), Clear(C) }

Paso 1 — MoverDesdeMesa(B,C):
  Pre: { On(B,Mesa) ✓, Clear(B) ✓, Clear(C) ✓ } → aplicable
  Después: { On(A,Mesa), On(B,C), On(C,Mesa), Clear(A), Clear(B) }

Paso 2 — MoverDesdeMesa(A,B):
  Pre: { On(A,Mesa) ✓, Clear(A) ✓, Clear(B) ✓ } → aplicable
  Después: { On(A,B), On(B,C), On(C,Mesa), Clear(A) }

Meta G ⊆ estado final? Sí ✓
```

![Traza de regresión en Blocks World]({{ '/16_planificacion_clasica/images/12_regression_trace.png' | url }})

**Cómo leer la figura:** la búsqueda va de **derecha a izquierda** (dirección de regresión, flechas naranjas): partimos de $g_0 = G$ (derecha), regresamos con MoverDesdeMesa(A,B) para obtener $g_1$ (centro), y luego con MoverDesdeMesa(B,C) para obtener $g_2$ (izquierda). El plan se ejecuta de **izquierda a derecha** (dirección de ejecución, flecha gris): primero MoverDesdeMesa(B,C) desde $s_0$, luego MoverDesdeMesa(A,B). Nota que $g_2 = s_0$ — el subobjetivo final coincide exactamente con el estado inicial, así que la búsqueda termina.

---

## 4. Pseudocódigo

El pseudocódigo de `BACKWARD-PLANNING` tiene la misma estructura que `FORWARD-PLANNING` del módulo anterior — es `GENERIC-SEARCH` con tres sustituciones diferentes. Las diferencias están marcadas con `[B1]`, `[B2]`, `[B3]`.

```
function BACKWARD-PLANNING(problema):

    frontera ← new Frontier()
    frontera.push(problema.G)                      [B1]  # ← empezamos desde la META
    explorado ← empty set
    padre ← { problema.G: (null, null) }

    while frontera is not empty:
        g ← frontera.pop()                                # g es un SUBOBJETIVO, no un estado

        # ── Test de terminación ──────────────────────────────────────
        if g ⊆ problema.s₀:                       [B2]  # ← ¿el estado inicial satisface g?
            return reconstruct_plan(padre, g)             # seguir padres de g hasta G

        explorado.add(g)

        # ── Expandir: buscar acciones relevantes y consistentes ──────
        for each a in problema.acciones:
            if Add(a) ∩ g ≠ ∅:                            # ¿relevante?
                if Del(a) ∩ g = ∅:                        # ¿consistente?
                    new_g ← (g - Add(a)) ∪ Pre(a) [B3]  # ← regresión (inverso de aplicar)
                    if new_g ∉ explorado and new_g ∉ frontera:
                        padre[new_g] ← (g, a)
                        frontera.push(new_g)

    return FAILURE
```

### Explicación línea por línea

**`frontera.push(problema.G)` [B1]** — En forward search, la frontera empieza con $s_0$. Aquí empieza con $G$. La meta es nuestro punto de partida.

**`g ← frontera.pop()`** — Sacamos un subobjetivo de la frontera. Si usamos cola FIFO, obtenemos BFS (primero en amplitud, encuentra el plan más corto). Si usamos pila, DFS. Si usamos cola de prioridad con heurística, A*.

**`if g ⊆ problema.s₀` [B2]** — En forward search, el test era "¿la meta está contenida en el estado actual?" ($G \subseteq s$). Aquí el test se invierte: "¿el subobjetivo está contenido en el estado inicial?" ($g \subseteq s_0$). Si todo lo que necesitamos ya es verdad en $s_0$, no necesitamos más acciones — el plan está completo.

**`reconstruct_plan(padre, g)`** — Seguimos el mapa de padres desde $g$ (que satisface $s_0$) hasta $G$, recolectando las acciones. Cada `padre[g_i] = (g_{i-1}, a_i)` significa: "ejecutar $a_i$ en un estado que satisfaga $g_i$ produce un estado que satisface $g_{i-1}$". Al caminar de $g$ (cerca de $s_0$) hacia $G$, las acciones se recolectan en **orden de ejecución** — primero la que se aplica a $s_0$, luego la siguiente, etc. No necesitamos invertir.

**`if Add(a) ∩ g ≠ ∅`** — Filtro de relevancia: la acción debe producir al menos una proposición que necesitamos.

**`if Del(a) ∩ g = ∅`** — Filtro de consistencia: la acción no debe destruir nada que necesitamos.

**`new_g ← (g - Add(a)) ∪ Pre(a)` [B3]** — La regresión. Quitamos lo que la acción producirá (ya no necesitamos que esté previamente) y agregamos lo que la acción requiere (ahora necesitamos que eso sea verdad antes). En forward search, la transición era `s' = (s - Del(a)) ∪ Add(a)`. Aquí es la operación espejo.

**`if new_g ∉ explorado and new_g ∉ frontera`** — Detección de duplicados, idéntica a forward search. Evita ciclos y trabajo redundante.

### Las tres diferencias, resumidas

| | Forward [D1, D2, D3] | Backward [B1, B2, B3] |
|---|---|---|
| **Nodo inicial** | $s_0$ (estado completo) | $G$ (subobjetivo) |
| **Test de terminación** | $G \subseteq s$? | $g \subseteq s_0$? |
| **Vecinos** | Acciones donde $\text{Pre}(a) \subseteq s$ | Acciones donde $\text{Add}(a) \cap g \neq \emptyset$ y $\text{Del}(a) \cap g = \emptyset$ |
| **Transición** | $s' = (s - \text{Del}) \cup \text{Add}$ | $g' = (g - \text{Add}) \cup \text{Pre}$ |

> **Observación:** Tanto forward como backward planning son instancias de `GENERIC-SEARCH`. La estructura del algoritmo es idéntica — lo que cambia es qué representan los nodos (estados vs subobjetivos), qué significa "meta", y cómo se generan los vecinos.

La siguiente figura muestra ambos algoritmos como diagramas de flujo lado a lado. Las cajas en rojo marcan exactamente las tres líneas que cambian — el resto de la estructura es idéntico.

![Algoritmos lado a lado]({{ '/16_planificacion_clasica/images/15_algorithm_flowchart.png' | url }})

**Cómo leer la figura:** sigue el flujo de arriba a abajo en cada columna. Las cajas con borde rojo y etiquetas [D1]/[D2]/[D3] (forward) y [B1]/[B2]/[B3] (backward) son las únicas diferencias. Todo lo demás — la estructura del ciclo, la frontera, el mapa de padres, la detección de duplicados — es exactamente `GENERIC-SEARCH`.

---

## 5. ¿Cuándo conviene buscar hacia atrás?

### El factor de ramificación

En forward search, el **factor de ramificación** es el número de acciones aplicables en cada estado. Si estamos en un estado donde muchas acciones son posibles (por ejemplo, el estado inicial con todos los bloques en la mesa y libres), el árbol de búsqueda se abre mucho.

En backward search, el factor de ramificación es el número de acciones **relevantes y consistentes** para cada subobjetivo. Si la meta es muy específica (pocas proposiciones, pocas acciones que las producen), el árbol hacia atrás es más angosto.

| Escenario | Factor de ramificación forward | Factor de ramificación backward | ¿Quién gana? |
|---|---|---|---|
| Meta específica, muchas acciones posibles desde $s_0$ | Alto | Bajo | **Backward** |
| Meta amplia, estado inicial restringido | Bajo | Alto | **Forward** |
| Meta y estado inicial similares en especificidad | Similar | Similar | Empate |

![Forward vs backward branching]({{ '/16_planificacion_clasica/images/13_forward_vs_backward_branching.png' | url }})

**Cómo leer la figura:** a la izquierda, el árbol forward crece desde $s_0$ (arriba) hacia $G$ (abajo). Cerca de $s_0$ hay muchas acciones aplicables (6 en nuestro ejemplo), así que el árbol es muy ancho al inicio y se va angostando. A la derecha, el árbol backward crece desde $G$ (arriba) hacia $s_0$ (abajo). Cerca de $G$, solo unas pocas acciones son relevantes y consistentes (2–3), así que el árbol empieza angosto. Cuando la meta es específica y el estado inicial tiene muchas acciones posibles, backward explora muchos menos nodos que forward.

### Ejemplo concreto

En nuestro Blocks World con 3 bloques:

- **Forward desde $s_0$**: el estado inicial tiene 6 acciones aplicables (las 6 MoverDesdeMesa). Factor de ramificación = 6 en la primera capa.
- **Backward desde $G$**: la meta tiene unas pocas acciones relevantes y consistentes (MoverDesdeMesa(A,B), MoverDesdeMesa(B,C), y algunas Mover). Factor de ramificación $\approx$ 3–5.

Con 3 bloques la diferencia es menor. Pero imagina un dominio de logística con 100 paquetes y 20 camiones. El estado inicial tiene miles de acciones aplicables (mover cualquier camión a cualquier ciudad, cargar cualquier paquete, etc.). Pero si la meta es "entregar el paquete P17 en la ciudad X", solo unas pocas acciones son relevantes: las que producen $\text{En}(P17, X)$. El árbol backward sería mucho más angosto.

### En la práctica

Los planificadores modernos más exitosos (como **FF**, **LAMA**, **Fast Downward**) usan búsqueda **hacia adelante** con heurísticas sofisticadas. ¿Por qué?

1. **Heurísticas más fáciles de calcular**: las heurísticas como $h^+$ (relajación por eliminación de deletes) se diseñaron para estados completos, no para subobjetivos parciales. Adaptar heurísticas a backward search es más complejo.

2. **Detección de duplicados más eficiente**: comparar estados completos (conjuntos de tamaño fijo) es más rápido que comparar subobjetivos de tamaño variable.

3. **Búsqueda bidireccional**: la idea más poderosa es combinar ambas direcciones — buscar desde $s_0$ hacia adelante y desde $G$ hacia atrás simultáneamente, esperando que los dos frentes se encuentren en el medio. Esto puede reducir exponencialmente el espacio explorado.

Sin embargo, las ideas de la regresión aparecen en muchos planificadores avanzados, incluso si no hacen búsqueda backward pura. Por ejemplo, Graphplan (Blum & Furst, 1997) usa regresión durante su fase de extracción de solución, y la planificación con SAT frecuentemente codifica restricciones que son equivalentes a razonar hacia atrás desde la meta.

> **Observación:** Entender la búsqueda hacia atrás no es solo un ejercicio teórico. Es una herramienta conceptual fundamental: la idea de "¿qué necesito que sea verdad para que esto funcione?" aparece en depuración de software, pruebas matemáticas (demostración por análisis), diseño de sistemas, y resolución de problemas en general.

---

**Anterior:** [Heurísticas para planificación ←](04_heuristicas_planificacion.md)  |  **Siguiente:** [Volver al índice →](00_index.md)
