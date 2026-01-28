---
title: "Computabilidad vs Decidibilidad"
---

# Computabilidad vs Decidibilidad

¿Cuál es la diferencia entre "eventualmente dar una respuesta" y "siempre terminar"?

## Introducción: Una Distinción Sutil pero Crucial

La computabilidad y la decidibilidad son conceptos relacionados pero **no equivalentes**. La diferencia está en las **garantías de terminación**:

| Concepto | Pregunta Clave | Garantía |
|----------|----------------|----------|
| **Computable** | ¿Puede dar respuesta? | Eventualmente da respuesta (para algunos inputs) |
| **Decidible** | ¿Siempre termina? | Siempre termina con respuesta (para todos los inputs) |

Veamos dos programas que ilustran esta diferencia:

---

### Ejemplo 1: Problema DECIDIBLE

**Programa A:** "Determinar si un número es par"

```python
def es_par(n):
    return n % 2 == 0
```

**Análisis:**
- Para **cualquier** entrada $n$: siempre termina con True o False
- Nunca hace loop infinito
- Tiempo: $O(1)$ (constante)

**Clasificación:** Este problema es **DECIDIBLE** (y también computable, obviamente).

✅ **Siempre termina con respuesta definitiva (sí o no)**

---

### Ejemplo 2: Problema COMPUTABLE pero NO Decidible

**Programa B:** "Buscar un contraejemplo a la Conjetura de Goldbach"

(La Conjetura de Goldbach afirma que todo número par > 2 es suma de dos primos. Aún no demostrada ni refutada desde 1742.)

```python
def buscar_contraejemplo():
    n = 4
    while True:
        # Verificar si n es suma de dos primos
        if not es_suma_de_dos_primos(n):
            return n  # ¡Contraejemplo encontrado!
        n += 2
```

**Análisis:**
- **Si existe contraejemplo:** El programa eventualmente lo encuentra y termina ✓
- **Si NO existe contraejemplo:** El programa **nunca termina** (loop infinito) ✗
- No podemos saber de antemano cuánto tiempo tomar (o si terminará)

**Clasificación:** Este problema es **COMPUTABLE** (puede encontrar respuesta "sí") pero **NO DECIDIBLE** (no garantiza respuesta "no").

⚠️ **Solo termina con respuesta definitiva en algunos casos**

---

### La Diferencia Clave

| Aspecto | Programa A (Par) | Programa B (Goldbach) |
|---------|------------------|----------------------|
| **Termina siempre?** | ✅ Sí | ❌ No (solo si hay contraejemplo) |
| **Da respuesta "sí"?** | ✅ Sí (cuando n es par) | ✅ Sí (si encuentra contraejemplo) |
| **Da respuesta "no"?** | ✅ Sí (cuando n es impar) | ❌ No (nunca puede confirmar "no existe") |
| **Clasificación** | **Decidible** | **Computable pero no decidible** |

**Intuición:**
- **Decidible:** "Te garantizo respuesta (sí o no) en tiempo finito"
- **Computable (no decidible):** "Te puedo confirmar si es 'sí', pero si es 'no', tal vez nunca lo sepamos"

**Analogía:**
- **Decidible:** Buscar en una lista finita — siempre terminas
- **Computable:** Buscar en una lista infinita — si está, lo encuentras; si no está, buscas por siempre

Esta distinción es **fundamental** en teoría de la computación: hay problemas que podemos "reconocer" (computables) pero no "decidir" (decidibles).

---

## Conceptos Fundamentales

### Reconocedor (Recognizer)

Un **reconocedor** para un lenguaje $L$ es una MT $M$ tal que:

$$L = \{w \mid M \text{ acepta } w\}$$

**Comportamiento:**
- Si $w \in L$ → $M$ acepta $w$ (eventualmente)
- Si $w \notin L$ → $M$ rechaza $w$ **O** hace loop infinito

**Nota clave:** No necesita dar respuesta para strings que NO están en $L$.

---

### Decididor (Decider)

Un **decididor** para un lenguaje $L$ es una MT $M$ tal que:

$$L = \{w \mid M \text{ acepta } w\}$$

**Y además:**
- $M$ **siempre se detiene** (nunca hace loop)
- Para todo $w$: o acepta o rechaza (en tiempo finito)

**Nota clave:** Debe dar respuesta (sí o no) para **toda** entrada posible.

---

## La Jerarquía de Lenguajes

```
┌────────────────────────────────────────────┐
│  Todos los lenguajes posibles              │
│                                            │
│  ┌──────────────────────────────────┐     │
│  │  Recursivamente Enumerables       │     │
│  │  (Computables/Reconocibles)      │     │
│  │  = tienen un reconocedor          │     │
│  │                                   │     │
│  │  ┌────────────────────────┐       │     │
│  │  │  Recursivos            │       │     │
│  │  │  (Decidibles)          │       │     │
│  │  │  = tienen un decididor │       │     │
│  │  │                        │       │     │
│  │  │  Ejemplos:             │       │     │
│  │  │  • {0ⁿ1ⁿ}             │       │     │
│  │  │  • Aritmética          │       │     │
│  │  │  • SAT                 │       │     │
│  │  └────────────────────────┘       │     │
│  │                                   │     │
│  │  Ejemplos fuera (solo reconoc):  │     │
│  │  • Halting problem (veremos)     │     │
│  │  • Algunos lenguajes matemáticos │     │
│  └──────────────────────────────────┘     │
│                                            │
│  Fuera: No recursivamente enumerables     │
│  (ni siquiera reconocibles)               │
└────────────────────────────────────────────┘
```

