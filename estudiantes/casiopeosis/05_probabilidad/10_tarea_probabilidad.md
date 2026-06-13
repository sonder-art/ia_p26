# Tarea: Ejercicios de Probabilidad

Esta tarea tiene como objetivo verificar y reforzar tu comprensión de los conceptos fundamentales de probabilidad que hemos visto en este módulo.

## Instrucciones

- **Fecha de entrega:** 4 de febrero de 2026
- **Puntos:** 20
- **Plataforma:** Canvas

### Formato de Entrega

Puedes entregar de cualquiera de estas formas, pero **todo debe estar en UN SOLO archivo ordenado**:

1. **PDF con fotos ordenadas** — Toma fotos de tu trabajo a mano y compílalas en un solo PDF ordenado (no fotos sueltas dispersas)
2. **Documento LaTeX/PDF** — Escribe las respuestas directamente en LaTeX
3. **Este archivo completado** — Puedes descargar este markdown, escribir tus respuestas en los espacios indicados, y subirlo como PDF
4. **Código + explicaciones** — Si prefieres código (Python/etc.), incluye las explicaciones y que esté todo en un documento ordenado

**IMPORTANTE:** No envíes archivos dispersos o fotos sin orden. Todo debe estar en **un solo documento** con las respuestas claramente identificadas por número de ejercicio.

### Sobre el Uso de IA

> **Esta tarea es un ejercicio para tu cerebro, no para el LLM.**

La recomendación es hacer los ejercicios **a mano con papel y lápiz**. Esto te ayuda a practicar y a internalizar los conceptos.

- **SÍ usa IA para:** Aprender, aclarar dudas, entender conceptos que no te quedan claros
- **NO uses IA para:** Que te resuelva los ejercicios directamente

El objetivo es evaluar **cómo estás tú** en probabilidad. Si el LLM hace la tarea, no sabrás dónde están tus áreas de oportunidad. Piensa los ejercicios tú mismo — es la única forma de realmente aprender.

---

## Parte I: Conceptos y Filosofía (6 puntos)

Responde brevemente las siguientes preguntas conceptuales.

### Ejercicio 1.1 (1 punto)
¿Cuáles son los tres **desiderata** que Jaynes establece para un sistema de razonamiento plausible? Descríbelos brevemente.

**Respuesta:**

1. Posibilidad de comparación al usar números reales y asignarlos a la plausibilidad de eventos.
2. Uso del 'sentido común' a la hora de razonar. Si hay una dependencia, el cambio en alguna de sus partes también debe de influir a la otra (A->B)
3. Consistencia en 3 aspectos: a) estructural: si una conclusión es posible via diversas maneras, entonces todos deben de llegar al la misma conclusión; b) consistencia: aunque 2 problemas sean representados de la misma manera, ellos deben tener el mismo resultado; c) lógica: no se puede 'excluir' o ignorar información relevante al problema bajo ninguna circunstancia.

---

### Ejercicio 1.2 (1 punto)
Explica la diferencia entre las interpretaciones **frecuentista**, **bayesiana subjetiva**, y la de **Jaynes/Cox** de la probabilidad. ¿Cuál es la ventaja del enfoque de Jaynes?

**Respuesta:**

a) Frecuentista: la probabilidad es el resultado observado tras la realización de infinitas repeticiones de un experimento
b) Bayesiana: relacionado con los grados de confianza que se tienen con respecto a la ocurrencia de un evento.
c) Jaynes-Cox: la probabilidad es una herramienta de inferencia, deriva las reglas de probabilidad desde primeros principios y permite asignar valores numéricos a probabilidades, que éstos sean consistentes esntre sí y que respondan a nueva información.

---

### Ejercicio 1.3 (1 punto)
¿Por qué decimos que la probabilidad es una "extensión de la lógica"? ¿Qué pasa con las reglas de probabilidad cuando $P(A) = 0$ o $P(A) = 1$?

**Respuesta:**

Porque ofrece un rango de respuestas infinitamente más valioso que un sí o no (1,0). 
    P(A) = 1, es una obviedad.
    P(B) = 0, se contradice.

---

### Ejercicio 1.4 (1 punto)
En el enfoque de Jaynes, se dice que "toda probabilidad es condicional". ¿Qué significa esto? ¿Por qué escribimos $P(A|I)$ en lugar de simplemente $P(A)$?

**Respuesta:**

Porque P(A|I) representa de forma fiel que las probabilidades siempre dependen de la información a nuestra disposición (conocimiento previo, supuestos, etc.) mientras que P(A) ls excluye (aquí tengo mis objeciones porque por algo se tienen parámetros).

