"""
SimpleLogger pattern for file-based logging.

This module provides the SimpleLogger class for adding logging to applications
without complex configuration. Messages are written to a file with timestamps
and log levels.

Example:
    logger = SimpleLogger("app.log")
    logger.info("Application started")
    logger.warning("Low memory detected")
    logger.error("Connection failed")
"""

from __future__ import annotations

import os
import threading
from datetime import datetime
from pathlib import Path


class SimpleLogger:
    """
    Simple file-based logging with timestamps and levels.

    This class provides a straightforward way to log messages to a file with
    automatic timestamps and log level indicators. No configuration is required.

    Parameters:
        file_path (str): Path to the log file. Created automatically if it
                        doesn't exist. Parent directories are created as needed.

    Attributes:
        file_path (str): The path to the log file.

    Methods:
        info(message): Log an info-level message.
        warning(message): Log a warning-level message.
        error(message): Log an error-level message.

    Raises:
        IOError: If file operations fail.

    Example:
        logger = SimpleLogger("logs/app.log")
        logger.info("User logged in")
        logger.warning("Deprecated function used")
        logger.error("Database connection failed")

    Note:
        - Log format: [TIMESTAMP] [LEVEL] message
        - Timestamp format: YYYY-MM-DD HH:MM:SS
        - Messages are appended to the file
        - File is created automatically on first write
        - Parent directories are created automatically
    """

    def __init__(self, file_path):
        """
        Initialize SimpleLogger with a file path.

        Parameters:
            file_path (str): Path to the log file.
        """
        self.file_path = self._validate_log_path(file_path)
        self._lock = threading.Lock()  # Thread-safe logging

    def _validate_log_path(self, file_path):
        if not isinstance(file_path, (str, os.PathLike)):
            raise TypeError("file_path must be a string or path-like object")

        normalized = os.fspath(file_path)
        if not normalized or not str(normalized).strip():
            raise ValueError("Log file path cannot be empty")
        if "\x00" in normalized:
            raise ValueError("Log file path contains null byte")

        reserved_names = {
            "CON", "PRN", "AUX", "NUL",
            "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
            "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
        }
        stem_upper = Path(normalized).name.split(".")[0].upper()
        if stem_upper in reserved_names:
            raise ValueError(f"Invalid log file path: {normalized}")

        if os.path.isdir(normalized):
            raise IsADirectoryError(f"Log path points to a directory: {normalized}")

        return normalized

    def info(self, message):
        """
        Log an info-level message.

        Parameters:
            message (str): The message to log.

        Returns:
            None

        Raises:
            IOError: If file write fails.
        """
        self._log("INFO", message)

    def warning(self, message):
        """
        Log a warning-level message.

        Parameters:
            message (str): The message to log.

        Returns:
            None

        Raises:
            IOError: If file write fails.
        """
        self._log("WARNING", message)

    def error(self, message):
        """
        Log an error-level message.

        Parameters:
            message (str): The message to log.

        Returns:
            None

        Raises:
            IOError: If file write fails.
        """
        self._log("ERROR", message)

    def _log(self, level, message):
        """
        Internal method to write a log message (thread-safe).

        Parameters:
            level (str): The log level (INFO, WARNING, ERROR).
            message (str): The message to log.

        Returns:
            None

        Raises:
            IOError: If file write fails.
        """
        with self._lock:  # Thread-safe file writing
            try:
                # Create parent directories if they don't exist
                parent_dir = os.path.dirname(self.file_path)
                if parent_dir:
                    Path(parent_dir).mkdir(parents=True, exist_ok=True)
                
                # Get current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Format log message
                log_entry = f"[{timestamp}] [{level}] {message}\n"
                
                # Append to log file with UTF-8 encoding
                with open(self.file_path, 'a', encoding='utf-8') as f:
                    f.write(log_entry)
            except (ValueError, TypeError, IsADirectoryError):
                raise
            except IOError as e:
                raise IOError(f"Failed to write to {self.file_path}: {e}")
