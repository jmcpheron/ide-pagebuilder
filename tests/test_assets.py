"""Tests for project assets like logos and documentation files."""

import re
from pathlib import Path


class TestLogos:
    """Test logo files and references."""

    def test_logo_files_exist(self):
        """Both logo files should exist in the project root."""
        logo_light = Path("logo.png")
        logo_dark = Path("logo-dark.png")
        
        assert logo_light.exists(), "Light theme logo (logo.png) should exist"
        assert logo_dark.exists(), "Dark theme logo (logo-dark.png) should exist"

    def test_logo_files_are_valid_png(self):
        """Logo files should be valid PNG images."""
        logo_light = Path("logo.png")
        logo_dark = Path("logo-dark.png")
        
        # Check that files exist first
        assert logo_light.exists(), "Light theme logo should exist"
        assert logo_dark.exists(), "Dark theme logo should exist"
        
        # Check PNG file signature (first 8 bytes)
        png_signature = b'\x89PNG\r\n\x1a\n'
        
        with open(logo_light, 'rb') as f:
            assert f.read(8) == png_signature, "logo.png should be a valid PNG file"
        
        with open(logo_dark, 'rb') as f:
            assert f.read(8) == png_signature, "logo-dark.png should be a valid PNG file"

    def test_logo_files_have_reasonable_size(self):
        """Logo files should have reasonable file sizes (not empty, not huge)."""
        logo_light = Path("logo.png")
        logo_dark = Path("logo-dark.png")
        
        # Files should be at least 1KB and less than 10MB
        min_size = 1024  # 1KB
        max_size = 10 * 1024 * 1024  # 10MB
        
        light_size = logo_light.stat().st_size
        dark_size = logo_dark.stat().st_size
        
        assert min_size <= light_size <= max_size, f"logo.png size ({light_size} bytes) should be between {min_size} and {max_size} bytes"
        assert min_size <= dark_size <= max_size, f"logo-dark.png size ({dark_size} bytes) should be between {min_size} and {max_size} bytes"


class TestReadmeAssets:
    """Test README references to assets."""

    def test_readme_references_correct_logos(self):
        """README should reference both logo files correctly."""
        readme_path = Path("README.md")
        assert readme_path.exists(), "README.md should exist"
        
        with open(readme_path, encoding="utf-8") as f:
            readme_content = f.read()
        
        # Should contain picture element with both logos
        assert '<picture>' in readme_content, "README should contain a picture element for responsive logos"
        assert 'logo.png' in readme_content, "README should reference logo.png"
        assert 'logo-dark.png' in readme_content, "README should reference logo-dark.png"
        assert 'prefers-color-scheme: dark' in readme_content, "README should use dark theme media query"

    def test_readme_logo_references_are_valid(self):
        """All logo files referenced in README should exist."""
        readme_path = Path("README.md")
        
        with open(readme_path, encoding="utf-8") as f:
            readme_content = f.read()
        
        # Find all image references in the README
        # Look for src="filename" and srcset="filename" patterns
        src_pattern = r'(?:src|srcset)=["\']([^"\']+\.(?:png|jpg|jpeg|gif|svg))["\']'
        referenced_images = re.findall(src_pattern, readme_content, re.IGNORECASE)
        
        for image_path in referenced_images:
            # Skip external URLs (http/https)
            if image_path.startswith(('http://', 'https://')):
                continue
            
            image_file = Path(image_path)
            assert image_file.exists(), f"Referenced image file should exist: {image_path}"

    def test_readme_has_proper_picture_element_structure(self):
        """README should have properly structured picture element for theme support."""
        readme_path = Path("README.md")
        
        with open(readme_path, encoding="utf-8") as f:
            readme_content = f.read()
        
        # Should have proper picture element structure
        picture_pattern = r'<picture>\s*<source[^>]*media="\(prefers-color-scheme:\s*dark\)"[^>]*srcset="logo-dark\.png"[^>]*>\s*<img[^>]*src="logo\.png"[^>]*>\s*</picture>'
        
        assert re.search(picture_pattern, readme_content, re.DOTALL | re.IGNORECASE), \
            "README should have properly structured picture element with dark theme support"


class TestProjectStructure:
    """Test overall project asset structure."""

    def test_no_orphaned_image_files(self):
        """All image files in the root should be referenced somewhere."""
        root_images = list(Path(".").glob("*.png")) + list(Path(".").glob("*.jpg")) + list(Path(".").glob("*.gif"))
        
        # Read README to see what's referenced
        readme_path = Path("README.md")
        with open(readme_path, encoding="utf-8") as f:
            readme_content = f.read()
        
        for image_file in root_images:
            image_name = image_file.name
            # Skip test artifacts or temporary files
            if image_name.startswith('.') or image_name.startswith('test_'):
                continue
                
            assert image_name in readme_content, f"Image file {image_name} should be referenced in README.md"

    def test_project_has_logo_in_structure_docs(self):
        """Project structure documentation should mention logo files."""
        readme_path = Path("README.md")
        
        with open(readme_path, encoding="utf-8") as f:
            readme_content = f.read()
        
        # Look for project structure section
        if "## Project Structure" in readme_content:
            structure_section = readme_content.split("## Project Structure")[1].split("##")[0]
            
            # Should mention logo files in the structure
            assert "logo" in structure_section.lower(), "Project structure should mention logo files"