"""Test newline handling in extract scripts to prevent mixed line ending issues."""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path to import the scripts
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract_literals import detect_newline_style, extract_literals_from_json, rebuild_json_from_literals
from extract_virtual_domains import extract_sql_from_json, rebuild_json_from_sql


class TestNewlineDetection:
    """Test the newline detection functionality."""
    
    def test_detect_unix_newlines(self):
        """Test detection of Unix-style newlines."""
        content = "Line 1\nLine 2\nLine 3\n"
        assert detect_newline_style(content) == '\n'
    
    def test_detect_windows_newlines(self):
        """Test detection of Windows-style newlines."""
        content = "Line 1\r\nLine 2\r\nLine 3\r\n"
        assert detect_newline_style(content) == '\r\n'
    
    def test_detect_mac_newlines(self):
        """Test detection of old Mac-style newlines."""
        content = "Line 1\rLine 2\rLine 3\r"
        assert detect_newline_style(content) == '\r'
    
    def test_detect_mixed_newlines_unix_dominant(self):
        """Test detection when Unix newlines are dominant."""
        content = "Line 1\nLine 2\nLine 3\r\nLine 4\n"
        assert detect_newline_style(content) == '\n'
    
    def test_detect_mixed_newlines_windows_dominant(self):
        """Test detection when Windows newlines are dominant."""
        content = "Line 1\r\nLine 2\r\nLine 3\nLine 4\r\n"
        assert detect_newline_style(content) == '\r\n'
    
    def test_detect_empty_content(self):
        """Test detection with empty content."""
        assert detect_newline_style("") == '\n'


class TestLiteralsNewlinePreservation:
    """Test that extract_literals preserves newlines correctly."""
    
    @pytest.fixture
    def sample_page_unix(self, tmp_path):
        """Create a sample page JSON with Unix newlines."""
        page_data = {
            "constantName": "testPage",
            "modelView": {
                "components": [
                    {
                        "type": "literal",
                        "name": "test_content",
                        "value": "<div>\n  <h1>Test</h1>\n  <p>Content</p>\n</div>"
                    }
                ]
            }
        }
        
        json_file = tmp_path / "page.unix.json"
        # Write with Unix newlines
        with open(json_file, 'w', newline='') as f:
            json.dump(page_data, f, indent=2)
        
        return json_file
    
    @pytest.fixture
    def sample_page_windows(self, tmp_path):
        """Create a sample page JSON with Windows newlines."""
        page_data = {
            "constantName": "testPage",
            "modelView": {
                "components": [
                    {
                        "type": "literal",
                        "name": "test_content",
                        "value": "<div>\r\n  <h1>Test</h1>\r\n  <p>Content</p>\r\n</div>"
                    }
                ]
            }
        }
        
        json_file = tmp_path / "page.windows.json"
        # Write with Windows newlines
        json_str = json.dumps(page_data, indent=2)
        json_str = json_str.replace('\n', '\r\n')
        with open(json_file, 'wb') as f:
            f.write(json_str.encode('utf-8'))
        
        return json_file
    
    def test_preserve_unix_newlines(self, sample_page_unix, tmp_path):
        """Test that Unix newlines are preserved during extract/rebuild."""
        output_dir = tmp_path / "extracted"
        
        # Extract
        extract_literals_from_json(str(sample_page_unix), str(output_dir))
        
        # Check extracted file has Unix newlines
        extracted_file = output_dir / "testPage" / "test_content.html"
        with open(extracted_file, 'rb') as f:
            content = f.read()
        
        assert b'\r\n' not in content  # No Windows newlines
        assert b'\n' in content  # Has Unix newlines
        
        # Rebuild
        rebuild_json_from_literals(str(output_dir / "testPage"))
        
        # Check JSON still has Unix newlines
        with open(sample_page_unix, 'rb') as f:
            rebuilt_content = f.read()
        
        assert b'\r\n' not in rebuilt_content
        assert b'\n' in rebuilt_content
    
    def test_preserve_windows_newlines(self, sample_page_windows, tmp_path):
        """Test that Windows newlines are preserved during extract/rebuild."""
        output_dir = tmp_path / "extracted"
        
        # Extract
        extract_literals_from_json(str(sample_page_windows), str(output_dir))
        
        # Check extraction map recorded Windows newlines
        map_file = output_dir / "testPage" / "_extraction_map.json"
        with open(map_file) as f:
            extraction_map = json.load(f)
        assert extraction_map['newline_style'] == '\r\n'
        
        # Rebuild
        rebuild_json_from_literals(str(output_dir / "testPage"))
        
        # Check JSON still has Windows newlines
        with open(sample_page_windows, 'rb') as f:
            rebuilt_content = f.read()
        
        assert b'\r\n' in rebuilt_content
    
    def test_normalize_newlines_option(self, sample_page_windows, tmp_path):
        """Test that --normalize-newlines converts to Unix style."""
        output_dir = tmp_path / "extracted"
        
        # Extract with normalization
        extract_literals_from_json(str(sample_page_windows), str(output_dir), normalize_newlines=True)
        
        # Check extracted file has Unix newlines
        extracted_file = output_dir / "testPage" / "test_content.html"
        with open(extracted_file, 'rb') as f:
            content = f.read()
        
        assert b'\r\n' not in content  # No Windows newlines
        assert b'\n' in content  # Has Unix newlines
        
        # Check extraction map records Unix style
        map_file = output_dir / "testPage" / "_extraction_map.json"
        with open(map_file) as f:
            extraction_map = json.load(f)
        assert extraction_map['newline_style'] == '\n'


