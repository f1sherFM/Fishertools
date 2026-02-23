"""Compatibility contract tests for formatter outputs."""

import json
import re

from fishertools.errors.formatters import get_formatter
from fishertools.errors.models import ErrorExplanation


def _sample_explanation() -> ErrorExplanation:
    return ErrorExplanation(
        original_error="division by zero",
        error_type="ZeroDivisionError",
        simple_explanation="Нельзя делить число на ноль.",
        fix_tip="Проверьте знаменатель перед делением.",
        code_example="if b != 0:\n    print(a / b)",
        additional_info="Проверьте входные данные.",
    )


def test_console_output_contract_sections_and_markers():
    out = get_formatter("console", use_colors=False).format(_sample_explanation())

    assert "Ошибка Python:" in out
    assert "=== Сообщение об ошибке ===" in out
    assert "=== Что это означает ===" in out
    assert "=== Как исправить ===" in out
    assert "=== Пример ===" in out
    assert "=== Дополнительная информация ===" in out
    # Legacy compatibility marker currently preserved in formatter output.
    assert (
        "Что это означает | Как исправить | Пример" in out
        or "Р§С‚Рѕ СЌС‚Рѕ РѕР·РЅР°С‡Р°РµС‚ | РљР°Рє РёСЃРїСЂР°РІРёС‚СЊ | РџСЂРёРјРµСЂ" in out
    )


def test_plain_output_contract_fields_without_ansi():
    out = get_formatter("plain").format(_sample_explanation())

    assert "Ошибка Python:" in out
    assert "Что это означает:" in out
    assert "Как исправить:" in out
    assert "Пример:" in out
    assert not re.search(r"\x1b\[[0-9;]*[a-zA-Z]?", out)


def test_json_output_contract_keys():
    out = get_formatter("json").format(_sample_explanation())
    parsed = json.loads(out)

    required = {
        "original_error",
        "error_type",
        "simple_explanation",
        "fix_tip",
        "code_example",
        "additional_info",
    }
    assert required.issubset(parsed.keys())
    assert parsed["error_type"] == "ZeroDivisionError"


def test_plain_output_normalizes_additional_info_diagnostics_whitespace():
    explanation = _sample_explanation()
    explanation.additional_info = "line1  \r\nline2\t \rline3  "

    out = get_formatter("plain").format(explanation)

    assert "line1\nline2\nline3" in out
    assert "line1  \r" not in out


def test_console_output_normalizes_additional_info_diagnostics_whitespace():
    explanation = _sample_explanation()
    explanation.additional_info = "diag A  \r\ndiag B   "

    out = get_formatter("console", use_colors=False).format(explanation)

    assert "diag A diag B" in " ".join(out.split())
    assert "diag A  \r" not in out
