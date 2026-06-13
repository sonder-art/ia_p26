---
title: "Tipos de juegos"
---

| Notebook | Colab |
|---------|:-----:|
| Notebook 01 — Juegos y árboles | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/15_adversarial_search/notebooks/01_juegos_y_arboles.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |

---

# Tipos de juegos

> *"Not all games are created equal."*

---

Antes de ver cómo minimax toma decisiones, necesitamos entender **por qué** funciona con un solo valor numérico. La respuesta está en la estructura del juego: los juegos de suma cero permiten representar los intereses de ambos jugadores con un único escalar. Esta propiedad no es trivial — la sección del Dilema del Prisionero muestra exactamente qué se rompe cuando no se cumple.

---

## 1. Taxonomía

Los juegos de dos jugadores se clasifican a lo largo de tres ejes independientes:

1. **Determinista / Estocástico**: ¿hay azar en el juego? Un dado en backgammon o cartas robadas en póker son ejemplos de estocasticidad — el resultado de una acción no es completamente determinado por el estado actual y la acción elegida.
2. **Información perfecta / Imperfecta**: ¿los jugadores ven el estado completo? En ajedrez ambos ven el tablero entero (información perfecta). En póker cada jugador ve solo sus propias cartas (información imperfecta).
3. **Suma cero / No-suma-cero**: ¿la ganancia de uno implica pérdida del otro? Esta propiedad determina si minimax puede usar un solo número para representar el estado del juego.

![Taxonomía de juegos]({{ '/15_adversarial_search/images/04_game_taxonomy.png' | url }})

---

## 2. Suma cero: la propiedad que hace funcionar minimax

**Definición formal**: un juego es de suma cero si para todo estado terminal $s$:

$$U_{\text{MAX}}(s) + U_{\text{MIN}}(s) = c$$

para alguna constante $c$ (usualmente $c = 0$ o $c = 1$).

La consecuencia algorítmica crítica:

> Si $U_{\text{MAX}}(s) + U_{\text{MIN}}(s) = 0$ en todo estado terminal, entonces $U_{\text{MIN}}(s) = -U_{\text{MAX}}(s)$. **Maximizar la utilidad de MAX es exactamente lo mismo que minimizar la utilidad de MIN.** Por eso minimax usa un solo escalar $V(s)$ — la utilidad de MAX determina completamente la utilidad de MIN.

Tic-tac-toe y Nim satisfacen la condición de suma cero. En tic-tac-toe, las tres posibles utilidades son:
- MAX gana: $U_{\text{MAX}} = +1$, $U_{\text{MIN}} = -1$. Suma: $0$. ✓
- Empate: $U_{\text{MAX}} = 0$, $U_{\text{MIN}} = 0$. Suma: $0$. ✓
- MIN gana: $U_{\text{MAX}} = -1$, $U_{\text{MIN}} = +1$. Suma: $0$. ✓

Sin la propiedad de suma cero necesitaríamos rastrear **dos valores** por nodo — uno para cada jugador — y la estructura del algoritmo cambiaría fundamentalmente.

---

## 3. No suma cero: el Dilema del Prisionero

Para mostrar qué ocurre cuando la suma no es cero, consideramos el **Dilema del Prisionero**: dos sospechosos son interrogados en celdas separadas. Cada uno decide independientemente si **callar** o **confesar**. La condena de cada uno depende de ambas decisiones.

**Matriz de pagos** (años de prisión, formato (jugador A, jugador B)):

```
               Jugador B: Callar    Jugador B: Confesar
Jugador A: Callar    (−1, −1)           (−10,  0)
Jugador A: Confesar  ( 0, −10)          (−5,  −5)
```

![Suma cero vs. no suma cero]({{ '/15_adversarial_search/images/05_payoff_matrices.png' | url }})

Tres observaciones:

1. **No es suma cero**: $(-1)+(-1) = -2$ en la celda superior izquierda, $(-5)+(-5) = -10$ en la celda inferior derecha. Los valores cambian por celda, no son constantes.

2. **Minimax aplicado**: MAX (jugador A) considera qué pasa en el peor caso. Si calla: MIN puede confesar, dejando a MAX con −10. Si confiesa: MIN puede callar (A obtiene 0) o confesar (A obtiene −5). El mínimo garantizado confesando es −5; callando es −10. MAX elige confesar. La misma lógica aplica a MIN. Resultado: ambos confiesan → $(−5, −5)$.

3. **Pero** la celda $(−1, −1)$ existe y es mejor para **ambos** jugadores — **domina en Pareto** la solución minimax. Minimax no la encuentra porque asume adversario que busca maximizar su propia utilidad, no cooperación.

**Conclusión**: minimax da una respuesta "racional" en el sentido de que ningún jugador puede mejorar su situación desviándose unilateralmente — es un equilibrio de Nash. Pero es subóptima en bienestar total comparada con la cooperación. Para estos juegos se necesitan otras herramientas — equilibrios de Nash, mecanismos de incentivos, teoría de juegos cooperativos — que abordaremos en módulos posteriores.

---

## 4. Juegos conocidos clasificados

| Juego | Determinista | Info perfecta | Suma cero | Algoritmo adecuado |
|---|:---:|:---:|:---:|---|
| Tic-tac-toe | Sí | Sí | Sí | Minimax exacto |
| Nim | Sí | Sí | Sí | Minimax / nim-sum XOR |
| Damas | Sí | Sí | Sí | Alpha-beta + eval |
| Ajedrez | Sí | Sí | Sí | Alpha-beta + eval |
| Go | Sí | Sí | Sí | MCTS + redes neuronales |
| Backgammon | **No** | Sí | Sí | Expectimax |
| Póker | **No** | **No** | No | Teoría de juegos |

---

## 5. Información perfecta: por qué importa

En un juego de **información perfecta**, ambos jugadores ven el estado completo del juego en todo momento. Esto garantiza que el árbol de juego esté completamente determinado: cada nodo tiene un conjunto bien definido de acciones y resultados.

En juegos de **información imperfecta** (póker, juegos de cartas), el estado del juego incluye información privada que solo un jugador conoce. El adversario no puede construir el árbol de juego desde el estado real — solo desde su información parcial. Esto requiere razonar sobre distribuciones de probabilidad sobre estados posibles, no sobre un estado único.

Este módulo se enfoca exclusivamente en: **juegos deterministas, con información perfecta, de dos jugadores, suma cero**. Tic-tac-toe, Nim y ajedrez son los tres ejemplos principales. Los juegos estocásticos (backgammon con expectimax) se mencionan brevemente en la sección 15.5.

---

**Siguiente:** [Minimax →](03_minimax.md)