**Relación:**
$$\text{Decidible} \subset \text{Reconocible} \subset \text{Todos los lenguajes}$$

---

## Computabilidad (Reconocibilidad)

### Definición Formal

Un lenguaje $L$ es **recursivamente enumerable** (RE) o **computable** si existe una MT $M$ que lo **reconoce**.

**Sinónimos:**
- Recursivamente enumerable
- Turing-reconocible
- Computable
- Semidecidible

### Características

✓ Si $w \in L$ → la MT **eventualmente acepta**

✗ Si $w \notin L$ → la MT puede rechazar **o** hacer loop (no sabemos cuándo parar)

### Ejemplo: Lenguaje de Programas que Imprimen "Hola"

$$L = \{\langle P \rangle \mid P \text{ es un programa que eventualmente imprime "Hola"}\}$$

**Reconocedor:**
```
En entrada <P>:
1. Simular P
2. Si P imprime "Hola" → aceptar
3. Si no... seguir esperando
```

**Observación:**
- Si $P$ imprime "Hola" → eventualmente lo detectamos ✓
- Si $P$ nunca imprime "Hola" → esperamos infinitamente ✗ (no podemos decidir "nunca lo hará")

Este lenguaje es **reconocible** pero veremos que NO es **decidible**.

---

## Decidibilidad (Recursividad)

### Definición Formal

Un lenguaje $L$ es **recursivo** o **decidible** si existe una MT $M$ que lo **decide**.

**Sinónimos:**
- Recursivo
- Turing-decidible
- Decidible
- Computable total

### Características

✓ Si $w \in L$ → la MT **acepta** (en tiempo finito)

✓ Si $w \notin L$ → la MT **rechaza** (en tiempo finito)

✓ **Siempre termina** con una respuesta clara: SÍ o NO

### Ejemplo: Lenguaje $\{0^n1^n \mid n \geq 0\}$

Este es **decidible** (vimos un decididor en la sección anterior).

Para cualquier string $w$:
- Si $w$ tiene la forma $0^n1^n$ → acepta
- Si no → rechaza
- Siempre termina ✓

---

## La Diferencia Clave: Tabla Comparativa

| Aspecto | Reconocible (RE) | Decidible (Recursivo) |
|---------|------------------|----------------------|
| **Sinónimo** | Recursivamente enumerable | Recursivo |
| **MT asociada** | Reconocedor | Decididor |
| **Si $w \in L$** | Acepta (eventualmente) | Acepta (en tiempo finito) |
| **Si $w \notin L$** | Rechaza O loop ∞ | Rechaza (en tiempo finito) |
| **Siempre termina?** | ❌ NO | ✅ SÍ |
| **Respuesta garantizada?** | Solo para $w \in L$ | Para todo $w$ |
| **Relación** | Más general | Más restrictivo |

**Analogía:**

- **Reconocible:** "Puedo confirmar las buenas noticias, pero las malas noticias pueden nunca llegar"
- **Decidible:** "Siempre te digo sí o no, sin importar cuánto tarde"

---

## Ejemplos Clasificados

### Decidibles ✅

1. **Lenguajes regulares** (todos)
   - Ejemplo: $\{w \mid w \text{ contiene "01"}\}$
   - Un autómata finito siempre termina

2. **Lenguajes libres de contexto** (todos)
   - Ejemplo: $\{0^n1^n \mid n \geq 0\}$
   - Parser siempre termina

3. **Aritmética de Presburger** (aritmética sin multiplicación)
   - Ejemplo: ¿$\exists x. 2x + 3 = 7$?
   - Decidible (aunque puede ser lento)

4. **SAT** (Satisfacibilidad Booleana)
   - ¿Esta fórmula tiene una asignación que la satisface?
   - Decidible (aunque NP-completo)

5. **Igualdad de strings**
   - ¿$w_1 = w_2$?
   - Trivialmente decidible

### Reconocibles pero NO Decidibles ⚠️

1. **Halting Problem** (veremos en detalle)
   - ¿Este programa se detiene con esta entrada?
   - Reconocible: si se detiene, eventualmente lo vemos
   - NO decidible: no podemos decidir "nunca se detendrá"

2. **Teoremas matemáticos**
   - ¿Esta afirmación es demostrable en ZFC?
   - Reconocible: si hay prueba, eventualmente la encontramos
   - NO decidible: no sabemos cuándo parar si no hay prueba

