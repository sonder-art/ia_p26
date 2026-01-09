# Troubleshooting

Common issues and solutions.

## Build Issues

### Pages Not Rendering

**Symptom**: Markdown file exists but no HTML generated

**Causes**:
1. File in excluded path (`b_libros/`, `??_*`)
2. Missing from collection glob
3. Invalid frontmatter YAML

**Solution**:
```bash
# Check if file is in collection
grep -r "filename" _site/
```

### Broken Internal Links

**Symptom**: Links show `.md` extension or 404

**Cause**: Link transform not applied

**Solution**: Ensure links use relative paths:
```markdown
[Link](./other-file.md)     ✓
[Link](other-file.md)       ✓
[Link](/absolute/path.md)   ✗ May not transform
```

### Missing Navigation Items

**Symptom**: Page not in sidebar

**Causes**:
1. File starts with `??_` (work-in-progress)
2. No `00_index.md` in parent directory
3. Sorting issue with prefix

**Solution**: Check file naming follows convention:
```
00_index.md   # Required for directory to appear
01_intro.md   # Numbered files
```

---

## Preprocessing Issues

### Empty tasks.json

**Symptom**: No homework/exams in lists

**Cause**: Components not extracted from metadata

**Solution**: Check component syntax:
```markdown
:::homework{id="A.1" title="Title"}  ✓
:::homework id="A.1" title="Title"   ✗ Missing braces
:::homework{id=A.1 title=Title}      ✗ Missing quotes
```

### Hierarchy Gaps

**Symptom**: Navigation numbering skips (1, 3, 4)

**Cause**: Missing numbered file/directory

**Solution**: Check all prefixes are sequential:
```
01_intro/
02_concepts/   # If missing, 03_ will show as 2
03_practice/
```

---

## Theming Issues

### Theme Not Switching

**Symptom**: Click toggle, nothing happens

**Causes**:
1. JavaScript error in console
2. localStorage blocked
3. CSS file not found

**Solution**: Check browser console for errors

### Wrong Colors

**Symptom**: Using wrong theme colors

**Cause**: CSS variable not defined in theme file

**Solution**: Ensure all variables exist in both themes:
```css
/* eva01.css */
--color-new-feature: #ff0000;

/* light.css */
--color-new-feature: #cc0000;
```

---

## Component Issues

### Component Not Styled

**Symptom**: Content appears but no border/color

**Causes**:
1. CSS class not in Tailwind safelist
2. Theme color not defined
3. Typo in component type

**Solution**: Check `tailwind.config.js` safelist includes:
```javascript
'text-homework', 'border-homework', 'bg-homework/15'
```

### Copy Button Not Working

**Symptom**: Prompt copy button does nothing

**Cause**: JavaScript function not defined

**Solution**: Check `copyPrompt` function exists in base.njk

---

## Known Issues

### XSS Vulnerability

**Risk**: `| safe` filter allows arbitrary HTML

**Current state**: Not sanitized

**Workaround**: Trust content sources; don't allow user-generated markdown

### Link Transform Edge Cases

**Issue**: Doesn't handle anchors or query params

```markdown
[Link](./file.md#section)   → ./file/#section (double slash)
[Link](./file.md?param=1)   → ./file/?param=1/ (trailing slash)
```

**Workaround**: Avoid anchors in .md links; use absolute URLs

### Bare Except Blocks

**Issue**: Python scripts catch all errors silently

**Location**: `extract_metadata.py:37`, `aggregate_tasks.py:36`

**Impact**: Errors hidden during preprocessing

---

## Debugging

### Check Preprocessing Output

```bash
# View generated JSON
cat uu_framework/eleventy/_data/metadata.json | jq '.'
cat uu_framework/eleventy/_data/hierarchy.json | jq '.'
cat uu_framework/eleventy/_data/tasks.json | jq '.'
```

### Check Eleventy Build

```bash
# Verbose build
npx @11ty/eleventy --dryrun
```

### Check Generated HTML

```bash
# Find specific page
find _site -name "*.html" | xargs grep "search-term"
```

### Docker Logs

```bash
# Watch build output
docker compose -f uu_framework/docker/docker-compose.yaml logs -f dev
```

---

## Getting Help

1. Check this documentation
2. Review agent findings in `/tmp/claude/.../tasks/`
3. Examine source code (line numbers referenced throughout)
4. File issue with reproduction steps
