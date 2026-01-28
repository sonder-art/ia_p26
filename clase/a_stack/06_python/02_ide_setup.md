:::homework{id="A.6.2" title="Configurar extensión Python y venv" due="2026-01-28" points="0"}

Instala la extensión de Python en Cursor, crea un entorno virtual con `python3 -m venv venv` y verifica que el intérprete correcto está seleccionado.

:::

# Configuración de Python en Cursor/VSCode

Para programar cómodamente, necesitamos que nuestro editor nos ayude con colores, autocompletado y detección de errores.

## 1. Instalar la Extensión de Python

1.  Abre Cursor.
2.  Ve a la pestaña de **Extensions** (el icono de los cuadritos o `Ctrl+Shift+X`).
3.  Busca "Python".
4.  Instala la extensión oficial de **Microsoft** (la que tiene millones de descargas).
    *   *Nota:* Esto habilita la inteligencia para Python (Pylance).

## 2. Entornos Virtuales (Virtual Environments)

En Python, es buena práctica aislar las librerías de cada proyecto para que no choquen entre sí. Usamos `venv`.

### Pasos para crear un entorno:

1.  Abre la terminal en Cursor (`Ctrl + ~`).
2.  Asegúrate de estar en la carpeta de tu proyecto.
3.  Ejecuta:
    ```bash
    python3 -m venv venv
    ```
    *   Esto crea una carpeta llamada `venv/` (o `.venv/`) que contiene un Python aislado.

### Pasos para activar el entorno en Cursor:

1.  Una vez creada la carpeta `venv`:
2.  Presiona `Ctrl + Shift + P` (Command Palette).
3.  Escribe: `Python: Select Interpreter`.
4.  Selecciona la opción que dice `venv` o `Recommended`.
    *   Debería decir algo como `Python 3.x.x ('venv': venv)`.

> **Prompt para LLM:**
> "Acabo de crear un entorno virtual con `python3 -m venv venv`. ¿Cómo hago que Cursor use este entorno automáticamente para ejecutar mi código y para el autocompletado? Explícame cómo seleccionar el intérprete."

## 3. Verificar que funciona

Crea un archivo `prueba.py` y escribe:

```python
import sys
print(sys.executable)
```

Al ejecutarlo (botón de "Play" arriba a la derecha), la ruta que imprime debería terminar en `.../venv/bin/python`, no en `/usr/bin/python`.

