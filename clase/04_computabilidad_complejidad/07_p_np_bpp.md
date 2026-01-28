---
title: "Clases de Complejidad: P, NP y BPP"
---

# Clases de Complejidad: P, NP y BPP

La jerarquía de dificultad computacional.

## Introducción: Clasificando Problemas por Dificultad

Ya sabemos usar Big-O para analizar algoritmos **específicos**. Ahora clasificamos **problemas** según su dificultad inherente.

**Pregunta central:** ¿Qué tan difícil es este problema en el mejor caso posible?

---

## Repaso: Lenguajes de Decisión

Recordemos que estudiamos problemas de decisión (respuesta sí/no):

**Formato estándar:** $L = \{x \mid x \text{ satisface la propiedad } P\}$

**Ejemplos:**
- $\text{SORTED} = \{\langle L \rangle \mid L \text{ está ordenada}\}$
- $\text{CONNECTED} = \{\langle G \rangle \mid G \text{ es un grafo conexo}\}$
- $\text{SAT} = \{\langle \phi \rangle \mid \phi \text{ es una fórmula satisfacible}\}$

**Nota:** Problemas de optimización se pueden reducir a decisión:
- Optimización: "¿Cuál es el tour más corto?"
- Decisión: "¿Existe un tour de longitud $\leq k$?"

---

## La Clase P (Polynomial Time)

### Definición

$$\mathbf{P} = \{L \mid L \text{ es decidible en tiempo polinomial por una MT determinista}\}$$

**En palabras:** P contiene todos los problemas que podemos resolver **eficientemente**.

**Formalmente:** Existe una MT determinista y una constante $k$ tal que decide $L$ en tiempo $O(n^k)$.

---

### Ejemplos en P

✅ **1. Búsqueda**
- Problema: ¿$x$ está en la lista $L$?
- Algoritmo: Recorrer la lista
- Complejidad: $O(n)$ ✓

✅ **2. Ordenamiento**
- Problema: Ordenar lista $L$
- Algoritmo: Mergesort
- Complejidad: $O(n \log n)$ ✓

✅ **3. Conectividad en Grafos**
- Problema: ¿Hay camino de $u$ a $v$ en grafo $G$?
- Algoritmo: BFS o DFS
- Complejidad: $O(V + E)$ ✓

✅ **4. Camino Más Corto**
- Problema: ¿Distancia de $u$ a $v$ es $\leq k$?
- Algoritmo: Dijkstra
- Complejidad: $O(V^2)$ o $O(E \log V)$ ✓

✅ **5. Matching en Grafos Bipartitos**
- Problema: ¿Existe matching perfecto?
- Algoritmo: Ford-Fulkerson
- Complejidad: $O(VE)$ ✓

✅ **6. Aritmética**
- Sumar, restar, multiplicar, dividir
- Complejidad: Polinomial en el tamaño de los bits

✅ **7. Programación Lineal**
- Optimizar función lineal con restricciones lineales
- Algoritmo: Elipsoide (Khachiyan 1979)
- Complejidad: Polinomial ✓

---

### Propiedades de P

**Cerrado bajo:**
- ✓ Unión: Si $L_1, L_2 \in \mathbf{P}$ → $L_1 \cup L_2 \in \mathbf{P}$
- ✓ Intersección: $L_1 \cap L_2 \in \mathbf{P}$
- ✓ Complemento: $\overline{L} \in \mathbf{P}$
- ✓ Concatenación, estrella de Kleene, etc.

**P es robusta:**
- Equivalente para MT multi-cinta, RAM, etc.
- Las diferencias son solo constantes multiplicativas

---

## La Clase NP (Nondeterministic Polynomial Time)

### Definición (Vía Verificación)

$$\mathbf{NP} = \{L \mid L \text{ tiene un verificador polinomial}\}$$

**Verificador:** Algoritmo $V$ tal que:

