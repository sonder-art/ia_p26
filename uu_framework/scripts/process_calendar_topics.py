#!/usr/bin/env python3
"""
Process calendar topics from CSV file.

Reads clase/calendario_temas.csv and converts it to JSON format for use in templates.
Creates a placeholder CSV if it doesn't exist, but NEVER overwrites existing data.
"""

import csv
import json
from pathlib import Path
from datetime import datetime


def create_placeholder_csv(csv_path: Path):
    """
    Create a placeholder CSV with headers and example rows.
    Only creates if file doesn't exist - NEVER overwrites.
    """
    if csv_path.exists():
        return False

    placeholder_content = """Clase,Fecha,Tema
1,12/01/2026,Introducción e Historia
2,14/01/2026,Tema pendiente
asueto,16/01/2026,asueto
"""

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write(placeholder_content)

    return True


def parse_date(date_str: str) -> str:
    """
    Parse date from DD/MM/YYYY format to YYYY-MM-DD (ISO format).
    Returns None if date is invalid or empty.
    """
    if not date_str or not date_str.strip():
        return None

    try:
        # Parse DD/MM/YYYY
        dt = datetime.strptime(date_str.strip(), '%d/%m/%Y')
        # Return YYYY-MM-DD
        return dt.strftime('%Y-%m-%d')
    except ValueError:
        return None


def process_calendar_topics(csv_path: Path, verbose: bool = False) -> list:
    """
    Process calendar topics CSV file.

    Returns a list of topic dictionaries with:
    - clase: class number or "asueto"
    - date: ISO date string (YYYY-MM-DD)
    - topic: topic name
    - is_holiday: boolean indicating if it's a holiday
    """
    if not csv_path.exists():
        if verbose:
            print(f"      CSV file not found at {csv_path}, creating placeholder...")
        create_placeholder_csv(csv_path)
        if verbose:
            print(f"      Created placeholder at {csv_path}")

    topics = []

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                clase = row.get('Clase', '').strip()
                fecha = row.get('Fecha', '').strip()
                tema = row.get('Tema', '').strip()

                # Skip if no date
                if not fecha:
                    continue

                # Parse date to ISO format
                iso_date = parse_date(fecha)
                if not iso_date:
                    if verbose:
                        print(f"      Warning: Invalid date format '{fecha}', skipping")
                    continue

                # Determine if it's a holiday
                is_holiday = clase.lower() == 'asueto'

                topic_entry = {
                    'clase': clase,
                    'date': iso_date,
                    'topic': tema if tema else '',
                    'is_holiday': is_holiday
                }

                topics.append(topic_entry)

        if verbose:
            print(f"      Processed {len(topics)} calendar entries")
            holidays = sum(1 for t in topics if t['is_holiday'])
            classes = len(topics) - holidays
            print(f"      ({classes} classes, {holidays} holidays)")

    except Exception as e:
        print(f"      Error reading CSV file: {e}")
        return []

    return topics


def main():
    """Test function for standalone execution."""
    import sys

    csv_path = Path('clase/calendario_temas.csv')
    topics = process_calendar_topics(csv_path, verbose=True)

    # Print JSON output
    print("\nGenerated JSON:")
    print(json.dumps(topics, indent=2, ensure_ascii=False))

    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
