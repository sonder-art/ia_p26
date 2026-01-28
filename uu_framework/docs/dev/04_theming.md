# Theming System

CSS variables, theme switching, and accessibility features.

## Theme Files

```
uu_framework/eleventy/src/css/
├── main.css              # Base Tailwind + components
└── themes/
    ├── eva01.css         # Dark theme (default)
    ├── light.css         # Light theme
    └── fonts.css         # Font definitions
```

---

## CSS Variables

### Eva Unit-01 Theme (Dark)

```css
:root {
  --color-bg: #1a0a2e;              /* Deep purple */
  --color-bg-secondary: #2d1b4e;
  --color-bg-tertiary: #3d2b5e;

  --color-text: #e8e8e8;
  --color-text-muted: #a0a0a0;

  --color-accent: #00ff41;          /* Neon green */
  --color-accent-secondary: #9d4edd;

  --color-border: #3d2b5e;
  --color-code-bg: #2d1b4e;

  /* Component colors */
  --color-homework: #ff6b35;        /* Orange */
  --color-exercise: #0dcaf0;        /* Cyan */
  --color-prompt: #6f42c1;          /* Purple */
  --color-example: #adb5bd;         /* Gray */
  --color-exam: #dc3545;            /* Red */
  --color-project: #ffc107;         /* Yellow */
}
```

### Light Theme

```css
:root {
  --color-bg: #ffffff;
  --color-text: #1a1a1a;
  --color-accent: #0066cc;
  /* ... same variable names, different values */
}
```

---

## Theme Switching

### JavaScript (`base.njk:562-624`)

```javascript
function toggleTheme() {
  const html = document.documentElement;
  const themeStylesheet = document.getElementById('theme-stylesheet');

  const currentTheme = localStorage.getItem('uu-theme') || 'eva01';
  const newTheme = currentTheme === 'eva01' ? 'light' : 'eva01';

  html.classList.remove(`theme-${currentTheme}`);
  html.classList.add(`theme-${newTheme}`);
  themeStylesheet.href = `/css/themes/${newTheme}.css`;

  localStorage.setItem('uu-theme', newTheme);
}
```

### HTML Structure

```html
<html class="theme-eva01">
  <head>
    <link rel="stylesheet" href="/css/themes/eva01.css" id="theme-stylesheet">
  </head>
</html>
```

---

## localStorage Keys

| Key | Values | Purpose |
|-----|--------|---------|
| `uu-theme` | `'eva01'`, `'light'` | Theme preference |
| `uu-dyslexic` | `'true'`, `'false'` | OpenDyslexic font |
| `uu-size` | `'normal'`, `'large'`, `'x-large'` | Font size |
| `uu-sidebar` | `'collapsed'`, `'expanded'` | Sidebar state |
| `uu-nav-scroll` | Number (string) | Scroll position |

---

## Accessibility Features

### 1. OpenDyslexic Font

Toggle in sidebar footer (lines 209-214, 575-590):

```javascript
function toggleDyslexic() {
  document.body.classList.toggle('font-dyslexic');
  const isDyslexic = document.body.classList.contains('font-dyslexic');
  localStorage.setItem('uu-dyslexic', isDyslexic);
}
```

CSS:
```css
body.font-dyslexic {
  font-family: 'OpenDyslexic', sans-serif;
}
```

### 2. Font Size Toggle

Three sizes cycle (lines 593-616):

```javascript
function toggleSize() {
  const sizes = ['normal', 'large', 'x-large'];
  const current = localStorage.getItem('uu-size') || 'normal';
  const idx = (sizes.indexOf(current) + 1) % sizes.length;
  const next = sizes[idx];

  document.body.classList.remove(`size-${current}`);
  document.body.classList.add(`size-${next}`);
  localStorage.setItem('uu-size', next);
}
```

CSS:
```css
body.size-normal { font-size: 1rem; }
body.size-large { font-size: 1.125rem; }
body.size-x-large { font-size: 1.25rem; }
```

### 3. Sidebar Scroll Persistence

Saves scroll position before navigation (lines 533-560):

```javascript
const sidebarNav = document.getElementById('sidebar-nav');

// Restore on load
const savedScrollPos = localStorage.getItem('uu-nav-scroll');
if (savedScrollPos) {
  sidebarNav.scrollTop = parseInt(savedScrollPos, 10);
}

// Save before navigating
sidebarNav.addEventListener('click', (e) => {
  if (e.target.closest('a')) {
    localStorage.setItem('uu-nav-scroll', sidebarNav.scrollTop);
  }
});
```

---

## Component Colors

Each component type has a distinct color:

```css
.component--homework { border-color: var(--color-homework); }  /* Orange */
.component--exercise { border-color: var(--color-exercise); }  /* Cyan */
.component--prompt { border-color: var(--color-prompt); }      /* Purple */
.component--example { border-color: var(--color-example); }    /* Gray */
.component--exam { border-color: var(--color-exam); }          /* Red */
.component--project { border-color: var(--color-project); }    /* Yellow */
```

Pseudo-element labels:
```css
.component--homework::before { content: '[TAREA]'; color: var(--color-homework); }
.component--exercise::before { content: '[EJERCICIO]'; color: var(--color-exercise); }
```

---

## Mermaid Diagram Theming

Diagrams adapt to current theme (`base.njk:375-476`):

```javascript
const isDark = document.documentElement.classList.contains('theme-eva01');
mermaid.initialize({
  theme: isDark ? 'dark' : 'default',
  themeVariables: isDark ? {
    primaryColor: '#9d4edd',
    primaryTextColor: '#e8e8e8',
    lineColor: '#00ff41',
    background: '#1a0a2e'
  } : {}
});
```

---

## Adding a New Theme

1. Create `src/css/themes/mytheme.css`:
   ```css
   :root {
     --color-bg: #...;
     --color-text: #...;
     /* all variables */
   }
   ```

2. Add to theme toggle logic in `base.njk`

3. Optionally add YAML config in `config/themes/`
