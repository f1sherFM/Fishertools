from __future__ import annotations

import ast
import importlib
import sys
import time
from pathlib import Path


def _collect_init_import_map() -> list[dict[str, object]]:
    """Parse top-level relative imports from fishertools/__init__.py for diagnostics."""
    source = Path("fishertools/__init__.py").read_text(encoding="utf-8")
    module = ast.parse(source)

    import_map: list[dict[str, object]] = []
    for node in module.body:
        if isinstance(node, ast.ImportFrom) and node.level == 1 and node.module:
            import_map.append(
                {
                    "module": node.module,
                    "symbols": [alias.name for alias in node.names],
                }
            )

    return import_map


class TestImportsBaseline:
    def test_import_fishertools_smoke_and_diagnostics(self):
        """Keep a diagnostic baseline for import surface without fragile timing thresholds."""
        before_modules = set(sys.modules)

        started_at = time.perf_counter()
        fishertools = importlib.import_module("fishertools")
        elapsed_ms = (time.perf_counter() - started_at) * 1000

        loaded_modules = set(sys.modules) - before_modules
        loaded_fishertools_modules = {m for m in loaded_modules if m.startswith("fishertools")}

        assert hasattr(fishertools, "__all__")
        assert isinstance(fishertools.__all__, list)
        assert len(fishertools.__all__) > 0

        # These modules are eagerly imported today and form the current baseline
        # for the epic's follow-up tasks (#31/#32).
        expected_eager_modules = {
            "fishertools.errors",
            "fishertools.safe",
            "fishertools.learn",
            "fishertools.visualization",
            "fishertools.network",
            "fishertools.i18n",
        }
        assert expected_eager_modules.issubset(loaded_fishertools_modules)

        # Timing is recorded only as diagnostics; the assertion just guards against
        # broken measurement values while keeping the test stable across CI machines.
        assert elapsed_ms >= 0

    def test_init_import_map_contains_expected_eager_groups(self):
        """Detect accidental drift in top-level eager import declarations."""
        import_map = _collect_init_import_map()
        modules = {entry["module"] for entry in import_map}

        expected_groups = {
            "_version",
            "api_mode",
            "errors",
            "safe",
            "visualization",
            "learn",
            "input_utils",
            "network",
            "i18n",
        }

        assert expected_groups.issubset(modules)

