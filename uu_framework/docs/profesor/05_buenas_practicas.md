# Buenas Prácticas

Recomendaciones basadas en el análisis del contenido actual.

## Estructura de Contenido

### ✓ Hacer

1. **Crear `00_index.md` en cada directorio**
   - Proporciona contexto del módulo
   - Lista los contenidos del capítulo
   - Define las tareas del módulo

2. **Usar prefijos numéricos consistentes**
   ```
   01_intro/
   02_conceptos/
   03_practica/
   ```

3. **Incluir tareas al inicio del archivo**
   - El componente `:::homework` primero
   - Luego el contenido de la lección

### ✗ Evitar

1. **Directorios sin índice**
   - No aparecerán correctamente en navegación

2. **Saltos en numeración**
   ```
   01_intro/
   03_avanzado/    ✗ Falta 02_
   ```

3. **Nombres con caracteres especiales**
   ```
   01_introducción.md    ✗ Acento
   01_mi tema.md         ✗ Espacio
   ```

---

## Componentes

### Cuándo Usar Cada Tipo

| Componente | Usar Para |
|------------|-----------|
| `homework` | Tareas calificadas con fecha de entrega |
| `exercise` | Práctica en clase sin calificación |
| `prompt` | Texto para copiar a ChatGPT/Claude |
| `example` | Demostrar código o conceptos |
| `exam` | Anunciar información de exámenes |
| `project` | Proyectos de largo plazo |

### IDs Significativos

```markdown
:::homework{id="A.1.1" title="..."}    ✓ Indica módulo A, sección 1, tarea 1
:::homework{id="git-ssh" title="..."}  ✓ Descriptivo
:::homework{id="1" title="..."}        ✗ Muy genérico
```

### Fechas Consistentes

```yaml
due="2026-02-15"    ✓ Formato ISO
due="15/02/2026"    ✗ Formato incorrecto
due="Feb 15"        ✗ Ambiguo
```

---

## Frontmatter

### Mínimo Recomendado

```yaml
---
title: "Título Descriptivo"
---
```

### Completo para Páginas Importantes

```yaml
---
title: "Módulo 1: Introducción"
summary: "Fundamentos del curso"
---
```

---

## Enlaces

### Relativos vs Absolutos

```markdown
[Siguiente](./02_next.md)           ✓ Relativo al archivo actual
[Referencia](../otro/archivo.md)    ✓ Relativo a otro directorio
[Externo](https://github.com)       ✓ URL completa
[Malo](/ruta/absoluta.md)           ✗ Puede fallar
```

### Links Externos

Incluir texto descriptivo:

```markdown
[Documentación de Python](https://python.org)    ✓
[Aquí](https://python.org)                       ✗ No descriptivo
```

---

## Código

### Especificar Lenguaje

````markdown
```python
def hello():
    print("Hello")
```
````

### Lenguajes Comunes

- `python` - Python
- `bash` - Comandos de terminal
- `javascript` - JavaScript
- `yaml` - Configuración
- `markdown` - Markdown
- `sql` - SQL

---

## Diagramas

### Mantener Simples

```mermaid
graph TD
    A --> B --> C    ✓ Claro y conciso
```

### Evitar Complejidad

Diagramas con más de 10 nodos son difíciles de leer. Divide en múltiples diagramas si es necesario.

---

## Imágenes

### Ubicación

Coloca imágenes en el mismo directorio o subdirectorio:

```
01_intro/
├── 00_index.md
├── diagrama.png
└── images/
    └── screenshot.png
```

### Referencia

```markdown
![Descripción](./diagrama.png)
![Screenshot](./images/screenshot.png)
```

### Formato

Prefiere `.png` para capturas de pantalla, `.svg` para diagramas vectoriales.

---

## Archivos Modelo

Estos archivos del curso son buenos ejemplos a seguir:

| Archivo | Por qué es bueno |
|---------|------------------|
| `a_stack/04_ide/00_index.md` | Índice completo con estructura clara |
| `a_stack/06_python/04_task_python.md` | Tarea bien estructurada |
| `a_stack/02_llms/01_conceptos_llm.md` | Contenido conceptual con diagramas |
| `a_stack/05_git/04_cheatsheet.md` | Referencia organizada |

---

## Checklist de Nuevo Contenido

- [ ] Archivo tiene prefijo numérico
- [ ] Nombre en minúsculas sin espacios
- [ ] Directorio tiene `00_index.md`
- [ ] Tareas tienen `id` único
- [ ] Fechas en formato YYYY-MM-DD
- [ ] Enlaces usan rutas relativas
- [ ] Código tiene lenguaje especificado
- [ ] Probado localmente antes de publicar
