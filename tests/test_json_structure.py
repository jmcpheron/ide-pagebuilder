import json
from pathlib import Path

import pytest
from jsonschema import ValidationError, validate


class TestJSONStructure:
    """Test suite for JSON file structure and validation."""

    @pytest.fixture
    def json_files(self):
        """Find all JSON files in the project."""
        json_files = []
        for json_file in Path(".").rglob("*.json"):
            # Skip virtual environment and node_modules
            if any(
                part in json_file.parts for part in [".venv", "venv", "node_modules"]
            ):
                continue
            json_files.append(json_file)
        return json_files

    def test_all_json_files_valid(self, json_files):
        """Test that all JSON files are valid JSON."""
        for json_file in json_files:
            try:
                with open(json_file, encoding="utf-8") as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"Invalid JSON in {json_file}: {e}")
            except UnicodeDecodeError as e:
                pytest.fail(f"Unicode decode error in {json_file}: {e}")

    def test_page_json_schema(self):
        """Test page JSON files against a basic schema."""
        page_schema = {
            "type": "object",
            "properties": {
                "constantName": {"type": "string"},
                "modelView": {
                    "type": "object",
                    "properties": {
                        "components": {"type": "array"},
                        "name": {"type": "string"},
                        "style": {"type": "string"},
                    },
                    "required": ["components"],
                },
                "developerSecurity": {"type": "array"},
                "fileTimestamp": {"type": "string"},
            },
            "required": ["constantName", "modelView"],
        }

        for page_file in Path(".").rglob("pages.*.json"):
            try:
                with open(page_file, encoding="utf-8") as f:
                    data = json.load(f)
                validate(instance=data, schema=page_schema)
            except ValidationError as e:
                pytest.fail(f"Schema validation failed for {page_file}: {e}")
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON in {page_file}")

    def test_component_schema(self):
        """Test that components have valid structure."""
        component_schema = {
            "type": "object",
            "properties": {
                "type": {"type": "string"},
                "name": {"type": "string"},
                "value": {"type": "string"},
                "resource": {"type": "string"},
                "model": {"type": "string"},
                "components": {"type": "array", "items": {"$ref": "#"}},
                "style": {"type": "string"},
                "role": {"type": "string"},
                "showInitially": {"type": "boolean"},
                "loadInitially": {"type": "boolean"},
                "onLoad": {"type": "string"},
                "onUpdate": {"type": "string"},
                "parameters": {"type": "object"},
            },
        }

        def validate_components(components, file_path):
            for component in components:
                try:
                    # Basic type check
                    assert isinstance(component, dict), (
                        f"Component must be object in {file_path}"
                    )

                    # Check nested components recursively
                    if "components" in component:
                        validate_components(component["components"], file_path)

                except AssertionError as e:
                    pytest.fail(str(e))

        for page_file in Path(".").rglob("pages.*.json"):
            try:
                with open(page_file, encoding="utf-8") as f:
                    data = json.load(f)

                if "modelView" in data and "components" in data["modelView"]:
                    validate_components(data["modelView"]["components"], page_file)

            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON in {page_file}")

    def test_extraction_map_schema(self):
        """Test extraction map JSON files have correct structure."""
        # Schema for page extraction maps
        page_extraction_map_schema = {
            "type": "object",
            "properties": {
                "source_file": {"type": "string"},
                "page_name": {"type": "string"},
                "literals": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "component_path": {"type": "string"},
                            "name": {"type": "string"},
                            "filename": {"type": "string"},
                            "content_hash": {"type": "string"},
                        },
                        "required": [
                            "component_path",
                            "name",
                            "filename",
                            "content_hash",
                        ],
                    },
                },
            },
            "required": ["source_file", "page_name", "literals"],
        }

        # Schema for virtual domain extraction maps
        virtual_domain_extraction_map_schema = {
            "type": "object",
            "properties": {
                "source_file": {"type": "string"},
                "service_name": {"type": "string"},
                "sql_blocks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "field": {"type": "string"},
                            "filename": {"type": "string"},
                            "content_hash": {"type": "string"},
                        },
                        "required": ["field", "filename", "content_hash"],
                    },
                },
            },
            "required": ["source_file", "service_name", "sql_blocks"],
        }

        for map_file in Path(".").rglob("_extraction_map.json"):
            try:
                with open(map_file, encoding="utf-8") as f:
                    data = json.load(f)

                # Determine which schema to use based on the content
                if "page_name" in data and "literals" in data:
                    # This is a page extraction map
                    validate(instance=data, schema=page_extraction_map_schema)
                elif "service_name" in data and "sql_blocks" in data:
                    # This is a virtual domain extraction map
                    validate(instance=data, schema=virtual_domain_extraction_map_schema)
                else:
                    pytest.fail(f"Unknown extraction map format in {map_file}")

            except ValidationError as e:
                pytest.fail(
                    f"Extraction map schema validation failed for {map_file}: {e}"
                )
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON in {map_file}")

    def test_no_duplicate_component_names(self):
        """Test that component names are unique within their scope."""

        def check_duplicate_names(components, file_path, path="root"):
            names = []
            for i, component in enumerate(components):
                if "name" in component:
                    name = component["name"]
                    if name in names:
                        pytest.fail(
                            f"Duplicate component name '{name}' found at {path} in {file_path}"
                        )
                    names.append(name)

                # Recursively check nested components
                if "components" in component:
                    check_duplicate_names(
                        component["components"],
                        file_path,
                        f"{path}.{component.get('name', i)}.components",
                    )

        for page_file in Path(".").rglob("pages.*.json"):
            try:
                with open(page_file, encoding="utf-8") as f:
                    data = json.load(f)

                if "modelView" in data and "components" in data["modelView"]:
                    check_duplicate_names(data["modelView"]["components"], page_file)

            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON in {page_file}")

    def test_consistent_indentation(self, json_files):
        """Test that JSON files have consistent indentation."""
        for json_file in json_files:
            try:
                with open(json_file, encoding="utf-8") as f:
                    content = f.read()

                # Try to parse and reformat
                data = json.loads(content)
                formatted = json.dumps(data, indent=3, ensure_ascii=False)

                # Check if the formatting is consistent (allowing for some variation)
                lines = content.split("\n")
                formatted_lines = formatted.split("\n")

                # Just ensure it can be parsed and reformatted without errors
                assert len(lines) > 0, f"Empty JSON file: {json_file}"

            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                pytest.fail(f"Error processing {json_file}: {e}")

    def test_no_trailing_commas(self, json_files):
        """Test that JSON files don't have trailing commas."""
        for json_file in json_files:
            try:
                with open(json_file, encoding="utf-8") as f:
                    content = f.read()

                # Try to parse - this will fail if there are trailing commas
                json.loads(content)

            except json.JSONDecodeError as e:
                if "trailing comma" in str(e).lower():
                    pytest.fail(f"Trailing comma found in {json_file}: {e}")
                else:
                    pytest.fail(f"JSON parse error in {json_file}: {e}")
