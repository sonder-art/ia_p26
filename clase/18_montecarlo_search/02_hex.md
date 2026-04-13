---
title: "Hex: el juego"
---

# 18.2 — Hex: el juego

> *"Hex is a game of pure strategy with simple rules but extraordinary depth."* — Martin Gardner

---

A lo largo de este módulo usaremos **Hex** como ejemplo principal — el mismo rol que Nim y tic-tac-toe cumplieron en el módulo 15. Hex tiene tres propiedades que lo hacen ideal para estudiar MCTS: sus reglas son extremadamente simples, **no existe una función de evaluación conocida** (a diferencia del ajedrez), y **nunca termina en empate**. Esto significa que los métodos exactos como minimax necesitan llegar hasta las hojas, pero el árbol es demasiado grande para eso en tableros de tamaño real. MCTS es la herramienta perfecta.

---

## 1. Historia

Hex fue inventado independientemente dos veces:

- **Piet Hein** (1942): matemático y poeta danés, lo presentó en el periódico *Politiken* bajo el nombre "Polygon"
- **John Nash** (1948): lo reinventó como estudiante de doctorado en Princeton, donde se conocía simplemente como "Nash" o "the Nash game"

Nash demostró que el primer jugador siempre tiene una estrategia ganadora (sección 5), pero nunca especificó cuál. Sesenta años después, nadie la ha encontrado para tableros grandes.

---

## 2. Reglas

Las reglas de Hex caben en cuatro oraciones:

1. **El tablero** es un rombo de celdas hexagonales. Los tamaños estándar son 7×7, 9×9, 11×11 y 13×13
2. **Dos jugadores** (Negro y Blanco) se turnan colocando una piedra de su color en cualquier celda vacía
3. **No hay capturas** ni movimientos especiales — las piedras, una vez colocadas, no se mueven ni se retiran
4. **Gana** el primer jugador que forme una cadena conectada de sus piedras entre sus dos lados opuestos del tablero: Negro conecta arriba con abajo, Blanco conecta izquierda con derecha

![Tablero de Hex vacío con lados etiquetados]({{ '/18_montecarlo_search/images/01_hex_empty_board.png' | url }})

El tablero vacío muestra la geometría: un rombo de hexágonos con los cuatro lados etiquetados por color. Los lados de Negro (arriba y abajo) y los de Blanco (izquierda y derecha) se alternan en las esquinas.

---

## 3. Anatomía de una celda

Cada celda hexagonal tiene exactamente **6 vecinos** (excepto las celdas del borde, que tienen menos). Esta es la estructura de adyacencia que define qué celdas están "conectadas":

![Vecinos de una celda hexagonal]({{ '/18_montecarlo_search/images/02_hex_neighbors.png' | url }})

La figura muestra una celda central y sus 6 vecinos. En un sistema de coordenadas $(r, c)$ (fila, columna), los vecinos de la celda $(r, c)$ son:

| Dirección | Coordenada |
|---|---|
| Arriba-izquierda | $(r-1, c)$ |
| Arriba-derecha | $(r-1, c+1)$ |
| Izquierda | $(r, c-1)$ |
| Derecha | $(r, c+1)$ |
| Abajo-izquierda | $(r+1, c-1)$ |
| Abajo-derecha | $(r+1, c)$ |

Esta lista de vecinos es todo lo que necesita el código para determinar conexiones.

---

## 4. Ejemplos visuales

### Una partida en progreso

![Movimientos legales resaltados]({{ '/18_montecarlo_search/images/03_hex_legal_moves.png' | url }})

A mitad de partida, las celdas vacías son los movimientos legales (resaltadas). Observa que las opciones disminuyen conforme avanza el juego — a diferencia de Go, donde la complejidad táctica puede crecer.

### Una partida terminada

![Partida ganada con cadena resaltada]({{ '/18_montecarlo_search/images/04_hex_winning_path.png' | url }})

El jugador Negro formó una cadena de piedras conectando su lado superior con su lado inferior. La cadena ganadora está resaltada. Nota que no necesita ser una línea recta — cualquier camino conectado cuenta.

### Hex 3×3: partidas completas

![Dos partidas completas en Hex 3×3]({{ '/18_montecarlo_search/images/05_hex_3x3_games.png' | url }})

Dos partidas en el tablero pequeño que usaremos para trazas. A la izquierda, Negro conecta su lado superior con su lado inferior a través de una cadena diagonal (resaltada en verde). A la derecha, Blanco conecta su lado izquierdo con su lado derecho cruzando por la fila central. En 3×3, el juego dura como máximo 9 movimientos y el árbol completo tiene $\sim 10^3$ nodos — lo suficientemente pequeño para que minimax (o MCTS con pocas iteraciones) lo resuelva.

---

## 5. El argumento de strategy-stealing: el primer jugador gana

