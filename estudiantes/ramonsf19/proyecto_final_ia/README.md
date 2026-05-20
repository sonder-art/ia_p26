# Clasificador de Gestos de Lengua de Senas

Proyecto gratuito para clasificar gestos de lengua de senas en tiempo real usando
coordenadas espaciales de la mano en lugar de imagenes completas.

## Objetivo

El sistema usa MediaPipe Hands para extraer 21 landmarks de una mano. Cada muestra
se guarda como un vector numerico de 63 valores:

```text
label, x1, y1, z1, ..., x21, y21, z21
```

Despues se normaliza cada vector para que el modelo no dependa de la posicion ni
del tamano aparente de la mano.

## Instalacion

```bash
pip uninstall -y mediapipe
pip install -r requirements.txt
```

Si MediaPipe muestra mensajes de TensorFlow sobre `oneDNN`, puedes ignorarlos:
son avisos informativos y no detienen el programa.

Este proyecto usa la API clasica `mediapipe.solutions.hands`, por eso
`requirements.txt` fija MediaPipe en `0.10.14`.

Si la descarga de MediaPipe falla por timeout, usa un tiempo de espera mayor:

ESTO NO: 
```bash
python -m pip install --timeout 1000 --retries 10 mediapipe==0.10.14
python -m pip install -r requirements.txt
```

## Captura de datos

Captura 300 muestras por cada sena:

```bash
python data_collection.py --label A --samples 700
python data_collection.py --label B --samples 700
python data_collection.py --label C --samples 700
```

Tambien puedes capturar varias letras en una sola sesion:

```bash
python data_collection.py --labels A B C D E F G H I J K L M N O P Q R S T U V W X Y Z HOLA ADIOS BIEN MAL --samples 700
```

O todo el alfabeto:

```bash
python data_collection.py --alphabet --samples 300
```

Las muestras se agregan a `dataset.csv`. En modo de varias letras, presiona `s`
para iniciar cada letra cuando tengas la mano lista. Presiona `q` para salir antes
de terminar.

## Entrenamiento

```bash
python train_model.py
```

El script:

- lee `dataset.csv`;
- normaliza las coordenadas;
- divide los datos en 80% entrenamiento y 20% prueba;
- entrena un `RandomForestClassifier`;
- imprime `classification_report`;
- imprime matriz de confusion;
- guarda `model.joblib`.

## Borrar o corregir muestras

Para revisar cuantas muestras tienes por letra:

```bash
python manage_dataset.py --summary
```

Para borrar una letra mal capturada, por ejemplo `R`:

```bash
python manage_dataset.py --delete-label R
python data_collection.py --label R --samples 300
python train_model.py
```

Para borrar todo el dataset y empezar desde cero:

```bash
python manage_dataset.py --delete-all
python data_collection.py --alphabet --samples 300
python train_model.py
```

Las acciones de borrado crean un backup automatico como
`dataset_backup_YYYYMMDD_HHMMSS.csv`.

## App en tiempo real

```bash
streamlit run app.py
```

La app carga `model.joblib`, toma video de la webcam, detecta landmarks, normaliza
el vector y predice la sena. Si la probabilidad es menor a 85%, muestra `Incierto`
para reducir falsos positivos.

La app tambien puede formar una oracion:

- mantén una letra estable frente a la cámara hasta que se agregue al texto;
- retira la mano un momento antes de hacer la siguiente letra;
- usa `Espacio` para separar palabras;
- usa `Borrar` para corregir la ultima letra;
- usa `Limpiar` para empezar de nuevo;
- usa `Hablar gratis` para reproducir el texto como audio en el navegador;
- elige un `Tono de voz para la IA`;
- usa `Hablar con IA` para corregir el texto y generar voz natural con OpenAI.

## Voz natural con OpenAI

Esta parte requiere una API key de OpenAI y puede generar costo segun uso. No
guardes la llave dentro del codigo. Configurala en PowerShell antes de abrir la
app:

```powershell
$env:OPENAI_API_KEY="tu_api_key"
streamlit run app.py
```

La app usa OpenAI para:

- corregir el texto detectado y convertirlo en una frase natural;
- generar audio MP3 con una voz sintetica mas realista;
- expresar el mensaje con tonos como normal, alegre, triste, enojado,
  emocionado, calmado o urgente.

Variables opcionales:

```powershell
$env:OPENAI_TEXT_MODEL="gpt-4o-mini"
$env:OPENAI_TTS_MODEL="gpt-4o-mini-tts"
$env:OPENAI_TTS_VOICE="coral"
```

## Normalizacion matematica

Para cada landmark se aplica:

```text
x_i' = x_i - x_0
y_i' = y_i - y_0
z_i' = z_i - z_0
```

Donde el landmark 0 es la muneca. Luego todos los puntos se dividen entre la
distancia maxima desde el origen:

```text
p_i'' = p_i' / max(||p_j'||)
```

Esto aporta:

- invarianza por traslacion: la muneca siempre queda en `(0, 0, 0)`;
- invarianza por escala: la mano funciona igual cerca o lejos de la camara;
- datos ligeros: el modelo recibe 63 features, no pixeles.

## Argumentacion de complejidad

- El modelo no ve imagenes: clasifica la topologia 3D de la mano.
- La normalizacion estadistica reduce variaciones de posicion y escala.
- La inferencia es ligera y se ejecuta en CPU con webcam estandar.
- El umbral de 85% maneja incertidumbre y evita mostrar senas dudosas.

## Archivos principales

- `data_collection.py`: genera `dataset.csv`.
- `src/preprocessing.py`: normaliza landmarks.
- `train_model.py`: entrena y valida el clasificador.
- `app.py`: despliega la prediccion en tiempo real.
