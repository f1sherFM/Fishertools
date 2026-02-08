"""
Data models for network operations.

This module defines the core data structures used throughout the network module
for representing requests, responses, and progress information.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class NetworkRequest:
    """
    Represents an HTTP request with all necessary parameters.
    
    Attributes:
        url: The target URL for the request
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        timeout: Request timeout in seconds
        headers: HTTP headers to include in the request
        params: URL query parameters
        data: Request body data
    """
    url: str
    method: str = 'GET'
    timeout: float = 10.0
    headers: Dict[str, str] = field(default_factory=dict)
    params: Dict[str, Any] = field(default_factory=dict)
    data: Optional[Any] = None


@dataclass
class NetworkResponse:
    """
    Structured response for network operations.
    
    This class provides a consistent interface for both successful and failed
    network operations, eliminating the need for exception handling in user code.
    
    Attributes:
        success: Whether the operation succeeded
        data: Response data (if successful)
        error: Error message (if failed)
        status_code: HTTP status code (if applicable)
    """
    success: bool
    data: Any = None
    error: Optional[str] = None
    status_code: Optional[int] = None
    
    def __bool__(self) -> bool:
        """Allow using response in boolean context."""
        return self.success
    
    def json(self) -> Any:
        """
        Get JSON data (requests library compatibility).
        
        Returns:
            Parsed JSON data (same as .data attribute)
        
        Raises:
            ValueError: If request failed or data is not available
        
        Example:
            >>> response = safe_request("https://api.github.com/users/octocat")
            >>> user_data = response.json()  # Compatible with requests
            >>> assert user_data == response.data  # Same result
        """
        if not self.success:
            raise ValueError(f"Cannot parse JSON from failed request: {self.error}")
        return self.data
    
    @property
    def content(self) -> bytes:
        """
        Get raw content as bytes (requests library compatibility).
        
        Returns:
            Response data encoded as UTF-8 bytes
        
        Example:
            >>> response = safe_request("https://example.com/data")
            >>> raw_bytes = response.content
            >>> text = raw_bytes.decode('utf-8')
        """
        if self.data is None:
            return b''
        if isinstance(self.data, bytes):
            return self.data
        if isinstance(self.data, str):
            return self.data.encode('utf-8')
        # For JSON data, serialize it
        import json
        return json.dumps(self.data).encode('utf-8')
    
    @property
    def text(self) -> str:
        """
        Get text content as string (requests library compatibility).
        
        Returns:
            Response data as string
        
        Example:
            >>> response = safe_request("https://example.com/page")
            >>> html = response.text
        """
        if self.data is None:
            return ''
        if isinstance(self.data, str):
            return self.data
        if isinstance(self.data, bytes):
            try:
                return self.data.decode('utf-8')
            except UnicodeDecodeError:
                # Fall back to latin-1 for non-UTF-8 bytes (like requests does)
                return self.data.decode('latin-1')
        # For JSON data, serialize it
        import json
        return json.dumps(self.data)


@dataclass
class DownloadProgress:
    """
    Represents the current state of a download operation.
    
    Attributes:
        bytes_downloaded: Number of bytes downloaded so far
        total_bytes: Total file size in bytes (if known)
        percentage: Download completion percentage (if total size is known)
        speed_bps: Current download speed in bytes per second
    """
    bytes_downloaded: int
    total_bytes: Optional[int] = None
    percentage: Optional[float] = None
    speed_bps: Optional[float] = None
    
    def __str__(self) -> str:
        """Human-readable progress representation."""
        if self.percentage is not None:
            return f"{self.percentage:.1f}% ({self.bytes_downloaded} bytes)"
        return f"{self.bytes_downloaded} bytes downloaded"


@dataclass
class DownloadResponse:
    """
    Structured response for file download operations.
    
    Attributes:
        success: Whether the download succeeded
        file_path: Path to the downloaded file (if successful)
        error: Error message (if failed)
        bytes_downloaded: Total bytes downloaded
    """
    success: bool
    file_path: Optional[str] = None
    error: Optional[str] = None
    bytes_downloaded: int = 0
    
    def __bool__(self) -> bool:
        """Allow using response in boolean context."""
        return self.success