---

### Ejercicio 1.5 (1 punto)
En el Teorema de Bayes $P(H|D,I) = \frac{P(D|H,I) \cdot P(H|I)}{P(D|I)}$, identifica y explica qué representa cada término:
- $P(H|D,I)$ =
- $P(D|H,I)$ = 
- $P(H|I)$ = 
- $P(D|I)$ = 

**Respuesta:**

- $P(H|D,I)$ = probabilidad de ocurrencia de la hipótesis, dados (considerando) los datos que se tienen y la información previa 
- $P(D|H,I)$ = probabilidad de que los datos sean ciertos, dada que la hipótesis también es cierta (y considerando la info. previa)
- $P(H|I)$ = probabilidad de que la hipótesis sea cierta considerando la información previa (sin ver los datos)
- $P(D|I)$ = probabilidad de que los datos sean ciertos considerando la información previa

---

### Ejercicio 1.6 (1 punto)
¿Por qué las reglas de probabilidad (producto y suma) no son arbitrarias según Jaynes? ¿De dónde se derivan?

**Respuesta:**

No son arbitrarias porque son consecuencias de la consistencia, surgen por los axiomas de Cox
Producto: desiderata 2 (relación entre transitividad y plausibilidad) y 3 (consistencia)
Adición: derivada por el desiderata 3 y 2 por la relación P(A|C) y P(~A|C) al P(~A|C) + P(A|C) = 1

---

## Parte II: Probabilidad Básica (10 puntos)

Resuelve los siguientes ejercicios mostrando tu procedimiento.

### Ejercicio 2.1 (1 punto)
Se lanza un dado justo de 6 caras. Sea $A$ = "sale número par" y $B$ = "sale número mayor que 3".

a) Calcula $P(A)$, $P(B)$, y $P(A \cap B)$.

b) ¿Son $A$ y $B$ independientes? Justifica tu respuesta.
    
**Respuesta:**
    a.1) P(A) = 3 {2,4,6} / 6 {1,2,3,4,5,6}
    a.2) P(B) = 3 {4,5,6} / 6 {1,2,3,4,5,6}
    a.3) P(A y B) = 2 {4,6} / 6 {1,2,3,4,5,6}

    b)No, por definición de independencia a pares P(A y B) debería de ser igual que P(A) * P(B)
    pero 1/3 != (1/4)

---

### Ejercicio 2.2 (1.5 puntos)
Una urna contiene 4 bolas rojas y 6 bolas azules. Se extraen 2 bolas **sin reemplazo**.

a) ¿Cuál es la probabilidad de que ambas sean rojas?

b) ¿Cuál es la probabilidad de que la segunda sea roja, dado que la primera fue azul?

**Respuesta:**

    a) por probabilidad condicional P(R1 y R2) = P(R2|R1) * P(R1)
    P(R1) = 4/10 y P(R2|R1)=3/9 entonces P(R1 y R2) = 2 / 15

    b) quedan 4 bolas rojas en la urna con 10-1=9 bolas entonces la P(R2|A1) = 4/9

---

### Ejercicio 2.3 (2 puntos)


Usando Bayes: $P(E|+) = \frac{P(+|E) \cdot P(E)}{P(+)}$

Primero calculamos $P(+)$ usando la regla de probabilidad total:
$P(+) = P(+|E) \cdot P(E) + P(+|S) \cdot P(S)$
$P(+) = 0.95 \times 0.02 + 0.10 \times 0.98 = 0.019 + 0.098 = 0.117$

Entonces:
$P(E|+) = \frac{0.95 \times 0.02}{0.117} = \frac{0.019}{0.117} \approx 0.162$

Solo hay ~16.2% de probabilidad de estar enfermo dado un resultado positivo.

---

### Ejercicio 2.4 (1.5 puntos)

**Respuesta:**

a) Distribución de X:

| X | P(X) | Resultados |
|---|------|------------|
| 0 | 1/4  | {CC}       |
| 1 | 2/4  | {C+, +C}   |
| 2 | 1/4  | {++}       |

b) $E[X] = 0 \times \frac{1}{4} + 1 \times \frac{2}{4} + 2 \times \frac{1}{4} = 0 + \frac{2}{4} + \frac{2}{4} = 1$

c) $E[X^2] = 0^2 \times \frac{1}{4} + 1^2 \times \frac{2}{4} + 2^2 \times \frac{1}{4} = 0 + \frac{2}{4} + \frac{4}{4} = \frac{6}{4} = 1.5$

