# Componentes

Bloques especiales para tareas, ejercicios, prompts y más.

## Sintaxis General

```markdown
:::tipo{atributo="valor"}

Contenido del componente...

:::
```

---

## Tipos de Componentes

### Tarea (homework)

Para trabajos calificados que los estudiantes deben entregar.

```markdown
:::homework{id="A.1.1" title="Crear cuentas" due="2026-02-01" points="10"}

Instrucciones:
1. Crear cuenta en GitHub
2. Crear cuenta en DataCamp
3. Verificar acceso

:::
```

**Atributos:**
- `id` (requerido): Identificador único
- `title` (requerido): Nombre de la tarea
- `due` (opcional): Fecha límite (YYYY-MM-DD)
- `points` (opcional): Puntos

**Aparece en:** Lista de Tareas (`/tareas/`)

---

### Ejercicio (exercise)

Para práctica no calificada.

```markdown
:::exercise{title="Práctica de Git" difficulty="2"}

Pasos:
1. Clonar el repositorio
2. Crear una rama
3. Hacer un commit

:::
```

**Atributos:**
- `title` (requerido): Nombre del ejercicio
- `difficulty` (opcional): 1-5 (se muestra como asteriscos)

**No aparece en listas** - solo inline.

---

### Prompt (prompt)

Para texto que el estudiante debe copiar y usar con un LLM.

```markdown
:::prompt{title="Prompt Inicial" for="ChatGPT"}

Hola, estoy aprendiendo programación.
Por favor ayúdame a entender este código:

[pegar código aquí]

:::
```

**Atributos:**
- `title` (requerido): Nombre del prompt
- `for` (opcional): LLM destino (ChatGPT, Claude, Cursor)

**Características:**
- Fuente monoespaciada
- Botón de copiar

---

### Ejemplo (example)

Para mostrar código o conceptos de ejemplo.

```markdown
:::example{title="Ejemplo de Clase"}

```python
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre

    def saludar(self):
        return f"Hola, soy {self.nombre}"
```

:::
```

**Atributos:**
- `title` (requerido): Nombre del ejemplo

---

### Examen (exam)

Para información de exámenes.

```markdown
:::exam{id="parcial-1" title="Primer Parcial" date="2026-03-15" location="Aula 301" duration="2 horas"}

**Temas:**
- Capítulo 1: Introducción
- Capítulo 2: Git y GitHub
- Capítulo 3: Python Básico

**Material permitido:** Calculadora, 1 hoja de notas

:::
```

**Atributos:**
- `id` (requerido): Identificador único
- `title` (requerido): Nombre del examen
- `date` (opcional): Fecha
- `location` (opcional): Lugar
- `duration` (opcional): Duración

**Aparece en:** Lista de Exámenes (`/examenes/`)

---

### Proyecto (project)

Para proyectos de largo plazo.

```markdown
:::project{id="proyecto-final" title="Proyecto Final" due="2026-05-15" team_size="3" points="30"}

**Objetivo:** Desarrollar una aplicación de IA

**Entregables:**
1. Código fuente en GitHub
2. Documentación
3. Presentación de 10 minutos

:::
```

**Atributos:**
- `id` (requerido): Identificador único
- `title` (requerido): Nombre del proyecto
- `due` (opcional): Fecha de entrega
- `team_size` (opcional): Tamaño del equipo
- `points` (opcional): Puntos

**Aparece en:** Lista de Proyectos (`/proyectos/`)

---

## Colores de Componentes

| Tipo | Color | Etiqueta |
|------|-------|----------|
| homework | Naranja | [TAREA] |
| exercise | Cian | [EJERCICIO] |
| prompt | Morado | [PROMPT] |
| example | Gris | [EJEMPLO] |
| exam | Rojo | [EXAMEN] |
| project | Amarillo | [PROYECTO] |

---

## Contenido Permitido

Dentro de los componentes puedes usar:

✓ Formato Markdown (negritas, cursivas)
✓ Listas (ordenadas y no ordenadas)
✓ Bloques de código
✓ Enlaces
✓ Tablas

**No permitido:**
✗ Componentes anidados (un componente dentro de otro)

---

## Errores Comunes

### Sintaxis Incorrecta

```markdown
:::homework id="1" title="Test"    ✗ Faltan llaves
:::homework{id=1 title=Test}       ✗ Faltan comillas
:::homework{id="1", title="Test"}  ✗ Coma extra
:::homework{id="1" title="Test"}   ✓ Correcto
```

### Cierre Faltante

```markdown
:::homework{id="1" title="Test"}
Contenido...
                                   ✗ Falta :::

:::homework{id="1" title="Test"}
Contenido...
:::                                ✓ Correcto
```

### ID Duplicado

Cada `id` debe ser único en todo el sitio.

```markdown
:::homework{id="tarea-1" title="Primera"}  ✓
:::homework{id="tarea-1" title="Segunda"}  ✗ ID duplicado
:::homework{id="tarea-2" title="Segunda"}  ✓
```
