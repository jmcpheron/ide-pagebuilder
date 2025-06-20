#!/usr/bin/env python3
"""
Script to extract and rebuild literal content from Banner Extensibility page JSON files.

This script addresses the code review challenge of having HTML/CSS/JS embedded as strings
in JSON files by extracting them into separate, reviewable files.

Usage:
    python extract_literals.py extract [file_pattern]  # Extract literals to separate files
    python extract_literals.py rebuild [file_pattern]  # Rebuild JSON from extracted files
    python extract_literals.py check [file_pattern]    # Check if extracted files are in sync
"""

import json
import os
import sys
import glob
import re
from pathlib import Path
from typing import Dict, List, Any
import hashlib


def get_file_extension(content: str, component_name: str) -> str:
    """Determine appropriate file extension based on content and component name."""
    content_lower = content.lower().strip()
    name_lower = component_name.lower()
    
    # Check for script tags or JS-related names
    if '<script' in content_lower or 'javascript' in content_lower or any(js_name in name_lower for js_name in ['js', 'script', 'function']):
        return '.js'
    
    # Check for style tags or CSS-related names  
    if '<style' in content_lower or any(css_name in name_lower for css_name in ['css', 'style']):
        return '.css'
    
    # Default to HTML for most literal content
    return '.html'


def extract_literals_from_json(json_file: str, output_dir: str) -> Dict[str, Any]:
    """Extract literal components from a JSON file into separate files."""
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    page_name = data.get('constantName', Path(json_file).stem)
    page_dir = Path(output_dir) / page_name
    page_dir.mkdir(parents=True, exist_ok=True)
    
    # Track extracted literals for rebuilding
    extraction_map = {
        'source_file': json_file,
        'page_name': page_name,
        'literals': []
    }
    
    def extract_from_components(components: List[Dict], path: str = ""):
        """Recursively extract literals from components."""
        for i, component in enumerate(components):
            component_path = f"{path}.{i}" if path else str(i)
            
            if component.get('type') == 'literal':
                name = component.get('name', f'unnamed_{i}')
                content = component.get('value', '')
                
                if content.strip():  # Only extract non-empty content
                    ext = get_file_extension(content, name)
                    filename = f"{name}{ext}"
                    filepath = page_dir / filename
                    
                    # Write the content to file
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    # Store mapping for rebuilding
                    extraction_map['literals'].append({
                        'component_path': component_path,
                        'name': name,
                        'filename': filename,
                        'content_hash': hashlib.md5(content.encode()).hexdigest()
                    })
                    
                    print(f"Extracted: {filepath}")
            
            # Recursively check nested components
            if 'components' in component:
                extract_from_components(component['components'], f"{component_path}.components")
    
    # Extract from main components
    if 'modelView' in data and 'components' in data['modelView']:
        extract_from_components(data['modelView']['components'])
    
    # Save extraction mapping
    map_file = page_dir / '_extraction_map.json'
    with open(map_file, 'w', encoding='utf-8') as f:
        json.dump(extraction_map, f, indent=2)
    
    print(f"Extraction map saved: {map_file}")
    return extraction_map


def rebuild_json_from_literals(page_dir: str) -> str:
    """Rebuild JSON file from extracted literal files."""
    
    page_path = Path(page_dir)
    map_file = page_path / '_extraction_map.json'
    
    if not map_file.exists():
        raise FileNotFoundError(f"Extraction map not found: {map_file}")
    
    with open(map_file, 'r', encoding='utf-8') as f:
        extraction_map = json.load(f)
    
    source_file = extraction_map['source_file']
    
    # Load original JSON
    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Read extracted content back
    literal_content = {}
    for literal_info in extraction_map['literals']:
        filepath = page_path / literal_info['filename']
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                literal_content[literal_info['component_path']] = content
    
    def update_components(components: List[Dict], path: str = ""):
        """Recursively update literal components with file content."""
        for i, component in enumerate(components):
            component_path = f"{path}.{i}" if path else str(i)
            
            if component.get('type') == 'literal' and component_path in literal_content:
                component['value'] = literal_content[component_path]
            
            # Recursively update nested components  
            if 'components' in component:
                update_components(component['components'], f"{component_path}.components")
    
    # Update main components
    if 'modelView' in data and 'components' in data['modelView']:
        update_components(data['modelView']['components'])
    
    # Write updated JSON back
    with open(source_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=3, ensure_ascii=False)
    
    print(f"Rebuilt: {source_file}")
    return source_file


def check_sync_status(page_dir: str) -> bool:
    """Check if extracted files are in sync with the source JSON."""
    
    page_path = Path(page_dir)
    map_file = page_path / '_extraction_map.json'
    
    if not map_file.exists():
        print(f"❌ No extraction map found: {map_file}")
        return False
    
    with open(map_file, 'r', encoding='utf-8') as f:
        extraction_map = json.load(f)
    
    source_file = extraction_map['source_file']
    
    if not os.path.exists(source_file):
        print(f"❌ Source file not found: {source_file}")
        return False
    
    # Load current JSON and extract current literal content
    with open(source_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    def get_literal_content(components: List[Dict], path: str = "") -> Dict[str, str]:
        """Extract current literal content from JSON."""
        content = {}
        for i, component in enumerate(components):
            component_path = f"{path}.{i}" if path else str(i)
            
            if component.get('type') == 'literal':
                content[component_path] = component.get('value', '')
            
            if 'components' in component:
                content.update(get_literal_content(component['components'], f"{component_path}.components"))
        
        return content
    
    current_content = {}
    if 'modelView' in data and 'components' in data['modelView']:
        current_content = get_literal_content(data['modelView']['components'])
    
    # Check each extracted file
    all_synced = True
    for literal_info in extraction_map['literals']:
        filepath = page_path / literal_info['filename']
        component_path = literal_info['component_path']
        
        if not filepath.exists():
            print(f"❌ Missing extracted file: {filepath}")
            all_synced = False
            continue
        
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        json_content = current_content.get(component_path, '')
        
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
    pattern = sys.argv[2] if len(sys.argv) > 2 else "**/*.json"
    
    # Find JSON files matching pattern
    json_files = []
    for file_path in glob.glob(pattern, recursive=True):
        if file_path.endswith('.json') and not file_path.endswith('_extraction_map.json'):
            # Basic check if it looks like a page definition
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if 'constantName' in data and 'modelView' in data:
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
            extract_literals_from_json(json_file, output_dir)
        
        print(f"\n✅ Extraction complete! Files saved to: {output_dir}")
        print("You can now edit the extracted HTML/CSS/JS files directly.")
        print("Run 'python extract_literals.py rebuild' to update the JSON files.")
    
    elif command == "rebuild":
        print(f"Rebuilding JSON files from extracted literals...")
        
        # Find all page directories
        for page_dir in Path(output_dir).iterdir():
            if page_dir.is_dir() and (page_dir / '_extraction_map.json').exists():
                print(f"\nRebuilding: {page_dir.name}")
                rebuild_json_from_literals(str(page_dir))
        
        print("\n✅ Rebuild complete!")
    
    elif command == "check":
        print(f"Checking sync status...")
        
        all_synced = True
        for page_dir in Path(output_dir).iterdir():
            if page_dir.is_dir() and (page_dir / '_extraction_map.json').exists():
                print(f"\nChecking: {page_dir.name}")
                if not check_sync_status(str(page_dir)):
                    all_synced = False
        
        if all_synced:
            print("\n✅ All files are in sync!")
            sys.exit(0)
        else:
            print("\n❌ Some files are out of sync. Run 'extract' or 'rebuild' as needed.")
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()