**Teorema (Nash, 1949).** En Hex de cualquier tamaño, el primer jugador tiene una estrategia ganadora.

La demostración es elegante y no constructiva — prueba que la estrategia *existe* sin decir cuál es:

1. **Hex no puede terminar en empate** (ver sección 6). Uno de los dos jugadores *debe* ganar
2. **Supongamos** que el segundo jugador tiene una estrategia ganadora $\sigma_2$
3. El primer jugador puede **robar** esa estrategia: hace un primer movimiento arbitrario, y luego sigue $\sigma_2$ como si fuera el segundo jugador. Si en algún momento $\sigma_2$ le pide jugar en la celda que ya ocupó con su primer movimiento, juega en otra celda arbitraria
4. Tener una piedra extra **nunca perjudica** en Hex (a diferencia de Go, donde existe el *zugzwang*). Así que el primer jugador, siguiendo $\sigma_2$ con una piedra de ventaja, gana
5. Pero dijimos que $\sigma_2$ era ganadora para el *segundo* jugador — contradicción
6. Por lo tanto, el segundo jugador **no puede** tener una estrategia ganadora. Como alguien debe ganar, el primer jugador tiene una

| Tamaño | ¿Resuelto? | Resultado |
|:---:|:---:|---|
| 1×1 – 6×6 | Sí | Primer jugador gana (estrategia conocida) |
| 7×7 – 9×9 | Sí (por computadora) | Primer jugador gana (brute-force) |
| 10×10 | Parcialmente | Primer jugador gana (con mucho cómputo) |
| 11×11+ | No | Primer jugador gana (por el teorema), pero la estrategia es desconocida |

**Implicación para MCTS**: como nadie conoce la estrategia ganadora para tableros grandes, no podemos simplemente programarla. Necesitamos un algoritmo que **descubra** buenas estrategias a través de la búsqueda — exactamente lo que hace MCTS.

---

## 6. El teorema de no-empate

**Teorema.** Una partida de Hex no puede terminar en empate.

Para entender por qué, pensemos en un tablero completamente lleno — todas las celdas ocupadas, ninguna vacía. Cada celda es negra o blanca. Ahora consideremos qué pasa con la conexión de Negro (arriba↔abajo):

- **Caso 1: Negro tiene un camino** de arriba a abajo → Negro gana.
- **Caso 2: Negro NO tiene un camino** de arriba a abajo → entonces existe un "muro" continuo de piedras blancas que separa el lado superior del inferior. Pero ese muro, para bloquear *completamente* a Negro en un tablero hexagonal con forma de rombo, necesariamente toca el lado izquierdo y el lado derecho del tablero. Es decir, ese muro **es** un camino de Blanco de izquierda a derecha → Blanco gana.

No hay un tercer caso: o Negro cruza de arriba a abajo, o Blanco cruza de izquierda a derecha. Siempre gana exactamente uno de los dos.

¿Por qué esto no ocurre en tableros cuadrados? En una cuadrícula, dos caminos perpendiculares pueden cruzarse en una celda sin compartirla — cada uno pasa "por un lado" de la celda. En la geometría hexagonal, esto es imposible: si un camino de Negro cruza de arriba a abajo, *físicamente bloquea* cualquier camino de Blanco de izquierda a derecha y viceversa. Los hexágonos no dejan huecos por donde un camino pueda "escabullirse" alrededor del otro. Esto es lo que formalmente se conoce como el **teorema del juego hexagonal** (una variante discreta del teorema de Brouwer del punto fijo).

**Consecuencia para el análisis**: como no hay empates, la utilidad es siempre $+1$ o $-1$. Esto simplifica los rollouts — cada simulación tiene un resultado binario, y el promedio de rollouts es directamente la probabilidad estimada de ganar.

---

## 7. Componentes formales

Siguiendo la formalización de 7 componentes del módulo 15 (§15.1):

| Componente | Hex $n \times n$ |
|---|---|
| $S_0$ (estado inicial) | Tablero vacío de $n \times n$ celdas |
| $\text{Jugadores}$ | $\{\text{Negro}, \text{Blanco}\}$ |
| $\text{Turno}(s)$ | Negro juega en turnos impares, Blanco en pares |
| $\text{Acciones}(s)$ | Todas las celdas vacías |
| $\text{Resultado}(s, a)$ | Colocar piedra del jugador actual en celda $a$ |
| $\text{Terminal}(s)$ | Algún jugador conectó sus dos lados |
| $U(s, p)$ | $+1$ si $p$ ganó, $-1$ si $p$ perdió |

Comparación con los juegos del módulo 15:

| Propiedad | Nim | Tic-tac-toe | **Hex** |
|---|:---:|:---:|:---:|
| Determinista | Sí | Sí | **Sí** |
| Información perfecta | Sí | Sí | **Sí** |
| Suma cero | Sí | Sí | **Sí** |
| ¿Empates? | No | Sí | **No** |
| $b$ (ramificación) | 2–3 | ~4 | **~30 (7×7)** |
| Nodos (árbol completo) | 12 | $\sim 10^5$ | **$\sim 10^{20}$ (7×7)** |

