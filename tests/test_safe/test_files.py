"""
Unit tests for safe file operations.
"""

import pytest
import tempfile
import os
from pathlib import Path
from fishertools.safe.files import (
    safe_read_file, safe_write_file, safe_file_exists, 
    safe_get_file_size, safe_list_files
)


class TestSafeFileOperations:
    """Unit tests for safe file operations."""
    
    def test_safe_read_file_existing_file(self):
        """Test reading an existing file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("Test content")
            temp_path = f.name
        
        try:
            result = safe_read_file(temp_path)
            assert result == "Test content"
        finally:
            os.unlink(temp_path)
    
    def test_safe_read_file_nonexistent_file(self):
        """Test reading a non-existent file returns default."""
        result = safe_read_file("nonexistent_file.txt", default="default content")
        assert result == "default content"
    
    def test_safe_write_file_success(self):
        """Test writing to a file successfully."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test_file.txt"
            result = safe_write_file(file_path, "Hello World")
            assert result is True
            assert file_path.exists()
            assert file_path.read_text(encoding='utf-8') == "Hello World"
    
    def test_safe_file_exists_existing_file(self):
        """Test checking existence of an existing file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            assert safe_file_exists(temp_path) is True
        finally:
            os.unlink(temp_path)
    
    def test_safe_file_exists_nonexistent_file(self):
        """Test checking existence of a non-existent file."""
        assert safe_file_exists("nonexistent_file.txt") is False
    
    def test_safe_get_file_size_existing_file(self):
        """Test getting size of an existing file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("12345")  # 5 bytes
            temp_path = f.name
        
        try:
            size = safe_get_file_size(temp_path)
            assert size == 5
        finally:
            os.unlink(temp_path)
    
    def test_safe_get_file_size_nonexistent_file(self):
        """Test getting size of a non-existent file returns default."""
        size = safe_get_file_size("nonexistent_file.txt", default=100)
        assert size == 100
    
    def test_safe_list_files_existing_directory(self):
        """Test listing files in an existing directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create some test files
            (Path(temp_dir) / "file1.txt").write_text("content1")
            (Path(temp_dir) / "file2.py").write_text("content2")
            (Path(temp_dir) / "subdir").mkdir()
            
            files = safe_list_files(temp_dir)
            assert "file1.txt" in files
            assert "file2.py" in files
            assert len(files) == 2  # Should not include subdirectory
    
    def test_safe_list_files_nonexistent_directory(self):
        """Test listing files in a non-existent directory returns default."""
        files = safe_list_files("nonexistent_directory", default=["default"])
        assert files == ["default"]
    
    def test_input_validation_errors(self):
        """Test that functions raise appropriate errors for invalid inputs."""
        from fishertools.errors.exceptions import SafeUtilityError
        
        with pytest.raises(SafeUtilityError, match="не может быть None"):
            safe_read_file(None)
        
        with pytest.raises(SafeUtilityError, match="должна быть строкой"):
            safe_read_file("test.txt", encoding=123)
        
        with pytest.raises(SafeUtilityError, match="должно быть строкой"):
            safe_write_file("test.txt", 123)