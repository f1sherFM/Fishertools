"""
Output formatters for error explanations.

This module contains formatters for different output types including console
output with color support and structured formatting.
"""

import json
import os
import sys
from typing import Any, Dict, Type
from .exceptions import FormattingError
from .models import ErrorExplanation
from .normalization import normalize_diagnostic_text


class Colors:
    """ANSI color codes for terminal output."""
    
    # Text colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Text styles
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    
    # Reset
    RESET = '\033[0m'
    
    # Background colors
    BG_RED = '\033[101m'
    BG_GREEN = '\033[102m'
    BG_YELLOW = '\033[103m'


class ConsoleFormatter:
    """
    Formatter for console output with color support and structured sections.
    
    Provides clear, readable formatting for error explanations with optional
    color coding to improve readability for beginners.
    """
    
    def __init__(self, use_colors: bool = True):
        """
        Initialize formatter with color support option.
        
        Args:
            use_colors: Whether to use ANSI color codes in output
        """
        self.use_colors = use_colors and self._supports_color()
    
    def _supports_color(self) -> bool:
        """
        Check if the current terminal supports color output.
        
        Returns:
            True if colors are supported, False otherwise
        """
        # Check if we're in a terminal that supports colors
        if not hasattr(sys.stdout, 'isatty') or not sys.stdout.isatty():
            return False
        
        # Check for common environment variables that indicate color support
        term = os.environ.get('TERM', '').lower()
        colorterm = os.environ.get('COLORTERM', '').lower()
        
        # Most modern terminals support colors
        if 'color' in term or 'color' in colorterm:
            return True
        if term in ['xterm', 'xterm-256color', 'screen', 'linux']:
            return True
        
        # Windows Command Prompt and PowerShell support colors in newer versions
        if os.name == 'nt':
            return True
        
        return False
    
    def _colorize(self, text: str, color: str) -> str:
        """
        Apply color to text if colors are enabled.
        
        Args:
            text: Text to colorize
            color: ANSI color code
            
        Returns:
            Colorized text or plain text if colors disabled
        """
        if self.use_colors:
            return f"{color}{text}{Colors.RESET}"
        return text
    
    def _format_section_header(self, title: str) -> str:
        """
        Format a section header with styling.
        
        Args:
            title: Section title
            
        Returns:
            Formatted section header
        """
        if self.use_colors:
            return f"\n{Colors.BOLD}{Colors.BLUE}═══ {title} ═══{Colors.RESET}\n"
        else:
            return f"\n=== {title} ===\n"
    
    def _format_code_block(self, code: str) -> str:
        """
        Format code examples with proper indentation and highlighting.
        
        Args:
            code: Code to format
            
        Returns:
            Formatted code block
        """
        lines = code.strip().split('\n')
        formatted_lines = []
        
        for line in lines:
            # Add consistent indentation
            if line.strip():
                formatted_line = f"    {line}"
                if self.use_colors:
                    # Simple syntax highlighting for Python keywords
                    formatted_line = self._highlight_python_syntax(formatted_line)
                formatted_lines.append(formatted_line)
            else:
                formatted_lines.append("")
        
        code_block = '\n'.join(formatted_lines)
        
        if self.use_colors:
            return f"{Colors.DIM}┌─ Пример кода ─┐{Colors.RESET}\n{code_block}\n{Colors.DIM}└────────────────┘{Colors.RESET}"
        else:
            return f"┌─ Пример кода ─┐\n{code_block}\n└────────────────┘"
    
    def _highlight_python_syntax(self, line: str) -> str:
        """
        Apply basic Python syntax highlighting to a line of code.
        
        Args:
            line: Line of code to highlight
            
        Returns:
            Line with syntax highlighting
        """
        # Keywords
        keywords = ['def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 
                   'finally', 'import', 'from', 'as', 'return', 'yield', 'pass', 'break', 
                   'continue', 'and', 'or', 'not', 'in', 'is', 'True', 'False', 'None']
        
        for keyword in keywords:
            # Use word boundaries to avoid partial matches
            import re
            pattern = r'\b' + re.escape(keyword) + r'\b'
            line = re.sub(pattern, f"{Colors.MAGENTA}{keyword}{Colors.RESET}", line)
        
        # Strings (simple detection)
        line = re.sub(r'(["\'])([^"\']*)\1', f"{Colors.GREEN}\\1\\2\\1{Colors.RESET}", line)
        
        # Comments
        line = re.sub(r'(#.*)', f"{Colors.DIM}\\1{Colors.RESET}", line)
        
        return line
    
    def _wrap_text(self, text: str, width: int = 70) -> str:
        """
        Wrap text to specified width while preserving formatting.
        
        Args:
            text: Text to wrap
            width: Maximum line width
            
        Returns:
            Wrapped text
        """
        import textwrap
        # Preserve long tokens intact (e.g., IDs, hashes, generated values)
        # so formatter does not alter semantic content during wrapping.
        return textwrap.fill(
            text,
            width=width,
            subsequent_indent="  ",
            break_long_words=False,
            break_on_hyphens=False,
        )

    def format(self, explanation: ErrorExplanation) -> str:
        """
        Format error explanation for console output with structured sections.
        
        Args:
            explanation: The error explanation to format
            
        Returns:
            Formatted string for console output with clear sections
        """
        sections = []
        
        # Header with error type
        header = (
            f"🚨 Ошибка Python: {explanation.error_type} "
            f"(рџљЁ РћС€РёР±РєР° Python: {explanation.error_type})"
        )
        sections.append(self._colorize(header, Colors.BOLD + Colors.RED))
        sections.append("Р§С‚Рѕ СЌС‚Рѕ РѕР·РЅР°С‡Р°РµС‚ | РљР°Рє РёСЃРїСЂР°РІРёС‚СЊ | РџСЂРёРјРµСЂ")
        
        # Original error section
        if explanation.original_error.strip():
            sections.append(self._format_section_header("Сообщение об ошибке"))
            error_msg = self._colorize(explanation.original_error, Colors.RED)
            sections.append(f"  {error_msg}")
        
        # Simple explanation section
        sections.append(self._format_section_header("Что это означает"))
        explanation_text = self._wrap_text(explanation.simple_explanation)
        sections.append(f"  {explanation_text}")
        
        # Fix tip section
        sections.append(self._format_section_header("Как исправить"))
        tip_text = self._wrap_text(explanation.fix_tip)
        tip_formatted = self._colorize(tip_text, Colors.YELLOW)
        sections.append(f"  {tip_formatted}")
        
        # Code example section
        if explanation.code_example.strip():
            sections.append(self._format_section_header("Пример"))
            code_block = self._format_code_block(explanation.code_example)
            sections.append(code_block)
        
        # Additional info section
        if explanation.additional_info and explanation.additional_info.strip():
            sections.append(self._format_section_header("Дополнительная информация"))
            info_text = self._wrap_text(
                normalize_diagnostic_text(explanation.additional_info)
            )
            info_formatted = self._colorize(info_text, Colors.CYAN)
            sections.append(f"  {info_formatted}")
        
        # Footer
        footer = "💡 Совет: Внимательно читайте сообщения об ошибках - они содержат важную информацию!"
        sections.append(f"\n{self._colorize(footer, Colors.DIM)}")
        
        return '\n'.join(sections)
    
    def format_simple(self, explanation: ErrorExplanation) -> str:
        """
        Format error explanation in a simple, compact format.
        
        Args:
            explanation: The error explanation to format
            
        Returns:
            Simple formatted string
        """
        parts = []
        
        if explanation.original_error.strip():
            parts.append(f"Ошибка: {explanation.original_error}")
        
        parts.append(f"Объяснение: {explanation.simple_explanation}")
        parts.append(f"Совет: {explanation.fix_tip}")
        
        if explanation.code_example.strip():
            parts.append(f"Пример:\n{explanation.code_example}")
        
        return '\n'.join(parts)


