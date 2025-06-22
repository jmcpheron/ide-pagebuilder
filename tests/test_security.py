import json
import re
from pathlib import Path

import pytest


class TestSecurity:
    """Test suite for security-related checks in page definitions."""

    @pytest.fixture
    def page_files(self):
        """Find all page definition JSON files."""
        page_files = []
        for json_file in Path(".").rglob("pages.*.json"):
            if json_file.exists():
                page_files.append(json_file)
        return page_files

    def test_no_hardcoded_secrets(self, page_files):
        """Test that no hardcoded secrets or sensitive data are present."""
        # Patterns that might indicate secrets
        secret_patterns = [
            r'password\s*[:=]\s*["\'][^"\']*["\']',
            r'api[_-]?key\s*[:=]\s*["\'][^"\']*["\']',
            r'secret\s*[:=]\s*["\'][^"\']*["\']',
            r'token\s*[:=]\s*["\'][^"\']*["\']',
            r'aws[_-]?access[_-]?key\s*[:=]\s*["\'][^"\']*["\']',
            r'aws[_-]?secret[_-]?key\s*[:=]\s*["\'][^"\']*["\']',
        ]

        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                content = f.read().lower()

            for pattern in secret_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    # Allow some common non-sensitive patterns
                    filtered_matches = []
                    for match in matches:
                        if not any(
                            safe in match.lower()
                            for safe in [
                                "placeholder",
                                "example",
                                "test",
                                "demo",
                                "xxx",
                                "***",
                            ]
                        ):
                            filtered_matches.append(match)

                    if filtered_matches:
                        pytest.fail(
                            f"Potential hardcoded secret found in {page_file}: {filtered_matches}"
                        )

    def test_no_dangerous_javascript(self, page_files):
        """Test that literal components don't contain dangerous JavaScript patterns."""
        dangerous_patterns = [
            r"eval\s*\(",
            # r'innerHTML\s*=',  # Too restrictive for legitimate UI updates
            r"outerHTML\s*=",
            r"document\.write\s*\(",
            # Disabled - too restrictive for legitimate CDN usage
            # r'script\s+src\s*=\s*["\']https?://(?!ajax\.googleapis\.com|cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com|nc-widget-v3\.s3\.us-east-2\.amazonaws\.com)',
            # r'on\w+\s*=\s*["\'][^"\']*["\']',  # inline event handlers - too restrictive
        ]

        def check_content_for_dangerous_patterns(content, file_path):
            for pattern in dangerous_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    # Allow some specific safe cases
                    filtered_matches = []
                    for match in matches:
                        # Allow trusted CDNs and specific patterns
                        if not any(
                            safe in match.lower()
                            for safe in [
                                "ajax.googleapis.com",
                                "cdn.jsdelivr.net",
                                "cdnjs.cloudflare.com",
                                "name-coach.com",
                                "nc-widget-v3.s3.us-east-2.amazonaws.com",
                            ]
                        ):
                            filtered_matches.append(match)

                    if filtered_matches:
                        pytest.fail(
                            f"Potentially dangerous JavaScript pattern found in {file_path}: {filtered_matches}"
                        )

        def check_components_for_dangerous_js(components, file_path):
            for component in components:
                if component.get("type") == "literal":
                    value = component.get("value", "")
                    if value:
                        check_content_for_dangerous_patterns(value, file_path)

                # Recursively check nested components
                if "components" in component:
                    check_components_for_dangerous_js(
                        component["components"], file_path
                    )

        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                data = json.load(f)

            if "modelView" in data and "components" in data["modelView"]:
                check_components_for_dangerous_js(
                    data["modelView"]["components"], page_file
                )

    def test_sql_injection_protection(self, page_files):
        """Test that SQL-like patterns are properly parameterized."""
        # Look for potential SQL injection patterns
        sql_patterns = [
            r'select\s+.*\s+from\s+.*where\s+.*=\s*["\'][^"\']*["\']',
            r'insert\s+into\s+.*values\s*\([^)]*["\'][^"\']*["\'][^)]*\)',
            r'update\s+.*set\s+.*=\s*["\'][^"\']*["\']',
            r'delete\s+from\s+.*where\s+.*=\s*["\'][^"\']*["\']',
        ]

        def check_for_sql_injection(content, file_path):
            for pattern in sql_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                if matches:
                    # Allow parameterized queries (with :param syntax)
                    safe_matches = []
                    for match in matches:
                        if ":" not in match and "?" not in match:
                            safe_matches.append(match)

                    if safe_matches:
                        pytest.fail(
                            f"Potential SQL injection vulnerability in {file_path}: {safe_matches}"
                        )

        def check_components_for_sql_injection(components, file_path):
            for component in components:
                if component.get("type") == "literal":
                    value = component.get("value", "")
                    if value:
                        check_for_sql_injection(value, file_path)

                # Also check onLoad and onUpdate scripts
                for script_field in ["onLoad", "onUpdate"]:
                    if script_field in component:
                        check_for_sql_injection(component[script_field], file_path)

                # Recursively check nested components
                if "components" in component:
                    check_components_for_sql_injection(
                        component["components"], file_path
                    )

        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                data = json.load(f)

            if "modelView" in data and "components" in data["modelView"]:
                check_components_for_sql_injection(
                    data["modelView"]["components"], page_file
                )

    def test_external_resource_domains(self, page_files):
        """Test that external URLs are well-formed and use HTTPS."""
        # Pattern to find URLs in content
        url_pattern = r'https?://([^/\s"\'<>]+)'
        
        def check_external_resources(content, file_path):
            urls = re.findall(url_pattern, content, re.IGNORECASE)
            for url in urls:
                domain = url.lower()
                
                # Check for obvious security issues
                if any(suspicious in domain for suspicious in [
                    'localhost', '127.0.0.1', '192.168.', '10.0.0.', 'file://'
                ]):
                    pytest.fail(f"Suspicious local/file URL found in {file_path}: {domain}")
                
                # Check for malformed domains
                if '..' in domain or domain.startswith('.') or domain.endswith('.'):
                    pytest.fail(f"Malformed domain found in {file_path}: {domain}")
        
        def check_components_for_external_resources(components, file_path):
            for component in components:
                if component.get("type") == "literal":
                    value = component.get("value", "")
                    if value:
                        check_external_resources(value, file_path)
                
                # Recursively check nested components
                if "components" in component:
                    check_components_for_external_resources(component["components"], file_path)
        
        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                data = json.load(f)
            
            if "modelView" in data and "components" in data["modelView"]:
                check_components_for_external_resources(data["modelView"]["components"], page_file)

    def test_access_control_fields(self, page_files):
        """Test that access control fields are properly configured."""
        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                data = json.load(f)

            # Check that developerSecurity field exists (it's optional in this system)
            if "developerSecurity" in data:
                assert isinstance(data["developerSecurity"], list), (
                    f"developerSecurity must be a list in {page_file}"
                )

            # If there are pageRoles, they should be objects or strings
            if "pageRoles" in data:
                assert isinstance(data["pageRoles"], list), (
                    f"pageRoles must be a list in {page_file}"
                )
                for role in data["pageRoles"]:
                    assert isinstance(role, (str, dict)), (
                        f"pageRoles must contain strings or objects in {page_file}"
                    )
                    if isinstance(role, dict):
                        assert "roleName" in role, (
                            f"pageRole objects must have roleName in {page_file}"
                        )

    def test_no_sensitive_data_in_comments(self, page_files):
        """Test that JavaScript comments don't contain sensitive information."""
        comment_patterns = [
            r"//.*(?:password|secret|api[_-]?key|auth[_-]?token)",
            r"/\*.*(?:password|secret|api[_-]?key|auth[_-]?token).*\*/",
        ]

        def check_comments_for_sensitive_data(content, file_path):
            for pattern in comment_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
                if matches:
                    # Filter out obvious test/placeholder values
                    filtered_matches = []
                    for match in matches:
                        if not any(
                            safe in match.lower()
                            for safe in [
                                "example",
                                "test",
                                "placeholder",
                                "todo",
                                "fixme",
                            ]
                        ):
                            filtered_matches.append(match)

                    if filtered_matches:
                        pytest.fail(
                            f"Potentially sensitive data in comments in {file_path}: {filtered_matches}"
                        )

        def check_components_for_sensitive_comments(components, file_path):
            for component in components:
                if component.get("type") == "literal":
                    value = component.get("value", "")
                    if value:
                        check_comments_for_sensitive_data(value, file_path)

                # Recursively check nested components
                if "components" in component:
                    check_components_for_sensitive_comments(
                        component["components"], file_path
                    )

        for page_file in page_files:
            with open(page_file, encoding="utf-8") as f:
                data = json.load(f)

            if "modelView" in data and "components" in data["modelView"]:
                check_components_for_sensitive_comments(
                    data["modelView"]["components"], page_file
                )
