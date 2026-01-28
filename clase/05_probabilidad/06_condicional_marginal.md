---
title: "Probabilidad Condicional y Marginal"
---

# Probabilidad Condicional y Marginal

Cómo la información afecta nuestras creencias.

## Probabilidad Condicional

La **probabilidad condicional** de $A$ dado $B$ es la probabilidad de $A$ cuando sabemos que $B$ es verdadero.

### Definición

$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

siempre que $P(B) > 0$.

### Interpretación

- **Frecuentista:** De todos los casos donde $B$ ocurre, ¿en qué fracción también ocurre $A$?
- **Jaynes:** Dado que sabemos $B$, ¿cuál es la plausibilidad de $A$?

### Ejemplo: Dados

Lanzamos un dado justo. Sea:
- $A$ = "salió 6"
- $B$ = "salió número par"

$$P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{P(\{6\})}{P(\{2,4,6\})} = \frac{1/6}{3/6} = \frac{1}{3}$$

Saber que salió par aumenta la probabilidad de 6 (de 1/6 a 1/3).

---

## La Perspectiva de Jaynes

En el enfoque de Jaynes, **toda probabilidad es condicional**:

$$P(A|I)$$

Donde $I$ representa la información de fondo.

**No existe** $P(A)$ sin contexto. Cuando escribimos $P(A)$, hay información implícita.

### Ejemplo

"$P(\text{lluvia}) = 0.3$" realmente significa:

$$P(\text{lluvia}|\text{fecha, ubicación, conocimiento meteorológico, ...})$$

Esto resuelve paradojas donde diferentes personas asignan diferentes probabilidades al "mismo" evento — tienen diferente información $I$.

---

## Probabilidad Conjunta

La **probabilidad conjunta** $P(A, B)$ o $P(A \cap B)$ es la probabilidad de que ambos eventos ocurran.

### Tabla de Probabilidad Conjunta

Para dos variables discretas $X$ e $Y$:

|  | $Y=y_1$ | $Y=y_2$ | $Y=y_3$ |
|--|---------|---------|---------|
| $X=x_1$ | $P(x_1, y_1)$ | $P(x_1, y_2)$ | $P(x_1, y_3)$ |
| $X=x_2$ | $P(x_2, y_1)$ | $P(x_2, y_2)$ | $P(x_2, y_3)$ |

La suma de todas las celdas es 1.

---

## Probabilidad Marginal

La **probabilidad marginal** se obtiene "sumando" sobre las otras variables.

### Definición (Caso Discreto)

$$P(X = x) = \sum_y P(X = x, Y = y)$$

### Definición (Caso Continuo)

$$f_X(x) = \int_{-\infty}^{\infty} f_{X,Y}(x, y) \, dy$$

### El Nombre "Marginal"

Viene de las tablas de probabilidad: si sumas las filas, obtienes los totales en el **margen**.

|  | $Y=y_1$ | $Y=y_2$ | **Marginal X** |
|--|---------|---------|----------------|
| $X=x_1$ | 0.2 | 0.3 | **0.5** |
| $X=x_2$ | 0.1 | 0.4 | **0.5** |
| **Marginal Y** | **0.3** | **0.7** | 1.0 |

---

## Marginalización: La Regla de la Suma Extendida

La **marginalización** es una herramienta fundamental:

$$P(A) = \sum_i P(A, B_i) = \sum_i P(A|B_i) P(B_i)$$

Donde $\{B_i\}$ es una partición del espacio muestral.

### Ejemplo: Probabilidad Total

Una urna contiene:
- Caja 1: 3 bolas rojas, 2 azules
- Caja 2: 1 bola roja, 4 azules

Eliges una caja al azar (50/50) y luego una bola. ¿Probabilidad de roja?

$$P(\text{roja}) = P(\text{roja}|\text{Caja 1})P(\text{Caja 1}) + P(\text{roja}|\text{Caja 2})P(\text{Caja 2})$$

$$= \frac{3}{5} \cdot \frac{1}{2} + \frac{1}{5} \cdot \frac{1}{2} = \frac{3}{10} + \frac{1}{10} = \frac{4}{10} = 0.4$$

---

## Independencia

Dos eventos son **independientes** si conocer uno no cambia la probabilidad del otro:

$$P(A|B) = P(A)$$

### Equivalencias

Las siguientes son equivalentes:
1. $P(A|B) = P(A)$
2. $P(B|A) = P(B)$
3. $P(A \cap B) = P(A) \cdot P(B)$

