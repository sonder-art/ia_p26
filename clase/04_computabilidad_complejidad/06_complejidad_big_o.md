---
title: "Complejidad Computacional y Big-O"
---

# Complejidad Computacional y Big-O

De "¿se puede resolver?" a "¿cuán rápido podemos resolverlo?"

## Introducción: La Pregunta de Eficiencia

Hasta ahora hemos estudiado **computabilidad**: ¿qué problemas podemos resolver en principio?

Ahora cambiamos de pregunta: Para problemas que **SÍ** son decidibles, ¿cuánto tiempo toma resolverlos?

**Ejemplos:**

| Problema | ¿Decidible? | ¿Eficiente? |
|----------|-------------|-------------|
| Ordenar n números | ✓ Sí | ✓ Sí — $O(n \log n)$ |
| Buscar en lista ordenada | ✓ Sí | ✓ Sí — $O(\log n)$ |
| Problema del Viajante | ✓ Sí | ✗ No — $O(n! )$ o peor |
| SAT (módulo anterior) | ✓ Sí | ? Desconocido (probablemente exponencial) |
| Halting Problem | ✗ No | N/A — ni siquiera decidible |

**La realidad:** Decidible ≠ Práctico

---

## Recursos Computacionales

Cuando ejecutamos un algoritmo, consume **recursos**:

### 1. Tiempo

**Pregunta:** ¿Cuántos pasos ejecuta el algoritmo?

**Depende de:** Tamaño de la entrada $n$

**Ejemplos:**
- Buscar en lista no ordenada: $n$ comparaciones en el peor caso
- Quicksort: $n \log n$ comparaciones en promedio
- Generar todas las permutaciones: $n!$ operaciones

---

### 2. Espacio

**Pregunta:** ¿Cuánta memoria usa el algoritmo?

**Ejemplos:**
- Buscar en lista: $O(1)$ — solo necesito índice actual
- Mergesort: $O(n)$ — necesito array auxiliar
- Recursión profunda: $O(n)$ — stack de llamadas

---

### 3. Otros Recursos (menos comunes)

- **Número de procesadores** (computación paralela)
- **Ancho de banda** (computación distribuida)
- **Energía** (computación móvil/verde)

**En este curso:** Nos enfocamos en **tiempo** principalmente.

---

## Análisis Asintótico: Big-O y Familia

### ¿Por Qué Asintótico?

No nos importa el tiempo **exacto** (depende de hardware, implementación, constantes).

Nos importa el **comportamiento cuando $n \to \infty$** (escala).

**Ejemplo:** ¿Qué algoritmo es mejor?

- Algoritmo A: $100n$ operaciones
- Algoritmo B: $n^2$ operaciones

Para $n$ pequeño (n=10): A toma 1000, B toma 100 → **B es mejor**

Para $n$ grande (n=10000): A toma 1,000,000, B toma 100,000,000 → **A es mejor**

**Conclusión:** Para entradas grandes, el **crecimiento** importa más que las constantes.

---

## Notación Big-O (O mayúscula)

### Definición Formal

Decimos que $f(n) = O(g(n))$ si existen constantes $c > 0$ y $n_0 > 0$ tales que:

$$f(n) \leq c \cdot g(n) \quad \forall n \geq n_0$$

**En palabras:** $f$ crece **a lo más** tan rápido como $g$ (salvo constantes).

**Intuición:** $g$ es un **límite superior** para el crecimiento de $f$.

---

### Ejemplo: Probar que $3n^2 + 5n + 2 = O(n^2)$

**Queremos mostrar:** Existe $c$ y $n_0$ tales que $3n^2 + 5n + 2 \leq c \cdot n^2$ para todo $n \geq n_0$.

**Idea:** Para $n$ grande, el término $n^2$ domina.

**Prueba:**

Para $n \geq 1$:
- $5n \leq 5n^2$ (pues $n \leq n^2$)
- $2 \leq 2n^2$ (pues $1 \leq n^2$)

Por lo tanto:
$$3n^2 + 5n + 2 \leq 3n^2 + 5n^2 + 2n^2 = 10n^2$$

Elegimos $c = 10$ y $n_0 = 1$.

**Conclusión:** $3n^2 + 5n + 2 = O(n^2)$ ✓

---

### Propiedades de Big-O

1. **Constantes no importan:** $O(5n) = O(n)$

2. **Términos menores no importan:** $O(n^2 + n) = O(n^2)$

3. **Transitividad:** Si $f = O(g)$ y $g = O(h)$, entonces $f = O(h)$

