---
title: "Teorema de Bayes"
---

# Teorema de Bayes

La joya de la corona: cómo actualizar creencias con evidencia.

## Derivación desde la Regla del Producto

El Teorema de Bayes no es un axioma adicional — es una **consecuencia directa** de la regla del producto.

### Punto de Partida

La regla del producto dice:
$$P(AB|C) = P(A|BC) \cdot P(B|C)$$

Pero también:
$$P(AB|C) = P(B|AC) \cdot P(A|C)$$

### Igualando

Como ambas expresan $P(AB|C)$:
$$P(A|BC) \cdot P(B|C) = P(B|AC) \cdot P(A|C)$$

### Despejando

$$P(A|BC) = \frac{P(B|AC) \cdot P(A|C)}{P(B|C)}$$

**¡Este es el Teorema de Bayes!**

---

## La Forma Estándar

Usando la notación tradicional:

$$P(H|D, I) = \frac{P(D|H, I) \cdot P(H|I)}{P(D|I)}$$

Donde:
- $H$ = **Hipótesis** (lo que queremos saber)
- $D$ = **Datos** (evidencia observada)
- $I$ = **Información de fondo** (contexto)

---

## Los Cuatro Términos

| Término | Nombre | Significado |
|---------|--------|-------------|
| $P(H\|D,I)$ | **Posterior** | Probabilidad de H después de ver los datos |
| $P(D\|H,I)$ | **Likelihood** | Probabilidad de los datos si H es verdadera |
| $P(H\|I)$ | **Prior** | Probabilidad de H antes de ver los datos |
| $P(D\|I)$ | **Evidencia** | Probabilidad total de los datos |

### La Fórmula en Palabras

$$\text{Posterior} = \frac{\text{Likelihood} \times \text{Prior}}{\text{Evidencia}}$$

O más intuitivamente:

$$\text{Nueva creencia} = \frac{\text{Qué tan bien H explica los datos} \times \text{Creencia previa}}{\text{Normalización}}$$

---

## El Factor de Normalización

El denominador $P(D|I)$ se calcula por marginalización:

$$P(D|I) = \sum_i P(D|H_i, I) \cdot P(H_i|I)$$

Donde $\{H_i\}$ son todas las hipótesis posibles (partición).

**Función:** Asegurar que los posteriors sumen 1.

---

## Ejemplo: Diagnóstico Médico

**Situación:**
- 1% de la población tiene cierta enfermedad: $P(E|I) = 0.01$
- El test detecta la enfermedad en 95% de enfermos: $P(T^+|E,I) = 0.95$
- El test da falso positivo en 5% de sanos: $P(T^+|\neg E,I) = 0.05$

**Pregunta:** Si el test es positivo, ¿probabilidad de enfermedad?

### Aplicando Bayes

$$P(E|T^+, I) = \frac{P(T^+|E,I) \cdot P(E|I)}{P(T^+|I)}$$

**Calculando el denominador:**
$$P(T^+|I) = P(T^+|E,I) \cdot P(E|I) + P(T^+|\neg E,I) \cdot P(\neg E|I)$$
$$= 0.95 \times 0.01 + 0.05 \times 0.99$$
$$= 0.0095 + 0.0495 = 0.059$$

**Aplicando la fórmula:**
$$P(E|T^+, I) = \frac{0.95 \times 0.01}{0.059} = \frac{0.0095}{0.059} \approx 0.16$$

### Interpretación

A pesar del test positivo, solo hay ~16% de probabilidad de enfermedad.

**¿Por qué tan bajo?**
- El prior es muy bajo (1%)
- Aunque el test es bueno, los falsos positivos de la población sana dominan

---

## El Prior: ¿De Dónde Viene?

El prior $P(H|I)$ representa lo que sabíamos **antes** de ver los datos.

### Fuentes de Priors

