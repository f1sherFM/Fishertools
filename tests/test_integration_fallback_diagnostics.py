from fishertools.integration import FishertoolsIntegration, reset_integration


class _DummySession:
    topic = "variables"
    level = "beginner"


def test_start_learning_session_logs_warning_on_fallback(caplog, monkeypatch):
    reset_integration()
    integration = FishertoolsIntegration(project_name="test_project")

    calls = {"n": 0}

    def flaky_start(topic, level):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("primary flow failed")
        return _DummySession()

    monkeypatch.setattr(integration.learning_system, "start_tutorial", flaky_start)

    with caplog.at_level("WARNING"):
        session = integration.start_learning_session("variables", "beginner")

    assert isinstance(session, _DummySession)
    assert "Failed to create full learning session" in caplog.text
