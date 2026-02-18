from fishertools.config.manager import ConfigurationManager
from fishertools.config.settings import SettingsManager


def test_default_config_logs_warning_when_parse_fails(caplog, monkeypatch, tmp_path):
    default_path = tmp_path / "default_config.json"
    default_path.write_text('{"default_level": "beginner"}', encoding="utf-8")

    manager = ConfigurationManager(default_config_path=str(default_path))

    def fail_parse(*args, **kwargs):
        raise ValueError("broken config")

    monkeypatch.setattr(manager.parser, "parse_file", fail_parse)

    with caplog.at_level("WARNING"):
        cfg = manager.get_default_config()

    assert cfg is not None
    assert "Default config fallback activated" in caplog.text


def test_settings_load_logs_warning_on_invalid_json(caplog, tmp_path):
    settings = SettingsManager(config_dir=str(tmp_path))
    settings.config_file.write_text("{broken-json", encoding="utf-8")

    with caplog.at_level("WARNING"):
        loaded = settings.load_settings()

    assert loaded is False
    assert "Settings load fallback activated" in caplog.text


def test_settings_save_logs_warning_when_write_fails(caplog, tmp_path):
    settings = SettingsManager(config_dir=str(tmp_path))
    # Force open() failure by making config_file point to a directory.
    settings.config_file.mkdir(exist_ok=True)

    with caplog.at_level("WARNING"):
        saved = settings.save_settings()

    assert saved is False
    assert "Settings save fallback activated" in caplog.text
