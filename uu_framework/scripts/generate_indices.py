#!/usr/bin/env python3
"""
Hierarchy Generation Script

Generates a hierarchical tree structure from the content directory.
Respects the file naming convention:
- 00_ = index files
- 01_, 02_ = chapters/sections (numeric order)
- 01_a_, 01_b_ = sub-sections (alphabetical)
- A_, B_ = appendices (after numbered content)
- code/ = special code directory
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional


def get_sort_key(name: str) -> tuple:
    """
    Generate sort key for a file/directory name.

    Returns tuple for proper sorting:
    - (-1, 0, 0, '') for utility pages (aleatorio, etc.) - before all content
    - (0, num, 0, '') for numbered items (01_, 02_)
    - (0, num, 1, letter) for lettered sub-items (01_a_, 01_b_)
    - (1, ord, 0, '') for appendices (a_, b_, A_, B_)
    - (2, 999, 0, name) for other items
    - (3, 0, 0, '') for code directories
    - (4, ord, 0, '') for z_ prefixed items (documentation, always last)

    Order: utility pages → numbered content → appendices → other → code → z_ docs
    """
    # Special utility pages - should appear at the very top
    utility_pages = ['aleatorio.md', 'aleatorio']
    if name.lower() in utility_pages or name.lower().replace('.md', '') in utility_pages:
        return (-1, 0, 0, '')

    # Numbered items: 01_, 02_, etc.
    match = re.match(r'^(\d+)_', name)
    if match:
        num = int(match.group(1))
        # Check for letter suffix: 01_a_, 01_b_
        letter_match = re.match(r'^\d+_([a-z])_', name)
        if letter_match:
            return (0, num, 1, letter_match.group(1))
        return (0, num, 0, '')

    # z_ prefixed items (documentation) - always last
    match = re.match(r'^z_', name, re.IGNORECASE)
    if match:
        return (4, ord(name[2].lower()) if len(name) > 2 else 0, 0, name.lower())

    # Appendices: a_, b_, A_, B_, etc. (letters, but not z_)
    match = re.match(r'^([a-yA-Y])_', name)
    if match:
        return (1, ord(match.group(1).upper()), 0, '')

    # Special directories (code, etc.)
    if name.lower() == 'code':
        return (3, 0, 0, '')

    # Everything else
    return (2, 999, 0, name.lower())


def build_tree(
    dir_path: Path,
    metadata: Dict[str, Any],
    base_path: Path,
    exclude: List[str],
    depth: int = 0
) -> Dict[str, Any]:
    """
    Recursively build hierarchy tree from directory.

    Returns:
        Dict with structure:
        {
            'name': 'dirname',
            'path': 'relative/path',
            'type': 'directory' | 'file',
            'title': 'Human Title',
            'order': 1,
            'has_index': True,
            'children': [...]
        }
    """
    rel_path = dir_path.relative_to(base_path)
    name = dir_path.name

    # Check exclusions
    for excl in exclude:
        if excl in str(rel_path):
            return None

    node = {
        'name': name,
        'path': str(rel_path),
        'type': 'directory',
        'order': get_sort_key(name),
        'children': [],
        'has_index': False,
    }

    # Get title from index file if exists
    index_path = dir_path / '00_index.md'
    rel_index = str(rel_path / '00_index.md')

    if index_path.exists() and rel_index in metadata:
        node['has_index'] = True
        node['title'] = metadata[rel_index].get('title', name)
    else:
        # Generate title from directory name
        node['title'] = title_from_dirname(name)

    # Process children
    children = []

    for item in sorted(dir_path.iterdir(), key=lambda x: get_sort_key(x.name)):
        # Skip hidden files
        if item.name.startswith('.'):
            continue

        # Check exclusions
        rel_item = item.relative_to(base_path)
        skip = False
        for excl in exclude:
            if excl in str(rel_item):
                skip = True
                break
        if skip:
            continue

        if item.is_dir():
            child = build_tree(item, metadata, base_path, exclude, depth + 1)
            if child:
                children.append(child)
        elif item.suffix == '.md':
            # Skip index files in children (they're part of parent)
            if item.name == '00_index.md':
                continue

            rel_file = str(rel_item)
            file_meta = metadata.get(rel_file, {})

            children.append({
                'name': item.name,
                'path': rel_file,
                'type': 'file',
                'title': file_meta.get('title', title_from_filename(item.stem)),
                'order': get_sort_key(item.name),
                'summary': file_meta.get('summary'),
            })
        elif item.suffix == '.py':
            # Python files
            children.append({
                'name': item.name,
                'path': str(rel_item),
                'type': 'code',
                'title': item.name,
                'order': get_sort_key(item.name),
            })

    # Sort children
    node['children'] = sorted(children, key=lambda x: x['order'])

    return node


def title_from_dirname(name: str) -> str:
    """Generate human-readable title from directory name."""
    # Remove prefix
    clean = re.sub(r'^\d+[_-]?', '', name)
    clean = re.sub(r'^[a-zA-Z]_', '', clean)

    # Convert to title case
    clean = clean.replace('_', ' ').replace('-', ' ')
    return ' '.join(word.capitalize() for word in clean.split()) or name


def title_from_filename(name: str) -> str:
    """Generate human-readable title from filename."""
    # Remove prefix and extension
    clean = re.sub(r'^\d+[_-]?', '', name)
    clean = re.sub(r'^[a-z]_', '', clean)

    # Convert to title case
    clean = clean.replace('_', ' ').replace('-', ' ')
    return ' '.join(word.capitalize() for word in clean.split()) or name


def validate_sequence(children: List[Dict], parent_path: str, verbose: bool = False) -> List[str]:
    """
    Validate that numbered items follow a logical sequence.
    Returns list of warning messages.
    """
    warnings = []

    # Extract numbered items
    numbered = []
    for child in children:
        name = child['name']
        match = re.match(r'^(\d+)[_-]', name)
        if match:
            num = int(match.group(1))
            # Skip 00_ index files
            if num > 0:
                numbered.append((num, name))

    if not numbered:
        return warnings

    # Sort by number
    numbered.sort(key=lambda x: x[0])

    # Check for gaps
    nums = [n[0] for n in numbered]
    expected_start = nums[0]  # First number sets the baseline

    for i, (num, name) in enumerate(numbered):
        if i == 0:
            # First item - warn if not starting at 1
            if num > 1:
                missing = ', '.join(f'{n:02d}_' for n in range(1, num))
                warnings.append(
                    f"⚠️  {parent_path}: Sequence starts at {num:02d}_ (missing: {missing})"
                )
        else:
            prev_num = numbered[i-1][0]
            if num != prev_num + 1:
                gap = num - prev_num - 1
                missing = ', '.join(f'{n:02d}_' for n in range(prev_num + 1, num))
                warnings.append(
                    f"⚠️  {parent_path}: Gap in sequence - {prev_num:02d}_ → {num:02d}_ (missing: {missing})"
                )

    return warnings


def validate_hierarchy(node: Dict, path: str = '', verbose: bool = False) -> List[str]:
    """
    Recursively validate hierarchy for sequence issues.
    """
    warnings = []

    if 'children' in node and node['children']:
        # Validate this level
        current_path = path + '/' + node['name'] if path else node['name']
        if node.get('type') in ['directory', 'root']:
            warnings.extend(validate_sequence(node['children'], current_path, verbose))

        # Recurse into children
        for child in node['children']:
            if child.get('type') == 'directory':
                warnings.extend(validate_hierarchy(child, current_path, verbose))

    return warnings


def generate_hierarchy(
    content_dir: Path,
    metadata: Dict[str, Any],
    exclude: List[str] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Generate complete hierarchy tree for content directory.
    """
    exclude = exclude or []
    content_path = Path(content_dir)

    if not content_path.exists():
        return {'children': []}

    # Build tree starting from content directory
    tree = {
        'name': content_path.name,
        'path': '',
        'type': 'root',
        'title': 'Contenido',
        'children': [],
    }

    for item in sorted(content_path.iterdir(), key=lambda x: get_sort_key(x.name)):
        if item.name.startswith('.'):
            continue

        # Check exclusions
        skip = False
        for excl in exclude:
            if excl in item.name:
                skip = True
                break
        if skip:
            continue

        if item.is_dir():
            child = build_tree(item, metadata, content_path, exclude)
            if child:
                tree['children'].append(child)
                if verbose:
                    print(f"      Added: {item.name}")
        elif item.suffix == '.md':
            # Include root-level markdown files (except index files, README, and top-bar-only pages)
            if item.name not in ['00_index.md', 'README_FLOW.md', 'aleatorio.md']:
                rel_file = item.name
                file_meta = metadata.get(rel_file, {})

                # Check if this is a utility page (no numbers)
                is_utility = get_sort_key(item.name)[0] == -1

                tree['children'].append({
                    'name': item.name,
                    'path': rel_file,
                    'type': 'file',
                    'title': file_meta.get('title', title_from_filename(item.stem)),
                    'order': get_sort_key(item.name),
                    'summary': file_meta.get('summary'),
                    'no_number': is_utility,  # Utility pages don't show numbers
                })
                if verbose:
                    print(f"      Added file: {item.name}")

    # Sort top-level children
    tree['children'] = sorted(tree['children'], key=lambda x: x['order'])

    # Validate hierarchy for sequence gaps (always print warnings)
    warnings = validate_hierarchy(tree, verbose=verbose)
    if warnings:
        print("\n      Sequence warnings (file numbering issues):")
        for warning in warnings:
            print(f"      {warning}")

    return tree


if __name__ == '__main__':
    import sys
    import json

    content_dir = sys.argv[1] if len(sys.argv) > 1 else 'clase'
    hierarchy = generate_hierarchy(Path(content_dir), {}, verbose=True)
    print(json.dumps(hierarchy, indent=2, ensure_ascii=False, default=str))
