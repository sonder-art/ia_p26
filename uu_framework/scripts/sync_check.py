#!/usr/bin/env python3
"""
Sync Check Script

Checks if files in clase/ that have been copied to estudiantes/
have been updated by the professor.

Usage:
    python3 sync_check.py <github_username>

This script is called by flow.sh after pulling from upstream.
It compares file hashes to detect updates and warns the student.
"""

import os
import sys
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple


# ANSI color codes for terminal output
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


def get_file_hash(filepath: Path) -> str:
    """Calculate MD5 hash of file content."""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return ''


def find_matching_files(
    clase_dir: Path,
    student_dir: Path
) -> List[Tuple[Path, Path]]:
    """
    Find files in student directory that match files in clase directory.

    Returns list of (clase_file, student_file) tuples.
    """
    matches = []

    if not student_dir.exists():
        return matches

    # Get all files in student directory
    for student_file in student_dir.rglob('*'):
        if student_file.is_dir():
            continue

        # Skip hidden files
        if any(part.startswith('.') for part in student_file.parts):
            continue

        # Look for matching file in clase/
        # Student might have copied from various subdirectories
        filename = student_file.name

        for clase_file in clase_dir.rglob(filename):
            if clase_file.is_file():
                matches.append((clase_file, student_file))
                break

    return matches


def check_for_updates(
    clase_dir: Path,
    student_dir: Path,
    verbose: bool = False
) -> List[Dict]:
    """
    Check for files that have been updated in clase/ but not in student directory.

    Returns list of dicts with update information.
    """
    updates = []
    matches = find_matching_files(clase_dir, student_dir)

    for clase_file, student_file in matches:
        clase_hash = get_file_hash(clase_file)
        student_hash = get_file_hash(student_file)

        if clase_hash != student_hash:
            # Files differ - profesor may have updated
            clase_mtime = clase_file.stat().st_mtime
            student_mtime = student_file.stat().st_mtime

            if clase_mtime > student_mtime:
                # Clase file is newer
                updates.append({
                    'clase_file': str(clase_file),
                    'student_file': str(student_file),
                    'type': 'updated',
                })

    return updates


def print_warnings(updates: List[Dict], username: str):
    """Print warnings about updated files."""
    if not updates:
        print(f"{GREEN}[SYNC] Todo al dia - no hay actualizaciones pendientes.{NC}")
        return

    print(f"\n{YELLOW}{'=' * 60}{NC}")
    print(f"{YELLOW}[SYNC] AVISO: Archivos actualizados por el profesor{NC}")
    print(f"{YELLOW}{'=' * 60}{NC}")
    print()
    print(f"Los siguientes archivos en tu carpeta tienen versiones")
    print(f"mas recientes en clase/. Revisa si necesitas actualizar:")
    print()

    for update in updates:
        print(f"  {BLUE}Archivo:{NC} {update['student_file']}")
        print(f"  {BLUE}Fuente:{NC}  {update['clase_file']}")
        print()

    print(f"{YELLOW}Para ver las diferencias, usa:{NC}")
    print(f"  diff <tu_archivo> <archivo_clase>")
    print()
    print(f"{YELLOW}Para actualizar manualmente:{NC}")
    print(f"  1. Revisa los cambios con diff")
    print(f"  2. Copia las partes que necesites")
    print(f"  3. O usa: cp <archivo_clase> <tu_archivo>")
    print()
    print(f"{RED}NOTA: El script NO sobrescribe tus archivos automaticamente")
    print(f"para proteger tu trabajo.{NC}")
    print()


def main():
    if len(sys.argv) < 2:
        print(f"Uso: {sys.argv[0]} <github_username>")
        print("Este script verifica si hay archivos actualizados por el profesor.")
        sys.exit(1)

    username = sys.argv[1]

    # Paths
    repo_root = Path.cwd()
    clase_dir = repo_root / 'clase'
    student_dir = repo_root / 'estudiantes' / username

    if not clase_dir.exists():
        print(f"{RED}Error: No se encontro el directorio clase/{NC}")
        sys.exit(1)

    if not student_dir.exists():
        # Student directory doesn't exist yet - nothing to check
        sys.exit(0)

    # Check for updates
    updates = check_for_updates(clase_dir, student_dir)

    # Print warnings
    print_warnings(updates, username)

    # Return 0 even if there are updates (don't block the sync)
    sys.exit(0)


if __name__ == '__main__':
    main()
