---
title: "Gödel: Límites Lógicos y Computacionales"
---

# Teoremas de Gödel: Límites en la Lógica

Los límites de la computación tienen un análogo en las matemáticas: los Teoremas de Incompletitud de Gödel.

## Contexto: Sistemas Formales

Antes de Gödel, había una visión optimista de las matemáticas:

**Programa de Hilbert (1920s):**
> Encontrar un sistema formal que sea:
> 1. **Consistente** — No demuestra contradicciones
> 2. **Completo** — Demuestra todas las verdades matemáticas
> 3. **Decidible** — Existe un procedimiento para verificar demostraciones

**Objetivo:** Reducir toda la matemática a manipulación mecánica de símbolos.

**Resultado:** Kurt Gödel (1931) demostró que este sueño es **imposible**.

---

## ¿Qué es un Sistema Formal?

Un **sistema formal** consiste en:

1. **Alfabeto** — Símbolos básicos (variables, conectivos, cuantificadores)
2. **Gramática** — Reglas para formar fórmulas bien formadas
3. **Axiomas** — Fórmulas que asumimos verdaderas
4. **Reglas de inferencia** — Cómo derivar nuevas fórmulas de axiomas

**Ejemplos:**
- **Aritmética de Peano** (PA) — Axiomas sobre números naturales
- **Teoría de Conjuntos ZFC** — Fundamento de las matemáticas modernas
- **Lógica Proposicional** — (Ya vimos en el módulo anterior)

**Propiedad clave:** Las demostraciones son **mecánicas** — podemos verificarlas algorítmicamente.

---

## Conceptos Clave

### Consistencia

Un sistema es **consistente** si no puede demostrar contradicciones.

$$\text{Consistente} \iff \nexists \phi \text{ tal que } \vdash \phi \land \vdash \neg\phi$$

**Ejemplo:** Si podemos demostrar "2 + 2 = 4" y "2 + 2 ≠ 4", el sistema es **inconsistente** (¡inútil!).

---

### Completitud

Un sistema es **completo** si toda afirmación verdadera es demostrable.

$$\text{Completo} \iff \forall \phi: (\phi \text{ es verdadera} \implies \vdash \phi)$$

**Equivalentemente:** Para toda afirmación $\phi$, o demostramos $\phi$ o demostramos $\neg\phi$.

**Intuición:** No hay "huecos" — podemos resolver cualquier pregunta.

---

### Completitud vs Consistencia

Nota que son propiedades **diferentes**:
- **Consistente:** No demostramos cosas falsas
- **Completo:** Demostramos todas las cosas verdaderas

**El ideal:** Ambas propiedades simultáneamente.

---

## Primer Teorema de Incompletitud de Gödel

### Enunciado Formal

> **Teorema (Gödel 1931):** Sea $T$ un sistema formal consistente que incluya aritmética básica. Entonces existe una afirmación $G$ tal que:
> 
> 1. $G$ es verdadera (en el sentido semántico)
> 2. $T \nvdash G$ (T no puede demostrar G)
> 3. $T \nvdash \neg G$ (T no puede demostrar ¬G)
> 
> En otras palabras, $G$ es **verdadera pero no demostrable** en $T$.

**Nota sobre "verdadera en el sentido semántico":**
- **Verdad sintáctica:** Lo que se puede **demostrar** dentro del sistema formal $T$ (manipulando símbolos según reglas)
- **Verdad semántica:** Lo que es **realmente cierto** sobre los números naturales en el modelo estándar (la "realidad matemática")

La afirmación $G$ es verdadera semánticamente (describe correctamente los números naturales) pero no es demostrable sintácticamente (no hay secuencia de pasos que la derive de los axiomas). Esta brecha entre verdad y demostrabilidad es el corazón del teorema de Gödel.

---

### Enunciado Simplificado

> En cualquier sistema formal suficientemente potente y consistente, hay afirmaciones verdaderas que el sistema **no puede demostrar**.

**Implicación:** No existe un sistema formal que capture **todas** las verdades matemáticas.

---

### La Afirmación de Gödel: "Esta afirmación no es demostrable"

La afirmación $G$ (llamada **sentencia de Gödel**) esencialmente dice:

$$G = \text{"Esta afirmación no es demostrable en el sistema T"}$$

**Análisis:**

