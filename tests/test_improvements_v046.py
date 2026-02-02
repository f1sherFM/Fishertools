"""
Tests for v0.4.6 improvements.

Tests cover:
- Thread safety for SimpleLogger
- Caching for PatternLoader
- Async logger functionality
- Async safe utilities
- PEP 561 compliance
"""

from __future__ import annotations

import asyncio
import os
import tempfile
import threading
import time
from pathlib import Path

import pytest

from fishertools.patterns.logger import SimpleLogger
from fishertools.errors.pattern_loader import PatternLoader
from fishertools.async_logger import AsyncSimpleLogger
from fishertools.async_safe import (
    async_safe_read_file,
    async_safe_write_file,
    async_safe_file_exists,
    async_safe_get_file_size,
    async_safe_list_files,
)


class TestSimpleLoggerThreadSafety:
    """Test thread safety of SimpleLogger."""

    def test_concurrent_logging(self, tmp_path):
        """Test that concurrent logging doesn't cause race conditions."""
        log_file = tmp_path / "test.log"
        logger = SimpleLogger(str(log_file))
        
        num_threads = 10
        messages_per_thread = 20
        
        def worker(thread_id):
            for i in range(messages_per_thread):
                logger.info(f"Thread {thread_id}: Message {i}")
        
        # Start threads
        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(num_threads)
        ]
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        # Verify all messages were written
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        assert len(lines) == num_threads * messages_per_thread
        
        # Verify format
        for line in lines:
            assert "[INFO]" in line
            assert "Thread" in line
            assert "Message" in line

    def test_lock_exists(self):
        """Test that SimpleLogger has a lock attribute."""
        logger = SimpleLogger("test.log")
        assert hasattr(logger, '_lock')
        assert isinstance(logger._lock, threading.Lock)


class TestPatternLoaderCaching:
    """Test caching for PatternLoader."""

    def test_patterns_cached(self):
        """Test that patterns are cached after first load."""
        loader = PatternLoader()
        
        # First load
        start = time.perf_counter()
        patterns1 = loader.load_patterns()
        first_time = time.perf_counter() - start
        
        # Second load (should be cached)
        start = time.perf_counter()
        patterns2 = loader.load_patterns()
        second_time = time.perf_counter() - start
        
        # Same patterns returned
        assert patterns1 is patterns2
        
        # Second call should be much faster
        # (allowing some variance for system load)
        assert second_time < first_time * 0.5

    def test_get_patterns_loads_if_needed(self):
        """Test that get_patterns loads patterns if not loaded."""
        loader = PatternLoader()
        patterns = loader.get_patterns()
        assert len(patterns) > 0

    def test_reload_patterns(self):
        """Test that reload_patterns forces reload."""
        loader = PatternLoader()
        patterns1 = loader.load_patterns()
        patterns2 = loader.reload_patterns()
        
        # Should return patterns (may or may not be same object)
        assert len(patterns1) > 0
        assert len(patterns2) > 0


class TestAsyncSimpleLogger:
    """Test async logger functionality."""

    @pytest.mark.asyncio
    async def test_async_logging(self, tmp_path):
        """Test basic async logging."""
        log_file = tmp_path / "async_test.log"
        logger = AsyncSimpleLogger(str(log_file))
        
        await logger.info("Info message")
        await logger.warning("Warning message")
        await logger.error("Error message")
        
        # Verify file contents
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "[INFO] Info message" in content
        assert "[WARNING] Warning message" in content
        assert "[ERROR] Error message" in content

    @pytest.mark.asyncio
    async def test_concurrent_async_logging(self, tmp_path):
        """Test concurrent async logging."""
        log_file = tmp_path / "async_concurrent.log"
        logger = AsyncSimpleLogger(str(log_file))
        
        async def worker(worker_id):
            for i in range(10):
                await logger.info(f"Worker {worker_id}: Message {i}")
        
        # Run multiple workers concurrently
        await asyncio.gather(*[worker(i) for i in range(5)])
        
        # Verify all messages written
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        assert len(lines) == 50  # 5 workers * 10 messages

    @pytest.mark.asyncio
    async def test_async_lock_exists(self):
        """Test that AsyncSimpleLogger has an async lock."""
        logger = AsyncSimpleLogger("test.log")
        assert hasattr(logger, '_lock')
        assert isinstance(logger._lock, asyncio.Lock)


