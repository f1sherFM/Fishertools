import json
import os

from fishertools.learning.progress import ProgressSystem


def test_save_progress_handles_json_serialization_error(caplog, monkeypatch, tmp_path):
    storage_path = tmp_path / "progress.json"
    system = ProgressSystem(storage_path=str(storage_path))
    system.create_user_profile("user-a")

    def fail_dump(*args, **kwargs):
        raise TypeError("not serializable")

    monkeypatch.setattr(json, "dump", fail_dump)

    with caplog.at_level("WARNING"):
        system.save_progress("user-a")

    assert "Progress persistence fallback activated" in caplog.text


def test_save_progress_handles_invalid_existing_json(caplog, tmp_path):
    storage_path = tmp_path / "progress.json"
    storage_path.write_text("{broken-json", encoding="utf-8")

    system = ProgressSystem(storage_path=str(storage_path))
    system.create_user_profile("user-b")

    with caplog.at_level("WARNING"):
        system.save_progress("user-b")

    assert "Progress persistence fallback activated" in caplog.text


def test_load_progress_logs_warning_on_corrupted_file(caplog, tmp_path):
    storage_path = tmp_path / "progress.json"
    os.makedirs(tmp_path, exist_ok=True)
    storage_path.write_text("{broken-json", encoding="utf-8")

    system = ProgressSystem(storage_path=str(storage_path))

    with caplog.at_level("WARNING"):
        result = system.load_progress("user-c")

    assert result is None
    assert "Progress load fallback activated" in caplog.text
