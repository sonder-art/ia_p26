# uu_framework

Static site generator for university course materials.

## Overview

uu_framework is a lightweight framework that renders Markdown course notes into a static website. It uses Eleventy + Tailwind CSS + Python preprocessing.

## Documentation

| Audience | Language | Path |
|----------|----------|------|
| **Developers** | English | [dev/](./dev/00_index.md) |
| **Professors** | Spanish | [profesor/](./profesor/00_index.md) |
| **Students** | Spanish | [estudiante/](./estudiante/00_index.md) |

### Developer Documentation

- [Architecture](./dev/01_architecture.md) - Complete data flow from markdown to HTML
- [Preprocessing](./dev/02_preprocessing.md) - Python scripts documentation
- [Eleventy](./dev/03_eleventy.md) - Filters, collections, transforms
- [Theming](./dev/04_theming.md) - CSS variables, themes, accessibility
- [Components](./dev/05_components.md) - All 6 component types
- [Templates](./dev/06_templates.md) - Nunjucks layouts and macros
- [Troubleshooting](./dev/07_troubleshooting.md) - Common issues and solutions

### Professor Documentation (Spanish)

- [Estructura](./profesor/01_estructura.md) - Directory structure and naming
- [Frontmatter](./profesor/02_frontmatter.md) - YAML metadata
- [Componentes](./profesor/03_componentes.md) - Homework, exercises, prompts
- [Mermaid](./profesor/04_mermaid.md) - Diagrams
- [Buenas Practicas](./profesor/05_buenas_practicas.md) - Recommendations

### Student Documentation (Spanish)

- [Navegacion](./estudiante/01_navegacion.md) - How to navigate the site
- [Accesibilidad](./estudiante/02_accesibilidad.md) - Themes, fonts, sizes
- [Tareas](./estudiante/03_tareas.md) - How to submit assignments

## Quick Start

### Requirements

- Docker (recommended) or:
  - Node.js 18+
  - Python 3.11+
  - npm

### Project Structure

```
uu_framework/
├── config/
│   ├── site.yaml           # Main configuration
│   └── themes/             # Color themes
├── scripts/
│   ├── preprocess.py       # Preprocessing orchestrator
│   ├── extract_metadata.py # Extract file metadata
│   ├── generate_indices.py # Generate hierarchy tree
│   ├── aggregate_tasks.py  # Aggregate tasks/exams
│   └── sync_check.py       # Check for updates
├── eleventy/
│   ├── .eleventy.js        # Eleventy configuration
│   ├── package.json        # Node dependencies
│   ├── _includes/          # Nunjucks templates
│   └── src/css/            # CSS styles
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yaml
└── docs/
    ├── README.md           # This file
    ├── dev/                # Developer documentation
    ├── profesor/           # Professor documentation
    └── estudiante/         # Student documentation
```

## Docker Usage

### Build the site

```bash
docker compose -f uu_framework/docker/docker-compose.yaml run build
```

### Development server

```bash
docker compose -f uu_framework/docker/docker-compose.yaml up dev
# Visit http://localhost:3000/{repo-name}/
```

## Without Docker

```bash
# Install Python dependencies
pip install pyyaml

# Install Node dependencies
cd uu_framework/eleventy
npm install

# Preprocessing
python3 uu_framework/scripts/preprocess.py

# Build site
npx @11ty/eleventy

# Build CSS
npx tailwindcss -i ./src/css/main.css -o ../../_site/css/styles.css --minify
```

## File Naming Convention

| Pattern | Meaning |
|---------|---------|
| `00_*.md` | Index file |
| `01_`, `02_` | Chapters (numeric order) |
| `01_a_`, `01_b_` | Sub-chapters (alphabetic) |
| `A_`, `B_` | Appendices |
| `code/` | Python code directory |

See [dev/01_architecture.md](./dev/01_architecture.md) for complete details.

## Component Syntax

```markdown
:::homework{id="task-01" title="My Task" due="2026-02-01"}
Task instructions...
:::

:::exercise{title="Exercise"}
Steps...
:::

:::prompt{title="LLM Prompt"}
Prompt text...
:::
```

See [dev/05_components.md](./dev/05_components.md) for all 6 component types.

## Themes

- **Eva Unit-01** (default): Dark purple with neon green accents
- **Light**: Light theme for bright environments
- **OpenDyslexic**: Accessible font toggle

See [dev/04_theming.md](./dev/04_theming.md) for theming details.

## Deployment

The site deploys automatically via GitHub Actions on push to `main`.

Live at: `https://{domain}/{base_url}/`

## Development

For detailed development guides, see:
- [Adding new components](./dev/05_components.md#adding-new-component-types)
- [Adding new themes](./dev/04_theming.md)
- [Troubleshooting](./dev/07_troubleshooting.md)