class PlainFormatter:
    """
    Plain text formatter without colors or special formatting.
    
    Useful for logging, file output, or environments that don't support colors.
    """
    
    def _strip_ansi_codes(self, text: str) -> str:
        """
        Remove ANSI escape codes from text.
        
        Args:
            text: Text that may contain ANSI codes
            
        Returns:
            Text with ANSI codes removed
        """
        import re
        # Remove ANSI escape sequences - both complete and incomplete
        # This pattern matches \x1b[ or \033[ followed by any characters until a letter
        # Also includes standalone \x1b[ or \033[ sequences
        ansi_escape = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]?|\x1b\[|\033\[')
        
        # Remove all ANSI sequences
        text = ansi_escape.sub('', text)
        return text

    def format(self, explanation: ErrorExplanation) -> str:
        """
        Format error explanation as plain text.
        
        Args:
            explanation: The error explanation to format
            
        Returns:
            Plain text formatted string
        """
        sections = []
        
        clean_error_type = self._strip_ansi_codes(explanation.error_type)
        sections.append(f"Ошибка Python: {clean_error_type}")
        sections.append(f"РћС€РёР±РєР° Python: {clean_error_type}")
        sections.append("=" * 50)
        
        if explanation.original_error.strip():
            clean_error = self._strip_ansi_codes(explanation.original_error)
            sections.append(f"\nСообщение об ошибке:\n{clean_error}")
        
        clean_explanation = self._strip_ansi_codes(explanation.simple_explanation)
        sections.append(f"\nЧто это означает:\n{clean_explanation}")
        
        clean_tip = self._strip_ansi_codes(explanation.fix_tip)
        sections.append(f"\nКак исправить:\n{clean_tip}")
        
        if explanation.code_example.strip():
            clean_code = self._strip_ansi_codes(explanation.code_example)
            sections.append(f"\nПример:\n{clean_code}")
        
        if explanation.additional_info and explanation.additional_info.strip():
            clean_info = normalize_diagnostic_text(
                self._strip_ansi_codes(explanation.additional_info)
            )
            sections.append(f"\nДополнительная информация:\n{clean_info}")
        
        return '\n'.join(sections)


class JsonFormatter:
    """
    JSON formatter for structured output.
    
    Useful for programmatic processing or integration with other tools.
    """
    
    def format(self, explanation: ErrorExplanation) -> str:
        """
        Format error explanation as JSON.
        
        Args:
            explanation: The error explanation to format
            
        Returns:
            JSON formatted string
        """
        try:
            payload = explanation.to_dict()
            additional_info = payload.get("additional_info")
            if isinstance(additional_info, str):
                payload["additional_info"] = normalize_diagnostic_text(additional_info)
            return json.dumps(payload, ensure_ascii=False, indent=2)
        except Exception as e:
            raise FormattingError(
                f"Не удалось преобразовать объяснение в JSON: {e}",
                formatter_type="json",
                original_error=e,
            )


_FORMATTER_REGISTRY: Dict[str, Type[Any]] = {
    "console": ConsoleFormatter,
    "plain": PlainFormatter,
    "json": JsonFormatter,
}


def register_formatter(name: str, formatter_cls: Type[Any]) -> None:
    """Register a custom formatter class for get_formatter()."""
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Formatter name must be a non-empty string")
    if not callable(formatter_cls):
        raise TypeError("formatter_cls must be callable")
    _FORMATTER_REGISTRY[name.strip().lower()] = formatter_cls


def get_registered_formatters() -> Dict[str, Type[Any]]:
    """Return a copy of the current formatter registry."""
    return dict(_FORMATTER_REGISTRY)


def get_formatter(format_type: str, **kwargs: Any) -> Any:
    """
    Factory function to get appropriate formatter.
    
    Args:
        format_type: Type of formatter ('console', 'plain', 'json')
        **kwargs: Additional arguments for formatter initialization
        
    Returns:
        Formatter instance
        
    Raises:
        FormattingError: If format_type is not supported or formatter creation fails
    """
    from .exceptions import FormattingError
    
    formatters = get_registered_formatters()
    
    format_key = format_type.strip().lower()
    if format_key not in formatters:
        raise FormattingError(f"Неподдерживаемый тип форматтера: {format_type}. "
                            f"Поддерживаемые типы: {list(formatters.keys())}", 
                            formatter_type=format_type)
    
    try:
        formatter_class = formatters[format_key]
        
        # Only pass kwargs that the formatter accepts
        if format_key == 'console':
            return formatter_class(use_colors=kwargs.get('use_colors', True))
        else:
            return formatter_class()
    except Exception as e:
        raise FormattingError(f"Не удалось создать форматтер типа {format_type}: {e}", 
                            formatter_type=format_type, original_error=e) from e
