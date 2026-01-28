#!/usr/bin/env python3
"""
Metadata Extraction Script

Extracts YAML frontmatter and component markers from markdown files.
Gracefully handles files without frontmatter.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter dict, remaining content)
    """
    if not content.startswith('---'):
        return {}, content

    # Find closing ---
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_str = match.group(1)
    remaining = content[match.end():]

    # Parse YAML
    try:
        import yaml
        frontmatter = yaml.safe_load(frontmatter_str) or {}
    except:
        # Simple fallback parser
        frontmatter = {}
        for line in frontmatter_str.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                frontmatter[key] = value

    return frontmatter, remaining


def extract_components(content: str) -> List[Dict[str, Any]]:
    """
    Extract :::component markers from markdown content.

    Supports:
        :::homework{id="..." title="..." due="..."}
        content
        :::
    """
    components = []
    component_types = ['homework', 'exercise', 'prompt', 'example', 'exam', 'project']

    # Pattern to match :::type{attrs}\ncontent\n:::
    pattern = r':::(\w+)(?:\{([^}]*)\})?\s*\n(.*?)\n:::'

    for match in re.finditer(pattern, content, re.DOTALL):
        comp_type = match.group(1)
        attrs_str = match.group(2) or ''
        comp_content = match.group(3).strip()

        if comp_type not in component_types:
            continue

        # Parse attributes
        attrs = {}
        for attr_match in re.finditer(r'(\w+)=["\']([^"\']+)["\']', attrs_str):
            attrs[attr_match.group(1)] = attr_match.group(2)

        components.append({
            'type': comp_type,
            'attrs': attrs,
            'content_preview': comp_content[:200] if comp_content else ''
        })

    return components


def extract_h1_title(content: str) -> Optional[str]:
    """Extract first H1 header from markdown content."""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def title_from_filename(filepath: Path) -> str:
    """Generate title from filename if no frontmatter title."""
    name = filepath.stem

    # Remove numeric prefix (00_, 01_, etc.)
    name = re.sub(r'^\d+[_-]?', '', name)

    # Remove letter suffix patterns (a_, b_, etc.)
    name = re.sub(r'^[a-z]_', '', name)

    # Convert underscores/hyphens to spaces and capitalize
    name = name.replace('_', ' ').replace('-', ' ')
    name = ' '.join(word.capitalize() for word in name.split())

    return name or 'Sin titulo'


def get_order_from_filename(filepath: Path) -> int:
    """Extract sort order from filename prefix."""
    name = filepath.stem
    match = re.match(r'^(\d+)', name)
    if match:
        return int(match.group(1))

    # Check for letter prefix (a, b, c -> 1, 2, 3)
    match = re.match(r'^([a-z])_', name)
    if match:
        return ord(match.group(1)) - ord('a') + 1

    # Appendix letters (A, B, C -> 100, 101, 102)
    match = re.match(r'^([A-Z])_', name)
    if match:
        return 100 + ord(match.group(1)) - ord('A')

    return 999


def extract_file_metadata(filepath: Path, verbose: bool = False) -> Dict[str, Any]:
    """Extract metadata from a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        if verbose:
            print(f"      Warning: Could not read {filepath}: {e}")
        return {}

    # Parse frontmatter
    frontmatter, body = parse_frontmatter(content)

    # Extract components
    components = extract_components(body)

    # Build metadata
    metadata = {
        'path': str(filepath),
        'title': frontmatter.get('title') or extract_h1_title(body) or title_from_filename(filepath),
        'type': frontmatter.get('type', 'lesson'),
        'order': frontmatter.get('order') or get_order_from_filename(filepath),
        'date': frontmatter.get('date'),
        'summary': frontmatter.get('summary'),
        'tags': frontmatter.get('tags', []),
        'due_date': frontmatter.get('due_date'),
        'components': components,
        'has_frontmatter': bool(frontmatter),
    }

    return metadata


def extract_all_metadata(
    content_dir: Path,
    exclude: List[str] = None,
    verbose: bool = False
) -> Dict[str, Dict[str, Any]]:
    """
    Extract metadata from all markdown files in content directory.

    Returns:
        Dict mapping file paths to their metadata
    """
    exclude = exclude or []
    metadata = {}

    content_path = Path(content_dir)
    if not content_path.exists():
        print(f"      Warning: Content directory {content_dir} does not exist")
        return metadata

    # Find all markdown files
    md_files = list(content_path.rglob('*.md'))

    for filepath in md_files:
        # Check exclusions
        rel_path = filepath.relative_to(content_path)
        skip = False
        for excl in exclude:
            if excl in str(rel_path):
                skip = True
                break

        if skip:
            if verbose:
                print(f"      Skipping excluded: {rel_path}")
            continue

        file_meta = extract_file_metadata(filepath, verbose)
        if file_meta:
            metadata[str(rel_path)] = file_meta

            if verbose:
                print(f"      Processed: {rel_path}")

    return metadata


if __name__ == '__main__':
    import sys
    import json

    content_dir = sys.argv[1] if len(sys.argv) > 1 else 'clase'
    metadata = extract_all_metadata(Path(content_dir), verbose=True)
    print(json.dumps(metadata, indent=2, ensure_ascii=False))
