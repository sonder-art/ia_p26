---
title: "Propiedades de las Cadenas de Markov"
---

| Notebook | Colab |
|---------|:-----:|
| Notebook 01 — Cadenas y simulación | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/19_cadenas_de_markov/notebooks/01_cadenas_y_simulacion.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |

---

# Propiedades de las Cadenas de Markov

> *"Not all chains converge. Understanding which ones do — and why — is the key to everything that follows."*

---

En la sección anterior definimos cadenas de Markov, construimos matrices de transición, y observamos un fenómeno notable: las potencias $\mathbf{P}^n$ convergen, las filas se vuelven idénticas, y la cadena "olvida" su estado inicial. Pero esto no ocurre siempre. Hay cadenas que no convergen, cadenas que oscilan, y cadenas cuyo comportamiento a largo plazo depende completamente de dónde empezaron.

Esta sección responde la pregunta: **¿qué condiciones debe cumplir una cadena para que la convergencia esté garantizada?** La respuesta involucra tres conceptos — clasificación de estados, irreducibilidad y aperiodicidad — y culmina con la distribución estacionaria y el teorema que conecta todo.

---

## 1. Clasificación de estados

Cada estado de una cadena de Markov se comporta de manera diferente a largo plazo. Clasificamos los estados según la probabilidad de que la cadena regrese a ellos después de salir.

**Estado transitorio.** Un estado (i) es **transitorio** si, comenzando en (i), la probabilidad de regresar a (i) alguna vez es **estrictamente menor que 1**. Equivalentemente, existe una probabilidad positiva de que, una vez que la cadena salga de (i), nunca vuelva a ese estado. Por ello, un estado transitorio solo puede ser visitado un número **finito de veces con probabilidad 1**.

**Estado recurrente.** Un estado (i) es **recurrente** si, comenzando en (i), la probabilidad de regresar a (i) alguna vez es **exactamente 1**. Equivalentemente, si la cadena sale de (i), volverá a ese estado **con probabilidad 1**. Por ello, un estado recurrente será visitado **infinitas veces con probabilidad 1**.

**Estado absorbente.** Un estado (i) es **absorbente** si, una vez que la cadena entra en él, nunca sale. Formalmente, ($P(i \to i) = 1$), es decir, la probabilidad de transición de (i) a sí mismo es 1, y a cualquier otro estado es 0. Un estado absorbente es un caso particular de estado recurrente, porque una vez que la cadena entra en él, permanece allí para siempre.

### Ejemplo: modelo de progresión estudiantil

Consideremos un modelo simplificado de la trayectoria de un estudiante universitario con estados:

$$S = \{1^{\text{er}} \text{sem},\; 2^{\text{do}} \text{sem},\; 3^{\text{er}} \text{sem},\; 4^{\text{to}} \text{sem},\; \text{Graduado},\; \text{Deserción}\}$$

- Los estados de semestre ($1^{\text{er}}$ a $4^{\text{to}}$) son **transitorios**: el estudiante pasa por ellos pero eventualmente los deja para siempre. No puedes estar en 2do semestre indefinidamente — o avanzas, o desertas.
- **Graduado** es **absorbente**: una vez que te gradúas, te quedas graduado. $P(\text{Graduado} \to \text{Graduado}) = 1$.
- **Deserción** es **absorbente**: una vez que abandonas, el modelo no contempla retorno. $P(\text{Deserción} \to \text{Deserción}) = 1$.

Observación importante: **la cadena V/C de la sección anterior NO tiene estados absorbentes**. Ambos estados — vocal y consonante — son recurrentes. La cadena siempre regresa a cada uno de ellos porque todas las probabilidades de transición son positivas. Esta distinción será crucial cuando hablemos de irreducibilidad.

![Clasificación de estados]({{ '/19_cadenas_de_markov/images/07_state_classification.png' | url }})

---

## 2. Irreducibilidad: "todos se comunican"

Una cadena de Markov es **irreducible** si desde cualquier estado se puede llegar a cualquier otro estado con probabilidad positiva (posiblemente en varios pasos). Formalmente: para todo par de estados $i, j \in S$, existe un entero $n \geq 1$ tal que $(\mathbf{P}^n)_{ij} > 0$.

En términos de grafos: el grafo de transición tiene un **único componente fuertemente conexo**. Hay un camino dirigido con probabilidad positiva entre cualquier par de nodos.

### Ejemplos

