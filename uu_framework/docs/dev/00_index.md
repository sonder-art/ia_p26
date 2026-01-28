---
title: "Developer Guide"
---

# uu_framework Developer Guide

A static site generator for ITAM course materials, built on Eleventy with Python preprocessing.

## Quick Start

```bash
# Start dev server (auto-detects repo from git remote)
docker compose -f uu_framework/docker/docker-compose.yaml up dev

# Visit http://localhost:3000/{repo-name}/ (e.g., /ia_p26/)
```

## Architecture Overview

```
Markdown (clase/)
    → Python preprocessing (scripts/)
    → JSON data files (_data/)
    → Eleventy build (.eleventy.js)
    → HTML output (_site/)
```

## Documentation

| Guide | Description |
|-------|-------------|
| [Architecture](./01_architecture.md) | Complete data flow and pipeline |
| [Preprocessing](./02_preprocessing.md) | Python scripts (extract, generate, aggregate) |
| [Eleventy](./03_eleventy.md) | Filters, collections, transforms |
| [Theming](./04_theming.md) | CSS variables, themes, accessibility |
| [Components](./05_components.md) | All 6 component types and how to add new |
| [Templates](./06_templates.md) | Nunjucks layouts and macros |
| [Troubleshooting](./07_troubleshooting.md) | Common issues and solutions |

## Key Files

| File | Purpose |
|------|---------|
| `.eleventy.js` | Main Eleventy configuration |
| `scripts/preprocess.py` | Orchestrates preprocessing |
| `_includes/layouts/base.njk` | Master HTML template |
| `_includes/components/nav.njk` | Sidebar navigation |
| `config/site.yaml` | Site configuration |

## Build Commands

```bash
# Full build
docker compose -f uu_framework/docker/docker-compose.yaml run build

# Dev server with hot reload
docker compose -f uu_framework/docker/docker-compose.yaml up dev

# Preprocessing only (debug)
docker compose -f uu_framework/docker/docker-compose.yaml run preprocess
```

## Directory Structure

```
uu_framework/
├── config/           # Site and theme configuration
├── scripts/          # Python preprocessing
├── eleventy/         # Eleventy SSG
│   ├── _data/        # Generated JSON
│   ├── _includes/    # Templates
│   └── src/css/      # Stylesheets
├── docker/           # Docker config
└── docs/             # This documentation
```
