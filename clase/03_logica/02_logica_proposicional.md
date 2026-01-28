---
title: "Lógica Proposicional"
---

# Lógica Proposicional

El lenguaje más simple para representar conocimiento formal.

## Introducción: ¿Qué Vamos a Aprender?

En esta sección aprenderemos el **lenguaje** que usaremos para representar conocimiento. Así como el español tiene gramática y significado, la lógica proposicional tiene:

- **Sintaxis**: Las reglas que dicen qué expresiones están "bien escritas"
- **Semántica**: El significado de esas expresiones (cuándo son verdaderas o falsas)

Al final de esta sección podrás:
- Escribir afirmaciones en lógica proposicional
- Determinar si una fórmula es verdadera o falsa
- Convertir fórmulas a formas estándar (CNF)

---

## ¿Qué es una Proposición?

Antes de hablar de lógica, necesitamos entender qué es una **proposición**.

Una **proposición** es una oración declarativa que puede ser **verdadera** o **falsa**, pero no ambas al mismo tiempo. Este es el bloque fundamental de la lógica proposicional.

### Ejemplos de Proposiciones

| Oración | ¿Es proposición? | ¿Por qué? |
|---------|:----------------:|-----------|
| "Está lloviendo" | ✓ Sí | Puede ser verdadera o falsa dependiendo del clima |
| "2 + 2 = 4" | ✓ Sí | Es verdadera (siempre) |
| "La luna es de queso" | ✓ Sí | Es falsa, pero sigue siendo una proposición |
| "¿Qué hora es?" | ✗ No | Es una pregunta, no una declaración |
| "¡Cierra la puerta!" | ✗ No | Es una orden, no se puede evaluar como V o F |
| "Esta oración es falsa" | ✗ No | Es una paradoja (no puede ser ni V ni F) |
| "x > 5" | ✗ No | Depende del valor de x — no es determinable |

La última fila es importante: en lógica **proposicional** no hay variables como "x". Cada proposición debe ser evaluable como verdadera o falsa sin información adicional. (Las variables aparecen en lógica de primer orden, que es más avanzada.)

---

## La Sintaxis: Construyendo Fórmulas

La **sintaxis** son las reglas gramaticales de nuestro lenguaje lógico. Define qué combinaciones de símbolos son expresiones válidas.

### Los Bloques Básicos: Símbolos Proposicionales

Usamos letras mayúsculas para representar proposiciones:

| Símbolo | Lo que representa |
|---------|-------------------|
| $P$, $Q$, $R$, $S$, ... | Proposiciones que elegimos (les damos significado nosotros) |
| $True$ (o $\top$) | Una proposición que siempre es verdadera |
| $False$ (o $\bot$) | Una proposición que siempre es falsa |

**Ejemplo de asignación de significado:**
- $P$ = "Está lloviendo"
- $Q$ = "Tengo un paraguas"
- $R$ = "Me voy a mojar"

Los símbolos solos no significan nada — nosotros les damos significado al modelar un problema.

### Los Conectivos Lógicos: Combinando Proposiciones

Los **conectivos** nos permiten construir proposiciones complejas a partir de proposiciones simples. Son como las conjunciones del español ("y", "o", "si...entonces").

| Conectivo | Símbolo | Nombre Técnico | Se lee como... | Ejemplo |
|-----------|:-------:|----------------|----------------|---------|
| **NO** | $\neg$ | Negación | "no P", "es falso que P" | $\neg P$ = "No está lloviendo" |
| **Y** | $\land$ | Conjunción | "P y Q" | $P \land Q$ = "Llueve y tengo paraguas" |
| **O** | $\lor$ | Disyunción | "P o Q (o ambos)" | $P \lor Q$ = "Llueve o tengo paraguas" |
| **SI...ENTONCES** | $\rightarrow$ | Implicación | "si P entonces Q" | $P \rightarrow R$ = "Si llueve, me mojo" |
| **SI Y SOLO SI** | $\leftrightarrow$ | Bicondicional | "P si y solo si Q" | $P \leftrightarrow Q$ = "Llueve exactamente cuando tengo paraguas" |

### Construyendo Fórmulas Complejas

Podemos combinar conectivos para hacer fórmulas más complejas:

**Ejemplo:** "Si llueve y no tengo paraguas, entonces me mojo"

