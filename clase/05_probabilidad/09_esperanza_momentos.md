---
title: "Esperanza y Momentos"
---

# Esperanza y Momentos

Resumiendo distribuciones con números clave.

## Valor Esperado (Esperanza)

El **valor esperado** de una variable aleatoria es su "promedio ponderado por probabilidad".

### Definición: Caso Discreto

$$E[X] = \sum_x x \cdot P(X = x)$$

### Definición: Caso Continuo

$$E[X] = \int_{-\infty}^{\infty} x \cdot f_X(x) \, dx$$

### Notación

- $E[X]$ — Valor esperado de X
- $\mu$ o $\mu_X$ — Media de X (sinónimo)
- $\langle X \rangle$ — Notación alternativa (física)

---

## Ejemplos

### Dado Justo

$$E[X] = \sum_{i=1}^{6} i \cdot \frac{1}{6} = \frac{1+2+3+4+5+6}{6} = \frac{21}{6} = 3.5$$

**Interpretación:** Si lanzas muchas veces, el promedio de resultados será ~3.5.

### Moneda (Bernoulli)

$X = 1$ si cara, $X = 0$ si cruz, con $P(\text{cara}) = p$

$$E[X] = 1 \cdot p + 0 \cdot (1-p) = p$$

### Distribución Normal

Si $X \sim \mathcal{N}(\mu, \sigma^2)$:

$$E[X] = \mu$$

(Por simetría alrededor de $\mu$)

---

## Propiedades de la Esperanza

### Linealidad

$$E[aX + b] = a \cdot E[X] + b$$

$$E[X + Y] = E[X] + E[Y]$$

**Nota:** La suma funciona **siempre**, incluso si X e Y son dependientes.

### Esperanza de una Función

$$E[g(X)] = \sum_x g(x) \cdot P(X = x)$$

**Cuidado:** En general, $E[g(X)] \neq g(E[X])$

Por ejemplo: $E[X^2] \neq (E[X])^2$ (en general)

---

## Varianza

La **varianza** mide cuánto se dispersan los valores alrededor de la media.

### Definición

$$\text{Var}(X) = E[(X - \mu)^2]$$

Donde $\mu = E[X]$.

### Fórmula Alternativa (útil para cálculos)

$$\text{Var}(X) = E[X^2] - (E[X])^2$$

### Notación

- $\text{Var}(X)$ o $\sigma^2$ — Varianza
- $\sigma = \sqrt{\text{Var}(X)}$ — **Desviación estándar** (mismas unidades que X)

---

## Propiedades de la Varianza

### Invarianza ante traslación

$$\text{Var}(X + c) = \text{Var}(X)$$

Agregar una constante no cambia la dispersión.

### Escalamiento

$$\text{Var}(aX) = a^2 \cdot \text{Var}(X)$$

### Suma de Variables Independientes

Si X e Y son **independientes**:

$$\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y)$$

**Cuidado:** Esta fórmula NO aplica si X e Y son dependientes.

---

## Ejemplos de Varianza

### Dado Justo

$E[X] = 3.5$

$E[X^2] = \frac{1^2 + 2^2 + 3^2 + 4^2 + 5^2 + 6^2}{6} = \frac{91}{6} \approx 15.17$

$\text{Var}(X) = E[X^2] - (E[X])^2 = \frac{91}{6} - 3.5^2 = 15.17 - 12.25 = 2.92$

$\sigma = \sqrt{2.92} \approx 1.71$

### Distribución Normal

Si $X \sim \mathcal{N}(\mu, \sigma^2)$:

$$\text{Var}(X) = \sigma^2$$

(El parámetro $\sigma^2$ ES la varianza)

---

## Momentos

Los **momentos** son valores esperados de potencias de X.

### Momento n-ésimo (alrededor del origen)

$$\mu'_n = E[X^n]$$

### Momento n-ésimo central (alrededor de la media)

$$\mu_n = E[(X - \mu)^2]$$

### Momentos Importantes

