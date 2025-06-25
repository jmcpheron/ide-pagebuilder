#!/usr/bin/env python3
"""
Script to extract and rebuild SQL code from Banner Extensibility virtual domain JSON files.

This script addresses the code review challenge of having SQL code embedded as strings
in JSON files by extracting them into separate, reviewable .sql files.

Usage:
    python extract_virtual_domains.py extract [file_pattern]  # Extract SQL to separate files
    python extract_virtual_domains.py rebuild [file_pattern]  # Rebuild JSON from extracted files
    python extract_virtual_domains.py check [file_pattern]    # Check if extracted files are in sync
"""

import glob
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


def extract_sql_from_json(json_file: str, output_dir: str) -> Dict[str, Any]:
    """Extract SQL code blocks from a virtual domain JSON file into separate .sql files."""
    
    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)
    
    service_name = data.get("serviceName", Path(json_file).stem.replace("virtualDomains.", ""))
    domain_dir = Path(output_dir) / service_name
    domain_dir.mkdir(parents=True, exist_ok=True)
    
    # Track extracted SQL for rebuilding
    extraction_map = {
        "source_file": json_file,
        "service_name": service_name,
        "sql_blocks": []
    }
    
    # SQL code fields that might contain extractable content
    sql_fields = ["codeGet", "codePost", "codePut", "codeDelete"]
    
    for field in sql_fields:
        sql_content = data.get(field)
        if sql_content and sql_content.strip():
            # Clean up common SQL formatting issues from Banner exports
            cleaned_content = sql_content.replace('\r\n', '\n').replace('\r', '\n')
            
            filename = f"{field.lower()}.sql"
            filepath = domain_dir / filename
            
            # Write the SQL content to file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(cleaned_content)
            
            # Store mapping for rebuilding
            extraction_map["sql_blocks"].append({
                "field": field,
                "filename": filename,
                "content_hash": hashlib.md5(cleaned_content.encode()).hexdigest(),
            })
            
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
    
    # Load original JSON
    with open(source_file, encoding="utf-8") as f:
        data = json.load(f)
    
    # Read extracted SQL content back
    for sql_info in extraction_map["sql_blocks"]:
        filepath = domain_path / sql_info["filename"]
        if filepath.exists():
            with open(filepath, encoding="utf-8") as f:
                content = f.read()
                # Update the JSON with the file content
                data[sql_info["field"]] = content
    
    # Write updated JSON back
    with open(source_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
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
        
        with open(filepath, encoding="utf-8") as f:
            file_content = f.read()
        
        json_content = data.get(field, "")
        
        # Normalize line endings for comparison
        file_content_normalized = file_content.replace('\r\n', '\n').replace('\r', '\n')
        json_content_normalized = json_content.replace('\r\n', '\n').replace('\r', '\n')
        
        if file_content_normalized != json_content_normalized:
            print(f"❌ Out of sync: {filepath}")
            print(f"   File hash: {hashlib.md5(file_content_normalized.encode()).hexdigest()}")
            print(f"   JSON hash: {hashlib.md5(json_content_normalized.encode()).hexdigest()}")
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
    
    # Find virtual domain JSON files matching pattern
    json_files = []
    for file_path in glob.glob(pattern, recursive=True):
        if file_path.endswith(".json") and not file_path.endswith("_extraction_map.json"):
            # Basic check if it looks like a virtual domain definition
            try:
                with open(file_path, encoding="utf-8") as f:
                    data = json.load(f)
                    # Virtual domains have serviceName and at least one of the code fields
                    if ("serviceName" in data and 
                        any(field in data for field in ["codeGet", "codePost", "codePut", "codeDelete"])):
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
            extract_sql_from_json(json_file, output_dir)
        
        print(f"\n✅ Extraction complete! Files saved to: {output_dir}")
        print("You can now edit the extracted .sql files directly.")
        print("Run 'python extract_virtual_domains.py rebuild' to update the JSON files.")
    
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
            print("\n❌ Some files are out of sync. Run 'extract' or 'rebuild' as needed.")
            sys.exit(1)
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()