3. **Post Correspondence Problem**
   - ¿Existe una secuencia que empareja estas fichas?
   - Reconocible pero no decidible

### Ni Siquiera Reconocibles ❌

1. **Complemento del Halting Problem**
   - ¿Este programa NO se detiene?
   - No es reconocible (veremos por qué)

2. **No-equivalencia de MTs**
   - ¿Estas dos MTs reconocen lenguajes diferentes?
   - No es reconocible

---

## Propiedades de Cierre

### Decidibles son Cerrados Bajo:

- ✓ **Unión**: Si $L_1$ y $L_2$ son decidibles → $L_1 \cup L_2$ es decidible
- ✓ **Intersección**: $L_1 \cap L_2$ es decidible
- ✓ **Complemento**: $\overline{L}$ es decidible
- ✓ **Concatenación**: $L_1 \cdot L_2$ es decidible
- ✓ **Estrella de Kleene**: $L^*$ es decidible

**Prueba intuitiva (Unión):**
```
En entrada w:
1. Ejecutar decididor de L₁ en w
2. Si acepta → aceptar
3. Si rechaza → ejecutar decididor de L₂ en w
4. Aceptar/rechazar según L₂
```
Siempre termina porque ambos decidores terminan ✓

### Reconocibles son Cerrados Bajo:

- ✓ **Unión**
- ✓ **Intersección**
- ✗ **NO cerrados bajo complemento** (crucial!)

**Por qué NO complemento:**
Si pudiéramos reconocer $L$ y $\overline{L}$, podríamos **decidir** $L$:
```
En entrada w:
1. Ejecutar reconocedor de L y reconocedor de L̄ en PARALELO
2. Uno de los dos eventualmente acepta
3. Si L acepta → w ∈ L; si L̄ acepta → w ∉ L
```
Esto daría un decididor para $L$. Contradicción si $L$ no es decidible.

---

## Teorema Fundamental

### Teorema de Cierre bajo Complemento

$$L \text{ es decidible} \iff L \text{ y } \overline{L} \text{ son ambos reconocibles}$$

**Demostración (⇒):**
Si $L$ es decidible, podemos construir reconocedores para $L$ y $\overline{L}$ fácilmente (invertir aceptar/rechazar).

**Demostración (⇐):**
Si tenemos reconocedores para $L$ y $\overline{L}$:
```
En entrada w:
1. Simular ambos reconocedores en PARALELO (intercalando pasos)
2. Uno de los dos eventualmente acepta (pues w ∈ L o w ∈ L̄)
3. Si reconocedor de L acepta → aceptar
4. Si reconocedor de L̄ acepta → rechazar
```
Este es un decididor para $L$ ✓

**Implicación:** Para probar que algo NO es decidible, basta mostrar que su complemento NO es reconocible.

---

## Computabilidad de Funciones

Hasta ahora hablamos de **lenguajes** (conjuntos de strings). ¿Qué hay de **funciones**?

### Función Computable

Una función $f: \Sigma^* \to \Sigma^*$ es **computable** si existe una MT que:
- En entrada $w$
- Se detiene con $f(w)$ escrito en la cinta

**Ejemplos computables:**
- $f(n) = n + 1$ (sumar 1 en binario)
- $f(w) = w^R$ (reversa de string)
- $f(n, m) = n \times m$ (multiplicación)

### Función Parcialmente Computable

Una función **parcial** $f: \Sigma^* \rightharpoonup \Sigma^*$ puede no estar definida para algunas entradas.

$f$ es **parcialmente computable** si existe una MT que:
- Si $f(w)$ está definida → se detiene con $f(w)$
- Si $f(w)$ no está definida → hace loop

**Ejemplo:** $f(\langle P, w \rangle) = \text{output de } P(w)$ si termina, indefinido si no.

---

## Resumen: ¿Qué Podemos Hacer?

```
┌─────────────────────────────────────┐
│  Problema                           │
│         ↓                           │
│  ¿Reconocible? (¿existe MT?)        │
│         ├─ NO → imposible            │
│         └─ SÍ ↓                     │
│           ¿Decidible? (¿MT siempre termina?) │
│               ├─ NO → solo reconocible│
│               └─ SÍ ↓               │
│                 ¿Eficiente? (¿P o NP?)│
│                     ├─ P → rápido    │
│                     └─ NP-completo → probablemente lento │
└─────────────────────────────────────┘
```

---

## Puntos Clave

| Concepto | Definición | Característica |
|----------|------------|----------------|
| **Reconocible** | Tiene un reconocedor | Puede no terminar en algunos inputs |
| **Decidible** | Tiene un decididor | Siempre termina con sí/no |
| **Relación** | Decidible ⊂ Reconocible | Todo decidible es reconocible |
| **Complemento** | Decide ↔ Ambos reconocibles | Test para decidibilidad |

**La gran pregunta:** ¿Hay problemas que NO son decidibles? ¡Sí! Y el ejemplo clásico es el **Halting Problem**.

---

**Siguiente:** [Límites: El Halting Problem →](04_limites_halting.md)
