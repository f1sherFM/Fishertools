"""Example: extending fishertools via plugin hooks."""

from fishertools.errors import (
    ErrorPattern,
    get_explanation,
    register_formatter,
    register_pattern_provider,
)
from fishertools.errors.models import ErrorExplanation
from fishertools.i18n import register_translation_provider, translate_error


class CompactFormatter:
    def format(self, explanation: ErrorExplanation) -> str:
        return f"[{explanation.error_type}] {explanation.simple_explanation}"


def pattern_provider():
    return [
        ErrorPattern(
            error_type=RuntimeError,
            error_keywords=["plugin-demo"],
            explanation="Runtime error detected by plugin pattern.",
            tip="Check plugin-managed runtime inputs.",
            example="raise RuntimeError('plugin-demo')",
            common_causes=["Custom pipeline failure"],
        )
    ]


def translation_provider():
    return {
        "en": {
            "RuntimeError": {
                "explanation": "Plugin i18n explanation: {error_type} - {error_message}",
                "suggestions": ["Inspect plugin runtime state."],
            }
        }
    }


if __name__ == "__main__":
    register_formatter("compact", CompactFormatter)
    register_pattern_provider(pattern_provider)
    register_translation_provider(translation_provider)

    try:
        raise RuntimeError("plugin-demo")
    except Exception as err:
        print(get_explanation(err, format_type="compact"))
        print(translate_error(err, lang="en").explanation)
