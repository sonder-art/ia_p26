---
title: "Juegos como búsqueda"
---

| Notebook | Colab |
|---------|:-----:|
| Notebook 01 — Juegos y árboles | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/15_adversarial_search/notebooks/01_juegos_y_arboles.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |

---

# Juegos como búsqueda

> *"Games are the most civilized form of warfare."*

---

La búsqueda de los módulos 13 y 14 asume un entorno inerte: el problema no cambia mientras buscas. En un juego, el entorno **te responde**. Un oponente toma decisiones activamente para frustrar las tuyas. Esta diferencia cambia todo: ya no buscas un *camino*, buscas una *estrategia* — una función que indica qué acción tomar en cada estado posible, sin importar cómo llegaste ahí.

---

## 1. Intuición: del camino a la estrategia

**¿Qué cambia?** Un agente de búsqueda controla cada acción del estado inicial al final. En un juego de dos jugadores, el agente controla la mitad de las acciones — la otra mitad las decide el oponente. No puedes planear el camino completo de antemano porque no controlas los movimientos del adversario.

| | Búsqueda (módulos 13–14) | Juego (módulo 15) |
|---|---|---|
| ¿Quién decide? | Un agente | Dos agentes con objetivos opuestos |
| ¿Cambia el entorno? | No | Sí — el oponente responde |
| ¿Qué buscamos? | Un **camino** óptimo | Una **estrategia**: acción óptima en cada estado posible |
| Resultado del éxito | Llegar a la meta | Ganar (o garantizar el mejor resultado posible) |
| Algoritmo base | `busqueda_generica` con frontera | Minimax: DFS con propagación de valores |

![Búsqueda vs juego]({{ '/15_adversarial_search/images/01_single_vs_adversarial.png' | url }})

---

## 2. Los 7 componentes formales

Todo juego de dos jugadores se puede describir con 7 elementos. La siguiente tabla los mapea contra los conceptos que ya conocemos:

| Componente del juego | Descripción | Análogo en búsqueda |
|---|---|---|
| $s_0$ — Estado inicial | Configuración al inicio del juego (tablero vacío, pilas de fichas) | `problema.inicio` |
| $S$ — Espacio de estados | Todos los tableros/configuraciones posibles | Nodos del grafo |
| $\text{Jugadores}(s)$ | ¿De quién es el turno en el estado $s$? (MAX o MIN) | — (nuevo) |
| $\text{Acciones}(s)$ | Movimientos legales desde $s$ | `problema.acciones(n)` |
| $\text{Resultado}(s, a)$ | Estado que resulta de aplicar acción $a$ en $s$ | `problema.resultado(n,a)` |
| $\text{Terminal}(s)$ | ¿Terminó el juego? (victoria, derrota, empate) | `problema.es_meta(n)` |
| $U(s, p)$ | Utilidad del jugador $p$ en estado terminal $s$ | `problema.costo(a)` (análogo) |

Los primeros cinco componentes son los mismos que en búsqueda — solo se añaden $\text{Jugadores}$ y $U$. Esta simetría no es coincidencia: minimax hereda toda la maquinaria de DFS y solo añade la lógica de alternancia y propagación de valores.

```python
# Interfaz de búsqueda (módulos 13-14)
class Problema:
    def inicio(self): ...
    def acciones(self, n): ...
    def resultado(self, n, a): ...
    def es_meta(self, n): ...
    def costo(self, a): ...

# Interfaz de juego (módulo 15)
class Juego:
    def estado_inicial(self): ...
    def jugador(self, s): ...      # nuevo: ¿de quién es el turno?
    def acciones(self, s): ...
    def resultado(self, s, a): ...
    def terminal(self, s): ...
    def utilidad(self, s, p): ...  # nuevo: considera quién gana
```

---

## 3. El árbol de juego

Un **árbol de juego** es el árbol de búsqueda donde los niveles alternan entre los dos jugadores. Los nodos MAX representan turnos donde el jugador que maximiza elige la acción; los nodos MIN representan turnos donde el oponente (que minimiza) elige.

