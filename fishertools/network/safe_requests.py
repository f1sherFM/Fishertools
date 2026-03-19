"""
Safe HTTP request operations with comprehensive error handling

This module provides a SafeHTTPClient that wraps the requests library
with proper timeout handling, error conversion, and structured responses.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional
import requests
from requests.exceptions import (
    RequestException,
    Timeout,
    ConnectionError,
    HTTPError,
    TooManyRedirects,
    InvalidURL,
)

from .models import NetworkRequest, NetworkResponse

logger = logging.getLogger(__name__)


class SafeHTTPClient:
    """
    Safe HTTP client with comprehensive error handling and timeouts
    
    This client wraps the requests library to provide:
    - Automatic timeout handling
    - Structured error responses instead of exceptions
    - Consistent response format
    - Input validation
    
    Example:
        >>> client = SafeHTTPClient(default_timeout=5.0)
        >>> response = client.safe_request('https://api.example.com/data')
        >>> if response.success:
        ...     print(response.data)
        ... else:
        ...     print(f"Error: {response.error}")
    """
    
    def __init__(self, default_timeout: float = 10.0):
        """
        Initialize the safe HTTP client
        
        Args:
            default_timeout: Default timeout in seconds for all requests
        """
        if default_timeout <= 0:
            raise ValueError("Timeout must be positive")
        
        self.default_timeout = default_timeout
        self.session = requests.Session()
    
    def safe_request(
        self,
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
        Make a safe HTTP request with proper error handling
        
        This method wraps requests to provide structured error responses
        instead of raising exceptions. All network errors are caught and
        converted to NetworkResponse objects with descriptive error messages.
        
        Args:
            url: The URL to request
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            timeout: Request timeout in seconds (uses default if not specified)
            headers: Optional HTTP headers
            params: Optional URL parameters
            data: Optional request body data
            json: Optional JSON data to send
            **kwargs: Additional arguments passed to requests
        
        Returns:
            NetworkResponse with success status, data, or error information
        
        Example:
            >>> client = SafeHTTPClient()
            >>> response = client.safe_request(
            ...     'https://api.example.com/users',
            ...     method='POST',
            ...     json={'name': 'John'}
            ... )
        """
        # Validate inputs
        validation_error = self._validate_request_params(url, method, timeout)
        if validation_error:
            return validation_error
        
        # Use default timeout if not specified
        request_timeout = timeout if timeout is not None else self.default_timeout
        
        # Prepare request parameters
        request_kwargs = {
            'timeout': request_timeout,
            'headers': headers or {},
            'params': params or {},
        }
        
        # Add data or json payload
        if data is not None:
            request_kwargs['data'] = data
        if json is not None:
            request_kwargs['json'] = json
        
        # Merge additional kwargs
        request_kwargs.update(kwargs)
        
        try:
            # Make the request
            response = self.session.request(method.upper(), url, **request_kwargs)
            
            # Check for HTTP errors (4xx, 5xx)
            response.raise_for_status()
            
            # Try to parse JSON response, fall back to text
            try:
                response_data = response.json()
            except ValueError:
                response_data = response.text
            
            return NetworkResponse(
                success=True,
                data=response_data,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        
        except RequestException as e:
            return self._handle_request_errors(e)
        except Exception as e:
            logger.exception(
                "Unexpected safe_request failure: method=%s url=%s",
                method,
                url,
            )
            return self._handle_request_errors(e)
    
    def _validate_request_params(
        self,
        url: str,
        method: str,
        timeout: Optional[float]
    ) -> Optional[NetworkResponse]:
        """
        Validate request parameters
        
        Args:
            url: The URL to validate
            method: HTTP method to validate
            timeout: Timeout value to validate
        
        Returns:
            NetworkResponse with error if validation fails, None otherwise
        """
        # Validate URL
        if not url or not isinstance(url, str):
            return NetworkResponse(
                success=False,
                error="Invalid URL: URL must be a non-empty string"
            )
        
        if not url.startswith(('http://', 'https://')):
            return NetworkResponse(
                success=False,
                error=f"Invalid URL: URL must start with http:// or https://, got: {url}"
            )
        
        # Validate method
        if not isinstance(method, str):
            return NetworkResponse(
                success=False,
                error=f"Invalid HTTP method: {method}. Method must be a string"
            )

        valid_methods = {'GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'}
        if method.upper() not in valid_methods:
            return NetworkResponse(
                success=False,
                error=f"Invalid HTTP method: {method}. Must be one of {valid_methods}"
            )
        
        # Validate timeout
        if timeout is not None and timeout <= 0:
            return NetworkResponse(
                success=False,
                error=f"Invalid timeout: {timeout}. Timeout must be positive"
            )
        
        return None
    
    def _handle_request_errors(self, exception: Exception) -> NetworkResponse:
        """
        Convert request exceptions to structured responses
        
        This method handles all types of request exceptions and converts
        them into user-friendly NetworkResponse objects with descriptive
        error messages.
        
        Args:
            exception: The exception that occurred during the request
        
        Returns:
            NetworkResponse with error information
        """
        # Timeout errors
        if isinstance(exception, Timeout):
            return NetworkResponse(
                success=False,
                error=f"Request timed out: The server did not respond within the timeout period"
            )
        
        # Connection errors (DNS, refused connection, etc.)
        if isinstance(exception, ConnectionError):
            return NetworkResponse(
                success=False,
                error=f"Connection failed: Unable to connect to the server. Check your internet connection and the URL"
            )
        
        # Invalid URL errors
        if isinstance(exception, InvalidURL):
            return NetworkResponse(
                success=False,
                error=f"Invalid URL: The URL format is incorrect"
            )
        
        # Too many redirects
        if isinstance(exception, TooManyRedirects):
            return NetworkResponse(
                success=False,
                error=f"Too many redirects: The request exceeded the maximum number of redirects"
            )
        
        # HTTP errors (4xx, 5xx status codes)
        if isinstance(exception, HTTPError):
            response = exception.response
            status_code = response.status_code if response else None
            
            # Provide specific messages for common status codes
            error_messages = {
                400: "Bad Request: The server could not understand the request",
                401: "Unauthorized: Authentication is required",
                403: "Forbidden: You don't have permission to access this resource",
                404: "Not Found: The requested resource does not exist",
                500: "Internal Server Error: The server encountered an error",
                502: "Bad Gateway: The server received an invalid response",
                503: "Service Unavailable: The server is temporarily unavailable",
            }
            
            error_msg = error_messages.get(
                status_code,
                f"HTTP Error {status_code}: Request failed"
            )
            
            return NetworkResponse(
                success=False,
                error=error_msg,
                status_code=status_code
            )
        
        # Generic request exception
        if isinstance(exception, RequestException):
            return NetworkResponse(
                success=False,
                error=f"Request failed: {str(exception)}"
            )
        
        # Unexpected errors
        return NetworkResponse(
            success=False,
            error=f"Unexpected error: {type(exception).__name__}: {str(exception)}"
        )
    
    def get(self, url: str, **kwargs) -> NetworkResponse:
        """Convenience method for GET requests"""
        return self.safe_request(url, method='GET', **kwargs)
    
    def post(self, url: str, **kwargs) -> NetworkResponse:
        """Convenience method for POST requests"""
        return self.safe_request(url, method='POST', **kwargs)
    
    def put(self, url: str, **kwargs) -> NetworkResponse:
        """Convenience method for PUT requests"""
        return self.safe_request(url, method='PUT', **kwargs)
    
    def delete(self, url: str, **kwargs) -> NetworkResponse:
        """Convenience method for DELETE requests"""
        return self.safe_request(url, method='DELETE', **kwargs)
    
    def close(self) -> None:
        """Close the session and release resources"""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close session"""
        self.close()