**Caso 1:** Supongamos que $G$ es demostrable ($T \vdash G$)
- Pero $G$ dice "no soy demostrable"
- Si es demostrable, entonces lo que dice es falso
- El sistema demuestra algo falso → **inconsistente**

**Caso 2:** Supongamos que $\neg G$ es demostrable ($T \vdash \neg G$)
- $\neg G$ dice "G es demostrable"
- Pero G no es demostrable (caso 1)
- El sistema demuestra algo falso → **inconsistente**

**Conclusión:** Si $T$ es consistente, entonces ni $G$ ni $\neg G$ son demostrables.

**Pero:** Nosotros (fuera del sistema) podemos ver que $G$ es **verdadera** — si fuera falsa, sería demostrable, lo cual crearía inconsistencia.

Por lo tanto: **$G$ es verdadera pero no demostrable** en $T$.

---

### Conexión con el Halting Problem

La demostración de Gödel es **análoga** al Halting Problem:

| Gödel | Halting |
|-------|---------|
| Sistema formal $T$ | Decididor hipotético $H$ |
| Afirmación $G$ | Máquina diagonal $D$ |
| "Esta afirmación no es demostrable" | "Esta máquina hace lo opuesto" |
| Auto-referencia en lógica | Auto-referencia en computación |
| → Incompletitud | → Indecidibilidad |

**Ambos usan la misma técnica:** Diagonalización + auto-referencia para crear un "punto ciego".

---

### Demostración Vía Computación (Sketch)

Podemos dar una demostración más moderna usando computabilidad:

**Paso 1:** Codificar demostraciones como números (Gödelización)
- Cada fórmula → número
- Cada demostración → secuencia de números

**Paso 2:** "Ser demostrable" es una propiedad **reconocible**
```python
def es_demostrable(afirmacion):
    prueba = 1
    while True:
        if es_demostracion_valida(prueba, afirmacion):
            return True
        prueba += 1
    # Nunca retorna False (puede hacer loop)
```

**Paso 3:** Si el sistema fuera completo:
- Para toda afirmación $\phi$: o $\vdash \phi$ o $\vdash \neg\phi$
- Podríamos decidir verdad en aritmética:
```python
def es_verdadero(afirmacion):
    # Buscar prueba de afirmacion o su negación (paralelo)
    if encontramos prueba de afirmacion:
        return True
    else:  # encontramos prueba de ¬afirmacion
        return False
```

**Paso 4:** Pero decidir verdad aritmética **implica decidir HALT**
- Podemos codificar "M se detiene en w" como afirmación aritmética
- Decidir esta afirmación → decidir HALT → **imposible**

**Conclusión:** El sistema no puede ser completo (si es consistente).

Esta es la **demostración de Turing** del teorema de Gödel — usa computabilidad en lugar de aritmetización.

---

### Demostración Intuitiva: El Programa Auto-Contradictorio

Aquí hay otra forma de ver el teorema, más cercana a la programación:

#### 1. El Entorno (El Sistema Formal)

Supongamos que tenemos una función `existe_prueba(afirmacion)`. Esta función es un bucle infinito que busca en la "base de datos" de todas las deducciones lógicas posibles.

- Si encuentra una prueba de que la `afirmacion` es verdadera → devuelve `True`
- Si no la encuentra → sigue buscando para siempre (nunca devuelve `False`)

#### 2. El Código: La Sentencia de Gödel

Vamos a escribir un programa llamado `G`. Su única misión es **contradecir al sistema**:

```python
def programa_G():
    """
    Este programa intenta encontrar una prueba de que 
    ÉL MISMO nunca se detendrá.
    """
    if existe_prueba("programa_G() NUNCA se detiene"):
        # Si el sistema matemático LOGRA PROBAR que yo no paro...
        return "¡Ja! Me detengo para que la prueba sea falsa."
    # Si no hay prueba, seguimos en el bucle infinito de existe_prueba()

# Ejecutamos el programa
programa_G()
```

#### 3. El Análisis de Ejecución

Aquí es donde el sistema matemático "explota". Analicemos los dos únicos casos posibles:

**Caso A: El programa G se detiene (ejecuta `return`)**

- Si se detuvo, es porque `existe_prueba` devolvió `True`
- Eso significa que el sistema matemático encontró una **prueba** de que "G nunca se detiene"
- **Contradicción:** El sistema probó algo falso (G sí se detuvo)
- **Resultado:** El sistema es **inconsistente** ✗ (ha demostrado una mentira, como decir que 2+2=5)

