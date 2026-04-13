---
title: "Aplicaciones"
---

# Aplicaciones de las cadenas de Markov

> *"Markov chains are everywhere — once you know what to look for, you see them in language, markets, biology, and algorithms."*

---

Las secciones anteriores construyeron la teoría: definimos las cadenas, identificamos las propiedades que garantizan buen comportamiento (irreducibilidad, aperiodicidad), y demostramos que las cadenas ergódicas convergen a su distribución estacionaria. Ahora mostramos por qué todo eso importa. Las tres aplicaciones de esta sección — lenguaje, finanzas, y PageRank — ilustran cómo una idea creada para ganar un argumento sobre Dios se convirtió en herramienta central de la ciencia y la industria modernas.

---

## 1. Modelado de lenguaje: de vocales a GPT

En la sección 01, vimos que Markov analizó las alternancias entre vocales y consonantes en *Eugenio Oneguin*. Ese fue el primer modelo de lenguaje basado en dependencias secuenciales. Aquí extendemos esa idea para entender cómo las cadenas de Markov generan texto, y por qué esa misma lógica subyace a los modelos de lenguaje modernos.

### La jerarquía de la estructura

Consideremos el alfabeto español (27 símbolos: a-z más espacio) y comparemos cuatro niveles de modelado:

**Nivel 0 — Letras aleatorias.** Cada letra se elige uniformemente al azar, sin considerar frecuencias ni contexto. Resultado típico:

> xqmzb plfrt jwkdg...

Ilegible. No hay estructura alguna.

**Nivel 1 — Frecuencias de letras.** Cada letra se muestrea según su frecuencia empírica en español: la "e" aparece ~13% del tiempo, la "a" ~12%, la "z" ~0.5%. No hay dependencia entre letras consecutivas — cada una se genera de forma independiente. Resultado típico:

> eaanio stlrd oecus...

Mejor — las letras comunes dominan — pero no hay estructura silábica ni patrones reconocibles.

**Nivel 2 — Cadena de Markov (orden 1).** Cada letra se genera condicionada en la letra *anterior*. Usamos una matriz de transición $\mathbf{P}$ de $27 \times 27$, estimada contando bigramas en texto real en español:

$$p_{ij} = \frac{\text{número de veces que la letra } j \text{ sigue a la letra } i}{\text{número total de apariciones de la letra } i}$$

Resultado típico:

> en de la contr espa...

Notablemente mejor. Las secuencias son reconocibles como fragmentos de español: las consonantes se combinan con vocales de forma natural, los espacios aparecen en posiciones razonables, y emergen fragmentos que parecen palabras reales.

**Nivel 3 — Cadena de orden superior.** Condicionamos en las 2 (o más) letras anteriores, denotando $X_t$ la letra en la posición $t$:

$$P(X_t \mid X_{t-1}, X_{t-2})$$

El texto generado es aún más legible: aparecen palabras completas reconocibles, la estructura silábica es casi perfecta, y ocasionalmente se forman frases con sentido parcial.

### La conexión con Shannon

Claude Shannon, en su artículo fundacional *A Mathematical Theory of Communication* (1948), usó **exactamente esta jerarquía** — cadenas de Markov sobre caracteres — para definir los conceptos de **entropía** y **redundancia** del lenguaje inglés.

Shannon demostró que conforme se incluye más contexto (más letras anteriores en la condición), el texto generado se vuelve más predecible y la **entropía por carácter** disminuye:

$$H_0 > H_1 > H_2 > \cdots$$

donde $H_k$ es la entropía del modelo de orden $k$. La diferencia $H_0 - H_k$ mide la **redundancia** que introduce la estructura del lenguaje. Cuanto más contexto incluimos, más predecible (menor entropía) se vuelve la siguiente letra.

### De Markov a GPT

Los modelos de lenguaje modernos (GPT, Claude) son la extensión extrema de la idea de Markov: en vez de condicionar en 1 o 2 caracteres anteriores, condicionan en **miles de tokens previos**. La arquitectura es radicalmente diferente — redes neuronales con miles de millones de parámetros en lugar de una matriz de transición — pero el principio matemático fundamental es el mismo: **las dependencias secuenciales crean estructura, y esa estructura permite predicción**.

