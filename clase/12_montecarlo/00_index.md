---
title: "Métodos de Monte Carlo"
---

:::homework{id="hw-montecarlo" title="Tarea Monte Carlo: notebooks y aplicación" due="2026-03-18" points="25"}
Entrega los siguientes notebooks del módulo:

- `01_fundamentos`
- `02_reduccion_varianza`
- Un notebook de aplicación (elige uno de la lista del módulo)

**Opciones de entrega (elige una):**

1. **Pull Request + Canvas:** Sube tu trabajo en un pull request al repositorio del curso y pega el enlace en la tarea de Canvas.
2. **Canvas directo:** Sube los archivos `.ipynb` directamente en la tarea de Canvas.
:::

# Métodos de Monte Carlo

> *"The first ENIAC runs were made in late 1947. The idea was to test whether the calculation of neutron diffusion was feasible using Monte Carlo... It worked beyond our expectations."*
> — Nicholas Metropolis

Hemos aprendido a representar la incertidumbre con probabilidad, a razonar con redes bayesianas y a inferir causalidad. Pero hay una pregunta práctica que ninguno de esos marcos responde solo: **¿cómo calculamos concretamente con distribuciones complejas?**

La respuesta —sorprendentemente simple y poderosa— es Monte Carlo: **muestrea y promedia**.

## Contenido

| Sección | Tema | Idea clave |
|:-------:|------|-----------|
| 12.1 | [Historia y Motivación](01_historia.md) | Von Neumann, Ulam, Metropolis y la controversia del nombre |
| 12.2 | [Fundamentos Formales](02_fundamentos.md) | LLN, CLT, error $O(1/\sqrt{n})$, independencia dimensional |

## Materiales y flujo de trabajo

| Paso | Material | Colab | Descripción |
|:----:|---------|:-----:|-------------|
| 1 | [12.1 Historia](01_historia.md) | — | Narrativa: el origen del método |
| 2 | [12.2 Fundamentos](02_fundamentos.md) | — | La matemática detrás: LLN, CLT, error $O(1/\sqrt{n})$, independencia dimensional |
| 3 | [Notebook 01 — Fundamentos](notebooks/01_fundamentos.ipynb) | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/12_montecarlo/notebooks/01_fundamentos.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> | Clase: π, integración, LLN/CLT, primer vistazo a reducción de varianza |
| 4 | [Notebook 02 — Reducción de Varianza](notebooks/02_reduccion_varianza.ipynb) | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/12_montecarlo/notebooks/02_reduccion_varianza.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> | Guiado: antithetic, control variates, importance sampling |
| 5 | Notebook de aplicación (elige uno) | — | Exploración profunda en un dominio |

### Notebooks de aplicación

Elige **uno** de los siguientes, o propón el tuyo:

| Notebook | Tema | Herramientas | Colab |
|---------|------|-------------|:-----:|
| [03 — Opciones Financieras](notebooks/aplicaciones/03_opcion_financiera.ipynb) | Pricing de opciones europeas y asiáticas con GBM | numpy, scipy | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/12_montecarlo/notebooks/aplicaciones/03_opcion_financiera.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> |
| [04 — Inferencia Bayesiana](notebooks/aplicaciones/04_inferencia_bayesiana.ipynb) | Rejection sampling, IS, preview de MCMC | numpy, scipy | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/12_montecarlo/notebooks/aplicaciones/04_inferencia_bayesiana.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> |
| [05 — Caminata Aleatoria](notebooks/aplicaciones/05_caminata_aleatoria.ipynb) | Difusión, conexión con Los Álamos, puzzle de Pólya | numpy, matplotlib | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/12_montecarlo/notebooks/aplicaciones/05_caminata_aleatoria.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> |
| [06 — Modelo de Ising](notebooks/aplicaciones/06_ising_metropolis.ipynb) | Metropolis-Hastings en su aplicación original; transiciones de fase; conexión a ML moderno | numpy, matplotlib | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/12_montecarlo/notebooks/aplicaciones/06_ising_metropolis.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> |
| [07 — Torneos Deportivos](notebooks/aplicaciones/07_torneos_deportivos.ipynb) | Simulación de Champions League con ratings Elo; suerte vs. talento; formatos de torneo | numpy, scipy | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/12_montecarlo/notebooks/aplicaciones/07_torneos_deportivos.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> |
| [08 — Epidemias Estocásticas](notebooks/aplicaciones/08_epidemias_sir.ipynb) | Modelo SIR estocástico; extinción aleatoria; inmunidad de rebaño; $R_0$ como umbral probabilístico | numpy, scipy | <a href="https://colab.research.google.com/github/sonder-art/ia_p26/blob/main/clase/12_montecarlo/notebooks/aplicaciones/08_epidemias_sir.ipynb" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Colab"></a> |

### Proponer tu propia aplicación

Si ninguno de los tres te convence, puedes proponer tu propio notebook. Requisitos mínimos:

1. **El problema** debe involucrar una integral o esperanza difícil o imposible de calcular analíticamente
2. **Verificación**: debes tener alguna forma de validar que tu estimador converge al valor correcto (solución exacta en un caso especial, límite conocido, o experimento controlado)
3. **Justificación**: explica brevemente por qué Monte Carlo es la herramienta adecuada para tu problema
4. **Alcance**: debe incluir al menos la estimación básica + análisis de convergencia + un ejercicio o extensión

## Objetivos de aprendizaje

Al terminar este módulo podrás:

1. **Explicar** el origen histórico de Monte Carlo y la controversia sobre su nombre
2. **Formular** cualquier problema de estimación como $\mathbb{E}[f(X)]$ y construir el estimador MC correspondiente
3. **Aplicar** la Ley de los Grandes Números y el Teorema Central del Límite para justificar y cuantificar el error del estimador
4. **Calcular** intervalos de confianza para estimados Monte Carlo y determinar el tamaño de muestra necesario para una precisión dada
5. **Explicar** por qué el error $O(1/\sqrt{n})$ es independiente de la dimensión y cuándo esto hace a MC superior a los métodos de cuadratura
6. **Implementar** al menos una técnica de reducción de varianza (antithetic variates, control variates o importance sampling) y verificar que reduce el error empíricamente
7. **Aplicar** Monte Carlo a un dominio concreto (finanzas, inferencia bayesiana o física estocástica)

## Prerrequisitos

| Concepto | Módulo |
|----------|--------|
| Esperanza, varianza, distribuciones | [05 — Probabilidad](../05_probabilidad/09_esperanza_momentos.md) |
| Ley de los Grandes Números | [05 — Probabilidad](../05_probabilidad/07_reglas_probabilidad.md) |
| Teorema Central del Límite | [05 — Probabilidad](../05_probabilidad/13_tlc_lgn.md) |
| Inferencia en redes bayesianas | [10 — Redes Bayesianas](../10_redes_bayesianas/03_inferencia_fuerza_bruta.md) |

## Cómo ejecutar el script de imágenes

Las imágenes en las notas se generan con `lab_montecarlo.py`:

```bash
cd clase/12_montecarlo
python3 lab_montecarlo.py
```

Dependencias: `numpy`, `matplotlib`, `scipy` (ver `requirements.txt`).
