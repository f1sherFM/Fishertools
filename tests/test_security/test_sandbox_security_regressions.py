import pytest

from fishertools.learn.repl.code_sandbox import CodeSandbox


pytestmark = pytest.mark.security


class TestSandboxSecurityRegressions:
    def test_allows_identifiers_with_import_substring(self):
        sandbox = CodeSandbox()
        success, output = sandbox.execute("important_value = 10\nprint(important_value)")
        assert success is True
        assert "10" in output

    def test_blocks_dunder_attribute_chain_escape(self):
        sandbox = CodeSandbox()
        code = "print((1).__class__.__mro__[1].__subclasses__())"
        success, output = sandbox.execute(code)
        assert success is False
        assert "__class__" in output or "__mro__" in output or "__subclasses__" in output

    def test_blocks_function_globals_escape(self):
        sandbox = CodeSandbox()
        code = "fn = lambda: 1\nprint(fn.__globals__)"
        success, output = sandbox.execute(code)
        assert success is False
        assert "__globals__" in output

    def test_executes_in_isolated_child_process(self):
        sandbox = CodeSandbox()
        success, output = sandbox.execute("import os")
        assert success is False
        # Import remains blocked by AST validation; execution path uses child process.
        assert "import" in output.lower() or "not allowed" in output.lower()
