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
