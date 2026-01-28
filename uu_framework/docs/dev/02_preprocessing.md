# Preprocessing Scripts

Three Python scripts run before Eleventy to generate JSON data files.

## Overview

```
preprocess.py (orchestrator)
├── extract_metadata.py  → metadata.json
├── generate_indices.py  → hierarchy.json
└── aggregate_tasks.py   → tasks.json
```

Location: `uu_framework/scripts/`

---

## 1. extract_metadata.py

Parses all markdown files and extracts metadata.

### Input
- All `.md` files in `clase/`
- Excludes paths matching `site.yaml` exclude patterns

### Processing

1. **YAML Frontmatter** (lines 34-45)
   ```yaml
   ---
   title: "Page Title"
   type: lesson
   ---
   ```

2. **Component Markers** (lines 60-85)
   ```markdown
   :::homework{id="A.1" title="Task"}
   Content here...
   :::
   ```

3. **Title Extraction** (fallback chain)
   - Frontmatter `title`
   - First H1 heading
   - Filename

### Output: `metadata.json`

```json
{
  "a_stack/01_intro/01_concepts.md": {
    "path": "clase/a_stack/01_intro/01_concepts.md",
    "title": "Conceptos",
    "type": "lesson",
    "order": 1,
    "components": [
      {
        "type": "homework",
        "attrs": {"id": "A.1.1", "title": "..."},
        "content_preview": "First 200 chars..."
      }
    ],
    "has_frontmatter": true
  }
}
```

---

## 2. generate_indices.py

Builds hierarchical tree structure for navigation.

### Sort Key Algorithm (lines 25-50)

```python
def get_sort_key(name):
    # Returns tuple: (category, number, sub_category, name)
    # "01_intro"    → (0, 1, 0, '')      # Numbered
    # "01_a_sub"    → (0, 1, 1, 'a')     # Sub-section
    # "a_stack"     → (2, 999, 0, 'a')   # Appendix (letter prefix)
```

Priority:
1. Numeric prefixes (00_, 01_, 02_)
2. Letter sub-prefixes (_a_, _b_)
3. Appendix prefixes (a_, b_)

### Output: `hierarchy.json`

```json
{
  "name": "clase",
  "type": "root",
  "children": [
    {
      "name": "a_stack",
      "type": "directory",
      "path": "a_stack",
      "has_index": true,
      "title": "Stack",
      "children": [...]
    }
  ]
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `name` | Directory/file name |
| `path` | Relative path from clase/ |
| `type` | `directory` or `file` |
| `has_index` | Has `00_index.md` |
| `title` | From metadata or derived |
| `order` | Sort tuple |
| `children` | Nested items |

---

## 3. aggregate_tasks.py

Collects homework, exams, and projects into lists.

### Processing

1. Reads `metadata.json`
2. Extracts components by type
3. Calculates overdue status
4. Generates URLs

### Output: `tasks.json`

```json
{
  "homework": [
    {
      "id": "A.1.1",
      "title": "Crear cuentas",
      "due": "2026-02-01",
      "points": null,
      "chapter": "Stack",
      "file": "a_stack/01_intro/01_cuentas.md",
      "url": "/a_stack/01_intro/01_cuentas/",
      "summary": "First 100 chars...",
      "overdue": false,
      "type": "homework"
    }
  ],
  "exams": [],
  "projects": []
}
```

### Overdue Calculation (lines 28-37)

```python
def is_overdue(due_str):
    if not due_str:
        return False
    try:
        due_date = datetime.strptime(due_str, '%Y-%m-%d').date()
        return due_date < datetime.now().date()
    except:
        return False
```

---

## Running Preprocessing

### Via Docker

```bash
# Full build (includes preprocessing)
docker compose -f uu_framework/docker/docker-compose.yaml run build

# Preprocessing only
docker compose -f uu_framework/docker/docker-compose.yaml run preprocess
```

### Manual

```bash
cd uu_framework
python3 scripts/preprocess.py --content ../clase --output eleventy/_data
```

---

## Error Handling

### Current Behavior

- Missing frontmatter: Falls back to H1 or filename
- Invalid YAML: Silently ignored, returns `{}`
- Missing files: Warning logged, continues
- Invalid dates: Treated as not overdue

### Known Issues

- Bare `except:` blocks catch all errors silently
- No validation of required component attributes
- No duplicate ID detection

See [Troubleshooting](./07_troubleshooting.md) for fixes.
