---
title: "Probabilidad como Lógica Extendida"
---

# Probabilidad como Lógica Extendida

La conexión profunda entre lógica deductiva y razonamiento probabilístico.

## La Gran Idea

La tesis central de Jaynes es:

> **La teoría de probabilidad es una extensión de la lógica deductiva para manejar situaciones de incertidumbre.**

Esto NO significa que probabilidad sea "lógica aproximada" o "lógica borrosa". Significa que:

1. La lógica deductiva es un **caso especial** de probabilidad
2. Ambas siguen de los mismos principios de consistencia
3. La probabilidad es la **única** extensión válida

---

## Lógica Deductiva: Certeza

Recordemos la lógica proposicional:

| Premisas | Conclusión | Tipo |
|----------|------------|------|
| $A \to B$, $A$ | $B$ | Modus Ponens (válido) |
| $A \to B$, $B$ | $A$ | Afirmación del consecuente (inválido) |
| $A \to B$, $\neg A$ | $\neg B$ | Negación del antecedente (inválido) |

En lógica clásica, las "falacias" no nos dicen nada. Pero en el mundo real, **sí nos dicen algo**:

- Si "lluvia → suelo mojado" y observamos suelo mojado, la lluvia es **más plausible**
- No es certeza, pero es información útil

---

## Probabilidad: Grados de Certeza

La probabilidad extiende la lógica de valores {0, 1} a todo el intervalo [0, 1]:

| Lógica | Probabilidad |
|--------|--------------|
| Verdadero (1) | $P = 1$ (certeza) |
| Falso (0) | $P = 0$ (imposibilidad) |
| ??? | $0 < P < 1$ (incertidumbre) |

Cuando $P(A) = 1$ o $P(A) = 0$, la probabilidad se reduce a lógica deductiva.

---

## Las "Falacias" Revisitadas

Lo que en lógica son falacias, en probabilidad son **actualizaciones legítimas**:

### Afirmación del Consecuente

**Lógica:** $A \to B$, $B$ ⊬ $A$ (inválido)

**Probabilidad:** Observar $B$ aumenta $P(A)$

$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

Si $P(B|A) > P(B)$, entonces $P(A|B) > P(A)$.

**Ejemplo:**
- Si llueve, el suelo se moja: $P(\text{mojado}|\text{lluvia}) \approx 1$
- Vemos el suelo mojado
- La probabilidad de que haya llovido **aumenta**

No podemos concluir con certeza, pero sí podemos actualizar nuestra creencia.

---

### Negación del Antecedente

**Lógica:** $A \to B$, $\neg A$ ⊬ $\neg B$ (inválido)

**Probabilidad:** Depende del contexto

Si $A$ era la única (o principal) causa de $B$, entonces $\neg A$ hace $B$ menos probable.

**Ejemplo:**
- "Si hay fuego, hay humo"
- No hay fuego
- El humo es menos probable (aunque no imposible — podría haber otras fuentes)

---

## La Notación Condicional

En el enfoque de Jaynes, **toda probabilidad es condicional**:

$$P(A|I)$$

Donde $I$ representa la **información de fondo** (background information).

**No existe** $P(A)$ sin contexto. Siempre hay información implícita:
- Conocimiento del dominio
- Supuestos del modelo
- Observaciones previas

Esto resuelve muchas paradojas aparentes de probabilidad.

---

## Comparación Formal

| Aspecto | Lógica Deductiva | Probabilidad |
|---------|------------------|--------------|
| **Valores** | {Verdadero, Falso} | [0, 1] |
| **Conjunción** | $A \land B$ | $P(AB) = P(A|B)P(B)$ |
| **Disyunción** | $A \lor B$ | $P(A \cup B) = P(A) + P(B) - P(AB)$ |
| **Negación** | $\neg A$ | $P(\neg A) = 1 - P(A)$ |
| **Implicación** | $A \to B$ | $P(B|A)$ |
| **Modus Ponens** | Si $A \to B$ y $A$, entonces $B$ | Si $P(B|A) = 1$ y $P(A) = 1$, entonces $P(B) = 1$ |

Cuando las probabilidades son 0 o 1, la tabla de probabilidad **colapsa** a la lógica deductiva.

---

## Ejemplo: El Silogismo Débil

**Silogismo fuerte (lógica):**
- Todos los hombres son mortales
- Sócrates es hombre
- Por lo tanto, Sócrates es mortal

**Silogismo débil (probabilidad):**
- La mayoría de los estudiantes aprueban el curso ($P(\text{aprobar}|\text{estudiante}) = 0.8$)
- Ana es estudiante
- Por lo tanto, Ana probablemente aprobará ($P(\text{Ana aprueba}) = 0.8$)

El silogismo débil no es una "versión inferior" — es la extensión natural cuando no tenemos certeza universal.

---

## Implicaciones Filosóficas

### 1. No hay "probabilidad objetiva" sin información

Preguntar "¿cuál es la probabilidad de X?" sin especificar la información disponible no tiene sentido.

Dos personas con diferente información pueden (y deben) asignar diferentes probabilidades al mismo evento.

### 2. Probabilidad ≠ Frecuencia (necesariamente)

La frecuencia es **una forma** de obtener información, pero no la única.

Puedo asignar probabilidad a:
- Eventos únicos ("¿Ganará este candidato?")
- Hipótesis científicas ("¿Es correcta la relatividad?")
- Proposiciones sobre el pasado ("¿Hubo vida en Marte?")

### 3. La probabilidad es epistemológica

La probabilidad describe **nuestro estado de conocimiento**, no necesariamente una propiedad del mundo.

---

## Consistencia: El Punto Clave

¿Por qué debemos usar probabilidad y no otra cosa?

**Teorema de Cox:** Cualquier sistema de "grados de creencia" que sea:
- Representable por números reales
- Consistente internamente
- Correspondiente con el sentido común

...debe ser matemáticamente equivalente a la probabilidad.

No es que probabilidad sea "una buena opción". Es la **única** opción consistente.

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| **Extensión de lógica** | Probabilidad generaliza lógica a incertidumbre |
| **Valores continuos** | De {0,1} a [0,1] |
| **Falacias útiles** | Afirmar consecuente y negar antecedente dan información |
| **Todo es condicional** | $P(A\|I)$ siempre relativo a información |
| **Teorema de Cox** | Probabilidad es la única extensión consistente |

---

**Siguiente:** [Interpretaciones de Probabilidad →](04_interpretaciones.md)
