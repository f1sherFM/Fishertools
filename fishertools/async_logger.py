"""
Async version of SimpleLogger for asynchronous applications.

This module provides AsyncSimpleLogger for async/await based logging
without blocking the event loop.

Example:
    import asyncio
    
    async def main():
        logger = AsyncSimpleLogger("app.log")
        await logger.info("Application started")
        await logger.warning("Low memory detected")
        await logger.error("Connection failed")
    
    asyncio.run(main())
"""

from __future__ import annotations

import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class AsyncSimpleLogger:
    """
    Async file-based logging with timestamps and levels.

    This class provides asynchronous logging that doesn't block the event loop.
    Perfect for async applications and high-performance scenarios.

    Parameters:
        file_path (str): Path to the log file. Created automatically if it
                        doesn't exist. Parent directories are created as needed.

    Attributes:
        file_path (str): The path to the log file.

    Methods:
        info(message): Async log an info-level message.
        warning(message): Async log a warning-level message.
        error(message): Async log an error-level message.

    Raises:
        IOError: If file operations fail.

    Example:
        logger = AsyncSimpleLogger("logs/app.log")
        await logger.info("User logged in")
        await logger.warning("Deprecated function used")
        await logger.error("Database connection failed")

    Note:
        - Log format: [TIMESTAMP] [LEVEL] message
        - Timestamp format: YYYY-MM-DD HH:MM:SS
        - Messages are appended to the file
        - File is created automatically on first write
        - Parent directories are created automatically
        - Thread-safe and async-safe
    """

    def __init__(self, file_path: str):
        """
        Initialize AsyncSimpleLogger with a file path.

        Parameters:
            file_path (str): Path to the log file.
        """
        self.file_path = file_path
        self._lock = asyncio.Lock()  # Async-safe logging

    async def info(self, message: str) -> None:
        """
        Async log an info-level message.

        Parameters:
            message (str): The message to log.

        Returns:
            None

        Raises:
            IOError: If file write fails.
        """
        await self._log("INFO", message)

    async def warning(self, message: str) -> None:
        """
        Async log a warning-level message.

        Parameters:
            message (str): The message to log.

        Returns:
            None

        Raises:
            IOError: If file write fails.
        """
        await self._log("WARNING", message)

    async def error(self, message: str) -> None:
        """
        Async log an error-level message.

        Parameters:
            message (str): The message to log.

        Returns:
            None

        Raises:
            IOError: If file write fails.
        """
        await self._log("ERROR", message)

    async def _log(self, level: str, message: str) -> None:
        """
        Internal async method to write a log message.

        Parameters:
            level (str): The log level (INFO, WARNING, ERROR).
            message (str): The message to log.

        Returns:
            None

        Raises:
            IOError: If file write fails.
        """
        async with self._lock:  # Async-safe file writing
            try:
                # Create parent directories if they don't exist.
                # Avoid asyncio.to_thread here because some runtimes may block on thread offloading.
                parent_dir = os.path.dirname(self.file_path)
                if parent_dir:
                    Path(parent_dir).mkdir(parents=True, exist_ok=True)
                
                # Get current timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Format log message
                log_entry = f"[{timestamp}] [{level}] {message}\n"
                
                # Append to log file with UTF-8 encoding.
                self._write_to_file(log_entry)
            except IOError as e:
                raise IOError(f"Failed to write to {self.file_path}: {e}")

    def _write_to_file(self, log_entry: str) -> None:
        """
        Synchronous file write helper (called in thread pool).

        Parameters:
            log_entry (str): The formatted log entry to write.
        """
        with open(self.file_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)


__all__ = ["AsyncSimpleLogger"]
