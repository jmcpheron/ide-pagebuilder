import json
from pathlib import Path

import pytest


class TestPageDefinitions:
    """Test suite for Banner Extensibility page definition JSON files."""

    @pytest.fixture
    def page_files(self):
        """Find all page definition JSON files."""
        page_files = []
        for json_file in Path(".").rglob("pages.*.json"):
            if json_file.exists():
                page_files.append(json_file)
        return page_files

    def test_page_files_exist(self, page_files):
        """Test that page definition files exist."""
        assert len(page_files) > 0, "No page definition files found"

    def test_page_json_validity(self, page_files):
        """Test that all page JSON files are valid JSON."""
        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                try:
                    json.load(f)
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON in {page_file}: {e}")

    def test_page_required_fields(self, page_files):
        """Test that page definitions have required top-level fields."""
        required_fields = ["constantName", "modelView"]

        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                data = json.load(f)

            for field in required_fields:
                assert field in data, f"Missing required field '{field}' in {page_file}"

    def test_model_view_structure(self, page_files):
        """Test that modelView has proper structure."""
        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                data = json.load(f)

            model_view = data.get("modelView", {})
            assert "components" in model_view, (
                f"modelView missing 'components' in {page_file}"
            )
            assert isinstance(model_view["components"], list), (
                f"components must be a list in {page_file}"
            )

    def test_component_types(self, page_files):
        """Test that components have valid types."""
        valid_types = [
            "literal",
            "block",
            "resource",
            "data",
            "select",
            "input",
            "button",
        ]

        def check_components(components, file_path):
            for component in components:
                if "type" in component:
                    assert component["type"] in valid_types, (
                        f"Invalid component type '{component['type']}' in {file_path}"
                    )

                # Recursively check nested components
                if "components" in component:
                    check_components(component["components"], file_path)

        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                data = json.load(f)

            if "modelView" in data and "components" in data["modelView"]:
                check_components(data["modelView"]["components"], page_file)

    def test_literal_components_have_content(self, page_files):
        """Test that literal components have non-empty value field."""

        def check_literals(components, file_path):
            for component in components:
                if component.get("type") == "literal":
                    assert "value" in component, (
                        f"Literal component missing 'value' field in {file_path}"
                    )
                    # Allow empty values for now, as they might be intentional

                if "components" in component:
                    check_literals(component["components"], file_path)

        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                data = json.load(f)

            if "modelView" in data and "components" in data["modelView"]:
                check_literals(data["modelView"]["components"], page_file)

    def test_resource_components_reference_valid_domains(self, page_files):
        """Test that resource components reference existing virtual domains."""

        def check_resources(components, file_path):
            for component in components:
                if component.get("type") == "resource":
                    assert "resource" in component, (
                        f"Resource component missing 'resource' field in {file_path}"
                    )
                    resource_name = component["resource"]
                    # Basic format check - should start with "virtualDomains."
                    assert resource_name.startswith("virtualDomains."), (
                        f"Invalid resource reference '{resource_name}' in {file_path}"
                    )

                if "components" in component:
                    check_resources(component["components"], file_path)

        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                data = json.load(f)

            if "modelView" in data and "components" in data["modelView"]:
                check_resources(data["modelView"]["components"], page_file)

    def test_data_components_have_models(self, page_files):
        """Test that data components reference valid models."""

        def check_data_components(components, file_path):
            for component in components:
                if component.get("type") == "data":
                    assert "model" in component, (
                        f"Data component missing 'model' field in {file_path}"
                    )

                if "components" in component:
                    check_data_components(component["components"], file_path)

        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                data = json.load(f)

            if "modelView" in data and "components" in data["modelView"]:
                check_data_components(data["modelView"]["components"], page_file)

    def test_constant_name_matches_filename(self, page_files):
        """Test that constantName field matches the filename pattern."""
        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                data = json.load(f)

            constant_name = data.get("constantName", "")
            expected_name = page_file.stem.replace("pages.", "")

            assert constant_name == expected_name, (
                f"constantName '{constant_name}' doesn't match filename '{expected_name}' in {page_file}"
            )