**Cadena V/C: irreducible.** Desde $V$ se puede llegar a $C$ en un paso ($P(V \to C) = 0.65 > 0$) y desde $C$ se puede llegar a $V$ en un paso ($P(C \to V) = 0.52 > 0$). Ambas direcciones son alcanzables.

**Cadena de mercado: irreducible.** Las 9 entradas de la matriz de transición son positivas — desde cualquier régimen se puede llegar a cualquier otro en un solo paso. Cuando toda la matriz tiene entradas positivas, la cadena es trivialmente irreducible.

**Modelo estudiantil: NO irreducible.** No existe ningún camino de Graduado a $1^{\text{er}}$ semestre — una vez graduado, no puedes regresar. El grafo de transición tiene varios componentes que no se comunican entre sí.

![Irreducible vs reducible]({{ '/19_cadenas_de_markov/images/08_irreducible_vs_reducible.png' | url }})

### ¿Qué pasa en cadenas reducibles?

Cuando una cadena NO es irreducible, el comportamiento a largo plazo **depende de dónde empieces**. Si el grafo de transición tiene dos componentes separados — digamos $\{A, B\}$ y $\{C, D\}$ — entonces:

- Si empiezas en $A$ o $B$, la cadena se queda en $\{A, B\}$ para siempre. Nunca visita $C$ o $D$.
- Si empiezas en $C$ o $D$, la cadena se queda en $\{C, D\}$ para siempre.
- Cada componente tiene su propia distribución estacionaria. No hay una sola $\pi$ que describa toda la cadena.
- El teorema ergódico **no aplica** a la cadena completa.

Esta es la primera razón por la que no todas las cadenas convergen: si la cadena no es irreducible, el largo plazo depende del inicio.

---

## 3. Aperiodicidad: "sin ritmo forzado"

### La intuición

Imagina una cadena que va $A \to B \to A \to B \to \ldots$ para siempre. Si empezaste en $A$, sabes con certeza que en tiempos pares (2, 4, 6, ...) estás en $A$ y en tiempos impares estás en $B$. La cadena tiene un **ritmo forzado** — un "reloj interno" que determina dónde puedes estar según la paridad del tiempo.

Esto es un problema porque **impide la convergencia**: las potencias $\mathbf{P}^n$ no se estabilizan, sino que oscilan entre distintas matrices indefinidamente. No existe una distribución límite.

Una cadena **aperiódica** es exactamente lo opuesto: no tiene ritmo forzado. Desde cualquier estado puedes regresar a él en distintos tiempos sin que haya un patrón de múltiplos obligatorio. Esto permite que $\mathbf{P}^n$ converja.

### Definición formal

El **periodo** de un estado $i$ es el máximo común divisor de todos los tiempos posibles de retorno:

$$d(i) = \gcd\{n \geq 1 : (\mathbf{P}^n)_{ii} > 0\}$$

- $d(i) = 1$: el estado es **aperiódico** — puede ser revisitado en tiempos sin un patrón de múltiplos forzado.
- $d(i) = 2$: solo se puede volver en tiempos pares ($2, 4, 6, \ldots$).
- $d(i) = k$: solo se puede volver en múltiplos de $k$.

Una cadena es **aperiódica** si todos sus estados tienen $d = 1$.

### Contraejemplo: cadena periódica con periodo 2

Estados $\{A, B\}$, cada uno fuerza al otro:

$$\mathbf{P} = \begin{pmatrix}
0 & 1 \\
1 & 0
\end{pmatrix}$$

$P(A \to B) = 1$ y $P(B \to A) = 1$. No hay otra opción — la trayectoria es determinista: $A \to B \to A \to B \to \ldots$

Calculemos las primeras potencias para ver qué pasa:

$$\mathbf{P}^2 = \begin{pmatrix}
1 & 0 \\
0 & 1
\end{pmatrix}, \qquad
\mathbf{P}^3 = \begin{pmatrix}
0 & 1 \\
1 & 0
\end{pmatrix}, \qquad
\mathbf{P}^4 = \begin{pmatrix}
1 & 0 \\
0 & 1
\end{pmatrix}, \qquad \ldots$$

$\mathbf{P}^n$ **oscila entre la identidad y la matriz original** — nunca se estabiliza. Interpetación: si empezaste en $A$, en tiempo par estás con certeza en $A$; en tiempo impar estás con certeza en $B$. No existe una distribución límite porque tu ubicación depende de la paridad del tiempo, no de cuánto tiempo ha pasado.