Paso a paso:
1. $P$ = "Llueve"
2. $Q$ = "Tengo paraguas"  
3. $R$ = "Me mojo"
4. "No tengo paraguas" = $\neg Q$
5. "Llueve y no tengo paraguas" = $P \land \neg Q$
6. Fórmula completa: $(P \land \neg Q) \rightarrow R$

### Precedencia de Operadores (Orden de Evaluación)

Cuando escribimos $\neg P \land Q$, ¿qué se evalúa primero?

Al igual que en matemáticas donde $2 + 3 \times 4 = 14$ (no 20) porque la multiplicación tiene precedencia, en lógica hay un orden:

| Prioridad | Operador | Ejemplo |
|:---------:|:--------:|---------|
| 1 (más alta) | $\neg$ | $\neg P \land Q$ significa $(\neg P) \land Q$ |
| 2 | $\land$ | $P \land Q \lor R$ significa $(P \land Q) \lor R$ |
| 3 | $\lor$ | |
| 4 | $\rightarrow$ | |
| 5 (más baja) | $\leftrightarrow$ | |

**Consejo:** Cuando hay duda, usa paréntesis para ser explícito. Es mejor escribir $(P \land Q) \rightarrow R$ que confiar en la precedencia.

---

## La Semántica: El Significado de las Fórmulas

La **semántica** nos dice cuándo una fórmula es verdadera y cuándo es falsa. Para esto necesitamos el concepto de **modelo**.

### ¿Qué es un Modelo?

Un **modelo** (también llamado **interpretación**) es una asignación de valores de verdad (True o False) a cada símbolo proposicional.

**Ejemplo:** Si tenemos los símbolos $P$, $Q$, $R$:

Un modelo posible es:
$$m_1 = \{P = True, Q = False, R = True\}$$

Esto significa: "En este modelo, P es verdadera, Q es falsa, y R es verdadera."

Otro modelo posible es:
$$m_2 = \{P = False, Q = False, R = False\}$$

### ¿Cuántos Modelos Hay?

Si tenemos $n$ símbolos proposicionales, cada uno puede ser True o False. Por lo tanto, hay $2^n$ modelos posibles.

| Símbolos | Modelos Posibles |
|:--------:|:----------------:|
| 1 ($P$) | $2^1 = 2$ |
| 2 ($P$, $Q$) | $2^2 = 4$ |
| 3 ($P$, $Q$, $R$) | $2^3 = 8$ |
| 10 | $2^{10} = 1024$ |
| 100 | $2^{100} \approx 10^{30}$ |

Este crecimiento exponencial es importante — veremos que tiene implicaciones computacionales serias.

### Tablas de Verdad: Definiendo el Significado de los Conectivos

Las **tablas de verdad** definen exactamente cuándo cada conectivo produce True o False.

#### Negación ($\neg$): "NO"

La negación invierte el valor de verdad:

| $P$ | $\neg P$ |
|:---:|:--------:|
| T | F |
| F | T |

**Intuición:** Si "está lloviendo" es verdadero, entonces "NO está lloviendo" es falso, y viceversa.

#### Conjunción ($\land$): "Y"

La conjunción es verdadera solo cuando **ambas** partes son verdaderas:

| $P$ | $Q$ | $P \land Q$ |
|:---:|:---:|:-----------:|
| T | T | **T** |
| T | F | F |
| F | T | F |
| F | F | F |

**Intuición:** "Tengo hambre Y tengo dinero" solo es verdadero si ambas cosas son ciertas. Si cualquiera es falsa, todo es falso.

#### Disyunción ($\lor$): "O" (inclusivo)

La disyunción es verdadera cuando **al menos una** parte es verdadera:

| $P$ | $Q$ | $P \lor Q$ |
|:---:|:---:|:---------:|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | **F** |

**Importante:** Este es el "o" **inclusivo** — "P o Q o ambos". Es diferente del "o" exclusivo del español ("¿quieres café o té?" usualmente implica que solo puedes elegir uno).

**Intuición:** "Apruebo si estudio O si tengo suerte" — apruebo si hago una cosa, la otra, o ambas.

#### Implicación ($\rightarrow$): "SI...ENTONCES"

Esta es la más confusa para muchos estudiantes:

| $P$ | $Q$ | $P \rightarrow Q$ |
|:---:|:---:|:-----------------:|
| T | T | T |
| T | F | **F** |
| F | T | T |
| F | F | T |

