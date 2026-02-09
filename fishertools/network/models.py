"""
Data models for network operations.

This module defines the core data structures used throughout the network module
for representing requests, responses, and progress information.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


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
    method: str = "GET"
    timeout: float = 10.0
    headers: dict[str, str] = field(default_factory=dict)
    params: dict[str, Any] = field(default_factory=dict)
    data: Any | None = None


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
    error: str | None = None
    status_code: int | None = None

    def __bool__(self) -> bool:
        """Allow using response in boolean context."""
        return self.success

    def json(self) -> Any:
        """
        Get JSON data (requests library compatibility).

        This method provides compatibility with the requests library's .json() method,
        making it easy to migrate code from requests to fishertools without changes.

        Returns:
            Parsed JSON data (same as .data attribute)

        Raises:
            ValueError: If request failed or data is not available

        Examples:
            Basic usage - compatible with requests library:

            >>> from fishertools.network import SafeHTTPClient
            >>> client = SafeHTTPClient()
            >>> response = client.safe_request("https://api.github.com/users/octocat")
            >>> if response.success:
            ...     user_data = response.json()  # Works like requests.Response.json()
            ...     print(f"User: {user_data['login']}")
            ...     print(f"Name: {user_data['name']}")

            Accessing API data:

            >>> response = client.safe_request("https://jsonplaceholder.typicode.com/posts/1")
            >>> if response:  # NetworkResponse supports boolean context
            ...     post = response.json()
            ...     print(f"Title: {post['title']}")
            ...     print(f"Body: {post['body']}")

            Handling failed requests:

            >>> response = client.safe_request("https://invalid-url-example.com/api")
            >>> try:
            ...     data = response.json()  # Raises ValueError if request failed
            ... except ValueError as e:
            ...     print(f"Cannot get JSON: {e}")

            Equivalence with .data attribute:

            >>> response = client.safe_request("https://api.github.com/users/octocat")
            >>> assert response.json() == response.data  # Both return the same data
        """
        if not self.success:
            raise ValueError(f"Cannot parse JSON from failed request: {self.error}")
        return self.data

    @property
    def content(self) -> bytes:
        """
        Get raw content as bytes (requests library compatibility).

        This property provides compatibility with the requests library's .content property,
        returning the response data as raw bytes. Useful for binary data or when you need
        precise control over encoding.

        Returns:
            Response data encoded as UTF-8 bytes

        Examples:
            Getting binary content:

            >>> from fishertools.network import SafeHTTPClient
            >>> client = SafeHTTPClient()
            >>> response = client.safe_request("https://example.com/image.png")
            >>> if response.success:
            ...     raw_bytes = response.content
            ...     with open('image.png', 'wb') as f:
            ...         f.write(raw_bytes)

            Decoding text with specific encoding:

            >>> response = client.safe_request("https://example.com/data.txt")
            >>> raw_bytes = response.content
            >>> text = raw_bytes.decode('utf-8')  # Explicit encoding control
            >>> print(text)

            Working with JSON as bytes:

            >>> response = client.safe_request("https://api.github.com/users/octocat")
            >>> json_bytes = response.content
            >>> import json
            >>> data = json.loads(json_bytes.decode('utf-8'))

            Handling different data types:

            >>> # String data is encoded to UTF-8 bytes
            >>> # Bytes data is returned as-is
            >>> # JSON data is serialized then encoded to bytes
        """
        if self.data is None:
            return b""
        if isinstance(self.data, bytes):
            return self.data
        if isinstance(self.data, str):
            return self.data.encode("utf-8")
        # For JSON data, serialize it
        import json

        return json.dumps(self.data).encode("utf-8")

    @property
    def text(self) -> str:
        """
        Get text content as string (requests library compatibility).

        This property provides compatibility with the requests library's .text property,
        returning the response data as a string. Automatically handles different data
        types and encoding.

        Returns:
            Response data as string

        Examples:
            Getting HTML content:

            >>> from fishertools.network import SafeHTTPClient
            >>> client = SafeHTTPClient()
            >>> response = client.safe_request("https://example.com")
            >>> if response.success:
            ...     html = response.text
            ...     print(html[:100])  # Print first 100 characters

            Getting plain text:

            >>> response = client.safe_request("https://example.com/readme.txt")
            >>> text_content = response.text
            >>> lines = text_content.split('\n')
            >>> for line in lines[:5]:
            ...     print(line)

            JSON data as formatted string:

            >>> response = client.safe_request("https://api.github.com/users/octocat")
            >>> json_string = response.text
            >>> print(json_string)  # Pretty-printed JSON

            Handling different encodings:

            >>> # UTF-8 bytes are decoded automatically
            >>> # Non-UTF-8 bytes fall back to latin-1 (like requests)
            >>> # JSON data is serialized to string
        """
        if self.data is None:
            return ""
        if isinstance(self.data, str):
            return self.data
        if isinstance(self.data, bytes):
            try:
                return self.data.decode("utf-8")
            except UnicodeDecodeError:
                # Fall back to latin-1 for non-UTF-8 bytes (like requests does)
                return self.data.decode("latin-1")
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
    total_bytes: int | None = None
    percentage: float | None = None
    speed_bps: float | None = None

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
    file_path: str | None = None
    error: str | None = None
    bytes_downloaded: int = 0

    def __bool__(self) -> bool:
        """Allow using response in boolean context."""
        return self.success