Propiedades clave:
- **Factor de ramificación** $b$: número de movimientos legales en un estado típico.
- **Profundidad** $m$: longitud de la partida (número total de acciones hasta el estado terminal).
- **Nodos terminales**: hojas del árbol con valor de utilidad asignado.

![Un agente vs árbol de juego]({{ '/15_adversarial_search/images/01_single_vs_adversarial.png' | url }})

En profundidad 0 tenemos el turno de MAX; en profundidad 1 el turno de MIN; en profundidad 2 el turno de MAX otra vez, y así sucesivamente. Los nodos terminales son hojas con valores de utilidad conocidos: el juego terminó y sabemos quién ganó.

**Utilidad vs función de evaluación** — una distinción que volverá en la sección 15.5:
- $U(s)$: valor **exacto** en estados terminales. Lo conocemos con certeza — el juego terminó.
- $eval(s)$: estimación del valor en estados **no terminales**. Necesaria cuando el árbol es demasiado grande para llegar a las hojas.

Esta distinción es la misma que entre costo real $g(n)$ y heurística $h(n)$ en el módulo 14 — excepto que aquí estimamos el valor del juego, no el costo restante del camino.

---

## 4. Ejemplo: tic-tac-toe

Mapeamos los 7 componentes explícitamente:

- **Estado inicial** $s_0$: tablero 3×3 vacío, representado como lista de 9 posiciones (`['', '', '', '', '', '', '', '', '']`).
- **Jugadores**: X es MAX (quiere maximizar), O es MIN (quiere minimizar). $\text{Jugadores}(s)$ = MAX si hay número par de fichas en el tablero, MIN si hay número impar.
- **Acciones**: celdas vacías. Si el tablero tiene $k$ fichas, hay $9-k$ acciones disponibles.
- **Resultado**: colocar X u O en la celda elegida según de quién sea el turno.
- **Terminal**: tres en raya para algún jugador, o tablero lleno (empate).
- **Utilidad**: $U(s, \text{MAX}) = +1$ si X gana, $-1$ si O gana, $0$ si empate.

![Anatomía de tic-tac-toe]({{ '/15_adversarial_search/images/02_tictactoe_anatomy.png' | url }})

Factor de ramificación: empieza en $b=9$, decrece a medida que se llenan celdas. Profundidad máxima: $m=9$. Nodos terminales: $\leq 9! = 362{,}880$ (con poda por victorias anticipadas, en la práctica muchos menos).

```python
class TicTacToe:
    """Tic-tac-toe con los 7 componentes formales."""

    def estado_inicial(self):
        return tuple([''] * 9)   # tablero vacío, 9 posiciones

    def jugador(self, s):
        # X juega primero (turno par de fichas = MAX)
        fichas = sum(1 for c in s if c != '')
        return 'MAX' if fichas % 2 == 0 else 'MIN'

    def acciones(self, s):
        return [i for i, c in enumerate(s) if c == '']

    def resultado(self, s, a):
        ficha = 'X' if self.jugador(s) == 'MAX' else 'O'
        nuevo = list(s)
        nuevo[a] = ficha
        return tuple(nuevo)

    def terminal(self, s):
        return self._ganador(s) is not None or '' not in s

    def utilidad(self, s, p='MAX'):
        gan = self._ganador(s)
        if gan == 'X': return +1
        if gan == 'O': return -1
        return 0

    def _ganador(self, s):
        lineas = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a, b, c in lineas:
            if s[a] == s[b] == s[c] != '':
                return s[a]
        return None
```

---

## 5. Ejemplo: Nim

Nim es el juego de ejemplo principal de este módulo porque su árbol cabe completamente en una figura — podemos trazar minimax nodo por nodo sin perder el hilo. Además esconde una propiedad matemática que veremos en la sección 15.5.

### Las reglas del juego

Imagina que hay $k$ montones de fichas sobre la mesa. En cada turno, el jugador activo elige **uno** de los montones y retira **todas las fichas que quiera** de ese montón — pero al menos una. No se puede pasar sin mover, ni retirar fichas de más de un montón a la vez. **El jugador que retira la última ficha gana** (y deja al oponente sin movimiento).

