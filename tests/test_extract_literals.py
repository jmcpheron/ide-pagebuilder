import json

# Import the functions we want to test
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from extract_literals import (
    check_sync_status,
    extract_literals_from_json,
    get_file_extension,
    rebuild_json_from_literals,
)


class TestExtractLiterals:
    """Test suite for the extract_literals.py functionality."""

    def test_get_file_extension_js(self):
        """Test file extension detection for JavaScript content."""
        assert get_file_extension('<script>alert("test")</script>', "test") == ".js"
        assert get_file_extension("function test() {}", "js_function") == ".js"
        assert get_file_extension('console.log("test")', "script_code") == ".js"
        assert get_file_extension("var x = 1;", "functions") == ".js"

    def test_get_file_extension_css(self):
        """Test file extension detection for CSS content."""
        assert (
            get_file_extension("<style>.test { color: red; }</style>", "test") == ".css"
        )
        assert get_file_extension(".class { margin: 0; }", "css_styles") == ".css"
        assert get_file_extension("body { background: white; }", "styles") == ".css"
        assert get_file_extension("div { padding: 10px; }", "style") == ".css"

    def test_get_file_extension_html(self):
        """Test file extension detection for HTML content."""
        assert get_file_extension("<div>Hello World</div>", "test") == ".html"
        assert get_file_extension("<p>Test content</p>", "test") == ".html"
        assert get_file_extension("Plain text content", "test") == ".html"
        assert (
            get_file_extension("<h1>Title</h1><p>Content</p>", "main_content")
            == ".html"
        )

    def test_extract_literals_from_json_basic(self):
        """Test basic literal extraction from JSON."""
        # Create a temporary JSON file
        test_data = {
            "constantName": "test_page",
            "modelView": {
                "components": [
                    {
                        "type": "literal",
                        "name": "test_content",
                        "value": "<div>Hello World</div>",
                    }
                ]
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "test.json"
            with open(json_file, "w") as f:
                json.dump(test_data, f)

            output_dir = Path(temp_dir) / "output"
            extraction_map = extract_literals_from_json(str(json_file), str(output_dir))

            # Check that extraction map was created
            assert extraction_map["page_name"] == "test_page"
            assert len(extraction_map["literals"]) == 1

            # Check that the literal file was created
            literal_file = output_dir / "test_page" / "test_content.html"
            assert literal_file.exists()

            with open(literal_file) as f:
                content = f.read()
            assert content == "<div>Hello World</div>"

    def test_extract_literals_nested_components(self):
        """Test extraction from nested components."""
        test_data = {
            "constantName": "nested_test",
            "modelView": {
                "components": [
                    {
                        "type": "block",
                        "name": "container",
                        "components": [
                            {
                                "type": "literal",
                                "name": "nested_content",
                                "value": "<p>Nested content</p>",
                            }
                        ],
                    }
                ]
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "nested.json"
            with open(json_file, "w") as f:
                json.dump(test_data, f)

            output_dir = Path(temp_dir) / "output"
            extraction_map = extract_literals_from_json(str(json_file), str(output_dir))

            assert len(extraction_map["literals"]) == 1
            assert extraction_map["literals"][0]["component_path"] == "0.components.0"

            literal_file = output_dir / "nested_test" / "nested_content.html"
            assert literal_file.exists()

    def test_extract_literals_skip_empty(self):
        """Test that empty literals are skipped."""
        test_data = {
            "constantName": "empty_test",
            "modelView": {
                "components": [
                    {"type": "literal", "name": "empty_content", "value": ""},
                    {
                        "type": "literal",
                        "name": "whitespace_content",
                        "value": "   \n\t  ",
                    },
                    {
                        "type": "literal",
                        "name": "real_content",
                        "value": "<div>Real content</div>",
                    },
                ]
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "empty.json"
            with open(json_file, "w") as f:
                json.dump(test_data, f)

            output_dir = Path(temp_dir) / "output"
            extraction_map = extract_literals_from_json(str(json_file), str(output_dir))

            # Should only extract the non-empty content
            assert len(extraction_map["literals"]) == 1
            assert extraction_map["literals"][0]["name"] == "real_content"

    def test_rebuild_json_from_literals(self):
        """Test rebuilding JSON from extracted literals."""
        test_data = {
            "constantName": "rebuild_test",
            "modelView": {
                "components": [
                    {
                        "type": "literal",
                        "name": "test_content",
                        "value": "<div>Original content</div>",
                    }
                ]
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "rebuild.json"
            with open(json_file, "w") as f:
                json.dump(test_data, f)

            output_dir = Path(temp_dir) / "output"

            # Extract first
            extract_literals_from_json(str(json_file), str(output_dir))

            # Modify the extracted file
            literal_file = output_dir / "rebuild_test" / "test_content.html"
            with open(literal_file, "w") as f:
                f.write("<div>Modified content</div>")

            # Rebuild
            rebuild_json_from_literals(str(output_dir / "rebuild_test"))

            # Check that JSON was updated
            with open(json_file) as f:
                updated_data = json.load(f)

            assert (
                updated_data["modelView"]["components"][0]["value"]
                == "<div>Modified content</div>"
            )

    def test_check_sync_status_in_sync(self):
        """Test sync status check when files are in sync."""
        test_data = {
            "constantName": "sync_test",
            "modelView": {
                "components": [
                    {
                        "type": "literal",
                        "name": "test_content",
                        "value": "<div>Sync test</div>",
                    }
                ]
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "sync.json"
            with open(json_file, "w") as f:
                json.dump(test_data, f)

            output_dir = Path(temp_dir) / "output"

            # Extract literals
            extract_literals_from_json(str(json_file), str(output_dir))

            # Check sync status
            is_synced = check_sync_status(str(output_dir / "sync_test"))
            assert is_synced is True

    def test_check_sync_status_out_of_sync(self):
        """Test sync status check when files are out of sync."""
        test_data = {
            "constantName": "out_of_sync_test",
            "modelView": {
                "components": [
                    {
                        "type": "literal",
                        "name": "test_content",
                        "value": "<div>Original content</div>",
                    }
                ]
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "out_of_sync.json"
            with open(json_file, "w") as f:
                json.dump(test_data, f)

            output_dir = Path(temp_dir) / "output"

            # Extract literals
            extract_literals_from_json(str(json_file), str(output_dir))

            # Modify the extracted file
            literal_file = output_dir / "out_of_sync_test" / "test_content.html"
            with open(literal_file, "w") as f:
                f.write("<div>Modified content</div>")

            # Check sync status
            is_synced = check_sync_status(str(output_dir / "out_of_sync_test"))
            assert is_synced is False

    def test_multiple_literal_types(self):
        """Test extraction of different literal types (HTML, CSS, JS)."""
        test_data = {
            "constantName": "multi_type_test",
            "modelView": {
                "components": [
                    {
                        "type": "literal",
                        "name": "html_content",
                        "value": "<div>HTML content</div>",
                    },
                    {
                        "type": "literal",
                        "name": "css_styles",
                        "value": "<style>.test { color: red; }</style>",
                    },
                    {
                        "type": "literal",
                        "name": "js_functions",
                        "value": "<script>function test() { return true; }</script>",
                    },
                ]
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "multi_type.json"
            with open(json_file, "w") as f:
                json.dump(test_data, f)

            output_dir = Path(temp_dir) / "output"
            extraction_map = extract_literals_from_json(str(json_file), str(output_dir))

            assert len(extraction_map["literals"]) == 3

            # Check file extensions
            page_dir = output_dir / "multi_type_test"
            assert (page_dir / "html_content.html").exists()
            assert (page_dir / "css_styles.css").exists()
            assert (page_dir / "js_functions.js").exists()
