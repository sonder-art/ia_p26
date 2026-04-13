---
title: "Más allá de minimax"
---

# 18.1 — Más allá de minimax: evaluación por simulación

> *"When you can't calculate the answer, simulate it."*

---

En el módulo 15 resolvimos juegos con minimax: recorrer el árbol hasta las hojas, propagar utilidades hacia arriba, elegir la mejor acción. Alpha-beta redujo el trabajo a la mitad en el mejor caso — pero la mitad de un número astronómico sigue siendo astronómico. Para juegos como Go ($b \approx 250$, $m \approx 150$), ni siquiera con la mejor poda llegamos a las hojas.

La solución del módulo 15 fue truncar el árbol y usar una **función de evaluación** $\text{eval}(s)$ diseñada por humanos. Eso funciona para ajedrez — décadas de experiencia ajedrecística destiladas en fórmulas de material, posición y estructura de peones. ¿Pero qué pasa cuando nadie sabe cómo evaluar una posición? ¿Y si pudiéramos evaluar **sin conocimiento del dominio**?

---

## 1. El muro de la complejidad

Recordemos los números del módulo 15:

| Juego | Factor de ramificación $b$ | Profundidad $m$ | Nodos (aprox.) | ¿Minimax exacto? |
|---|:---:|:---:|:---:|:---:|
| Nim(1,2) | 2–3 | 4 | 12 | Sí |
| Tic-tac-toe | ~4 | 9 | $\sim 10^5$ | Sí |
| **Hex 3×3** | ~5 | 9 | $\sim 10^3$ | **Sí** |
| **Hex 7×7** | ~30 | 49 | $\sim 10^{20}$ | **No** |
| Ajedrez | ~35 | ~80 | $\sim 10^{123}$ | No |
| Go | ~250 | ~150 | $\sim 10^{360}$ | No |

Para Hex 7×7, incluso alpha-beta con orden perfecto ($O(b^{m/2}) \approx 10^{10}$) podría ser factible con suficiente optimización. Pero para Go, no hay poda que alcance. Y lo más importante: **nadie ha encontrado una buena función $\text{eval}(s)$ para Go**. El patrón visual es demasiado complejo para descomponerlo en features manuales como se hace en ajedrez.

Necesitamos una forma de evaluar posiciones que no dependa de conocimiento humano.

---

## 2. La idea: jugar al azar y promediar

Imagina que estás en una posición de un juego y no sabes si es buena o mala. Podrías hacer lo siguiente:

1. Desde esa posición, jugar movimientos al azar hasta que el juego termine
2. Anotar quién ganó
3. Repetir muchas veces
4. Promediar los resultados

Si en 1000 partidas aleatorias desde esa posición ganas el 73%, probablemente es una buena posición. Si solo ganas el 28%, probablemente es mala.

Esta es exactamente la idea de un **rollout** (o **simulación**): una partida completa jugada con movimientos aleatorios desde una posición dada hasta un estado terminal.

Antes de formalizar, fijemos los dos conceptos centrales:

- **Rollout** (simulación): una partida completa jugada con movimientos aleatorios desde un estado $s$ hasta un estado terminal. El resultado es la utilidad final ($+1$, $0$ o $-1$).
- **Eval** (función de evaluación, §15.5): una función $\text{eval}(s)$ diseñada por humanos que asigna un valor numérico a un estado sin necesidad de llegar al final del juego. Requiere conocimiento experto del dominio (e.g., contar material en ajedrez).

La diferencia clave: $\text{eval}(s)$ es rápida pero necesita que alguien sepa *qué hace buena una posición*; un rollout no necesita ningún conocimiento — solo las reglas — pero requiere simular muchas partidas para obtener una buena estimación.

---

## 3. El rollout como estimador Monte Carlo

La conexión con el módulo 12 es directa. En aquel módulo definimos el estimador Monte Carlo:

$$\hat\mu_n = \frac{1}{n}\sum_{i=1}^{n} f(X_i)$$

donde $X_1, \ldots, X_n$ son muestras i.i.d. y $f$ es la función que queremos evaluar.

En un rollout:

| Concepto Monte Carlo (§12) | Concepto en juegos |
|---|---|
| Muestra $X_i$ | Una partida aleatoria completa |
| Función $f(X_i)$ | Resultado del juego: $+1$ (gana), $0$ (empate), $-1$ (pierde) |
| Esperanza $\mu = \mathbb{E}[f(X)]$ | Probabilidad de ganar desde esa posición con juego aleatorio |
| Estimador $\hat\mu_n$ | Promedio de $n$ resultados de rollouts |

Por la **Ley de los Grandes Números** (§12.2), $\hat\mu_n \to \mu$ cuando $n \to \infty$. Por el **Teorema Central del Límite**, el error es $O(1/\sqrt{n})$ — **independiente de la complejidad del juego**. No importa si el árbol tiene $10^3$ o $10^{360}$ nodos: con 10,000 rollouts, la precisión es la misma.

---

## 4. Pseudocódigo

