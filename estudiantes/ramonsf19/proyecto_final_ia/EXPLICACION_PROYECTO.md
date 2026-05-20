# Explicacion del Proyecto para Principiantes

## Que hace este proyecto

Este proyecto reconoce letras hechas con la mano usando una webcam. La idea es
tomar gestos de lengua de senas, convertirlos en texto y despues hacer que ese
texto se lea en voz alta.

En pocas palabras:

```text
mano frente a la camara -> letra detectada -> texto formado -> frase corregida -> voz
```

El sistema no trabaja directamente con fotos completas. En lugar de eso, detecta
los puntos importantes de la mano y usa esos puntos como numeros.

## Que tecnologias usamos

Usamos varias herramientas, cada una con una tarea especifica:

- `OpenCV`: abre la webcam y obtiene los frames de video.
- `MediaPipe Hands`: detecta la mano y obtiene 21 puntos clave.
- `NumPy`: ayuda a trabajar con los numeros de las coordenadas.
- `Pandas`: lee y organiza el archivo `dataset.csv`.
- `Scikit-Learn`: entrena el modelo que reconoce las letras.
- `RandomForestClassifier`: modelo de machine learning que aprende a clasificar.
- `Streamlit`: crea la interfaz web.
- `streamlit-webrtc`: permite usar la camara dentro de Streamlit.
- `OpenAI API`: corrige el texto y genera una voz mas natural.

## Como se guardan los datos

Cada vez que se detecta una mano, MediaPipe entrega 21 puntos. Cada punto tiene
tres coordenadas:

```text
x, y, z
```

Entonces:

```text
21 puntos * 3 coordenadas = 63 valores
```

Cada muestra se guarda asi:

```text
label, x1, y1, z1, x2, y2, z2, ..., x21, y21, z21
```

Por ejemplo, si estamos capturando la letra A:

```text
A, 0.42, 0.51, -0.02, ...
```

Ese archivo se llama `dataset.csv`.

## Por que no usamos imagenes

Usar imagenes completas seria mas pesado. Cada imagen tiene miles o millones de
pixeles. En cambio, este proyecto solo usa 63 numeros por muestra.

Eso hace que el sistema sea:

- mas rapido;
- mas ligero;
- posible de ejecutar con una computadora normal;
- mas facil de explicar matematicamente.

## La normalizacion: la parte matematica importante

Un problema es que la mano puede aparecer en diferentes lugares de la camara. A
veces esta arriba, abajo, cerca o lejos. Si usamos las coordenadas tal cual, el
modelo podria confundirse.

Para evitar eso hacemos dos pasos.

### 1. Mover la muneca al origen

El punto 0 de MediaPipe es la muneca. Restamos la posicion de la muneca a todos
los puntos.

Asi la muneca siempre queda en:

```text
(0, 0, 0)
```

Esto significa que el modelo ya no depende tanto de donde este la mano en la
pantalla.

### 2. Ajustar el tamano

Despues calculamos que tan lejos esta el punto mas lejano de la mano y dividimos
todas las coordenadas entre esa distancia.

Esto ayuda a que no importe si la mano esta cerca o lejos de la camara.

En resumen:

- mover la muneca al origen corrige la posicion;
- dividir por el tamano corrige la escala.

## Como aprende el modelo

Primero capturamos muchas muestras. Por ejemplo:

```text
300 muestras de A
300 muestras de B
300 muestras de C
...
```

Luego `train_model.py` lee `dataset.csv`, normaliza las coordenadas y entrena un
modelo llamado `RandomForestClassifier`.

Este modelo aprende patrones. Por ejemplo:

- cuando los puntos estan de cierta forma, probablemente es una A;
- cuando los dedos estan extendidos de otra forma, probablemente es una B;
- cuando la mano tiene otra posicion, puede ser una C.

El modelo no memoriza una foto. Aprende relaciones entre puntos de la mano.

## Donde entra la IA

En este proyecto hay varias partes de IA.

### IA 1: MediaPipe

MediaPipe usa modelos ya entrenados para encontrar la mano en la imagen y ubicar
sus 21 puntos clave.

Sin MediaPipe, tendriamos que detectar la mano desde cero, lo cual seria mucho
mas dificil.

### IA 2: Clasificador de letras

Nuestro modelo de Scikit-Learn aprende a reconocer letras usando los 63 valores
de cada mano.

Este es el modelo que nosotros entrenamos con nuestras propias muestras.

### IA 3: Correccion de texto con OpenAI

Cuando formamos una frase con letras, puede quedar algo como:

```text
HOLA COMO ESTAS
```

La API de OpenAI puede convertir eso en algo mas natural:

```text
Hola, ¿como estas?
```

Aqui la IA ayuda a que el texto no parezca solo letras pegadas, sino una frase
normal.

### IA 4: Voz natural con OpenAI

La voz gratis del navegador puede sonar robotica. Con OpenAI Text-to-Speech,
podemos generar una voz mas clara, natural y humana.

