# Templates

Nunjucks templates for page layouts and components.

## Layout Hierarchy

```
base.njk (master)
├── chapter.njk
├── index.njk
└── task-list.njk
```

Location: `uu_framework/eleventy/_includes/layouts/`

---

## base.njk (641 lines)

Master layout for all pages.

### Structure

```html
<!DOCTYPE html>
<html lang="es" class="theme-eva01">
<head>
  <!-- Meta, fonts, CSS -->
</head>
<body>
  <!-- Sidebar -->
  <aside id="sidebar">
    <!-- Header with logo -->
    <!-- Navigation (nav.njk) -->
    <!-- Footer with toggles -->
  </aside>

  <!-- Main content -->
  <main id="main-content">
    <!-- Breadcrumb -->
    <!-- Prev/Next arrows -->
    <!-- Page title (h1) -->
    <!-- Content -->
    <article class="prose">{{ content | safe }}</article>
    <!-- Bottom navigation -->
  </main>

  <!-- Mermaid modal -->
  <!-- JavaScript -->
</body>
</html>
```

### Key Sections

| Lines | Section |
|-------|---------|
| 1-16 | Head (meta, fonts, CSS) |
| 17-53 | Inline CSS (sidebar, mobile) |
| 55-130 | Mermaid styles |
| 132-230 | Sidebar |
| 232-340 | Main content |
| 342-370 | Mermaid modal |
| 372-480 | Mermaid JavaScript |
| 482-640 | Theme/accessibility JavaScript |

---

## nav.njk (198 lines)

Sidebar navigation component.

### Key Macros

#### isActive

```nunjucks
{% macro isActive(itemPath, currentUrl) %}
{%- set fullCurrentUrl = currentUrl | url -%}
{%- set normalizedCurrent = fullCurrentUrl | replace("/00_index/", "/") -%}
{%- if itemPath == fullCurrentUrl or itemPath == normalizedCurrent -%}current
{%- elif fullCurrentUrl.startsWith(itemPathBase) -%}ancestor
{%- else -%}inactive{%- endif -%}
{% endmacro %}
```

#### itemUrl

```nunjucks
{% macro itemUrl(item) %}
{%- if item.type == "directory" and item.has_index -%}
{{ ("/" + item.path + "/00_index/") | url }}
{%- elif item.type == "file" -%}
{{ ("/" + item.path | replace(".md", "") + "/") | url }}
{%- else -%}#
{%- endif -%}
{% endmacro %}
```

#### renderNavItem (recursive)

```nunjucks
{% macro renderNavItem(item, prefix, index, depth, currentUrl) %}
{% set num = item.name | getNavNumber(prefix, index) %}
{% set activeState = isActive(thisUrl, currentUrl) | trim %}

<div class="nav-item" data-expanded="true" data-depth="{{ depth }}" data-active="{{ activeState }}">
  <!-- Toggle button -->
  <!-- Link with number and title -->
  <!-- Recursive children -->
</div>
{% endmacro %}
```

### Navigation Sections

1. **Task Pages** (lines 96-141)
   - Tareas, Exámenes, Proyectos links
   - Badge counts from `tasks` data

2. **Content Navigation** (lines 143-159)
   - Recursive tree from `hierarchy`
   - Hierarchical numbering (1, 1.1, A.2)

---

## task-list.njk

Task list page layout.

### Usage

```yaml
---
title: Lista de Tareas
layout: layouts/task-list.njk
permalink: /tareas/
---
```

### Available Data

```nunjucks
{% for task in tasks.homework %}
  {{ task.id }}
  {{ task.title }}
  {{ task.due | formatDate }}
  {{ task.chapter }}
  {{ task.url }}
{% endfor %}
```

---

## Component Templates

Location: `uu_framework/eleventy/_includes/components/`

### homework.njk

```nunjucks
{% if task %}
<div class="component component--homework" data-id="{{ task.id }}">
  <h3 class="text-homework">{{ task.title }}</h3>
  {% if task.due %}
  <span class="{% if task.overdue %}text-exam{% endif %}">
    Fecha limite: {{ task.due | formatDate }}
  </span>
  {% endif %}
  {% if task.points %}
  <p>{{ task.points }} puntos</p>
  {% endif %}
  <a href="{{ task.url | url }}">Ver instrucciones →</a>
</div>
{% endif %}
```

### prompt.njk

```nunjucks
{% if prompt %}
<div class="component component--prompt relative">
  <h3 class="text-prompt">{{ prompt.title }}</h3>
  <div class="prompt-content font-mono">{{ prompt.content | safe }}</div>
  <button class="copy-btn" onclick="copyPrompt(this)">[Copiar]</button>
</div>
{% endif %}
```

---

## Template Context

### Global Data

```nunjucks
{{ site.name }}           {# From site.json #}
{{ site.description }}
{{ hierarchy }}           {# From hierarchy.json #}
{{ tasks.homework }}      {# From tasks.json #}
{{ tasks.exams }}
{{ tasks.projects }}
```

### Page Data

```nunjucks
{{ title }}               {# From frontmatter or derived #}
{{ content }}             {# Rendered markdown #}
{{ page.url }}            {# Current URL #}
{{ page.inputPath }}      {# Source file path #}
```

### Computed Data

```nunjucks
{{ prevPage.url }}        {# Previous in collection #}
{{ prevPage.title }}
{{ nextPage.url }}        {# Next in collection #}
{{ nextPage.title }}
```

---

## Adding a New Layout

1. Create `_includes/layouts/newlayout.njk`:

```nunjucks
{% extends "layouts/base.njk" %}

{% block content %}
  <!-- Custom content structure -->
  {{ content | safe }}
{% endblock %}
```

2. Use in frontmatter:

```yaml
---
layout: layouts/newlayout.njk
---
```