El periodo de $A$ es 2 porque los únicos tiempos de retorno posibles son $\{2, 4, 6, \ldots\}$ y $\gcd(2, 4, 6, \ldots) = 2$.

### Por qué la aperiodicidad importa: necesitas poder regresar en distintos tiempos

Para que $\mathbf{P}^n$ converja, necesitas que desde cualquier estado puedas regresar a él en **tiempos de distintas longitudes sin un factor común mayor que 1**. Si puedes regresar en tiempos 1 y 2, entonces $\gcd(1, 2) = 1$ y el periodo es 1. Si puedes regresar solo en $\{3, 6, 9, \ldots\}$, el periodo es 3 y las potencias oscilan con ese ritmo.

### La solución: un self-loop rompe el ritmo

Un **self-loop** — probabilidad positiva de quedarse en el mismo estado — introduce un tiempo de retorno de longitud 1. Eso es suficiente para romper cualquier periodicidad.

Si añadimos $P(A \to A) = 0.1$:

$$\mathbf{P} = \begin{pmatrix}
0.1 & 0.9 \\
1 & 0
\end{pmatrix}$$

Ahora desde $A$ puedo regresar a $A$ en 1 paso (self-loop) y también en 2 pasos ($A \to B \to A$). Los tiempos de retorno posibles incluyen $\{1, 2, 3, \ldots\}$, y $\gcd(1, 2) = 1$. Periodo = 1. La cadena es aperiódica.

> **Regla práctica**: en una cadena irreducible, basta con que **un solo estado** tenga un self-loop (probabilidad de quedarse $> 0$) para que toda la cadena sea aperiódica.

### La cadena V/C es aperiódica

$P(V \to V) = 0.35 > 0$ — hay self-loop en $V$. Los tiempos de retorno a $V$ incluyen 1 (self-loop directo) y 2 (vía $V \to C \to V$). Como $\gcd(1, 2) = 1$, el periodo es 1. Lo mismo aplica a $C$: $P(C \to C) = 0.48 > 0$.

La cadena V/C es aperiódica — y por eso sus potencias $\mathbf{P}^n$ convergen en lugar de oscilar.

![Periódica vs aperiódica]({{ '/19_cadenas_de_markov/images/09_periodic_vs_aperiodic.png' | url }})

---

## 4. Distribución estacionaria

Dado un vector de probabilidad $\pi = (\pi_1, \pi_2, \ldots, \pi_k)$ (entradas no negativas, suma igual a 1), decimos que $\pi$ es una **distribución estacionaria** de la cadena si:

$$\pi \mathbf{P} = \pi$$

Es decir: si distribuimos la cadena según $\pi$ y aplicamos un paso de transición, la distribución no cambia. $\pi$ es un **punto fijo** del operador de transición.

Interpretación: imagina un número muy grande de partículas distribuidas entre los estados según $\pi$. En cada paso, cada partícula se mueve según las probabilidades de $\mathbf{P}$. Después del paso, la proporción de partículas en cada estado sigue siendo $\pi$. El flujo de partículas que sale de cada estado es exactamente igual al flujo que entra.

### Cálculo guiado: resolver $\pi \mathbf{P} = \pi$ para la cadena V/C

La cadena V/C tiene la matriz de transición:

$$\mathbf{P} = \begin{pmatrix}
0.35 & 0.65 \\
0.52 & 0.48
\end{pmatrix}$$

Buscamos $\pi = (\pi_V, \pi_C)$ tal que $\pi \mathbf{P} = \pi$ y $\pi_V + \pi_C = 1$.

**Paso 1: escribir el sistema de ecuaciones.**

La condición $\pi \mathbf{P} = \pi$ se expande como:

$$\text{Ecuación 1: } \pi_V \cdot 0.35 + \pi_C \cdot 0.52 = \pi_V$$

$$\text{Ecuación 2: } \pi_V \cdot 0.65 + \pi_C \cdot 0.48 = \pi_C$$

$$\text{Ecuación 3: } \pi_V + \pi_C = 1$$

La Ecuación 2 es redundante con la Ecuación 1 (ambas dicen lo mismo porque las filas de $\mathbf{P}$ suman 1). Esto siempre ocurre — por eso necesitamos la Ecuación 3 como restricción adicional.

**Paso 2: despejar de la Ecuación 1.**

$$\pi_C \cdot 0.52 = \pi_V - \pi_V \cdot 0.35$$

$$\pi_C \cdot 0.52 = \pi_V \cdot (1 - 0.35)$$

