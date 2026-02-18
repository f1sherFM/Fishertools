"""
Settings management for persistent configuration.

Provides a unified interface for managing network, visualization, and i18n
configuration with file persistence and validation.
"""

import json
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Union
from dataclasses import asdict

from .models import NetworkConfig, VisualizationConfig, I18nConfig, ValidationResult, ConfigError, ErrorSeverity

logger = logging.getLogger(__name__)


class SettingsManager:
    """
    Manages persistent settings for fishertools enhancements.
    
    Handles loading, saving, and validation of configuration settings
    for network operations, visualization, and internationalization.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the settings manager.
        
        Args:
            config_dir: Optional directory for configuration files.
                       Defaults to ~/.fishertools/
        """
        if config_dir is None:
            config_dir = os.path.join(Path.home(), '.fishertools')
        
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / 'settings.json'
        
        # Current configuration instances
        self._network_config: Optional[NetworkConfig] = None
        self._visualization_config: Optional[VisualizationConfig] = None
        self._i18n_config: Optional[I18nConfig] = None
        
        # Ensure config directory exists
        self._ensure_config_dir()
    
    def _ensure_config_dir(self) -> None:
        """Ensure configuration directory exists."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            # If we can't create the directory, we'll use in-memory defaults
            logger.warning(
                "Settings directory fallback activated: dir=%s error=%s",
                self.config_dir,
                e,
            )
    
    def load_settings(self) -> bool:
        """
        Load settings from configuration file.
        
        Returns:
            bool: True if settings were loaded successfully, False otherwise
        """
        try:
            if not self.config_file.exists():
                # Initialize with defaults if file doesn't exist
                self._network_config = NetworkConfig()
                self._visualization_config = VisualizationConfig()
                self._i18n_config = I18nConfig()
                return False
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load each configuration section
            self._network_config = self._load_network_config(data.get('network', {}))
            self._visualization_config = self._load_visualization_config(data.get('visualization', {}))
            self._i18n_config = self._load_i18n_config(data.get('i18n', {}))
            
            return True
            
        except Exception as e:
            # On error, use defaults
            logger.warning(
                "Settings load fallback activated: path=%s error=%s",
                self.config_file,
                e,
            )
            self._network_config = NetworkConfig()
            self._visualization_config = VisualizationConfig()
            self._i18n_config = I18nConfig()
            return False
    
    def save_settings(self) -> bool:
        """
        Save current settings to configuration file.
        
        Returns:
            bool: True if settings were saved successfully, False otherwise
        """
        try:
            # Ensure we have configuration objects
            if self._network_config is None:
                self._network_config = NetworkConfig()
            if self._visualization_config is None:
                self._visualization_config = VisualizationConfig()
            if self._i18n_config is None:
                self._i18n_config = I18nConfig()
            
            # Build configuration dictionary
            config_data = {
                'network': asdict(self._network_config),
                'visualization': asdict(self._visualization_config),
                'i18n': asdict(self._i18n_config)
            }
            
            # Ensure directory exists
            self._ensure_config_dir()
            
            # Write to file
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            logger.warning(
                "Settings save fallback activated: path=%s error=%s",
                self.config_file,
                e,
            )
            return False
    
    def _load_network_config(self, data: Dict[str, Any]) -> NetworkConfig:
        """Load NetworkConfig from dictionary with defaults."""
        defaults = asdict(NetworkConfig())
        defaults.update(data)
        return NetworkConfig(**defaults)
    
    def _load_visualization_config(self, data: Dict[str, Any]) -> VisualizationConfig:
        """Load VisualizationConfig from dictionary with defaults."""
        defaults = asdict(VisualizationConfig())
        defaults.update(data)
        return VisualizationConfig(**defaults)
    
    def _load_i18n_config(self, data: Dict[str, Any]) -> I18nConfig:
        """Load I18nConfig from dictionary with defaults."""
        defaults = asdict(I18nConfig())
        defaults.update(data)
        return I18nConfig(**defaults)
    
    def get_network_config(self) -> NetworkConfig:
        """
        Get current network configuration.
        
        Returns:
            NetworkConfig: Current network configuration
        """
        if self._network_config is None:
            self.load_settings()
        return self._network_config or NetworkConfig()
    
    def set_network_config(self, config: NetworkConfig) -> None:
        """
        Set network configuration.
        
        Args:
            config: New network configuration
        """
        self._network_config = config
    
    def get_visualization_config(self) -> VisualizationConfig:
        """
        Get current visualization configuration.
        
        Returns:
            VisualizationConfig: Current visualization configuration
        """
        if self._visualization_config is None:
            self.load_settings()
        return self._visualization_config or VisualizationConfig()
    
    def set_visualization_config(self, config: VisualizationConfig) -> None:
        """
        Set visualization configuration.
        
        Args:
            config: New visualization configuration
        """
        self._visualization_config = config
    
    def get_i18n_config(self) -> I18nConfig:
        """
        Get current internationalization configuration.
        
        Returns:
            I18nConfig: Current i18n configuration
        """
        if self._i18n_config is None:
            self.load_settings()
        return self._i18n_config or I18nConfig()
    
    def set_i18n_config(self, config: I18nConfig) -> None:
        """
        Set internationalization configuration.
        
        Args:
            config: New i18n configuration
        """
        self._i18n_config = config
    
    def validate_network_config(self, config: NetworkConfig) -> ValidationResult:
        """
        Validate network configuration.
        
        Args:
            config: Network configuration to validate
            
        Returns:
            ValidationResult: Validation result with errors/warnings
        """
        errors = []
        warnings = []
        
        # Validate timeout
        if config.default_timeout <= 0:
            errors.append(ConfigError(
                message="default_timeout must be positive",
                field_path="network.default_timeout",
                severity=ErrorSeverity.ERROR,
                suggested_fix="Set default_timeout to a positive value (e.g., 10.0)"
            ))
        elif config.default_timeout > 300:
            warnings.append(ConfigError(
                message="default_timeout is very high (>300 seconds)",
                field_path="network.default_timeout",
                severity=ErrorSeverity.WARNING,
                suggested_fix="Consider using a lower timeout value"
            ))
        
        # Validate max_retries
        if config.max_retries < 0:
            errors.append(ConfigError(
                message="max_retries cannot be negative",
                field_path="network.max_retries",
                severity=ErrorSeverity.ERROR,
                suggested_fix="Set max_retries to 0 or a positive value"
            ))
        elif config.max_retries > 10:
            warnings.append(ConfigError(
                message="max_retries is very high (>10)",
                field_path="network.max_retries",
                severity=ErrorSeverity.WARNING,
                suggested_fix="Consider using fewer retries"
            ))
        
        # Validate retry_delay
        if config.retry_delay < 0:
            errors.append(ConfigError(
                message="retry_delay cannot be negative",
                field_path="network.retry_delay",
                severity=ErrorSeverity.ERROR,
                suggested_fix="Set retry_delay to 0 or a positive value"
            ))
        
        # Validate chunk_size
        if config.chunk_size <= 0:
            errors.append(ConfigError(
                message="chunk_size must be positive",
                field_path="network.chunk_size",
                severity=ErrorSeverity.ERROR,
                suggested_fix="Set chunk_size to a positive value (e.g., 8192)"
            ))
        elif config.chunk_size < 1024:
            warnings.append(ConfigError(
                message="chunk_size is very small (<1024 bytes)",
                field_path="network.chunk_size",
                severity=ErrorSeverity.WARNING,
                suggested_fix="Consider using a larger chunk size for better performance"
            ))
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_visualization_config(self, config: VisualizationConfig) -> ValidationResult:
        """
        Validate visualization configuration.
        
        Args:
            config: Visualization configuration to validate
            
        Returns:
            ValidationResult: Validation result with errors/warnings
        """
        errors = []
        warnings = []
        
        # Validate style
        valid_styles = ['default', 'tree', 'compact', 'detailed']
        if config.default_style not in valid_styles:
            warnings.append(ConfigError(
                message=f"default_style '{config.default_style}' is not a standard style",
                field_path="visualization.default_style",
                severity=ErrorSeverity.WARNING,
                suggested_fix=f"Consider using one of: {', '.join(valid_styles)}"
            ))
        
        # Validate color_scheme
        valid_schemes = ['default', 'dark', 'light', 'monochrome']
        if config.color_scheme not in valid_schemes:
            warnings.append(ConfigError(
                message=f"color_scheme '{config.color_scheme}' is not a standard scheme",
                field_path="visualization.color_scheme",
                severity=ErrorSeverity.WARNING,
                suggested_fix=f"Consider using one of: {', '.join(valid_schemes)}"
            ))
        
        # Validate export_directory
        if not config.export_directory:
            errors.append(ConfigError(
                message="export_directory cannot be empty",
                field_path="visualization.export_directory",
                severity=ErrorSeverity.ERROR,
                suggested_fix="Set export_directory to a valid path (e.g., './exports')"
            ))
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_i18n_config(self, config: I18nConfig) -> ValidationResult:
        """
        Validate internationalization configuration.
        
        Args:
            config: I18n configuration to validate
            
        Returns:
            ValidationResult: Validation result with errors/warnings
        """
        errors = []
        warnings = []
        
        # Validate languages
        supported_languages = ['en', 'ru']
        
        if config.default_language not in supported_languages:
            errors.append(ConfigError(
                message=f"default_language '{config.default_language}' is not supported",
                field_path="i18n.default_language",
                severity=ErrorSeverity.ERROR,
                suggested_fix=f"Set default_language to one of: {', '.join(supported_languages)}"
            ))
        
        if config.fallback_language not in supported_languages:
            errors.append(ConfigError(
                message=f"fallback_language '{config.fallback_language}' is not supported",
                field_path="i18n.fallback_language",
                severity=ErrorSeverity.ERROR,
                suggested_fix=f"Set fallback_language to one of: {', '.join(supported_languages)}"
            ))
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
    
    def validate_all(self) -> ValidationResult:
        """
        Validate all current configurations.
        
        Returns:
            ValidationResult: Combined validation result
        """
        all_errors = []
        all_warnings = []
        
        # Validate network config
        network_result = self.validate_network_config(self.get_network_config())
        all_errors.extend(network_result.errors)
        all_warnings.extend(network_result.warnings)
        
        # Validate visualization config
        viz_result = self.validate_visualization_config(self.get_visualization_config())
        all_errors.extend(viz_result.errors)
        all_warnings.extend(viz_result.warnings)
        
        # Validate i18n config
        i18n_result = self.validate_i18n_config(self.get_i18n_config())
        all_errors.extend(i18n_result.errors)
        all_warnings.extend(i18n_result.warnings)
        
        return ValidationResult(
            is_valid=len(all_errors) == 0,
            errors=all_errors,
            warnings=all_warnings
        )
    
    def reset_to_defaults(self) -> None:
        """Reset all configurations to default values."""
        self._network_config = NetworkConfig()
        self._visualization_config = VisualizationConfig()
        self._i18n_config = I18nConfig()


# Global settings manager instance
_settings_manager: Optional[SettingsManager] = None


def get_settings_manager() -> SettingsManager:
    """
    Get the global settings manager instance.
    
    Returns:
        SettingsManager: Global settings manager
    """
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
        _settings_manager.load_settings()
    return _settings_manager


def reset_settings_manager() -> None:
    """Reset the global settings manager instance."""
    global _settings_manager
    _settings_manager = None