class TestVirtualDomainsNewlinePreservation:
    """Test that extract_virtual_domains preserves newlines correctly."""
    
    @pytest.fixture
    def sample_vd_windows(self, tmp_path):
        """Create a sample virtual domain JSON with Windows newlines and SQL."""
        vd_data = {
            "serviceName": "testService",
            "codeGet": "SELECT *\r\nFROM test_table\r\nWHERE id = :id"
        }
        
        json_file = tmp_path / "virtualDomain.windows.json"
        # Write with Windows newlines
        json_str = json.dumps(vd_data, indent=2)
        json_str = json_str.replace('\n', '\r\n')
        with open(json_file, 'wb') as f:
            f.write(json_str.encode('utf-8'))
        
        return json_file
    
    def test_vd_preserve_windows_newlines(self, sample_vd_windows, tmp_path):
        """Test that Windows newlines in SQL are preserved."""
        output_dir = tmp_path / "extracted_vd"
        
        # Extract
        extract_sql_from_json(str(sample_vd_windows), str(output_dir))
        
        # Check SQL file content
        sql_file = output_dir / "testService" / "codeget.sql"
        with open(sql_file, 'rb') as f:
            content = f.read().decode('utf-8')
        
        # SQL content should be preserved as-is
        assert "SELECT *\r\nFROM test_table\r\nWHERE id = :id" in content
        
        # Rebuild
        rebuild_json_from_sql(str(output_dir / "testService"))
        
        # Check JSON still has Windows newlines
        with open(sample_vd_windows, 'rb') as f:
            rebuilt_content = f.read()
        
        assert b'\r\n' in rebuilt_content
    
    def test_vd_normalize_newlines(self, sample_vd_windows, tmp_path):
        """Test normalizing SQL newlines."""
        output_dir = tmp_path / "extracted_vd"
        
        # Extract with normalization
        extract_sql_from_json(str(sample_vd_windows), str(output_dir), normalize_newlines=True)
        
        # Check SQL file has Unix newlines
        sql_file = output_dir / "testService" / "codeget.sql"
        with open(sql_file, 'rb') as f:
            content = f.read()
        
        assert b'\r\n' not in content
        assert b'\n' in content


class TestMixedNewlineScenarios:
    """Test handling of files with mixed newlines that could cause git issues."""
    
    def test_mixed_newlines_in_literals(self, tmp_path):
        """Test handling content with accidentally mixed newlines."""
        # Create a file that simulates what happens when Windows editors
        # modify extracted files
        page_data = {
            "constantName": "mixedTest",
            "modelView": {
                "components": [
                    {
                        "type": "literal",
                        "name": "mixed_content",
                        # This simulates content that has been edited on different systems
                        "value": "<div>\n  <h1>Unix line</h1>\r\n  <p>Windows line</p>\n</div>"
                    }
                ]
            }
        }
        
        json_file = tmp_path / "mixed.json"
        with open(json_file, 'w') as f:
            json.dump(page_data, f)
        
        output_dir = tmp_path / "extracted"
        
        # Extract with normalization should fix the mixed newlines
        extract_literals_from_json(str(json_file), str(output_dir), normalize_newlines=True)
        
        # Check that extracted content has consistent newlines
        extracted_file = output_dir / "mixedTest" / "mixed_content.html"
        with open(extracted_file, 'rb') as f:
            content = f.read()
        
        # Should only have Unix newlines
        assert b'\r\n' not in content
        assert b'\n' in content
        
        # Count newlines to ensure they're all consistent
        text = content.decode('utf-8')
        assert '\r\n' not in text
        assert text.count('\n') == 3  # Three line breaks in the content
    
    def test_detect_and_warn_mixed_newlines(self):
        """Test that mixed newlines are properly detected."""
        # Various mixed content scenarios
        mixed_contents = [
            "Unix\nWindows\r\nUnix\n",
            "Start\r\nMiddle\nEnd\r\n",
            "\n\r\n\n\r\n",  # Alternating
        ]
        
        for content in mixed_contents:
            style = detect_newline_style(content)
            # Should detect the predominant style
            assert style in ['\n', '\r\n', '\r']


class TestRealWorldScenarios:
    """Test scenarios that match real-world usage patterns."""
    
    def test_windows_developer_unix_server(self, tmp_path):
        """Test workflow: Windows developer edits files, deploys to Unix server."""
        # Create initial file with Unix newlines (as it would be in git)
        page_data = {
            "constantName": "deployment",
            "modelView": {
                "components": [
                    {
                        "type": "literal",
                        "name": "app",
                        "value": "#!/bin/bash\necho 'Deploy script'\nexit 0"
                    }
                ]
            }
        }
        
        json_file = tmp_path / "deploy.json"
        with open(json_file, 'w', newline='') as f:
            json.dump(page_data, f, indent=2)
        
        output_dir = tmp_path / "extracted"
        
        # Extract (preserves Unix newlines)
        extract_literals_from_json(str(json_file), str(output_dir))
        
        # Simulate Windows editor changing the file
        app_file = output_dir / "deployment" / "app.html"
        with open(app_file, 'r') as f:
            content = f.read()
        
        # Windows editor might add CRLF
        content_windows = content.replace('\n', '\r\n')
        with open(app_file, 'wb') as f:
            f.write(content_windows.encode('utf-8'))
        
        # Rebuild should preserve the JSON's original Unix newlines
        rebuild_json_from_literals(str(output_dir / "deployment"))
        
        # Verify JSON still has Unix newlines (no git changes)
        with open(json_file, 'rb') as f:
            final_content = f.read()
        
        # The JSON should maintain Unix newlines despite Windows editing
        assert b'\r\n' not in final_content
        assert b'\n' in final_content