$$x \in L \iff \exists \text{ certificado } c \text{ tal que } V(x, c) = \text{acepta}$$

Y $V$ corre en tiempo polinomial en $|x|$.

---

### Intuición: "Fácil de Verificar"

**Idea:** Resolver el problema puede ser difícil, pero **verificar** una solución propuesta es fácil.

**Analogía:**
- **Resolver sudoku:** Difícil (puede requerir backtracking)
- **Verificar sudoku resuelto:** Fácil (revisar filas/columnas/bloques)

---

### Definición Alternativa (MT No Determinista)

$$\mathbf{NP} = \{L \mid L \text{ es decidible en tiempo polinomial por una MT no determinista}\}$$

**MT No Determinista:** Puede "adivinar" la respuesta correcta.
- Si existe secuencia de elecciones que lleva a aceptar → acepta
- Corre en tiempo polinomial si todas las ramas terminan en tiempo polinomial

**Equivalencia:** Certificado $c$ = secuencia de elecciones no deterministas

---

### Ejemplos en NP

✅ **1. SAT (Satisfacibilidad Booleana)**
- **Problema:** ¿Existe asignación que satisface $\phi$?
- **Certificado:** Una asignación $A$
- **Verificación:** Evaluar $\phi$ con $A$ → $O(n)$ ✓
- (Vimos esto en el módulo de Lógica)

✅ **2. CLIQUE**
- **Problema:** ¿$G$ tiene un clique de tamaño $\geq k$?
- **Certificado:** Un conjunto $C$ de $k$ vértices
- **Verificación:** Revisar que todo par en $C$ es adyacente → $O(k^2)$ ✓

✅ **3. SUBSET-SUM**
- **Problema:** ¿Existe subconjunto que suma exactamente $k$?
- **Certificado:** El subconjunto
- **Verificación:** Sumar elementos → $O(n)$ ✓

✅ **4. HAMILTONIAN-PATH**
- **Problema:** ¿$G$ tiene un camino hamiltoniano?
- **Certificado:** Una secuencia de vértices
- **Verificación:** Revisar que es camino válido y visita todos → $O(n)$ ✓

✅ **5. TSP (Decisión)**
- **Problema:** ¿Existe tour de longitud $\leq k$?
- **Certificado:** Una permutación de ciudades
- **Verificación:** Calcular longitud del tour → $O(n)$ ✓

✅ **6. 3-COLORING**
- **Problema:** ¿$G$ es 3-coloreable?
- **Certificado:** Una coloración de vértices
- **Verificación:** Revisar que aristas no conectan mismo color → $O(E)$ ✓

✅ **7. COMPOSITES (números compuestos)**
- **Problema:** ¿$n$ es compuesto?
- **Certificado:** Un factor no trivial $p$
- **Verificación:** Dividir $n$ por $p$ → polinomial ✓

---

### P ⊆ NP

**Teorema:** $\mathbf{P} \subseteq \mathbf{NP}$

**Prueba:** Si $L \in \mathbf{P}$, existe algoritmo polinomial que lo decide.

Construir verificador:
```
V(x, c):  // c es ignorado
    Ejecutar algoritmo para L en x
    Aceptar sii algoritmo acepta
```

Este es un verificador polinomial → $L \in \mathbf{NP}$ ✓

**Intuición:** Si puedes resolver algo rápido, también puedes verificarlo rápido (¡ignora el certificado!).

---

## La Clase NP-Completo

### Reducciones Polinomiales

Decimos que $L_1 \leq_p L_2$ ($L_1$ se reduce a $L_2$) si existe una función $f$ computable en tiempo polinomial tal que:

$$x \in L_1 \iff f(x) \in L_2$$

**Intuición:** Si puedes resolver $L_2$, puedes resolver $L_1$ (transformando la entrada).

---

### Definición de NP-Completo

Un lenguaje $L$ es **NP-completo** si:

1. $L \in \mathbf{NP}$
2. Para todo $L' \in \mathbf{NP}$: $L' \leq_p L$

