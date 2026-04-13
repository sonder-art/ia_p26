---
title: "Algoritmo de Viterbi"
---

# Algoritmo de Viterbi

> *Problema 2 — Decodificación: ¿Cuál fue la secuencia de estados ocultos más probable?*

---

## 1. ¿En qué se diferencia de Forward?

El algoritmo Forward calcula $P(O \mid \lambda)$ sumando sobre **todas** las trayectorias posibles:

$$P(O \mid \lambda) = \sum_{\text{todas las trayectorias}} P(O, \text{trayectoria} \mid \lambda)$$

Eso es correcto cuando queremos la probabilidad total. Pero ahora queremos la **trayectoria única más probable** — no un promedio, sino el máximo:

$$q_1^∗, q_2^∗, \ldots, q_T^∗ = \arg\max_{q_1, \ldots, q_T} P(q_1, \ldots, q_T, O \mid \lambda)$$

El cambio parece pequeño — reemplazamos $\sum$ por $\max$ — pero tiene consecuencias importantes: ahora debemos recordar **de dónde vino** cada máximo para poder reconstruir el camino al final.

| | Forward | Viterbi |
|---|:-------:|:-------:|
| Operación central | Suma sobre estados anteriores | Máximo sobre estados anteriores |
| Resultado | $P(O \mid \lambda)$ — probabilidad total | Secuencia óptima $q_1^∗, \ldots, q_T^∗$ |
| ¿Necesita backpointers? | No | Sí |

---

## 2. Las dos variables de Viterbi

**Variable $\delta_t(i)$** — la probabilidad del **mejor camino** hasta el estado $i$ en el instante $t$:

$$\delta_t(i) = \max_{q_1, \ldots, q_{t-1}} P(q_1, \ldots, q_{t-1}, q_t = i, O_1, \ldots, O_t \mid \lambda)$$

En palabras: de todas las trayectorias que terminan en el estado $i$ en el instante $t$ habiendo generado $O_1, \ldots, O_t$, ¿cuál es la probabilidad de la mejor?

**Variable $\psi_t(j)$** — el **backpointer**: ¿desde qué estado $i$ llegamos a $j$ en el mejor camino?

$$\psi_t(j) = \arg\max_{i} \delta_{t-1}(i) \cdot A_{ij}$$

Los backpointers son la clave para reconstruir la secuencia óptima al final del algoritmo.

---

## 3. Inicialización, recursión y backtracking

**[P1] Inicialización** ($t = 1$):

$$\delta_1(i) = \pi_i \cdot B_{i,O_1} \qquad \text{para todo } i$$

$$\psi_1(i) = 0 \qquad \text{(no hay estado previo en } t=1\text{)}$$

**[P2] Recursión** ($t = 2, 3, \ldots, T$):

$$\delta_t(j) = \max_{i} \left[\delta_{t-1}(i) \cdot A_{ij}\right] \cdot B_{j,O_t}$$

$$\psi_t(j) = \arg\max_{i} \left[\delta_{t-1}(i) \cdot A_{ij}\right]$$

Nota: $\psi_t(j)$ se calcula sin el factor $B_{j,O_t}$ porque la emisión no afecta cuál estado anterior fue el mejor.

**[P3] Terminación y backtracking**:

```
# Encontrar el mejor estado final:
q*[T] = argmax_i δ[T][i]

# Seguir los backpointers hacia atrás:
para t = T-1 hasta 1:
    q*[t] = ψ[t+1][ q*[t+1] ]
```

---

## 4. Visualización: el trellis de Viterbi

```
Estado │  t=1           t=2              t=3
───────┼────────────────────────────────────────────────
  S    │  δ₁(S)=0.540   δ₂(S)=0.0378    δ₃(S)=0.00518
       │                ψ₂(S)=S         ψ₃(S)=R
       │
  R    │  δ₁(R)=0.080   δ₂(R)=0.1296   δ₃(R)=0.06221
       │                ψ₂(R)=S         ψ₃(R)=R

  O_t  │   O₁=0          O₂=1            O₃=1

Mejor estado final: R (δ₃(R)=0.06221 > δ₃(S)=0.00518)
Backtrack: R → ψ₃(R)=R → ψ₂(R)=S
Secuencia óptima: S → R → R
```

![Viterbi Trellis]({{ '/20_hmm/images/07_viterbi_trellis.png' | url }})

---

## 5. Traza completa: el ejemplo de Lain

Parámetros: $\pi = (0.6, 0.4)$, $O = (0, 1, 1)$

$$A = \begin{pmatrix}
0.7 & 0.3 \\\\
0.4 & 0.6
\end{pmatrix}, \qquad B = \begin{pmatrix}
0.9 & 0.1 \\\\
0.2 & 0.8
\end{pmatrix}$$

**Paso 1 — Inicialización** ($O_1 = 0$):

$$\delta_1(S) = \pi_S \cdot B_{S,0} = 0.6 \times 0.9 = 0.540, \qquad \psi_1(S) = 0$$

$$\delta_1(\mathrm{R}) = \pi_R \cdot B_{R,0} = 0.4 \times 0.2 = 0.080, \qquad \psi_1(\mathrm{R}) = 0$$

**Paso 2 — Recursión** ($O_2 = 1$):

Para el estado $S$ en $t=2$:

$$\delta_2(S) = \max(\delta_1(S) \cdot A_{SS}, \delta_1(\mathrm{R}) \cdot A_{RS}) \cdot B_{S,1}$$
$$= \max(0.540 \times 0.7, 0.080 \times 0.4) \times 0.1 = \max(0.378, 0.032) \times 0.1 = 0.0378$$
$$\psi_2(S) = \arg\max(0.378, 0.032) = S \text{ (índice 0)}$$

