---
title: "El Robot Pensante y los Desiderata"
---

# El Robot Pensante y los Desiderata

¿Qué requisitos debe cumplir un sistema de razonamiento bajo incertidumbre?

## El Robot de Jaynes

Jaynes propone un experimento mental: imaginemos un **robot** que debe razonar sobre el mundo.

Este robot:
- Recibe información (proposiciones que pueden ser verdaderas o falsas)
- Debe asignar **grados de plausibilidad** a diferentes hipótesis
- No tiene intuición ni emociones — solo sigue reglas

**Pregunta clave:** ¿Qué reglas debe seguir?

El punto no es construir un robot real, sino preguntarnos: **¿qué reglas de razonamiento son las correctas?**

---

## Los Desiderata

Jaynes establece que nuestro robot debe cumplir tres requisitos fundamentales, llamados **desiderata**:

### Desideratum I: Representación por Números Reales

> Los grados de plausibilidad se representan mediante **números reales**.

**¿Por qué?**
- Necesitamos poder comparar: "A es más plausible que B"
- Los números reales permiten ordenamiento total
- Permiten operaciones matemáticas

**Convención:**
- Mayor número = mayor plausibilidad
- Usaremos el rango $[0, 1]$ donde:
  - $0$ = imposible (certeza de falsedad)
  - $1$ = cierto (certeza de verdad)
  - Valores intermedios = grados de plausibilidad

---

### Desideratum II: Correspondencia Cualitativa con el Sentido Común

> El razonamiento del robot debe **corresponder cualitativamente** con el razonamiento humano sensato.

Esto significa:

**a) Si la plausibilidad de A aumenta, y la de "A implica B" permanece constante, entonces la plausibilidad de B debe aumentar (o al menos no disminuir).**

Ejemplo: Si me vuelvo más seguro de que "va a llover", y sigo creyendo que "si llueve, el suelo se moja", entonces debo volverme más seguro de que "el suelo se mojará".

**b) Si tenemos más información que hace A más plausible, nuestra asignación debe reflejar eso.**

El robot no puede tener "corazonadas" contradictorias — debe ser sensato.

---

### Desideratum III: Consistencia

> El robot debe ser **consistente** en tres sentidos:

**a) Consistencia estructural:**
Si una conclusión puede alcanzarse por múltiples caminos, todos deben dar el mismo resultado.

Ejemplo: $P(A \cap B) = P(B \cap A)$ — el orden no importa.

**b) Consistencia lógica:**
El robot debe usar toda la información relevante, no solo parte de ella.

**c) Consistencia bajo cambio de representación:**
Dos problemas equivalentes deben tener la misma respuesta, sin importar cómo se formulen.

---

## Lo Que NO Son los Desiderata

Nota que los desiderata **no especifican**:

- ❌ Qué fórmulas usar
- ❌ Qué valor asignar a qué proposición
- ❌ Ningún axioma específico de probabilidad

Los desiderata son **requisitos de racionalidad**, no reglas específicas.

Lo notable es que de estos requisitos generales se **derivan** las reglas de probabilidad.

---

## El Teorema de Cox

En 1946, Richard Cox demostró un teorema fundamental:

> **Teorema de Cox:** Si un sistema de razonamiento plausible satisface los desiderata, entonces sus reglas deben ser **isomorfas** a las reglas de probabilidad.

"Isomorfas" significa que pueden no verse idénticas, pero son matemáticamente equivalentes (quizás con un cambio de escala).

**Implicación profunda:** Las reglas de probabilidad no son una elección arbitraria entre muchas posibles — son la **única** elección consistente.

---

## Derivación Informal

¿Cómo se llega de los desiderata a las reglas? Aquí un esbozo:

### Paso 1: La regla del producto

Queremos: ¿cómo se relaciona $P(A \cap B | C)$ con $P(A|C)$ y $P(B|C)$?

Por el Desideratum II (sentido común):
- La plausibilidad de "$A$ Y $B$" depende de:
  - Qué tan plausible es $B$ dado $C$
  - Qué tan plausible es $A$ dado que $B$ y $C$ son verdaderos

Esto sugiere una forma funcional:
$$P(AB|C) = f(P(A|BC), P(B|C))$$

Por el Desideratum III (consistencia):
- La función $f$ debe ser asociativa y conmutativa en cierto sentido
- El análisis funcional muestra que $f$ debe ser el **producto**

**Resultado:**
$$P(AB|C) = P(A|BC) \cdot P(B|C)$$

---

### Paso 2: La regla de la suma

Queremos: ¿cómo se relaciona $P(A|C)$ con $P(\neg A|C)$?

Por el Desideratum II:
- Si $A$ se vuelve más plausible, $\neg A$ debe volverse menos plausible
- Hay una relación funcional: $P(\neg A|C) = g(P(A|C))$

Por el Desideratum III (consistencia):
- Aplicando la relación dos veces: $P(A|C) = g(g(P(A|C)))$
- Esto impone restricciones fuertes sobre $g$

**Resultado:**
$$P(A|C) + P(\neg A|C) = 1$$

---

## Resumen de Resultados

De los desiderata se derivan:

| Regla | Fórmula | Origen |
|-------|---------|--------|
| **Producto** | $P(AB\|C) = P(A\|BC) \cdot P(B\|C)$ | Consistencia + Sentido común |
| **Suma** | $P(A\|C) + P(\neg A\|C) = 1$ | Consistencia + Sentido común |
| **Bayes** | Se deriva de aplicar producto dos veces | Consecuencia |

---

## La Lección Profunda

**No elegimos** las reglas de probabilidad porque son convenientes.

**Las reglas de probabilidad son inevitables** si queremos:
1. Razonar con grados de plausibilidad
2. Ser consistentes
3. Corresponder con el sentido común

Cualquier otro sistema de "razonamiento plausible" o:
- Viola algún desideratum
- Es equivalente a probabilidad (quizás disfrazado)

---

## Conexión con IA

Un agente inteligente ES este robot:
- Recibe observaciones del ambiente
- Debe actualizar sus creencias
- Debe ser consistente

Los desiderata son **requisitos de diseño** para cualquier agente racional.

```
┌─────────────────────────────────────────────────┐
│                AGENTE RACIONAL                  │
├─────────────────────────────────────────────────┤
│  Entrada: Observaciones, conocimiento previo    │
│  Proceso: Actualización de creencias            │
│  Requisitos: Los desiderata de Jaynes           │
│  Resultado: Las reglas de probabilidad          │
│  Salida: Decisiones bajo incertidumbre          │
└─────────────────────────────────────────────────┘
```

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| **Robot de Jaynes** | Agente ideal que razona con plausibilidades |
| **Desideratum I** | Grados de plausibilidad como números reales |
| **Desideratum II** | Correspondencia con sentido común |
| **Desideratum III** | Consistencia (estructural, lógica, representacional) |
| **Teorema de Cox** | Los desiderata implican las reglas de probabilidad |

---

**Siguiente:** [Probabilidad como Lógica Extendida →](03_probabilidad_como_logica.md)
