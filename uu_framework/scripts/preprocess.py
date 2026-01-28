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
from process_calendar_topics import process_calendar_topics


def detect_git_info(verbose: bool = False) -> dict:
    """
    Auto-detect repository information from git remote.
    Returns dict with: repo_name, org, upstream_url, or empty values if detection fails.
    """
    import subprocess

    try:
        # Get remote origin URL
        result = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            capture_output=True,
            text=True,
            check=True
        )
        remote_url = result.stdout.strip()

        if verbose:
            print(f"      Detected git remote: {remote_url}")

        # Parse GitHub URL (handles both SSH and HTTPS)
        # SSH: git@github.com:org/repo.git
        # HTTPS: https://github.com/org/repo.git

        # Try SSH format first
        match = re.match(r'git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$', remote_url)
        if not match:
            # Try HTTPS format
            match = re.match(r'https://github\.com/([^/]+)/([^/]+?)(?:\.git)?$', remote_url)

        if match:
            org = match.group(1)
            repo_name = match.group(2)
            upstream_url = f"git@github.com:{org}/{repo_name}.git"

            if verbose:
                print(f"      Auto-detected: org={org}, repo={repo_name}")

            return {
                'repo_name': repo_name,
                'org': org,
                'upstream_url': upstream_url
            }
    except Exception as e:
        if verbose:
            print(f"      Warning: Could not auto-detect git info: {e}")

    return {'repo_name': '', 'org': '', 'upstream_url': ''}


def merge_repo_config(config: dict, git_info: dict, verbose: bool = False) -> dict:
    """
    Merge repository config from site.yaml with auto-detected git info.
    Config values take precedence over auto-detection.
    """
    repo_config = config.get('repository', {})

    result = {
        'repo_name': repo_config.get('name', '') or git_info.get('repo_name', ''),
        'org': repo_config.get('org', '') or git_info.get('org', ''),
        'upstream_url': repo_config.get('upstream_url', '') or git_info.get('upstream_url', '')
    }

    # Compute derived values
    if result['repo_name']:
        result['base_url'] = f"/{result['repo_name']}"
        result['pr_compare_url'] = f"https://github.com/{result['org']}/{result['repo_name']}/compare" if result['org'] else ""
    else:
        result['base_url'] = ''
        result['pr_compare_url'] = ''

    if verbose:
        print(f"      Final repo config: {result}")

    return result


def validate_repo_config(repo_config: dict, git_info: dict) -> None:
    """
    Validate repository configuration. Raises SystemExit if invalid.
    """
    # Check if we have any configuration at all
    if not repo_config.get('repo_name'):
        print("\nERROR: Cannot determine repository configuration.")
        print("Either:")
        print("  1. Add a git remote: git remote add origin git@github.com:org/repo.git")
        print("  2. Configure uu_framework/config/site.yaml repository section")
        sys.exit(1)

    # If both git remote and explicit config exist, verify they match
    if git_info.get('repo_name') and repo_config.get('repo_name'):
        if git_info['repo_name'] != repo_config['repo_name']:
            print("\nERROR: Repository mismatch detected!")
            print(f"  Config says: {repo_config['repo_name']}")
            print(f"  Git remote says: {git_info['repo_name']}")
            print("\nPlease ensure site.yaml and git remote match, or leave site.yaml empty for auto-detection.")
            sys.exit(1)


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


def generate_landing_page(config: dict, verbose: bool = False) -> bool:
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

        # Get site title from config (extract first part before " - ")
        site_name = config.get('site', {}).get('name', 'Course Site')
        # Extract the course name (before " - ITAM" or similar suffix)
        title = site_name.split(' - ')[0] if ' - ' in site_name else site_name

        # Generate clase/README.md with frontmatter
        frontmatter = f"""---
title: "{title}"
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
            "![Landing Page]({{ '/images/landing_page.png' | url }})"
        )

        # Get domain and repo name from config for URL conversion
        domain = config.get('site', {}).get('domain', 'sonder.art')
        repo_name = config.get('repository', {}).get('name', '')

        # Only convert URLs pointing to OUR site (domain/repo_name/...)
        # This preserves external URLs like shields.io badges, drive.google.com, etc.
        if repo_name:
            # Match: [text](https://www.sonder.art/repo_name/path) or [text](https://sonder.art/repo_name/path)
            # Convert to: [text]({{ '/path' | url }})
            pattern = rf'\[([^\]]+)\]\(https://(?:www\.)?{re.escape(domain)}/{re.escape(repo_name)}/([^\)]*)\)'
            web_content = re.sub(pattern, r"[\1]({{ '/\2' | url }})", web_content)

            # Also handle the site root: [text](https://www.sonder.art/repo_name/)
            pattern_root = rf'\[([^\]]+)\]\(https://(?:www\.)?{re.escape(domain)}/{re.escape(repo_name)}/?\)'
            web_content = re.sub(pattern_root, r"[\1]({{ '/' | url }})", web_content)

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
    print("\n[0/5] Generating landing page...")
    generate_landing_page(config, args.verbose)

    # Step 1: Extract metadata from all markdown files
    print("\n[1/5] Extracting metadata from markdown files...")
    metadata = extract_all_metadata(args.content, exclude, args.verbose)

    # Save metadata
    metadata_path = args.output / 'metadata.json'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"      Saved {len(metadata)} file metadata records to {metadata_path}")

    # Step 2: Generate hierarchy tree
    print("\n[2/5] Generating hierarchy tree...")
    hierarchy = generate_hierarchy(args.content, metadata, exclude, args.verbose)

    # Add documentation hierarchy (from uu_framework/docs/, rendered to /docs/)
    print("\n[2b/5] Adding documentation hierarchy...")
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
    print("\n[3/5] Aggregating tasks...")
    tasks = aggregate_all_tasks(args.content, metadata, args.verbose)

    # Save tasks
    tasks_path = args.output / 'tasks.json'
    with open(tasks_path, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
    print(f"      Saved {sum(len(v) for v in tasks.values())} tasks to {tasks_path}")

    # Step 4: Process calendar topics from CSV
    print("\n[4/5] Processing calendar topics...")
    csv_path = args.content / 'calendario_temas.csv'
    calendar_topics = process_calendar_topics(csv_path, args.verbose)

    # Save calendar topics
    calendar_path = args.output / 'calendar_topics.json'
    with open(calendar_path, 'w', encoding='utf-8') as f:
        json.dump(calendar_topics, f, indent=2, ensure_ascii=False)
    print(f"      Saved {len(calendar_topics)} calendar entries to {calendar_path}")

    # Save site config for templates
    site_path = args.output / 'site.json'
    with open(site_path, 'w', encoding='utf-8') as f:
        json.dump(config.get('site', {}), f, indent=2, ensure_ascii=False)

    # Step 5: Auto-detect and save repository config
    print("\n[5/5] Detecting repository configuration...")
    git_info = detect_git_info(args.verbose)
    repo_config = merge_repo_config(config, git_info, args.verbose)

    # Validate and fail if configuration is invalid
    validate_repo_config(repo_config, git_info)

    repo_path = args.output / 'repo.json'
    with open(repo_path, 'w', encoding='utf-8') as f:
        json.dump(repo_config, f, indent=2, ensure_ascii=False)
    print(f"      Saved repository config to {repo_path}")

    print("\n" + "=" * 60)
    print("Preprocessing complete!")
    print("=" * 60)

    return 0


if __name__ == '__main__':
    sys.exit(main())