$\text{Var}(X) = E[X^2] - (E[X])^2 = 1.5 - 1 = 0.5$

---

### Ejercicio 2.5 (1.5 puntos)

**Respuesta:**

a) $P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{0.2}{0.5} = 0.4$

b) $P(A \cup B) = P(A) + P(B) - P(A \cap B) = 0.4 + 0.5 - 0.2 = 0.7$

c) Sí son independientes, porque $P(A \cap B) = 0.2 = P(A) \times P(B) = 0.4 \times 0.5 = 0.2$ ✓

---

### Ejercicio 2.6 (1.5 puntos)

**Respuesta:**

a) $E[3X + 2] = 3E[X] + 2 = 3(5) + 2 = 17$

b) $\text{Var}(3X + 2) = 3^2 \text{Var}(X) = 9(4) = 36$
   (la constante no afecta la varianza)

c) $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) = 4 + 9 = 13$
   (por independencia, la covarianza es cero)

---

### Ejercicio 2.7 (1 punto)


Partimos de $\text{Var}(X) = E[(X - \mu)^2]$ donde $\mu = E[X]$

$\text{Var}(X) = E[(X - \mu)^2]$

$= E[X^2 - 2\mu X + \mu^2]$

$= E[X^2] - E[2\mu X] + E[\mu^2]$ (linealidad del valor esperado)

$= E[X^2] - 2\mu E[X] + \mu^2$

$= E[X^2] - 2\mu \cdot \mu + \mu^2$ (porque $E[X] = \mu$)

$= E[X^2] - 2\mu^2 + \mu^2$

$= E[X^2] - \mu^2$

$= E[X^2] - (E[X])^2$ ∎

---

## Parte III: Álgebra Booleana (4 puntos)

### Ejercicio 3.1 (1 punto)

**Respuesta:**

a) $A + AB = A(1 + B) = A \cdot 1 = A$
   (por distributividad y porque $1 + B = 1$ en álgebra booleana)

b) $A(A + B) = AA + AB = A + AB = A$
   (por distributividad, idempotencia, y resultado anterior)

c) $A + \bar{A}B = (A + \bar{A})(A + B) = 1 \cdot (A + B) = A + B$
   (por distributividad y complemento)

---

### Ejercicio 3.2 (1.5 puntos)

**Respuesta:**

a) $\overline{A + B + C}$

Aplicamos De Morgan:al´po{jefg}
$\overline{A + B + C} = \overline{(A + B) + C}$
$= \overline{(A + B)} \cdot \bar{C}$ (primera aplicación de De Morgan)
$= (\bar{A} \cdot \bar{B}) \cdot \bar{C}$ (segunda aplicación de De Morgan)
$= \bar{A}\bar{B}\bar{C}$ ✓

b) $\overline{ABC}$

Aplicamos De Morgan:
$\overline{ABC} = \overline{(AB) \cdot C}$
$= \overline{AB} + \bar{C}$ (primera aplicación de De Morgan)
$= (\bar{A} + \bar{B}) + \bar{C}$ (segunda aplicación de De Morgan)
$= \bar{A} + \bar{B} + \bar{C}$ ✓

---

### Ejercicio 3.3 (1.5 puntos)

**Respuesta:**

a) $P(A \cup B)$ → notación booleana = $P(A + B)$

b) $P(A \cap B^c)$ → notación booleana = $P(A\bar{B})$

c) $P(\bar{A} + B)$ → notación de conjuntos = $P(\bar{A} \cup B)$ o $P(A^c \cup B)$

d) $P(A\bar{B})$ → notación de conjuntos = $P(A \cap B^c)$ o $P(A \cap \bar{B})$

## Resumen de Puntos

| Parte | Tema | Puntos |
|-------|------|--------|
| I | Conceptos y Filosofía | 6 |
| II | Probabilidad Básica | 10 |
| III | Álgebra Booleana | 4 |
| **Total** | | **20** |

---

## Checklist de Entrega

Antes de enviar, verifica:

- [ ] Todas las respuestas están claramente identificadas por número de ejercicio
- [ ] Todo está en **UN SOLO archivo/documento ordenado**
- [ ] El trabajo es legible (si son fotos, que se vean bien)
- [ ] Mostraste el procedimiento, no solo respuestas finales

---

**Fecha límite:** 4 de febrero de 2026

**Recuerda:** Esta tarea es para TI. El objetivo es que practiques y descubras dónde necesitas reforzar. Si tienes dudas, consulta las notas del módulo o las lecturas de Jaynes — pero intenta resolver los ejercicios con tu propio razonamiento primero.

¡Éxito!
