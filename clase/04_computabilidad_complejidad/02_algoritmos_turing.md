---
title: "Algoritmos y Máquinas de Turing"
---

# Algoritmos y Máquinas de Turing

El modelo fundamental de computación que define qué es computable.

## ¿Qué es un Algoritmo?

Intuitivamente, un **algoritmo** es:

> Un procedimiento paso a paso, preciso y finito, que toma una entrada y produce una salida.

**Características informales:**
1. **Finito** — Descripción de longitud finita (no infinitas instrucciones)
2. **Determinista** — Cada paso está completamente especificado
3. **Efectivo** — Cada paso es ejecutable mecánicamente
4. **Entrada/Salida** — Toma datos y produce resultados
5. **Eventualmente termina** — ...o al menos, eso esperamos

**Ejemplos cotidianos:**
- Receta de cocina
- Instrucciones de IKEA
- Algoritmo de ordenamiento
- Tu rutina matutina

**Problema:** Esta definición es vaga. ¿Cómo la hacemos **precisa**?

**Solución:** Alan Turing (1936) propuso un modelo matemático formal.

---

## La Máquina de Turing

Una **Máquina de Turing** (MT) es el modelo matemático más simple de computación que captura todo lo que podemos hacer con una computadora.

### Intuición: Una Computadora Minimalista

Imagina:
- Una **cinta infinita** dividida en celdas (la memoria)
- Un **cabezal lector/escritor** que puede moverse izquierda/derecha
- Un **conjunto finito de estados** (como un programa con un contador de programa)
- Una **función de transición** (las instrucciones del programa)

```
                 ┌─────┐
                 │  q₁ │  ← Estado actual
                 └──┬──┘
                    ↓
    ... □ │ a │ b │ b │ a │ □ │ □ ...
                    ↑
                 cabezal
```

En cada paso:
1. Lee el símbolo bajo el cabezal
2. Basándose en el estado actual y el símbolo leído:
   - Escribe un nuevo símbolo (o el mismo)
   - Mueve el cabezal izquierda (L) o derecha (R)
   - Cambia a un nuevo estado

**¡Eso es todo!** Y con esto podemos simular cualquier computadora.

---

### Definición Formal

Una **Máquina de Turing** es una 7-tupla:

$$M = (Q, \Sigma, \Gamma, \delta, q_0, q_{accept}, q_{reject})$$

Donde:

| Componente | Descripción |
|------------|-------------|
| $Q$ | Conjunto **finito** de estados |
| $\Sigma$ | Alfabeto de **entrada** (no incluye el símbolo blanco) |
| $\Gamma$ | Alfabeto de la **cinta** ($\Sigma \subseteq \Gamma$, incluye el símbolo blanco $\sqcup$) |
| $\delta$ | **Función de transición**: $Q \times \Gamma \to Q \times \Gamma \times \{L, R\}$ |
| $q_0$ | Estado **inicial** ($q_0 \in Q$) |
| $q_{accept}$ | Estado de **aceptación** |
| $q_{reject}$ | Estado de **rechazo** ($q_{reject} \neq q_{accept}$) |

**Función de transición:**

