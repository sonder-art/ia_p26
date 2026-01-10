#!/usr/bin/env python3
"""
uu_framework Preprocessing Script

Main orchestrator for preprocessing course content.
Runs all preprocessing steps in order:
1. Copy documentation to processing location
2. Extract metadata from markdown files
3. Generate hierarchy tree
4. Aggregate tasks (homework, exams, projects)

Usage:
    python3 preprocess.py [--config CONFIG_PATH] [--content CONTENT_DIR]
"""

import os
import sys
import argparse
import json
import re
from pathlib import Path

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from extract_metadata import extract_all_metadata
from generate_indices import generate_hierarchy
from aggregate_tasks import aggregate_all_tasks


def load_config(config_path: Path) -> dict:
    """Load site configuration from YAML file."""
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except ImportError:
        # Fallback if PyYAML not available
        print("Warning: PyYAML not installed, using defaults")
        return {}
    except FileNotFoundError:
        print(f"Warning: Config file not found at {config_path}, using defaults")
        return {}


def generate_docs_hierarchy(docs_dir: Path, verbose: bool = False) -> dict:
    """
    Generate hierarchy for documentation from uu_framework/docs/.
    Returns a hierarchy dict to be merged into main hierarchy.
    Docs are processed separately and rendered to /docs/ path.
    """
    if not docs_dir.exists():
        if verbose:
            print(f"      Docs directory not found: {docs_dir}")
        return None

    docs_children = []
    for item in sorted(docs_dir.iterdir()):
        if item.is_dir() and item.name in ['dev', 'profesor', 'estudiante']:
            section = {
                "name": item.name,
                "path": f"docs/{item.name}",
                "url": f"/docs/{item.name}/",  # Direct URL to avoid /00_index/
                "type": "directory",
                "title": {
                    "dev": "Developer Guide",
                    "profesor": "Guía del Profesor",
                    "estudiante": "Guía del Estudiante"
                }.get(item.name, item.name.title()),
                "has_index": False,  # Uses pagination, not actual 00_index.md
                "no_number": True,  # Docs don't show numbers
                "children": []
            }

            # Add children (files in directory)
            for child in sorted(item.iterdir()):
                if child.is_file() and child.suffix == '.md':
                    child_entry = {
                        "name": child.stem,
                        "path": f"docs/{item.name}/{child.stem}",
                        "type": "file",
                        "title": get_title_from_file(child),
                        "has_index": False,
                        "no_number": True,  # Docs don't show numbers
                        "children": []
                    }
                    section["children"].append(child_entry)

            docs_children.append(section)
            if verbose:
                print(f"      Found: {item.name}/ ({len(section['children'])} files)")

    if docs_children:
        return {
            "name": "docs",
            "path": "docs",  # Used for nav-path
            "url": "/docs/",  # Direct URL override
            "type": "directory",
            "title": "Documentación",
            "has_index": False,  # Uses pagination template, not 00_index.md
            "no_number": True,  # Don't show numbers in navigation
            "children": docs_children
        }
    return None


def get_title_from_file(file_path: Path) -> str:
    """Extract title from markdown file frontmatter or filename."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check for YAML frontmatter
            if content.startswith('---'):
                end = content.find('---', 3)
                if end > 0:
                    match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content[3:end], re.MULTILINE)
                    if match:
                        return match.group(1)
    except Exception:
        pass
    # Fallback to filename
    name = file_path.stem
    # Remove numeric prefix
    name = re.sub(r'^\d+_', '', name)
    return name.replace('_', ' ').title()


def generate_landing_page(verbose: bool = False) -> bool:
    """
    Auto-generate clase/README.md from root README.md.
    Adds frontmatter and auto-generated notice.

    Returns True if successful, False otherwise.
    """
    root_readme = Path('README.md')
    clase_readme = Path('clase/README.md')

    if not root_readme.exists():
        if verbose:
            print(f"      Warning: {root_readme} not found, skipping landing page generation")
        return False

    try:
        # Read root README
        with open(root_readme, 'r', encoding='utf-8') as f:
            content = f.read()

        # Generate clase/README.md with frontmatter
        frontmatter = """---