| Fuente | Ejemplo |
|--------|---------|
| **Frecuencias conocidas** | "1% de la población tiene la enfermedad" |
| **Conocimiento experto** | "Los físicos asignan alta probabilidad a la relatividad" |
| **Principios de simetría** | "Si no sé nada, asigno igual probabilidad a cada cara del dado" |
| **Máxima entropía** | "La distribución que hace menos suposiciones" |

### La Posición de Jaynes

El prior NO es "subjetivo" en el sentido de arbitrario:
- Dado el mismo conocimiento previo $I$, todos deben asignar el mismo prior
- El prior **codifica** la información disponible
- Hay métodos objetivos para elegir priors (entropía máxima)

---

## Actualización Secuencial

Bayes permite actualizar creencias paso a paso:

$$P(H|D_1, I) = \frac{P(D_1|H,I) \cdot P(H|I)}{P(D_1|I)}$$

Luego, con nuevos datos $D_2$:

$$P(H|D_2, D_1, I) = \frac{P(D_2|H, D_1, I) \cdot P(H|D_1, I)}{P(D_2|D_1, I)}$$

**El posterior de hoy es el prior de mañana.**

### Ejemplo: Moneda Sospechosa

Sospecho que una moneda puede estar sesgada. Mi prior es $P(\text{justa}) = 0.5$.

- Lanzo 1: Sale cara → actualizo
- Lanzo 2: Sale cara → actualizo
- Lanzo 3: Sale cara → actualizo
- ...

Con cada observación, mi creencia se actualiza. Después de muchas caras seguidas, $P(\text{justa})$ será muy baja.

---

## Odds y Bayes Factor

Una forma alternativa de expresar Bayes:

### Odds (Momios)

$$\text{Odds}(H) = \frac{P(H)}{P(\neg H)}$$

### Bayes Factor

$$\text{BF} = \frac{P(D|H)}{P(D|\neg H)}$$

### La Forma de Odds

$$\frac{P(H|D)}{P(\neg H|D)} = \frac{P(H)}{P(\neg H)} \times \frac{P(D|H)}{P(D|\neg H)}$$

$$\text{Posterior Odds} = \text{Prior Odds} \times \text{Bayes Factor}$$

**Ventaja:** No necesitas calcular $P(D)$.

---

## Aplicaciones en IA

### Clasificación Bayesiana

Clasificar un email como spam o no-spam:

$$P(\text{spam}|\text{palabras}) \propto P(\text{palabras}|\text{spam}) \cdot P(\text{spam})$$

### Inferencia en Redes Bayesianas

Propagar probabilidades en grafos de variables:
- Usar Bayes para actualizar nodos
- Marginalizar para obtener probabilidades de interés

### Aprendizaje Bayesiano

En lugar de un solo parámetro, mantener una **distribución** sobre parámetros:

$$P(\theta|D) = \frac{P(D|\theta) \cdot P(\theta)}{P(D)}$$

---

## Errores Comunes

### 1. Ignorar el Prior (Base Rate Neglect)

"El test es 99% preciso, así que 99% de probabilidad de enfermedad"

**Error:** Ignora que la enfermedad es rara.

### 2. Confundir P(A|B) con P(B|A)

"P(positivo|enfermo) = 0.95" no es lo mismo que "P(enfermo|positivo)"

**Error:** La falacia del fiscal.

### 3. Prior Inadecuado

Elegir priors por conveniencia sin justificación.

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| **Teorema de Bayes** | Se deriva de la regla del producto |
| **Prior** | Creencia antes de ver datos |
| **Likelihood** | Qué tan bien la hipótesis explica los datos |
| **Posterior** | Creencia después de ver datos |
| **Evidencia** | Normalizador; probabilidad total de los datos |
| **Actualización** | El posterior de hoy es el prior de mañana |

### La Fórmula

$$P(H|D,I) = \frac{P(D|H,I) \cdot P(H|I)}{P(D|I)}$$

Esta simple ecuación es la base de:
- Inferencia estadística
- Aprendizaje automático
- Toma de decisiones bajo incertidumbre
- Inteligencia artificial

---

**Siguiente:** [Esperanza y Momentos →](09_esperanza_momentos.md)