**Caso B: El programa G NO se detiene (bucle infinito)**

- Si nunca se detiene, la afirmación "G nunca se detiene" es **verdadera en la realidad**
- Pero para que no se detenga, `existe_prueba` tiene que estar buscando para siempre sin encontrar nada
- Eso significa que el sistema **no puede probar** que "G nunca se detiene"
- **Resultado:** Tenemos una afirmación que es **verdadera pero indemostrable** ✓

**Conclusión:**
- Si el sistema es **consistente** (no prueba falsedades) → entonces debe ser **incompleto** (hay verdades que no puede probar)
- Si el sistema es **completo** (prueba todo lo verdadero) → entonces es **inconsistente** (prueba falsedades)

No se puede tener ambas propiedades simultáneamente.

---

### ¿Por Qué Necesitamos Multiplicación? (Aritmética de Peano vs Presburger)

Un detalle técnico importante: el teorema de Gödel requiere **multiplicación**, no solo suma.

#### Aritmética de Presburger (Solo Suma)

- Operaciones: `+`, `-`, comparaciones
- **Resultado:** Es **completa** y **decidible** ✓
- **Limitación:** No puede expresar bucles ni autorreferencia

#### ¿Por Qué la Suma No Basta?

**La suma es un "triturador de información":**

Si guardas dos instrucciones: `A = 7` y `B = 3`
```
7 + 3 = 10
```

Cuando el sistema ve el `10`, la información original se ha perdido:
- ¿Era 7+3? ¿Era 5+5? ¿Era 9+1? ¿Era 6+4?
- **No hay forma de saberlo** — la suma es muchos-a-uno

**Analogía:** Es como un lenguaje de programación que solo tiene una variable entera. No puedes crear arrays, objetos ni punteros. No puedes escribir un programa que se analice a sí mismo.

---

#### ¿Por Qué la Multiplicación es Necesaria?

**La multiplicación es un "serializador" (como JSON):**

Gracias al **Teorema Fundamental de la Aritmética** (descomposición única en primos), la multiplicación preserva estructura.

Si quieres guardar `A = 7` y `B = 3`, usas potencias de primos:
```
2^7 × 3^3 = 128 × 27 = 3,456
```

El número `3,456` es un **contenedor**. Puedes recuperar exactamente los valores originales:
- Factoriza: `3,456 = 2^7 × 3^3`
- El primo `2` actúa como "dirección de memoria" de la primera instrucción
- El primo `3` es la "dirección" de la segunda
- Los exponentes (7 y 3) son los **datos** almacenados

**Ejemplo completo: Codificar código en un número**

Queremos codificar: `IF ( X == 0 )`

**Paso 1:** Asignar IDs a símbolos:

| Símbolo | ID |
|---------|:--:|
| IF | 1 |
| ( | 2 |
| X | 3 |
| == | 4 |
| 0 | 5 |
| ) | 6 |

**Paso 2:** Usar primos como "slots de memoria":

```
G = 2^1 × 3^2 × 5^3 × 7^4 × 11^5 × 13^6
```

Este número gigante (`G ≈ 1.7×10^15`) **codifica la secuencia** `[1, 2, 3, 4, 5, 6]`.

**Paso 3:** Decodificar (leer la memoria):

