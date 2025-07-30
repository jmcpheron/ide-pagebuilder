#!/usr/bin/env python3
"""
Script to extract and rebuild literal content from Banner Extensibility page JSON files.

This script addresses the code review challenge of having HTML/CSS/JS embedded as strings
in JSON files by extracting them into separate, reviewable files.

Usage:
    python extract_literals.py extract [file_pattern]  # Extract literals to separate files
    python extract_literals.py rebuild [file_pattern]  # Rebuild JSON from extracted files
    python extract_literals.py check [file_pattern]    # Check if extracted files are in sync

Options:
    --normalize-newlines    Convert all files to Unix-style newlines (LF)
"""

import glob
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


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


def get_file_extension(content: str, component_name: str) -> str:
    """Determine appropriate file extension based on content and component name."""
    content_lower = content.lower().strip()
    name_lower = component_name.lower()

    # Check for script tags or JS-related names
    if (
        "<script" in content_lower
        or "javascript" in content_lower
        or any(js_name in name_lower for js_name in ["js", "script", "function"])
    ):
        return ".js"

    # Check for style tags or CSS-related names
    if "<style" in content_lower or any(
        css_name in name_lower for css_name in ["css", "style"]
    ):
        return ".css"

    # Default to HTML for most literal content
    return ".html"


def extract_literals_from_json(json_file: str, output_dir: str, normalize_newlines: bool = False) -> Dict[str, Any]:
    """Extract literal components from a JSON file into separate files."""

    # Read the entire file to detect newline style
    with open(json_file, 'rb') as f:
        raw_content = f.read()
    
    # Decode and detect newline style
    text_content = raw_content.decode('utf-8')
    detected_newline = detect_newline_style(text_content)
    
    # Parse JSON
    data = json.loads(text_content)

    page_name = data.get("constantName", Path(json_file).stem)
    page_dir = Path(output_dir) / page_name
    page_dir.mkdir(parents=True, exist_ok=True)

    # Track extracted literals for rebuilding
    extraction_map = {
        "source_file": json_file,
        "page_name": page_name,
        "literals": [],
        "newline_style": detected_newline if not normalize_newlines else '\n'
    }

    def extract_from_components(components: List[Dict], path: str = ""):
        """Recursively extract literals from components."""
        for i, component in enumerate(components):
            component_path = f"{path}.{i}" if path else str(i)

            if component.get("type") == "literal":
                name = component.get("name", f"unnamed_{i}")
                content = component.get("value", "")

                if content.strip():  # Only extract non-empty content
                    ext = get_file_extension(content, name)
                    filename = f"{name}{ext}"
                    filepath = page_dir / filename

                    # Normalize newlines if requested
                    if normalize_newlines:
                        # Normalize all types of newlines to Unix style
                        content = content.replace('\r\n', '\n').replace('\r', '\n')
                    
                    # Write the content to file preserving newline style
                    with open(filepath, 'wb') as f:
                        f.write(content.encode('utf-8'))

                    # Store mapping for rebuilding
                    extraction_map["literals"].append(
                        {
                            "component_path": component_path,
                            "name": name,
                            "filename": filename,
                            "content_hash": hashlib.md5(content.encode()).hexdigest(),
                        }
                    )

                    print(f"Extracted: {filepath}")

            # Recursively check nested components
            if "components" in component:
                extract_from_components(
                    component["components"], f"{component_path}.components"
                )

    # Extract from main components
    if "modelView" in data and "components" in data["modelView"]:
        extract_from_components(data["modelView"]["components"])

    # Save extraction mapping
    map_file = page_dir / "_extraction_map.json"
    with open(map_file, "w", encoding="utf-8") as f:
        json.dump(extraction_map, f, indent=2)

    print(f"Extraction map saved: {map_file}")
    return extraction_map


