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

## Ejemplo Completo: Reconocer Cadenas de Solo Unos

Vamos a construir paso a paso una MT que reconozca el lenguaje:

$$L = \{1^n \mid n \geq 1\} = \{1, 11, 111, 1111, ...\}$$

Es decir: acepta cadenas que contengan **solo unos** (al menos uno), rechaza cualquier otra cosa.

### Paso 1: Definición Formal de la MT

$$M_{unos} = (Q, \Sigma, \Gamma, \delta, q_0, q_{accept}, q_{reject})$$

| Componente | Valor | Explicación |
|------------|-------|-------------|
| $Q$ | $\{q_0, q_{accept}, q_{reject}\}$ | Solo 3 estados: inicial, aceptar, rechazar |
| $\Sigma$ | $\{0, 1\}$ | Alfabeto de entrada (dígitos binarios) |
| $\Gamma$ | $\{0, 1, \sqcup\}$ | Alfabeto de cinta = entrada + blanco |
| $q_0$ | $q_0$ | Estado inicial |
| $q_{accept}$ | $q_{accept}$ | Estado de aceptación |
| $q_{reject}$ | $q_{reject}$ | Estado de rechazo |

### Paso 2: Función de Transición δ

La función de transición define qué hacer en cada situación:

| Estado actual | Símbolo leído | → | Nuevo estado | Escribir | Mover |
|:-------------:|:-------------:|:-:|:------------:|:--------:|:-----:|
| $q_0$ | 1 | → | $q_0$ | 1 | R |
| $q_0$ | 0 | → | $q_{reject}$ | 0 | R |
| $q_0$ | $\sqcup$ | → | $q_{accept}$ | $\sqcup$ | R |

**En palabras:**
- Si estoy en $q_0$ y veo **1**: lo dejo igual, avanzo a la derecha, sigo en $q_0$
- Si estoy en $q_0$ y veo **0**: encontré algo que no es 1, **rechazo**
- Si estoy en $q_0$ y veo **blanco**: llegué al final sin ver ningún 0, **acepto**

### Paso 3: Diagrama de Estados

```
                    1 → 1, R
                   ┌────────┐
                   │        │
                   ▼        │
    ┌─────┐      ┌────┐     │
    │START│ ──▶  │ q₀ │ ────┘
    └─────┘      └────┘
                   │
         ┌─────────┴─────────┐
         │                   │
      0 → 0, R            □ → □, R
         │                   │
         ▼                   ▼
    ┌─────────┐       ┌──────────┐
    │ REJECT  │       │  ACCEPT  │
    └─────────┘       └──────────┘
```

### Paso 4: El Ciclo de Ejecución

En cada paso, la MT hace exactamente esto:

```
┌────────────────────────────────────────────────────┐
│  1. ¿Estoy en q_accept o q_reject?                 │
│     → SÍ: PARAR (la máquina termina)               │
│     → NO: continuar al paso 2                      │
│                                                    │
│  2. Leer el símbolo bajo el cabezal                │
│                                                    │
│  3. Buscar en la tabla δ la entrada:               │
│        δ(estado_actual, símbolo_leído)             │
│                                                    │
│  4. Ejecutar la transición encontrada:             │
│     a) Escribir el nuevo símbolo en la cinta       │
│     b) Mover el cabezal (L o R)                    │
│     c) Cambiar al nuevo estado                     │
│                                                    │
│  5. Volver al paso 1                               │
└────────────────────────────────────────────────────┘
```

### Paso 5: Ejecución que ACEPTA (entrada "111")

Notación: `estado | cinta con [cabezal]`