title: "Inteligencia Artificial"
layout: layouts/base.njk
permalink: /
eleventyExcludeFromCollections: true
---

<!--
  ⚠️  AUTO-GENERATED FILE - DO NOT EDIT
  This file is automatically generated from /README.md during preprocessing.
  Edit the root README.md instead, then run: python3 uu_framework/scripts/preprocess.py
-->

"""

        # Convert image path for web rendering
        web_content = content.replace(
            '![Landing Page](clase/images/landing_page.png)',
            '![Landing Page]({{ \'/images/landing_page.png\' | url }})'
        )

        # Convert absolute links to use url filter
        web_content = re.sub(
            r'\[([^\]]+)\]\(https://www\.sonder\.art/ia_p26/([^\)]+)\)',
            r'[\1]({{ \'/\2\' | url }})',
            web_content
        )

        # Write to clase/README.md
        with open(clase_readme, 'w', encoding='utf-8') as f:
            f.write(frontmatter + web_content)

        if verbose:
            print(f"      Generated {clase_readme} from {root_readme}")

        return True

    except Exception as e:
        print(f"      Error generating landing page: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='uu_framework preprocessor')
    parser.add_argument('--config', type=Path,
                        default=Path('uu_framework/config/site.yaml'),
                        help='Path to site configuration')
    parser.add_argument('--content', type=Path,
                        default=Path('clase'),
                        help='Path to content directory')
    parser.add_argument('--docs', type=Path,
                        default=Path('uu_framework/docs'),
                        help='Path to documentation directory')
    parser.add_argument('--output', type=Path,
                        default=Path('uu_framework/eleventy/_data'),
                        help='Path to output data directory')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Enable verbose output')

    args = parser.parse_args()

    # Ensure output directory exists
    args.output.mkdir(parents=True, exist_ok=True)

    # Load configuration
    config = load_config(args.config)
    if args.verbose:
        print(f"Loaded config from {args.config}")

    # Get exclude patterns from config
    exclude = config.get('source', {}).get('exclude', [])

    print("=" * 60)
    print("uu_framework Preprocessing")
    print("=" * 60)

    # Step 0: Generate landing page from root README.md
    print("\n[0/4] Generating landing page...")
    generate_landing_page(args.verbose)

    # Step 1: Extract metadata from all markdown files
    print("\n[1/4] Extracting metadata from markdown files...")
    metadata = extract_all_metadata(args.content, exclude, args.verbose)

    # Save metadata
    metadata_path = args.output / 'metadata.json'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"      Saved {len(metadata)} file metadata records to {metadata_path}")

    # Step 2: Generate hierarchy tree
    print("\n[2/4] Generating hierarchy tree...")
    hierarchy = generate_hierarchy(args.content, metadata, exclude, args.verbose)

    # Add documentation hierarchy (from uu_framework/docs/, rendered to /docs/)
    print("\n[2b/4] Adding documentation hierarchy...")
    docs_hierarchy = generate_docs_hierarchy(args.docs, args.verbose)
    if docs_hierarchy and 'children' in hierarchy:
        hierarchy['children'].append(docs_hierarchy)
        print(f"      Added docs section with {len(docs_hierarchy['children'])} subsections")
    else:
        print("      No documentation found")

    # Save hierarchy
    hierarchy_path = args.output / 'hierarchy.json'
    with open(hierarchy_path, 'w', encoding='utf-8') as f:
        json.dump(hierarchy, f, indent=2, ensure_ascii=False)
    print(f"      Saved hierarchy to {hierarchy_path}")

    # Step 3: Aggregate tasks (homework, exams, projects)
    print("\n[3/4] Aggregating tasks...")
    tasks = aggregate_all_tasks(args.content, metadata, args.verbose)

    # Save tasks
    tasks_path = args.output / 'tasks.json'
    with open(tasks_path, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    print(f"      Saved {sum(len(v) for v in tasks.values())} tasks to {tasks_path}")

    # Save site config for templates
    site_path = args.output / 'site.json'
    with open(site_path, 'w', encoding='utf-8') as f:
        json.dump(config.get('site', {}), f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("Preprocessing complete!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
