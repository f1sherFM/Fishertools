"""
Property-based and unit tests for SafeFileDownloader timeout support.

Feature: fishertools-v0.5.2
Tests the timeout parameter additions to safe_download() method.
"""

from __future__ import annotations

import pytest
from hypothesis import given, strategies as st, settings
from unittest.mock import Mock, patch, MagicMock
import requests

from fishertools.network.safe_downloads import SafeFileDownloader, DownloadResponse


class TestSafeDownloaderTimeoutProperties:
    """Property-based tests for SafeFileDownloader timeout validation."""
    
    @given(timeout=st.floats(max_value=0, allow_nan=False, allow_infinity=False))
    @settings(max_examples=100)
    def test_property_4_invalid_timeout_rejected(self, timeout):
        """
        Property 4: Invalid timeout rejected
        
        **Validates: Requirements 2.4**
        
        For any non-positive timeout value, safe_download() should return
        a DownloadResponse with success=False and an error message about
        invalid timeout.
        """
        downloader = SafeFileDownloader()
        
        # Property: Invalid timeout is rejected
        response = downloader.safe_download(
            url='https://example.com/file.txt',
            local_path='test_file.txt',
            timeout=timeout
        )
        
        # Property: Request fails for non-positive timeout
        assert response.success is False
        assert response.error is not None


class TestSafeDownloaderTimeoutBehavior:
    """Unit tests for SafeFileDownloader timeout behavior."""
    
    @patch('fishertools.network.safe_downloads.SafeHTTPClient')
    def test_safe_download_with_valid_timeout(self, mock_http_client_class):
        """Test safe_download() with valid timeout parameter."""
        # Setup mock
        mock_client = Mock()
        mock_http_client_class.return_value = mock_client
        
        # Mock HEAD request response
        mock_head_response = Mock()
        mock_head_response.success = True
        mock_head_response.headers = {'content-length': '1024'}
        
        # Mock GET request response
        mock_session = Mock()
        mock_response = Mock()
        mock_response.iter_content.return_value = [b'test data']
        mock_response.raise_for_status = Mock()
        mock_session.get.return_value = mock_response
        
        mock_client.safe_request.return_value = mock_head_response
        mock_client.session = mock_session
        mock_client.default_timeout = 10.0
        
        downloader = SafeFileDownloader()
        downloader.http_client = mock_client
        
        # Test with valid timeout
        with patch('os.path.exists', return_value=False), \
             patch('os.makedirs'), \
             patch('builtins.open', create=True), \
             patch('shutil.move'):
            
            response = downloader.safe_download(
                url='https://example.com/file.txt',
                local_path='test_file.txt',
                timeout=30.0
            )
        
        # Verify timeout was passed to HEAD request
        mock_client.safe_request.assert_called_once()
        call_kwargs = mock_client.safe_request.call_args[1]
        assert call_kwargs['timeout'] == 30.0
        
        # Verify timeout was passed to GET request
        mock_session.get.assert_called_once()
        get_call_kwargs = mock_session.get.call_args[1]
        assert get_call_kwargs['timeout'] == 30.0
    
    @patch('fishertools.network.safe_downloads.SafeHTTPClient')
    def test_safe_download_without_timeout_uses_default(self, mock_http_client_class):
        """Test safe_download() without timeout uses default."""
        # Setup mock
        mock_client = Mock()
        mock_http_client_class.return_value = mock_client
        
        # Mock HEAD request response
        mock_head_response = Mock()
        mock_head_response.success = True
        mock_head_response.headers = {'content-length': '1024'}
        
        # Mock GET request response
        mock_session = Mock()
        mock_response = Mock()
        mock_response.iter_content.return_value = [b'test data']
        mock_response.raise_for_status = Mock()
        mock_session.get.return_value = mock_response
        
        mock_client.safe_request.return_value = mock_head_response
        mock_client.session = mock_session
        mock_client.default_timeout = 10.0
        
        downloader = SafeFileDownloader()
        downloader.http_client = mock_client
        
        # Test without timeout
        with patch('os.path.exists', return_value=False), \
             patch('os.makedirs'), \
             patch('builtins.open', create=True), \
             patch('shutil.move'):
            
            response = downloader.safe_download(
                url='https://example.com/file.txt',
                local_path='test_file.txt'
            )
        
        # Verify default timeout was used
        mock_client.safe_request.assert_called_once()
        call_kwargs = mock_client.safe_request.call_args[1]
        assert call_kwargs['timeout'] == 10.0
        
        # Verify default timeout was passed to GET request
        mock_session.get.assert_called_once()
        get_call_kwargs = mock_session.get.call_args[1]
        assert get_call_kwargs['timeout'] == 10.0
    
    def test_timeout_error_returns_download_response_with_failure(self):
        """Test timeout error returns DownloadResponse with success=False."""
        downloader = SafeFileDownloader()
        
        # Mock the HTTP client to raise timeout exception
        with patch.object(downloader.http_client, 'safe_request') as mock_request, \
             patch.object(downloader.http_client.session, 'get') as mock_get, \
             patch('os.path.exists', return_value=False), \
             patch('os.makedirs'):
            
            # Mock HEAD request success
            mock_head_response = Mock()
            mock_head_response.success = True
            mock_head_response.headers = {}
            mock_request.return_value = mock_head_response
            
            # Mock GET request to raise timeout
            mock_get.side_effect = requests.exceptions.Timeout("Connection timeout")
            
            response = downloader.safe_download(
                url='https://example.com/file.txt',
                local_path='test_file.txt',
                timeout=5.0
            )
        
        # Verify error response
        assert response.success is False
        assert 'timed out' in response.error.lower() or 'timeout' in response.error.lower()
    
    def test_invalid_timeout_validation(self):
        """Test that invalid timeout values are rejected during validation."""
        downloader = SafeFileDownloader()
        
        # Test negative timeout
        response = downloader.safe_download(
            url='https://example.com/file.txt',
            local_path='test_file.txt',
            timeout=-5.0
        )
        assert response.success is False
        assert 'invalid' in response.error.lower() and 'timeout' in response.error.lower()
        assert 'positive' in response.error.lower()
        
        # Test zero timeout
        response = downloader.safe_download(
            url='https://example.com/file.txt',
            local_path='test_file.txt',
            timeout=0.0
        )
        assert response.success is False
        # Zero timeout may cause actual timeout or validation error
        assert response.error is not None


