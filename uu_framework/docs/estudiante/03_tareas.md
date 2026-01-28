# Tareas

Cómo ver y entregar las tareas del curso.

## Ver Lista de Tareas

1. Haz clic en **"Tareas"** en la barra lateral
2. O visita directamente: `/{repo-name}/tareas/`

### Información Mostrada

- **Nombre** de la tarea
- **Fecha límite** (si tiene)
- **Puntos** (si aplica)
- **Módulo** donde se encuentra
- **Estado** (pendiente o vencida)

---

## Identificar Tareas en el Contenido

Las tareas aparecen con borde **naranja** y etiqueta `[TAREA]`:

```
┌─────────────────────────────────────┐
│ [TAREA]                             │
│ Nombre de la Tarea                  │
│ Fecha límite: 15 de febrero de 2026 │
│                                     │
│ Instrucciones de la tarea...        │
│                                     │
│ Ver instrucciones completas →       │
└─────────────────────────────────────┘
```

---

## Entregar Tareas

Las tareas se entregan usando Git y GitHub:

### Flujo Básico

```
1. Trabajar en tu carpeta → estudiantes/tu-usuario/
2. Guardar cambios      → ./clase/flow.sh save "mensaje"
3. Subir a GitHub       → ./clase/flow.sh upload
4. Crear Pull Request   → En GitHub
```

### Comandos del Script flow.sh

```bash
# Iniciar una tarea
./clase/flow.sh start nombre-tarea

# Guardar progreso
./clase/flow.sh save "Completé la parte 1"

# Subir a GitHub
./clase/flow.sh upload

# Limpiar después de que se apruebe el PR
./clase/flow.sh finish
```

---

## Estructura de Carpetas

```
ia_p26/
├── clase/              ← Material del curso (NO MODIFICAR)
└── estudiantes/
    └── tu-usuario/     ← TU CARPETA (aquí trabajas)
        ├── tarea-01/
        ├── tarea-02/
        └── ...
```

### Reglas Importantes

1. **Trabaja SOLO en tu carpeta** (`estudiantes/tu-usuario/`)
2. **NO modifiques** nada en `clase/`
3. **Crea una subcarpeta** por tarea

---

## Estados de Tareas

| Estado | Significado |
|--------|-------------|
| Pendiente | Aún no vence |
| Vencida | Pasó la fecha límite |
| Sin fecha | No tiene fecha límite |

---

## Consejos

### Antes de Empezar

1. Lee todas las instrucciones
2. Revisa la fecha límite
3. Pregunta si algo no está claro

### Durante el Trabajo

1. Guarda frecuentemente (`flow.sh save`)
2. Usa commits descriptivos
3. Prueba tu código antes de entregar

### Al Entregar

1. Verifica que todo funciona
2. Revisa que los archivos correctos estén incluidos
3. Crea el Pull Request con descripción clara

---

## Problemas Comunes

### "No puedo hacer commit"

```bash
# Verifica que estés en la rama correcta
git status

# Verifica que tengas cambios
git diff
```

### "Mi PR tiene conflictos"

```bash
# Sincroniza con el repo principal
./clase/flow.sh sync

# Resuelve conflictos manualmente
# Luego guarda y sube de nuevo
```

### "No encuentro la tarea"

1. Revisa la sección "Tareas" en el sitio
2. Busca en el módulo correspondiente
3. Pregunta al profesor si no la encuentras

---

## Preguntas Frecuentes

### ¿Dónde entrego?

En tu carpeta personal: `estudiantes/tu-usuario/`

### ¿Cómo sé si se entregó?

Cuando tu Pull Request está creado en GitHub.

### ¿Puedo entregar tarde?

Depende de la política del curso. Consulta con el profesor.

### ¿Puedo modificar después de entregar?

Sí, mientras el PR no esté cerrado. Haz más commits y push.
