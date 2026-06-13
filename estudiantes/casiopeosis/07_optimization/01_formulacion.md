---
title: "Formulación matemática de problemas de optimización"
---

# Formulación matemática de problemas de optimización

Antes de resolver un problema de optimización, hay que **escribirlo**. Esta sección enseña el lenguaje estándar: cómo expresar qué quieres optimizar, sobre qué variables, y bajo qué restricciones.

---

## Anatomía de un problema de optimización

Todo problema de optimización tiene **3 componentes**:

### 1. Función objetivo $f(x)$

Lo que quieres minimizar (o maximizar). Es una función que toma tus variables de decisión y devuelve un número real.

$$f: \mathbb{R}^n \to \mathbb{R}$$

### 2. Variables de decisión $x \in \mathbb{R}^n$

Los "botones que puedes girar". Son los valores que controlas y quieres encontrar.

$$x = (x_1, x_2, \ldots, x_n)$$

### 3. Restricciones

Límites sobre los valores permitidos de $x$. Hay tres tipos:

| Tipo | Notación | Ejemplo |
|------|----------|---------|
| Igualdad | $h_i(x) = 0$ | $x_1 + x_2 = 1$ |
| Desigualdad | $g_j(x) \leq 0$ | $x_1^2 + x_2^2 - 1 \leq 0$ |
| Cotas | $l_k \leq x_k \leq u_k$ | $0 \leq x_1 \leq 10$ |

---

## Forma estándar

La forma estándar de un problema de optimización es:

$$
\min_{x \in \mathbb{R}^n} f(x)
$$

sujeto a:

$$
\begin{aligned}
h_i(x) &= 0, \quad i = 1, \ldots, p \\
g_j(x) &\leq 0, \quad j = 1, \ldots, m \\
x &\in \mathcal{X}
\end{aligned}
$$

donde $\mathcal{X}$ representa las cotas sobre las variables.

---

## Equivalencia min $\leftrightarrow$ max

Maximizar $f(x)$ es lo mismo que minimizar $-f(x)$:

$$\max_x f(x) = -\min_x \bigl(-f(x)\bigr)$$

Por convención, la mayoría de los textos y software usan **minimización**. Si tu problema es de maximización, simplemente niega la función objetivo.

---

## Sin restricciones vs con restricciones

| | Sin restricciones | Con restricciones |
|---|---|---|
| **Forma** | $\min_x f(x)$ | $\min_x f(x)$ sujeto a $g(x) \leq 0$, $h(x) = 0$ |
| **Ejemplo** | Mínimos cuadrados | Programación lineal |
| **Dificultad** | Generalmente más fácil | Más difícil (hay que respetar la región factible) |
| **Algoritmos típicos** | Descenso de gradiente | Simplex, puntos interiores, Lagrange |

> **Notebook — Abre NB1: Función objetivo**
> <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/07_optimization/notebooks/01_formulacion_y_paisaje.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
>
> 1. Completa la función `ganancia()` y verifica con el assert.
> 2. Cambia los precios a &#36;7 y &#36;2 — ¿cómo cambia la ganancia?
> 3. ¿Qué pasa si un producto tiene ganancia negativa?

---

## Ejemplos

:::example{title="Ejemplo 1: Producción (programación lineal)"}

Una fábrica produce dos productos ($x_1$ y $x_2$). Cada unidad de producto 1 genera &#36;5 de ganancia; cada unidad de producto 2 genera &#36;4. Pero los recursos son limitados:

- Recurso A: cada unidad de producto 1 usa 6 unidades, cada unidad de producto 2 usa 4 unidades. Disponible: 24.
- Recurso B: cada unidad de producto 1 usa 1 unidad, cada unidad de producto 2 usa 2 unidades. Disponible: 6.
- No se pueden producir cantidades negativas.

**Formulación:**

$$
\max_{x_1, x_2} \quad 5x_1 + 4x_2
$$

sujeto a:

$$
\begin{aligned}
6x_1 + 4x_2 &\leq 24 \\
x_1 + 2x_2 &\leq 6 \\
x_1, x_2 &\geq 0
\end{aligned}
$$

En notación matricial: $\max \, c^T x$ sujeto a $Ax \leq b$, $x \geq 0$, donde:

$$
c = \begin{pmatrix} 5 \\ 4 \end{pmatrix}, \quad
A = \begin{pmatrix} 6 & 4 \\ 1 & 2 \end{pmatrix}, \quad
b = \begin{pmatrix} 24 \\ 6 \end{pmatrix}
$$

:::

:::example{title="Ejemplo 2: Mínimos cuadrados (regresión)"}

Tienes datos $(x_i, y_i)$ para $i = 1, \ldots, N$ y quieres encontrar el parámetro $\beta$ que mejor ajusta una línea $y = \beta x$.

**Formulación:**

$$
\min_{\beta} \sum_{i=1}^{N} (y_i - \beta x_i)^2
$$

