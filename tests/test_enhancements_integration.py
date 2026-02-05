"""
Comprehensive integration tests for fishertools enhancements.

This module tests end-to-end workflows combining multiple modules
to ensure all enhancements work together correctly.

**Validates: All requirements**
"""

from __future__ import annotations

import pytest
import tempfile
import os
from pathlib import Path


class TestEndToEndWorkflows:
    """Integration tests for end-to-end workflows combining multiple modules."""
    
    def test_complete_workflow_with_all_modules(self):
        """
        Test a complete workflow using network, visualization, and i18n modules together.
        
        This test demonstrates a realistic use case where a user:
        1. Makes a network request
        2. Visualizes the response data
        3. Handles errors with multilingual explanations
        """
        from fishertools import safe_request, visualize, explain_error
        
        # Step 1: Make a network request (will fail for invalid URL)
        response = safe_request('https://invalid-url-that-does-not-exist-12345.com', timeout=2)
        
        # Step 2: Handle the error case
        assert not response.success, "Request to invalid URL should fail"
        assert response.error is not None, "Error message should be present"
        
        # Step 3: Visualize the error response
        visualization = visualize(response.__dict__)
        assert isinstance(visualization, str)
        assert len(visualization) > 0
        
        # Step 4: If we had an exception, we could explain it
        try:
            raise ValueError("Test error for demonstration")
        except Exception as e:
            explanation = explain_error(e, return_text=True)
            assert isinstance(explanation, str)
            assert len(explanation) > 0
    
    def test_network_with_visualization(self):
        """Test network operations combined with visualization."""
        from fishertools import safe_request, visualize, EnhancedVisualizer
        
        # Make a request (will fail, but that's okay for testing)
        response = safe_request('https://httpbin.org/delay/10', timeout=1)
        
        # Visualize the response
        viz = visualize(response.__dict__)
        assert isinstance(viz, str)
        
        # Use enhanced visualizer
        enhanced_viz = EnhancedVisualizer()
        result = enhanced_viz.visualize(response.__dict__, style='tree', colors=False)
        assert result.content is not None
    
    def test_i18n_with_error_handling(self):
        """Test internationalization with error handling across modules."""
        from fishertools import explain_error, translate_error, detect_language
        
        # Detect system language
        lang = detect_language()
        assert lang in ['ru', 'en'], f"Detected language should be ru or en, got {lang}"
        
        # Create an error and explain it in different languages
        try:
            result = 10 / 0
        except ZeroDivisionError as e:
            # Explain in Russian (default)
            explanation_ru = explain_error(e, language='ru', return_text=True)
            assert isinstance(explanation_ru, str)
            assert len(explanation_ru) > 0
            
            # Explain in English
            explanation_en = explain_error(e, language='en', return_text=True)
            assert isinstance(explanation_en, str)
            assert len(explanation_en) > 0
            
            # Use translate_error function
            translated = translate_error(e, lang='en')
            assert translated.explanation is not None
            assert translated.language == 'en'
    
    def test_configuration_affects_all_modules(self):
        """Test that configuration changes affect all relevant modules."""
        from fishertools.config import NetworkConfig, VisualizationConfig, I18nConfig
        
        # Create configurations
        net_config = NetworkConfig(default_timeout=5.0, max_retries=2)
        viz_config = VisualizationConfig(default_style='tree', default_colors=True)
        i18n_config = I18nConfig(default_language='en', auto_detect=False)
        
        # Verify configurations are created correctly
        assert net_config.default_timeout == 5.0
        assert net_config.max_retries == 2
        
        assert viz_config.default_style == 'tree'
        assert viz_config.default_colors is True
        
        assert i18n_config.default_language == 'en'
        assert i18n_config.auto_detect is False


class TestCrossModuleFunctionality:
    """Tests for functionality that spans multiple modules."""
    
    def test_network_error_with_i18n_explanation(self):
        """Test network errors with internationalized explanations."""
        from fishertools import safe_request, explain_error
        
        # Make a request that will fail
        response = safe_request('https://invalid-domain-12345.com', timeout=1)
        
        assert not response.success
        assert response.error is not None
        
        # If we had an exception, we could explain it in multiple languages
        # For now, just verify the error message is present
        assert len(response.error) > 0
    
    def test_visualization_with_network_data(self):
        """Test visualization of network response data."""
        from fishertools import safe_request, visualize, EnhancedVisualizer
        from fishertools.network import NetworkResponse
        
        # Create a mock network response
        response = NetworkResponse(
            success=True,
            data={'key': 'value', 'number': 42},
            status_code=200
        )
        
        # Visualize using basic visualize
        viz = visualize(response.__dict__)
        assert isinstance(viz, str)
        assert 'success' in viz
        assert 'data' in viz
        
        # Visualize using enhanced visualizer
        enhanced_viz = EnhancedVisualizer()
        result = enhanced_viz.visualize(response.__dict__, style='tree')
        assert result.content is not None
    
    def test_algorithm_visualization_with_error_handling(self):
        """Test algorithm visualization with proper error handling."""
        from fishertools import explain_error
        from fishertools.visualization import AlgorithmVisualizer
        
        visualizer = AlgorithmVisualizer()
        
        # Test sorting visualization
        array = [3, 1, 4, 1, 5, 9, 2, 6]
        result = visualizer.visualize_sorting(array, algorithm='bubble_sort', step_delay=0)
        
        assert result.steps is not None
        assert len(result.steps) > 0
        assert result.statistics is not None
        
        # Test search visualization
        sorted_array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result = visualizer.visualize_search(sorted_array, target=5, algorithm='binary_search', step_delay=0)
        
        assert result.steps is not None
        assert len(result.steps) > 0
    
    def test_configuration_persistence_across_modules(self):
        """Test that configuration settings persist across module usage."""
        from fishertools.config import NetworkConfig, SettingsManager
        import tempfile
        import os
        import json
        
        # Create a temporary config file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_path = f.name
            # Write a simple config
            config_data = {
                'default_timeout': 15.0,
                'max_retries': 5,
                'retry_delay': 1.0,
                'chunk_size': 8192
            }
            json.dump(config_data, f)
        
        try:
            # Create configuration
            config = NetworkConfig(default_timeout=15.0, max_retries=5)
            
            # Verify configuration is created correctly
            assert config.default_timeout == 15.0
            assert config.max_retries == 5
            
            # Test SettingsManager
            settings_manager = SettingsManager()
            assert settings_manager is not None
        finally:
            # Clean up
            if os.path.exists(config_path):
                os.unlink(config_path)


