"""
Async versions of safe utilities for asynchronous applications.

This module provides async/await versions of common safe utilities
that don't block the event loop.

Example:
    import asyncio
    from fishertools.async_safe import async_safe_read_file
    
    async def main():
        content = await async_safe_read_file("data.txt")
        print(content)
    
    asyncio.run(main())
"""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path
from typing import Optional, List, Any

logger = logging.getLogger(__name__)


async def async_safe_read_file(
    file_path: str, 
    default: Optional[str] = None, 
    encoding: str = 'utf-8'
) -> Optional[str]:
    """
    Async safely read a file without raising exceptions.
    
    Parameters:
        file_path (str): Path to the file to read.
        default (str, optional): Value to return if file cannot be read.
        encoding (str): File encoding (default: 'utf-8').
    
    Returns:
        str: File contents, or default value if file cannot be read.
    
    Example:
        content = await async_safe_read_file("config.txt", default="")
        if content:
            print(f"Config: {content}")
    """
    try:
        return await asyncio.to_thread(_read_file_sync, file_path, encoding)
    except Exception:
        logger.exception("async_safe_read_file failed for path=%s", file_path)
        return default


async def async_safe_write_file(
    file_path: str, 
    content: str, 
    encoding: str = 'utf-8'
) -> bool:
    """
    Async safely write to a file without raising exceptions.
    
    Parameters:
        file_path (str): Path to the file to write.
        content (str): Content to write to the file.
        encoding (str): File encoding (default: 'utf-8').
    
    Returns:
        bool: True if write succeeded, False otherwise.
    
    Example:
        success = await async_safe_write_file("output.txt", "Hello, World!")
        if success:
            print("File written successfully")
    """
    try:
        await asyncio.to_thread(_write_file_sync, file_path, content, encoding)
        return True
    except Exception:
        logger.exception("async_safe_write_file failed for path=%s", file_path)
        return False


async def async_safe_file_exists(file_path: str) -> bool:
    """
    Async safely check if a file exists.
    
    Parameters:
        file_path (str): Path to check.
    
    Returns:
        bool: True if file exists, False otherwise.
    
    Example:
        if await async_safe_file_exists("data.txt"):
            content = await async_safe_read_file("data.txt")
    """
    try:
        return await asyncio.to_thread(os.path.exists, file_path)
    except Exception:
        logger.exception("async_safe_file_exists failed for path=%s", file_path)
        return False


async def async_safe_get_file_size(file_path: str, default: int = 0) -> int:
    """
    Async safely get file size in bytes.
    
    Parameters:
        file_path (str): Path to the file.
        default (int): Value to return if size cannot be determined.
    
    Returns:
        int: File size in bytes, or default value.
    
    Example:
        size = await async_safe_get_file_size("data.txt")
        print(f"File size: {size} bytes")
    """
    try:
        return await asyncio.to_thread(os.path.getsize, file_path)
    except Exception:
        logger.exception("async_safe_get_file_size failed for path=%s", file_path)
        return default


async def async_safe_list_files(
    directory: str, 
    pattern: Optional[str] = None
) -> List[str]:
    """
    Async safely list files in a directory.
    
    Parameters:
        directory (str): Directory path to list.
        pattern (str, optional): Glob pattern to filter files (e.g., "*.txt").
    
    Returns:
        list: List of file paths, or empty list if directory cannot be read.
    
    Example:
        files = await async_safe_list_files("data", pattern="*.json")
        for file in files:
            print(file)
    """
    try:
        return await asyncio.to_thread(_list_files_sync, directory, pattern)
    except Exception:
        logger.exception(
            "async_safe_list_files failed for directory=%s pattern=%s",
            directory,
            pattern,
        )
        return []


# Synchronous helper functions (called in thread pool)

def _read_file_sync(file_path: str, encoding: str) -> str:
    """Synchronous file read helper."""
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()


def _write_file_sync(file_path: str, content: str, encoding: str) -> None:
    """Synchronous file write helper."""
    parent_dir = os.path.dirname(file_path)
    if parent_dir:
        Path(parent_dir).mkdir(parents=True, exist_ok=True)
    
    with open(file_path, 'w', encoding=encoding) as f:
        f.write(content)


def _list_files_sync(directory: str, pattern: Optional[str]) -> List[str]:
    """Synchronous file listing helper."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        return []
    
    if pattern:
        return [str(f) for f in path.glob(pattern) if f.is_file()]
    else:
        return [str(f) for f in path.iterdir() if f.is_file()]


__all__ = [
    "async_safe_read_file",
    "async_safe_write_file", 
    "async_safe_file_exists",
    "async_safe_get_file_size",
    "async_safe_list_files",
]
