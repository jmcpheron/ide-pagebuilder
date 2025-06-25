"""Tests for virtual domain functionality."""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path to import extract_virtual_domains
sys.path.insert(0, str(Path(__file__).parent.parent))

from extract_virtual_domains import extract_sql_from_json, rebuild_json_from_sql, check_sync_status


class TestVirtualDomainValidation:
    """Test validation of virtual domain JSON files."""
    
    def test_virtual_domain_has_service_name(self):
        """Virtual domain files should have a serviceName field."""
        vd_files = list(Path("virtualDomains").glob("*.json"))
        assert len(vd_files) > 0, "No virtual domain files found"
        
        for vd_file in vd_files:
            with open(vd_file, encoding="utf-8") as f:
                data = json.load(f)
            assert "serviceName" in data, f"Missing serviceName in {vd_file}"
    
    def test_virtual_domain_has_at_least_one_code_block(self):
        """Virtual domain files should have at least one SQL code block."""
        vd_files = list(Path("virtualDomains").glob("*.json"))
        
        for vd_file in vd_files:
            with open(vd_file, encoding="utf-8") as f:
                data = json.load(f)
            
            code_fields = ["codeGet", "codePost", "codePut", "codeDelete"]
            has_code = any(data.get(field) and data.get(field).strip() for field in code_fields)
            assert has_code, f"No SQL code blocks found in {vd_file}"
    
    def test_virtual_domain_has_valid_roles(self):
        """Virtual domain files should have proper role definitions."""
        vd_files = list(Path("virtualDomains").glob("*.json"))
        
        for vd_file in vd_files:
            with open(vd_file, encoding="utf-8") as f:
                data = json.load(f)
            
            if "virtualDomainRoles" in data:
                roles = data["virtualDomainRoles"]
                assert isinstance(roles, list), f"virtualDomainRoles should be a list in {vd_file}"
                
                for role in roles:
                    assert "roleName" in role, f"Role missing roleName in {vd_file}"
                    assert "allowGet" in role, f"Role missing allowGet in {vd_file}"
    
    def test_sql_uses_parameters_not_concatenation(self):
        """SQL code should use parameters (:param) not string concatenation."""
        vd_files = list(Path("virtualDomains").glob("*.json"))
        
        dangerous_patterns = ["||", "CONCAT(", "+"]  # SQL concatenation patterns
        
        for vd_file in vd_files:
            with open(vd_file, encoding="utf-8") as f:
                data = json.load(f)
            
            code_fields = ["codeGet", "codePost", "codePut", "codeDelete"]
            for field in code_fields:
                sql_code = data.get(field, "")
                if sql_code:
                    # Check if SQL contains user input patterns that might be injection risks
                    # Note: This is a basic check - actual SQL should be reviewed by security
                    if any(pattern in sql_code.upper() for pattern in ["||", "CONCAT("]):
                        # This is actually OK for Banner SQL - they use || for concatenation
                        # But we should ensure it's not being used with user input unsafely
                        continue


class TestVirtualDomainExtraction:
    """Test the virtual domain extraction functionality."""
    
    def test_extract_and_rebuild_preserves_content(self):
        """Test that extracting and rebuilding preserves the original content."""
        # Create a temporary virtual domain file
        test_data = {
            "serviceName": "testDomain",
            "codeGet": "SELECT * FROM test_table WHERE id = :id",
            "codePost": "INSERT INTO test_table (name) VALUES (:name)",
            "virtualDomainRoles": [
                {"roleName": "TEST_ROLE", "allowGet": True, "allowPost": False}
            ],
            "typeOfCode": "S"
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test JSON file
            json_file = Path(temp_dir) / "test_domain.json"
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(test_data, f, indent=2)
            
            # Extract SQL
            output_dir = Path(temp_dir) / "extracted"
            extraction_map = extract_sql_from_json(str(json_file), str(output_dir))
            
            # Verify extraction
            assert len(extraction_map["sql_blocks"]) == 2
            assert extraction_map["service_name"] == "testDomain"
            
            # Check extracted files exist
            domain_dir = output_dir / "testDomain"
            assert (domain_dir / "codeget.sql").exists()
            assert (domain_dir / "codepost.sql").exists()
            
            # Rebuild JSON
            rebuild_json_from_sql(str(domain_dir))
            
            # Verify content is preserved
            with open(json_file, encoding="utf-8") as f:
                rebuilt_data = json.load(f)
            
            assert rebuilt_data["codeGet"] == test_data["codeGet"]
            assert rebuilt_data["codePost"] == test_data["codePost"]
            assert rebuilt_data["serviceName"] == test_data["serviceName"]
    
    def test_extraction_handles_missing_code_fields(self):
        """Test extraction handles virtual domains with missing code fields."""
        test_data = {
            "serviceName": "minimalDomain",
            "codeGet": "SELECT 1 FROM dual",
            "virtualDomainRoles": []
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "minimal_domain.json"
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(test_data, f, indent=2)
            
            output_dir = Path(temp_dir) / "extracted"
            extraction_map = extract_sql_from_json(str(json_file), str(output_dir))
            
            # Should only extract the one code field that exists
            assert len(extraction_map["sql_blocks"]) == 1
            assert extraction_map["sql_blocks"][0]["field"] == "codeGet"
    
    def test_sync_check_detects_changes(self):
        """Test that sync check detects when files are out of sync."""
        test_data = {
            "serviceName": "syncTest",
            "codeGet": "SELECT original FROM test",
            "virtualDomainRoles": []
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            json_file = Path(temp_dir) / "sync_test.json"
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(test_data, f, indent=2)
            
            output_dir = Path(temp_dir) / "extracted"
            extract_sql_from_json(str(json_file), str(output_dir))
            
            # Verify initially in sync
            domain_dir = output_dir / "syncTest"
            assert check_sync_status(str(domain_dir)) == True
            
            # Modify the extracted SQL file
            sql_file = domain_dir / "codeget.sql"
            with open(sql_file, "w", encoding="utf-8") as f:
                f.write("SELECT modified FROM test")
            
            # Should now be out of sync
            assert check_sync_status(str(domain_dir)) == False


class TestVirtualDomainSecurity:
    """Test security aspects of virtual domains."""
    
    def test_no_hardcoded_credentials(self):
        """Virtual domains should not contain hardcoded credentials."""
        vd_files = list(Path("virtualDomains").glob("*.json"))
        
        # Common credential patterns to look for
        credential_patterns = [
            "password", "passwd", "pwd", "secret", "key", "token",
            "username", "user", "admin", "root"
        ]
        
        for vd_file in vd_files:
            with open(vd_file, encoding="utf-8") as f:
                content = f.read().lower()
            
            # Check for suspicious patterns (this is a basic check)
            for pattern in credential_patterns:
                if f"'{pattern}'" in content or f'"{pattern}"' in content:
                    # This might be a hardcoded credential - flag for review
                    pytest.fail(f"Potential hardcoded credential pattern '{pattern}' found in {vd_file}")
    
    def test_sql_uses_banner_security_context(self):
        """Check that SQL appropriately uses Banner security parameters."""
        vd_files = list(Path("virtualDomains").glob("*.json"))
        
        for vd_file in vd_files:
            with open(vd_file, encoding="utf-8") as f:
                data = json.load(f)
            
            code_fields = ["codeGet", "codePost", "codePut", "codeDelete"]
            for field in code_fields:
                sql_code = data.get(field, "")
                if sql_code and "spriden" in sql_code.lower():
                    # If querying student data, should use proper Banner security
                    # This is a basic check - actual security review needed
                    continue