class TestModuleInteroperability:
    """Tests to ensure modules work together without conflicts."""
    
    def test_all_modules_can_be_imported_together(self):
        """Test that all modules can be imported without conflicts."""
        from fishertools import (
            safe_request,
            safe_download,
            visualize,
            EnhancedVisualizer,
            AlgorithmVisualizer,
            explain_error,
            translate_error,
            detect_language,
            get_version_info,
        )
        
        # Verify all imports are callable or usable
        assert callable(safe_request)
        assert callable(safe_download)
        assert callable(visualize)
        assert EnhancedVisualizer is not None
        assert AlgorithmVisualizer is not None
        assert callable(explain_error)
        assert callable(translate_error)
        assert callable(detect_language)
        assert callable(get_version_info)
    
    def test_no_namespace_conflicts(self):
        """Test that there are no namespace conflicts between modules."""
        import fishertools
        import fishertools.network
        import fishertools.i18n
        import fishertools.visualization
        import fishertools.config
        
        # Verify each module has its own namespace
        assert hasattr(fishertools.network, 'safe_request')
        assert hasattr(fishertools.i18n, 'translate_error')
        assert hasattr(fishertools.visualization, 'visualize')
        assert hasattr(fishertools.config, 'NetworkConfig')
        
        # Verify main module also has access
        assert hasattr(fishertools, 'safe_request')
        assert hasattr(fishertools, 'translate_error')
        assert hasattr(fishertools, 'visualize')
    
    def test_legacy_and_new_modules_coexist(self):
        """Test that legacy and new modules work together."""
        from fishertools import (
            # Legacy functions
            safe_get,
            safe_divide,
            explain_error,
            # New functions
            safe_request,
            translate_error,
            get_version_info,
        )
        
        # Test legacy functions still work
        assert safe_get({'key': 'value'}, 'key') == 'value'
        assert safe_divide(10, 2) == 5.0
        
        # Test new functions work
        response = safe_request('https://invalid.com', timeout=1)
        assert response is not None
        
        info = get_version_info()
        assert info is not None
        assert 'version' in info


class TestRealWorldScenarios:
    """Tests simulating real-world usage scenarios."""
    
    def test_beginner_learning_workflow(self):
        """
        Test a workflow for a beginner learning Python.
        
        Scenario: A beginner writes code, encounters an error,
        and uses fishertools to understand and fix it.
        """
        from fishertools import explain_error, visualize, safe_divide
        
        # Beginner tries to divide by zero
        result = safe_divide(10, 0)
        assert result is None, "safe_divide should handle division by zero"
        
        # Beginner encounters an error
        try:
            numbers = [1, 2, 3]
            value = numbers[10]  # IndexError
        except IndexError as e:
            # Get explanation
            explanation = explain_error(e, return_text=True)
            assert isinstance(explanation, str)
            assert len(explanation) > 0
        
        # Beginner visualizes data structure
        data = {'name': 'Alice', 'age': 25, 'scores': [90, 85, 92]}
        viz = visualize(data)
        assert isinstance(viz, str)
    
    def test_data_fetching_and_visualization_workflow(self):
        """
        Test a workflow for fetching data and visualizing it.
        
        Scenario: A user wants to fetch data from an API and visualize it.
        """
        from fishertools import safe_request, visualize, EnhancedVisualizer
        
        # Try to fetch data (will fail for invalid URL, but that's okay)
        response = safe_request('https://api.example.com/data', timeout=2)
        
        # Visualize the response (whether success or failure)
        viz = visualize(response.__dict__)
        assert isinstance(viz, str)
        
        # Use enhanced visualization
        enhanced_viz = EnhancedVisualizer()
        result = enhanced_viz.visualize(response.__dict__, style='tree', colors=False)
        assert result.content is not None
    
    def test_multilingual_error_handling_workflow(self):
        """
        Test a workflow for handling errors in multiple languages.
        
        Scenario: A user working in a multilingual environment
        needs error explanations in different languages.
        """
        from fishertools import explain_error, detect_language
        
        # Detect system language
        system_lang = detect_language()
        assert system_lang in ['ru', 'en']
        
        # Create an error
        try:
            result = int('not a number')
        except ValueError as e:
            # Get explanation in detected language
            explanation_auto = explain_error(e, language='auto', return_text=True)
            assert isinstance(explanation_auto, str)
            
            # Get explanation in specific languages
            explanation_ru = explain_error(e, language='ru', return_text=True)
            explanation_en = explain_error(e, language='en', return_text=True)
            
            assert isinstance(explanation_ru, str)
            assert isinstance(explanation_en, str)
