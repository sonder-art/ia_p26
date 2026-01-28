---
title: "Introducción: ¿Por qué Probabilidad?"
---

# Introducción: ¿Por qué Probabilidad?

El problema fundamental del razonamiento bajo incertidumbre.

## El Límite de la Lógica Deductiva

En la sección anterior estudiamos **lógica proposicional**: un sistema donde las afirmaciones son verdaderas o falsas, y las conclusiones siguen con certeza absoluta.

Pero considera este escenario:

> Un policía llega a una joyería. La ventana está rota, hay vidrios en el piso, y la vitrina de diamantes está vacía. El dueño reporta que falta mercancía valiosa.

**Pregunta:** ¿Hubo un robo?

Con lógica deductiva pura, **no podemos concluir nada**:
- No vimos el robo ocurrir
- No tenemos prueba definitiva de quién lo hizo
- Podría haber otras explicaciones (aunque improbables)

Sin embargo, cualquier persona razonable diría: "Probablemente hubo un robo."

**Este es el problema:** La lógica deductiva solo maneja certezas, pero el mundo real está lleno de incertidumbre.

---

## Razonamiento Plausible

Lo que hacemos naturalmente es **razonamiento plausible**:

| Lógica Deductiva | Razonamiento Plausible |
|------------------|------------------------|
| "Si A entonces B. A es verdad. Por lo tanto B." | "Si A entonces B es más plausible. B es verdad. Por lo tanto A es más plausible." |
| Certeza absoluta | Grados de creencia |
| Silogismo clásico | Actualización de evidencia |

**Ejemplo del policía:**
- Si hubo un robo → esperaríamos ventana rota, vitrina vacía, etc.
- Observamos ventana rota, vitrina vacía, etc.
- Por lo tanto, la hipótesis "hubo un robo" se vuelve **más plausible**

Este no es un silogismo válido en lógica clásica (es la "falacia de afirmar el consecuente"). Pero es exactamente cómo razonamos — y cómo **debemos** razonar cuando no tenemos certeza.

---

## La Pregunta Fundamental

Si vamos a razonar con incertidumbre, necesitamos responder:

> **¿Cómo asignamos y actualizamos grados de plausibilidad de manera consistente?**

Resulta que hay **una única respuesta** a esta pregunta, y esa respuesta es la teoría de probabilidad.

Esto es lo que E.T. Jaynes demuestra en su libro "Probability Theory: The Logic of Science":

1. Si queremos que nuestro razonamiento sea **consistente**
2. Y que corresponda con el **sentido común**
3. Entonces **debemos** usar las reglas de probabilidad

No es que elijamos usar probabilidad porque es conveniente — es que **no hay otra opción** si queremos ser racionales.

---

## Tres Preguntas que Responderemos

### 1. ¿Qué es probabilidad?

No solo "frecuencia de eventos" — es algo más fundamental.

### 2. ¿De dónde vienen las reglas?

Las reglas de probabilidad (producto, suma, Bayes) no son axiomas arbitrarios — se **derivan** de requisitos de consistencia.

### 3. ¿Cómo se usa en la práctica?

Actualizar creencias con evidencia, tomar decisiones bajo incertidumbre, cuantificar lo que no sabemos.

---

## Dos Tipos de Incertidumbre

Es útil distinguir entre:

**Incertidumbre epistémica (del conocimiento):**
- No sabemos algo, pero en principio podríamos saberlo
- Ejemplo: ¿Cuál es la capital de Mongolia? (No lo sé, pero existe una respuesta)

**Incertidumbre aleatoria (del mundo):**
- El resultado es inherentemente impredecible
- Ejemplo: ¿Qué saldrá en el próximo lanzamiento de dado?

La probabilidad maneja **ambos** tipos de incertidumbre con el mismo formalismo. Esta es una de las ideas más profundas de Jaynes: no hay diferencia fundamental entre "no saber" y "ser aleatorio" — en ambos casos, asignamos grados de plausibilidad.

---

## El Enfoque de Este Módulo

Seguiremos el enfoque de **E.T. Jaynes**, que difiere del tratamiento tradicional:

| Enfoque Tradicional | Enfoque Jaynes |
|---------------------|----------------|
| Empieza con axiomas (Kolmogorov) | Empieza con desiderata (requisitos) |
| Define probabilidad sobre conjuntos | Define probabilidad como extensión de lógica |
| Las reglas se postulan | Las reglas se **derivan** |
| "Frecuencia" o "creencia subjetiva" | "Grado de plausibilidad racional" |

El resultado matemático es el mismo (las mismas reglas), pero la **interpretación** y la **justificación** son más profundas.

---

## Por Qué Importa para IA

Los agentes inteligentes operan bajo incertidumbre:

- **Percepción:** Los sensores son ruidosos
- **Modelos:** El mundo es parcialmente observable
- **Acciones:** Los efectos son probabilísticos
- **Aprendizaje:** Generalizar requiere manejar incertidumbre

Un agente que no puede razonar probabilísticamente está condenado a:
- Paralizarse ante la incertidumbre
- Tomar decisiones arbitrarias
- No aprender de la experiencia

La probabilidad es el **lenguaje** del razonamiento bajo incertidumbre.

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| **Límite de la lógica** | No puede manejar incertidumbre |
| **Razonamiento plausible** | Lo que hacemos naturalmente ante evidencia incompleta |
| **Probabilidad** | La única extensión consistente de la lógica |
| **Enfoque Jaynes** | Derivar las reglas, no postularlas |

---

**Siguiente:** [El Robot Pensante y los Desiderata →](02_robot_desiderata.md)