**¿Por qué la implicación es True cuando P es False?**

Esta es la pregunta más común. Pensemos en una promesa:

*"Si sacas 10 en el examen, te compro un carro."*

- Si sacas 10 y te compro el carro → Cumplí mi promesa ✓
- Si sacas 10 y NO te compro el carro → Rompí mi promesa ✗
- Si NO sacas 10... → No puedes acusarme de mentir ✓

Cuando la condición (el antecedente) no se cumple, la promesa no se rompe. Esto se llama **verdad por vacuidad**.

:::example{title="Implicaciones Vacuamente Verdaderas"}

Considera: "Si los cerdos vuelan, entonces 2+2=5"

- $P$ = "Los cerdos vuelan" = **False**
- $Q$ = "2+2=5" = **False**

$P \rightarrow Q$ = **True**

Esto parece raro, pero tiene sentido: como los cerdos NO vuelan, la condición nunca se activa, así que no podemos decir que la implicación sea falsa.

**Otro ejemplo:** "Todos los unicornios son morados" es técnicamente verdadero porque no hay unicornios que puedan contradecirlo.

:::

#### Bicondicional ($\leftrightarrow$): "SI Y SOLO SI"

El bicondicional es verdadero cuando ambos lados tienen el **mismo** valor:

| $P$ | $Q$ | $P \leftrightarrow Q$ |
|:---:|:---:|:---------------------:|
| T | T | **T** |
| T | F | F |
| F | T | F |
| F | F | **T** |

**Intuición:** "Apruebas si y solo si estudias" significa que aprobar y estudiar siempre van juntos — si haces uno, haces el otro; si no haces uno, no haces el otro.

---

## Evaluando Fórmulas Complejas

Para evaluar una fórmula en un modelo específico, aplicamos las tablas de verdad paso a paso, de adentro hacia afuera.

:::example{title="Evaluación Paso a Paso"}

**Fórmula:** $(P \land Q) \rightarrow \neg R$

**Modelo:** $m = \{P = T, Q = T, R = F\}$

**Evaluación:**

1. Sustituir valores: $(T \land T) \rightarrow \neg F$
2. Evaluar $\neg F$: $(T \land T) \rightarrow T$
3. Evaluar $T \land T$: $T \rightarrow T$
4. Evaluar $T \rightarrow T$: $T$

**Resultado:** La fórmula es **verdadera** en este modelo.

:::

### Construyendo Tablas de Verdad Completas

Para analizar una fórmula completamente, construimos una tabla con **todos** los modelos posibles.

**Fórmula:** $P \rightarrow (P \lor Q)$

| $P$ | $Q$ | $P \lor Q$ | $P \rightarrow (P \lor Q)$ |
|:---:|:---:|:----------:|:--------------------------:|
| T | T | T | T |
| T | F | T | T |
| F | T | T | T |
| F | F | F | T |

**Observación:** La fórmula es **siempre verdadera** sin importar los valores de P y Q. A esto se le llama **tautología**.

---

## Equivalencias Lógicas

Dos fórmulas son **lógicamente equivalentes** (escritas como $\alpha \equiv \beta$) cuando tienen el **mismo valor de verdad en todos los modelos posibles**.

Esto significa que podemos sustituir una por otra sin cambiar el significado.

### Las Equivalencias Más Importantes

#### Leyes de De Morgan

Estas leyes nos dicen cómo "distribuir" una negación sobre AND y OR:

$$\neg (P \land Q) \equiv \neg P \lor \neg Q$$

**Intuición:** "NO es cierto que (llueve Y hace frío)" es lo mismo que "NO llueve O NO hace frío".

$$\neg (P \lor Q) \equiv \neg P \land \neg Q$$

**Intuición:** "NO es cierto que (llueve O hace frío)" es lo mismo que "NO llueve Y NO hace frío".

#### La Implicación como Disyunción

Esta equivalencia es **fundamental** y la usaremos constantemente:

$$P \rightarrow Q \equiv \neg P \lor Q$$

**Intuición:** "Si llueve, me mojo" es lo mismo que "NO llueve O me mojo". 

Piénsalo así: la única forma de que la implicación sea falsa es que llueva ($P$ verdadero) y no me moje ($Q$ falso). En cualquier otro caso, es verdadera.

#### La Contrapositiva

$$P \rightarrow Q \equiv \neg Q \rightarrow \neg P$$