$$\delta(q, a) = (q', b, D)$$

Se lee: "Estando en estado $q$ y leyendo símbolo $a$, escribo $b$, me muevo en dirección $D$ (L o R), y cambio al estado $q'$."

**Estados especiales:**
- $q_{accept}$ y $q_{reject}$ son estados de **parada** (halting states)
- Una vez que la MT entra a uno, se detiene inmediatamente

---

## Ejemplo 1: Reconocer el Lenguaje $\{0^n1^n \mid n \geq 0\}$

**Problema:** Aceptar cadenas como "01", "0011", "000111" y rechazar "00" "011", "01010".

**Estrategia:**
1. Marcar un 0, marcar un 1
2. Repetir hasta que no queden símbolos sin marcar
3. Si todo coincide → aceptar; si no → rechazar

**Descripción informal:**

```
Estado q₀ (inicio):
  - Si veo 0 → escribo X, muevo R, voy a q₁
  - Si veo X → muevo R, quedo en q₀ (saltar Xs)
  - Si veo □ → acepto (cadena vacía)
  
Estado q₁ (buscar el 1 correspondiente):
  - Si veo 0 o X → muevo R, quedo en q₁
  - Si veo 1 → escribo Y, muevo L, voy a q₂
  - Si veo □ → rechazo (faltan 1s)
  
Estado q₂ (regresar al inicio):
  - Si veo 0, X, Y → muevo L, quedo en q₂
  - Si veo □ → muevo R, voy a q₀
  
Estado q₃ (verificar que solo quedan Ys):
  - Si veo Y → muevo R, quedo en q₃
  - Si veo □ → acepto
  - Cualquier otra cosa → rechazo
```

**Ejecución en "0011":**

```
Paso 0: q₀  [0]011      (lee 0)
Paso 1: Xq₁  0[1]1      (marcó X, busca 1)
Paso 2: Xq₁  01[1]      (sigue buscando)
Paso 3: X0q₂  Y[1]      (marcó Y, regresa)
Paso 4: Xq₂ [0]Y1       (regresando)
Paso 5: q₂ [X]0Y1       (regresando)
Paso 6: □q₀ X[0]Y1      (de vuelta al inicio)
Paso 7: □Xq₁ [0]Y1      (salta X, busca siguiente 0)
Paso 8: □XXq₁ Y[1]      (encontró Y, sigue)
Paso 9: □XXq₁ YY[□]     (encontró 1, lo marca)
... (similar, marca el último 1)
... llegamos a: □XXYY□
Paso N: acepta ✓
```

**Conclusión:** La cadena "0011" es aceptada.

---

## Ejemplo 2: Sumar 1 a un Número Binario

**Problema:** Entrada "1011" (11 en decimal) → Salida "1100" (12 en decimal)

**Estrategia:** Ir al final, sumar 1, propagar el acarreo.

**Descripción informal:**

```
q₀: Mover a la derecha hasta encontrar el blanco
q₁: Empezar a sumar desde el dígito menos significativo
    - Si veo 1 → escribo 0, muevo L (acarreo)
    - Si veo 0 → escribo 1, acepto (sin acarreo)
    - Si veo □ → escribo 1, acepto (acarreo al inicio)
```

**Ejecución en "1011":**

```
Paso 0: q₀ [1]011       (moverse al final)
Paso 1: q₀ 1[0]11
Paso 2: q₀ 10[1]1
Paso 3: q₀ 101[1]
Paso 4: q₀ 1011[□]      (fin de cadena)
Paso 5: q₁ 101[1]       (sumar 1)
Paso 6: q₁ 10[1]0       (acarreo: 1+1=10)
Paso 7: q₁ 1[0]00       (acarreo: 1+1=10)
Paso 8: q₁ [1]100       (sin acarreo: 0+1=1)
Resultado: 1100 ✓
```

---

## Ejemplo 3: Copiar una Cadena

**Problema:** Entrada "ab" → Salida "ab#ab" (copiar la cadena después de un separador)

**Estrategia:** 
1. Marcar un símbolo del input
2. Moverlo al final
3. Regresar
4. Repetir

Esta MT necesitaría varios estados para:
- Recordar qué símbolo estamos copiando
- Navegar entre el origen y el destino
- Marcar qué ya copiamos

(Dejamos los detalles como ejercicio — ¡el patrón es similar!)

---

## ¿Por Qué las Máquinas de Turing?

### Ventajas del Modelo

1. **Simplicidad matemática** — Fácil de analizar formalmente
2. **Poder expresivo** — Puede simular cualquier computadora
3. **Modelo de referencia** — Para comparar otros modelos

### Tesis de Church-Turing

> **Informal:** Todo lo que intuitivamente llamamos "computable" puede ser computado por una Máquina de Turing.

Esta NO es una afirmación matemática demostrable — es una **tesis** sobre la naturaleza de la computación.

**Evidencia a favor:**
- Todos los modelos propuestos (λ-calculus, funciones recursivas, Python, Java, ...) son equivalentes a MTs
- Nadie ha encontrado un modelo más poderoso que sea "razonable"
- 90 años sin contraejemplos

**Implicación:** Si no puede hacerse en una MT, no es computable por ninguna computadora.

---

## Variantes de Máquinas de Turing

Existen muchas variantes de MTs, pero todas tienen el **mismo poder expresivo**:

### MT con Múltiples Cintas

En lugar de una cinta, tiene $k$ cintas independientes.

**¿Más poderosa?** NO — se puede simular con una cinta (multiplexando)

**¿Más rápida?** SÍ — puede ser cuadráticamente más rápida

---

### MT No Determinista

En cada paso, puede tener **múltiples** transiciones posibles (como "adivinar").

$$\delta: Q \times \Gamma \to \mathcal{P}(Q \times \Gamma \times \{L, R\})$$

Acepta si **existe** alguna secuencia de elecciones que lleva a $q_{accept}$.

**¿Más poderosa?** NO — una MT determinista puede simularla (explorando todas las ramas)

**¿Más rápida?** ¡Quizás! Este es el problema **P vs NP**

---

### MT Enumeradora

En lugar de aceptar/rechazar, **imprime** strings en una cinta de salida.

**Uso:** Enumerar todos los strings de un lenguaje.

**Equivalencia:** Un lenguaje es reconocible ↔ tiene un enumerador

---

### Todas son Equivalentes

**Teorema:** MT estándar ≡ MT multi-cinta ≡ MT no determinista ≡ Enumeradores ≡ ...

Este teorema justifica usar la definición más simple (MT estándar) para estudiar computabilidad.

---

## Lenguajes y MTs

Una MT define un **lenguaje**:

$$L(M) = \{w \in \Sigma^* \mid M \text{ acepta } w\}$$

### Tres Posibles Resultados

Dada una entrada $w$, una MT puede:

1. **Aceptar** — Llega a $q_{accept}$
2. **Rechazar** — Llega a $q_{reject}$
3. **Loop** — Nunca para (se ejecuta infinitamente)

Esta tercera opción es crucial para entender los límites de la computación.

---

## ¿Tu Laptop es una Máquina de Turing?

**Casi.**

Diferencias:
- Tu laptop tiene **memoria finita** (RAM limitada)
- Una MT tiene **cinta infinita**

Formalmente:
- Tu laptop es un **autómata finito gigante** (con $2^{10^{10}}$ estados o más)
- Una MT es más poderosa en teoría

**En la práctica:** Para la mayoría de los propósitos, podemos pensar en nuestras computadoras como MTs (ignorando límites de memoria).

---

## Computación Universal

**Pregunta:** ¿Puede una MT simular otra MT?

**Respuesta:** ¡SÍ! Existe una **Máquina de Turing Universal** $U$.

$$U(\langle M \rangle, w) = M(w)$$

Donde $\langle M \rangle$ es una codificación (string) de la MT $M$.

**Implicación:** Esto es como un **intérprete** — $U$ lee la "descripción" de otra MT y la ejecuta.

**Analogía moderna:** Tu computadora puede ejecutar cualquier programa — es una "máquina universal".

**Conexión con Halting:** Esta universalidad es clave para demostrar que el Halting Problem es indecidible.

---

## Resumen

| Concepto | Descripción |
|----------|-------------|
| **Algoritmo** | Procedimiento finito, determinista, efectivo |
| **Máquina de Turing** | Modelo formal de computación (cinta + estados + transiciones) |
| **Aceptar/Rechazar/Loop** | Tres resultados posibles de una MT |
| **Church-Turing Thesis** | MTs capturan todo lo "computable" |
| **Variantes** | Multi-cinta, no determinista, etc. — todas equivalentes |
| **MT Universal** | Una MT puede simular cualquier otra MT |

**Punto clave:** Las Máquinas de Turing son el modelo fundamental que usaremos para estudiar qué es computable y qué no.

---

**Siguiente:** [Computabilidad vs Decidibilidad →](03_computabilidad_decidibilidad.md)