- ¿Qué hay en posición 1? Divide `G` entre `2` repetidamente → se puede 1 vez → ID = **1** (IF)
- ¿Qué hay en posición 2? Divide entre `3` repetidamente → se puede 2 veces → ID = **2** (()
- ¿Qué hay en posición 3? Divide entre `5` repetidamente → se puede 3 veces → ID = **3** (X)
- Y así sucesivamente...

**La clave:** Los primos no se "contaminan" entre sí. Es un sistema de archivos perfecto dentro de un número.

---

#### La Conexión con Gödel

Gödel se dio cuenta de que con multiplicación podía crear una fórmula matemática que dijera:

> "El número resultante de factorizar el número $G$ tiene la propiedad de ser indemostrable"

Como $G$ es **el número que codifica a la propia fórmula**, ¡la matemática está hablando de sí misma!

**Sin multiplicación:**
- Los números son "montones de arena" (sumas)
- No puedes construir estructuras complejas
- No hay autorreferencia posible
- ✓ **Resultado:** Sistema decidible (Aritmética de Presburger)

**Con multiplicación:**
- Los números son "piezas de LEGO"
- Puedes construir una computadora con ellas
- Esa computadora puede contener los planos de sí misma
- ✗ **Resultado:** Sistema incompleto (Teorema de Gödel)

**Gödel "programó" en 1931 usando solo factores primos** — creó el primer "código auto-reflexivo" en matemáticas.

---

### Resumen de las Demostraciones

| Enfoque | Técnica | Insight Clave |
|---------|---------|---------------|
| **Clásico (Gödel)** | Aritmetización + diagonalización | Codificar lógica en números |
| **Computacional (Turing)** | Halting Problem + reducción | Decidir verdad → decidir HALT |
| **Programático (moderno)** | Auto-contradicción en código | `programa_G()` que se contradice |
| **Por qué multiplicación** | Descomposición en primos | Preserva estructura = permite autorreferencia |

Todas estas demostraciones llegan a la misma conclusión: **la auto-referencia crea límites inevitables**.

---

## Segundo Teorema de Incompletitud de Gödel

### Enunciado Formal

> **Teorema (Gödel 1931):** Sea $T$ un sistema formal que incluya aritmética. Si $T$ es consistente, entonces $T$ **no puede demostrar** su propia consistencia.
> 
> Formalmente: Si $T$ es consistente, entonces $T \nvdash \text{Con}(T)$
> 
> donde $\text{Con}(T)$ es una afirmación que dice "T es consistente".

---

### Enunciado Simplificado

> Un sistema matemático suficientemente potente **no puede probar su propia consistencia** (asumiendo que es consistente).

**Interpretación:** Las matemáticas no pueden validarse a sí mismas — necesitas "salir" del sistema para verificar que no hay contradicciones.

---

### Intuición

**Idea:** Si $T$ pudiera probar $\text{Con}(T)$:

1. Por el Primer Teorema, existe $G$ (verdadera pero no demostrable)
2. Se puede mostrar que: $\text{Con}(T) \to G$
   - "Si T es consistente, entonces G es verdadera"
3. Si $T \vdash \text{Con}(T)$, entonces $T \vdash G$
4. Pero el Primer Teorema dice $T \nvdash G$ → **contradicción**

**Conclusión:** $T$ no puede probar su propia consistencia.

---

### Demostración Intuitiva para Programadores

Si el Primer Teorema nos decía que en todo lenguaje de programación potente **hay bugs lógicos indetectables** (verdades indemostrables), el Segundo Teorema es aún más demoledor:

> Ningún compilador puede certificar, usando sus propias reglas, que **no tiene bugs**.

Para un programador, esto significa que **no puedes escribir un unit test dentro de un sistema que garantice que el sistema mismo nunca entrará en contradicción**.

#### 1. Consistencia en Código

En programación, que un sistema sea **consistente** significa que no puede demostrar una falsedad (como `0 == 1`).

Llamemos a esto: `SISTEMA_ES_FIABLE`

#### 2. Lo que Sabemos del Primer Teorema

Del Primer Teorema aprendimos que el sistema "sabe" esta regla:

```python
# El sistema puede demostrar esta implicación:
if SISTEMA_ES_FIABLE:
    # Entonces G es verdadero (pero G no tiene prueba dentro del sistema)
    assert G_ES_VERDADERO
```

Formalmente: $\text{Con}(T) \to G$ (el sistema puede demostrar esta implicación)

#### 3. La Trampa del Segundo Teorema

**Supongamos** que el sistema intenta demostrar su propia fiabilidad:

```python
# ¿Puede el sistema ejecutar esto?
demostrar(SISTEMA_ES_FIABLE)
```

Si el sistema lograra demostrar `SISTEMA_ES_FIABLE`:

1. Como el sistema ya "sabe" que `SISTEMA_ES_FIABLE → G_ES_VERDADERO`...
2. ...entonces por Modus Ponens, el sistema tendría una **prueba de G**
3. **Pero el Primer Teorema dice que G NO tiene prueba** (si el sistema es consistente)
4. **Contradicción** ✗

#### 4. La Conclusión Inevitable

Para evitar la contradicción, el sistema tiene una única salida:

**Es incapaz de demostrar que es fiable**.

| Escenario | Resultado |
|-----------|-----------|
| Sistema **consistente** | No puede probar su propia consistencia ✓ |
| Sistema **prueba** su consistencia | Entonces es **inconsistente** (violó el Primer Teorema) ✗ |

**Paradoja:** Si logras probar que eres consistente, acabas de demostrar que eres inconsistente.

#### 5. Formulación Formal (Resumen)

Para cualquier sistema formal $T$ (como Aritmética de Peano) que sea consistente:

$$T \nvdash \text{Con}(T)$$

Donde $\text{Con}(T)$ es la sentencia "No existe prueba en $T$ de una contradicción".

**Prueba (sketch):**
1. El sistema puede demostrar: $\text{Con}(T) \to G$
2. Si el sistema demostrara $\text{Con}(T)$
3. Entonces demostraría $G$ (por Modus Ponens)
4. Pero Primer Teorema dice $T \nvdash G$
5. Contradicción → $T \nvdash \text{Con}(T)$ ✓

---

### Implicaciones para Ingeniería

#### Muerte del "Programa de Hilbert"

Este teorema destruyó el sueño de David Hilbert (1920s), quien quería encontrar una base matemática que **se probara a sí misma**.

Gödel demostró en 1931 que esto es **imposible**.

#### Para Desarrollo de Software:

**❌ Confianza ciega:**
- Si un sistema (o IA, o lenguaje) te dice: *"He verificado matemáticamente mis propias reglas y garantizo que soy 100% consistente"*
- Está **mintiendo** o es **erróneo**

**✓ Validación externa:**
- Para probar que un sistema $A$ es consistente, necesitas un sistema $B$ **más potente** que $A$
- Pero entonces necesitas $C$ para probar $B$, luego $D$ para $C$...
- **Recursión infinita** — no hay punto final

**Analogía:** Es el **Stack Overflow definitivo** de la lógica.

#### Para Verificación Formal:

Herramientas modernas de verificación (Coq, Isabelle, Lean):
- Pueden verificar propiedades de tu programa
- **NO pueden** verificar que sus propias reglas de inferencia son consistentes
- Necesitas confiar en un meta-nivel externo

#### Para IA y Machine Learning:

Un sistema de IA:
- Puede tener heurísticas para detectar errores
- **NO puede** garantizar que su propio razonamiento está libre de contradicciones
- Necesita validación externa (humana o de sistemas diferentes)

---

### Implicaciones Filosóficas

**Para las Matemáticas:**
- No hay una "demostración absoluta" de que las matemáticas son consistentes
- Confiamos en la consistencia de ZFC, pero no podemos probarlo dentro de ZFC
- Solo podemos probar consistencia usando un sistema "más fuerte" (pero entonces, ¿cómo probamos la consistencia de ese sistema?)

**Para la Lógica:**
- Los sistemas lógicos tienen "puntos ciegos" inevitables
- Hay una **jerarquía infinita** de sistemas, cada uno más potente que el anterior

**Para la Computación:**
- Análogo a que no podemos verificar universalmente si un programa tiene bugs
- Auto-verificación tiene límites fundamentales

---

## Comparación: Gödel vs Turing

| Aspecto | Teoremas de Gödel | Halting Problem |
|---------|-------------------|-----------------|
| **Campo** | Lógica matemática | Teoría de la computación |
| **Año** | 1931 | 1936 |
| **Muestra límites de** | Demostrabilidad | Decidibilidad |
| **Técnica** | Diagonalización + auto-referencia | Diagonalización + auto-referencia |
| **Resultado** | Hay verdades no demostrables | Hay problemas no decidibles |
| **Implicación** | Matemáticas incompletas | Computación limitada |

**Conexión profunda:** Ambos resultados muestran que la **auto-referencia** crea límites fundamentales e inevitables.

---

## Teorías Completas vs Incompletas

### Teorías Completas (existen, pero limitadas)

Algunos sistemas lógicos **son** completos:

1. **Lógica Proposicional**
   - Decidible y completa
   - Pero expresividad limitada (no habla de números)

2. **Aritmética de Presburger** (suma sin multiplicación)
   - Completa y decidible
   - Pero no puede expresar multiplicación

3. **Geometría Euclidiana**
   - Completa
   - Pero menos expresiva que aritmética

**Pattern:** Los sistemas completos son **menos expresivos** — no pueden hablar de aritmética completa.

---

### Teorías Incompletas (poderosas pero incompletas)

1. **Aritmética de Peano (PA)**
   - Incluye suma y multiplicación
   - Incompleta (por Gödel)
   - Pero reconocible (podemos enumerar teoremas)

2. **Teoría de Conjuntos ZFC**
   - Fundamento de matemáticas modernas
   - Incompleta
   - Muchas preguntas abiertas (Hipótesis del Continuo, etc.)

**Trade-off fundamental:** 
- Más expresividad → Incompletitud
- Completitud → Menos expresividad

---

## Ejemplos Concretos de Incompletitud

### Hipótesis del Continuo

**Afirmación:** No existe un conjunto cuyo tamaño esté estrictamente entre los naturales y los reales.

**Resultado (Gödel 1938 + Cohen 1963):** 
- La Hipótesis del Continuo es **independiente** de ZFC
- No se puede demostrar ni refutar en ZFC
- Es un ejemplo concreto de incompletitud

---

### Teorema de Goodstein

**Afirmación:** Ciertas secuencias de números (secuencias de Goodstein) eventualmente llegan a 0.

**Resultado:**
- Es **verdadero** (se puede demostrar en teoría de conjuntos)
- **NO demostrable** en aritmética de Peano
- Ejemplo explícito de afirmación verdadera pero no demostrable en PA

---

## Relación con P vs NP

**Pregunta especulativa:** ¿Es P vs NP demostrable?

Algunos investigadores conjeturan que P vs NP podría ser **independiente** de ZFC (no demostrable ni refutable).

**Argumentos:**
- Es una pregunta muy fundamental
- Ha resistido décadas de intentos
- Quizás está "más allá" de los axiomas actuales

**Contra-argumentos:**
- La mayoría de matemáticos creen que es demostrable
- Es un problema combinatorio concreto (no parece "transcendente")

**Estado actual:** No se sabe. Es posible que:
1. P ≠ NP sea demostrable
2. P = NP sea demostrable
3. Sea independiente de ZFC (requeriría nuevos axiomas)

---

## Implicaciones para IA

### ¿Pueden las máquinas hacer matemáticas?

**Pregunta:** ¿Un programa de IA puede descubrir todas las verdades matemáticas?

**Respuesta:** **No** — por Gödel, hay verdades no demostrables mecánicamente.

**Matiz:** Pero los humanos tampoco pueden descubrir todas las verdades (¡también somos computaciones!).

---

### ¿Qué significa "entender"?

**Penrose's Argument** (1989, controvertido):
- Los humanos pueden "ver" que la afirmación de Gödel es verdadera
- Las máquinas están limitadas a demostraciones formales
- Por lo tanto, los humanos no son máquinas

**Contra-argumentos:**
- Los humanos "vemos" la verdad porque operamos en un **meta-sistema**
- Una máquina en un meta-sistema también podría "verlo"
- No está claro que los humanos puedan hacer más que las máquinas

**Debate abierto:** Gödel no resuelve si la mente humana es computable o no.

---

## Resumen

| Teorema | Afirmación | Implicación |
|---------|-----------|-------------|
| **Gödel 1** | Hay verdades no demostrables | Matemáticas incompletas |
| **Gödel 2** | No puedes probar tu propia consistencia | Auto-verificación imposible |
| **Conexión con Turing** | Misma técnica (diagonalización) | Límites en lógica ≈ límites en computación |

**Filosofía:**
- Hay **límites fundamentales** al conocimiento formal
- La auto-referencia crea "puntos ciegos" inevitables
- No podemos "salir" de nuestro propio sistema para validarlo completamente

---

## Reflexión Final

Los Teoremas de Gödel y el Halting Problem muestran que:

✓ Hay **límites matemáticos** a lo que podemos demostrar

✓ Hay **límites computacionales** a lo que podemos decidir

✓ Estos límites son **profundos y relacionados** — ambos usan auto-referencia

✓ No son limitaciones de "tecnología" o "inteligencia" — son límites **lógicos** inherentes

**La paradoja hermosa:** Usamos la lógica para demostrar que la lógica tiene límites.

---

**Siguiente:** [Complejidad y Big-O →](06_complejidad_big_o.md)
