"""
Safe file download operations with progress tracking

This module provides a SafeFileDownloader that handles file downloads
with progress callbacks, conflict resolution, and automatic cleanup on failure.
"""

from __future__ import annotations

import os
import shutil
import time
from typing import Any, Callable

from .models import DownloadProgress, DownloadResponse
from .safe_requests import SafeHTTPClient


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
        timeout: float | None = None,
        progress_callback: Callable[[DownloadProgress], None] | None = None,
    ) -> DownloadResponse:
        """
        Download a file safely with progress tracking and timeout control.

        This method downloads a file from a URL to a local path with comprehensive
        error handling, progress tracking, and timeout control. It automatically
        handles file conflicts, validates disk space, and cleans up on failure.

        Args:
            url: URL of the file to download
            local_path: Local path where the file should be saved
            overwrite: Whether to overwrite existing files (default: False)
            timeout: Request timeout in seconds (uses client default if None)
            progress_callback: Optional callback for progress updates

        Returns:
            DownloadResponse with success status and file path or error

        Examples:
            Basic file download:

            >>> from fishertools.network import SafeFileDownloader
            >>> downloader = SafeFileDownloader()
            >>> response = downloader.safe_download(
            ...     'https://example.com/data.json',
            ...     'downloads/data.json'
            ... )
            >>> if response.success:
            ...     print(f"Downloaded to: {response.file_path}")
            ...     print(f"Size: {response.bytes_downloaded} bytes")
            ... else:
            ...     print(f"Download failed: {response.error}")

            Download with timeout control:

            >>> # Set a 60-second timeout for large files
            >>> response = downloader.safe_download(
            ...     'https://example.com/large-file.zip',
            ...     'downloads/file.zip',
            ...     timeout=60.0  # 60 second timeout
            ... )
            >>> if not response.success:
            ...     print(f"Download timed out or failed: {response.error}")

            Download with progress tracking:

            >>> def show_progress(progress):
            ...     if progress.percentage:
            ...         print(f"Progress: {progress.percentage:.1f}%")
            ...         if progress.speed_bps:
            ...             speed_mb = progress.speed_bps / (1024 * 1024)
            ...             print(f"Speed: {speed_mb:.2f} MB/s")
            ...     else:
            ...         print(f"Downloaded: {progress.bytes_downloaded} bytes")
            >>>
            >>> response = downloader.safe_download(
            ...     'https://example.com/video.mp4',
            ...     'downloads/video.mp4',
            ...     progress_callback=show_progress,
            ...     timeout=300.0  # 5 minute timeout for large file
            ... )

            Overwriting existing files:

            >>> # First download
            >>> response1 = downloader.safe_download(
            ...     'https://example.com/data.json',
            ...     'data.json'
            ... )
            >>>
            >>> # Second download without overwrite fails
            >>> response2 = downloader.safe_download(
            ...     'https://example.com/data.json',
            ...     'data.json'
            ... )
            >>> print(response2.error)  # "File already exists..."
            >>>
            >>> # Third download with overwrite succeeds
            >>> response3 = downloader.safe_download(
            ...     'https://example.com/data.json',
            ...     'data.json',
            ...     overwrite=True
            ... )
            >>> print(response3.success)  # True

            Using context manager for automatic cleanup:

            >>> with SafeFileDownloader() as downloader:
            ...     response = downloader.safe_download(
            ...         'https://example.com/file.pdf',
            ...         'downloads/file.pdf',
            ...         timeout=30.0
            ...     )
            ...     if response.success:
            ...         print(f"Downloaded: {response.file_path}")
            # Downloader automatically closed after context

            Handling download errors:

            >>> response = downloader.safe_download(
            ...     'https://slow-server.com/huge-file.iso',
            ...     'downloads/file.iso',
            ...     timeout=10.0  # Short timeout
            ... )
            >>> if not response.success:
            ...     if 'timeout' in response.error.lower():
            ...         print("Server too slow, try again later")
            ...     elif 'connection' in response.error.lower():
            ...         print("Cannot connect to server")
            ...     else:
            ...         print(f"Download failed: {response.error}")
        """
        # Validate inputs
        validation_error = self._validate_download_params(url, local_path, timeout)
        if validation_error is not None:
            return validation_error

        # Check for file conflicts
        if os.path.exists(local_path) and not overwrite:
            return DownloadResponse(
                success=False,
                error=f"File already exists: {local_path}. Use overwrite=True to replace it",
            )

        # Ensure target directory exists
        target_dir = os.path.dirname(local_path)
        if target_dir:
            try:
                os.makedirs(target_dir, exist_ok=True)
            except OSError as e:
                return DownloadResponse(
                    success=False, error=f"Failed to create directory: {str(e)}"
                )

        # Make HEAD request to get file size
        request_timeout = (
            timeout if timeout is not None else self.http_client.default_timeout
        )
        head_response = self.http_client.safe_request(
            url, method="HEAD", timeout=request_timeout
        )
        total_bytes = None
        if head_response.success and head_response.headers:
            content_length = head_response.headers.get("content-length")
            if content_length:
                try:
                    total_bytes = int(content_length)
                    # Check disk space
                    if not self._check_disk_space(total_bytes, local_path):
                        return DownloadResponse(
                            success=False,
                            error=f"Insufficient disk space: Need {total_bytes} bytes",
                        )
                except ValueError:
                    pass  # Continue without size information

        # Download the file
        temp_path = f"{local_path}.download"
        bytes_downloaded = 0
        start_time = time.time()

        response = None
        try:
            # Stream the download
            response = self.http_client.session.get(
                url, stream=True, timeout=request_timeout
            )
            response.raise_for_status()

            with open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=self.chunk_size):
                    if chunk:  # Filter out keep-alive chunks
                        f.write(chunk)
                        bytes_downloaded += len(chunk)

                        # Call progress callback if provided
                        if progress_callback:
                            elapsed_time = time.time() - start_time
                            speed = (
                                bytes_downloaded / elapsed_time
                                if elapsed_time > 0
                                else None
                            )
                            percentage = (
                                (bytes_downloaded / total_bytes * 100)
                                if total_bytes
                                else None
                            )

                            progress = DownloadProgress(
                                bytes_downloaded=bytes_downloaded,
                                total_bytes=total_bytes,
                                percentage=percentage,
                                speed_bps=speed,
                            )
                            progress_callback(progress)

            # Move temp file to final location
            if os.path.exists(local_path):
                os.remove(local_path)
            shutil.move(temp_path, local_path)

            return DownloadResponse(
                success=True, file_path=local_path, bytes_downloaded=bytes_downloaded
            )

        except Exception as e:
            # Clean up partial download
            self._cleanup_partial_file(temp_path)

            # Convert exception to error response
            error_msg = self._format_download_error(e)
            return DownloadResponse(
                success=False, error=error_msg, bytes_downloaded=bytes_downloaded
            )
        finally:
            if response is not None:
                try:
                    response.close()
                except Exception:
                    pass

    def _validate_download_params(
        self, url: str, local_path: str, timeout: float | None = None
    ) -> DownloadResponse | None:
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
                success=False, error="Invalid URL: URL must be a non-empty string"
            )

        if not url.startswith(("http://", "https://")):
            return DownloadResponse(
                success=False,
                error="Invalid URL: URL must start with http:// or https://",
            )

        # Validate local path
        if not local_path or not isinstance(local_path, str):
            return DownloadResponse(
                success=False,
                error="Invalid path: Local path must be a non-empty string",
            )

        # Check if path is a directory
        if os.path.isdir(local_path):
            return DownloadResponse(
                success=False,
                error=f"Invalid path: {local_path} is a directory, not a file path",
            )

        # Validate timeout
        if timeout is not None and timeout <= 0:
            return DownloadResponse(
                success=False,
                error=f"Invalid timeout: {timeout}. Timeout must be positive",
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
            target_dir = os.path.dirname(target_path) or "."

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
        if "timeout" in error_msg.lower():
            return "Download timed out: The server did not respond in time"

        if "connection" in error_msg.lower():
            return "Connection failed: Unable to connect to the server"

        if "permission" in error_msg.lower():
            return f"Permission denied: Cannot write to {error_msg}"

        if "disk" in error_msg.lower() or "space" in error_msg.lower():
            return "Insufficient disk space: Not enough space to save the file"

        return f"Download failed: {error_type}: {error_msg}"

    def close(self) -> None:
        """Close the HTTP client and release resources"""
        self.http_client.close()

    def __enter__(self) -> SafeFileDownloader:
        """Context manager entry"""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit - close client"""
        self.close()