Eso es todo. Tres frases. Pero la estrategia óptima es profundamente no-obvia.

### Por qué el juego es interesante: un ejemplo de razonamiento estratégico

Considera **Nim(1,2)**: pila A tiene 1 ficha, pila B tiene 2 fichas. Tú eres MAX y mueves primero.

Imagina que retiras las 2 fichas de B y dejas el estado *(1,0)*. Ahora MIN tiene una sola ficha en A. MIN la retira. Todas las pilas vacías: **MAX no puede mover → MAX pierde**. Mala decisión.

Ahora imagina que retiras 1 ficha de B y dejas el estado *(1,1)*. Cada pila tiene exactamente 1 ficha. Cualquier cosa que haga MIN — retire la de A o la de B — quedará una ficha en la otra pila. MAX la retira. Todas las pilas vacías: **MIN no puede mover → MAX gana**. La clave fue forzar una posición *simétrica* que le da el control a MAX.

Esta intuición no siempre es obvia. Minimax la descubrirá automáticamente.

### Partida de ejemplo completa

```
Estado inicial: (1, 2)  →  pila A = 1 ficha,  pila B = 2 fichas

Turno 1 (MAX): retira 1 de B  →  estado (1, 1)   ← jugada óptima
Turno 2 (MIN): retira 1 de A  →  estado (0, 1)   ← MIN tiene que mover algo
Turno 3 (MAX): retira 1 de B  →  estado (0, 0)   ← MAX toma la última ficha
              ╔══════════════════════════════════╗
              ║  (0,0): MIN no puede mover       ║
              ║  → MAX GANA                      ║
              ╚══════════════════════════════════╝
```

### Convención de utilidad: ¿por qué solo un número?

En Nim solo hay dos resultados para MAX: **gana (+1)** o **pierde (−1)**. El empate no existe.

Como el juego es de **suma cero**, si MAX gana (+1) entonces MIN pierde (−1), y viceversa. Conocer el resultado de uno determina completamente el del otro. Por eso usamos **un solo número** — la utilidad desde la perspectiva de MAX — en lugar de un par. Esto no es una simplificación: es la consecuencia directa de la propiedad de suma cero que vimos en la sección 2.

**Convención de terminal**: cuando el estado es $(0,0,\ldots,0)$, el jugador cuyo turno es en ese momento **no puede mover y pierde**. Así:
- Si le toca a MAX en $(0,0)$: MAX no puede mover → MAX pierde → utilidad = **−1**
- Si le toca a MIN en $(0,0)$: MIN no puede mover → MIN pierde → utilidad = **+1** (bueno para MAX)

### Los 7 componentes formales

- **Estado inicial**: tupla de enteros, e.g. `(1, 2)` — cada número es el tamaño de una pila. El orden importa: el primer número es la pila A, el segundo la pila B, etc.
- **Jugadores**: alterna MAX/MIN en cada turno. En la implementación se controla con un booleano `es_max` que se invierte en cada llamada recursiva.
- **Acciones** desde estado $(a, b)$: todas las combinaciones *(pila, cantidad)*. Las acciones legales son retirar 1, 2, … hasta $a$ de la pila A, y 1, 2, … hasta $b$ de la pila B. En notación: `A-1`, `A-2`, …, `B-1`, `B-2`, …
- **Resultado**: el estado con la pila elegida reducida en la cantidad retirada. `resultado((1,2), B-1) = (1,1)`.
- **Terminal**: el estado $(0, 0, \ldots, 0)$ — todas las pilas vacías, ningún movimiento posible.
- **Utilidad**: desde la perspectiva de MAX. Si le toca a MAX en el terminal → −1; si le toca a MIN → +1.

### Lectura del árbol de Nim(1,2)

![Reglas y árbol de Nim]({{ '/15_adversarial_search/images/03_nim_rules_and_tree.png' | url }})

