# Component System

Six component types for course content, parsed by markdown-it-container.

## Overview

| Type | Color | Purpose | Aggregated |
|------|-------|---------|------------|
| `homework` | Orange | Graded assignments | Yes |
| `exercise` | Cyan | Practice (ungraded) | No |
| `prompt` | Purple | LLM prompts with copy | No |
| `example` | Gray | Code/concept demos | No |
| `exam` | Red | Exam information | Yes |
| `project` | Yellow | Long-term projects | Yes |

---

## Syntax

### Basic Format

```markdown
:::type{attr1="value1" attr2="value2"}

Content here (supports all markdown)

:::
```

### Homework

```markdown
:::homework{id="A.1.1" title="Task Name" due="2026-02-01" points="10"}

Instructions for the assignment.

:::
```

**Attributes:**
- `id` (required): Unique identifier
- `title` (required): Display name
- `due` (optional): Due date (YYYY-MM-DD)
- `points` (optional): Point value

### Exercise

```markdown
:::exercise{title="Exercise Title" difficulty="3"}

Step-by-step instructions.

:::
```

**Attributes:**
- `title` (required): Display name
- `difficulty` (optional): 1-5 scale (shown as asterisks)

### Prompt

```markdown
:::prompt{title="Prompt Name" for="ChatGPT"}

Prompt text to copy/paste into LLM.

:::
```

**Attributes:**
- `title` (required): Display name
- `for` (optional): Target LLM (ChatGPT, Claude, Cursor)

### Example

```markdown
:::example{title="Example Title"}

Example content with code:

```python
def hello():
    print("Hello!")
```

:::
```

**Attributes:**
- `title` (required): Display name
- `language` (optional): Not currently used

### Exam

```markdown
:::exam{id="parcial-01" title="Primer Parcial" date="2026-03-15" location="Aula 201" duration="2 horas"}

Topics and exam information.

:::
```

**Attributes:**
- `id` (required): Unique identifier
- `title` (required): Display name
- `date` (optional): Exam date
- `location` (optional): Location
- `duration` (optional): Duration

### Project

```markdown
:::project{id="proyecto-final" title="Final Project" due="2026-05-15" team_size="3" points="50"}

Project description and requirements.

:::
```

**Attributes:**
- `id` (required): Unique identifier
- `title` (required): Display name
- `due` (optional): Due date
- `team_size` (optional): Team size
- `points` (optional): Point value

---

## HTML Output

```html
<div class="component component--homework" data-id="A.1.1" data-title="Task Name" data-due="2026-02-01">
  <!-- Rendered markdown content -->
</div>
```

---

## CSS Styling

### Base Styles (`main.css`)

```css
.component {
  @apply p-4 rounded-lg mb-4;
  border-left: 4px solid;
  background: var(--color-bg-secondary);
}

.component::before {
  @apply text-xs font-bold uppercase mb-2 block;
}
```

### Per-Type Styles

```css
.component--homework { border-color: var(--color-homework); }
.component--homework::before { content: '[TAREA]'; color: var(--color-homework); }

.component--exercise { border-color: var(--color-exercise); }
.component--exercise::before { content: '[EJERCICIO]'; color: var(--color-exercise); }

.component--prompt { border-color: var(--color-prompt); }
.component--prompt::before { content: '[PROMPT]'; color: var(--color-prompt); }
```

---

## Nesting Rules

### Allowed

- Markdown formatting (bold, italic, links)
- Code blocks (fenced with ```)
- Lists (ordered and unordered)
- Tables
- Headings (H2, H3, etc.)

### Not Allowed

- Components inside components (nested containers)
- The inner `:::` would be treated as literal text

---

## Adding a New Component

### Step 1: Update `.eleventy.js`

Add to `componentTypes` array (line 32):

```javascript
const componentTypes = ['homework', 'exercise', 'prompt', 'example', 'exam', 'project', 'note'];
```

### Step 2: Add CSS Styles

In `main.css`:

```css
.component--note {
  border-color: var(--color-note);
}

.component--note::before {
  content: '[NOTA]';
  color: var(--color-note);
}
```

### Step 3: Add Theme Color

In each theme file (`eva01.css`, `light.css`):

```css
--color-note: #17a2b8;  /* Teal */
```

### Step 4: Update Tailwind Safelist

In `tailwind.config.js`:

```javascript
safelist: [
  // ... existing
  'text-note', 'border-note', 'bg-note/15',
]
```

### Step 5 (Optional): Add Template

Create `_includes/components/note.njk`:

```nunjucks
{% if note %}
<div class="component component--note">
  <h3 class="font-bold text-note">{{ note.title }}</h3>
  {{ note.content | safe }}
</div>
{% endif %}
```

### Step 6 (Optional): Add Aggregation

In `aggregate_tasks.py`, add extraction logic.

---

## Attribute Validation

### Current Behavior

- Missing attributes: Empty string or `null`
- Invalid format: Silently ignored
- Duplicate IDs: Not detected

### Best Practices

- Always quote attribute values: `id="value"`
- Use YYYY-MM-DD for dates
- Use alphanumeric IDs (no special characters)
