# Reflexion sobre los videos de IA

Despues de ver los videos, me quedo con la idea de que muchas tecnicas de inteligencia artificial no son magia, sino formas inteligentes de trabajar con incertidumbre. El primer video, sobre cadenas de Markov, muestra como una idea simple, que el siguiente estado puede depender del estado actual, explica aplicaciones como Monte Carlo, texto predictivo y mezcla de cartas. Me sorprendio que un concepto que empieza con contar letras en un poema ruso termine conectado con buscadores web y modelos de lenguaje.

Aprendi que la independencia no siempre es necesaria para razonar con probabilidad. Markov estudio procesos donde los eventos estan relacionados y aun asi tienen estructura suficiente para predecir. Las cadenas de Markov no intentan recordar todo el pasado, sino resumir lo relevante en el estado actual. Esa simplificacion permite modelar sistemas sin que el calculo se vuelva imposible.

El segundo video, sobre modelos ocultos de Markov, agrega una capa mas realista, muchas veces no observamos directamente el estado que nos importa, solo vemos senales. Por ejemplo, podemos observar palabras, acciones o sintomas, pero no siempre la causa interna. Ahi entran los estados ocultos, las probabilidades de transicion y las probabilidades de emision.

Lo que mas me sorprendio fue que estos modelos aparecen en problemas cotidianos como etiquetar partes de una oracion, predecir texto, decidir que pagina web es relevante o estimar un proceso fisico complejo. Tambien me llamo la atencion que la eficiencia computacional sea central. No basta con escribir la probabilidad correcta; si las combinaciones crecen demasiado, se necesitan algoritmos como forward, backward o Viterbi.

Esto conecta con el curso porque hemos visto probabilidad condicional, redes bayesianas, inferencia, busqueda y complejidad. Los modelos ocultos de Markov parecen una version secuencial de esas ideas: hay dependencias, observaciones y algo que inferir. Monte Carlo tambien se relaciona con simulacion, porque aproxima resultados cuando el calculo exacto es dificil.

Mi reflexion final es que la IA depende mucho de como representamos un problema. Elegir que cuenta como estado, que observar y que dependencias asumir cambia lo que un sistema puede aprender. Tambien queda claro que los modelos simplifican la realidad y tienen limites. Para un mini examen, recordaria tres ideas: cadenas de Markov modelan transiciones, modelos ocultos de Markov infieren estados no observables y los algoritmos eficientes permiten usar estas ideas en problemas reales.
