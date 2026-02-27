from __future__ import annotations

import fishertools


def test_get_version_info_matches_runtime_version_key():
    info = fishertools.get_version_info()
    expected_key = f"v{fishertools.__version__}"

    assert info["version"] == fishertools.__version__
    assert expected_key in info["enhancements"]


def test_get_version_info_does_not_contain_stale_historical_enhancement_key():
    info = fishertools.get_version_info()
    assert "v0.4.7" not in info["enhancements"]


def test_get_version_info_schema_stability():
    info = fishertools.get_version_info()

    assert set(info.keys()) == {"version", "author", "features", "enhancements"}
    assert isinstance(info["features"], list)
    assert isinstance(info["enhancements"], dict)
    assert all(isinstance(v, list) for v in info["enhancements"].values())