| Momento | Nombre | Significado |
|---------|--------|-------------|
| $E[X]$ | Primer momento | Centro (media) |
| $E[(X-\mu)^2]$ | Segundo momento central | Dispersión (varianza) |
| $E[(X-\mu)^3]/\sigma^3$ | Asimetría (skewness) | ¿Distribución simétrica? |
| $E[(X-\mu)^4]/\sigma^4$ | Curtosis | ¿Colas pesadas? |

---

## Covarianza

La **covarianza** mide cómo dos variables varían juntas.

### Definición

$$\text{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)]$$

### Fórmula Alternativa

$$\text{Cov}(X, Y) = E[XY] - E[X]E[Y]$$

### Interpretación

| Valor | Significado |
|-------|-------------|
| $\text{Cov}(X,Y) > 0$ | X e Y tienden a moverse juntas |
| $\text{Cov}(X,Y) < 0$ | X e Y tienden a moverse en direcciones opuestas |
| $\text{Cov}(X,Y) = 0$ | Sin relación lineal (pero pueden ser dependientes) |

### Propiedades

$$\text{Cov}(X, X) = \text{Var}(X)$$

$$\text{Cov}(X, Y) = \text{Cov}(Y, X)$$

$$\text{Cov}(aX, bY) = ab \cdot \text{Cov}(X, Y)$$

---

## Correlación

La **correlación** es la covarianza normalizada.

### Definición

$$\rho_{XY} = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y}$$

### Propiedades

- $-1 \leq \rho \leq 1$
- $\rho = 1$: Relación lineal positiva perfecta
- $\rho = -1$: Relación lineal negativa perfecta
- $\rho = 0$: Sin correlación lineal

### Correlación vs Independencia

- Independientes → $\rho = 0$ (no correlacionadas)
- $\rho = 0$ → **NO implica** independencia

Ejemplo: $Y = X^2$ donde $X \sim \text{Uniform}(-1, 1)$
- $\text{Cov}(X, Y) = 0$ (simétrico)
- Pero X e Y son completamente dependientes

---

## Varianza de una Suma (General)

Para cualquier X e Y (no necesariamente independientes):

$$\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\text{Cov}(X, Y)$$

**Caso especial:** Si son independientes, $\text{Cov}(X,Y) = 0$, recuperamos:
$$\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y)$$

---

## Esperanza Condicional

La **esperanza condicional** es el valor esperado dado cierta información.

### Definición

$$E[X|Y=y] = \sum_x x \cdot P(X=x|Y=y)$$

### La Ley de la Esperanza Total

$$E[X] = E[E[X|Y]]$$

En palabras: El promedio de los promedios condicionales es el promedio total.

---

## Aplicaciones

### En IA: Funciones de Pérdida

El **riesgo esperado** es:

$$R(h) = E[L(h(X), Y)]$$

Donde $L$ es la función de pérdida.

### En Decisiones: Valor Esperado

$$\text{Valor de acción } a = E[\text{recompensa}|a]$$

### En Estadística: Estimadores

Un estimador $\hat{\theta}$ es **insesgado** si:

$$E[\hat{\theta}] = \theta$$

---

## Resumen

| Concepto | Fórmula | Significado |
|----------|---------|-------------|
| **Esperanza** | $E[X] = \sum x \cdot P(x)$ | Centro de la distribución |
| **Varianza** | $\text{Var}(X) = E[(X-\mu)^2]$ | Dispersión |
| **Desv. estándar** | $\sigma = \sqrt{\text{Var}(X)}$ | Dispersión en unidades originales |
| **Covarianza** | $\text{Cov}(X,Y) = E[(X-\mu_X)(Y-\mu_Y)]$ | Co-variación |
| **Correlación** | $\rho = \text{Cov}(X,Y)/(\sigma_X \sigma_Y)$ | Covarianza normalizada [-1, 1] |

### Propiedades Clave

- Esperanza es **lineal**: $E[aX + bY] = aE[X] + bE[Y]$
- Varianza escala al **cuadrado**: $\text{Var}(aX) = a^2\text{Var}(X)$
- Para independientes: $\text{Var}(X+Y) = \text{Var}(X) + \text{Var}(Y)$

---

**Anterior:** [Teorema de Bayes ←](08_bayes.md)

**Volver al índice:** [Índice →](00_index.md)
