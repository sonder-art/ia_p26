# Frontmatter YAML

Metadatos opcionales al inicio del archivo.

## Formato Básico

```yaml
---
title: "Título de la Página"
---

# Contenido aquí
```

El frontmatter va entre `---` al inicio del archivo.

## Campos Disponibles

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `title` | texto | Título de la página |
| `layout` | texto | Plantilla a usar |
| `permalink` | texto | URL personalizada |
| `summary` | texto | Descripción breve |
| `date` | fecha | Fecha de publicación |
| `tags` | lista | Etiquetas |

## Ejemplos

### Página Simple

```yaml
---
title: "Introducción a Python"
---
```

### Página de Índice

```yaml
---
title: "Módulo 1: Fundamentos"
layout: layouts/index.njk
---
```

### Página Principal

```yaml
---
title: Inicio
layout: layouts/index.njk
permalink: /
---
```

### Con Todos los Campos

```yaml
---
title: "Conceptos de Machine Learning"
summary: "Introducción a los conceptos básicos de ML"
date: 2026-01-15
tags: [ml, python, data-science]
---
```

## Sin Frontmatter

Si no incluyes frontmatter, el sistema:

1. Usa el primer encabezado H1 como título
2. Si no hay H1, usa el nombre del archivo

```markdown
# Este es el Título

Contenido...
```

Equivale a:

```yaml
---
title: "Este es el Título"
---
```

## Plantillas Disponibles

| Layout | Uso |
|--------|-----|
| `layouts/base.njk` | Páginas de contenido (predeterminado) |
| `layouts/index.njk` | Páginas de índice con lista |
| `layouts/task-list.njk` | Lista de tareas/exámenes |

## URLs Personalizadas

Usa `permalink` para URLs especiales:

```yaml
---
title: Lista de Tareas
layout: layouts/task-list.njk
permalink: /tareas/
---
```

Esto crea la página en `/{repo-name}/tareas/` en lugar de la ruta normal.

## Notas Importantes

1. **YAML es sensible a espacios** - Usa espacios, no tabuladores
2. **Comillas opcionales** - Úsalas para texto con caracteres especiales
3. **Fechas en formato ISO** - `2026-01-15` (año-mes-día)
4. **Listas entre corchetes** - `[item1, item2, item3]`
