"""
Tests for enhancement configuration models.

This module tests the configuration data structures for network, visualization,
and i18n enhancements.
"""

from __future__ import annotations

import pytest

from fishertools.config.models import (
    NetworkConfig,
    VisualizationConfig,
    I18nConfig,
)


class TestNetworkConfig:
    """Tests for NetworkConfig data model."""
    
    def test_default_network_config(self):
        """Test default NetworkConfig."""
        config = NetworkConfig()
        assert config.default_timeout == 10.0
        assert config.max_retries == 3
        assert config.retry_delay == 1.0
        assert config.chunk_size == 8192
    
    def test_custom_network_config(self):
        """Test custom NetworkConfig."""
        config = NetworkConfig(
            default_timeout=30.0,
            max_retries=5,
            retry_delay=2.0,
            chunk_size=16384
        )
        assert config.default_timeout == 30.0
        assert config.max_retries == 5
        assert config.retry_delay == 2.0
        assert config.chunk_size == 16384


class TestVisualizationConfig:
    """Tests for VisualizationConfig data model."""
    
    def test_default_visualization_config(self):
        """Test default VisualizationConfig."""
        config = VisualizationConfig()
        assert config.default_style == 'default'
        assert config.default_colors is False
        assert config.color_scheme == 'default'
        assert config.export_directory == './exports'
    
    def test_custom_visualization_config(self):
        """Test custom VisualizationConfig."""
        config = VisualizationConfig(
            default_style='tree',
            default_colors=True,
            color_scheme='dark',
            export_directory='/tmp/viz'
        )
        assert config.default_style == 'tree'
        assert config.default_colors is True
        assert config.color_scheme == 'dark'
        assert config.export_directory == '/tmp/viz'


class TestI18nConfig:
    """Tests for I18nConfig data model."""
    
    def test_default_i18n_config(self):
        """Test default I18nConfig."""
        config = I18nConfig()
        assert config.default_language == 'ru'
        assert config.fallback_language == 'en'
        assert config.auto_detect is True
    
    def test_custom_i18n_config(self):
        """Test custom I18nConfig."""
        config = I18nConfig(
            default_language='en',
            fallback_language='ru',
            auto_detect=False
        )
        assert config.default_language == 'en'
        assert config.fallback_language == 'ru'
        assert config.auto_detect is False
