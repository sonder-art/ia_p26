---
title: "Las Reglas de Probabilidad"
---

# Las Reglas de Probabilidad

Dos caminos al mismo destino: axiomas vs desiderata.

## Dos Enfoques

Hay dos formas de llegar a las reglas de probabilidad:

| Enfoque | Autor | Método |
|---------|-------|--------|
| **Axiomático** | Kolmogorov (1933) | Postular axiomas, derivar consecuencias |
| **Constructivo** | Cox/Jaynes | Derivar reglas de requisitos de consistencia |

Ambos llegan a las **mismas reglas matemáticas**, pero con diferente justificación.

---

## El Enfoque de Kolmogorov

### Los Axiomas

Kolmogorov define probabilidad mediante tres axiomas:

**Axioma 1 (No negatividad):**
$$P(A) \geq 0$$

**Axioma 2 (Normalización):**
$$P(\Omega) = 1$$

**Axioma 3 (Aditividad):**
Si $A \cap B = \emptyset$, entonces:
$$P(A \cup B) = P(A) + P(B)$$

### Ventajas

- **Riguroso:** Base matemática sólida
- **General:** Funciona para cualquier espacio de probabilidad
- **Aceptado:** Estándar en matemáticas

### Limitación

Los axiomas se **postulan**, no se justifican. ¿Por qué estos axiomas y no otros?

---

## El Enfoque de Jaynes/Cox

### El Punto de Partida

En lugar de axiomas, Jaynes parte de **desiderata** (requisitos):

1. Los grados de plausibilidad son números reales
2. Correspondencia cualitativa con sentido común
3. Consistencia

### La Derivación

De estos requisitos, se **derivan** las reglas:

**Paso 1:** Buscar la forma funcional de $P(AB|C)$

Por el desideratum de sentido común:
- La plausibilidad de "$A$ y $B$" depende de la plausibilidad de $B$ y de $A$ dado $B$
- Debe existir una función: $P(AB|C) = F(P(A|BC), P(B|C))$

Por consistencia (asociatividad):
- $P(ABC|D) = F(F(P(A|BCD), P(B|CD)), P(C|D))$
- $P(ABC|D) = F(P(A|BCD), F(P(B|CD), P(C|D)))$

El análisis funcional muestra que $F$ debe ser el **producto**.

**Paso 2:** Derivar la regla de la suma

Por sentido común:
- Si $A$ es más plausible, $\neg A$ es menos plausible
- Existe una función: $P(\neg A|B) = S(P(A|B))$

Por consistencia:
- $P(A|B) = S(S(P(A|B)))$ (negar dos veces)
- Esto restringe fuertemente la forma de $S$

El resultado: $S(x) = 1 - x$, es decir:
$$P(A|B) + P(\neg A|B) = 1$$

---

## Las Dos Reglas Fundamentales

### Regla del Producto

$$P(AB|C) = P(A|BC) \cdot P(B|C) = P(B|AC) \cdot P(A|C)$$

**Lectura:** "La probabilidad de A y B dado C es la probabilidad de B dado C, multiplicada por la probabilidad de A dado que B y C son verdaderos."

### Regla de la Suma

$$P(A|C) + P(\neg A|C) = 1$$

**Lectura:** "Las probabilidades de A y no-A suman 1."

**Extensión para eventos mutuamente excluyentes:**
$$P(A \cup B|C) = P(A|C) + P(B|C) \quad \text{si } A \cap B = \emptyset$$

---

## Comparación de Enfoques

| Aspecto | Kolmogorov | Jaynes |
|---------|------------|--------|
| **Punto de partida** | Axiomas | Desiderata |
| **Justificación** | "Son los axiomas" | "Son las únicas reglas consistentes" |
| **Reglas** | Se postulan | Se derivan |
| **Interpretación** | Neutral | Probabilidad como lógica extendida |
| **Resultado** | Idéntico | Idéntico |

**El punto clave:** Jaynes no cambia las matemáticas, cambia la **justificación**.

---

## ¿Por Qué Importa la Diferencia?

### Para la Filosofía

Kolmogorov: "Usamos estas reglas porque las definimos así"
Jaynes: "Debemos usar estas reglas si queremos ser consistentes"

### Para la Práctica

Cuando enfrentamos problemas de asignación de probabilidades:
- Kolmogorov: Los axiomas no dicen cómo asignar valores específicos
- Jaynes: Los desiderata guían la asignación (máxima entropía, etc.)

### Para la IA

Un agente que "razona bajo incertidumbre" no tiene opción:
- Si quiere ser consistente, debe usar probabilidad
- Las reglas no son una elección de diseño, son un requisito

---

## La Regla de la Suma Generalizada

Para eventos que no son mutuamente excluyentes:

$$P(A \cup B|C) = P(A|C) + P(B|C) - P(AB|C)$$

**Derivación:**

$A \cup B$ se puede descomponer en partes disjuntas:
- $A \cup B = A \cup (B \cap \neg A)$
- $P(A \cup B) = P(A) + P(B \cap \neg A)$
- $P(B \cap \neg A) = P(B) - P(AB)$

Por lo tanto:
$$P(A \cup B) = P(A) + P(B) - P(AB)$$

---

## Regla del Producto: Versión Simétrica

De la regla del producto:
$$P(AB|C) = P(A|BC) \cdot P(B|C)$$
$$P(AB|C) = P(B|AC) \cdot P(A|C)$$

Igualando:
$$P(A|BC) \cdot P(B|C) = P(B|AC) \cdot P(A|C)$$

Esta simetría es la base del **Teorema de Bayes**.

---

## Regla de la Cadena

Extendiendo la regla del producto a múltiples variables:

$$P(A_1, A_2, ..., A_n | C) = P(A_1|C) \cdot P(A_2|A_1, C) \cdot P(A_3|A_1, A_2, C) \cdots P(A_n|A_1,...,A_{n-1}, C)$$

**Ejemplo con tres variables:**
$$P(ABC|D) = P(A|D) \cdot P(B|AD) \cdot P(C|ABD)$$

Esto es fundamental para:
- Modelos gráficos probabilísticos
- Redes bayesianas
- Modelos de lenguaje (¡LLMs!)

---

## Resumen

| Regla | Fórmula | Origen |
|-------|---------|--------|
| **Producto** | $P(AB\|C) = P(A\|BC) \cdot P(B\|C)$ | Consistencia + sentido común |
| **Suma** | $P(A\|C) + P(\neg A\|C) = 1$ | Consistencia |
| **Suma general** | $P(A \cup B) = P(A) + P(B) - P(AB)$ | Derivada de las anteriores |
| **Cadena** | $P(A_1...A_n) = \prod_i P(A_i\|A_1...A_{i-1})$ | Aplicación repetida |

**Lo fundamental:** Estas no son reglas arbitrarias — son las **únicas** reglas que satisfacen requisitos básicos de racionalidad.

---

**Siguiente:** [Teorema de Bayes →](08_bayes.md)
