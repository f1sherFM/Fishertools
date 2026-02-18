import json

from click.testing import CliRunner

from fishertools import cli


class TestLearnCliSmoke:
    def test_topic_command(self):
        runner = CliRunner()
        result = runner.invoke(cli.main, ["learn", "topic", "variables"])

        assert result.exit_code == 0
        payload = json.loads(result.output)
        assert isinstance(payload, dict)

    def test_explain_command(self):
        runner = CliRunner()
        result = runner.invoke(cli.main, ["learn", "explain", "list"])

        assert result.exit_code == 0
        assert result.output.strip()

    def test_quiz_command(self):
        runner = CliRunner()
        result = runner.invoke(cli.main, ["learn", "quiz", "variables", "--level", "beginner"])

        assert result.exit_code == 0
        assert "Quiz:" in result.output

    def test_repl_command(self, monkeypatch):
        runner = CliRunner()

        called = {"ok": False}

        def fake_start(self):
            called["ok"] = True

        monkeypatch.setattr("fishertools.cli.REPLEngine.start", fake_start)

        result = runner.invoke(cli.main, ["learn", "repl"])

        assert result.exit_code == 0
        assert called["ok"] is True