Markov lo demostró con vocales y consonantes en 1913. Shannon lo formalizó con entropía en 1948. Los modelos de lenguaje modernos lo llevan al extremo — pero la intuición subyacente es la misma.

---

## 2. Finanzas: modelos de cambio de régimen

Los mercados financieros no tienen un solo comportamiento — alternan entre **regímenes** con características distintas:

| Régimen | Retornos | Volatilidad | Sentimiento |
|---------|----------|-------------|-------------|
| **Alcista (Bull)** | Positivos | Baja | Confianza |
| **Bajista (Bear)** | Negativos | Alta | Miedo |
| **Lateral (Flat)** | Pequeños | Media | Incertidumbre |

Modelamos estos regímenes como una cadena de Markov con tres estados. La matriz de transición se estima a partir de datos históricos:

| | Alcista | Bajista | Lateral |
|---|:---:|:---:|:---:|
| **desde Alcista** | 0.70 | 0.15 | 0.15 |
| **desde Bajista** | 0.10 | 0.65 | 0.25 |
| **desde Lateral** | 0.20 | 0.15 | 0.65 |

Esta cadena es irreducible (cualquier régimen puede alcanzar cualquier otro) y aperiódica (los valores diagonales son positivos), por lo que el teorema ergódico aplica. La distribución estacionaria nos da información práctica sobre el comportamiento a largo plazo del mercado.

### Aplicaciones del teorema ergódico

**Fracciones de largo plazo.** La distribución estacionaria $\pi$ indica qué fracción del tiempo el mercado pasa en cada régimen. Resolviendo $\pi \mathbf{P} = \pi$ (sistema de ecuaciones lineales, mismo procedimiento que en la sección 03) obtenemos:

$$\pi \approx (0.34,\; 0.30,\; 0.36)$$

Interpretación: a largo plazo, el mercado es alcista ~34% del tiempo, bajista ~30%, y lateral ~36%. El mercado no es permanentemente alcista ni bajista — todos los regímenes ocurren con frecuencias estables.

**Duración esperada de un régimen.** Si la probabilidad de permanecer en el estado Bear es $p = P(\text{Bear} \to \text{Bear}) = 0.65$, entonces la duración esperada de un periodo bajista es:

$$\mathbb{E}[\text{duración Bear}] = \frac{1}{1 - p} = \frac{1}{1 - 0.65} = \frac{1}{0.35} \approx 2.9 \text{ meses}$$

Esto se deduce de que la duración en un estado sigue una distribución geométrica: en cada paso, la cadena permanece con probabilidad $p$ y sale con probabilidad $1 - p$.

**Retorno promedio de largo plazo.** Si $r_j$ es el retorno promedio mensual en el régimen $j$, el teorema ergódico garantiza que el retorno promedio de largo plazo es:

$$\mathbb E_\pi(\text{retorno}) = \sum_{j \in S} \pi_j \cdot r_j$$

Por ejemplo, con $r_{\text{Bull}} = +2\%$, $r_{\text{Bear}} = -3\%$, $r_{\text{Flat}} = +0.2\%$:

$$\mathbb{E}_\pi[\text{retorno}] = 0.34 \times 2 + 0.30 \times (-3) + 0.36 \times 0.2 = 0.68 - 0.90 + 0.072 = -0.148\%$$

**Evaluación de riesgo a mediano plazo.** "Estamos en un mercado alcista. ¿Cuál es la probabilidad de estar en un mercado bajista dentro de 6 meses?" La respuesta es directa:

$$P(X_6 = \text{Bear} \mid X_0 = \text{Bull}) = (\mathbf{P}^6)[\text{Bull}, \text{Bear}]$$

Calculamos la sexta potencia de la matriz de transición y leemos la entrada correspondiente. El poder de la formulación matricial es que preguntas complejas sobre el futuro se reducen a multiplicación de matrices.

---

## 3. PageRank: la cadena de Markov de mil millones de dólares

En 1998, Larry Page y Sergey Brin — entonces estudiantes de doctorado en Stanford — propusieron modelar la World Wide Web como una cadena de Markov gigante. La idea era elegante:

- **Estados** = páginas web (miles de millones).
- **Transiciones** = hipervínculos. Si una página tiene $k$ enlaces salientes, el "navegante aleatorio" elige cada enlace con probabilidad $1/k$.
- Un navegante aleatorio recorre la web haciendo clic en enlaces al azar.