**En palabras:** $L$ es al menos tan difícil como **cualquier** problema en NP.

**Consecuencia:** Si encontramos algoritmo polinomial para **un** problema NP-completo, entonces $\mathbf{P} = \mathbf{NP}$.

---

### El Primer Problema NP-Completo

**Teorema de Cook-Levin (1971):** **SAT es NP-completo**.

**Idea de la prueba:**
1. SAT está en NP (ya vimos)
2. Para cualquier $L \in \mathbf{NP}$:
   - $L$ tiene MT no determinista $M$ que corre en tiempo polinomial
   - Dada entrada $x$, construir fórmula $\phi_{M,x}$ que es satisfacible sii $M$ acepta $x$
   - $\phi_{M,x}$ codifica: estados, transiciones, aceptación
   - Construcción toma tiempo polinomial
3. Por lo tanto, $L \leq_p \text{SAT}$ para todo $L \in \mathbf{NP}$ → SAT es NP-completo ✓

---

### Otros Problemas NP-Completos

Una vez que SAT es NP-completo, podemos probar que otros problemas también lo son mediante reducciones:

**Patrón:**
1. Tomar problema NP-completo conocido (ej: SAT)
2. Reducirlo al nuevo problema
3. El nuevo problema es NP-completo

**Ejemplos NP-Completos:**

| Problema | Reducción desde |
|----------|----------------|
| 3-SAT | SAT |
| CLIQUE | 3-SAT |
| VERTEX-COVER | CLIQUE |
| HAMILTONIAN-PATH | VERTEX-COVER |
| TSP | HAMILTONIAN-PATH |
| 3-COLORING | 3-SAT |
| SUBSET-SUM | VERTEX-COVER |
| KNAPSACK | SUBSET-SUM |

**Miles de problemas** son NP-completos — aparecen en scheduling, optimización, biología, criptografía, etc.

---

### Consecuencias de NP-Completitud

Si un problema es NP-completo:

❌ **Probablemente no hay algoritmo polinomial** (asumiendo $\mathbf{P} \neq \mathbf{NP}$)

✅ **Soluciones prácticas:**
1. **Heurísticas** — Algoritmos que funcionan bien en promedio (sin garantías)
2. **Aproximación** — Solución cercana al óptimo con garantías
3. **Casos especiales** — Restricciones que lo hacen polinomial
4. **Exponencial mejorado** — $O(1.5^n)$ en lugar de $O(2^n)$

**Ejemplo (TSP):**
- **Exacto:** Exponencial
- **Heurística:** Nearest neighbor (rápido, sin garantías)
- **Aproximación:** Christofides (garantiza ≤ 1.5 × óptimo)
- **Casos especiales:** TSP métrico, euclidiano

---

## P vs NP: El Problema del Millón

### La Pregunta

$$\mathbf{P} \stackrel{?}{=} \mathbf{NP}$$

**En palabras:** ¿Resolver es tan fácil como verificar?

---

### Estado Actual

✓ **Lo que sabemos:**
- $\mathbf{P} \subseteq \mathbf{NP}$ (demostrado)
- Hay miles de problemas NP-completos
- Nadie ha encontrado algoritmo polinomial para ningún problema NP-completo
- Nadie ha probado que no existe tal algoritmo

❓ **Lo que NO sabemos:**
- Si $\mathbf{P} = \mathbf{NP}$ o $\mathbf{P} \neq \mathbf{NP}$

---

### Creencia de la Comunidad

**~99% de expertos creen: $\mathbf{P} \neq \mathbf{NP}$**

**Razones:**
1. 50+ años de intentos sin éxito
2. Miles de problemas NP-completos, ninguno resuelto eficientemente
3. Diferencia fundamental entre "encontrar" y "verificar" parece profunda

**Pero:** No hay prueba. Es posible que $\mathbf{P} = \mathbf{NP}$.

