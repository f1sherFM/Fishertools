"""
Unit tests for specific error handling scenarios.

Tests specific examples of import errors and file operation errors
to ensure educational explanations are provided correctly.

Validates: Requirements 8.3
"""

import pytest
from fishertools.errors import (
    EducationalErrorWrapper,
    explain_exception,
    with_educational_errors
)


class TestImportErrorSuggestions:
    """Test that import errors get helpful installation suggestions."""
    
    def test_module_not_found_suggests_pip_install(self):
        """Test ModuleNotFoundError suggests pip install."""
        wrapper = EducationalErrorWrapper()
        exception = ModuleNotFoundError("No module named 'requests'")
        
        result = wrapper.enhance_import_error(exception)
        
        # Should suggest pip install
        assert 'pip install' in result
        assert 'requests' in result
        
        # Should be educational
        assert 'Модуль' in result or 'модуль' in result
        assert 'установлен' in result or 'установить' in result
    
    def test_import_error_suggests_pip_install(self):
        """Test ImportError suggests pip install."""
        wrapper = EducationalErrorWrapper()
        exception = ImportError("No module named 'numpy'")
        
        result = wrapper.enhance_import_error(exception)
        
        # Should suggest pip install
        assert 'pip install' in result
        assert 'numpy' in result
    
    def test_import_error_without_module_name(self):
        """Test ImportError without clear module name still provides help."""
        wrapper = EducationalErrorWrapper()
        exception = ImportError("cannot import name 'something'")
        
        result = wrapper.enhance_import_error(exception)
        
        # Should still provide helpful information
        assert 'pip' in result or 'модуль' in result
        assert len(result) > 50  # Should have substantial content
    
    def test_import_error_suggests_checking_spelling(self):
        """Test that import errors suggest checking spelling."""
        wrapper = EducationalErrorWrapper()
        exception = ModuleNotFoundError("No module named 'requets'")  # Typo
        
        result = wrapper.enhance_import_error(exception)
        
        # Should suggest checking spelling
        assert 'Проверьте' in result or 'проверьте' in result
        assert 'написания' in result or 'имени' in result
    
    def test_import_error_suggests_virtual_environment(self):
        """Test that import errors mention virtual environments."""
        wrapper = EducationalErrorWrapper()
        exception = ModuleNotFoundError("No module named 'django'")
        
        result = wrapper.enhance_import_error(exception)
        
        # Should mention virtual environment
        assert 'виртуальн' in result.lower() or 'среда' in result.lower()
    
    def test_import_error_suggests_pip_upgrade(self):
        """Test that import errors suggest upgrading pip."""
        wrapper = EducationalErrorWrapper()
        exception = ImportError("No module named 'test_package'")
        
        result = wrapper.enhance_import_error(exception)
        
        # Should suggest pip upgrade
        assert 'pip' in result
        assert 'upgrade' in result or 'обновл' in result.lower()


class TestFileOperationExplanations:
    """Test that file operation errors get clear explanations."""
    
    def test_file_not_found_explains_path_issues(self):
        """Test FileNotFoundError explains path issues."""
        wrapper = EducationalErrorWrapper()
        exception = FileNotFoundError("data.txt")
        
        result = wrapper.enhance_file_error(exception)
        
        # Should explain path issues
        assert 'путь' in result.lower()
        assert 'файл' in result.lower()
        assert 'не найден' in result.lower() or 'не существует' in result.lower()
    
    def test_file_not_found_suggests_checking_existence(self):
        """Test FileNotFoundError suggests checking file existence."""
        wrapper = EducationalErrorWrapper()
        exception = FileNotFoundError("missing_file.txt")
        
        result = wrapper.enhance_file_error(exception)
        
        # Should suggest checking existence
        assert 'os.path.exists' in result or 'существует' in result.lower()
        assert 'Проверьте' in result or 'проверьте' in result
    
    def test_file_not_found_suggests_checking_current_directory(self):
        """Test FileNotFoundError suggests checking current directory."""
        wrapper = EducationalErrorWrapper()
        exception = FileNotFoundError("config.json")
        
        result = wrapper.enhance_file_error(exception)
        
        # Should suggest checking current directory
        assert 'os.getcwd' in result or 'директори' in result.lower()
    
    def test_permission_error_explains_access_rights(self):
        """Test PermissionError explains access rights."""
        wrapper = EducationalErrorWrapper()
        exception = PermissionError("Permission denied: 'protected_file.txt'")
        
        result = wrapper.enhance_file_error(exception)
        
        # Should explain access rights
        assert 'прав' in result.lower()
        assert 'доступ' in result.lower()
        assert 'PermissionError' in result
    
    def test_permission_error_suggests_closing_file(self):
        """Test PermissionError suggests closing file in other programs."""
        wrapper = EducationalErrorWrapper()
        exception = PermissionError("File is in use")
        
        result = wrapper.enhance_file_error(exception)
        
        # Should suggest closing file
        assert 'Закройте' in result or 'закройте' in result or 'открыт' in result.lower()
        assert 'программ' in result.lower()
    
    def test_permission_error_suggests_admin_rights(self):
        """Test PermissionError suggests running as administrator."""
        wrapper = EducationalErrorWrapper()
        exception = PermissionError("Access denied")
        
        result = wrapper.enhance_file_error(exception)
        
        # Should suggest admin rights
        assert 'администратор' in result.lower() or 'прав' in result.lower()
    
    def test_io_error_provides_general_guidance(self):
        """Test IOError provides general file operation guidance."""
        wrapper = EducationalErrorWrapper()
        exception = IOError("Input/output error")
        
        result = wrapper.enhance_file_error(exception)
        
        # Should provide general guidance
        assert 'файл' in result.lower()
        assert len(result) > 50  # Should have substantial content
    
    def test_file_error_suggests_with_statement(self):
        """Test file errors suggest using with statement."""
        wrapper = EducationalErrorWrapper()
        exception = IOError("File operation failed")
        
        result = wrapper.enhance_file_error(exception)
        
        # Should suggest with statement
        assert 'with open' in result.lower() or 'with' in result