Esto hace que el proyecto no solo reconozca senas, sino que tambien pueda
"hablar" el mensaje.

Ademas, la app permite elegir el tono emocional de la voz, por ejemplo:

- normal;
- alegre;
- triste;
- enojado;
- emocionado;
- calmado;
- urgente.

Esto es importante porque muchas veces el mensaje no solo depende de las
palabras, sino tambien de como se dicen.

## Por que la IA es vital en este proyecto

La IA es importante porque el problema no es simplemente programar reglas.

Una mano no siempre se ve igual:

- cambia la luz;
- cambia la distancia a la camara;
- cambia el angulo;
- cambia el tamano de la mano;
- cada persona hace la sena un poco diferente.

Seria muy dificil escribir reglas manuales como:

```text
si el dedo indice esta exactamente aqui y el pulgar esta exactamente alla,
entonces es la letra A
```

Eso fallaria muy rapido.

La IA permite que el sistema aprenda ejemplos. En vez de decirle todas las reglas
a mano, le mostramos muchas muestras y el modelo aprende los patrones.

Ademas, OpenAI ayuda en la parte final:

- convierte texto crudo en frases mas naturales;
- genera voz menos robotica;
- permite expresar emocion mediante el tono de voz;
- mejora la experiencia para una persona que escucha el resultado.

## Como funciona todo el flujo

### 1. Captura de datos

Se ejecuta:

```powershell
python data_collection.py --alphabet --samples 300
```

El programa abre la camara y guarda muestras de cada letra.

### 2. Entrenamiento

Se ejecuta:

```powershell
python train_model.py
```

El programa entrena el modelo y crea:

```text
model.joblib
```

Ese archivo contiene el modelo ya aprendido.

### Corregir una letra mal capturada

Si te equivocaste al capturar una letra, por ejemplo si guardaste otra sena como
`R`, no tienes que borrar todo el proyecto.

Primero borras solo las muestras de esa letra:

```powershell
python manage_dataset.py --delete-label R
```

Luego vuelves a capturar esa letra:

```powershell
python data_collection.py --label R --samples 300
```

Y finalmente entrenas otra vez:

```powershell
python train_model.py
```

Esto es necesario porque el modelo aprende desde `dataset.csv`. Si cambias el
dataset, tambien debes regenerar `model.joblib`.

### 3. Uso en tiempo real

Se ejecuta:

```powershell
streamlit run app.py
```

La app abre una pagina web. Ahi se puede:

- detectar letras;
- formar una oracion;
- separar palabras;
- borrar errores;
- hablar con voz gratis;
- hablar con voz generada por IA.

## Que pasa cuando usamos la app

Cuando haces una sena frente a la camara:

1. OpenCV toma el frame.
2. MediaPipe detecta la mano.
3. Se extraen los 21 landmarks.
4. Se normalizan los 63 valores.
5. El modelo predice la letra.
6. Si la confianza es alta, se agrega al texto.
7. OpenAI puede corregir el texto.
8. OpenAI puede generar el audio.

## Que significa la confianza del modelo

El modelo devuelve probabilidades. Por ejemplo:

```text
A: 92%
B: 5%
C: 3%
```

Si la probabilidad es mayor o igual a 85%, el sistema acepta la letra. Si es
menor, muestra:

```text
Incierto
```

Esto evita que el sistema agregue letras equivocadas con demasiada facilidad.

## Limitaciones actuales

Este proyecto reconoce poses de la mano, no movimientos completos.

Por eso letras como `J` y `Z`, que en muchas lenguas de senas implican movimiento,
pueden ser mas dificiles. Para reconocer movimientos reales se necesitaria guardar
secuencias de frames, no solo una pose.

Tambien hay que recordar que el modelo depende de los datos capturados. Si solo
se entrena con una persona y una iluminacion, puede fallar mas con otras personas
o en otros lugares.

## Como se podria mejorar

Algunas mejoras posibles:

- capturar datos de varias personas;
- capturar con diferentes fondos e iluminaciones;
- agregar mas muestras por letra;
- reconocer palabras completas, no solo letras;
- reconocer movimientos para letras como J y Z;
- usar una red neuronal para secuencias de video;
- guardar historial de frases habladas;
- agregar traduccion a otros idiomas.

## Resumen final

Este proyecto combina vision por computadora, machine learning e IA generativa.

La camara ve la mano, MediaPipe encuentra puntos clave, Scikit-Learn reconoce la
letra, Streamlit muestra el resultado y OpenAI ayuda a convertir el texto en una
frase natural con voz realista.

Lo mas importante es que no estamos haciendo una simple app de webcam. Estamos
creando un pipeline completo:

```text
vision -> datos numericos -> normalizacion -> clasificacion -> lenguaje -> voz
```

Esa combinacion es lo que hace que el proyecto tenga mas complejidad y valor.
