# Flujo de Trabajo Detallado para Entregar Tareas en GitHub

Este documento describe el ciclo de vida completo para trabajar en una tarea, desde la sincronización inicial hasta la entrega final mediante un Pull Request.

## Resumen del Flujo

1.  **Sincronizar:** Traer los últimos cambios de la clase (`upstream/main`) a tu `main`.
2.  **Rama:** Crear una rama específica para la tarea (`tarea-X`) desde `main`.
3.  **Trabajar:** Hacer cambios en tu carpeta `estudiantes/tu_usuario/`.
4.  **Subir:** Publicar tu rama `tarea-X` a tu GitHub (`origin`).
5.  **Entregar:** Crear un Pull Request desde tu rama `tarea-X` hacia el `main` de la clase (`upstream`).

---

## Automatización con `flow.sh`

Para facilitar este proceso, hemos creado un script que automatiza estos comandos.
Consulta la guía completa en: **[clase/README_FLOW.md](../../README_FLOW.md)**

Puedes usarlo con tu LLM:
> "Usa el script `clase/flow.sh` para crear una rama llamada 'tarea-2' y sincronizar el repo."

---

## Paso 1: Actualizar tu repositorio (Sincronización)

### Configuración Previa (Solo una vez)
Si es la primera vez que haces esto, necesitas decirle a Git cuál es el repositorio del profesor.
```bash
git remote add upstream git@github.com:{org}/{repo-name}.git
```
Verifica que tengas `origin` (tu repo) y `upstream` (mi repo):
```bash
git remote -v
```

### Rutina Diaria
Antes de empezar cualquier tarea nueva, debes asegurarte de que tu copia local tiene las últimas diapositivas y ejercicios del profesor.

1.  Abre tu terminal y navega a la carpeta de tu repositorio:
    ```bash
    cd [ruta_a_tu_repositorio]
    ```
2.  Muévete a la rama principal:
    ```bash
    git checkout main
    ```
3.  Trae los cambios del profesor (`upstream`) y mézclalos con tu `main`:
    ```bash
    git pull upstream main
    ```
4.  Actualiza tu copia en la nube (`origin`) para que también esté al día:
    ```bash
    git push origin main
    ```

*Ahora tu `main` es idéntico al `main` del profesor.*

---

## Paso 2: Crear una rama para la tarea

Nunca trabajes directamente en `main`. Crea una rama aislada para tu tarea.

1.  Crea la rama y cámbiate a ella en un solo paso:
    ```bash
    git checkout -b [nombre-rama-tarea]
    ```
    *Ejemplo:* `git checkout -b tarea-1-intro`

2.  Verifica que estás en la rama correcta:
    ```bash
    git status
    ```
    *Debe decir: `On branch tarea-1-intro`*

---

## Paso 3: Trabajar en tu carpeta asignada

> **⚠️ REGLA DE ORO:** Solo puedes modificar archivos dentro de `estudiantes/[tu_usuario_de_github]/`. Si tocas algo fuera de ahí, tu tarea será rechazada automáticamente.

1.  **Navega a tu carpeta personal.** Es vital que te muevas a tu carpeta antes de empezar.
    ```bash
    # Reemplaza 'usuario' con TU usuario de github
    cd estudiantes/usuario
    ```

2.  **Verifica dónde estás.**
    ```bash
    pwd
    ```
    *Deberías ver algo que termina en `.../estudiantes/tu-usuario`.*

3.  **Trabaja:**
    *   Crea archivos nuevos.
    *   Si creas una carpeta nueva y está vacía, git la ignorará. Para que git la detecte, crea un archivo vacío llamado `.gitkeep` dentro:
        ```bash
        touch carpeta-nueva/.gitkeep
        ```
    *   Resuelve los ejercicios o copia el código de la clase a tu carpeta.

---

## Paso 4: Guardar cambios (Commit)

Una vez que terminaste una parte del trabajo:

1.  **Revisa qué archivos modificaste.** Esto te ayuda a evitar subir archivos basura.
    ```bash
    git status
    ```
    *Deberías ver tus archivos en rojo.*

2.  **Agrega los archivos.**
    *   **Peligro:** `git add .` agrega TODO lo que hay en la carpeta actual. Úsalo solo si estás seguro de que estás dentro de tu carpeta personal y no hay archivos basura.
    *   **Mejor opción:** Agrega archivos o carpetas específicas:
        ```bash
        git add archivo.py
        # O para una carpeta entera
        git add mi-carpeta/
        ```

3.  **Guarda la "foto" de tu trabajo (Commit).**
    ```bash
    git commit -m "Descripción clara de lo que hice"
    ```
    *Ejemplo:* `git commit -m "Terminé el ejercicio 1 de python"`

---

## Paso 5: Subir tu rama a GitHub (Push)

Ahora subiremos tu rama `tarea-1-intro` a **TU** cuenta de GitHub (conocida como `origin`).
Recuerda: No estás subiendo al repo del profesor, estás subiendo a tu Fork.

1.  Ejecuta el push de la rama específica:
    ```bash
    git push origin [nombre-rama-tarea]
    ```
    *Ejemplo:* `git push origin tarea-1-intro`

---

## Paso 6: Crear el Pull Request (La Entrega)

Aquí es donde oficialmente entregas tu tarea al profesor. Es como enviar el correo con el adjunto, pero versión programador.

1.  Ve a la página de **TU Fork** en GitHub (`https://github.com/TU_USUARIO/NOMBRE_DEL_FORK`).
2.  GitHub suele ser inteligente y te mostrará un recuadro amarillo diciendo "Compare & pull request" con tu rama reciente.
    *   Si no aparece, ve a la pestaña "Pull requests" -> "New pull request".
    *   Busca la opción que dice "compare across forks" o asegúrate de que estás comparando repositorios distintos.
3.  **Configura la comparación (MUY IMPORTANTE):**
    Asegurate de que la flecha apunte hacia la izquierda (`base <- head`).

    *   **Base repository:** `{org}/{repo-name}` (Repo del profesor)
    *   **Base branch:** `main`
    *   **Head repository:** `[tu-usuario]/[tu-fork]` (Tu repositorio)
    *   **Compare branch:** `[nombre-rama-tarea]` (La rama donde trabajaste)
    
    *⚠️ Error común: No uses tu `main` en el "compare branch". Debes seleccionar la rama específica de tu tarea.*

4.  **Título:** `[Tarea X] Tu Nombre - Título Breve`
5.  **Descripción:** Explica brevemente qué hiciste o pega el template que te pida la tarea.
6.  Dale click a **Create Pull Request**.

---

## Paso 7: Limpieza (Post-Entrega)

Una vez que tu tarea fue aceptada (Merges) por el profesor o ya la terminaste.

1.  Regresa a tu `main` local:
    ```bash
    git checkout main
    ```
2.  Trae los cambios nuevos (donde tu tarea ya es parte oficial del historial):
    ```bash
    git pull upstream main
    ```
3.  Sincroniza tu `main` en la nube:
    ```bash
    git push origin main
    ```
4.  (Opcional) Borra la rama de la tarea que ya entregaste, pues ya está en `main`:
    ```bash
    git branch -d tarea-1-intro
    ```
