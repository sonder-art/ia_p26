# Architecture

Complete data flow from markdown source to rendered HTML.

## Pipeline Overview

```
[1] Python Preprocessing
    ├── extract_metadata.py   → metadata.json
    ├── generate_indices.py   → hierarchy.json
    └── aggregate_tasks.py    → tasks.json

[2] Eleventy Build
    ├── Parse markdown with markdown-it
    ├── Apply Nunjucks templates
    ├── Transform :::components to HTML
    └── Generate HTML pages

[3] CSS Processing
    └── Tailwind + theme CSS variables
```

## Data Flow Example

**Input**: `clase/a_stack/06_python/01_install_python.md`

### Step 1: Preprocessing

`extract_metadata.py` reads the file:
```json
{
  "a_stack/06_python/01_install_python.md": {
    "path": "clase/a_stack/06_python/01_install_python.md",
    "title": "Instalación de Python",
    "type": "lesson",
    "order": 1,
    "components": [{
      "type": "homework",
      "attrs": {"id": "A.6.1", "title": "Instalar Python 3"},
      "content_preview": "Instala Python 3..."
    }]
  }
}
```

### Step 2: Hierarchy Generation

`generate_indices.py` builds tree:
```json
{
  "name": "06_python",
  "path": "a_stack/06_python",
  "type": "directory",
  "has_index": true,
  "children": [{
    "name": "01_install_python.md",
    "type": "file",
    "title": "Instalación de Python"
  }]
}
```

### Step 3: Task Aggregation

`aggregate_tasks.py` extracts homework:
```json
{
  "homework": [{
    "id": "A.6.1",
    "title": "Instalar Python 3",
    "chapter": "Stack",
    "url": "/a_stack/06_python/01_install_python/"
  }]
}
```

### Step 4: Eleventy Build

1. File discovered via `clase/**/*.md` glob
2. Markdown parsed by markdown-it with plugins
3. `:::homework{...}` → `<div class="component component--homework">`
4. Template `base.njk` renders with nav, content, prev/next

### Step 5: Output

```
_site/{repo-name}/a_stack/06_python/01_install_python/index.html
```

## Configuration

### Directory Mapping (`.eleventy.js:233-244`)

```javascript
dir: {
  input: "clase",                              // Source markdown
  includes: "../uu_framework/eleventy/_includes", // Templates
  data: "../uu_framework/eleventy/_data",        // JSON data
  output: "_site"                              // Output HTML
},
pathPrefix: "/{repo-name}/"  // GitHub Pages path
```

### Content Collection

Filters applied (`.eleventy.js:146-162`):
- Excludes `b_libros/` (PDFs)
- Excludes `README_FLOW`
- Excludes `task-pages/`
- Excludes `??_*` (work-in-progress)

### URL Generation

```
clase/a_stack/02_llms/01_concepts.md
    ↓ Remove clase/, .md
/a_stack/02_llms/01_concepts/
    ↓ Add pathPrefix
/{repo-name}/a_stack/02_llms/01_concepts/
```

## Template Context

Available in all Nunjucks templates:

```nunjucks
{{ title }}              {# Page title #}
{{ content }}            {# Rendered HTML #}
{{ page.url }}           {# Current URL #}

{{ prevPage.url }}       {# Previous page #}
{{ prevPage.title }}

{{ nextPage.url }}       {# Next page #}
{{ nextPage.title }}

{{ site.name }}          {# From site.json #}
{{ hierarchy }}          {# From hierarchy.json #}
{{ tasks.homework }}     {# From tasks.json #}
```

## Link Transformation

`.md` links are converted to `/` URLs (`.eleventy.js:195-217`):

```
href="./01_intro.md"    → href="../01_intro/"
href="../file.md"       → href="../../file/"
```

**Known Issue**: Doesn't handle `#anchor` or `?query` params.