**Intuición:** "Si llueve, la calle se moja" es equivalente a "Si la calle NO está mojada, NO llovió".

Esta equivalencia es muy útil en demostraciones. Si quieres probar $P \rightarrow Q$, puedes probar su contrapositiva en su lugar.

#### Otras Equivalencias Útiles

| Nombre | Equivalencia |
|--------|--------------|
| Doble negación | $\neg \neg P \equiv P$ |
| Conmutatividad | $P \land Q \equiv Q \land P$ y $P \lor Q \equiv Q \lor P$ |
| Asociatividad | $(P \land Q) \land R \equiv P \land (Q \land R)$ |
| Distributividad | $P \land (Q \lor R) \equiv (P \land Q) \lor (P \land R)$ |
| Distributividad | $P \lor (Q \land R) \equiv (P \lor Q) \land (P \lor R)$ |
| Bicondicional | $P \leftrightarrow Q \equiv (P \rightarrow Q) \land (Q \rightarrow P)$ |

---

## Formas Normales: Estandarizando Fórmulas

Cualquier fórmula proposicional se puede reescribir en formas estandarizadas llamadas **formas normales**. Estas son útiles porque simplifican los algoritmos que procesan fórmulas.

### Vocabulario Previo

Antes de definir las formas normales, necesitamos algunos términos:

**Literal:** Un símbolo proposicional o su negación.
- Literales positivos: $P$, $Q$, $R$
- Literales negativos: $\neg P$, $\neg Q$, $\neg R$

**Cláusula:** Una disyunción (OR) de literales.
- Ejemplo: $P \lor \neg Q \lor R$
- Esto se lee: "P, o no-Q, o R"

### Forma Normal Conjuntiva (CNF)

Una fórmula está en **CNF** (Conjunctive Normal Form) si es una **conjunción de cláusulas** — es decir, cláusulas conectadas con AND.

**Estructura:** (cláusula₁) $\land$ (cláusula₂) $\land$ ... $\land$ (cláusulaₙ)

**Ejemplo en CNF:**
$$(P \lor Q) \land (\neg P \lor R) \land (\neg Q \lor \neg R \lor S)$$

Esto se lee: "P o Q, Y, no-P o R, Y, no-Q o no-R o S"

**¿Por qué es importante CNF?**
- Los algoritmos de SAT (satisfacibilidad) trabajan con CNF
- El algoritmo de resolución requiere CNF
- Es una forma "universal" — toda fórmula se puede convertir a CNF

### Forma Normal Disyuntiva (DNF)

Una fórmula está en **DNF** si es una **disyunción de conjunciones** — es decir, grupos de ANDs conectados con OR.

**Estructura:** (conj₁) $\lor$ (conj₂) $\lor$ ... $\lor$ (conjₙ)

**Ejemplo en DNF:**
$$(P \land Q) \lor (\neg P \land R) \lor (Q \land \neg R \land S)$$

### Algoritmo para Convertir a CNF

Cualquier fórmula se puede convertir a CNF siguiendo estos pasos:

**Paso 1:** Eliminar bicondicionales ($\leftrightarrow$)
$$\alpha \leftrightarrow \beta \quad\Rightarrow\quad (\alpha \rightarrow \beta) \land (\beta \rightarrow \alpha)$$

**Paso 2:** Eliminar implicaciones ($\rightarrow$)
$$\alpha \rightarrow \beta \quad\Rightarrow\quad \neg \alpha \lor \beta$$

**Paso 3:** Mover negaciones hacia adentro (usando De Morgan)
- $\neg(\alpha \land \beta) \Rightarrow \neg\alpha \lor \neg\beta$
- $\neg(\alpha \lor \beta) \Rightarrow \neg\alpha \land \neg\beta$
- $\neg\neg\alpha \Rightarrow \alpha$

**Paso 4:** Distribuir OR sobre AND
$$\alpha \lor (\beta \land \gamma) \quad\Rightarrow\quad (\alpha \lor \beta) \land (\alpha \lor \gamma)$$

:::example{title="Conversión a CNF Completa"}

**Convertir:** $P \rightarrow (Q \land R)$

**Paso 1:** No hay bicondicionales — nada que hacer.

**Paso 2:** Eliminar la implicación
$$\neg P \lor (Q \land R)$$

**Paso 3:** Las negaciones ya están en los literales — nada que hacer.

