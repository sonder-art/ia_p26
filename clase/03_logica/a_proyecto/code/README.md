# Cascarón de Proyecto de Lógica

Este es un punto de partida para tu proyecto. Está diseñado de forma modular para separar la **Lógica de Inferencia** (Backend) de la **Interfaz de Usuario** (Frontend).

## 🚀 Cómo correr el cascarón

1.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Ejecuta la aplicación:**
    ```bash
    streamlit run app.py
    ```

## 📂 Estructura de archivos

- `logic.py`: Contiene la clase `KnowledgeBase`. Aquí es donde debes implementar los algoritmos vistos en clase (`Forward Chaining`, `Resolución`, etc.).
- `app.py`: Contiene la interfaz en Streamlit. Conecta los botones y checkboxes con los métodos de `logic.py`.
- `requirements.txt`: Lista de librerías necesarias.

## 🛠️ Instrucciones para el alumno

1.  **Define tus variables:** Usa el método `get_symbol` en `logic.py` para crear los literales de tu problema.
2.  **Carga tu KB:** En el constructor de `KnowledgeBase` o desde `app.py`, añade las reglas que definen tu mundo.
3.  **Implementa `ask`:** El motor de inferencia está vacío por ahora. Debes usar lo aprendido en el Módulo 3 para que el sistema pueda responder preguntas.
