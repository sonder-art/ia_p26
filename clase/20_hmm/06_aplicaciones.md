---
title: "Aplicaciones"
---

# Aplicaciones de los HMMs

Los HMMs son uno de los modelos probabilísticos secuenciales más influyentes en la historia de la inteligencia artificial. En las décadas de 1980 y 1990 dominaron el reconocimiento de voz; hoy siguen siendo la base de muchos sistemas de etiquetado y detección. En esta sección describimos cuatro aplicaciones concretas.

---

## 1. Reconocimiento de voz

**Problema:** Convertir una señal de audio en texto.

| Capa del HMM | En reconocimiento de voz |
|--------------|--------------------------|
| Estados ocultos | Fonemas (unidades de sonido: /a/, /t/, /s/...) |
| Observaciones | Vectores de características acústicas (MFCC) extraídas del audio cada 10 ms |
| Parámetros | Aprendidos de millones de horas de audio etiquetado |

**Problema HMM relevante:** Los tres.
- **Evaluación** (Forward): dado un modelo de "hola" y el audio, ¿cuán probable es que el audio diga "hola"?
- **Decodificación** (Viterbi): ¿qué secuencia de fonemas explica mejor el audio?
- **Aprendizaje** (Baum-Welch): ajustar el modelo de fonemas a partir de datos.

Los sistemas de reconocimiento de voz de los años 1990–2010 (incluyendo los primeros sistemas de Siri y Google Voice) estaban basados enteramente en HMMs. Hoy conviven con redes neuronales, pero los HMMs siguen siendo parte de muchos sistemas de producción.

---

## 2. Etiquetado morfosintáctico (POS tagging)

**Problema:** Dado un texto, asignar a cada palabra su categoría gramatical (sustantivo, verbo, adjetivo, etc.).

| Capa del HMM | En POS tagging |
|--------------|----------------|
| Estados ocultos | Categorías gramaticales (NN, VB, JJ, DT...) |
| Observaciones | Las palabras del texto |
| $A_{ij}$ | Probabilidad de que una categoría $i$ sea seguida por la categoría $j$ (aprendido de corpus etiquetados) |
| $B_{ik}$ | Probabilidad de que la categoría $i$ genere la palabra $k$ |

**Ejemplo:**

Texto: "El perro corre rápido"

| Palabra | Estado oculto (etiqueta) |
|---------|:------------------------:|
| El | DT (determinante) |
| perro | NN (sustantivo) |
| corre | VB (verbo) |
| rápido | JJ (adjetivo) |

**Problema HMM relevante:** Decodificación (Viterbi). Dado el modelo y las palabras, encontrar la secuencia de etiquetas más probable.

El POS tagging con HMMs fue el estado del arte en NLP desde los años 1990 hasta mediados de la década de 2010. NLTK en Python todavía incluye un tagger basado en HMMs como herramienta estándar.

---

## 3. Bioinformática: alineamiento y perfiles de proteínas

**Problema:** Identificar si una secuencia de aminoácidos pertenece a una familia de proteínas, o encontrar genes codificantes en una secuencia de ADN.

| Capa del HMM | En bioinformática |
|--------------|-------------------|
| Estados ocultos | Posiciones funcionales del gen o proteína (inicio, codificante, intrón, fin) |
| Observaciones | Nucleótidos (A, T, G, C) o aminoácidos (20 posibilidades) |
| $A_{ij}$ | Probabilidad de pasar de una región funcional a otra |
| $B_{ik}$ | Probabilidad de observar el nucleótido/aminoácido $k$ en la región $i$ |

**Aplicación concreta — HMM de perfil:**
Una familia de proteínas (por ejemplo, las kinasas) tiene posiciones conservadas y posiciones variables. Un HMM de perfil modela esta variabilidad: estados de "match" (posición conservada), "insert" (inserción), "delete" (deleción). Para clasificar una nueva proteína, se compara su verosimilitud bajo el modelo de la familia vs. un modelo aleatorio.

**Problema HMM relevante:** Evaluación (Forward) para clasificación, Viterbi para alineamiento óptimo.

La base de datos Pfam contiene más de 20,000 familias de proteínas, todas descritas mediante HMMs de perfil.

---

## 4. Regímenes financieros

**Problema:** Los mercados financieros alternan entre períodos de baja volatilidad (mercado "toro") y alta volatilidad (mercado "oso"). Detectar el régimen actual permite ajustar estrategias de inversión.

| Capa del HMM | En finanzas |
|--------------|-------------|
| Estados ocultos | Régimen de mercado (bull = alcista, bear = bajista, lateral) |
| Observaciones | Retornos diarios del índice S&P 500, o características derivadas (volatilidad realizada, spread) |
| $A_{ij}$ | Probabilidad de transición entre regímenes (aprendida de datos históricos) |
| $B_{ik}$ | Distribución de los retornos en cada régimen (normal con distinta media/varianza) |

**Problema HMM relevante:** Los tres, pero especialmente:
- **Aprendizaje** (Baum-Welch): estimar los parámetros del régimen a partir de datos históricos sin conocer los regímenes verdaderos.
- **Decodificación** (Viterbi): dado el modelo aprendido y la serie temporal reciente, ¿en qué régimen estamos hoy?
- **Evaluación** (Forward): ¿cuán probable es que la secuencia de retornos reciente sea compatible con el régimen actual?

Un modelo de dos estados con distribuciones gaussianas entrenado sobre el S&P 500 logra capturar las crisis financieras (2001, 2008, 2020) como períodos de alta probabilidad de estar en el estado "oso".

---

## 5. Resumen: qué tipo de problema HMM importa en cada dominio

| Aplicación | Evaluación | Decodificación | Aprendizaje |
|------------|:----------:|:--------------:|:-----------:|
| Reconocimiento de voz | ✓ (clasificar candidatos) | ✓ (transcripción) | ✓ (entrenamiento) |
| POS tagging | — | ✓ (etiquetar texto) | ✓ (entrenar con corpus) |
| Bioinformática | ✓ (clasificar secuencias) | ✓ (alinear) | ✓ (perfil de familia) |
| Regímenes financieros | ✓ (detección online) | ✓ (régimen actual) | ✓ (datos históricos) |

Los HMMs no resuelven todos los problemas secuenciales — las redes neuronales recurrentes (RNNs) y los Transformers tienen mayor capacidad de modelado. Pero los HMMs tienen ventajas únicas: son **interpretables** (los estados tienen significado concreto), **eficientes** (Forward y Viterbi escalan bien), y **funcionan bien con pocos datos** (pocos parámetros que estimar). Siguen siendo la herramienta correcta para muchos problemas de escala pequeña o mediana.