---

### Implicaciones si P = NP

Si alguien encuentra algoritmo polinomial para SAT (o cualquier problema NP-completo):

**🚀 Revoluciones positivas:**
- Criptografía rota (pero también nuevos algoritmos)
- Optimización perfecta (scheduling, rutas, diseño)
- Avances en biología (protein folding)
- IA super-poderosa (aprendizaje óptimo)
- Matemáticas automatizadas (encontrar pruebas)

**💥 Consecuencias negativas:**
- Seguridad de internet colapsaría
- RSA, criptografía actual inútil
- Necesitaríamos nuevos sistemas de seguridad

**Opinión mayoritaria:** Probablemente no sucederá.

---

### Implicaciones si P ≠ NP

**Confirmación de límites:**
- Hay problemas inherentemente difíciles
- No todo es optimizable
- Algunas cosas requieren heurísticas

**Para la práctica:** Continuar como ahora (ya asumimos esto).

---

## La Clase BPP (Bounded-Error Probabilistic Polynomial)

### Motivación: Algoritmos Probabilísticos

Algunos problemas son más fáciles si permitimos **aleatorización**:

**Ejemplo:** ¿Es $n$ primo?
- **Determinista:** Algoritmo AKS (2002) — polinomial pero lento: $O((\log n)^{12})$
- **Probabilístico:** Miller-Rabin — $O(k (\log n)^3)$ con error $\leq 2^{-k}$

Para $k = 100$: error $< 2^{-100}$ (esencialmente 0) y **mucho más rápido**.

---

### Definición de BPP

$$\mathbf{BPP} = \{L \mid L \text{ decidible en tiempo polinomial probabilístico con error acotado}\}$$

**Formalmente:** Existe MT probabilística $M$ que corre en tiempo polinomial tal que:

$$\begin{cases}
x \in L \implies P[M \text{ acepta } x] \geq 2/3 \\
x \notin L \implies P[M \text{ rechaza } x] \geq 2/3
\end{cases}$$

**Notas:**
- Error $\leq 1/3$ en ambas direcciones
- Podemos reducir error a $2^{-k}$ repitiendo $O(k)$ veces
- Constante 2/3 es arbitraria (cualquier $> 1/2$ funciona)

---

### Tipos de Algoritmos Probabilísticos

**1. Monte Carlo**
- Tiempo polinomial **siempre**
- Puede dar respuesta incorrecta con probabilidad baja

**Ejemplo:** Miller-Rabin para primalidad

**2. Las Vegas**
- Respuesta **siempre correcta**
- Tiempo esperado polinomial (puede tomar más tiempo raramente)

**Ejemplo:** Quicksort con pivote aleatorio

**BPP:** Enfocado en Monte Carlo.

---

### Ejemplos en BPP

✅ **1. Primality Testing**
- Algoritmo: Miller-Rabin
- Error: $\leq 2^{-k}$ en $k$ rondas
- Complejidad: $O(k (\log n)^3)$ ✓

✅ **2. Polynomial Identity Testing**
- Problema: ¿$P(x) \equiv 0$ para polinomio multivariado?
- Algoritmo: Evaluar en puntos aleatorios (Schwartz-Zippel)
- Error: Pequeño
- Aplicación: Verificar multiplicación de matrices

✅ **3. Aproximación de #SAT**
- Contar número de asignaciones satisfactorias
- Algoritmo: Sampleo Monte Carlo
- Da aproximación con alta probabilidad

---

### Relaciones entre Clases

```
    ┌─────────────────┐
    │      NP         │
    │                 │
    │    ┌──────┐     │
    │    │ BPP? │     │
    │    └──┬───┘     │
    │       │         │
    └───────┼─────────┘
            │
        ┌───▼──┐
        │  P   │
        └──────┘
```