**Paso 4:** Distribuir $\lor$ sobre $\land$
$$(\neg P \lor Q) \land (\neg P \lor R)$$

**Resultado:** Dos cláusulas: $(\neg P \lor Q)$ y $(\neg P \lor R)$

**Verificación:** La fórmula original dice "si P, entonces Q y R". Las cláusulas dicen "no-P o Q" y "no-P o R", que es equivalente a "si P entonces Q" y "si P entonces R".

:::

---

## Cláusulas de Horn: Un Caso Especial Importante

Las **cláusulas de Horn** son un tipo especial de cláusula que tiene propiedades computacionales muy favorables.

### Definición

Una **cláusula de Horn** es una cláusula con **a lo más un literal positivo**.

| Tipo | Literales Positivos | Ejemplo | Significado |
|------|:-------------------:|---------|-------------|
| **Hecho** | 1, ningún negativo | $P$ | "P es verdadero" |
| **Regla** | 1 positivo, algunos negativos | $\neg P \lor \neg Q \lor R$ | "Si P y Q, entonces R" |
| **Objetivo** | 0, todos negativos | $\neg P \lor \neg Q$ | "¿Es verdad P y Q?" |

### ¿Por qué son Importantes?

Las cláusulas de Horn se pueden escribir como **reglas de producción** naturales:

La cláusula $\neg A \lor \neg B \lor C$ es equivalente a:
$$(A \land B) \rightarrow C$$

Que se lee: "Si A y B son verdaderos, entonces C es verdadero."

**Ventaja computacional:** Mientras que determinar satisfacibilidad para fórmulas generales en CNF es un problema NP-completo (muy difícil), para cláusulas de Horn se puede resolver en **tiempo lineal** O(n). Esto hace que sean muy prácticas para sistemas basados en reglas.

---

## Ejercicios

:::exercise{title="Construir Tabla de Verdad" difficulty="1"}

Construye la tabla de verdad completa para: $(P \rightarrow Q) \land (Q \rightarrow P)$

Pista: Esta fórmula tiene un nombre especial — ¿cuál es?

:::

<details>
<summary><strong>Ver Solución</strong></summary>

| $P$ | $Q$ | $P \rightarrow Q$ | $Q \rightarrow P$ | $(P \rightarrow Q) \land (Q \rightarrow P)$ |
|:---:|:---:|:-----------------:|:-----------------:|:-------------------------------------------:|
| T | T | T | T | **T** |
| T | F | F | T | **F** |
| F | T | T | F | **F** |
| F | F | T | T | **T** |

**Observación:** El patrón T, F, F, T es exactamente el mismo que el bicondicional $P \leftrightarrow Q$.

Esto confirma la equivalencia: $P \leftrightarrow Q \equiv (P \rightarrow Q) \land (Q \rightarrow P)$

El bicondicional significa "P implica Q Y Q implica P", es decir, van siempre juntos.

</details>

---

:::exercise{title="Demostrar Equivalencia" difficulty="2"}

Usando tablas de verdad, demuestra que la contrapositiva es válida:

$$P \rightarrow Q \equiv \neg Q \rightarrow \neg P$$

:::

<details>
<summary><strong>Ver Solución</strong></summary>

| $P$ | $Q$ | $\neg P$ | $\neg Q$ | $P \rightarrow Q$ | $\neg Q \rightarrow \neg P$ |
|:---:|:---:|:--------:|:--------:|:-----------------:|:---------------------------:|
| T | T | F | F | T | T |
| T | F | F | T | **F** | **F** |
| F | T | T | F | T | T |
| F | F | T | T | T | T |

Las columnas de $P \rightarrow Q$ y $\neg Q \rightarrow \neg P$ son **idénticas**, lo que demuestra que son lógicamente equivalentes.

**Intuición:** "Si estudias, apruebas" es lo mismo que "Si no apruebas, no estudiaste". Son dos formas de decir lo mismo.

</details>

---

:::exercise{title="Formalización" difficulty="2"}

Traduce a lógica proposicional:

1. "Puedes votar si eres mayor de edad y estás registrado"
2. "El semáforo está en verde o en rojo, pero no en ambos"
3. "Llegaré tarde a menos que salga ahora"

Define tus símbolos claramente.

:::

<details>
<summary><strong>Ver Solución</strong></summary>

