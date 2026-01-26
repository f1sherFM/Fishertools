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



class TestProjectRoot:
    """Tests for project_root function."""
    
    def test_project_root_from_current_directory(self):
        """Test finding project root from current directory."""
        from fishertools.safe.files import project_root
        
        root = project_root()
        assert root is not None
        assert Path(root).exists()
        # Should find one of the markers
        markers = ['setup.py', 'pyproject.toml', '.git', '.gitignore']
        assert any((Path(root) / marker).exists() for marker in markers)
    
    def test_project_root_from_subdirectory(self):
        """Test finding project root from a subdirectory."""
        from fishertools.safe.files import project_root
        
        # Get root from current directory
        root1 = project_root()
        
        # Get root from a subdirectory
        subdir = Path(root1) / "fishertools"
        if subdir.exists():
            root2 = project_root(subdir)
            assert root1 == root2
    
    def test_project_root_not_found(self):
        """Test that RuntimeError is raised when project root cannot be found."""
        from fishertools.safe.files import project_root
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a temporary directory with no markers
            with pytest.raises(RuntimeError, match="Could not determine project root"):
                project_root(temp_dir)


class TestFindFile:
    """Tests for find_file function."""
    
    def test_find_file_existing_file(self):
        """Test finding an existing file."""
        from fishertools.safe.files import find_file
        
        # Find setup.py which should exist in project root
        path = find_file("setup.py")
        assert path is not None
        assert Path(path).exists()
        assert Path(path).name == "setup.py"
    
    def test_find_file_nonexistent_file(self):
        """Test finding a non-existent file returns None."""
        from fishertools.safe.files import find_file
        
        path = find_file("nonexistent_file_12345.txt")
        assert path is None
    
    def test_find_file_from_subdirectory(self):
        """Test finding a file starting from a subdirectory."""
        from fishertools.safe.files import find_file
        
        # Create a test file in a temporary subdirectory
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            subdir = temp_path / "subdir"
            subdir.mkdir()
            
            # Create a test file in the subdirectory
            test_file = subdir / "test.txt"
            test_file.write_text("test content")
            
            # Find the file from the subdirectory
            path = find_file("test.txt", subdir)
            assert path is not None
            assert Path(path).exists()
            assert Path(path).name == "test.txt"


class TestSafeOpen:
    """Tests for safe_open function."""
    
    def test_safe_open_existing_file(self):
        """Test opening an existing file."""
        from fishertools.safe.files import safe_open
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("Test content")
            temp_path = f.name
        
        try:
            with safe_open(temp_path) as f:
                content = f.read()
            assert content == "Test content"
        finally:
            os.unlink(temp_path)
    
    def test_safe_open_nonexistent_file(self):
        """Test opening a non-existent file raises FileNotFoundError."""
        from fishertools.safe.files import safe_open
        
        with pytest.raises(FileNotFoundError):
            safe_open("nonexistent_file_12345.txt")
    
    def test_safe_open_write_mode(self):
        """Test opening a file in write mode."""
        from fishertools.safe.files import safe_open
        
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test_file.txt"
            
            with safe_open(file_path, mode='w') as f:
                f.write("Hello World")
            
            assert file_path.exists()
            assert file_path.read_text(encoding='utf-8') == "Hello World"
