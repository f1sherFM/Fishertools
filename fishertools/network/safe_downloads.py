"""
Safe file download operations with progress tracking

This module provides a SafeFileDownloader that handles file downloads
with progress callbacks, conflict resolution, and automatic cleanup on failure.
"""

from __future__ import annotations

import os
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

from .safe_requests import SafeHTTPClient, NetworkResponse


@dataclass
class DownloadProgress:
    """Progress information for file downloads"""
    bytes_downloaded: int
    total_bytes: Optional[int]
    percentage: Optional[float]
    speed_bps: Optional[float]  # bytes per second
    
    def __str__(self) -> str:
        """Human-readable progress string"""
        if self.percentage is not None:
            return f"{self.percentage:.1f}% ({self.bytes_downloaded}/{self.total_bytes} bytes)"
        return f"{self.bytes_downloaded} bytes downloaded"


@dataclass
class DownloadResponse:
    """Structured response for download operations"""
    success: bool
    file_path: Optional[str] = None
    error: Optional[str] = None
    bytes_downloaded: int = 0
    
    def __bool__(self) -> bool:
        """Allow using response in boolean context"""
        return self.success


class SafeFileDownloader:
    """
    Safe file downloader with progress tracking and error handling
    
    This downloader provides:
    - Progress callbacks for monitoring downloads
    - Automatic cleanup on failure
    - File conflict handling
    - Disk space checking
    - Comprehensive error handling
    
    Example:
        >>> downloader = SafeFileDownloader()
        >>> def progress_callback(progress):
        ...     print(f"Downloaded: {progress.percentage:.1f}%")
        >>> response = downloader.safe_download(
        ...     'https://example.com/file.zip',
        ...     'downloads/file.zip',
        ...     progress_callback=progress_callback
        ... )
        >>> if response.success:
        ...     print(f"Downloaded to: {response.file_path}")
    """
    
    def __init__(self, chunk_size: int = 8192):
        """
        Initialize the file downloader
        
        Args:
            chunk_size: Size of chunks to download at a time (in bytes)
        """
        if chunk_size <= 0:
            raise ValueError("Chunk size must be positive")
        
        self.chunk_size = chunk_size
        self.http_client = SafeHTTPClient()
    
    def safe_download(
        self,
        url: str,
        local_path: str,
        overwrite: bool = False,
        timeout: Optional[float] = None,
        progress_callback: Optional[Callable[[DownloadProgress], None]] = None
    ) -> DownloadResponse:
        """
        Download a file safely with progress tracking
        
        This method downloads a file from a URL to a local path with:
        - Progress tracking via callback
        - Automatic cleanup on failure
        - File conflict handling
        - Disk space validation
        - Timeout control
        
        Args:
            url: URL of the file to download
            local_path: Local path where the file should be saved
            overwrite: Whether to overwrite existing files
            timeout: Request timeout in seconds (uses client default if None)
            progress_callback: Optional callback for progress updates
        
        Returns:
            DownloadResponse with success status and file path or error
        
        Example:
            >>> downloader = SafeFileDownloader()
            >>> response = downloader.safe_download(
            ...     'https://example.com/data.json',
            ...     'data/data.json',
            ...     overwrite=True
            ... )
            >>> # With timeout
            >>> response = downloader.safe_download(
            ...     'https://example.com/large-file.zip',
            ...     'downloads/file.zip',
            ...     timeout=60.0  # 60 second timeout
            ... )
        """
        # Validate inputs
        validation_error = self._validate_download_params(url, local_path, timeout)
        if validation_error is not None:
            return validation_error
        
        # Check for file conflicts
        if os.path.exists(local_path) and not overwrite:
            return DownloadResponse(
                success=False,
                error=f"File already exists: {local_path}. Use overwrite=True to replace it"
            )
        
        # Ensure target directory exists
        target_dir = os.path.dirname(local_path)
        if target_dir:
            try:
                os.makedirs(target_dir, exist_ok=True)
            except OSError as e:
                return DownloadResponse(
                    success=False,
                    error=f"Failed to create directory: {str(e)}"
                )
        
        # Make HEAD request to get file size
        request_timeout = timeout if timeout is not None else self.http_client.default_timeout
        head_response = self.http_client.safe_request(url, method='HEAD', timeout=request_timeout)
        total_bytes = None
        if head_response.success and head_response.headers:
            content_length = head_response.headers.get('content-length')
            if content_length:
                try:
                    total_bytes = int(content_length)
                    # Check disk space
                    if not self._check_disk_space(total_bytes, local_path):
                        return DownloadResponse(
                            success=False,
                            error=f"Insufficient disk space: Need {total_bytes} bytes"
                        )
                except ValueError:
                    pass  # Continue without size information
        
        # Download the file
        temp_path = f"{local_path}.download"
        bytes_downloaded = 0
        start_time = time.time()
        
        try:
            # Stream the download
            response = self.http_client.session.get(
                url,
                stream=True,
                timeout=request_timeout
            )
            response.raise_for_status()
            
            with open(temp_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:  # Filter out keep-alive chunks
                        f.write(chunk)
                        bytes_downloaded += len(chunk)
                        
                        # Call progress callback if provided
                        if progress_callback:
                            elapsed_time = time.time() - start_time
                            speed = bytes_downloaded / elapsed_time if elapsed_time > 0 else None
                            percentage = (
                                (bytes_downloaded / total_bytes * 100)
                                if total_bytes else None
                            )
                            
                            progress = DownloadProgress(
                                bytes_downloaded=bytes_downloaded,
                                total_bytes=total_bytes,
                                percentage=percentage,
                                speed_bps=speed
                            )
                            progress_callback(progress)
            
            # Move temp file to final location
            if os.path.exists(local_path):
                os.remove(local_path)
            shutil.move(temp_path, local_path)
            
            return DownloadResponse(
                success=True,
                file_path=local_path,
                bytes_downloaded=bytes_downloaded
            )
        
        except Exception as e:
            # Clean up partial download
            self._cleanup_partial_file(temp_path)
            
            # Convert exception to error response
            error_msg = self._format_download_error(e)
            return DownloadResponse(
                success=False,
                error=error_msg,
                bytes_downloaded=bytes_downloaded
            )
    
    def _validate_download_params(
        self,
        url: str,
        local_path: str,
        timeout: Optional[float] = None
    ) -> Optional[DownloadResponse]:
        """
        Validate download parameters
        
        Args:
            url: URL to validate
            local_path: Local path to validate
            timeout: Timeout value to validate
        
        Returns:
            DownloadResponse with error if validation fails, None otherwise
        """
        # Validate URL
        if not url or not isinstance(url, str):
            return DownloadResponse(
                success=False,
                error="Invalid URL: URL must be a non-empty string"
            )
        
        if not url.startswith(('http://', 'https://')):
            return DownloadResponse(
                success=False,
                error=f"Invalid URL: URL must start with http:// or https://"
            )
        
        # Validate local path
        if not local_path or not isinstance(local_path, str):
            return DownloadResponse(
                success=False,
                error="Invalid path: Local path must be a non-empty string"
            )
        
        # Check if path is a directory
        if os.path.isdir(local_path):
            return DownloadResponse(
                success=False,
                error=f"Invalid path: {local_path} is a directory, not a file path"
            )
        
        # Validate timeout
        if timeout is not None and timeout <= 0:
            return DownloadResponse(
                success=False,
                error=f"Invalid timeout: {timeout}. Timeout must be positive"
            )
        
        return None
    
    def _check_disk_space(self, file_size: int, target_path: str) -> bool:
        """
        Check if sufficient disk space is available
        
        Args:
            file_size: Size of file to download in bytes
            target_path: Path where file will be saved
        
        Returns:
            True if sufficient space is available, False otherwise
        """
        try:
            # Get the directory where file will be saved
            target_dir = os.path.dirname(target_path) or '.'
            
            # Get disk usage statistics
            stat = shutil.disk_usage(target_dir)
            
            # Add 10% buffer for safety
            required_space = file_size * 1.1
            
            return stat.free >= required_space
        except Exception:
            # If we can't check, assume space is available
            return True
    
    def _cleanup_partial_file(self, file_path: str) -> None:
        """
        Remove partially downloaded files on failure
        
        Args:
            file_path: Path to the partial file to remove
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception:
            # Silently ignore cleanup errors
            pass
    
    def _format_download_error(self, exception: Exception) -> str:
        """
        Format download exception into user-friendly error message
        
        Args:
            exception: The exception that occurred
        
        Returns:
            Formatted error message
        """
        error_type = type(exception).__name__
        error_msg = str(exception)
        
        # Provide specific messages for common errors
        if 'timeout' in error_msg.lower():
            return "Download timed out: The server did not respond in time"
        
        if 'connection' in error_msg.lower():
            return "Connection failed: Unable to connect to the server"
        
        if 'permission' in error_msg.lower():
            return f"Permission denied: Cannot write to {error_msg}"
        
        if 'disk' in error_msg.lower() or 'space' in error_msg.lower():
            return "Insufficient disk space: Not enough space to save the file"
        
        return f"Download failed: {error_type}: {error_msg}"
    
    def close(self) -> None:
        """Close the HTTP client and release resources"""
        self.http_client.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close client"""
        self.close()
