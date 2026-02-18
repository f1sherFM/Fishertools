from fishertools.errors import (
    ErrorPattern,
    get_formatter,
    get_registered_formatters,
    register_formatter,
    register_pattern_provider,
)
from fishertools.errors.models import ErrorExplanation
from fishertools.i18n import ErrorTranslator, register_translation_provider


class _CustomFormatter:
    def format(self, explanation: ErrorExplanation) -> str:
        return f"CUSTOM::{explanation.error_type}"


def test_custom_formatter_plugin_registration():
    register_formatter("custom", _CustomFormatter)
    formatter = get_formatter("custom")
    out = formatter.format(
        ErrorExplanation(
            original_error="x",
            error_type="ValueError",
            simple_explanation="a",
            fix_tip="b",
            code_example="c",
        )
    )
    assert out == "CUSTOM::ValueError"
    assert "custom" in get_registered_formatters()


def test_custom_pattern_provider_used_by_explainer():
    def provider():
        return [
            ErrorPattern(
                error_type=RuntimeError,
                error_keywords=["plugin-test"],
                explanation="plugin explanation",
                tip="plugin tip",
                example="raise RuntimeError('plugin-test')",
                common_causes=["test"],
            )
        ]

    register_pattern_provider(provider)

    from fishertools.errors import ErrorExplainer

    explainer = ErrorExplainer()
    result = explainer.explain(RuntimeError("plugin-test"))
    assert "plugin explanation" in result.simple_explanation.lower()


def test_custom_translation_provider_used_by_translator():
    def provider():
        return {
            "en": {
                "RuntimeError": {
                    "explanation": "Plugin translated: {error_type} - {error_message}",
                    "suggestions": ["plugin suggestion"],
                }
            }
        }

    register_translation_provider(provider)

    translator = ErrorTranslator()
    explained = translator.explain_error(RuntimeError("boom"), lang="en")
    assert "Plugin translated" in explained.explanation
    assert "plugin suggestion" in explained.suggestions
