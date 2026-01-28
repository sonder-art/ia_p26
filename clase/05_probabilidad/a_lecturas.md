---
title: "Lecturas de Probabilidad"
---

# Lecturas de Probabilidad

Material de lectura para este módulo.

## Lectura Principal

### E.T. Jaynes - "Probability Theory: The Logic of Science"

**Archivo:** [lecturas_probabilidad.pdf](lecturas_probabilidad.pdf)

**Páginas extraídas:** 13-61 (Capítulos 1-2)

**Contenido:**
- **Capítulo 1:** Plausible Reasoning
  - El problema del razonamiento bajo incertidumbre
  - El robot pensante
  - Los desiderata
  
- **Capítulo 2:** The Quantitative Rules
  - Derivación de la regla del producto
  - Derivación de la regla de la suma
  - Comentarios sobre la interpretación

---

## Cómo Generar el PDF

Para extraer las páginas del libro de Jaynes, ejecuta:

```bash
cd clase/b_libros
python extract_probability_chapter.py
```

Esto creará `clase/05_probabilidad/lecturas_probabilidad.pdf` con las páginas relevantes.

**Requisitos:**
- Python 3
- pypdf
- reportlab

---

## Lectura Recomendada

### Sobre el Enfoque de Jaynes

- **Jaynes, E.T.** (2003). *Probability Theory: The Logic of Science*. Cambridge University Press.
  - El libro completo desarrolla la visión de probabilidad como extensión de la lógica
  - Capítulos 1-2 son fundamentales para la filosofía
  - Capítulos posteriores aplican el enfoque a problemas específicos

### Sobre el Teorema de Cox

- **Cox, R.T.** (1946). "Probability, Frequency and Reasonable Expectation". *American Journal of Physics*.
  - El artículo original que demuestra que las reglas de probabilidad se derivan de requisitos de consistencia

### Comparación de Interpretaciones

- **Hájek, A.** (2019). "Interpretations of Probability". *Stanford Encyclopedia of Philosophy*.
  - Excelente resumen de las diferentes interpretaciones
  - Disponible gratuitamente online

---

## Videos Recomendados

### 3Blue1Brown - Bayes Theorem

Una excelente visualización del Teorema de Bayes:
- [Bayes theorem, the geometry of changing beliefs](https://www.youtube.com/watch?v=HZGCoVF3YvM)

### Veritasium - The Bayesian Trap

Sobre los peligros de ignorar el prior:
- [The Bayesian Trap](https://www.youtube.com/watch?v=R13BD8qKeTg)

---

## Nota sobre el Libro de Jaynes

El libro de Jaynes es considerado uno de los tratamientos más profundos de los fundamentos de la probabilidad. Sin embargo, tiene algunas características:

**Fortalezas:**
- Justificación rigurosa de las reglas de probabilidad
- Enfoque unificador (supera el debate frecuentista vs bayesiano)
- Muchos ejemplos y aplicaciones
- Escrito con personalidad y humor

**Desafíos:**
- Puede ser técnicamente denso
- El autor tiene opiniones fuertes (a veces polémicas)
- Algunos capítulos posteriores son muy avanzados

**Recomendación:** Lee los capítulos 1-2 cuidadosamente. Son la base conceptual de todo lo demás.

---

## Resumen de Recursos

| Recurso | Tipo | Tema |
|---------|------|------|
| Jaynes Cap. 1-2 | PDF | Fundamentos, desiderata, reglas |
| Cox (1946) | Artículo | Derivación original |
| Stanford Encyclopedia | Web | Interpretaciones de probabilidad |
| 3Blue1Brown | Video | Visualización de Bayes |
| Veritasium | Video | Intuición sobre priors |

---

**Volver al índice:** [Índice →](00_index.md)