Hay un problema técnico: la web no es irreducible. Existen páginas sin enlaces salientes ("sumideros") y conjuntos de páginas que forman ciclos aislados. Para garantizar ergodicidad, Page y Brin añadieron un mecanismo de **teletransporte**: en cada paso, con probabilidad $\alpha = 1 - d$ (donde $d \approx 0.85$ es el **factor de amortiguamiento**), el navegante ignora los enlaces y salta a una página completamente aleatoria. Con probabilidad $d$, sigue un enlace de la página actual. Esto hace la cadena irreducible y aperiódica.

La **distribución estacionaria** $\pi$ de esta cadena modificada es el **PageRank** de cada página. Una página con $\pi_i$ alto es "importante" — no porque alguien lo declare, sino porque la estructura de enlaces de toda la web converge a darle ese peso. Las páginas importantes son aquellas a las que apuntan muchas otras páginas, o aquellas a las que apuntan páginas importantes (la definición es recursiva, exactamente como $\pi = \pi \mathbf{P}$).

Google calculaba el PageRank usando **iteración de potencias**: empezar con una distribución arbitraria y multiplicar repetidamente por $\mathbf{P}$ hasta convergencia. El teorema ergódico garantiza que este proceso converge, independientemente de la distribución inicial. El mismo teorema que Markov demostró para ganar un argumento sobre Dios — que los promedios de secuencias dependientes convergen — se convirtió en el fundamento matemático de una empresa que hoy vale más de un billón de dólares.

---

## 4. Conexiones y referencias futuras

Las cadenas de Markov no son un destino final — son un punto de partida. Cada una de las tres extensiones siguientes nace de una pregunta natural sobre lo que hemos visto.

### Modelos Ocultos de Markov (HMMs, Módulo 20)

En el ejemplo de regímenes financieros, *asumimos* que podíamos observar directamente si el mercado estaba en modo alcista, bajista, o lateral. Pero en la realidad, el régimen es invisible — solo observamos los retornos, la volatilidad, el volumen. ¿Qué pasa si el estado de la cadena está **oculto** y solo tenemos acceso a observaciones ruidosas generadas por ese estado?

Eso es un **Modelo Oculto de Markov**: una cadena de Markov invisible que genera observaciones visibles. El desafío es inferir la secuencia de estados ocultos a partir de las observaciones — un problema que tiene soluciones elegantes (el algoritmo de Viterbi, el algoritmo forward-backward) y aplicaciones que van desde reconocimiento de voz hasta genómica.

### MCMC (Sección 06)

Hemos visto que toda cadena ergódica converge a su distribución estacionaria única $\pi$. El teorema ergódico lo garantiza. Pero ¿qué pasa si **invertimos la pregunta**? Dada una distribución objetivo $\pi$, ¿podemos **construir** una cadena de Markov que converja exactamente a ella?

Si la respuesta es sí, entonces podemos **muestrear** de cualquier distribución — incluso de distribuciones que no podemos normalizar, como las posteriores bayesianas. Eso es **MCMC: Markov Chain Monte Carlo**. En lugar de recibir una cadena y calcular su estacionaria, *diseñamos* la cadena para que su estacionaria sea la distribución que nos interesa. Esta idea conecta directamente con el Módulo 12 (Monte Carlo) y es el tema de la siguiente sección.

### Procesos de Decisión de Markov (MDPs)

En todo lo que hemos visto, la matriz de transición $\mathbf{P}$ es fija: el sistema evoluciona según probabilidades que no controlamos. Pero ¿qué pasa si podemos **elegir** qué transiciones seguir? En cada estado, elegimos una **acción**, y cada acción tiene su propia matriz de transición. Elegir la mejor acción en cada estado — la **política óptima** — es el problema central de un **Proceso de Decisión de Markov**.

Los MDPs son el fundamento matemático del **aprendizaje por refuerzo** (reinforcement learning): un agente interactúa con un entorno markoviano, elige acciones, recibe recompensas, y aprende la política que maximiza la recompensa acumulada. De las cadenas de Markov pasivas a los agentes que toman decisiones — el mismo marco matemático, con una capa de control encima.

---

**[← Teorema Ergódico](04_teorema_ergodico.md)** · **Siguiente:** [MCMC →](06_mcmc.md)
