# Videos Cadena de Markov

## The Strange Math That Predicts (Almost) Anything

Nekrasov decía que el libre albedrío no era solo una idea filosófica, sino algo que se podía medir casi científicamente. Markov no estaba de acuerdo: para él, no tenía sentido ligar la independencia matemática con el libre albedrío. Entonces quiso probar que eventos dependientes también podían seguir la ley de los grandes números.

Lo probó con texto. Tomó las primeras 20,000 letras de *Eugene Onegin* de Pushkin, quitó espacios y puntuación, y contó cuántas eran vocales y cuántas consonantes: 43% vocales y 57% consonantes. Luego armó pares superpuestos de letras y vio cuatro casos: **vv, vc, cv y cc**. Si las letras fueran independientes, **vv** debería salir como **0.43**, o sea **18%**, pero en realidad salía solo **6%**. Ahí mostró que sí había dependencia.

Después construyó una especie de máquina de predicción con dos estados: **vocal** y **consonante**. Calculó transiciones como **0.06 / 0.43 = 0.13** para pasar de vocal a vocal, y **0.87** para vocal a consonante. Repitió el proceso muchas veces y, aunque al principio brincaba mucho, al final convergía otra vez a **43%** y **57%**. Con eso mostró que sí se puede hacer probabilidad con eventos dependientes.

---

## Hidden Markov Model: Data Science Concepts

El video explica que en un **Hidden Markov Model** hay *key definitions*: **transition probabilities**, **hidden states**, **emissions** y **observed states**. Los **hidden states** son variables que no observamos directamente, mientras que los **observed states** sí los podemos ver. La idea central es que **the hidden states directly affect the observed states**. En el ejemplo, el *mood* de la profesora es el estado oculto y el color de su camisa es el estado observado.

Después, si vemos una secuencia de colores, queremos encontrar qué secuencia de *moods* la explica mejor. Por eso buscamos la **combination that gives you the highest probability**, y entonces **we maximize the combination of the observed states and the hidden states**. Esa probabilidad conjunta primero se escribe de forma grande, pero luego se simplifica con dos ideas: cada observación depende solo del estado oculto de ese momento, y por la **Markov assumption**, cada estado oculto depende solo del estado anterior. Así, el modelo se vuelve una multiplicación de transiciones y emisiones que permite encontrar la secuencia oculta más probable.