def rebuild_json_from_literals(page_dir: str) -> str:
    """Rebuild JSON file from extracted literal files."""

    page_path = Path(page_dir)
    map_file = page_path / "_extraction_map.json"

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

    # Read extracted content back
    literal_content = {}
    for literal_info in extraction_map["literals"]:
        filepath = page_path / literal_info["filename"]
        if filepath.exists():
            with open(filepath, 'rb') as f:
                content = f.read().decode('utf-8')
                literal_content[literal_info["component_path"]] = content

    def update_components(components: List[Dict], path: str = ""):
        """Recursively update literal components with file content."""
        for i, component in enumerate(components):
            component_path = f"{path}.{i}" if path else str(i)

            if component.get("type") == "literal" and component_path in literal_content:
                component["value"] = literal_content[component_path]

            # Recursively update nested components
            if "components" in component:
                update_components(
                    component["components"], f"{component_path}.components"
                )

    # Update main components
    if "modelView" in data and "components" in data["modelView"]:
        update_components(data["modelView"]["components"])

    # Write updated JSON back with proper newline handling
    json_str = json.dumps(data, indent=3, ensure_ascii=False)
    
    # Convert newlines to match the original file's style
    if newline_style != '\n':
        json_str = json_str.replace('\n', newline_style)
    
    with open(source_file, 'wb') as f:
        f.write(json_str.encode('utf-8'))

    print(f"Rebuilt: {source_file}")
    return source_file


def check_sync_status(page_dir: str) -> bool:
    """Check if extracted files are in sync with the source JSON."""

    page_path = Path(page_dir)
    map_file = page_path / "_extraction_map.json"

    if not map_file.exists():
        print(f"❌ No extraction map found: {map_file}")
        return False

    with open(map_file, encoding="utf-8") as f:
        extraction_map = json.load(f)

    source_file = extraction_map["source_file"]

    if not os.path.exists(source_file):
        print(f"❌ Source file not found: {source_file}")
        return False

    # Load current JSON and extract current literal content
    with open(source_file, encoding="utf-8") as f:
        data = json.load(f)

    def get_literal_content(components: List[Dict], path: str = "") -> Dict[str, str]:
        """Extract current literal content from JSON."""
        content = {}
        for i, component in enumerate(components):
            component_path = f"{path}.{i}" if path else str(i)

            if component.get("type") == "literal":
                content[component_path] = component.get("value", "")

            if "components" in component:
                content.update(
                    get_literal_content(
                        component["components"], f"{component_path}.components"
                    )
                )

        return content

    current_content = {}
    if "modelView" in data and "components" in data["modelView"]:
        current_content = get_literal_content(data["modelView"]["components"])

    # Check each extracted file
    all_synced = True
    for literal_info in extraction_map["literals"]:
        filepath = page_path / literal_info["filename"]
        component_path = literal_info["component_path"]

        if not filepath.exists():
            print(f"❌ Missing extracted file: {filepath}")
            all_synced = False
            continue

        with open(filepath, 'rb') as f:
            file_content = f.read().decode('utf-8')

        json_content = current_content.get(component_path, "")

        if file_content != json_content:
            print(f"❌ Out of sync: {filepath}")
            print(f"   File hash: {hashlib.md5(file_content.encode()).hexdigest()}")
            print(f"   JSON hash: {hashlib.md5(json_content.encode()).hexdigest()}")
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

    # Find JSON files matching pattern
    json_files = []
    for file_path in glob.glob(pattern, recursive=True):
        if file_path.endswith(".json") and not file_path.endswith(
            "_extraction_map.json"
        ):
            # Basic check if it looks like a page definition
            try:
                with open(file_path, encoding="utf-8") as f:
                    data = json.load(f)
                    if "constantName" in data and "modelView" in data:
                        json_files.append(file_path)
            except (json.JSONDecodeError, KeyError):
                continue

    if not json_files:
        print(f"No page JSON files found matching pattern: {pattern}")
        sys.exit(1)

    output_dir = "extracted_literals"

    if command == "extract":
        print(f"Extracting literals from {len(json_files)} files...")
        for json_file in json_files:
            print(f"\nProcessing: {json_file}")
            extract_literals_from_json(json_file, output_dir, normalize_newlines)

        print(f"\n✅ Extraction complete! Files saved to: {output_dir}")
        print("You can now edit the extracted HTML/CSS/JS files directly.")
        print("Run 'python extract_literals.py rebuild' to update the JSON files.")

    elif command == "rebuild":
        print("Rebuilding JSON files from extracted literals...")

        # Find all page directories
        for page_dir in Path(output_dir).iterdir():
            if page_dir.is_dir() and (page_dir / "_extraction_map.json").exists():
                print(f"\nRebuilding: {page_dir.name}")
                rebuild_json_from_literals(str(page_dir))

        print("\n✅ Rebuild complete!")

    elif command == "check":
        print("Checking sync status...")

        all_synced = True
        for page_dir in Path(output_dir).iterdir():
            if page_dir.is_dir() and (page_dir / "_extraction_map.json").exists():
                print(f"\nChecking: {page_dir.name}")
                if not check_sync_status(str(page_dir)):
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
