---
title: "Guía del Profesor"
---

# Guía del Profesor

Cómo crear y organizar contenido para el curso.

## Inicio Rápido

1. Crea un archivo `.md` en la carpeta `clase/`
2. Nombra el archivo con prefijo numérico: `01_tema.md`
3. Escribe contenido en Markdown
4. Usa `:::homework{...}` para tareas

## Documentación

| Guía | Descripción |
|------|-------------|
| [Estructura](./01_estructura.md) | Convención de nombres y carpetas |
| [Frontmatter](./02_frontmatter.md) | Metadatos YAML opcionales |
| [Componentes](./03_componentes.md) | Tareas, ejercicios, prompts |
| [Mermaid](./04_mermaid.md) | Diagramas de flujo |
| [Buenas Prácticas](./05_buenas_practicas.md) | Recomendaciones |

## Ejemplo Básico

```markdown
# Título del Tema

Contenido introductorio.

:::homework{id="1.1" title="Mi Tarea" due="2026-02-15"}

Instrucciones de la tarea aquí.

:::

## Sección 1

Más contenido...
```

## Comandos Útiles

```bash
# Ver sitio localmente
docker compose -f uu_framework/docker/docker-compose.yaml up dev

# URL local
http://localhost:3000/{repo-name}/
```

## Archivos Clave

| Archivo | Propósito |
|---------|-----------|
| `clase/00_index.md` | Página principal del curso |
| `clase/a_stack/` | Apéndice A: Stack Tecnológico |
| `clase/flow.sh` | Script de Git para estudiantes |