La figura de la derecha muestra el **árbol de juego completo** de Nim(1,2). Así se lee:

- **Cada nodo** es un estado del juego, escrito como la tupla *(A, B)*. El nodo raíz *(1,2)* es el estado inicial.
- **Nivel superior (azul)**: nodo MAX — es el turno de MAX, que quiere maximizar.
- **Nivel siguiente (rojo)**: nodo MIN — es el turno de MIN, que quiere minimizar.
- Los niveles siguen alternando: MAX, MIN, MAX, MIN… hasta las hojas.
- **Cada arista** es un movimiento legal. La etiqueta sobre la arista (p.ej. `B-1`) dice qué pila se usó y cuántas fichas se retiraron. La arista `A-1` desde *(1,2)* lleva a *(0,2)* porque se retiró 1 ficha de la pila A.
- **Nodos terminales** (cuadrados): el estado *(0,0)* donde ningún jugador puede mover. El número dentro del cuadrado es la utilidad desde la perspectiva de MAX: **+1** si MAX gana (el turno corresponde a MIN en ese terminal), **−1** si MAX pierde (el turno corresponde a MAX en ese terminal).
- **El valor junto a cada nodo no-terminal** es el valor minimax: el resultado garantizado bajo juego perfecto de ambos lados desde ese nodo. Lo calcularemos formalmente en la sección 3.
- La **arista verde gruesa** marca la jugada óptima de MAX desde la raíz: B-1 → *(1,1)*.

Observa que todas las hojas del árbol son *(0,0)* pero con **valores distintos** (+1 o −1). Esto es consistente: el valor depende de *quién tiene el turno* cuando se llega a *(0,0)*, no solo del estado en sí.

```python
class Nim:
    """Juego de Nim para k pilas."""

    def estado_inicial(self, pilas):
        return tuple(pilas)          # e.g. (1, 2) para pila A=1, pila B=2

    def jugador(self, s, turno_max=True):
        return 'MAX' if turno_max else 'MIN'

    def acciones(self, s):
        # Genera todos los movimientos legales: (índice_pila, cantidad_a_retirar)
        acciones = []
        for i, pila in enumerate(s):
            for cant in range(1, pila + 1):   # retirar entre 1 y pila[i] fichas
                acciones.append((i, cant))
        return acciones

    def resultado(self, s, a):
        pile_idx, amount = a
        nuevo = list(s)
        nuevo[pile_idx] -= amount    # aplica el movimiento
        return tuple(nuevo)

    def terminal(self, s):
        return all(p == 0 for p in s)    # todas las pilas vacías

    def utilidad(self, s, es_max_turno):
        # El jugador en turno no puede mover → pierde
        # Si es el turno de MAX: MAX pierde → −1
        # Si es el turno de MIN: MIN pierde → +1 (bueno para MAX)
        return -1 if es_max_turno else +1
```

**¿Por qué Nim y no tic-tac-toe para las trazas?** El árbol de Nim(1,2) tiene exactamente **12 nodos** — cabe en una figura y podemos seguir cada llamada a mano. El árbol de tic-tac-toe completo tiene hasta 362,880 nodos — imposible de trazar nodo por nodo.

---

## 6. ¿Y el ajedrez?

Los mismos 7 componentes aplican, pero los números hacen que minimax exacto sea inviable:

| Parámetro | Valor |
|---|---|
| Factor de ramificación $b$ | $\approx 35$ movimientos legales por posición |
| Profundidad $m$ | $\approx 80$ semi-movimientos en una partida típica |
| Partidas posibles | $\approx 10^{123}$ (número de Shannon) |
| Posiciones únicas | $\approx 10^{43}$ |

Incluso a 1 billón de nodos por segundo, explorar $10^{123}$ nodos tomaría más tiempo que la edad del universo ($\approx 4 \times 10^{17}$ segundos). La sección 15.5 muestra cómo resolver esto con límite de profundidad y funciones de evaluación.

---

**Siguiente:** [Tipos de juegos →](02_tipos_de_juegos.md)
