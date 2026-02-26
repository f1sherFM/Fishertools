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

        # Core eager baseline remains imported immediately after the #32 partial
        # lazy-top-level migration.
        expected_core_eager_modules = {
            "fishertools.errors",
            "fishertools.safe",
        }
        assert expected_core_eager_modules.issubset(loaded_fishertools_modules)

        # Selected modules are now expected to be lazy-loaded on attribute access.
        expected_lazy_modules = {
            "fishertools.learn",
            "fishertools.visualization",
            "fishertools.network",
            "fishertools.i18n",
        }
        assert expected_lazy_modules.isdisjoint(loaded_fishertools_modules)

        # Timing is recorded only as diagnostics; the assertion just guards against
        # broken measurement values while keeping the test stable across CI machines.
        assert elapsed_ms >= 0

    def test_init_import_map_contains_expected_eager_groups(self):
        """Detect accidental drift in top-level eager import declarations."""
        import_map = _collect_init_import_map()
        modules = {entry["module"] for entry in import_map}

        expected_eager_import_groups = {
            "_version",
            "api_mode",
            "_import_facade_contract",
            "errors",
            "safe",
        }

        assert expected_eager_import_groups.issubset(modules)

        # These groups moved from eager imports to lazy symbol dispatch in #32.
        migrated_to_lazy_symbol_dispatch = {"visualization", "learn", "input_utils", "network", "i18n"}
        assert migrated_to_lazy_symbol_dispatch.isdisjoint(modules)

    def test_minimal_eager_exports_are_accessible_after_import(self):
        from fishertools._import_facade_contract import MINIMAL_EAGER_EXPORTS

        fishertools = importlib.import_module("fishertools")
        for name in MINIMAL_EAGER_EXPORTS:
            assert hasattr(fishertools, name), f"{name} should be available after import fishertools"