$$\pi_C \cdot 0.52 = \pi_V \cdot 0.65$$

$$\pi_C = \pi_V \cdot \frac{0.65}{0.52} = \pi_V \cdot 1.25$$

**Paso 3: sustituir en la Ecuación 3.**

$$\pi_V + 1.25 \cdot \pi_V = 1$$

$$2.25 \cdot \pi_V = 1$$

$$\pi_V = \frac{1}{2.25} = 0.444\ldots$$

$$\pi_C = 1 - 0.444 = 0.556\ldots$$

**Paso 4: verificación.**

Comprobamos que $\pi \mathbf{P} = \pi$:

$$[0.444,\; 0.556] \times \mathbf{P} = [0.444 \times 0.35 + 0.556 \times 0.52,\;\; 0.444 \times 0.65 + 0.556 \times 0.48]$$

$$= [0.155 + 0.289,\;\; 0.289 + 0.267]$$

$$= [0.444,\;\; 0.556] = \pi \quad \checkmark$$

**Interpretación.** A largo plazo, aproximadamente el **44.4% de los caracteres son vocales** y el **55.6% son consonantes**. Esto coincide con lo que Markov encontró empíricamente al analizar *Eugenio Oneguin* en 1913.

**Conexión con la sección anterior.** Estos son exactamente los valores a los que convergían las potencias $\mathbf{P}^n$. Recuerda que ambas filas de $\mathbf{P}^{16}$ eran $[0.444, 0.556]$. La distribución estacionaria es el vector al que convergen las filas de $\mathbf{P}^n$ cuando $n \to \infty$.

![Distribución estacionaria]({{ '/19_cadenas_de_markov/images/10_stationary_distribution.png' | url }})

### Cálculo para la cadena de mercado

Para la cadena de regímenes de mercado ($3 \times 3$), el sistema $\pi \mathbf{P} = \pi$ con $\pi_A + \pi_B + \pi_L = 1$ se resuelve de forma análoga (aunque el álgebra es más extensa con 3 ecuaciones). El resultado es:

$$\pi \approx [0.34,\;\; 0.30,\;\; 0.36] \quad \text{para } [\text{Alcista},\; \text{Bajista},\; \text{Lateral}]$$

Interpretación: a largo plazo, el mercado pasa aproximadamente un **34% del tiempo en régimen alcista**, un **30% en régimen bajista**, y un **36% en régimen lateral**. Los tres regímenes tienen proporciones similares — el mercado no pasa dramáticamente más tiempo en un estado que en otro.

---

## 5. Existencia y unicidad

Hemos calculado distribuciones estacionarias para dos cadenas y observado que $\mathbf{P}^n$ converge. Pero, ¿siempre existe una distribución estacionaria? ¿Siempre es única? ¿Siempre hay convergencia?

La respuesta depende de las propiedades que acabamos de definir.

> **Teorema.** Si una cadena de Markov es **finita**, **irreducible** y **aperiódica**, entonces:
> 1. Existe una **única** distribución estacionaria $\pi$.
> 2. Para cualquier distribución inicial $\pi_0$, la distribución converge: $\pi_0 \mathbf{P}^n \to \pi$ cuando $n \to \infty$.
> 3. La cadena **"olvida" su estado inicial**: el comportamiento a largo plazo es independiente de dónde empezó.

La siguiente sección (04) demuestra **por qué** esto ocurre usando el argumento de acoplamiento — una de las ideas más elegantes de la teoría de probabilidad.

### Resumen: ¿qué pasa si falta una condición?

| Condición | Qué garantiza | Si falta... |
|---|---|---|
| Finita | Cálculo tratable | Cadenas infinitas requieren herramientas más avanzadas |
| Irreducible | $\pi$ única | Múltiples $\pi$ posibles (depende del inicio) |
| Aperiódica | $\mathbf{P}^n$ converge | $\mathbf{P}^n$ oscila sin converger |

Las tres condiciones juntas forman lo que se llama una cadena **ergódica**. Ambas cadenas de este módulo — V/C y mercado — son ergódicas: finitas, irreducibles y aperiódicas. El modelo estudiantil, en cambio, no lo es (no es irreducible). La cadena periódica $A \leftrightarrow B$ tampoco (no es aperiódica). Solo las cadenas ergódicas gozan de la convergencia completa que el teorema garantiza.

---

**[← Cadenas de Markov](02_cadenas_de_markov.md)** · **Siguiente:** [Teorema Ergódico →](04_teorema_ergodico.md)
