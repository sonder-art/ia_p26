# Reflexión: Cadenas de Markov y Cadenas de Markov Ocultas

**Nombre:** Saúl  
**Curso:** Inteligencia Artificial  
**Videos:** *The Strange Math That Predicts (Almost) Anything* — Veritasium · *Hidden Markov Model: Data Science Concepts* — ritvikmath

---

## Lo que aprendí

El video de Veritasium abre con un origen histórico que no esperaba: Andrei Markov desarrolló su teoría a principios del siglo XX no por una necesidad aplicada, sino como respuesta a un debate filosófico sobre si la Ley de los Grandes Números podía extenderse a eventos dependientes. Su respuesta fue demostrar que, siempre que el siguiente estado dependa únicamente del estado actual y no de toda la historia previa del proceso, la convergencia estadística sigue garantizada. A esa condición se le llama la **propiedad de Markov** o *falta de memoria* (*memorylessness*), y es el corazón de todo el formalismo.

Lo que sigue en el video es un recorrido por aplicaciones que, a primera vista, parecen no tener nada en común. Stanislaw Ulam, atrapado en cama jugando solitario durante una convalecencia, se preguntó cuál era la probabilidad de ganar una partida concreta. No encontró forma de calcularlo analíticamente, así que propuso simularlo miles de veces y promediar los resultados: eso fue el germen del **método Monte Carlo**. Von Neumann lo adoptó para simular la difusión de neutrones en los reactores de fisión del Proyecto Manhattan, ya que el comportamiento de una partícula: colisionar, absorberse, escapar, se puede modelar como una cadena de transiciones probabilísticas entre estados.

Décadas después, Larry Page y Sergey Brin usaron exactamente la misma idea para construir **PageRank**: un navegante aleatorio que sigue hipervínculos indefinidamente convergerá, gracias a la propiedad de la cadena, a una distribución estacionaria donde cada página recibe un peso proporcional a cuánto tráfico le llegaría en el largo plazo. Ese peso es la relevancia de la página. El video también muestra cómo el **texto predictivo** funciona contando con qué frecuencia una palabra sigue a otra en grandes corpus, construyendo así una cadena de Markov sobre el lenguaje. Y un resultado que me pareció especialmente curioso: se puede demostrar matemáticamente que se necesitan **al menos siete cortes de cartas** para mezclar una baraja de forma verdaderamente aleatoria, y esa prueba también se apoya en el análisis de convergencia de cadenas de Markov.

El segundo video, de ritvikmath, extiende el marco hacia una situación más realista y más difícil: ¿qué pasa cuando los estados del sistema **no son directamente observables**? Un médico no ve el estado de salud de un paciente directamente; ve lo que el paciente hace: comer, dormir, salir a caminar. Un lingüista no observa la intención del hablante; observa las palabras. Esa brecha entre lo latente y lo observable es exactamente lo que formaliza el **Modelo de Markov Oculto (HMM)**.

Un HMM tiene tres componentes: la **matriz de transición** (con qué probabilidad pasa el sistema de un estado oculto a otro), la **matriz de emisión** (con qué probabilidad se observa cada símbolo dado un estado oculto) y la **distribución inicial** (en qué estado oculto empieza el proceso). Con esos tres ingredientes se pueden abordar tres problemas canónicos: calcular la probabilidad de una secuencia de observaciones (algoritmo *forward*), encontrar la secuencia de estados ocultos más probable que explica lo observado (algoritmo de **Viterbi**), y aprender los parámetros del modelo a partir de datos de observación (algoritmo de **Baum-Welch**, una instancia del EM).

## Lo que me sorprendió

Lo que más me impactó del primer video es la universalidad del modelo. No se trata de una herramienta especializada: el mismo formalismo que describe el salto de un neutrón entre estados energéticos también describe cómo un buscador web asigna relevancia a páginas o cómo tu teclado predice la siguiente palabra. Hay algo casi filosófico en eso: la abstracción matemática logra capturar estructuras tan distintas bajo una misma descripción.

Del video de los HMMs, lo que me sorprendió fue la elegancia con que resuelven el problema de la *observabilidad parcial*. El algoritmo de Viterbi, en particular, me resultó ingenioso: en lugar de explorar exponencialmente todas las secuencias de estados posibles, aprovecha la estructura de la cadena para descomponer el problema y resolverlo de forma eficiente con programación dinámica. Es un ejemplo bonito de cómo la estructura del modelo habilita algoritmos que de otro modo serían computacionalmente inviables.

## Conexión con el curso

Estos videos conectan con varios temas que hemos trabajado en clase. La propiedad de Markov es el fundamento de los **Procesos de Decisión de Markov (MDP)**, el marco formal del aprendizaje por refuerzo: el agente observa un estado, ejecuta una acción y transiciona estocásticamente a un nuevo estado. Que el siguiente estado no dependa de la historia completa es exactamente lo que hace tractable la ecuación de Bellman.

Los HMMs, por su parte, son un antecedente directo de los modelos modernos de procesamiento de lenguaje. Antes de los Transformers, eran el estado del arte en reconocimiento de voz y traducción automática. La tarea de decodificación, inferir la secuencia latente más probable, es análoga a lo que hacen hoy los modelos de lenguaje cuando infieren estructura semántica a partir de tokens. Además, el algoritmo Baum-Welch conecta directamente con el tema de **inferencia sobre variables latentes**: la alternancia entre estimar los estados ocultos dadas las observaciones y actualizar los parámetros dadas esas estimaciones es precisamente la estructura del algoritmo EM.

En conjunto, los dos videos me ayudaron a ver las Cadenas de Markov no como un tema aislado, sino como la columna vertebral de una familia extensa de modelos probabilísticos que atraviesa la historia de la computación y llega hasta los sistemas de IA más modernos.