```
Configuración inicial:
  - Cinta: 1 1 1 □ □ □ ...
  - Cabezal: posición 0 (primer símbolo)
  - Estado: q₀

Paso 0: q₀ | [1] 1  1  □
        Busco δ(q₀, 1) = (q₀, 1, R)
        → Escribo 1 (sin cambio), muevo R, voy a q₀

Paso 1: q₀ |  1 [1] 1  □
        Busco δ(q₀, 1) = (q₀, 1, R)
        → Escribo 1, muevo R, voy a q₀

Paso 2: q₀ |  1  1 [1] □
        Busco δ(q₀, 1) = (q₀, 1, R)
        → Escribo 1, muevo R, voy a q₀

Paso 3: q₀ |  1  1  1 [□]
        Busco δ(q₀, □) = (q_accept, □, R)
        → Escribo □, muevo R, voy a q_accept

Paso 4: q_accept | ...
        ¡PARAR! Estado de aceptación alcanzado.

═══════════════════════════════════════════════════
RESULTADO: ACEPTA ✓
La cadena "111" pertenece al lenguaje L.
═══════════════════════════════════════════════════
```

### Paso 6: Ejecución que RECHAZA (entrada "101")

```
Configuración inicial:
  - Cinta: 1 0 1 □ □ □ ...
  - Cabezal: posición 0
  - Estado: q₀

Paso 0: q₀ | [1] 0  1  □
        Busco δ(q₀, 1) = (q₀, 1, R)
        → Escribo 1, muevo R, voy a q₀

Paso 1: q₀ |  1 [0] 1  □
        Busco δ(q₀, 0) = (q_reject, 0, R)
        → Escribo 0, muevo R, voy a q_reject

Paso 2: q_reject | ...
        ¡PARAR! Estado de rechazo alcanzado.

═══════════════════════════════════════════════════
RESULTADO: RECHAZA ✗
La cadena "101" NO pertenece al lenguaje L.
═══════════════════════════════════════════════════
```

### Paso 7: Código Equivalente en Python

Esta MT es equivalente a este programa:

```python
def MT_unos(entrada):
    """
    Máquina de Turing que acepta cadenas de solo unos.
    Retorna True (acepta) o False (rechaza).
    """
    # Preparar la cinta: entrada + blancos infinitos
    cinta = list(entrada) + ['□'] * 100  # simulamos infinito
    cabezal = 0
    estado = 'q0'
    
    while True:
        # Paso 1: ¿Estado de parada?
        if estado == 'q_accept':
            return True   # ACEPTA
        if estado == 'q_reject':
            return False  # RECHAZA
        
        # Paso 2: Leer símbolo
        simbolo = cinta[cabezal]
        
        # Paso 3 y 4: Aplicar transición según δ
        if estado == 'q0':
            if simbolo == '1':
                # δ(q0, 1) = (q0, 1, R)
                cinta[cabezal] = '1'  # escribir
                cabezal += 1          # mover R
                estado = 'q0'         # nuevo estado
            elif simbolo == '0':
                # δ(q0, 0) = (q_reject, 0, R)
                cinta[cabezal] = '0'
                cabezal += 1
                estado = 'q_reject'
            elif simbolo == '□':
                # δ(q0, □) = (q_accept, □, R)
                cinta[cabezal] = '□'
                cabezal += 1
                estado = 'q_accept'

# Pruebas
print(MT_unos("111"))   # True  (acepta)
print(MT_unos("1"))     # True  (acepta)
print(MT_unos("101"))   # False (rechaza)
print(MT_unos("0"))     # False (rechaza)
print(MT_unos("110"))   # False (rechaza)
```

### Paso 8: ¿Por Qué Este Ejemplo es Importante?

Este ejemplo simple ilustra **todos** los conceptos clave:

| Concepto | En este ejemplo |
|----------|-----------------|
| **Estados** | Solo 3 estados bastan para decidir |
| **Transiciones** | Tabla δ con 3 reglas |
| **Lectura** | Lee un símbolo a la vez |
| **Movimiento** | Siempre mueve R (muy simple) |
| **Aceptación** | Llegar a $q_{accept}$ |
| **Rechazo** | Llegar a $q_{reject}$ |
| **Determinismo** | Cada (estado, símbolo) tiene exactamente UNA transición |

**Observación:** Esta MT siempre termina — nunca entra en loop infinito. Esto es porque siempre avanza a la derecha y eventualmente encuentra el blanco.

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