4. **Suma:** $O(f) + O(g) = O(\max(f, g))$

5. **Producto:** $O(f) \cdot O(g) = O(f \cdot g)$

---

## Otras Notaciones Asintóticas

### Big-Omega (Ω): Límite Inferior

$$f(n) = \Omega(g(n))$$

Significa: $f$ crece **al menos** tan rápido como $g$.

**Definición formal:** Existen $c > 0$ y $n_0$ tales que $f(n) \geq c \cdot g(n)$ para todo $n \geq n_0$.

**Uso:** Probar que un problema **requiere** al menos cierto tiempo.

**Ejemplo:** Ordenar por comparaciones es $\Omega(n \log n)$ — no existe algoritmo más rápido (en el peor caso).

---

### Big-Theta (Θ): Límite Ajustado

$$f(n) = \Theta(g(n))$$

Significa: $f$ y $g$ crecen **al mismo ritmo**.

**Definición formal:** $f = O(g)$ Y $f = \Omega(g)$.

Es decir, $c_1 \cdot g(n) \leq f(n) \leq c_2 \cdot g(n)$ para constantes $c_1, c_2 > 0$ y $n \geq n_0$.

**Uso:** Cuando conocemos el comportamiento exacto (salvo constantes).

**Ejemplo:** Buscar en lista no ordenada es $\Theta(n)$ — necesitas revisar todos los elementos.

---

### Little-o (o): Límite Estricto Superior

$$f(n) = o(g(n))$$

Significa: $f$ crece **estrictamente más lento** que $g$.

**Definición:** $\lim_{n \to \infty} \frac{f(n)}{g(n)} = 0$

**Ejemplo:** $n = o(n^2)$ pero $n \neq o(n)$.

---

### Resumen de Notaciones

| Notación | Significado | Relación |
|----------|-------------|----------|
| $f = O(g)$ | $f$ crece a lo más como $g$ | $f \leq g$ (asintóticamente) |
| $f = \Omega(g)$ | $f$ crece al menos como $g$ | $f \geq g$ (asintóticamente) |
| $f = \Theta(g)$ | $f$ crece igual que $g$ | $f = g$ (asintóticamente) |
| $f = o(g)$ | $f$ crece estrictamente menos que $g$ | $f < g$ (asintóticamente) |

**En la práctica:** Big-O es la más usada (por simplicidad).

---

## Jerarquía de Complejidades Comunes

De más rápido a más lento:

| Notación | Nombre | Ejemplo |
|----------|--------|---------|
| $O(1)$ | **Constante** | Acceder array por índice |
| $O(\log n)$ | **Logarítmica** | Búsqueda binaria |
| $O(\sqrt{n})$ | **Raíz** | Verificar si n es primo (método naive) |
| $O(n)$ | **Lineal** | Buscar en lista no ordenada |
| $O(n \log n)$ | **Lineal-logarítmica** | Quicksort, Mergesort |
| $O(n^2)$ | **Cuadrática** | Bubble sort, inserción |
| $O(n^3)$ | **Cúbica** | Multiplicación de matrices naive |
| $O(2^n)$ | **Exponencial** | Subconjuntos, muchos problemas NP |
| $O(n!)$ | **Factorial** | Generar permutaciones, TSP brute-force |

---

### Comparación Práctica

Para $n = 1000$:

| Complejidad | Operaciones | Tiempo (1 GHz) |
|-------------|-------------|----------------|
| $O(1)$ | 1 | 1 nanosegundo |
| $O(\log n)$ | ~10 | 10 nanosegundos |
| $O(n)$ | 1,000 | 1 microsegundo |
| $O(n \log n)$ | ~10,000 | 10 microsegundos |
| $O(n^2)$ | 1,000,000 | 1 milisegundo |
| $O(n^3)$ | 1,000,000,000 | 1 segundo |
| $O(2^n)$ | ~$10^{301}$ | **Edad del universo × $10^{280}$** |
| $O(n!)$ | ~$10^{2567}$ | **Imposible** |

**Observación clave:** La diferencia entre $O(n^3)$ y $O(2^n)$ es **astronómica**.

---

## Ejemplos de Análisis

### Ejemplo 1: Búsqueda Lineal

```python
def buscar(lista, objetivo):
    for i in range(len(lista)):
        if lista[i] == objetivo:
            return i
    return -1
```

**Análisis:**
- Peor caso: objetivo no está → revisamos $n$ elementos
- Complejidad: $O(n)$

---

### Ejemplo 2: Búsqueda Binaria

