"""
Tests for backward compatibility of fishertools enhancements.

This module ensures that all existing functionality continues to work
after adding the new enhancement modules.
"""

from __future__ import annotations

import pytest


class TestBackwardCompatibility:
    """Tests to ensure backward compatibility is maintained."""
    
    def test_can_import_main_functions(self):
        """Test that main functions can still be imported."""
        from fishertools import explain_error, safe_get, visualize
        
        assert callable(explain_error)
        assert callable(safe_get)
        assert callable(visualize)
    
    def test_can_import_safe_utilities(self):
        """Test that safe utilities can still be imported."""
        from fishertools import (
            safe_divide, safe_max, safe_min, safe_sum,
            safe_read_file, safe_write_file
        )
        
        assert callable(safe_divide)
        assert callable(safe_max)
        assert callable(safe_min)
        assert callable(safe_sum)
        assert callable(safe_read_file)
        assert callable(safe_write_file)
    
    def test_can_import_learning_functions(self):
        """Test that learning functions can still be imported."""
        from fishertools import (
            generate_example, show_best_practice,
            list_available_concepts, list_available_topics
        )
        
        assert callable(generate_example)
        assert callable(show_best_practice)
        assert callable(list_available_concepts)
        assert callable(list_available_topics)
    
    def test_can_import_input_functions(self):
        """Test that input validation functions can still be imported."""
        from fishertools import ask_int, ask_float, ask_str, ask_choice
        
        assert callable(ask_int)
        assert callable(ask_float)
        assert callable(ask_str)
        assert callable(ask_choice)
    
    def test_can_import_legacy_modules(self):
        """Test that legacy modules can still be imported."""
        from fishertools import utils, decorators, helpers
        
        assert utils is not None
        assert decorators is not None
        assert helpers is not None
    
    def test_can_import_existing_modules(self):
        """Test that existing modules can still be imported."""
        from fishertools import errors, safe, learn, legacy
        
        assert errors is not None
        assert safe is not None
        assert learn is not None
        assert legacy is not None
    
    def test_can_import_new_modules(self):
        """Test that new enhancement modules can be imported."""
        from fishertools import network, i18n
        
        assert network is not None
        assert i18n is not None
    
    def test_version_information_available(self):
        """Test that version information is available."""
        import fishertools
        
        assert hasattr(fishertools, '__version__')
        assert isinstance(fishertools.__version__, str)
        assert len(fishertools.__version__) > 0


class TestNewModuleStructure:
    """Tests for the new module structure."""
    
    def test_network_module_structure(self):
        """Test that network module has expected components."""
        from fishertools.network import (
            SafeHTTPClient,
            SafeFileDownloader,
            NetworkResponse,
            DownloadResponse,
            safe_request,
            safe_download,
        )
        
        assert SafeHTTPClient is not None
        assert SafeFileDownloader is not None
        assert NetworkResponse is not None
        assert DownloadResponse is not None
        assert callable(safe_request)
        assert callable(safe_download)
    
    def test_i18n_module_structure(self):
        """Test that i18n module has expected components."""
        from fishertools.i18n import (
            ErrorTranslator,
            LanguageDetector,
            ErrorExplanation,
            translate_error,
            detect_language,
        )
        
        assert ErrorTranslator is not None
        assert LanguageDetector is not None
        assert ErrorExplanation is not None
        assert callable(translate_error)
        assert callable(detect_language)
    
    def test_visualization_enhanced_structure(self):
        """Test that enhanced visualization has expected components."""
        from fishertools.visualization import (
            EnhancedVisualizer,
            AlgorithmVisualizer,
            VisualizationConfig,
            VisualizationResult,
        )
        
        assert EnhancedVisualizer is not None
        assert AlgorithmVisualizer is not None
        assert VisualizationConfig is not None
        assert VisualizationResult is not None
    
    def test_config_enhanced_structure(self):
        """Test that config module has new configuration models."""
        from fishertools.config import (
            NetworkConfig,
            VisualizationConfig,
            I18nConfig,
        )
        
        assert NetworkConfig is not None
        assert VisualizationConfig is not None
        assert I18nConfig is not None


class TestExistingFunctionalityWorks:
    """Tests to ensure existing functionality still works correctly."""
    
    def test_safe_get_still_works(self):
        """Test that safe_get function still works."""
        from fishertools import safe_get
        
        data = {"key": "value"}
        result = safe_get(data, "key")
        assert result == "value"
        
        result = safe_get(data, "missing", default="default")
        assert result == "default"
    
    def test_safe_divide_still_works(self):
        """Test that safe_divide function still works."""
        from fishertools import safe_divide
        
        result = safe_divide(10, 2)
        assert result == 5.0
        
        result = safe_divide(10, 0, default=0)
        assert result == 0
    
    def test_visualize_still_works(self):
        """Test that visualize function still works."""
        from fishertools import visualize
        
        result = visualize([1, 2, 3])
        assert isinstance(result, str)
        assert len(result) > 0