Esto es un problema **sin restricciones**. La función objetivo es la suma de errores al cuadrado. La variable de decisión es $\beta \in \mathbb{R}$.

Nota: este problema tiene **solución cerrada** (derivar, igualar a cero, despejar):

$$
\beta^{∗} = \frac{\sum_i x_i y_i}{\sum_i x_i^2}
$$

Pero cuando el modelo es más complejo (redes neuronales, por ejemplo), no hay solución cerrada y necesitamos algoritmos iterativos.

:::

:::example{title="Ejemplo 3: Clasificación con margen (estilo SVM)"}

Quieres separar dos clases de puntos con un hiperplano $w^T x + b = 0$, maximizando el **margen** (distancia al punto más cercano).

**Formulación:**

$$
\min_{w, b} \quad \frac{1}{2} \|w\|^2
$$

sujeto a:

$$
y_i (w^T x_i + b) \geq 1, \quad i = 1, \ldots, N
$$

donde $y_i \in \{-1, +1\}$ es la etiqueta de clase.

- **Objetivo**: minimizar $\|w\|^2$ (equivale a maximizar el margen $\frac{2}{\|w\|}$).
- **Variables**: $w \in \mathbb{R}^n$, $b \in \mathbb{R}$.
- **Restricciones**: cada punto debe estar del lado correcto del margen.

:::

:::example{title="Ejemplo 4: Regularización — ajuste vs simplicidad"}

¿Qué pasa si el modelo de mínimos cuadrados (Ejemplo 2) sobreajusta? Añadimos un **término de penalización** que castiga pesos grandes:

**Ridge regression** (penalización L2):

$$\min_w \|y - Xw\|^2 + \lambda \|w\|^2$$

**Lasso** (penalización L1):

$$\min_w \|y - Xw\|^2 + \lambda \|w\|_1$$

El hiperparámetro $\lambda \geq 0$ es la "perilla" que controla el balance entre **ajuste a los datos** (primer término) y **simplicidad del modelo** (segundo término):
- $\lambda = 0$: mínimos cuadrados ordinarios (sin regularización)
- $\lambda \to \infty$: todos los pesos se van a cero

**¿Por qué dos penalizaciones?**
- **L2 (Ridge)**: pesos pequeños pero no cero — regularización suave
- **L1 (Lasso)**: muchos pesos exactamente cero — **selección de variables** automática

**Conexión con restricciones:** Ridge es equivalente a un problema con restricción:

$$\min_w \|y - Xw\|^2 \quad \text{s.t.} \quad \|w\|^2 \leq t$$

Es decir, regularizar es optimizar sobre una **bola** en el espacio de parámetros. El $\lambda$ del Lagrangiano controla el radio $t$. Esta dualidad entre penalización y restricción aparece constantemente en optimización y ML.

:::

> **Notebook — Abre NB1: Producción (LP)**
> <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/07_optimization/notebooks/01_formulacion_y_paisaje.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
>
> 1. Escribe las matrices $c$, $A$, $b$ como arrays de numpy.
> 2. Verifica que $x = (2, 1)$ es factible.
> 3. Encuentra $x = (3, 1.5)$ y confirma que es la solución óptima.

---

## Receta para formular

Cuando te encuentres un problema de optimización "en palabras", sigue estos pasos:

1. **¿Qué controlas?** → Variables de decisión $x$
2. **¿Qué quieres optimizar?** → Función objetivo $f(x)$ (¿minimizar o maximizar?)
3. **¿Qué limitaciones hay?** → Restricciones $g(x) \leq 0$, $h(x) = 0$, cotas

:::exercise{title="Ejercicio: Formula el problema" difficulty="2"}

Una empresa de logística tiene 3 rutas para enviar paquetes. Cada ruta $i$ tiene:
- Un costo por paquete $c_i$: ruta 1 cuesta &#36;2, ruta 2 cuesta &#36;5, ruta 3 cuesta &#36;3.
- Una capacidad máxima: ruta 1 puede llevar 100 paquetes, ruta 2 puede llevar 80, ruta 3 puede llevar 120.

La empresa necesita enviar **exactamente 200 paquetes** en total y quiere minimizar el costo.

**Tarea:** Escribe la función objetivo $f(x)$, las variables de decisión $x$, y todas las restricciones.

<details>
<summary><strong>Ver Solución</strong></summary>

**Variables de decisión:** $x_i$ = número de paquetes enviados por la ruta $i$, para $i \in \{1, 2, 3\}$.

**Función objetivo:**

$$\min_{x_1, x_2, x_3} \quad 2x_1 + 5x_2 + 3x_3$$

**Restricciones:**

$$
\begin{aligned}
x_1 + x_2 + x_3 &= 200 \quad \text{(demanda exacta)} \\
x_1 &\leq 100 \\
x_2 &\leq 80 \\
x_3 &\leq 120 \\
x_1, x_2, x_3 &\geq 0
\end{aligned}
$$

</details>

:::

---

**Siguiente:** [Paisaje y conceptos →](02_paisaje_y_conceptos.md)
