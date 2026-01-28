:::homework{id="5.10" title="Ejercicios de Probabilidad" due="2026-02-04" points="20"}

Ejercicios para reforzar conceptos de probabilidad, filosofía y álgebra booleana.

:::

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

<br><br><br><br><br><br>

---

### Ejercicio 1.2 (1 punto)
Explica la diferencia entre las interpretaciones **frecuentista**, **bayesiana subjetiva**, y la de **Jaynes/Cox** de la probabilidad. ¿Cuál es la ventaja del enfoque de Jaynes?

**Respuesta:**

<br><br><br><br><br><br><br><br>

---

### Ejercicio 1.3 (1 punto)
¿Por qué decimos que la probabilidad es una "extensión de la lógica"? ¿Qué pasa con las reglas de probabilidad cuando $P(A) = 0$ o $P(A) = 1$?

**Respuesta:**

<br><br><br><br><br><br>

---

### Ejercicio 1.4 (1 punto)
En el enfoque de Jaynes, se dice que "toda probabilidad es condicional". ¿Qué significa esto? ¿Por qué escribimos $P(A|I)$ en lugar de simplemente $P(A)$?

**Respuesta:**

<br><br><br><br><br><br>

---

### Ejercicio 1.5 (1 punto)
En el Teorema de Bayes $P(H|D,I) = \frac{P(D|H,I) \cdot P(H|I)}{P(D|I)}$, identifica y explica qué representa cada término:
- $P(H|D,I)$ =
- $P(D|H,I)$ =
- $P(H|I)$ =
- $P(D|I)$ =

**Respuesta:**

<br><br><br><br><br><br><br><br>

---

### Ejercicio 1.6 (1 punto)
¿Por qué las reglas de probabilidad (producto y suma) no son arbitrarias según Jaynes? ¿De dónde se derivan?

**Respuesta:**

<br><br><br><br><br><br>

---

## Parte II: Probabilidad Básica (10 puntos)

Resuelve los siguientes ejercicios mostrando tu procedimiento.

### Ejercicio 2.1 (1 punto)
Se lanza un dado justo de 6 caras. Sea $A$ = "sale número par" y $B$ = "sale número mayor que 3".

a) Calcula $P(A)$, $P(B)$, y $P(A \cap B)$.

b) ¿Son $A$ y $B$ independientes? Justifica tu respuesta.

**Respuesta:**

<br><br><br><br><br><br><br><br>

---

### Ejercicio 2.2 (1.5 puntos)
Una urna contiene 4 bolas rojas y 6 bolas azules. Se extraen 2 bolas **sin reemplazo**.

a) ¿Cuál es la probabilidad de que ambas sean rojas?

b) ¿Cuál es la probabilidad de que la segunda sea roja, dado que la primera fue azul?

**Respuesta:**

<br><br><br><br><br><br><br><br>

---

### Ejercicio 2.3 (2 puntos)
En una población, el 2% tiene cierta enfermedad. Un test de diagnóstico tiene:
- Sensibilidad: $P(\text{positivo}|\text{enfermo}) = 0.95$
- Especificidad: $P(\text{negativo}|\text{sano}) = 0.90$

Si una persona obtiene un resultado **positivo**, ¿cuál es la probabilidad de que realmente tenga la enfermedad? Usa el Teorema de Bayes.

**Respuesta:**

<br><br><br><br><br><br><br><br><br><br>

---

### Ejercicio 2.4 (1.5 puntos)
Se lanzan dos monedas justas. Sea $X$ = "número de caras obtenidas".

a) Escribe la distribución de probabilidad de $X$ (tabla con valores y probabilidades).

b) Calcula $E[X]$ (valor esperado).

c) Calcula $\text{Var}(X)$ (varianza).

**Respuesta:**

<br><br><br><br><br><br><br><br><br><br>

---

### Ejercicio 2.5 (1.5 puntos)
Si $P(A) = 0.4$, $P(B) = 0.5$, y $P(A \cap B) = 0.2$:

a) Calcula $P(A|B)$.

b) Calcula $P(A \cup B)$.

c) ¿Son $A$ y $B$ independientes?

**Respuesta:**

<br><br><br><br><br><br><br><br>

---

### Ejercicio 2.6 (1.5 puntos)
Sea $X$ una variable aleatoria con $E[X] = 5$ y $\text{Var}(X) = 4$.

a) Calcula $E[3X + 2]$.

b) Calcula $\text{Var}(3X + 2)$.

c) Si $Y$ es independiente de $X$ con $\text{Var}(Y) = 9$, calcula $\text{Var}(X + Y)$.

**Respuesta:**

<br><br><br><br><br><br><br><br>

---

### Ejercicio 2.7 (1 punto)
Demuestra que $\text{Var}(X) = E[X^2] - (E[X])^2$ partiendo de la definición $\text{Var}(X) = E[(X - \mu)^2]$.

**Respuesta:**

<br><br><br><br><br><br><br><br><br><br>

---

## Parte III: Álgebra Booleana (4 puntos)

### Introducción Breve

El **álgebra booleana** es el sistema formal que subyace a la lógica proposicional y que Jaynes utiliza como base para desarrollar la teoría de probabilidad.

**Notación:**
- $A + B$ significa "$A$ O $B$" (disyunción, OR)
- $AB$ o $A \cdot B$ significa "$A$ Y $B$" (conjunción, AND)
- $\bar{A}$ significa "NO $A$" (negación, NOT)

**Dato importante:** Las operaciones del álgebra booleana forman una **teoría completa** — cualquier proposición lógica puede expresarse usando solo estas tres operaciones. Esto es fundamental porque las reglas de probabilidad se construyen sobre esta base.

**Conexión con probabilidad:**
- $P(A + B)$ = probabilidad de $A$ o $B$
- $P(AB)$ = probabilidad de $A$ y $B$
- $P(\bar{A})$ = probabilidad de no $A$

**Leyes importantes:**
- Conmutatividad: $A + B = B + A$, $AB = BA$
- Asociatividad: $(A + B) + C = A + (B + C)$
- Distributividad: $A(B + C) = AB + AC$
- De Morgan: $\overline{A + B} = \bar{A}\bar{B}$, $\overline{AB} = \bar{A} + \bar{B}$
- Complemento: $A + \bar{A} = 1$, $A\bar{A} = 0$
- Idempotencia: $A + A = A$, $AA = A$

**Referencia:** Jaynes, "Probability Theory: The Logic of Science", Capítulo 1 (páginas 13-29 en nuestro PDF de lecturas).

---

### Ejercicio 3.1 (1 punto)
Simplifica las siguientes expresiones booleanas:

a) $A + AB$ =

b) $A(A + B)$ =

c) $A + \bar{A}B$ =

**Respuesta (muestra los pasos):**

<br><br><br><br><br><br><br><br>

---

### Ejercicio 3.2 (1.5 puntos)
Usando las leyes de De Morgan, demuestra que:

a) $\overline{A + B + C} = \bar{A}\bar{B}\bar{C}$

b) $\overline{ABC} = \bar{A} + \bar{B} + \bar{C}$

**Respuesta:**

<br><br><br><br><br><br><br><br>

---

### Ejercicio 3.3 (1.5 puntos)
Convierte las siguientes expresiones de notación de conjuntos a notación de álgebra booleana, y viceversa:

a) $P(A \cup B)$ → notación booleana =

b) $P(A \cap B^c)$ → notación booleana =

c) $P(\bar{A} + B)$ → notación de conjuntos =

d) $P(A\bar{B})$ → notación de conjuntos =

**Respuesta:**

<br><br><br><br><br><br>

---

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