Para el estado $R$ en $t=2$:

$$\delta_2(\mathrm{R}) = \max(\delta_1(S) \cdot A_{SR}, \delta_1(\mathrm{R}) \cdot A_{RR}) \cdot B_{R,1}$$
$$= \max(0.540 \times 0.3, 0.080 \times 0.6) \times 0.8 = \max(0.162, 0.048) \times 0.8 = 0.1296$$
$$\psi_2(\mathrm{R}) = \arg\max(0.162, 0.048) = S \text{ (índice 0)}$$

Intuición: en $t=2$, el mejor camino a ambos estados pasa por $S$ en $t=1$ (porque $\delta_1(S)$ es mucho mayor que $\delta_1(\mathrm{R})$).

**Paso 3 — Recursión** ($O_3 = 1$):

Para el estado $S$ en $t=3$:

$$\delta_3(S) = \max(\delta_2(S) \cdot A_{SS}, \delta_2(\mathrm{R}) \cdot A_{RS}) \cdot B_{S,1}$$
$$= \max(0.0378 \times 0.7, 0.1296 \times 0.4) \times 0.1 = \max(0.02646, 0.05184) \times 0.1 = 0.005184$$
$$\psi_3(S) = \arg\max(0.02646, 0.05184) = R \text{ (índice 1)}$$

Para el estado $R$ en $t=3$:

$$\delta_3(\mathrm{R}) = \max(\delta_2(S) \cdot A_{SR}, \delta_2(\mathrm{R}) \cdot A_{RR}) \cdot B_{R,1}$$
$$= \max(0.0378 \times 0.3, 0.1296 \times 0.6) \times 0.8 = \max(0.01134, 0.07776) \times 0.8 = 0.06221$$
$$\psi_3(\mathrm{R}) = \arg\max(0.01134, 0.07776) = R \text{ (índice 1)}$$

**Tabla resumen de $\delta$ y $\psi$:**

| $t$ | $O_t$ | $\delta_t(S)$ | $\psi_t(S)$ | $\delta_t(\mathrm{R})$ | $\psi_t(\mathrm{R})$ |
|:---:|:-----:|:-------------:|:-----------:|:-------------:|:-----------:|
| 1 | 0 | 0.54000 | — | 0.08000 | — |
| 2 | 1 | 0.03780 | S | 0.12960 | S |
| 3 | 1 | 0.00518 | R | 0.06221 | R |

**Backtracking:**

1. Mejor estado en $t=3$: $q_3^∗ = \arg\max(\delta_3(S), \delta_3(\mathrm{R})) = \arg\max(0.00518, 0.06221) = R$
2. $q_2^∗ = \psi_3(\mathrm{R}) = R$
3. $q_1^∗ = \psi_2(\mathrm{R}) = S$

**Secuencia óptima: $S \to R \to R$**

Interpretación: el día sin paraguas fue soleado (lógico: B(S,0)=0.9), y los dos días con paraguas fueron lluviosos (lógico: B(R,1)=0.8). La cadena de Markov "prefiere" mantenerse en el mismo estado (A_SS=0.7, A_RR=0.6), lo que hace que S→R→R sea más probable que S→S→R o cualquier otra variación.

---

## 6. Pseudocódigo

```
función VITERBI(O, π, A, B):
    T ← longitud(O)
    N ← número de estados

    [P1] Inicialización:
        para i = 1 hasta N:
            δ[1][i] ← π[i] × B[i][O[1]]
            ψ[1][i] ← 0

    [P2] Recursión:
        para t = 2 hasta T:
            para j = 1 hasta N:
                mejor_val ← -∞
                mejor_i   ← 0
                para i = 1 hasta N:
                    val ← δ[t-1][i] × A[i][j]
                    si val > mejor_val:
                        mejor_val ← val
                        mejor_i   ← i
                δ[t][j] ← mejor_val × B[j][O[t]]
                ψ[t][j] ← mejor_i

    [P3] Terminación:
        q*[T] ← argmax_i δ[T][i]

    [P4] Backtracking:
        para t = T-1 hasta 1:
            q*[t] ← ψ[t+1][ q*[t+1] ]

    retornar q*, δ, ψ
```

---

## 7. Complejidad

Igual que Forward: $O(N^2 T)$ en tiempo, $O(NT)$ en espacio (más $O(NT)$ para los backpointers $\psi$). El cambio de suma a máximo no altera la complejidad asintótica — solo la naturaleza de la operación en el bucle interno.

---

## 8. Viterbi vs Forward: una última comparación

Una confusión frecuente: el estado de máxima probabilidad **marginal** $\arg\max_i \gamma_t(i)$ (donde $\gamma_t(i) = P(q_t=i \mid O, \lambda)$ es la posterior calculada en la sección 20.3) no es necesariamente el mismo que el estado de la secuencia de Viterbi $q_t^∗$.

¿Por qué? Porque $\gamma_t(i)$ maximiza cada instante de forma independiente, sin garantizar que la secuencia completa sea coherente (por ejemplo, podría resultar una secuencia donde la transición de $q_t^∗$ a $q_{t+1}^∗$ tiene probabilidad cero).

Viterbi maximiza la probabilidad de la **secuencia completa** conjuntamente, lo que garantiza una trayectoria coherente con las probabilidades de transición del modelo.

Usa $\gamma$ (Forward-Backward) cuando quieras el estado más probable en cada instante por separado. Usa Viterbi cuando quieras la secuencia más probable como un todo.
