#!/usr/bin/env python3
"""
Task Aggregation Script

Collects all homework, exams, and projects from content files
and organizes them for display on dedicated pages.
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


def get_chapter_name(file_path: str) -> str:
    """Extract chapter name from file path."""
    parts = file_path.split('/')
    if len(parts) >= 2:
        # Get first directory after content root
        chapter = parts[0]
        # Clean up name
        clean = re.sub(r'^\d+[_-]?', '', chapter)
        clean = re.sub(r'^[a-zA-Z]_', '', clean)
        return clean.replace('_', ' ').title() or chapter
    return 'General'


def is_overdue(due_date: str) -> bool:
    """Check if a due date has passed."""
    if not due_date:
        return False

    try:
        due = datetime.strptime(str(due_date), '%Y-%m-%d')
        return due.date() < datetime.now().date()
    except:
        return False


def aggregate_all_tasks(
    content_dir: Path,
    metadata: Dict[str, Any],
    verbose: bool = False
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Aggregate all tasks from metadata.

    Returns:
        Dict with keys: 'homework', 'exams', 'projects'
        Each contains list of task dicts
    """
    tasks = {
        'homework': [],
        'exams': [],
        'projects': [],
    }

    for file_path, file_meta in metadata.items():
        components = file_meta.get('components', [])
        chapter = get_chapter_name(file_path)

        for comp in components:
            comp_type = comp.get('type')
            attrs = comp.get('attrs', {})

            if comp_type == 'homework':
                task = {
                    'id': attrs.get('id', ''),
                    'title': attrs.get('title', 'Tarea'),
                    'due': attrs.get('due'),
                    'points': attrs.get('points'),
                    'chapter': chapter,
                    'file': file_path,
                    'url': '/' + file_path.replace('.md', '/'),
                    'summary': comp.get('content_preview', '')[:100],
                    'overdue': is_overdue(attrs.get('due')),
                    'type': 'homework',
                }
                tasks['homework'].append(task)

                if verbose:
                    print(f"      Found homework: {task['title']} in {chapter}")

            elif comp_type == 'exam':
                task = {
                    'id': attrs.get('id', ''),
                    'title': attrs.get('title', 'Examen'),
                    'date': attrs.get('date'),
                    'location': attrs.get('location'),
                    'duration': attrs.get('duration'),
                    'points': attrs.get('points'),
                    'chapter': chapter,
                    'file': file_path,
                    'url': '/' + file_path.replace('.md', '/'),
                    'summary': comp.get('content_preview', '')[:100],
                    'overdue': is_overdue(attrs.get('date')),
                    'type': 'exam',
                }
                tasks['exams'].append(task)

                if verbose:
                    print(f"      Found exam: {task['title']} in {chapter}")

            elif comp_type == 'project':
                task = {
                    'id': attrs.get('id', ''),
                    'title': attrs.get('title', 'Proyecto'),
                    'due': attrs.get('due'),
                    'points': attrs.get('points'),
                    'team_size': attrs.get('team_size'),
                    'chapter': chapter,
                    'file': file_path,
                    'url': '/' + file_path.replace('.md', '/'),
                    'summary': comp.get('content_preview', '')[:100],
                    'overdue': is_overdue(attrs.get('due')),
                    'type': 'project',
                }
                tasks['projects'].append(task)

                if verbose:
                    print(f"      Found project: {task['title']} in {chapter}")

    # Sort by file path (follows section numbering convention)
    # e.g., a_stack/02_llms/... comes before a_stack/03_os_setup/...
    def sort_key(task):
        return task.get('file', '')

    tasks['homework'].sort(key=sort_key)
    tasks['exams'].sort(key=sort_key)
    tasks['projects'].sort(key=sort_key)

    return tasks


def aggregate_by_chapter(
    tasks: Dict[str, List[Dict[str, Any]]]
) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """
    Reorganize tasks by chapter.

    Returns:
        Dict mapping chapter names to their tasks
    """
    by_chapter = {}

    for task_type, task_list in tasks.items():
        for task in task_list:
            chapter = task.get('chapter', 'General')

            if chapter not in by_chapter:
                by_chapter[chapter] = {
                    'homework': [],
                    'exams': [],
                    'projects': [],
                }

            by_chapter[chapter][task_type].append(task)

    return by_chapter


if __name__ == '__main__':
    import sys
    import json

    # Test with sample metadata
    sample_metadata = {
        'a_stack/05_git/05_task_certifications.md': {
            'title': 'Tarea: Certificaciones',
            'components': [
                {
                    'type': 'homework',
                    'attrs': {
                        'id': 'tarea-01',
                        'title': 'Certificaciones',
                        'due': '2026-02-01'
                    },
                    'content_preview': 'Completar cursos de DataCamp...'
                }
            ]
        }
    }

    tasks = aggregate_all_tasks(Path('clase'), sample_metadata, verbose=True)
    print(json.dumps(tasks, indent=2, ensure_ascii=False))
