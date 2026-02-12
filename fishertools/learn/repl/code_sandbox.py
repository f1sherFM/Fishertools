"""
Code sandbox for safely executing user code in the REPL.

This module provides a restricted execution environment that prevents access to
dangerous operations like file I/O, imports, and other restricted functions.
"""

import io
import sys
import time
import builtins
from contextlib import redirect_stdout, redirect_stderr
from typing import Tuple, Dict, Any


class CodeSandbox:
    """
    Safely executes Python code with restrictions and timeout support.
    
    The sandbox prevents access to:
    - File I/O operations (open, read, write)
    - Module imports
    - System operations (os, sys, subprocess)
    - Dangerous built-in functions
    
    Example:
        >>> sandbox = CodeSandbox()
        >>> success, output = sandbox.execute("print(2 + 2)")
        >>> print(output)
        4
    """
    
    # Built-in functions that are allowed in the sandbox
    ALLOWED_BUILTINS = {
        "abs", "all", "any", "ascii", "bin", "bool", "bytearray", "bytes",
        "chr", "complex", "dict", "divmod", "enumerate", "filter",
        "float", "format", "frozenset", "hash", "hex", "int",
        "isinstance", "issubclass", "iter", "len", "list", "map",
        "max", "min", "next", "oct", "ord", "pow", "print", "range",
        "repr", "reversed", "round", "set", "slice", "sorted", "str",
        "sum", "tuple", "zip",
    }
    
    # Dangerous built-in functions that should be blocked
    BLOCKED_BUILTINS = {
        "open", "input", "exec", "eval", "compile", "__import__",
        "globals", "locals", "vars", "dir", "getattr", "setattr",
        "delattr", "hasattr", "callable", "classmethod", "staticmethod",
        "property", "super", "type", "object", "memoryview",
    }
    
    # Dangerous modules that cannot be imported
    BLOCKED_MODULES = {
        "os", "sys", "subprocess", "socket", "urllib", "requests",
        "pickle", "shelve", "dbm", "sqlite3", "tempfile", "shutil",
        "glob", "fnmatch", "linecache", "fileinput", "stat", "filecmp",
        "pathlib", "zipfile", "tarfile", "gzip", "bz2", "lzma",
        "zlib", "configparser", "netrc", "xdrlib", "plistlib",
        "hashlib", "hmac", "secrets", "ssl", "asyncio", "threading",
        "multiprocessing", "concurrent", "ctypes", "mmap", "select",
        "selectors", "fcntl", "resource", "nis", "syslog", "grp", "pwd",
        "spwd", "crypt", "termios", "tty", "pty", "fcntl", "pipes",
        "posixfile", "resource", "nis", "syslog", "grp", "pwd",
    }
    
    def __init__(self, timeout: float = 5.0, max_steps: int = 200_000):
        """
        Initialize the code sandbox.
        
        Args:
            timeout: Maximum execution time in seconds (default: 5.0)
            max_steps: Max executed source lines before forced stop
        """
        self.timeout = timeout
        self.max_steps = max_steps
        self.execution_count = 0
    
    def execute(self, code: str, timeout: float = None) -> Tuple[bool, str]:
        """
        Execute code safely in a sandbox.
        
        Args:
            code: Python code to execute
            timeout: Optional timeout override (in seconds)
        
        Returns:
            Tuple of (success, output_or_error) where:
            - success: True if code executed without errors
            - output_or_error: Captured output or error message
        
        Example:
            >>> sandbox = CodeSandbox()
            >>> success, output = sandbox.execute("print('Hello')")
            >>> print(success, output)
            True Hello
        """
        if timeout is None:
            timeout = self.timeout
        
        # Validate code before execution
        validation_error = self._validate_code(code)
        if validation_error:
            return False, validation_error
        
        if not isinstance(timeout, (int, float)) or timeout <= 0:
            return False, "Timeout must be a positive number"

        # Create restricted globals
        restricted_globals = self._create_restricted_globals()
        
        # Capture output
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()

        try:
            compiled_code = compile(code, "<sandbox>", "exec")

            start_time = time.perf_counter()
            executed_steps = 0

            def tracer(frame, event, arg):
                nonlocal executed_steps
                if frame.f_code.co_filename == "<sandbox>" and event == "line":
                    executed_steps += 1
                    if executed_steps > self.max_steps:
                        raise TimeoutError("Code execution exceeded step limit")
                    if time.perf_counter() - start_time > float(timeout):
                        raise TimeoutError("Code execution timed out")
                return tracer

            old_trace = sys.gettrace()
            # Execute code with output redirection
            with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
                sys.settrace(tracer)
                try:
                    exec(compiled_code, restricted_globals, restricted_globals)
                finally:
                    sys.settrace(old_trace)
            
            output = output_buffer.getvalue()
            return True, output
        
        except SyntaxError as e:
            error_msg = f"Syntax Error: {e.msg}"
            if e.lineno:
                error_msg += f" (line {e.lineno})"
            return False, error_msg
        
        except TimeoutError:
            return False, "Code execution timed out. Try simpler code."
        
        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            return False, f"{error_type}: {error_msg}"
    
    def _validate_code(self, code: str) -> str:
        """
        Validate code for dangerous operations.
        
        Args:
            code: Code to validate
        
        Returns:
            Error message if validation fails, empty string if valid
        """
        if not code or not code.strip():
            return "Code cannot be empty"
        
        # Check for dangerous imports
        dangerous_keywords = ["import ", "from ", "__import__"]
        code_lower = code.lower()
        
        for keyword in dangerous_keywords:
            if keyword in code_lower:
                return "Imports are not allowed in the sandbox"
        
        # Check for file operations
        file_keywords = ["open(", "read(", "write(", "file("]
        for keyword in file_keywords:
            if keyword in code_lower:
                return "File operations are not allowed in the sandbox"
        
        # Check for dangerous functions
        dangerous_funcs = ["exec(", "eval(", "compile(", "globals(", "locals("]
        for func in dangerous_funcs:
            if func in code_lower:
                return f"The function '{func[:-1]}' is not allowed in the sandbox"
        
        return ""
    
    def _create_restricted_globals(self) -> Dict[str, Any]:
        """
        Create a restricted globals dictionary for code execution.
        
        Returns:
            Dictionary with safe built-in functions and common modules
        """
        # Start with safe built-ins
        safe_builtins = {
            name: getattr(builtins, name)
            for name in self.ALLOWED_BUILTINS
            if hasattr(builtins, name)
        }
        
        # Add safe modules
        import math
        safe_modules = {
            "math": math,
        }
        
        # Combine into globals
        restricted_globals = {
            "__builtins__": safe_builtins,
            **safe_modules,
        }
        
        return restricted_globals
    
    def get_available_builtins(self) -> list:
        """
        Get list of available built-in functions in the sandbox.
        
        Returns:
            Sorted list of available built-in function names
        """
        return sorted(self.ALLOWED_BUILTINS)
    
    def get_blocked_builtins(self) -> list:
        """
        Get list of blocked built-in functions.
        
        Returns:
            Sorted list of blocked built-in function names
        """
        return sorted(self.BLOCKED_BUILTINS)
    
    def get_blocked_modules(self) -> list:
        """
        Get list of blocked modules.
        
        Returns:
            Sorted list of blocked module names
        """
        return sorted(self.BLOCKED_MODULES)
