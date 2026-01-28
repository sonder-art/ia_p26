---
title: "Conceptos Básicos de Probabilidad"
---

# Conceptos Básicos de Probabilidad

Los elementos fundamentales del lenguaje probabilístico.

## Espacio Muestral

El **espacio muestral** $\Omega$ es el conjunto de todos los resultados posibles de un experimento o situación.

### Ejemplos

| Experimento | Espacio Muestral $\Omega$ |
|-------------|---------------------------|
| Lanzar una moneda | $\{cara, cruz\}$ |
| Lanzar un dado | $\{1, 2, 3, 4, 5, 6\}$ |
| Temperatura mañana | $\mathbb{R}$ (o un intervalo) |
| Resultado de un partido | $\{victoria, empate, derrota\}$ |

**Requisito:** Los elementos de $\Omega$ deben ser:
- **Mutuamente excluyentes:** Solo uno puede ocurrir
- **Colectivamente exhaustivos:** Uno debe ocurrir

---

## Eventos

Un **evento** $A$ es un subconjunto del espacio muestral: $A \subseteq \Omega$

### Ejemplos

Para un dado ($\Omega = \{1,2,3,4,5,6\}$):

| Evento | Subconjunto |
|--------|-------------|
| "Sacar par" | $\{2, 4, 6\}$ |
| "Sacar más de 4" | $\{5, 6\}$ |
| "Sacar 3" | $\{3\}$ |
| "Sacar algo" | $\{1,2,3,4,5,6\} = \Omega$ |
| "Sacar 7" | $\emptyset$ |

### Operaciones con Eventos

| Operación | Notación | Significado |
|-----------|----------|-------------|
| Unión | $A \cup B$ | "A o B (o ambos)" |
| Intersección | $A \cap B$ | "A y B" |
| Complemento | $A^c$ o $\bar{A}$ | "No A" |
| Diferencia | $A \setminus B$ | "A pero no B" |

---

## Medida de Probabilidad

Una **medida de probabilidad** $P$ asigna un número a cada evento, satisfaciendo:

### Axiomas de Kolmogorov (1933)

1. **No negatividad:** $P(A) \geq 0$ para todo evento $A$

2. **Normalización:** $P(\Omega) = 1$

3. **Aditividad:** Si $A$ y $B$ son disjuntos ($A \cap B = \emptyset$):
   $$P(A \cup B) = P(A) + P(B)$$

### Consecuencias Inmediatas

De estos axiomas se derivan:

| Propiedad | Fórmula |
|-----------|---------|
| Probabilidad del vacío | $P(\emptyset) = 0$ |
| Complemento | $P(A^c) = 1 - P(A)$ |
| Rango | $0 \leq P(A) \leq 1$ |
| Monotonía | Si $A \subseteq B$, entonces $P(A) \leq P(B)$ |
| Unión general | $P(A \cup B) = P(A) + P(B) - P(A \cap B)$ |

---

## Notación

Usaremos varias notaciones equivalentes:

| Notación | Significado |
|----------|-------------|
| $P(A)$ | Probabilidad del evento A |
| $P(A \cap B)$ | Probabilidad de A y B |
| $P(AB)$ | Abreviación de $P(A \cap B)$ |
| $P(A \| B)$ | Probabilidad de A dado B |
| $P(A, B \| C)$ | $P(A \cap B \| C)$ |

**Convención de Jaynes:** Siempre escribir la información condicionante:
- $P(A|I)$ en lugar de $P(A)$
- Donde $I$ es el conocimiento de fondo

---

## Variables Aleatorias

Una **variable aleatoria** $X$ es una función que asigna un número a cada resultado:

$$X: \Omega \to \mathbb{R}$$

### Ejemplo

Lanzar dos dados. Sea $X = $ "suma de los dados"

- $\Omega = \{(1,1), (1,2), ..., (6,6)\}$ (36 pares)
- $X((3,4)) = 7$
- $X((1,1)) = 2$

### Tipos

| Tipo | Valores | Ejemplo |
|------|---------|---------|
| **Discreta** | Contables | Número de caras en 10 lanzamientos |
| **Continua** | Intervalo | Altura de una persona |

---

## Distribución de Probabilidad

La **distribución** de una variable aleatoria $X$ describe cómo se distribuye la probabilidad sobre sus valores.

### Caso Discreto

**Función de masa de probabilidad (PMF):**
$$p_X(x) = P(X = x)$$

**Propiedades:**
- $p_X(x) \geq 0$
- $\sum_x p_X(x) = 1$

### Caso Continuo

**Función de densidad de probabilidad (PDF):**
$$f_X(x)$$

**Propiedades:**
- $f_X(x) \geq 0$
- $\int_{-\infty}^{\infty} f_X(x) dx = 1$
- $P(a \leq X \leq b) = \int_a^b f_X(x) dx$

**Nota:** $f_X(x)$ NO es una probabilidad. Puede ser mayor que 1.

---

## Distribuciones Comunes

### Discretas

| Distribución | Notación | Uso típico |
|--------------|----------|------------|
| Bernoulli | $\text{Bernoulli}(p)$ | Éxito/fracaso |
| Binomial | $\text{Binomial}(n, p)$ | Número de éxitos en n intentos |
| Poisson | $\text{Poisson}(\lambda)$ | Eventos raros |
| Geométrica | $\text{Geom}(p)$ | Intentos hasta primer éxito |

### Continuas

| Distribución | Notación | Uso típico |
|--------------|----------|------------|
| Uniforme | $\text{Uniform}(a, b)$ | Ignorancia sobre un intervalo |
| Normal/Gaussiana | $\mathcal{N}(\mu, \sigma^2)$ | La más común; límite central |
| Exponencial | $\text{Exp}(\lambda)$ | Tiempos de espera |
| Beta | $\text{Beta}(\alpha, \beta)$ | Probabilidades desconocidas |

---

## La Distribución Normal

Por su importancia, destacamos la **distribución normal** (Gaussiana):

$$f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

**Parámetros:**
- $\mu$ = media (centro)
- $\sigma^2$ = varianza (dispersión)

**Propiedades:**
- Simétrica alrededor de $\mu$
- ~68% de los datos en $[\mu - \sigma, \mu + \sigma]$
- ~95% de los datos en $[\mu - 2\sigma, \mu + 2\sigma]$
- ~99.7% de los datos en $[\mu - 3\sigma, \mu + 3\sigma]$

**¿Por qué tan común?** El Teorema del Límite Central explica por qué aparece en tantos contextos.

---

## Resumen

| Concepto | Notación | Descripción |
|----------|----------|-------------|
| Espacio muestral | $\Omega$ | Todos los resultados posibles |
| Evento | $A \subseteq \Omega$ | Subconjunto de resultados |
| Probabilidad | $P(A)$ | Número en [0,1] asignado a A |
| Variable aleatoria | $X: \Omega \to \mathbb{R}$ | Función numérica sobre resultados |
| PMF (discreta) | $p_X(x)$ | $P(X = x)$ |
| PDF (continua) | $f_X(x)$ | Densidad (no probabilidad) |

---

**Siguiente:** [Probabilidad Condicional y Marginal →](06_condicional_marginal.md)
