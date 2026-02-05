"""
Configuration Management Module

Handles learning system configuration through various file formats
with validation and error recovery. Also provides configuration for
network operations, visualization, and internationalization.
"""

from .manager import ConfigurationManager
from .parser import ConfigurationParser
from .models import (
    LearningConfig,
    ValidationResult,
    RecoveryAction,
    ConfigError,
    NetworkConfig,
    VisualizationConfig,
    I18nConfig,
)
from .settings import (
    SettingsManager,
    get_settings_manager,
    reset_settings_manager,
)

__all__ = [
    "ConfigurationManager",
    "ConfigurationParser",
    "LearningConfig",
    "ValidationResult",
    "RecoveryAction", 
    "ConfigError",
    "NetworkConfig",
    "VisualizationConfig",
    "I18nConfig",
    "SettingsManager",
    "get_settings_manager",
    "reset_settings_manager",
]