class TestErrorWrapperIntegration:
    """Test integration of error wrapper with various scenarios."""
    
    def test_wrap_error_handles_import_error(self):
        """Test wrap_error handles ImportError correctly."""
        wrapper = EducationalErrorWrapper()
        exception = ImportError("No module named 'pandas'")
        
        result = wrapper.wrap_error(exception)
        
        # Should contain educational content
        assert 'ImportError' in result
        assert len(result) > 100
        assert 'Что произошло' in result or 'ОШИБКА' in result
    
    def test_wrap_error_handles_file_not_found(self):
        """Test wrap_error handles FileNotFoundError correctly."""
        wrapper = EducationalErrorWrapper()
        exception = FileNotFoundError("test.txt")
        
        result = wrapper.wrap_error(exception)
        
        # Should contain educational content
        assert 'FileNotFoundError' in result
        assert len(result) > 100
        assert 'Что произошло' in result or 'ОШИБКА' in result
    
    def test_wrap_error_with_context_for_import(self):
        """Test wrap_error includes context for import errors."""
        wrapper = EducationalErrorWrapper()
        exception = ModuleNotFoundError("No module named 'scipy'")
        context = "loading scientific computing library"
        
        result = wrapper.wrap_error(exception, context)
        
        # Should include context
        assert 'Контекст' in result or context in result
        assert 'ModuleNotFoundError' in result
    
    def test_wrap_error_with_context_for_file_error(self):
        """Test wrap_error includes context for file errors."""
        wrapper = EducationalErrorWrapper()
        exception = PermissionError("Cannot write to file")
        context = "saving configuration"
        
        result = wrapper.wrap_error(exception, context)
        
        # Should include context
        assert 'Контекст' in result or context in result
        assert 'PermissionError' in result
    
    def test_explain_exception_convenience_for_import(self):
        """Test explain_exception convenience function for import errors."""
        exception = ImportError("No module named 'matplotlib'")
        
        result = explain_exception(exception, "plotting graphs")
        
        # Should work correctly
        assert isinstance(result, str)
        assert 'ImportError' in result
        assert len(result) > 50
    
    def test_explain_exception_convenience_for_file_error(self):
        """Test explain_exception convenience function for file errors."""
        exception = FileNotFoundError("data.csv")
        
        result = explain_exception(exception, "reading data file")
        
        # Should work correctly
        assert isinstance(result, str)
        assert 'FileNotFoundError' in result
        assert len(result) > 50
    
    def test_decorator_with_import_error(self):
        """Test decorator handles import errors correctly."""
        @with_educational_errors("importing module")
        def import_function():
            raise ImportError("No module named 'test'")
        
        # Should raise the error but log educational info
        with pytest.raises(ImportError):
            import_function()
    
    def test_decorator_with_file_error(self):
        """Test decorator handles file errors correctly."""
        @with_educational_errors("reading file")
        def file_function():
            raise FileNotFoundError("missing.txt")
        
        # Should raise the error but log educational info
        with pytest.raises(FileNotFoundError):
            file_function()


class TestErrorMessageQuality:
    """Test the quality and completeness of error messages."""
    
    def test_import_error_message_is_comprehensive(self):
        """Test that import error messages are comprehensive."""
        wrapper = EducationalErrorWrapper()
        exception = ModuleNotFoundError("No module named 'tensorflow'")
        
        result = wrapper.enhance_import_error(exception)
        
        # Should have multiple sections
        assert 'pip install' in result
        assert 'Проверьте' in result or 'проверьте' in result
        
        # Should be reasonably long (comprehensive)
        assert len(result) > 200
    
    def test_file_error_message_is_comprehensive(self):
        """Test that file error messages are comprehensive."""
        wrapper = EducationalErrorWrapper()
        exception = FileNotFoundError("important_data.json")
        
        result = wrapper.enhance_file_error(exception)
        
        # Should have multiple sections
        assert 'Что произошло' in result or 'Ошибка' in result
        assert 'Как исправить' in result or 'причин' in result.lower()
        
        # Should be reasonably long (comprehensive)
        assert len(result) > 200
    
    def test_error_messages_are_beginner_friendly(self):
        """Test that error messages use beginner-friendly language."""
        wrapper = EducationalErrorWrapper()
        
        # Test with various errors
        errors = [
            ImportError("No module named 'requests'"),
            FileNotFoundError("data.txt"),
            PermissionError("Access denied")
        ]
        
        for exception in errors:
            if isinstance(exception, ImportError):
                result = wrapper.enhance_import_error(exception)
            else:
                result = wrapper.enhance_file_error(exception)
            
            # Should avoid overly technical jargon
            # Should use clear, simple language
            assert len(result) > 50
            
            # Should not be just a stack trace
            assert result != str(exception)
    
    def test_error_messages_include_examples(self):
        """Test that error messages include code examples."""
        wrapper = EducationalErrorWrapper()
        exception = FileNotFoundError("test.txt")
        
        result = wrapper.enhance_file_error(exception)
        
        # Should include code examples
        assert 'os.path.exists' in result or 'os.getcwd' in result or 'with open' in result