```python
def buscar_binaria(lista, objetivo):
    izq, der = 0, len(lista) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if lista[medio] == objetivo:
            return medio
        elif lista[medio] < objetivo:
            izq = medio + 1
        else:
            der = medio - 1
    return -1
```

**Análisis:**
- En cada iteración, reducimos el espacio de búsqueda a la mitad
- Número de iteraciones: $\log_2 n$
- Complejidad: $O(\log n)$

---

### Ejemplo 3: Bubble Sort

```python
def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        for j in range(n - i - 1):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
```

**Análisis:**
- Loop externo: $n$ iteraciones
- Loop interno: $n - i$ iteraciones
- Total: $\sum_{i=0}^{n-1} (n-i) = n + (n-1) + ... + 1 = \frac{n(n+1)}{2} = O(n^2)$
- Complejidad: $O(n^2)$

---

### Ejemplo 4: Mergesort

```python
def mergesort(lista):
    if len(lista) <= 1:
        return lista
    medio = len(lista) // 2
    izq = mergesort(lista[:medio])
    der = mergesort(lista[medio:])
    return merge(izq, der)

def merge(izq, der):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] < der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado
```

**Análisis:**
- Dividimos el problema en 2 subproblemas de tamaño $n/2$
- Merge toma $O(n)$
- Recurrencia: $T(n) = 2T(n/2) + O(n)$
- Por el Master Theorem: $T(n) = O(n \log n)$

---

### Ejemplo 5: Generar Todos los Subconjuntos

```python
def subconjuntos(lista):
    if not lista:
        return [[]]
    resto = subconjuntos(lista[1:])
    with_first = [[lista[0]] + s for s in resto]
    return resto + with_first
```

**Análisis:**
- Número de subconjuntos: $2^n$
- Cada uno toma $O(n)$ para construir
- Complejidad: $O(n \cdot 2^n)$

---

## El Master Theorem (Herramienta Útil)

Para recurrencias de la forma:

$$T(n) = aT(n/b) + f(n)$$

Donde:
- $a \geq 1$ (número de subproblemas)
- $b > 1$ (factor de reducción)
- $f(n)$ (costo de dividir/combinar)

**Resultado:**

1. Si $f(n) = O(n^{\log_b a - \epsilon})$ para algún $\epsilon > 0$:
   $$T(n) = \Theta(n^{\log_b a})$$

2. Si $f(n) = \Theta(n^{\log_b a})$:
   $$T(n) = \Theta(n^{\log_b a} \log n)$$

3. Si $f(n) = \Omega(n^{\log_b a + \epsilon})$ y $af(n/b) \leq cf(n)$ para $c < 1$:
   $$T(n) = \Theta(f(n))$$

---

### Ejemplos con Master Theorem

**Mergesort:** $T(n) = 2T(n/2) + O(n)$
- $a = 2, b = 2, f(n) = n$
- $\log_b a = \log_2 2 = 1$
- $f(n) = n = \Theta(n^1)$ → Caso 2
- **Resultado:** $T(n) = \Theta(n \log n)$ ✓

**Búsqueda Binaria:** $T(n) = T(n/2) + O(1)$
- $a = 1, b = 2, f(n) = 1$
- $\log_b a = \log_2 1 = 0$
- $f(n) = 1 = \Theta(n^0)$ → Caso 2
- **Resultado:** $T(n) = \Theta(\log n)$ ✓

**Multiplicación de Karatsuba:** $T(n) = 3T(n/2) + O(n)$
- $a = 3, b = 2, f(n) = n$
- $\log_b a = \log_2 3 \approx 1.585$
- $f(n) = n = O(n^{1.585 - \epsilon})$ → Caso 1
- **Resultado:** $T(n) = \Theta(n^{1.585})$ — ¡Mejor que $O(n^2)$!

---

## Complejidad en el Mejor/Peor/Promedio Caso

Algoritmos pueden comportarse diferente según la entrada:

### Quicksort

```python
def quicksort(lista):
    if len(lista) <= 1:
        return lista
    pivot = lista[0]
    menores = [x for x in lista[1:] if x < pivot]
    mayores = [x for x in lista[1:] if x >= pivot]
    return quicksort(menores) + [pivot] + quicksort(mayores)
```

**Análisis:**

- **Mejor caso:** Pivot siempre divide en mitades iguales → $O(n \log n)$
- **Peor caso:** Pivot siempre es el mínimo/máximo → $O(n^2)$
- **Caso promedio:** En promedio, particiones razonables → $O(n \log n)$

