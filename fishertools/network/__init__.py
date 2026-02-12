"""
Safe network operations module for fishertools

This module provides safe HTTP request and file download operations with
comprehensive error handling, timeouts, and progress tracking.

Main components:
    - SafeHTTPClient: Safe HTTP request operations
    - SafeFileDownloader: Safe file download with progress tracking
    - NetworkResponse: Structured response for HTTP operations
    - DownloadResponse: Structured response for download operations
    
Convenience functions:
    - safe_request(): Make a safe HTTP request without creating a client
    - safe_download(): Download a file safely without creating a downloader
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Callable

from .safe_requests import SafeHTTPClient
from .models import NetworkRequest, NetworkResponse
from .safe_downloads import (
    SafeFileDownloader, 
    DownloadResponse, 
    DownloadProgress
)

# Module-level default client and downloader for convenience functions
_default_client: Optional[SafeHTTPClient] = None
_default_downloader: Optional[SafeFileDownloader] = None


def _get_default_client() -> SafeHTTPClient:
    """Get or create the default HTTP client"""
    global _default_client
    if _default_client is None:
        _default_client = SafeHTTPClient()
    return _default_client


def _get_default_downloader() -> SafeFileDownloader:
    """Get or create the default file downloader"""
    global _default_downloader
    if _default_downloader is None:
        _default_downloader = SafeFileDownloader()
    return _default_downloader


def safe_request(
    url: str,
    method: str = 'GET',
    timeout: Optional[float] = None,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Any] = None,
    json: Optional[Any] = None,
    **kwargs
) -> NetworkResponse:
    """
    Convenience function to make a safe HTTP request
    
    This is a module-level convenience function that uses a shared
    SafeHTTPClient instance. For more control, create your own
    SafeHTTPClient instance.
    
    Args:
        url: The URL to request
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        timeout: Request timeout in seconds
        headers: Optional HTTP headers
        params: Optional URL parameters
        data: Optional request body data
        json: Optional JSON data to send
        **kwargs: Additional arguments passed to requests
    
    Returns:
        NetworkResponse with success status, data, or error information
    
    Example:
        >>> response = safe_request('https://api.example.com/data')
        >>> if response.success:
        ...     print(response.data)
    """
    client = _get_default_client()
    return client.safe_request(
        url=url,
        method=method,
        timeout=timeout,
        headers=headers,
        params=params,
        data=data,
        json=json,
        **kwargs
    )


def safe_download(
    url: str,
    local_path: str,
    overwrite: bool = False,
    progress_callback: Optional[Callable[[DownloadProgress], None]] = None,
    timeout: Optional[float] = None
) -> DownloadResponse:
    """
    Convenience function to download a file safely
    
    This is a module-level convenience function that uses a shared
    SafeFileDownloader instance. For more control, create your own
    SafeFileDownloader instance.
    
    Args:
        url: The URL of the file to download
        local_path: Local path where the file should be saved
        overwrite: Whether to overwrite existing files
        progress_callback: Optional callback for progress updates
        timeout: Request timeout in seconds
    
    Returns:
        DownloadResponse with success status, file path, or error information
    
    Example:
        >>> response = safe_download(
        ...     'https://example.com/file.zip',
        ...     'downloads/file.zip'
        ... )
        >>> if response.success:
        ...     print(f"Downloaded to {response.file_path}")
    """
    downloader = _get_default_downloader()
    return downloader.safe_download(
        url=url,
        local_path=local_path,
        overwrite=overwrite,
        progress_callback=progress_callback,
        timeout=timeout
    )


__all__ = [
    "SafeHTTPClient",
    "NetworkResponse",
    "NetworkRequest",
    "SafeFileDownloader",
    "DownloadResponse",
    "DownloadProgress",
    "safe_request",
    "safe_download",
]
