import pytest

from fishertools.api_mode import api_mode, get_api_mode, set_api_mode
from fishertools.errors.exceptions import SafeUtilityError
from fishertools.safe.files import safe_file_exists, safe_read_file


class TestApiBehaviorModes:
    def test_set_get_mode(self):
        old = get_api_mode()
        try:
            set_api_mode("strict")
            assert get_api_mode() == "strict"
            set_api_mode("friendly")
            assert get_api_mode() == "friendly"
        finally:
            set_api_mode(old)

    def test_friendly_mode_returns_defaults(self):
        with api_mode("friendly"):
            assert safe_read_file(None, default="fallback") == "fallback"
            assert safe_file_exists(None) is False

    def test_strict_mode_raises(self):
        with api_mode("strict"):
            with pytest.raises(SafeUtilityError):
                safe_read_file(None, default="fallback")
            with pytest.raises(SafeUtilityError):
                safe_file_exists(None)
