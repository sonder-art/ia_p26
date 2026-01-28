:::homework{id="A.6.0" title="Certificación & Lectura de seccion A.6 Python Básico" due="2026-01-28" points="20"}

Completa el curso [Introduction to Python for Data Science](https://app.datacamp.com/learn/courses/intro-to-python-for-data-science). Despues de completar el curso lee la seccion completa de Python Básico.  
La tarea solo contara como completada si se sube la evidencia de la certificacion y se lee la seccion completa de Python Básico.  
El archivo para subirla esta en la carpeta [07_certificaciones](../07_certificaciones/python_intro.md)
:::

:::homework{id="A.6.1" title="Instalar Python 3" due="2026-01-28" points="0"}

Instala Python 3 en tu sistema (dentro de WSL si usas Windows) y verifica con `python3 --version`.  
Leer la seccion A.6 Python Básico completa.
:::

# Instalación de Python

Python es un lenguaje interpretado. Necesitamos instalar el "intérprete" para que nuestra computadora entienda el código `.py`.

## Guía con Ayuda de IA

Igual que con el IDE, la mejor forma de instalarlo es preguntando a tu LLM con los detalles de tu sistema.

### Prompt para Windows (WSL2) - **IMPORTANTE**

Si estás en Windows, **NO** instales Python en Windows normal. Debes instalarlo **DENTRO** de Ubuntu (WSL).

> **Copia y pega esto a tu LLM:**
> "Estoy usando WSL2 con Ubuntu. Quiero instalar Python 3 y pip.
> 1. ¿Cuál es el comando `apt` para instalarlos?
> 2. ¿Cómo verifico que se instalaron correctamente?
> 3. Explícame por qué debo instalarlo en WSL y no en Windows si voy a usar la terminal de Ubuntu."

### Prompt para macOS

> **Copia y pega esto a tu LLM:**
> "Tengo una Mac. Quiero instalar la última versión de Python 3.
> 1. ¿Me recomiendas usar el instalador oficial de python.org o usar Homebrew?
> 2. Si es Homebrew, ¿cuál es el comando?
> 3. ¿Cómo evito conflictos con el Python que ya trae Mac por defecto?"

### Prompt para Linux

> **Copia y pega esto a tu LLM:**
> "Estoy en [Tu Distro, ej. Ubuntu/Fedora].
> 1. ¿Cómo instalo `python3`, `pip` y `venv`?
> 2. Dame los comandos exactos de terminal."

---

## Verificación

Abre tu terminal y ejecuta:

```bash
python3 --version
# Debería salir algo como "Python 3.10.x" o superior
```

Si sale un error, copia ese error y pégalo en el chat de tu LLM.

