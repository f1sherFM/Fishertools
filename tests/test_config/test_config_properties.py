"""
Property-based tests for configuration management.

Feature: fishertools-enhancements
"""

import json
import tempfile
import os
from hypothesis import given, strategies as st, assume
import pytest

from fishertools.config.models import LearningConfig
from fishertools.config.manager import ConfigurationManager
from fishertools.config.parser import ConfigurationParser


def _is_valid_json(text: str) -> bool:
    """Helper function to check if text is valid JSON."""
    try:
        json.loads(text)
        return True
    except (json.JSONDecodeError, ValueError):
        return False


# Strategy for generating valid LearningConfig objects
@st.composite
def learning_config_strategy(draw):
    """Generate valid LearningConfig objects for property testing."""
    return LearningConfig(
        default_level=draw(st.sampled_from(["beginner", "intermediate", "advanced"])),
        explanation_verbosity=draw(st.sampled_from(["brief", "detailed", "comprehensive"])),
        visual_aids_enabled=draw(st.booleans()),
        diagram_style=draw(st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        color_scheme=draw(st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        progress_tracking_enabled=draw(st.booleans()),
        save_progress_locally=draw(st.booleans()),
        suggested_topics_count=draw(st.integers(min_value=1, max_value=10)),
        max_examples_per_topic=draw(st.integers(min_value=1, max_value=20)),
        exercise_difficulty_progression=draw(st.lists(
            st.sampled_from(["beginner", "intermediate", "advanced"]),
            min_size=1, max_size=5
        )),
        readthedocs_project=draw(st.one_of(
            st.none(),
            st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc')))
        )),
        sphinx_theme=draw(st.text(min_size=1, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc')))),
        enable_interactive_sessions=draw(st.booleans()),
        session_timeout_minutes=draw(st.integers(min_value=1, max_value=180)),
        max_hint_count=draw(st.integers(min_value=0, max_value=10))
    )


# Strategy for generating valid configuration dictionaries
@st.composite
def valid_config_dict_strategy(draw):
    """Generate valid configuration dictionaries for property testing."""
    return {
        "default_level": draw(st.sampled_from(["beginner", "intermediate", "advanced"])),
        "explanation_verbosity": draw(st.sampled_from(["brief", "detailed", "comprehensive"])),
        "visual_aids_enabled": draw(st.booleans()),
        "diagram_style": draw(st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        "color_scheme": draw(st.text(min_size=1, max_size=20, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd')))),
        "progress_tracking_enabled": draw(st.booleans()),
        "save_progress_locally": draw(st.booleans()),
        "suggested_topics_count": draw(st.integers(min_value=1, max_value=10)),
        "max_examples_per_topic": draw(st.integers(min_value=1, max_value=20)),
        "exercise_difficulty_progression": draw(st.lists(
            st.sampled_from(["beginner", "intermediate", "advanced"]),
            min_size=1, max_size=5
        )),
        "readthedocs_project": draw(st.one_of(
            st.none(),
            st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc')))
        )),
        "sphinx_theme": draw(st.text(min_size=1, max_size=30, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc')))),
        "enable_interactive_sessions": draw(st.booleans()),
        "session_timeout_minutes": draw(st.integers(min_value=1, max_value=180)),
        "max_hint_count": draw(st.integers(min_value=0, max_value=10))
    }


# Strategy for generating invalid configuration dictionaries
@st.composite
def invalid_config_dict_strategy(draw):
    """Generate invalid configuration dictionaries for property testing."""
    config = {}
    
    # Add some valid fields
    if draw(st.booleans()):
        config["default_level"] = draw(st.sampled_from(["beginner", "intermediate", "advanced"]))
    
    # Add invalid fields with wrong types or values
    invalid_choices = draw(st.sampled_from([
        "wrong_type_level",
        "wrong_type_verbosity", 
        "wrong_type_bool",
        "wrong_type_int",
        "invalid_enum_value",
        "missing_required"
    ]))
    
    if invalid_choices == "wrong_type_level":
        config["default_level"] = draw(st.integers())  # Should be string
    elif invalid_choices == "wrong_type_verbosity":
        config["explanation_verbosity"] = draw(st.integers())  # Should be string
    elif invalid_choices == "wrong_type_bool":
        config["visual_aids_enabled"] = draw(st.text())  # Should be bool
    elif invalid_choices == "wrong_type_int":
        config["suggested_topics_count"] = draw(st.text())  # Should be int
    elif invalid_choices == "invalid_enum_value":
        config["default_level"] = draw(st.text().filter(lambda x: x not in ["beginner", "intermediate", "advanced"]))
        config["explanation_verbosity"] = "detailed"  # Add required field
    elif invalid_choices == "missing_required":
        # Don't add required fields
        config["visual_aids_enabled"] = True
    
    return config


class TestConfigurationRoundTrip:
    """Property tests for configuration round-trip serialization."""
    
    @given(config=learning_config_strategy())
    def test_json_round_trip_property(self, config):
        """
        Property 8: Configuration Serialization Round-trip (JSON)
        
        For any valid configuration object, parsing then formatting then parsing 
        should produce an equivalent configuration object.
        
        Validates: Requirements 7.4
        """
        # Feature: fishertools-enhancements, Property 8: Configuration Serialization Round-trip
        
        parser = ConfigurationParser()
        manager = ConfigurationManager()
        
        # Format config to JSON
        json_content = parser.format_to_json(config)
        
        # Parse JSON back to dict
        parsed_dict = parser.parse_json(json_content)
        
        # Convert back to LearningConfig
        reconstructed_config = manager._dict_to_config(parsed_dict)
        
        # Verify equivalence
        assert reconstructed_config.default_level == config.default_level
        assert reconstructed_config.explanation_verbosity == config.explanation_verbosity
        assert reconstructed_config.visual_aids_enabled == config.visual_aids_enabled
        assert reconstructed_config.diagram_style == config.diagram_style
        assert reconstructed_config.color_scheme == config.color_scheme
        assert reconstructed_config.progress_tracking_enabled == config.progress_tracking_enabled
        assert reconstructed_config.save_progress_locally == config.save_progress_locally
        assert reconstructed_config.suggested_topics_count == config.suggested_topics_count
        assert reconstructed_config.max_examples_per_topic == config.max_examples_per_topic
        assert reconstructed_config.exercise_difficulty_progression == config.exercise_difficulty_progression
        assert reconstructed_config.readthedocs_project == config.readthedocs_project
        assert reconstructed_config.sphinx_theme == config.sphinx_theme
        assert reconstructed_config.enable_interactive_sessions == config.enable_interactive_sessions
        assert reconstructed_config.session_timeout_minutes == config.session_timeout_minutes
        assert reconstructed_config.max_hint_count == config.max_hint_count
    
    @given(config=learning_config_strategy())
    def test_yaml_round_trip_property(self, config):
        """
        Property 8: Configuration Serialization Round-trip (YAML)
        
        For any valid configuration object, parsing then formatting then parsing 
        should produce an equivalent configuration object.
        
        Validates: Requirements 7.4
        """
        # Feature: fishertools-enhancements, Property 8: Configuration Serialization Round-trip
        
        parser = ConfigurationParser()
        manager = ConfigurationManager()
        
        try:
            # Format config to YAML
            yaml_content = parser.format_to_yaml(config)
            
            # Parse YAML back to dict
            parsed_dict = parser.parse_yaml(yaml_content)
            
            # Convert back to LearningConfig
            reconstructed_config = manager._dict_to_config(parsed_dict)
            
            # Verify equivalence
            assert reconstructed_config.default_level == config.default_level
            assert reconstructed_config.explanation_verbosity == config.explanation_verbosity
            assert reconstructed_config.visual_aids_enabled == config.visual_aids_enabled
            assert reconstructed_config.diagram_style == config.diagram_style
            assert reconstructed_config.color_scheme == config.color_scheme
            assert reconstructed_config.progress_tracking_enabled == config.progress_tracking_enabled
            assert reconstructed_config.save_progress_locally == config.save_progress_locally
            assert reconstructed_config.suggested_topics_count == config.suggested_topics_count
            assert reconstructed_config.max_examples_per_topic == config.max_examples_per_topic
            assert reconstructed_config.exercise_difficulty_progression == config.exercise_difficulty_progression
            assert reconstructed_config.readthedocs_project == config.readthedocs_project
            assert reconstructed_config.sphinx_theme == config.sphinx_theme
            assert reconstructed_config.enable_interactive_sessions == config.enable_interactive_sessions
            assert reconstructed_config.session_timeout_minutes == config.session_timeout_minutes
            assert reconstructed_config.max_hint_count == config.max_hint_count
            
        except ValueError as e:
            if "YAML support not available" in str(e):
                pytest.skip("YAML support not available")
            else:
                raise
    
    @given(config=learning_config_strategy())
    def test_file_round_trip_property_json(self, config):
        """
        Property 8: Configuration Serialization Round-trip (File I/O JSON)
        
        For any valid configuration object, saving to file then loading 
        should produce an equivalent configuration object.
        
        Validates: Requirements 7.4
        """
        # Feature: fishertools-enhancements, Property 8: Configuration Serialization Round-trip
        
        manager = ConfigurationManager()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name
        
        try:
            # Save config to file
            manager.save_config(config, temp_path)
            
            # Load config from file
            loaded_config = manager.load_config(temp_path)
            
            # Verify equivalence
            assert loaded_config.default_level == config.default_level
            assert loaded_config.explanation_verbosity == config.explanation_verbosity
            assert loaded_config.visual_aids_enabled == config.visual_aids_enabled
            assert loaded_config.diagram_style == config.diagram_style
            assert loaded_config.color_scheme == config.color_scheme
            assert loaded_config.progress_tracking_enabled == config.progress_tracking_enabled
            assert loaded_config.save_progress_locally == config.save_progress_locally
            assert loaded_config.suggested_topics_count == config.suggested_topics_count
            assert loaded_config.max_examples_per_topic == config.max_examples_per_topic
            assert loaded_config.exercise_difficulty_progression == config.exercise_difficulty_progression
            assert loaded_config.readthedocs_project == config.readthedocs_project
            assert loaded_config.sphinx_theme == config.sphinx_theme
            assert loaded_config.enable_interactive_sessions == config.enable_interactive_sessions
            assert loaded_config.session_timeout_minutes == config.session_timeout_minutes
            assert loaded_config.max_hint_count == config.max_hint_count
            
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    @given(config=learning_config_strategy())
    def test_file_round_trip_property_yaml(self, config):
        """
        Property 8: Configuration Serialization Round-trip (File I/O YAML)
        
        For any valid configuration object, saving to file then loading 
        should produce an equivalent configuration object.
        
        Validates: Requirements 7.4
        """
        # Feature: fishertools-enhancements, Property 8: Configuration Serialization Round-trip
        
        manager = ConfigurationManager()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            temp_path = f.name
        
        try:
            # Save config to file
            manager.save_config(config, temp_path)
            
            # Load config from file
            loaded_config = manager.load_config(temp_path)
            
            # Verify equivalence
            assert loaded_config.default_level == config.default_level
            assert loaded_config.explanation_verbosity == config.explanation_verbosity
            assert loaded_config.visual_aids_enabled == config.visual_aids_enabled
            assert loaded_config.diagram_style == config.diagram_style
            assert loaded_config.color_scheme == config.color_scheme
            assert loaded_config.progress_tracking_enabled == config.progress_tracking_enabled
            assert loaded_config.save_progress_locally == config.save_progress_locally
            assert loaded_config.suggested_topics_count == config.suggested_topics_count
            assert loaded_config.max_examples_per_topic == config.max_examples_per_topic
            assert loaded_config.exercise_difficulty_progression == config.exercise_difficulty_progression
            assert loaded_config.readthedocs_project == config.readthedocs_project
            assert loaded_config.sphinx_theme == config.sphinx_theme
            assert loaded_config.enable_interactive_sessions == config.enable_interactive_sessions
            assert loaded_config.session_timeout_minutes == config.session_timeout_minutes
            assert loaded_config.max_hint_count == config.max_hint_count
            
        except ValueError as e:
            if "YAML support not available" in str(e):
                pytest.skip("YAML support not available")
            else:
                raise
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)


class TestConfigurationParsingRobustness:
    """Property tests for configuration parsing robustness."""
    
    @given(config_dict=valid_config_dict_strategy())
    def test_valid_config_parsing_property(self, config_dict):
        """
        Property 7: Configuration Parsing Robustness (Valid Configs)
        
        For any valid configuration dictionary, the parser should successfully
        parse it and validation should pass.
        
        Validates: Requirements 7.1, 7.2, 7.5
        """
        # Feature: fishertools-enhancements, Property 7: Configuration Parsing Robustness
        
        parser = ConfigurationParser()
        manager = ConfigurationManager()
        
        # Validation should pass for valid configs
        validation_result = parser.validate_structure(config_dict)
        assert validation_result.is_valid, f"Valid config failed validation: {validation_result.errors}"
        
        # Should be able to convert to LearningConfig without errors
        learning_config = manager._dict_to_config(config_dict)
        assert isinstance(learning_config, LearningConfig)
        
        # JSON serialization should work
        json_content = parser.format_to_json(learning_config)
        assert isinstance(json_content, str)
        assert len(json_content) > 0
        
        # JSON parsing should work
        parsed_dict = parser.parse_json(json_content)
        assert isinstance(parsed_dict, dict)
    
    @given(config_dict=invalid_config_dict_strategy())
    def test_invalid_config_parsing_property(self, config_dict):
        """
        Property 7: Configuration Parsing Robustness (Invalid Configs)
        
        For any invalid configuration dictionary, the parser should detect
        validation errors and provide descriptive error messages.
        
        Validates: Requirements 7.1, 7.2, 7.5
        """
        # Feature: fishertools-enhancements, Property 7: Configuration Parsing Robustness
        
        parser = ConfigurationParser()
        
        # Validation should fail for invalid configs
        validation_result = parser.validate_structure(config_dict)
        
        # Should have validation errors
        assert not validation_result.is_valid or len(validation_result.errors) > 0
        
        # Error messages should be descriptive
        for error in validation_result.errors:
            assert isinstance(error.message, str)
            assert len(error.message) > 0
            assert isinstance(error.field_path, str)
            assert len(error.field_path) > 0
    
    def test_malformed_json_parsing_property(self):
        """
        Property 7: Configuration Parsing Robustness (Malformed JSON)
        
        For any malformed JSON string, the parser should raise a ValueError
        with a descriptive error message.
        
        Validates: Requirements 7.1, 7.2, 7.5
        """
        # Feature: fishertools-enhancements, Property 7: Configuration Parsing Robustness
        
        parser = ConfigurationParser()
        
        # Test with known malformed JSON strings
        malformed_examples = [
            '{"key": value}',  # Missing quotes around value
            '{"key": "value",}',  # Trailing comma
            '{key: "value"}',  # Missing quotes around key
            '{"key": "value"',  # Missing closing brace
            '{"key": "value"}}',  # Extra closing brace
            '{"key": "value" "key2": "value2"}',  # Missing comma
        ]
        
        for malformed_json in malformed_examples:
            # Should raise ValueError for malformed JSON
            with pytest.raises(ValueError) as exc_info:
                parser.parse_json(malformed_json)
            
            # Error message should be descriptive
            error_message = str(exc_info.value)
            assert "Invalid JSON configuration" in error_message
            assert len(error_message) > 0
    
    @given(config_dict=valid_config_dict_strategy())
    def test_config_change_application_property(self, config_dict):
        """
        Property 7: Configuration Parsing Robustness (Dynamic Changes)
        
        For any valid configuration, the system should be able to apply
        configuration changes dynamically without errors.
        
        Validates: Requirements 7.5
        """
        # Feature: fishertools-enhancements, Property 7: Configuration Parsing Robustness
        
        manager = ConfigurationManager()
        
        # Create LearningConfig from dict
        learning_config = manager._dict_to_config(config_dict)
        
        # Should be able to apply configuration without errors
        manager.apply_config(learning_config)
        
        # Should be able to retrieve current config
        current_config = manager.get_current_config()
        assert current_config is not None
        assert isinstance(current_config, LearningConfig)
        
        # Current config should match applied config
        assert current_config.default_level == learning_config.default_level
        assert current_config.explanation_verbosity == learning_config.explanation_verbosity



# Strategies for generating NetworkConfig, VisualizationConfig, and I18nConfig
@st.composite
def network_config_strategy(draw):
    """Generate valid NetworkConfig objects for property testing."""
    from fishertools.config.models import NetworkConfig
    return NetworkConfig(
        default_timeout=draw(st.floats(min_value=0.1, max_value=300.0)),
        max_retries=draw(st.integers(min_value=0, max_value=10)),
        retry_delay=draw(st.floats(min_value=0.0, max_value=10.0)),
        chunk_size=draw(st.integers(min_value=1024, max_value=1048576))
    )


@st.composite
def visualization_config_strategy(draw):
    """Generate valid VisualizationConfig objects for property testing."""
    from fishertools.config.models import VisualizationConfig
    return VisualizationConfig(
        default_style=draw(st.sampled_from(['default', 'tree', 'compact', 'detailed'])),
        default_colors=draw(st.booleans()),
        color_scheme=draw(st.sampled_from(['default', 'dark', 'light', 'monochrome'])),
        export_directory=draw(st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=('Lu', 'Ll', 'Nd', 'Pc', 'Pd'))))
    )


@st.composite
def i18n_config_strategy(draw):
    """Generate valid I18nConfig objects for property testing."""
    from fishertools.config.models import I18nConfig
    return I18nConfig(
        default_language=draw(st.sampled_from(['en', 'ru'])),
        fallback_language=draw(st.sampled_from(['en', 'ru'])),
        auto_detect=draw(st.booleans())
    )


class TestConfigurationPersistence:
    """
    Property tests for configuration persistence.
    
    **Property 18: Configuration persistence**
    **Validates: Requirements 7.1, 7.2, 7.3**
    """
    
    @given(network_config=network_config_strategy())
    def test_network_config_persistence_property(self, network_config):
        """
        Property 18: Configuration persistence (Network)
        
        For any valid network configuration, once set, it should be applied 
        to all subsequent operations until changed.
        
        Validates: Requirements 7.1, 7.2, 7.3
        """
        # Feature: fishertools-enhancements, Property 18: Configuration persistence
        
        from fishertools.config.settings import SettingsManager
        import tempfile
        
        # Create a temporary config directory
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = SettingsManager(config_dir=temp_dir)
            
            # Set network configuration
            manager.set_network_config(network_config)
            
            # Save settings
            save_result = manager.save_settings()
            assert save_result is True
            
            # Create a new manager instance to simulate restart
            new_manager = SettingsManager(config_dir=temp_dir)
            load_result = new_manager.load_settings()
            assert load_result is True
            
            # Retrieve configuration
            loaded_config = new_manager.get_network_config()
            
            # Verify persistence
            assert loaded_config.default_timeout == network_config.default_timeout
            assert loaded_config.max_retries == network_config.max_retries
            assert loaded_config.retry_delay == network_config.retry_delay
            assert loaded_config.chunk_size == network_config.chunk_size
    
    @given(viz_config=visualization_config_strategy())
    def test_visualization_config_persistence_property(self, viz_config):
        """
        Property 18: Configuration persistence (Visualization)
        
        For any valid visualization configuration, once set, it should be applied 
        to all subsequent operations until changed.
        
        Validates: Requirements 7.1, 7.2, 7.3
        """
        # Feature: fishertools-enhancements, Property 18: Configuration persistence
        
        from fishertools.config.settings import SettingsManager
        import tempfile
        
        # Create a temporary config directory
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = SettingsManager(config_dir=temp_dir)
            
            # Set visualization configuration
            manager.set_visualization_config(viz_config)
            
            # Save settings
            save_result = manager.save_settings()
            assert save_result is True
            
            # Create a new manager instance to simulate restart
            new_manager = SettingsManager(config_dir=temp_dir)
            load_result = new_manager.load_settings()
            assert load_result is True
            
            # Retrieve configuration
            loaded_config = new_manager.get_visualization_config()
            
            # Verify persistence
            assert loaded_config.default_style == viz_config.default_style
            assert loaded_config.default_colors == viz_config.default_colors
            assert loaded_config.color_scheme == viz_config.color_scheme
            assert loaded_config.export_directory == viz_config.export_directory
    
    @given(i18n_config=i18n_config_strategy())
    def test_i18n_config_persistence_property(self, i18n_config):
        """
        Property 18: Configuration persistence (I18n)
        
        For any valid i18n configuration, once set, it should be applied 
        to all subsequent operations until changed.
        
        Validates: Requirements 7.1, 7.2, 7.3
        """
        # Feature: fishertools-enhancements, Property 18: Configuration persistence
        
        from fishertools.config.settings import SettingsManager
        import tempfile
        
        # Create a temporary config directory
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = SettingsManager(config_dir=temp_dir)
            
            # Set i18n configuration
            manager.set_i18n_config(i18n_config)
            
            # Save settings
            save_result = manager.save_settings()
            assert save_result is True
            
            # Create a new manager instance to simulate restart
            new_manager = SettingsManager(config_dir=temp_dir)
            load_result = new_manager.load_settings()
            assert load_result is True
            
            # Retrieve configuration
            loaded_config = new_manager.get_i18n_config()
            
            # Verify persistence
            assert loaded_config.default_language == i18n_config.default_language
            assert loaded_config.fallback_language == i18n_config.fallback_language
            assert loaded_config.auto_detect == i18n_config.auto_detect
    
    @given(
        network_config=network_config_strategy(),
        viz_config=visualization_config_strategy(),
        i18n_config=i18n_config_strategy()
    )
    def test_all_configs_persistence_property(self, network_config, viz_config, i18n_config):
        """
        Property 18: Configuration persistence (All configs)
        
        For any valid set of configurations, once set, they should all be 
        persisted and loaded correctly together.
        
        Validates: Requirements 7.1, 7.2, 7.3
        """
        # Feature: fishertools-enhancements, Property 18: Configuration persistence
        
        from fishertools.config.settings import SettingsManager
        import tempfile
        
        # Create a temporary config directory
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = SettingsManager(config_dir=temp_dir)
            
            # Set all configurations
            manager.set_network_config(network_config)
            manager.set_visualization_config(viz_config)
            manager.set_i18n_config(i18n_config)
            
            # Save settings
            save_result = manager.save_settings()
            assert save_result is True
            
            # Create a new manager instance to simulate restart
            new_manager = SettingsManager(config_dir=temp_dir)
            load_result = new_manager.load_settings()
            assert load_result is True
            
            # Retrieve all configurations
            loaded_network = new_manager.get_network_config()
            loaded_viz = new_manager.get_visualization_config()
            loaded_i18n = new_manager.get_i18n_config()
            
            # Verify all configurations persisted correctly
            assert loaded_network.default_timeout == network_config.default_timeout
            assert loaded_network.max_retries == network_config.max_retries
            
            assert loaded_viz.default_style == viz_config.default_style
            assert loaded_viz.default_colors == viz_config.default_colors
            
            assert loaded_i18n.default_language == i18n_config.default_language
            assert loaded_i18n.fallback_language == i18n_config.fallback_language



class TestConfigurationFileLoading:
    """
    Property tests for configuration file loading.
    
    **Property 19: Configuration file loading**
    **Validates: Requirements 7.4**
    """
    
    @given(
        network_config=network_config_strategy(),
        viz_config=visualization_config_strategy(),
        i18n_config=i18n_config_strategy()
    )
    def test_config_file_loading_property(self, network_config, viz_config, i18n_config):
        """
        Property 19: Configuration file loading
        
        For any valid configuration file, the library should load and apply 
        the settings correctly at startup.
        
        Validates: Requirements 7.4
        """
        # Feature: fishertools-enhancements, Property 19: Configuration file loading
        
        from fishertools.config.settings import SettingsManager
        import tempfile
        
        # Create a temporary config directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create and save configuration
            manager = SettingsManager(config_dir=temp_dir)
            manager.set_network_config(network_config)
            manager.set_visualization_config(viz_config)
            manager.set_i18n_config(i18n_config)
            manager.save_settings()
            
            # Create a new manager and load settings
            new_manager = SettingsManager(config_dir=temp_dir)
            load_result = new_manager.load_settings()
            
            # Loading should succeed
            assert load_result is True
            
            # All configurations should be loaded correctly
            loaded_network = new_manager.get_network_config()
            loaded_viz = new_manager.get_visualization_config()
            loaded_i18n = new_manager.get_i18n_config()
            
            # Verify network config
            assert loaded_network.default_timeout == network_config.default_timeout
            assert loaded_network.max_retries == network_config.max_retries
            assert loaded_network.retry_delay == network_config.retry_delay
            assert loaded_network.chunk_size == network_config.chunk_size
            
            # Verify visualization config
            assert loaded_viz.default_style == viz_config.default_style
            assert loaded_viz.default_colors == viz_config.default_colors
            assert loaded_viz.color_scheme == viz_config.color_scheme
            assert loaded_viz.export_directory == viz_config.export_directory
            
            # Verify i18n config
            assert loaded_i18n.default_language == i18n_config.default_language
            assert loaded_i18n.fallback_language == i18n_config.fallback_language
            assert loaded_i18n.auto_detect == i18n_config.auto_detect
    
    def test_missing_config_file_loading_property(self):
        """
        Property 19: Configuration file loading (Missing file)
        
        When no configuration file exists, the library should use safe defaults
        and not raise errors.
        
        Validates: Requirements 7.4
        """
        # Feature: fishertools-enhancements, Property 19: Configuration file loading
        
        from fishertools.config.settings import SettingsManager
        from fishertools.config.models import NetworkConfig, VisualizationConfig, I18nConfig
        import tempfile
        
        # Create a temporary config directory (empty, no config file)
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = SettingsManager(config_dir=temp_dir)
            
            # Loading should not raise errors
            load_result = manager.load_settings()
            
            # Should return False since no file exists
            assert load_result is False
            
            # Should use default configurations
            network_config = manager.get_network_config()
            viz_config = manager.get_visualization_config()
            i18n_config = manager.get_i18n_config()
            
            # Verify defaults are used
            default_network = NetworkConfig()
            assert network_config.default_timeout == default_network.default_timeout
            assert network_config.max_retries == default_network.max_retries
            
            default_viz = VisualizationConfig()
            assert viz_config.default_style == default_viz.default_style
            assert viz_config.default_colors == default_viz.default_colors
            
            default_i18n = I18nConfig()
            assert i18n_config.default_language == default_i18n.default_language
            assert i18n_config.fallback_language == default_i18n.fallback_language
    
    def test_corrupted_config_file_loading_property(self):
        """
        Property 19: Configuration file loading (Corrupted file)
        
        When a configuration file is corrupted, the library should use safe 
        defaults and not crash.
        
        Validates: Requirements 7.4
        """
        # Feature: fishertools-enhancements, Property 19: Configuration file loading
        
        from fishertools.config.settings import SettingsManager
        from fishertools.config.models import NetworkConfig, VisualizationConfig, I18nConfig
        import tempfile
        from pathlib import Path
        
        # Create a temporary config directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a corrupted config file
            config_file = Path(temp_dir) / 'settings.json'
            with open(config_file, 'w') as f:
                f.write('{ invalid json content }')
            
            # Create manager and try to load
            manager = SettingsManager(config_dir=temp_dir)
            load_result = manager.load_settings()
            
            # Loading should not crash, should return False
            assert load_result is False
            
            # Should use default configurations
            network_config = manager.get_network_config()
            viz_config = manager.get_visualization_config()
            i18n_config = manager.get_i18n_config()
            
            # Verify defaults are used
            default_network = NetworkConfig()
            assert network_config.default_timeout == default_network.default_timeout
            
            default_viz = VisualizationConfig()
            assert viz_config.default_style == default_viz.default_style
            
            default_i18n = I18nConfig()
            assert i18n_config.default_language == default_i18n.default_language
    
    @given(
        network_config=network_config_strategy(),
        viz_config=visualization_config_strategy(),
        i18n_config=i18n_config_strategy()
    )
    def test_partial_config_file_loading_property(self, network_config, viz_config, i18n_config):
        """
        Property 19: Configuration file loading (Partial config)
        
        When a configuration file contains only some settings, the library 
        should load those settings and use defaults for missing ones.
        
        Validates: Requirements 7.4
        """
        # Feature: fishertools-enhancements, Property 19: Configuration file loading
        
        from fishertools.config.settings import SettingsManager
        from fishertools.config.models import NetworkConfig, VisualizationConfig, I18nConfig
        import tempfile
        from pathlib import Path
        from dataclasses import asdict
        
        # Create a temporary config directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a partial config file (only network settings)
            config_file = Path(temp_dir) / 'settings.json'
            partial_config = {
                'network': asdict(network_config)
                # Missing visualization and i18n sections
            }
            
            with open(config_file, 'w') as f:
                json.dump(partial_config, f)
            
            # Create manager and load
            manager = SettingsManager(config_dir=temp_dir)
            load_result = manager.load_settings()
            
            # Loading should succeed
            assert load_result is True
            
            # Network config should match what we saved
            loaded_network = manager.get_network_config()
            assert loaded_network.default_timeout == network_config.default_timeout
            assert loaded_network.max_retries == network_config.max_retries
            
            # Visualization and i18n should use defaults
            loaded_viz = manager.get_visualization_config()
            default_viz = VisualizationConfig()
            assert loaded_viz.default_style == default_viz.default_style
            
            loaded_i18n = manager.get_i18n_config()
            default_i18n = I18nConfig()
            assert loaded_i18n.default_language == default_i18n.default_language



# Strategies for generating invalid configurations
@st.composite
def invalid_network_config_strategy(draw):
    """Generate invalid NetworkConfig objects for property testing."""
    from fishertools.config.models import NetworkConfig
    
    invalid_choice = draw(st.sampled_from([
        'negative_timeout',
        'negative_retries',
        'negative_delay',
        'zero_chunk_size',
        'negative_chunk_size'
    ]))
    
    if invalid_choice == 'negative_timeout':
        return NetworkConfig(default_timeout=-1.0)
    elif invalid_choice == 'negative_retries':
        return NetworkConfig(max_retries=-1)
    elif invalid_choice == 'negative_delay':
        return NetworkConfig(retry_delay=-1.0)
    elif invalid_choice == 'zero_chunk_size':
        return NetworkConfig(chunk_size=0)
    else:  # negative_chunk_size
        return NetworkConfig(chunk_size=-1024)


@st.composite
def invalid_visualization_config_strategy(draw):
    """Generate invalid VisualizationConfig objects for property testing."""
    from fishertools.config.models import VisualizationConfig
    
    # Empty export directory is invalid
    return VisualizationConfig(export_directory='')


@st.composite
def invalid_i18n_config_strategy(draw):
    """Generate invalid I18nConfig objects for property testing."""
    from fishertools.config.models import I18nConfig
    
    invalid_choice = draw(st.sampled_from([
        'invalid_default_lang',
        'invalid_fallback_lang',
        'both_invalid'
    ]))
    
    if invalid_choice == 'invalid_default_lang':
        return I18nConfig(default_language='fr')  # Unsupported language
    elif invalid_choice == 'invalid_fallback_lang':
        return I18nConfig(fallback_language='de')  # Unsupported language
    else:  # both_invalid
        return I18nConfig(default_language='fr', fallback_language='de')


class TestConfigurationValidation:
    """
    Property tests for configuration validation.
    
    **Property 20: Configuration validation**
    **Validates: Requirements 7.5**
    """
    
    @given(network_config=network_config_strategy())
    def test_valid_network_config_validation_property(self, network_config):
        """
        Property 20: Configuration validation (Valid network config)
        
        For any valid network configuration, validation should pass without errors.
        
        Validates: Requirements 7.5
        """
        # Feature: fishertools-enhancements, Property 20: Configuration validation
        
        from fishertools.config.settings import SettingsManager
        
        manager = SettingsManager()
        validation_result = manager.validate_network_config(network_config)
        
        # Valid configuration should pass validation
        assert validation_result.is_valid is True
        assert len(validation_result.errors) == 0
    
    @given(invalid_config=invalid_network_config_strategy())
    def test_invalid_network_config_validation_property(self, invalid_config):
        """
        Property 20: Configuration validation (Invalid network config)
        
        For any invalid network configuration, validation should detect errors
        and provide descriptive messages.
        
        Validates: Requirements 7.5
        """
        # Feature: fishertools-enhancements, Property 20: Configuration validation
        
        from fishertools.config.settings import SettingsManager
        
        manager = SettingsManager()
        validation_result = manager.validate_network_config(invalid_config)
        
        # Invalid configuration should fail validation
        assert validation_result.is_valid is False
        assert len(validation_result.errors) > 0
        
        # Error messages should be descriptive
        for error in validation_result.errors:
            assert isinstance(error.message, str)
            assert len(error.message) > 0
            assert error.field_path.startswith('network.')
            assert error.suggested_fix is not None
            assert len(error.suggested_fix) > 0
    
    @given(viz_config=visualization_config_strategy())
    def test_valid_visualization_config_validation_property(self, viz_config):
        """
        Property 20: Configuration validation (Valid visualization config)
        
        For any valid visualization configuration, validation should pass without errors.
        
        Validates: Requirements 7.5
        """
        # Feature: fishertools-enhancements, Property 20: Configuration validation
        
        from fishertools.config.settings import SettingsManager
        
        manager = SettingsManager()
        validation_result = manager.validate_visualization_config(viz_config)
        
        # Valid configuration should pass validation
        assert validation_result.is_valid is True
        assert len(validation_result.errors) == 0
    
    @given(invalid_config=invalid_visualization_config_strategy())
    def test_invalid_visualization_config_validation_property(self, invalid_config):
        """
        Property 20: Configuration validation (Invalid visualization config)
        
        For any invalid visualization configuration, validation should detect errors
        and provide descriptive messages.
        
        Validates: Requirements 7.5
        """
        # Feature: fishertools-enhancements, Property 20: Configuration validation
        
        from fishertools.config.settings import SettingsManager
        
        manager = SettingsManager()
        validation_result = manager.validate_visualization_config(invalid_config)
        
        # Invalid configuration should fail validation
        assert validation_result.is_valid is False
        assert len(validation_result.errors) > 0
        
        # Error messages should be descriptive
        for error in validation_result.errors:
            assert isinstance(error.message, str)
            assert len(error.message) > 0
            assert error.field_path.startswith('visualization.')
            assert error.suggested_fix is not None
            assert len(error.suggested_fix) > 0
    
    @given(i18n_config=i18n_config_strategy())
    def test_valid_i18n_config_validation_property(self, i18n_config):
        """
        Property 20: Configuration validation (Valid i18n config)
        
        For any valid i18n configuration, validation should pass without errors.
        
        Validates: Requirements 7.5
        """
        # Feature: fishertools-enhancements, Property 20: Configuration validation
        
        from fishertools.config.settings import SettingsManager
        
        manager = SettingsManager()
        validation_result = manager.validate_i18n_config(i18n_config)
        
        # Valid configuration should pass validation
        assert validation_result.is_valid is True
        assert len(validation_result.errors) == 0
    
    @given(invalid_config=invalid_i18n_config_strategy())
    def test_invalid_i18n_config_validation_property(self, invalid_config):
        """
        Property 20: Configuration validation (Invalid i18n config)
        
        For any invalid i18n configuration, validation should detect errors
        and provide descriptive messages.
        
        Validates: Requirements 7.5
        """
        # Feature: fishertools-enhancements, Property 20: Configuration validation
        
        from fishertools.config.settings import SettingsManager
        
        manager = SettingsManager()
        validation_result = manager.validate_i18n_config(invalid_config)
        
        # Invalid configuration should fail validation
        assert validation_result.is_valid is False
        assert len(validation_result.errors) > 0
        
        # Error messages should be descriptive
        for error in validation_result.errors:
            assert isinstance(error.message, str)
            assert len(error.message) > 0
            assert error.field_path.startswith('i18n.')
            assert error.suggested_fix is not None
            assert len(error.suggested_fix) > 0
    
    @given(
        network_config=network_config_strategy(),
        viz_config=visualization_config_strategy(),
        i18n_config=i18n_config_strategy()
    )
    def test_validate_all_configs_property(self, network_config, viz_config, i18n_config):
        """
        Property 20: Configuration validation (All configs)
        
        For any set of valid configurations, validate_all should pass without errors.
        
        Validates: Requirements 7.5
        """
        # Feature: fishertools-enhancements, Property 20: Configuration validation
        
        from fishertools.config.settings import SettingsManager
        
        manager = SettingsManager()
        manager.set_network_config(network_config)
        manager.set_visualization_config(viz_config)
        manager.set_i18n_config(i18n_config)
        
        validation_result = manager.validate_all()
        
        # All valid configurations should pass validation
        assert validation_result.is_valid is True
        assert len(validation_result.errors) == 0
    
    def test_validation_with_warnings_property(self):
        """
        Property 20: Configuration validation (Warnings)
        
        For configurations with non-standard but valid values, validation should
        pass but include warnings.
        
        Validates: Requirements 7.5
        """
        # Feature: fishertools-enhancements, Property 20: Configuration validation
        
        from fishertools.config.settings import SettingsManager
        from fishertools.config.models import NetworkConfig, VisualizationConfig
        
        manager = SettingsManager()
        
        # Create config with values that trigger warnings
        network_config = NetworkConfig(
            default_timeout=400.0,  # Very high timeout (>300)
            max_retries=15,  # Very high retries (>10)
            chunk_size=512  # Very small chunk size (<1024)
        )
        
        validation_result = manager.validate_network_config(network_config)
        
        # Should be valid but have warnings
        assert validation_result.is_valid is True
        assert len(validation_result.errors) == 0
        assert len(validation_result.warnings) > 0
        
        # Warnings should be descriptive
        for warning in validation_result.warnings:
            assert isinstance(warning.message, str)
            assert len(warning.message) > 0
            assert warning.suggested_fix is not None
    
    def test_reset_to_defaults_property(self):
        """
        Property 20: Configuration validation (Reset to defaults)
        
        After resetting to defaults, all configurations should be valid.
        
        Validates: Requirements 7.5
        """
        # Feature: fishertools-enhancements, Property 20: Configuration validation
        
        from fishertools.config.settings import SettingsManager
        
        manager = SettingsManager()
        
        # Reset to defaults
        manager.reset_to_defaults()
        
        # Validate all configurations
        validation_result = manager.validate_all()
        
        # Default configurations should always be valid
        assert validation_result.is_valid is True
        assert len(validation_result.errors) == 0
