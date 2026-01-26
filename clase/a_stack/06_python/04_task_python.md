:::homework{id="A.6.4" title="Script de python 101" due="2026-01-28" points="5"}

Crea un script Python con clase/función/if-else, y envía todo mediante Pull Request.

:::

# Tarea Práctica: Python Básico

Es hora de escribir código. Vas a crear tu propio script, ejecutarlo y subirlo a GitHub.

## Instrucciones Paso a Paso

### 1. Ejecuta el Ejemplo
Antes de crear el tuyo, asegúrate de que puedes correr el que te dimos.
1.  Abre la terminal en `clase/a_stack/06_python/`.
2.  Ejecuta: `python3 ejemplo_clase.py`
3.  Si funciona, ¡estás listo!

### 2. Prepara tu Rama (Git)
Como siempre, **nunca trabajamos en main**. Puedes hacerlo manual o usando nuestro script de automatización `flow.sh`.

#### Opción Automática (Recomendada)
Esta es la forma más fácil. Puedes ejecutar el comando tú mismo o pedirle a Cursor que lo haga por ti.

> **Prompt para Cursor:**
> "Por favor lee el archivo `clase/README_FLOW.md` para entender cómo funciona el script de automatización. Luego, usa el script para iniciar una nueva tarea llamada `tarea-02-python`."


#### Opción Manual
1.  Sincroniza tu repo: `git checkout main` -> `git pull upstream main`.
2.  Crea la rama: `git checkout -b tarea-02-python`.

> **Tip:** Pregúntale a Cursor: *"¿Cómo uso el script flow.sh para iniciar una nueva tarea llamada tarea-02-python?"*

### 3. Crea tu Archivo
1.  Ve a tu carpeta personal: `cd estudiantes/tu_usuario/`.
2.  Crea una carpeta nueva: `mkdir python_basics`.
3.  Entra: `cd python_basics`.
4.  Crea un archivo llamado `mi_script.py`.

### 4. Escribe Código (Con ayuda de IA)
Tu script debe tener al menos:
*   Una clase.
*   Una función.
*   Un `if/else`.
*   Imprimir algo en consola.

> **Prompt para LLM:**
> "Ayúdame a escribir un script en Python sencillo. Quiero hacer una clase llamada 'CalculadoraEspacial' que pueda sumar combustible y calcular distancias. Debe tener un método que decida si tenemos suficiente combustible para llegar a Marte (necesitamos 100 unidades). Incluye comentarios explicando el código."

### 5. Ejecútalo
Prueba que tu código no tenga errores:
```bash
python3 mi_script.py
```

### 6. Sube tus Cambios (Pull Request)

#### Opción Automática
Nuevamente, deja que Cursor te ayude.

> **Prompt para Cursor:**
> "Lee `clase/README_FLOW.md`. Quiero guardar mis cambios con el mensaje 'Agrego mi primer script de python' y subirlos. Usa el script `flow.sh` por favor."

```bash
# O hazlo manual:
./clase/flow.sh save "Agrego mi primer script de python"
./clase/flow.sh upload
```

#### Opción Manual
1.  Guarda cambios: `git add .`
2.  Commit: `git commit -m "Agrego mi primer script de python"`
3.  Push: `git push origin tarea-02-python`

4.  Ve a GitHub y crea el Pull Request hacia `{org}/{repo-name}`.

> **Recuerda:** Puedes pedirle ayuda a tu agente de IA: *"Ayúdame a subir mis cambios usando el script flow.sh, estoy en la rama tarea-02-python"*.

---

## 🆘 Troubleshooting con IA

Si algo sale mal, usa estos prompts:

*   **Error de Sintaxis:**
    > "Me sale este error: `IndentationError: expected an indented block`. ¿Qué significa y cómo lo arreglo en mi archivo?"
*   **Error de Ejecución:**
    > "Cuando corro el script, me dice `ModuleNotFoundError`. ¿Me falta instalar algo?"
*   **Duda de Git:**
    > "Hice el commit pero olvidé guardar el archivo. ¿Cómo puedo agregar el cambio al último commit sin crear uno nuevo?"