**1. "Puedes votar si eres mayor de edad y estás registrado"**

Símbolos:
- $V$ = "Puedes votar"
- $M$ = "Eres mayor de edad"
- $R$ = "Estás registrado"

Fórmula: $(M \land R) \rightarrow V$

*Nota: "si" introduce la condición suficiente. "Puedes votar SI..." significa que la condición implica poder votar.*

**2. "El semáforo está en verde o en rojo, pero no en ambos"**

Símbolos:
- $V$ = "El semáforo está en verde"
- $R$ = "El semáforo está en rojo"

Fórmula: $(V \lor R) \land \neg(V \land R)$

*Esta es la definición del OR exclusivo (XOR). En español, "o...pero no ambos" indica exclusividad.*

**3. "Llegaré tarde a menos que salga ahora"**

Símbolos:
- $T$ = "Llegaré tarde"
- $S$ = "Salgo ahora"

"A menos que" es complicado. Significa "si no":
- "Llegaré tarde a menos que salga" = "Si no salgo, llegaré tarde"

Fórmula: $\neg S \rightarrow T$

Equivalente: $S \lor T$ (o salgo ahora, o llego tarde, o ambos)

</details>

---

:::exercise{title="Conversión a CNF" difficulty="2"}

Convierte a CNF: $(P \lor Q) \rightarrow R$

Muestra cada paso del proceso.

:::

<details>
<summary><strong>Ver Solución</strong></summary>

**Fórmula original:** $(P \lor Q) \rightarrow R$

**Paso 1:** No hay bicondicionales.

**Paso 2:** Eliminar implicación ($\alpha \rightarrow \beta \Rightarrow \neg\alpha \lor \beta$)
$$\neg(P \lor Q) \lor R$$

**Paso 3:** Mover negación hacia adentro (De Morgan: $\neg(P \lor Q) \Rightarrow \neg P \land \neg Q$)
$$(\neg P \land \neg Q) \lor R$$

**Paso 4:** Distribuir OR sobre AND
$$(\neg P \lor R) \land (\neg Q \lor R)$$

**Resultado en CNF:** $(\neg P \lor R) \land (\neg Q \lor R)$

Dos cláusulas:
1. $\neg P \lor R$
2. $\neg Q \lor R$

**Verificación:** La fórmula original dice "Si P o Q, entonces R". Las cláusulas dicen "Si P entonces R" y "Si Q entonces R", que es lo mismo.

</details>

---

:::exercise{title="Identificar Cláusulas de Horn" difficulty="1"}

¿Cuáles de estas cláusulas son cláusulas de Horn?

1. $P \lor Q \lor R$
2. $\neg P \lor \neg Q \lor R$
3. $\neg P \lor \neg Q$
4. $P$
5. $\neg P \lor Q \lor R$

:::

<details>
<summary><strong>Ver Solución</strong></summary>

Recuerda: Una cláusula de Horn tiene **a lo más un literal positivo**.

| Cláusula | Literales Positivos | ¿Es Horn? |
|----------|:-------------------:|:---------:|
| $P \lor Q \lor R$ | 3 (P, Q, R) | ✗ No |
| $\neg P \lor \neg Q \lor R$ | 1 (R) | ✓ Sí — es una regla |
| $\neg P \lor \neg Q$ | 0 | ✓ Sí — es un objetivo |
| $P$ | 1 (P) | ✓ Sí — es un hecho |
| $\neg P \lor Q \lor R$ | 2 (Q, R) | ✗ No |

Las cláusulas 2, 3 y 4 son de Horn.

</details>

---

## Puntos Clave

1. Una **proposición** es una oración que es verdadera o falsa, no ambas
2. La **sintaxis** define qué fórmulas están bien formadas
3. La **semántica** define cuándo las fórmulas son verdaderas (usando modelos)
4. Los **conectivos** ($\neg$, $\land$, $\lor$, $\rightarrow$, $\leftrightarrow$) combinan proposiciones
5. La **implicación** es verdadera cuando el antecedente es falso (verdad por vacuidad)
6. Las **equivalencias** permiten reescribir fórmulas: De Morgan, contrapositiva, $P \rightarrow Q \equiv \neg P \lor Q$
7. **CNF** (conjunción de cláusulas) es la forma estándar para algoritmos
8. Las **cláusulas de Horn** permiten inferencia eficiente en tiempo lineal