**Lo que sabemos:**
- $\mathbf{P} \subseteq \mathbf{BPP}$ (algoritmo determinista = probabilístico con error 0)
- $\mathbf{BPP} \subseteq \mathbf{NP}$ (probablemente, no demostrado)

**Conjetura mayoritaria:** $\mathbf{P} = \mathbf{BPP}$

**Razones:**
- Todos los problemas en BPP conocidos tienen algoritmos deterministas (después de mucho esfuerzo)
- Derandomización parece posible en general
- Pero no hay prueba

**Implicación:** La aleatoriedad quizás no añade poder computacional, solo **eficiencia práctica**.

---

### BPP en la Práctica

**Ventajas de algoritmos probabilísticos:**
- ✓ Más simples
- ✓ Más rápidos
- ✓ Más fáciles de paralelizar

**Desventajas:**
- ✗ No garantía absoluta de corrección
- ✗ Dependen de aleatoriedad de calidad

**En la práctica:** Ampliamente usados (hashing, ML, criptografía, simulaciones).

---

## Otras Clases de Complejidad (Breve Mención)

### PSPACE

$$\mathbf{PSPACE} = \{L \mid L \text{ decidible en espacio polinomial}\}$$

**Ejemplos:**
- Juegos (ajedrez, Go en tableros n×n)
- Quantified Boolean Formulas (QBF)

**Relaciones:**
$$\mathbf{P} \subseteq \mathbf{NP} \subseteq \mathbf{PSPACE}$$

---

### EXPTIME

$$\mathbf{EXPTIME} = \{L \mid L \text{ decidible en tiempo } 2^{poly(n)}\}$$

**Ejemplos:**
- Algunos juegos generalizados
- Lógica de primer orden

**Sabemos:** $\mathbf{P} \neq \mathbf{EXPTIME}$ (¡esto SÍ está demostrado!)

Pero no sabemos si $\mathbf{NP} \neq \mathbf{EXPTIME}$ o $\mathbf{P} \neq \mathbf{PSPACE}$.

---

### La Jerarquía Completa

```
┌──────────────────────────────┐
│     No Computable            │
│  (ej: Halting Problem)       │
└──────────────────────────────┘
          ↑
┌──────────────────────────────┐
│      Computable              │
│                              │
│  ┌────────────────────┐      │
│  │   EXPTIME          │      │
│  │                    │      │
│  │  ┌──────────────┐  │      │
│  │  │   PSPACE     │  │      │
│  │  │              │  │      │
│  │  │  ┌────────┐  │  │      │
│  │  │  │   NP   │  │  │      │
│  │  │  │  ┌───┐ │  │  │      │
│  │  │  │  │ P │ │  │  │      │
│  │  │  │  └───┘ │  │  │      │
│  │  │  └────────┘  │  │      │
│  │  └──────────────┘  │      │
│  └────────────────────┘      │
└──────────────────────────────┘
```

**Sabemos:** $\mathbf{P} \subseteq \mathbf{NP} \subseteq \mathbf{PSPACE} \subseteq \mathbf{EXPTIME}$

**NO sabemos:** Si alguna contención es estricta (excepto $\mathbf{P} \neq \mathbf{EXPTIME}$).

---

## Resumen

| Clase | Definición | Intuición | Ejemplos |
|-------|-----------|-----------|----------|
| **P** | Decidible en tiempo polinomial determinista | "Eficientemente resoluble" | Ordenar, búsqueda, caminos |
| **NP** | Verificable en tiempo polinomial | "Fácil de verificar" | SAT, TSP, Clique |
| **NP-Completo** | Los más difíciles de NP | "Si resuelves uno, resuelves todos" | SAT, TSP, 3-Color |
| **BPP** | Decidible probabilísticamente con error acotado | "Rápido con aleatoriedad" | Primalidad, PIT |

**La gran pregunta:** ¿$\mathbf{P} = \mathbf{NP}$? ($1,000,000 para quien la resuelva)

---

**Siguiente:** [Síntesis Final →](08_sintesis.md)