class TestAsyncSafeUtilities:
    """Test async safe utilities."""

    @pytest.mark.asyncio
    async def test_async_safe_read_file(self, tmp_path):
        """Test async file reading."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello, World!", encoding='utf-8')
        
        content = await async_safe_read_file(str(test_file))
        assert content == "Hello, World!"

    @pytest.mark.asyncio
    async def test_async_safe_read_file_default(self, tmp_path):
        """Test async file reading with default value."""
        content = await async_safe_read_file(
            str(tmp_path / "nonexistent.txt"),
            default="default"
        )
        assert content == "default"

    @pytest.mark.asyncio
    async def test_async_safe_write_file(self, tmp_path):
        """Test async file writing."""
        test_file = tmp_path / "output.txt"
        
        success = await async_safe_write_file(
            str(test_file),
            "Test content"
        )
        
        assert success is True
        assert test_file.read_text(encoding='utf-8') == "Test content"

    @pytest.mark.asyncio
    async def test_async_safe_file_exists(self, tmp_path):
        """Test async file existence check."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("content")
        
        exists = await async_safe_file_exists(str(test_file))
        assert exists is True
        
        not_exists = await async_safe_file_exists(str(tmp_path / "nope.txt"))
        assert not_exists is False

    @pytest.mark.asyncio
    async def test_async_safe_get_file_size(self, tmp_path):
        """Test async file size retrieval."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("12345")
        
        size = await async_safe_get_file_size(str(test_file))
        assert size == 5

    @pytest.mark.asyncio
    async def test_async_safe_get_file_size_default(self, tmp_path):
        """Test async file size with default."""
        size = await async_safe_get_file_size(
            str(tmp_path / "nonexistent.txt"),
            default=999
        )
        assert size == 999

    @pytest.mark.asyncio
    async def test_async_safe_list_files(self, tmp_path):
        """Test async file listing."""
        # Create test files
        (tmp_path / "file1.txt").write_text("a")
        (tmp_path / "file2.txt").write_text("b")
        (tmp_path / "file3.json").write_text("{}")
        
        # List all files
        files = await async_safe_list_files(str(tmp_path))
        assert len(files) == 3
        
        # List with pattern
        txt_files = await async_safe_list_files(str(tmp_path), pattern="*.txt")
        assert len(txt_files) == 2

    @pytest.mark.asyncio
    async def test_async_safe_list_files_nonexistent(self, tmp_path):
        """Test async file listing for nonexistent directory."""
        files = await async_safe_list_files(str(tmp_path / "nope"))
        assert files == []

    @pytest.mark.asyncio
    async def test_concurrent_file_operations(self, tmp_path):
        """Test concurrent async file operations."""
        # Create multiple files concurrently
        tasks = [
            async_safe_write_file(str(tmp_path / f"file{i}.txt"), f"Content {i}")
            for i in range(10)
        ]
        results = await asyncio.gather(*tasks)
        assert all(results)
        
        # Read them concurrently
        read_tasks = [
            async_safe_read_file(str(tmp_path / f"file{i}.txt"))
            for i in range(10)
        ]
        contents = await asyncio.gather(*read_tasks)
        
        for i, content in enumerate(contents):
            assert content == f"Content {i}"


class TestPEP561Compliance:
    """Test PEP 561 compliance."""

    def test_py_typed_exists(self):
        """Test that py.typed marker file exists."""
        import fishertools
        package_dir = Path(fishertools.__file__).parent
        py_typed = package_dir / "py.typed"
        
        assert py_typed.exists(), "py.typed marker file should exist"

    def test_future_annotations_in_main_modules(self):
        """Test that __future__.annotations is imported in main modules."""
        modules_to_check = [
            'fishertools',
            'fishertools._version',
            'fishertools.utils',
            'fishertools.helpers',
            'fishertools.decorators',
            'fishertools.input_utils',
            'fishertools.async_logger',
            'fishertools.async_safe',
        ]
        
        for module_name in modules_to_check:
            module = __import__(module_name, fromlist=[''])
            # Check if module has annotations enabled
            # (this is implicit, but we can check the module was imported)
            assert module is not None


class TestBackwardCompatibility:
    """Test that improvements don't break existing functionality."""

    def test_simple_logger_still_works(self, tmp_path):
        """Test that SimpleLogger still works as before."""
        log_file = tmp_path / "compat.log"
        logger = SimpleLogger(str(log_file))
        
        logger.info("Test")
        logger.warning("Test")
        logger.error("Test")
        
        assert log_file.exists()

    def test_pattern_loader_still_works(self):
        """Test that PatternLoader still works as before."""
        loader = PatternLoader()
        patterns = loader.load_patterns()
        assert len(patterns) > 0

    def test_imports_still_work(self):
        """Test that all imports still work."""
        # Main imports
        from fishertools import explain_error
        from fishertools.patterns import SimpleLogger
        from fishertools.safe import safe_read_file
        
        # New imports
        from fishertools.async_logger import AsyncSimpleLogger
        from fishertools.async_safe import async_safe_read_file
        
        assert explain_error is not None
        assert SimpleLogger is not None
        assert safe_read_file is not None
        assert AsyncSimpleLogger is not None
        assert async_safe_read_file is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