```
# ── ROLLOUT ──────────────────────────────────────────────────────────────────
# Juega una partida aleatoria desde `estado` hasta el final.
# Retorna la utilidad del estado terminal para el jugador que nos interesa.

función ROLLOUT(juego, estado, jugador):
    s ← estado                                    # [R1] copia el estado actual
    mientras no juego.terminal(s):                 # [R2] juega hasta que termine
        acciones ← juego.acciones(s)              #      obtener movimientos legales
        a ← elegir_al_azar(acciones)              # [R3] movimiento uniformemente aleatorio
        s ← juego.resultado(s, a)                 #      aplicar la acción
    retornar juego.utilidad(s, jugador)            # [R4] +1, 0 o -1
```

```
# ── EVALUAR_POR_ROLLOUTS ─────────────────────────────────────────────────────
# Estima el valor de `estado` promediando N rollouts.
# Este ES el estimador Monte Carlo del módulo 12.

función EVALUAR_POR_ROLLOUTS(juego, estado, jugador, N):
    total ← 0
    para i = 1, …, N:
        total ← total + ROLLOUT(juego, estado, jugador)   # [E1] acumular resultados
    retornar total / N                                     # [E2] promedio = estimador MC
```

**Observaciones clave:**

- `[R3]` es el corazón: los movimientos son completamente aleatorios. No se usa ningún conocimiento del juego — solo las reglas.
- `[E2]` es literalmente $\hat\mu_n = \frac{1}{n}\sum f(X_i)$ del módulo 12.
- La calidad del estimador **no depende del tamaño del árbol**. Depende solo de $N$ (número de rollouts) y de la varianza de los resultados.

---

## 5. Ejemplo: 5 rollouts desde una posición

Supongamos una posición en un juego donde le toca a MAX. Hacemos 5 rollouts:

| Rollout | Secuencia (aleatorio) | Resultado | $f(X_i)$ |
|:---:|---|:---:|:---:|
| 1 | MAX juega a3, MIN juega b2, MAX juega c1, … | MAX gana | $+1$ |
| 2 | MAX juega b1, MIN juega a3, MAX juega c2, … | MIN gana | $-1$ |
| 3 | MAX juega c2, MIN juega a1, MAX juega b3, … | MAX gana | $+1$ |
| 4 | MAX juega a1, MIN juega c2, MAX juega b1, … | MAX gana | $+1$ |
| 5 | MAX juega b3, MIN juega a2, MAX juega c1, … | MIN gana | $-1$ |

$$\hat\mu_5 = \frac{1+(-1)+1+1+(-1)}{5} = \frac{1}{5} = 0.2$$

Interpretación: con juego aleatorio, MAX gana el 60% de las veces desde esta posición ($(0.2 + 1)/2 = 0.6$ si normalizamos a $[0,1]$). Con más rollouts, esta estimación se refinaría.

---

## 6. Rollouts vs eval(s): dos filosofías

| | $\text{eval}(s)$ (§15.5) | Rollouts (§18.1) |
|---|---|---|
| **Conocimiento** | Requiere expertise humano | Solo las reglas del juego |
| **Velocidad** | Muy rápido ($\mu$s) | Lento (ms–s por estimación) |
| **Sesgo** | Puede ser arbitrariamente malo si las features son malas | Sin sesgo (por LLN) |
| **Precisión** | Fija (determinada por el diseño) | Mejora con más rollouts ($O(1/\sqrt{N})$) |
| **Dominio** | Hay que diseñar uno nuevo para cada juego | Funciona en cualquier juego |
| **Ajedrez** | Décadas de features manuales → excelente | Los rollouts aleatorios juegan mal → estimación ruidosa |
| **Go** | Nadie supo diseñar un buen eval | Rollouts funcionan razonablemente bien |

La observación clave: **los rollouts son una evaluación universal**. No son óptimos para ningún juego en particular, pero funcionan para todos. Y como veremos en las siguientes secciones, se pueden mejorar enormemente construyendo un árbol que acumula estadísticas — eso es MCTS.

---

## 7. El problema con rollouts puros

Usar `EVALUAR_POR_ROLLOUTS` para elegir un movimiento es sencillo: evaluar cada acción legal, elegir la de mayor valor. Pero tiene dos problemas:

1. **Desperdicio de información**: cada evaluación descarta los rollouts anteriores. Si evaluamos la posición A con 1000 rollouts y luego evaluamos B, no reutilizamos nada de lo que aprendimos sobre A.

2. **Sin foco**: dedicamos el mismo esfuerzo a acciones claramente malas que a las prometedoras. Si después de 50 rollouts una acción gana el 2% de las veces, probablemente no deberíamos seguir gastando rollouts en ella.

La solución a ambos problemas es **construir un árbol**: almacenar las estadísticas de cada nodo y usar una política inteligente para decidir dónde invertir los siguientes rollouts. Eso es exactamente lo que hace MCTS — y la política inteligente resulta ser UCB1 del módulo 17.

---

**Siguiente →** [Hex: el juego](02_hex.md)
