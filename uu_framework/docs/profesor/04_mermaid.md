# Diagramas Mermaid

Cómo crear diagramas de flujo, secuencia y más.

## Sintaxis Básica

````markdown
```mermaid
graph TD
    A[Inicio] --> B[Proceso]
    B --> C[Fin]
```
````

## Tipos de Diagramas

### Diagrama de Flujo

```mermaid
graph TD
    A[Inicio] --> B{¿Condición?}
    B -->|Sí| C[Acción 1]
    B -->|No| D[Acción 2]
    C --> E[Fin]
    D --> E
```

**Código:**
````markdown
```mermaid
graph TD
    A[Inicio] --> B{¿Condición?}
    B -->|Sí| C[Acción 1]
    B -->|No| D[Acción 2]
    C --> E[Fin]
    D --> E
```
````

### Diagrama de Secuencia

```mermaid
sequenceDiagram
    Estudiante->>GitHub: Push código
    GitHub->>CI: Ejecutar tests
    CI-->>GitHub: Resultado
    GitHub-->>Estudiante: Notificación
```

**Código:**
````markdown
```mermaid
sequenceDiagram
    Estudiante->>GitHub: Push código
    GitHub->>CI: Ejecutar tests
    CI-->>GitHub: Resultado
    GitHub-->>Estudiante: Notificación
```
````

### Diagrama de Flujo Horizontal

```mermaid
graph LR
    A[Entrada] --> B[Proceso 1]
    B --> C[Proceso 2]
    C --> D[Salida]
```

**Código:**
````markdown
```mermaid
graph LR
    A[Entrada] --> B[Proceso 1]
    B --> C[Proceso 2]
    C --> D[Salida]
```
````

---

## Formas de Nodos

| Sintaxis | Forma |
|----------|-------|
| `A[Texto]` | Rectángulo |
| `A(Texto)` | Rectángulo redondeado |
| `A{Texto}` | Diamante (decisión) |
| `A((Texto))` | Círculo |
| `A>Texto]` | Bandera |

---

## Tipos de Flechas

| Sintaxis | Tipo |
|----------|------|
| `-->` | Flecha sólida |
| `---` | Línea sólida |
| `-.-` | Línea punteada |
| `-.->` | Flecha punteada |
| `==>` | Flecha gruesa |
| `-->|texto|` | Flecha con etiqueta |

---

## Estilos

Puedes agregar colores con `style`:

````markdown
```mermaid
graph TD
    A[Correcto] --> B[Incorrecto]
    style A fill:#00ff41,stroke:#333
    style B fill:#ff6b35,stroke:#333
```
````

Colores del tema Eva01:
- Verde: `#00ff41`
- Morado: `#9d4edd`
- Naranja: `#ff6b35`
- Rojo: `#ef233c`

---

## Características Especiales

### Click para Expandir

Los diagramas tienen un botón "Expandir" que abre el diagrama en pantalla completa.

### Tema Automático

Los diagramas adaptan sus colores al tema actual (oscuro/claro).

---

## Ejemplos del Curso

### Flujo de Git

````markdown
```mermaid
graph TD
    A[Tu Repo Local] -->|git add| B[Staging]
    B -->|git commit| C[Commits Locales]
    C -->|git push| D[GitHub]
    D -->|PR| E[Repo Profesor]
```
````

### Proceso de LLM

````markdown
```mermaid
graph LR
    A[Texto] --> B[Tokenización]
    B --> C[Embeddings]
    C --> D[Transformer]
    D --> E[Predicción]
```
````

### Workflow de Tareas

````markdown
```mermaid
sequenceDiagram
    Estudiante->>Repo: Fork
    Estudiante->>Local: Clone
    Estudiante->>Local: Trabajo
    Estudiante->>GitHub: Push
    Estudiante->>Profesor: Pull Request
    Profesor-->>Estudiante: Review
```
````

---

## Consejos

1. **Mantén los diagramas simples** - Máximo 8-10 nodos
2. **Usa etiquetas descriptivas** - Texto corto y claro
3. **Orienta el flujo** - TD (arriba-abajo) o LR (izquierda-derecha)
4. **Prueba localmente** - Verifica que renderiza bien

---

## Recursos

- [Documentación oficial de Mermaid](https://mermaid.js.org/)
- [Editor en línea](https://mermaid.live/)