class TestLibraryImportCompatibility:
    """Unit tests for library import compatibility.
    
    **Validates: Requirements 6.3**
    """
    
    def test_import_from_main_module(self):
        """Test that all functions can be imported from main module."""
        # This should not raise ImportError
        from fishertools import (
            explain_error,
            safe_get,
            safe_divide,
            visualize,
            safe_request,
            safe_download,
            translate_error,
            detect_language,
            get_version_info,
        )
        
        assert callable(explain_error)
        assert callable(safe_get)
        assert callable(safe_divide)
        assert callable(visualize)
        assert callable(safe_request)
        assert callable(safe_download)
        assert callable(translate_error)
        assert callable(detect_language)
        assert callable(get_version_info)
    
    def test_import_classes_from_main_module(self):
        """Test that all classes can be imported from main module."""
        from fishertools import (
            SafeHTTPClient,
            SafeFileDownloader,
            NetworkResponse,
            DownloadResponse,
            ErrorTranslator,
            LanguageDetector,
            ErrorExplanation,
            EnhancedVisualizer,
            AlgorithmVisualizer,
            VisualizationConfig,
            VisualizationResult,
        )
        
        assert SafeHTTPClient is not None
        assert SafeFileDownloader is not None
        assert NetworkResponse is not None
        assert DownloadResponse is not None
        assert ErrorTranslator is not None
        assert LanguageDetector is not None
        assert ErrorExplanation is not None
        assert EnhancedVisualizer is not None
        assert AlgorithmVisualizer is not None
        assert VisualizationConfig is not None
        assert VisualizationResult is not None
    
    def test_import_submodules(self):
        """Test that submodules can be imported."""
        import fishertools.network
        import fishertools.i18n
        import fishertools.visualization
        import fishertools.config
        import fishertools.errors
        import fishertools.safe
        import fishertools.learn
        
        assert fishertools.network is not None
        assert fishertools.i18n is not None
        assert fishertools.visualization is not None
        assert fishertools.config is not None
        assert fishertools.errors is not None
        assert fishertools.safe is not None
        assert fishertools.learn is not None
    
    def test_no_import_errors_on_module_load(self):
        """Test that importing fishertools doesn't raise any errors."""
        try:
            import fishertools
            assert fishertools is not None
        except ImportError as e:
            pytest.fail(f"Failed to import fishertools: {e}")
    
    def test_all_exports_in_all_list(self):
        """Test that __all__ contains all expected exports."""
        import fishertools
        
        # Check that __all__ exists
        assert hasattr(fishertools, '__all__')
        assert isinstance(fishertools.__all__, list)
        
        # Check that key functions are in __all__
        expected_exports = [
            'explain_error',
            'safe_get',
            'safe_divide',
            'visualize',
            'safe_request',
            'safe_download',
            'translate_error',
            'detect_language',
            'get_version_info',
        ]
        
        for export in expected_exports:
            assert export in fishertools.__all__, f"{export} should be in __all__"
    
    def test_backward_compatible_imports_work(self):
        """Test that old import patterns still work."""
        # Old pattern: from fishertools import utils
        from fishertools import utils, decorators, helpers
        
        assert utils is not None
        assert decorators is not None
        assert helpers is not None
        
        # Old pattern: from fishertools.safe import safe_get
        from fishertools.safe import safe_get
        assert callable(safe_get)
        
        # Old pattern: from fishertools.errors import explain_error
        from fishertools.errors import explain_error
        assert callable(explain_error)



class TestVersionInformation:
    """Unit tests for version information.
    
    **Validates: Requirements 6.5**
    """
    
    def test_version_attribute_exists(self):
        """Test that __version__ attribute exists."""
        import fishertools
        
        assert hasattr(fishertools, '__version__')
        assert isinstance(fishertools.__version__, str)
    
    def test_version_format(self):
        """Test that version follows semantic versioning format."""
        import fishertools
        import re
        
        # Accept release hotfix suffix format too: X.Y.Z or X.Y.Z.W
        version_pattern = r'^\d+\.\d+\.\d+(?:\.\d+)?$'
        assert re.match(version_pattern, fishertools.__version__), \
            f"Version {fishertools.__version__} doesn't follow semantic versioning"
    
    def test_version_is_055(self):
        """Test that version info remains dynamic and release-agnostic in tests."""
        import fishertools
        from fishertools import get_version_info

        info = get_version_info()
        assert fishertools.__version__ == info["version"]
    
    def test_get_version_info_function_exists(self):
        """Test that get_version_info function exists."""
        from fishertools import get_version_info
        
        assert callable(get_version_info)
    
    def test_get_version_info_returns_dict(self):
        """Test that get_version_info returns a dictionary."""
        from fishertools import get_version_info
        
        info = get_version_info()
        
        assert isinstance(info, dict)
        assert 'version' in info
        assert 'author' in info
        assert 'features' in info
        assert 'enhancements' in info
    
    def test_get_version_info_version_matches(self):
        """Test that get_version_info version matches __version__."""
        import fishertools
        from fishertools import get_version_info
        
        info = get_version_info()
        
        assert info['version'] == fishertools.__version__
    
    def test_get_version_info_has_new_features(self):
        """Test that get_version_info includes new enhancement features."""
        from fishertools import get_version_info
        
        info = get_version_info()
        
        # Check that new features are listed
        assert 'features' in info
        assert isinstance(info['features'], list)
        
        expected_features = [
            'network_operations',
            'internationalization',
            'algorithm_visualization',
        ]
        
        for feature in expected_features:
            assert feature in info['features'], \
                f"Feature '{feature}' should be in version info"
    
    def test_get_version_info_enhancements_are_aligned_with_current_version(self):
        """Test that get_version_info enhancements are not tied to stale historical versions."""
        from fishertools import get_version_info
        import fishertools
        
        info = get_version_info()
        
        assert 'enhancements' in info
        current_key = f"v{fishertools.__version__}"
        assert current_key in info['enhancements']
        assert "v0.4.7" not in info["enhancements"]
        assert isinstance(info['enhancements'][current_key], list)
        assert len(info['enhancements'][current_key]) > 0
    
    def test_author_information(self):
        """Test that author information is present."""
        import fishertools
        
        assert hasattr(fishertools, '__author__')
        assert isinstance(fishertools.__author__, str)
        assert len(fishertools.__author__) > 0
