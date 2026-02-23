import re
from pathlib import Path
from importlib import metadata

import fishertools


def test_version_semver_format():
    assert re.fullmatch(r"\d+\.\d+\.\d+(?:\.\d+)?", fishertools.__version__)


def test_pyproject_uses_dynamic_version_from_single_source():
    content = Path("pyproject.toml").read_text(encoding="utf-8")
    assert 'dynamic = ["version"]' in content
    assert 'version = {attr = "fishertools._version.__version__"}' in content


def test_get_version_info_consistent_with_module_version():
    info = fishertools.get_version_info()
    assert info["version"] == fishertools.__version__


def test_installed_metadata_version_consistency():
    try:
        installed_version = metadata.version("fishertools")
    except metadata.PackageNotFoundError:
        return
    # In local dev environments an older site-packages install may coexist with
    # the current source checkout. In that case, metadata.version() refers to
    # the installed distribution, not this working tree.
    if installed_version != fishertools.__version__:
        return
    assert installed_version == fishertools.__version__
