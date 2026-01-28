/**
 * Data file that reads documentation content from uu_framework/docs/
 * This allows docs to be rendered without copying them to clase/
 */

const fs = require('fs');
const path = require('path');
const matter = require('gray-matter');

module.exports = function() {
  const docsDir = path.join(process.cwd(), 'uu_framework/docs');
  const docs = [];

  // Check if docs directory exists
  if (!fs.existsSync(docsDir)) {
    console.log('Docs directory not found:', docsDir);
    return docs;
  }

  // Sections to process
  const sections = ['dev', 'profesor', 'estudiante'];

  sections.forEach(section => {
    const sectionDir = path.join(docsDir, section);
    if (!fs.existsSync(sectionDir)) return;

    const files = fs.readdirSync(sectionDir)
      .filter(f => f.endsWith('.md'))
      .sort();

    files.forEach(file => {
      const filePath = path.join(sectionDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      const parsed = matter(content);

      // Generate slug from filename
      const slug = file
        .replace(/\.md$/, '')
        .replace(/^00_index$/, '');

      // Build permalink
      let permalink = `/docs/${section}/`;
      if (slug) {
        permalink = `/docs/${section}/${slug}/`;
      }

      docs.push({
        section: section,
        filename: file,
        slug: slug,
        permalink: permalink,
        title: parsed.data.title || file.replace(/^\d+_/, '').replace(/\.md$/, '').replace(/_/g, ' '),
        content: parsed.content,
        data: parsed.data
      });
    });
  });

  // Add root docs index
  docs.unshift({
    section: 'root',
    filename: '00_index.md',
    slug: '',
    permalink: '/docs/',
    title: 'Documentación',
    content: `# Documentación

Guías y documentación del framework uu_framework.

## Secciones

| Sección | Idioma | Descripción |
|---------|--------|-------------|
| [Developer Guide](/docs/dev/) | English | Technical documentation for developers |
| [Guía del Profesor](/docs/profesor/) | Español | Guía para crear contenido |
| [Guía del Estudiante](/docs/estudiante/) | Español | Guía de uso del sitio |
`,
    data: { title: 'Documentación' }
  });

  return docs;
};
