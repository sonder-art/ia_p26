# Eleventy Configuration

Main configuration in `uu_framework/eleventy/.eleventy.js` (301 lines).

## Markdown Processing

### Plugins (lines 6-9)

```javascript
const markdownIt = require("markdown-it");
const markdownItContainer = require("markdown-it-container");
const markdownItAttrs = require("markdown-it-attrs");
const markdownItAnchor = require("markdown-it-anchor");
```

### Options (lines 17-22)

```javascript
const mdOptions = {
  html: true,        // Allow raw HTML
  breaks: false,     // Don't convert \n to <br>
  linkify: true,     // Auto-link URLs
  typographer: true  // Smart quotes, dashes
};
```

### Component Container (lines 32-56)

```javascript
const componentTypes = ['homework', 'exercise', 'prompt', 'example', 'exam', 'project'];

componentTypes.forEach(type => {
  md.use(markdownItContainer, type, {
    validate: (params) => params.trim().match(new RegExp(`^${type}\\s*(.*)$`)),
    render: (tokens, idx) => {
      if (tokens[idx].nesting === 1) {
        // Opening: <div class="component component--TYPE" data-*="...">
        return `<div class="component component--${type}" ${attrsHtml}>\n`;
      } else {
        return '</div>\n';
      }
    }
  });
});
```

---

## Filters

### formatDate (lines 78-86)

```javascript
eleventyConfig.addFilter("formatDate", function(date) {
  return new Date(date).toLocaleDateString('es-MX', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
});
// "2026-02-01" → "1 de febrero de 2026"
```

### titleFromFilename (lines 89-99)

```javascript
eleventyConfig.addFilter("titleFromFilename", function(filename) {
  const name = filename.split('/').pop().replace(/\.\w+$/, '');
  const withoutPrefix = name.replace(/^\d+[_-]?/, '');
  return withoutPrefix
    .replace(/[_-]/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase());
});
// "01_install_python.md" → "Install Python"
```

### getOrder (lines 102-106)

```javascript
eleventyConfig.addFilter("getOrder", function(filename) {
  const match = filename.match(/^(\d+)/);
  return match ? parseInt(match[1], 10) : 999;
});
// "02_intro" → 2
```

### getNavNumber (lines 110-126)

```javascript
eleventyConfig.addFilter("getNavNumber", function(name, prefix, index) {
  // Letter prefix (appendix): a_stack → "A"
  const letterMatch = name.match(/^([a-z])_/i);
  if (letterMatch) {
    return letterMatch[1].toUpperCase();
  }
  // Numeric prefix: 02_llms → "A.2" (with parent prefix)
  const numMatch = name.match(/^(\d+)[_-]/);
  if (numMatch) {
    return prefix + parseInt(numMatch[1], 10);
  }
  // Fallback
  return prefix + (index + 1);
});
```

### cleanNavTitle (lines 129-139)

```javascript
eleventyConfig.addFilter("cleanNavTitle", function(title) {
  return title
    .replace(/^Módulo\s*\d+\s*[:\-]\s*/i, '')  // Remove "Módulo X:"
    .replace(/^Module\s*\d+\s*[:\-]\s*/i, '')
    .replace(/^Capítulo\s*\d+\s*[:\-]\s*/i, '')
    .trim();
});
// "Módulo 2: LLMs" → "LLMs"
```

---

## Collections

### content (lines 146-162)

```javascript
eleventyConfig.addCollection("content", function(collectionApi) {
  return collectionApi.getFilteredByGlob("clase/**/*.md")
    .filter(item => {
      if (item.inputPath.includes('b_libros')) return false;
      if (item.inputPath.includes('README_FLOW')) return false;
      if (item.inputPath.includes('task-pages')) return false;
      if (item.inputPath.includes('??_')) return false;
      return true;
    })
    .sort((a, b) => {
      const orderA = a.data.order || getOrderFromPath(a.inputPath);
      const orderB = b.data.order || getOrderFromPath(b.inputPath);
      return orderA - orderB;
    });
});
```

---

## Transforms

### fixMdLinks (lines 195-217)

Converts `.md` links to `/` URLs in output HTML:

```javascript
eleventyConfig.addTransform("fixMdLinks", function(content, outputPath) {
  if (outputPath && outputPath.endsWith(".html")) {
    return content.replace(
      /href="([^"]*?)\.md"/g,
      (match, path) => {
        if (path.startsWith('http')) return match;
        let newPath = path;
        if (newPath.startsWith('./')) {
          newPath = '../' + newPath.slice(2);
        }
        return `href="${newPath}/"`;
      }
    );
  }
  return content;
});
```

---

## Passthrough Copy

```javascript
// CSS
eleventyConfig.addPassthroughCopy({ "src/css": "css" });

// Fonts
eleventyConfig.addPassthroughCopy({ "src/fonts": "fonts" });

// Images from content
eleventyConfig.addPassthroughCopy("clase/**/*.{png,jpg,jpeg,gif,svg,webp}");
```

---

## Shortcodes

### icon (lines 169-182)

```javascript
eleventyConfig.addShortcode("icon", function(name) {
  const icons = {
    homework: '[T]',
    exercise: '[E]',
    prompt: '[>]',
    example: '[*]',
    exam: '[!]',
    project: '[P]'
  };
  return icons[name] || `[${name}]`;
});
```

Usage: `{% icon "homework" %}` → `[T]`

---

## Global Data

```javascript
eleventyConfig.addGlobalData("layout", "layouts/base.njk");
```

All markdown files use `base.njk` unless overridden in frontmatter.

---

## Helper Functions

### parseAttributes (lines 254-265)

```javascript
function parseAttributes(str) {
  const attrs = {};
  const regex = /(\w+)=["']([^"']+)["']/g;
  let match;
  while ((match = regex.exec(str)) !== null) {
    attrs[match[1]] = match[2];
  }
  return attrs;
}
// '{id="A.1" title="Test"}' → {id: "A.1", title: "Test"}
```

### getOrderFromPath (lines 272-300)

```javascript
function getOrderFromPath(path) {
  // Calculates sort order from file path
  // Uses weighted numeric prefixes
  // Letter prefixes (a_, b_) sort after numbers
}
```