Hex comparte todas las propiedades deseables (determinista, información perfecta, suma cero) pero con un árbol mucho más grande — exactamente donde minimax falla y MCTS brilla.

---

## 8. Complejidad por tamaño

| Tamaño | Celdas | Estados (aprox.) | ¿Minimax factible? | ¿MCTS útil? |
|:---:|:---:|:---:|:---:|:---:|
| 3×3 | 9 | $\sim 10^3$ | Sí (traza completa) | Sí (para aprender) |
| 5×5 | 25 | $\sim 10^{10}$ | Difícil | Sí |
| 7×7 | 49 | $\sim 10^{20}$ | No | **Sí** |
| 9×9 | 81 | $\sim 10^{33}$ | No | Sí |
| 11×11 | 121 | $\sim 10^{50}$ | No | Sí |
| 13×13 | 169 | $\sim 10^{70}$ | No | Sí |

Usaremos **Hex 3×3** como el Nim del módulo 18: lo suficientemente pequeño para trazar MCTS paso a paso. Y **Hex 7×7** como el juego real donde compararemos agentes.

---

## 9. Patrones estratégicos básicos

Aunque no necesitamos conocimiento estratégico para MCTS (ese es el punto), entender algunos patrones ayuda a apreciar lo que el algoritmo debe descubrir:

![Patrones estratégicos en Hex]({{ '/18_montecarlo_search/images/06_hex_strategy.png' | url }})

- **Puente** (*bridge*): dos piedras separadas por un hueco de una celda. El oponente no puede bloquear ambas conexiones — siempre puedes completar el puente
- **Escalera** (*ladder*): una cadena de puentes forzados que corre diagonalmente por el tablero. Si tienes una escalera y el borde está abierto, la conexión está garantizada
- **Esquinas**: las cuatro esquinas del tablero son estratégicamente valiosas porque tocan dos lados a la vez

Estos patrones emergen naturalmente cuando MCTS juega muchas partidas: las posiciones con puentes y control de esquinas obtienen mejores estadísticas, así que el algoritmo las favorece sin que nadie le haya enseñado su importancia.

---

## 10. Implementación en Python

La clase `Hex` sigue la misma interfaz que `TicTacToe` y `Nim` del módulo 15:

```python
class Hex:
    def __init__(self, size=7):
        self.size = size
        self.board = [[0] * size for _ in range(size)]  # 0=vacío, 1=Negro, 2=Blanco
        self.current_player = 1  # Negro empieza

    def actions(self):
        """Retorna lista de celdas vacías (r, c)."""
        return [(r, c) for r in range(self.size)
                for c in range(self.size) if self.board[r][c] == 0]

    def result(self, action):
        """Aplica la acción y retorna un nuevo estado."""
        import copy
        new = copy.deepcopy(self)
        r, c = action
        new.board[r][c] = self.current_player
        new.current_player = 3 - self.current_player  # alterna 1 ↔ 2
        return new

    def is_terminal(self):
        """True si algún jugador conectó sus lados."""
        return self._has_path(1) or self._has_path(2)

    def utility(self, player):
        """Retorna +1 si player ganó, -1 si perdió."""
        if self._has_path(player):
            return 1
        if self._has_path(3 - player):
            return -1
        return 0  # juego no terminado (no debería ocurrir en terminal)

    def _has_path(self, player):
        """BFS: ¿player conectó sus dos lados?"""
        n = self.size
        # Negro (1): conecta fila 0 con fila n-1
        # Blanco (2): conecta columna 0 con columna n-1
        if player == 1:
            start = [(0, c) for c in range(n) if self.board[0][c] == 1]
            goal = lambda r, c: r == n - 1
        else:
            start = [(r, 0) for r in range(n) if self.board[r][0] == 2]
            goal = lambda r, c: c == n - 1

        visited = set()
        queue = list(start)
        for pos in queue:
            if pos in visited:
                continue
            visited.add(pos)
            r, c = pos
            if goal(r, c):
                return True
            for dr, dc in [(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and self.board[nr][nc] == player:
                    queue.append((nr, nc))
        return False
```

**Observaciones:**

- `_has_path` usa BFS para verificar conexión — los 6 vecinos hexagonales son las direcciones `[(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]`
- La interfaz es idéntica a la de los juegos del módulo 15: `actions()`, `result(a)`, `is_terminal()`, `utility(p)`
- El tablero se representa como una matriz $n \times n$ donde las filas están desplazadas (coordenadas *offset*), que es la representación estándar para tableros hexagonales

---

**Anterior →** [Más allá de minimax](01_mas_alla_de_minimax.md) | **Siguiente →** [MCTS: las cuatro fases](03_mcts.md)
