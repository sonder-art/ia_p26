# Guía de Uso del Script `flow.sh`

Para facilitar tu trabajo en este curso, hemos creado un pequeño programa (script) llamado `flow.sh` que automatiza todos los comandos complicados de Git.

Este script está diseñado para que tú (o tu asistente de IA) puedan ejecutarlo y mantener todo en orden.

## ¿Cómo usarlo?

1.  Abre tu terminal en la carpeta del proyecto.
2.  Ejecuta el script con `./clase/flow.sh [comando]`.

> **Tip:** Si estás en la raíz, puedes llamarlo así: `./clase/flow.sh`.

---

## Comandos Disponibles

### 1. Configuración Inicial (`setup`)
Ejecuta esto **una sola vez** cuando clones el repositorio.
*   Conecta tu repo con el del profesor.
*   Crea tu carpeta en `estudiantes/` si no existe.

```bash
./clase/flow.sh setup
```

### 2. Empezar una Tarea (`start`)
Úsalo cada vez que el profesor deje una tarea nueva.
*   Sincroniza tu repo con el del profesor (baja lo nuevo).
*   Crea una rama nueva para tu tarea.

```bash
./clase/flow.sh start tarea-1-intro
```

### 3. Guardar Avance (`save`)
Úsalo cada vez que quieras guardar "una foto" de tu trabajo.
*   Hace `git add .` y `git commit`.

```bash
./clase/flow.sh save "Avance del ejercicio 1"
```

### 4. Subir Tarea (`upload`)
Úsalo cuando termines por hoy o quieras entregar.
*   Sube tus cambios a GitHub.
*   Te da el link para crear el Pull Request.

```bash
./clase/flow.sh upload
```

### 5. Sincronizar (`sync`)
Úsalo si solo quieres bajar las diapositivas nuevas sin empezar tarea.

```bash
./clase/flow.sh sync
```

### 6. Copiar Archivos Segura (`copy`)
Úsalo para traer plantillas o ejercicios de la carpeta `clase/` a tu carpeta personal.
*   **Seguridad:** Si el archivo ya existe en tu carpeta, **NO** lo sobrescribirá para evitar borrar tu trabajo accidentalmente.

```bash
./clase/flow.sh copy clase/ejemplo.py estudiantes/tu_usuario/ejemplo.py
```

---

## Para Agentes de IA (Cursor / Copilot)

Si estás usando una IA para programar, puedes decirle:

> "Usa el script `clase/flow.sh` para gestionar git. Por favor sincroniza el repo y crea una rama llamada 'tarea-X'."

El script está optimizado para dar salidas claras que la IA puede entender.

