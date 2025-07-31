#!/usr/bin/env python3
"""
Script to extract and rebuild SQL code from Banner Extensibility virtual domain JSON files.

This script addresses the code review challenge of having SQL code embedded as strings
in JSON files by extracting them into separate, reviewable .sql files.

Usage:
    python extract_virtual_domains.py extract [file_pattern]  # Extract SQL to separate files
    python extract_virtual_domains.py rebuild [file_pattern]  # Rebuild JSON from extracted files
    python extract_virtual_domains.py check [file_pattern]    # Check if extracted files are in sync

Options:
    --normalize-newlines    Convert all files to Unix-style newlines (LF)
"""

import glob
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def detect_newline_style(content: str) -> str:
    """Detect the predominant newline style in content."""
    if not content:
        return '\n'  # Default to Unix style
    
    # Count different newline types
    crlf_count = content.count('\r\n')
    lf_count = content.count('\n') - crlf_count  # Subtract CRLF occurrences
    cr_count = content.count('\r') - crlf_count  # Subtract CRLF occurrences
    
    # Return the most common style
    if crlf_count > max(lf_count, cr_count):
        return '\r\n'
    elif cr_count > lf_count:
        return '\r'
    else:
        return '\n'


def extract_sql_from_json(json_file: str, output_dir: str, normalize_newlines: bool = False) -> Dict[str, Any]:
    """Extract SQL code blocks from a virtual domain JSON file into separate .sql files."""

    # Read the entire file to detect newline style
    with open(json_file, 'rb') as f:
        raw_content = f.read()
    
    # Decode and detect newline style
    text_content = raw_content.decode('utf-8')
    detected_newline = detect_newline_style(text_content)
    
    # Parse JSON
    data = json.loads(text_content)

    service_name = data.get(
        "serviceName", Path(json_file).stem.replace("virtualDomains.", "")
    )
    domain_dir = Path(output_dir) / service_name
    domain_dir.mkdir(parents=True, exist_ok=True)

    # Track extracted SQL for rebuilding
    extraction_map = {
        "source_file": json_file,
        "service_name": service_name,
        "sql_blocks": [],
        "newline_style": detected_newline if not normalize_newlines else '\n'
    }

    # SQL code fields that might contain extractable content
    sql_fields = ["codeGet", "codePost", "codePut", "codeDelete"]

    for field in sql_fields:
        sql_content = data.get(field)
        if sql_content and sql_content.strip():
            # Normalize newlines if requested
            if normalize_newlines:
                sql_content = sql_content.replace("\r\n", "\n").replace("\r", "\n")

            filename = f"{field.lower()}.sql"
            filepath = domain_dir / filename

            # Write the SQL content to file preserving newline style
            with open(filepath, 'wb') as f:
                f.write(sql_content.encode('utf-8'))

            # Store mapping for rebuilding
            extraction_map["sql_blocks"].append(
                {
                    "field": field,
                    "filename": filename,
                    "content_hash": hashlib.md5(sql_content.encode()).hexdigest(),
                }
            )

            print(f"Extracted: {filepath}")

    # Save extraction mapping if we extracted any SQL
    if extraction_map["sql_blocks"]:
        map_file = domain_dir / "_extraction_map.json"
        with open(map_file, "w", encoding="utf-8") as f:
            json.dump(extraction_map, f, indent=2)

        print(f"Extraction map saved: {map_file}")
    else:
        print(f"No SQL content found in: {json_file}")

    return extraction_map


def rebuild_json_from_sql(domain_dir: str) -> str:
    """Rebuild JSON file from extracted SQL files."""

    domain_path = Path(domain_dir)
    map_file = domain_path / "_extraction_map.json"

    if not map_file.exists():
        raise FileNotFoundError(f"Extraction map not found: {map_file}")

    with open(map_file, encoding="utf-8") as f:
        extraction_map = json.load(f)

    source_file = extraction_map["source_file"]

    # Load original JSON preserving format
    with open(source_file, 'rb') as f:
        raw_content = f.read()
    
    text_content = raw_content.decode('utf-8')
    data = json.loads(text_content)
    
    # Get the newline style to use
    newline_style = extraction_map.get('newline_style', '\n')

    # Read extracted SQL content back
    for sql_info in extraction_map["sql_blocks"]:
        filepath = domain_path / sql_info["filename"]
        if filepath.exists():
            with open(filepath, 'rb') as f:
                content = f.read().decode('utf-8')
                # Update the JSON with the file content
                data[sql_info["field"]] = content

    # Write updated JSON back with proper newline handling
    json_str = json.dumps(data, indent=2, ensure_ascii=False)
    
    # Convert newlines to match the original file's style
    if newline_style != '\n':
        json_str = json_str.replace('\n', newline_style)
    
    with open(source_file, 'wb') as f:
        f.write(json_str.encode('utf-8'))

    print(f"Rebuilt: {source_file}")
    return source_file