### Ejemplo

Lanzar dos monedas:
- $A$ = "primera moneda es cara"
- $B$ = "segunda moneda es cara"

$P(A \cap B) = \frac{1}{4} = \frac{1}{2} \cdot \frac{1}{2} = P(A) \cdot P(B)$

Son independientes — el resultado de una no afecta a la otra.

### Independencia ≠ Disjuntos

**Cuidado:** Independencia y eventos disjuntos son cosas diferentes:
- Disjuntos: $A \cap B = \emptyset$ (no pueden ocurrir juntos)
- Independientes: $P(A \cap B) = P(A)P(B)$ (información de uno no afecta al otro)

Si $A$ y $B$ son disjuntos con probabilidades positivas, son **dependientes** (saber que $A$ ocurrió implica que $B$ no ocurrió).

---

## Independencia Condicional

$A$ y $B$ son **condicionalmente independientes** dado $C$ si:

$$P(A|B, C) = P(A|C)$$

O equivalentemente:
$$P(A, B|C) = P(A|C) \cdot P(B|C)$$

### Importancia

La independencia condicional es más útil que la independencia simple:
- En el mundo real, pocas cosas son absolutamente independientes
- Pero muchas son independientes **dado cierto contexto**

### Ejemplo

- $A$ = "persona tiene tos"
- $B$ = "persona tiene fiebre"

$A$ y $B$ no son independientes (ambos sugieren enfermedad).

Pero dado $C$ = "persona tiene gripe":
- $P(\text{tos}|\text{fiebre, gripe}) \approx P(\text{tos}|\text{gripe})$

Una vez que sabemos que tiene gripe, saber que tiene fiebre no cambia mucho nuestra expectativa de tos.

---

## Relación entre Condicional, Conjunta y Marginal

Las tres están relacionadas:

```
         P(A,B)
        /      \
       /        \
   P(A|B)      P(B)
      
P(A,B) = P(A|B) · P(B) = P(B|A) · P(A)

P(A) = Σ_b P(A,B=b)  [marginalización]
```

### Tabla Resumen

| Tipo | Notación | Cómo obtenerla |
|------|----------|----------------|
| Conjunta | $P(A,B)$ | Modelo directo |
| Condicional | $P(A\|B)$ | $P(A,B)/P(B)$ |
| Marginal | $P(A)$ | $\sum_B P(A,B)$ |

---

## Ejemplo Completo: Diagnóstico Médico

**Situación:**
- Enfermedad D afecta al 1% de la población
- Test T: 90% de sensibilidad (positivo si enfermo)
- Test T: 95% de especificidad (negativo si sano)

**Probabilidades:**
- $P(D) = 0.01$
- $P(T^+|D) = 0.90$
- $P(T^-|\neg D) = 0.95$

**Pregunta:** Si el test es positivo, ¿probabilidad de tener la enfermedad?

**Paso 1:** Calcular la probabilidad conjunta
- $P(T^+, D) = P(T^+|D) \cdot P(D) = 0.90 \times 0.01 = 0.009$
- $P(T^+, \neg D) = P(T^+|\neg D) \cdot P(\neg D) = 0.05 \times 0.99 = 0.0495$

**Paso 2:** Marginalizar para obtener $P(T^+)$
- $P(T^+) = P(T^+, D) + P(T^+, \neg D) = 0.009 + 0.0495 = 0.0585$

**Paso 3:** Calcular condicional
- $P(D|T^+) = \frac{P(T^+, D)}{P(T^+)} = \frac{0.009}{0.0585} \approx 0.154$

**Resultado:** Solo ~15% de probabilidad de estar enfermo con test positivo.

Esto es contraintuitivo pero correcto — la enfermedad es rara.

---

## Resumen

| Concepto | Definición | Uso |
|----------|------------|-----|
| **Condicional** | $P(A\|B) = P(AB)/P(B)$ | Actualizar con información |
| **Conjunta** | $P(A,B)$ | Probabilidad de ambos |
| **Marginal** | $\sum_B P(A,B)$ | "Sumar" sobre variables |
| **Independencia** | $P(A\|B) = P(A)$ | Simplificar modelos |
| **Ind. Condicional** | $P(A\|B,C) = P(A\|C)$ | Modelos gráficos |

---

**Siguiente:** [Las Reglas de Probabilidad →](07_reglas_probabilidad.md)
