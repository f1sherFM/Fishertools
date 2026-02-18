"""
Code sandbox for safely executing user code in the REPL.

This module provides a restricted execution environment that prevents access to
dangerous operations like file I/O, imports, and other restricted functions.
"""

import ast
import builtins
import json
import subprocess
import sys
from typing import Any, Dict, Optional, Tuple

try:
    import resource
except ImportError:  # pragma: no cover - not available on some platforms
    resource = None


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

    BLOCKED_ATTRIBUTE_NAMES = {
        "__class__", "__mro__", "__subclasses__", "__globals__",
        "__getattribute__", "__dict__", "__base__", "__bases__",
        "__code__", "__closure__", "__func__", "__self__", "__module__",
    }

    BLOCKED_NAMES = {
        "__builtins__", "__import__", "__loader__", "__spec__",
        "globals", "locals", "vars", "getattr", "setattr", "delattr", "dir",
    }
    
    def __init__(
        self,
        timeout: float = 5.0,
        max_steps: int = 200_000,
        max_memory_mb: int = 128,
    ):
        """
        Initialize the code sandbox.
        
        Args:
            timeout: Maximum execution time in seconds (default: 5.0)
            max_steps: Max executed source lines before forced stop
            max_memory_mb: Memory cap for child process in MB (best effort)
        """
        self.timeout = timeout
        self.max_steps = max_steps
        self.max_memory_mb = max_memory_mb
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

        payload = {
            "code": code,
            "timeout": float(timeout),
            "max_steps": int(self.max_steps),
            "allowed_builtins": sorted(self.ALLOWED_BUILTINS),
        }

        preexec_fn = None
        if resource is not None:
            max_bytes = int(self.max_memory_mb) * 1024 * 1024

            def set_limits() -> None:
                for limit_name in ("RLIMIT_AS", "RLIMIT_DATA"):
                    if hasattr(resource, limit_name):
                        limit = getattr(resource, limit_name)
                        try:
                            resource.setrlimit(limit, (max_bytes, max_bytes))
                        except (OSError, ValueError):
                            continue

            preexec_fn = set_limits

        try:
            proc = subprocess.run(
                [sys.executable, "-c", _SANDBOX_CHILD_RUNNER],
                input=json.dumps(payload),
                text=True,
                capture_output=True,
                timeout=float(timeout) + 0.5,
                preexec_fn=preexec_fn,
            )
        except subprocess.TimeoutExpired:
            return False, "Code execution timed out. Try simpler code."
        except Exception:
            return False, "Sandbox execution failed unexpectedly"

        stdout = proc.stdout.strip()
        if not stdout:
            return False, "Sandbox execution failed unexpectedly"
        try:
            result = json.loads(stdout)
            return bool(result.get("success")), str(result.get("output", ""))
        except Exception:
            return False, "Sandbox execution failed unexpectedly"
    
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
        
        try:
            tree = ast.parse(code, mode="exec")
        except SyntaxError as e:
            error_msg = f"Syntax Error: {e.msg}"
            if e.lineno:
                error_msg += f" (line {e.lineno})"
            return error_msg

        return self._validate_ast(tree)

    def _validate_ast(self, tree: ast.AST) -> str:
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                return "Imports are not allowed in the sandbox"

            if isinstance(node, ast.Attribute):
                if node.attr.startswith("__") or node.attr in self.BLOCKED_ATTRIBUTE_NAMES:
                    return f"Attribute '{node.attr}' is not allowed in the sandbox"

            if isinstance(node, ast.Name) and node.id in self.BLOCKED_NAMES:
                return f"The name '{node.id}' is not allowed in the sandbox"

            if isinstance(node, ast.Call):
                blocked_call = self._extract_called_name(node.func)
                if blocked_call:
                    return f"The function '{blocked_call}' is not allowed in the sandbox"
        return ""

    def _extract_called_name(self, func: ast.AST) -> Optional[str]:
        if isinstance(func, ast.Name):
            if func.id in self.BLOCKED_BUILTINS or func.id in self.BLOCKED_NAMES:
                return func.id
            return None

        if isinstance(func, ast.Attribute):
            if func.attr.startswith("__") or func.attr in self.BLOCKED_ATTRIBUTE_NAMES:
                return func.attr
        return None

    def _create_restricted_globals(self) -> Dict[str, Any]:
        """
        Create a restricted globals dictionary for code execution.
        
        Returns:
            Dictionary with safe built-in functions and common modules
        """
        return self._create_restricted_globals_static()

    @classmethod
    def _create_restricted_globals_static(cls) -> Dict[str, Any]:
        # Start with safe built-ins
        safe_builtins = {
            name: getattr(builtins, name)
            for name in cls.ALLOWED_BUILTINS
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


_SANDBOX_CHILD_RUNNER = r"""
import io
import json
import sys
import time
import builtins
from contextlib import redirect_stdout, redirect_stderr

payload = json.loads(sys.stdin.read())
code = payload["code"]
timeout = float(payload["timeout"])
max_steps = int(payload["max_steps"])
allowed_builtins = payload["allowed_builtins"]

safe_builtins = {
    name: getattr(builtins, name)
    for name in allowed_builtins
    if hasattr(builtins, name)
}

import math
restricted_globals = {
    "__builtins__": safe_builtins,
    "math": math,
}

output_buffer = io.StringIO()
error_buffer = io.StringIO()

try:
    compiled_code = compile(code, "<sandbox>", "exec")
    start_time = time.perf_counter()
    executed_steps = 0

    def tracer(frame, event, arg):
        global executed_steps
        if frame.f_code.co_filename == "<sandbox>" and event == "line":
            executed_steps += 1
            if executed_steps > max_steps:
                raise TimeoutError("Code execution exceeded step limit")
            if time.perf_counter() - start_time > timeout:
                raise TimeoutError("Code execution timed out")
        return tracer

    with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
        old_trace = sys.gettrace()
        sys.settrace(tracer)
        try:
            exec(compiled_code, restricted_globals, restricted_globals)
        finally:
            sys.settrace(old_trace)
    print(json.dumps({"success": True, "output": output_buffer.getvalue()}))
except SyntaxError as e:
    msg = f"Syntax Error: {e.msg}"
    if e.lineno:
        msg += f" (line {e.lineno})"
    print(json.dumps({"success": False, "output": msg}))
except TimeoutError:
    print(json.dumps({"success": False, "output": "Code execution timed out. Try simpler code."}))
except MemoryError:
    print(json.dumps({"success": False, "output": "Code execution exceeded memory limit."}))
except Exception as e:
    print(json.dumps({"success": False, "output": f"{type(e).__name__}: {e}"}))
"""
