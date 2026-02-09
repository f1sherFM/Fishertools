"""
Tests for network module data models.

This module tests the core data structures used in network operations.
"""

from __future__ import annotations

import pytest
from hypothesis import given, strategies as st

from fishertools.network.models import (
    NetworkRequest,
    NetworkResponse,
    DownloadProgress,
    DownloadResponse,
)


class TestNetworkRequest:
    """Tests for NetworkRequest data model."""
    
    def test_network_request_creation(self):
        """Test basic NetworkRequest creation."""
        request = NetworkRequest(url="https://example.com")
        assert request.url == "https://example.com"
        assert request.method == "GET"
        assert request.timeout == 10.0
    
    def test_network_request_with_custom_values(self):
        """Test NetworkRequest with custom values."""
        request = NetworkRequest(
            url="https://api.example.com",
            method="POST",
            timeout=30.0,
            headers={"Content-Type": "application/json"},
            params={"key": "value"},
            data={"test": "data"}
        )
        assert request.url == "https://api.example.com"
        assert request.method == "POST"
        assert request.timeout == 30.0
        assert request.headers == {"Content-Type": "application/json"}
        assert request.params == {"key": "value"}
        assert request.data == {"test": "data"}


class TestNetworkResponse:
    """Tests for NetworkResponse data model."""
    
    def test_successful_response(self):
        """Test successful NetworkResponse."""
        response = NetworkResponse(success=True, data={"result": "ok"})
        assert response.success is True
        assert response.data == {"result": "ok"}
        assert response.error is None
        assert bool(response) is True
    
    def test_failed_response(self):
        """Test failed NetworkResponse."""
        response = NetworkResponse(
            success=False,
            error="Connection timeout",
            status_code=408
        )
        assert response.success is False
        assert response.error == "Connection timeout"
        assert response.status_code == 408
        assert bool(response) is False
    
    # New tests for v0.5.1 enhancements
    
    def test_json_method_on_successful_response(self):
        """Test .json() method returns data on successful response."""
        data = {"user": "test", "id": 123}
        response = NetworkResponse(success=True, data=data)
        assert response.json() == data
        assert response.json() == response.data
    
    def test_json_method_raises_on_failed_response(self):
        """Test .json() raises ValueError on failed requests."""
        response = NetworkResponse(success=False, error="Network error")
        with pytest.raises(ValueError) as exc_info:
            response.json()
        assert "Cannot parse JSON from failed request" in str(exc_info.value)
        assert "Network error" in str(exc_info.value)
    
    def test_content_property_with_none(self):
        """Test .content handles None data."""
        response = NetworkResponse(success=True, data=None)
        assert response.content == b''
    
    def test_content_property_with_string(self):
        """Test .content handles string data."""
        response = NetworkResponse(success=True, data="Hello World")
        assert response.content == b'Hello World'
    
    def test_content_property_with_bytes(self):
        """Test .content handles bytes data."""
        response = NetworkResponse(success=True, data=b'Binary data')
        assert response.content == b'Binary data'
    
    def test_content_property_with_dict(self):
        """Test .content handles dict data (JSON serialization)."""
        data = {"key": "value", "number": 42}
        response = NetworkResponse(success=True, data=data)
        content = response.content
        assert isinstance(content, bytes)
        # Verify it's valid JSON
        import json
        decoded = json.loads(content.decode('utf-8'))
        assert decoded == data
    
    def test_text_property_with_none(self):
        """Test .text handles None data."""
        response = NetworkResponse(success=True, data=None)
        assert response.text == ''
    
    def test_text_property_with_string(self):
        """Test .text handles string data."""
        response = NetworkResponse(success=True, data="Hello World")
        assert response.text == "Hello World"
    
    def test_text_property_with_bytes_utf8(self):
        """Test .text handles UTF-8 bytes data."""
        response = NetworkResponse(success=True, data=b'Hello World')
        assert response.text == "Hello World"
    
    def test_text_property_with_bytes_non_utf8(self):
        """Test .text handles non-UTF-8 bytes data (falls back to latin-1)."""
        response = NetworkResponse(success=True, data=b'\x80\x81\x82')
        # Should not raise, should decode with latin-1
        text = response.text
        assert isinstance(text, str)
        assert len(text) == 3
    
    def test_text_property_with_dict(self):
        """Test .text handles dict data (JSON serialization)."""
        data = {"key": "value", "number": 42}
        response = NetworkResponse(success=True, data=data)
        text = response.text
        assert isinstance(text, str)
        # Verify it's valid JSON
        import json
        decoded = json.loads(text)
        assert decoded == data
    
    def test_backward_compatibility_data_attribute(self):
        """Test backward compatibility - .data attribute still works."""
        data = {"test": "data"}
        response = NetworkResponse(success=True, data=data)
        # Direct access to .data should work
        assert response.data == data
        # Should be the same object
        assert response.data is data


class TestDownloadProgress:
    """Tests for DownloadProgress data model."""
    
    def test_download_progress_with_total(self):
        """Test DownloadProgress with known total size."""
        progress = DownloadProgress(
            bytes_downloaded=500,
            total_bytes=1000,
            percentage=50.0,
            speed_bps=1024.0
        )
        assert progress.bytes_downloaded == 500
        assert progress.total_bytes == 1000
        assert progress.percentage == 50.0
        assert progress.speed_bps == 1024.0
        assert "50.0%" in str(progress)
    
    def test_download_progress_without_total(self):
        """Test DownloadProgress without known total size."""
        progress = DownloadProgress(bytes_downloaded=500)
        assert progress.bytes_downloaded == 500
        assert progress.total_bytes is None
        assert progress.percentage is None
        assert "500 bytes" in str(progress)


class TestDownloadResponse:
    """Tests for DownloadResponse data model."""
    
    def test_successful_download(self):
        """Test successful DownloadResponse."""
        response = DownloadResponse(
            success=True,
            file_path="/tmp/file.txt",
            bytes_downloaded=1024
        )
        assert response.success is True
        assert response.file_path == "/tmp/file.txt"
        assert response.bytes_downloaded == 1024
        assert bool(response) is True
    
    def test_failed_download(self):
        """Test failed DownloadResponse."""
        response = DownloadResponse(
            success=False,
            error="Disk full",
            bytes_downloaded=512
        )
        assert response.success is False
        assert response.error == "Disk full"
        assert response.bytes_downloaded == 512
        assert bool(response) is False