**En la práctica:** Quicksort es muy rápido (caso promedio) con pivote aleatorio.

---

## Complejidad Espacial

Además del tiempo, el **espacio** (memoria) también importa:

**Ejemplos:**

| Algoritmo | Tiempo | Espacio |
|-----------|--------|---------|
| Búsqueda lineal | $O(n)$ | $O(1)$ |
| Búsqueda binaria (iterativa) | $O(\log n)$ | $O(1)$ |
| Búsqueda binaria (recursiva) | $O(\log n)$ | $O(\log n)$ — stack |
| Mergesort | $O(n \log n)$ | $O(n)$ — array auxiliar |
| Quicksort | $O(n \log n)$ | $O(\log n)$ — stack |
| Bubble sort | $O(n^2)$ | $O(1)$ — in-place |

**Trade-off:** A veces más espacio permite menos tiempo (memoización, tablas hash).

---

## Clases de Complejidad Temporal

Ahora que entendemos Big-O, podemos clasificar problemas:

### Tiempo Polinomial

Un problema está en **PTIME** si existe un algoritmo que lo resuelve en $O(n^k)$ para alguna constante $k$.

**Ejemplos:**
- Buscar: $O(n)$ ✓
- Ordenar: $O(n \log n)$ ✓
- Multiplicar matrices: $O(n^3)$ ✓
- Camino más corto (Dijkstra): $O(n^2)$ ✓

**Considerado "eficiente"** (aunque $O(n^{100})$ sería horrible en la práctica).

---

### Tiempo Exponencial

Un problema requiere tiempo **exponencial** si el mejor algoritmo conocido es $O(2^{poly(n)})$ o peor.

**Ejemplos:**
- Subconjuntos: $O(2^n)$
- TSP brute-force: $O(n!)$
- SAT naive: $O(2^n)$

**Generalmente impracticable** para $n$ grande.

---

## Límites Inferiores

**Pregunta:** ¿Cuál es el algoritmo **más rápido posible** para un problema?

**Límite inferior:** Prueba de que **ningún** algoritmo puede ser más rápido que cierta cota.

### Ejemplos de Límites Inferiores

**1. Ordenar por comparaciones: $\Omega(n \log n)$**

**Argumento (árbol de decisión):**
- Cualquier algoritmo basado en comparaciones puede representarse como árbol de decisión
- Hay $n!$ permutaciones posibles
- Árbol binario con $n!$ hojas tiene altura $\geq \log_2(n!) = \Omega(n \log n)$
- **Conclusión:** Mergesort y Heapsort son **óptimos**

**2. Buscar en lista no ordenada: $\Omega(n)$**

**Argumento:** En el peor caso, el elemento puede estar en cualquier posición → debes revisar todos.

---

## Complejidad Amortizada

A veces, una operación costosa ocurre **raramente**, y el **costo promedio** es bajo.

### Ejemplo: Dynamic Array (ArrayList)

```python
class DynamicArray:
    def __init__(self):
        self.array = [None] * 1
        self.size = 0
        
    def append(self, x):
        if self.size == len(self.array):
            self._resize()  # Copiar a array 2x más grande
        self.array[self.size] = x
        self.size += 1
```

**Análisis:**
- La mayoría de `append`: $O(1)$
- Cada potencia de 2, `resize`: $O(n)$ (copiar $n$ elementos)

**Costo amortizado:** $O(1)$ por inserción (en promedio sobre secuencia)

**Prueba informal:**
- Insertar $n$ elementos requiere resize en $n=1, 2, 4, 8, ...$
- Costo total: $n + (1 + 2 + 4 + ... + n) \leq n + 2n = O(n)$
- Costo por inserción: $O(n) / n = O(1)$ ✓

---

## Resumen

| Concepto | Definición | Uso |
|----------|------------|-----|
| **Big-O** | Límite superior asintótico | "A lo más tan rápido" |
| **Big-Ω** | Límite inferior asintótico | "Al menos tan rápido" |
| **Big-Θ** | Límite ajustado | "Exactamente tan rápido" |
| **Polinomial** | $O(n^k)$ | Generalmente eficiente |
| **Exponencial** | $O(2^n)$ o peor | Generalmente impracticable |
| **Límite inferior** | Prueba de dificultad inherente | "Ningún algoritmo puede ser mejor" |

**Punto clave:** Complejidad asintótica predice escalabilidad — ¿qué pasa cuando $n \to \infty$?

---

**Siguiente:** [Clases: P, NP y BPP →](07_p_np_bpp.md)
