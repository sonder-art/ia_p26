# Tarea Práctica: Configuración y Certificaciones

Este ejercicio es tu "examen de manejo" para el curso. Vamos a poner en práctica todo lo aprendido sobre Git, GitHub, Flujo de trabajo y LLMs.

**Objetivo:** Crear tu espacio de trabajo personal y entregar evidencias de tus cursos completados mediante un Pull Request.

---

## Pre-requisitos: Prepara a tu Copiloto (LLM)

Antes de empezar, abre tu chat con ChatGPT, Claude o Gemini. Para que te ayuden correctamente, necesitan contexto.

> **Prompt Inicial para tu LLM:**
> "Hola, estoy tomando un curso de programación. Estamos usando un flujo de trabajo específico con Git y GitHub.
> Por favor, analiza los siguientes documentos para entender cómo debo trabajar:"
>
> *(Copia y pega el contenido de `clase/a_stack/05_git/02_repo_structure.md` y `clase/a_stack/05_git/03_workflow.md` en el chat)*. O si estas usando cursor referencia el archivo `clase/a_stack/05_git/04_cheatsheet.md` para comandos basicos de git.
>
> "A partir de ahora, ayúdame a seguir este flujo estrictamente. Si tengo un error de git, explícame qué pasó y cómo arreglarlo respetando estas reglas (usar ramas, no tocar la carpeta 'clase', etc)."

---

## Instrucciones Paso a Paso

### 1. Preparación del Entorno
Si aún no has clonado el repositorio y configurado el upstream, hazlo ahora (ver [02_repo_structure.md](./02_repo_structure.md)).

#### Opción Automática (Recomendada)
Vamos a usar el script mágico `flow.sh`. Primero, necesitamos darle permisos de ejecución (hacerlo funcionar).

1.  Abre tu terminal en la raíz del proyecto `ia_p26`.
2.  Ejecuta este comando (solo una vez en la vida):
    ```bash
    chmod +x clase/flow.sh
    ```
    *(Esto le dice a tu computadora que este archivo es un programa seguro).*
3.  Configura tu entorno inicial:
    ```bash
    ./clase/flow.sh setup
    ```
    *Esto configurará el `upstream` y creará tu carpeta automáticamente.*

#### Opción Manual
Sincroniza tu repositorio para tener lo último:
```bash
git checkout main
git pull upstream main
git push origin main
```

### 2. Crear la Rama de la Tarea
Vamos a crear una rama específica para esta entrega.
*   **Nombre de la rama:** `tarea-01-certificaciones`

```bash
# Opción Manual
git checkout -b tarea-01-certificaciones

# Opción Automática
./clase/flow.sh start tarea-01-certificaciones
```

> **¿Problemas?** Pregúntale a tu LLM:
> *"Intenté correr el script pero me dice 'Permission denied' o 'Command not found'. Estoy en la carpeta [ruta]. ¿Qué hago?"*

### 3. Crear tu Espacio Personal
1.  Ve a la carpeta `estudiantes/`.
2.  Crea una carpeta con tu **nombre de usuario de GitHub** (exactamente igual).
    ```bash
    mkdir estudiantes/tu_usuario
    ```

### 4. Copiar la Estructura de Certificaciones
Vamos a copiar la plantilla de certificaciones desde la carpeta `clase` a tu carpeta personal.

1.  Crea una carpeta llamada `certificaciones` dentro de tu carpeta personal.
    ```bash
    mkdir estudiantes/tu_usuario/certificaciones
    ```
2.  Copia los archivos de plantilla:
    ```bash
    cp clase/certificaciones/coding_llm.md estudiantes/tu_usuario/certificaciones/
    cp clase/certificaciones/github.md estudiantes/tu_usuario/certificaciones/
    ```

> **Prompt de Ayuda:**
> *"No estoy seguro si copié bien los archivos. ¿Qué comando puedo usar para listar los archivos dentro de mi carpeta 'estudiantes/mi_usuario/certificaciones' y ver si están ahí?"*

### 5. Llenar las Evidencias
Ahora debes editar los archivos que acabas de copiar en **TU** carpeta.

1.  **Coding con LLMs:**
    *   Completa el curso de DataCamp: [AI Assisted Coding for Developers](https://app.datacamp.com/learn/courses/ai-assisted-coding-for-developers).
    *   Toma una captura de pantalla (screenshot) donde se vea tu nombre y el curso completado al 100%.
    *   Guarda la imagen en `estudiantes/tu_usuario/certificaciones/evidencia_llm.png`.
    *   Edita `estudiantes/tu_usuario/certificaciones/coding_llm.md` e inserta la imagen o el link público a tu certificado.

2.  **Conceptos de GitHub:**
    *   Completa el curso: [Introduction to GitHub Concepts](https://app.datacamp.com/learn/courses/introduction-to-github-concepts).
    *   Toma captura de pantalla.
    *   Guarda la imagen en `estudiantes/tu_usuario/certificaciones/evidencia_github.png`.
    *   Edita `estudiantes/tu_usuario/certificaciones/github.md` e inserta la evidencia.

### 6. Guardar y Subir (Commit & Push)
Es hora de guardar tu trabajo.

```bash
# Opción Manual
git add estudiantes/tu_usuario/certificaciones/
git commit -m "Agrego evidencias de cursos DataCamp"
git push origin tarea-01-certificaciones

# Opción Automática
./clase/flow.sh save "Agrego evidencias de cursos DataCamp"
./clase/flow.sh upload
```

> **Troubleshooting con LLM:**
> Si el script falla o prefieres hacerlo manual, pregúntale a tu LLM:
> *"Quiero subir mis cambios manualmente. Estoy en la rama 'tarea-01-certificaciones'. ¿Cuáles son los comandos `git add`, `git commit` y `git push` exactos que debo usar para subir solo la carpeta 'estudiantes/mi_usuario'?"*

### 7. Crear el Pull Request (La Entrega)
Ve a GitHub y crea el Pull Request siguiendo las reglas de [03_workflow.md](./03_workflow.md).

*   **Base repository:** `sonder-art/ia_p26` (main)
*   **Head repository:** `tu-usuario/ia_p26` (tarea-01-certificaciones)
*   **Título del PR:** `[Tarea 01] Tu Nombre - Certificaciones`
*   **Descripción:**
    ```markdown
    Hola, entrego mis certificaciones.
    - [x] Carpeta personal creada
    - [x] Curso de LLMs completado
    - [x] Curso de GitHub completado
    ```

---

> **Nota:** Si usas el script `flow.sh`, puedes decirle a tu LLM (Cursor): *"Ayúdame a ejecutar el comando de upload usando el script flow.sh"*.

### ¿Algo salió mal? Guía de Pánico

Si Git te da errores rojos y feos:

1.  **No entres en pánico.** Es normal.
2.  Copia el error completo de la terminal.
3.  Pégalo en tu LLM junto con este contexto:
    > "Estoy intentando hacer [lo que hacías]. Me salió este error:
    > [PEGAR ERROR]
    > ¿Cómo lo soluciono sin borrar mi carpeta personal? Recuerda que uso un flujo de Feature Branch."
