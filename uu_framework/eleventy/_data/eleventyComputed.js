/**
 * Computed data for all pages
 * Provides prev/next navigation based on content collection
 */

// Extract hierarchy number from file path (e.g., "a_stack/02_llms/01_conceptos" -> "A.2.1")
function getHierarchyNumber(inputPath) {
  if (!inputPath) return '';

  // Remove ./clase/ prefix and .md extension
  const clean = inputPath
    .replace(/^\.?\/?(clase\/)?/, '')
    .replace(/\.md$/, '')
    .replace(/\/00_index$/, '');  // Remove index suffix

  const parts = clean.split('/');
  const numbers = [];

  for (const part of parts) {
    // Check for appendix prefix (a_, b_, etc.)
    const letterMatch = part.match(/^([a-z])_/i);
    if (letterMatch) {
      numbers.push(letterMatch[1].toUpperCase());
      continue;
    }

    // Check for numeric prefix (01_, 02_, etc.)
    const numMatch = part.match(/^(\d+)[_-]/);
    if (numMatch) {
      const num = parseInt(numMatch[1], 10);
      if (num > 0) {  // Skip 00_ (index files)
        numbers.push(num.toString());
      }
    }
  }

  return numbers.join('.');
}

// Clean title - remove "Módulo X:", "Module X:", etc.
function cleanTitle(title) {
  if (!title) return '';
  return title
    .replace(/^Módulo\s*\d+\s*[:\-]\s*/i, '')
    .replace(/^Module\s*\d+\s*[:\-]\s*/i, '')
    .replace(/^Capítulo\s*\d+\s*[:\-]\s*/i, '')
    .replace(/^Chapter\s*\d+\s*[:\-]\s*/i, '')
    .replace(/^Plantilla:\s*/i, '')
    .replace(/^\?\?\s*/, '')
    .trim();
}

// Get title from various sources
function getRawTitle(item, metadata) {
  // Try frontmatter title first
  if (item.data?.title) {
    return item.data.title;
  }

  // Try metadata from preprocessing
  const relativePath = item.inputPath?.replace('./clase/', '');
  if (metadata && relativePath && metadata[relativePath]) {
    return metadata[relativePath].title;
  }

  // Generate from filename
  const slug = item.fileSlug || '';
  if (slug && slug !== '00_index') {
    const clean = slug
      .replace(/^\d+[_-]?/, '')
      .replace(/[_-]/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
    return clean || slug;
  }

  // For index files, try parent folder name
  if (item.inputPath) {
    const parts = item.inputPath.split('/');
    if (parts.length >= 2) {
      const folder = parts[parts.length - 2];
      const clean = folder
        .replace(/^\d+[_-]?/, '')
        .replace(/[_-]/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase());
      return clean || folder;
    }
  }

  return 'Sin título';
}

// Get formatted nav title with hierarchy number
function getNavTitle(item, metadata) {
  const hierarchy = getHierarchyNumber(item.inputPath);
  const rawTitle = getRawTitle(item, metadata);
  const title = cleanTitle(rawTitle);

  if (hierarchy) {
    return `${hierarchy} ${title}`;
  }
  return title;
}

module.exports = {
  // Compute previous page
  prevPage: function(data) {
    const collections = data.collections;
    if (!collections || !collections.content || !data.page) return null;

    const content = collections.content;
    const currentUrl = data.page.url;
    const metadata = data.metadata || {};

    const currentIndex = content.findIndex(item => item.url === currentUrl);

    if (currentIndex > 0) {
      const prev = content[currentIndex - 1];
      return {
        url: prev.url,
        title: getNavTitle(prev, metadata)
      };
    }

    return null;
  },

  // Compute next page
  nextPage: function(data) {
    const collections = data.collections;
    if (!collections || !collections.content || !data.page) return null;

    const content = collections.content;
    const currentUrl = data.page.url;
    const metadata = data.metadata || {};

    const currentIndex = content.findIndex(item => item.url === currentUrl);

    if (currentIndex >= 0 && currentIndex < content.length - 1) {
      const next = content[currentIndex + 1];
      return {
        url: next.url,
        title: getNavTitle(next, metadata)
      };
    }

    return null;
  }
};