def check_sync_status(domain_dir: str) -> bool:
    """Check if extracted SQL files are in sync with the source JSON."""

    domain_path = Path(domain_dir)
    map_file = domain_path / "_extraction_map.json"

    if not map_file.exists():
        print(f"❌ No extraction map found: {map_file}")
        return False

    with open(map_file, encoding="utf-8") as f:
        extraction_map = json.load(f)

    source_file = extraction_map["source_file"]

    if not os.path.exists(source_file):
        print(f"❌ Source file not found: {source_file}")
        return False

    # Load current JSON
    with open(source_file, encoding="utf-8") as f:
        data = json.load(f)

    # Check each extracted SQL file
    all_synced = True
    for sql_info in extraction_map["sql_blocks"]:
        filepath = domain_path / sql_info["filename"]
        field = sql_info["field"]

        if not filepath.exists():
            print(f"❌ Missing extracted file: {filepath}")
            all_synced = False
            continue

        with open(filepath, 'rb') as f:
            file_content = f.read().decode('utf-8')

        json_content = data.get(field, "")

        # Normalize line endings for comparison
        file_content_normalized = file_content.replace("\r\n", "\n").replace("\r", "\n")
        json_content_normalized = json_content.replace("\r\n", "\n").replace("\r", "\n")

        if file_content_normalized != json_content_normalized:
            print(f"❌ Out of sync: {filepath}")
            print(
                f"   File hash: {hashlib.md5(file_content_normalized.encode()).hexdigest()}"
            )
            print(
                f"   JSON hash: {hashlib.md5(json_content_normalized.encode()).hexdigest()}"
            )
            all_synced = False
        else:
            print(f"✅ In sync: {filepath}")

    return all_synced


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    
    # Check for --normalize-newlines flag
    normalize_newlines = '--normalize-newlines' in sys.argv
    if normalize_newlines:
        sys.argv.remove('--normalize-newlines')
    
    pattern = sys.argv[2] if len(sys.argv) > 2 else "**/*.json"

    # Find virtual domain JSON files matching pattern
    json_files = []
    for file_path in glob.glob(pattern, recursive=True):
        if file_path.endswith(".json") and not file_path.endswith(
            "_extraction_map.json"
        ):
            # Basic check if it looks like a virtual domain definition
            try:
                with open(file_path, encoding="utf-8") as f:
                    data = json.load(f)
                    # Virtual domains have serviceName and at least one of the code fields
                    if "serviceName" in data and any(
                        field in data
                        for field in ["codeGet", "codePost", "codePut", "codeDelete"]
                    ):
                        json_files.append(file_path)
            except (json.JSONDecodeError, KeyError):
                continue

    if not json_files:
        print(f"No virtual domain JSON files found matching pattern: {pattern}")
        sys.exit(1)

    output_dir = "extracted_virtual_domains"

    if command == "extract":
        print(f"Extracting SQL from {len(json_files)} virtual domain files...")
        for json_file in json_files:
            print(f"\nProcessing: {json_file}")
            extract_sql_from_json(json_file, output_dir, normalize_newlines)

        print(f"\n✅ Extraction complete! Files saved to: {output_dir}")
        print("You can now edit the extracted .sql files directly.")
        print(
            "Run 'python extract_virtual_domains.py rebuild' to update the JSON files."
        )

    elif command == "rebuild":
        print("Rebuilding JSON files from extracted SQL...")

        # Find all domain directories
        for domain_dir in Path(output_dir).iterdir():
            if domain_dir.is_dir() and (domain_dir / "_extraction_map.json").exists():
                print(f"\nRebuilding: {domain_dir.name}")
                rebuild_json_from_sql(str(domain_dir))

        print("\n✅ Rebuild complete!")

    elif command == "check":
        print("Checking sync status...")

        all_synced = True
        for domain_dir in Path(output_dir).iterdir():
            if domain_dir.is_dir() and (domain_dir / "_extraction_map.json").exists():
                print(f"\nChecking: {domain_dir.name}")
                if not check_sync_status(str(domain_dir)):
                    all_synced = False

        if all_synced:
            print("\n✅ All files are in sync!")
            sys.exit(0)
        else:
            print(
                "\n❌ Some files are out of sync. Run 'extract' or 'rebuild' as needed."
            )
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
