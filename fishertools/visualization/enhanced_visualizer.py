"""
Enhanced visualization with multiple display options.

This module extends the existing visualize() function with new display styles,
color highlighting, depth limiting, and export functionality.
"""

from __future__ import annotations

import json
import html
from pathlib import Path
from typing import Any, Optional, Dict, Callable

from .models import VisualizationResult, VisualizationConfig


class EnhancedVisualizer:
    """
    Enhanced visualizer with multiple display options and export capabilities.
    
    This class extends the basic visualization functionality with support for
    different display styles, color highlighting, depth limiting, and export
    to various formats.
    """
    
    def __init__(self):
        """Initialize the enhanced visualizer."""
        self.color_scheme = self._init_color_scheme()
        self.export_handlers = self._init_export_handlers()
    
    def visualize(
        self,
        data: Any,
        style: str = 'default',
        colors: bool = False,
        max_depth: Optional[int] = None,
        export: Optional[str] = None,
        **kwargs: Any
    ) -> VisualizationResult:
        """
        Enhanced visualization with multiple display options.
        
        This method provides enhanced visualization with support for different
        styles, color highlighting, depth limiting, and export functionality.
        
        Args:
            data: Data to visualize
            style: Display style ('default', 'tree', 'compact')
            colors: Whether to use color highlighting
            max_depth: Maximum depth to display (None for unlimited)
            export: Export format ('json', 'html', or None)
            **kwargs: Additional visualization options
        
        Returns:
            VisualizationResult with content and optional export file path
        
        Raises:
            ValueError: If invalid parameters are provided
        """
        # Validate parameters
        valid_styles = ['default', 'tree', 'compact']
        if style not in valid_styles:
            raise ValueError(
                f"Invalid style '{style}'. Must be one of: {', '.join(valid_styles)}"
            )
        
        if export is not None:
            valid_formats = ['json', 'html']
            if export not in valid_formats:
                raise ValueError(
                    f"Invalid export format '{export}'. Must be one of: {', '.join(valid_formats)}"
                )
        
        if max_depth is not None and max_depth < 0:
            raise ValueError(f"max_depth must be non-negative, got {max_depth}")
        
        # Render content based on style
        if style == 'tree':
            content = self._render_tree_style(data, max_depth, depth=0)
        elif style == 'compact':
            content = self._render_compact_style(data, max_depth)
        else:  # default
            content = self._render_default_style(data, max_depth, depth=0)
        
        # Apply color highlighting if requested
        if colors:
            content = self._apply_colors_to_content(content, data)
        
        # Export if requested
        exported_file = None
        if export:
            filename = kwargs.get('filename', 'visualization')
            exported_file = self._export_visualization(content, export, filename, data)
        
        return VisualizationResult(content=content, exported_file=exported_file)
    
    def _init_color_scheme(self) -> Dict[str, str]:
        """
        Initialize color scheme for highlighting.
        
        Returns:
            Dictionary mapping data types to ANSI color codes
        """
        return {
            'str': '\033[92m',      # Green
            'int': '\033[94m',      # Blue
            'float': '\033[94m',    # Blue
            'bool': '\033[95m',     # Magenta
            'None': '\033[90m',     # Gray
            'list': '\033[93m',     # Yellow
            'dict': '\033[96m',     # Cyan
            'tuple': '\033[93m',    # Yellow
            'set': '\033[93m',      # Yellow
            'reset': '\033[0m'      # Reset
        }
    
    def _init_export_handlers(self) -> Dict[str, Callable]:
        """
        Initialize export handlers for different formats.
        
        Returns:
            Dictionary mapping format names to handler functions
        """
        return {
            'json': self._export_json,
            'html': self._export_html
        }
    
    def _render_tree_style(
        self, 
        data: Any, 
        max_depth: Optional[int],
        depth: int = 0,
        prefix: str = ""
    ) -> str:
        """
        Render data in tree-like hierarchical format.
        
        Args:
            data: Data to render
            max_depth: Maximum depth to render
            depth: Current depth level
            prefix: Prefix for tree branches
        
        Returns:
            Tree-style visualization string
        """
        if max_depth is not None and depth >= max_depth:
            return f"{prefix}..."
        
        lines = []
        
        if isinstance(data, dict):
            for i, (key, value) in enumerate(data.items()):
                is_last = i == len(data) - 1
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{key}: ", )
                
                if isinstance(value, (dict, list, tuple, set)):
                    child_prefix = prefix + ("    " if is_last else "│   ")
                    lines.append(self._render_tree_style(value, max_depth, depth + 1, child_prefix))
                else:
                    lines.append(f"{self._format_value(value)}")
        
        elif isinstance(data, (list, tuple, set)):
            items = list(data)
            for i, item in enumerate(items):
                is_last = i == len(items) - 1
                connector = "└── " if is_last else "├── "
                
                if isinstance(item, (dict, list, tuple, set)):
                    lines.append(f"{prefix}{connector}[{i}]:")
                    child_prefix = prefix + ("    " if is_last else "│   ")
                    lines.append(self._render_tree_style(item, max_depth, depth + 1, child_prefix))
                else:
                    lines.append(f"{prefix}{connector}[{i}]: {self._format_value(item)}")
        
        else:
            lines.append(f"{prefix}{self._format_value(data)}")
        
        return "\n".join(lines)
    
    def _render_default_style(
        self,
        data: Any,
        max_depth: Optional[int],
        depth: int = 0,
        indent: str = "  "
    ) -> str:
        """
        Render data in default style with indentation.
        
        Args:
            data: Data to render
            max_depth: Maximum depth to render
            depth: Current depth level
            indent: Indentation string
        
        Returns:
            Default-style visualization string
        """
        if max_depth is not None and depth >= max_depth:
            return "..."
        
        current_indent = indent * depth
        
        if isinstance(data, dict):
            if not data:
                return "{}"
            lines = ["{"]
            for key, value in data.items():
                if isinstance(value, (dict, list, tuple, set)):
                    nested = self._render_default_style(value, max_depth, depth + 1, indent)
                    lines.append(f"{current_indent}{indent}{repr(key)}: {nested}")
                else:
                    lines.append(f"{current_indent}{indent}{repr(key)}: {self._format_value(value)}")
            lines.append(f"{current_indent}}}")
            return "\n".join(lines)
        
        elif isinstance(data, (list, tuple)):
            if not data:
                return "[]" if isinstance(data, list) else "()"
            bracket_open = "[" if isinstance(data, list) else "("
            bracket_close = "]" if isinstance(data, list) else ")"
            lines = [bracket_open]
            for item in data:
                if isinstance(item, (dict, list, tuple, set)):
                    nested = self._render_default_style(item, max_depth, depth + 1, indent)
                    lines.append(f"{current_indent}{indent}{nested},")
                else:
                    lines.append(f"{current_indent}{indent}{self._format_value(item)},")
            lines.append(f"{current_indent}{bracket_close}")
            return "\n".join(lines)
        
        elif isinstance(data, set):
            if not data:
                return "set()"
            lines = ["{"]
            for item in data:
                lines.append(f"{current_indent}{indent}{self._format_value(item)},")
            lines.append(f"{current_indent}}}")
            return "\n".join(lines)
        
        else:
            return self._format_value(data)
    
    def _render_compact_style(self, data: Any, max_depth: Optional[int]) -> str:
        """
        Render data in compact single-line style.
        
        Args:
            data: Data to render
            max_depth: Maximum depth to render (applied via truncation)
        
        Returns:
            Compact visualization string
        """
        result = repr(data)
        if len(result) > 100:
            result = result[:97] + "..."
        return result
    
    def _format_value(self, value: Any) -> str:
        """Format a single value for display."""
        if isinstance(value, str):
            return repr(value)
        elif value is None:
            return "None"
        elif isinstance(value, bool):
            return str(value)
        else:
            return str(value)
    
    def _apply_colors_to_content(self, content: str, data: Any) -> str:
        """
        Apply color highlighting to content based on data types.
        
        Args:
            content: Content to colorize
            data: Original data for type detection
        
        Returns:
            Colorized content string
        """
        # Apply colors based on data type patterns
        data_type = type(data).__name__
        
        if data_type in self.color_scheme:
            color = self.color_scheme[data_type]
            reset = self.color_scheme['reset']
            return f"{color}{content}{reset}"
        
        return content
    
    def _apply_color_highlighting(self, text: str, data_type: str) -> str:
        """
        Apply color highlighting based on data types.
        
        Args:
            text: Text to colorize
            data_type: Type of data for color selection
        
        Returns:
            Colorized text string
        """
        if data_type in self.color_scheme:
            color = self.color_scheme[data_type]
            reset = self.color_scheme['reset']
            return f"{color}{text}{reset}"
        return text
    
    def _export_visualization(
        self,
        content: str,
        format: str,
        filename: str,
        data: Any
    ) -> Optional[str]:
        """
        Export visualization to specified format.
        
        Args:
            content: Visualization content
            format: Export format ('json', 'html')
            filename: Output filename (without extension)
            data: Original data for export
        
        Returns:
            Path to exported file if successful, None otherwise
        """
        handler = self.export_handlers.get(format)
        if not handler:
            return None
        
        try:
            return handler(content, filename, data)
        except Exception:
            return None
    
    def _export_json(self, content: str, filename: str, data: Any) -> str:
        """
        Export visualization data to JSON format.
        
        Args:
            content: Visualization content (not used for JSON)
            filename: Output filename
            data: Original data to export
        
        Returns:
            Path to exported JSON file
        """
        filepath = Path(f"{filename}.json")
        
        # Convert data to JSON-serializable format
        export_data = {
            'data': self._make_json_serializable(data),
            'visualization': content
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def _export_html(self, content: str, filename: str, data: Any) -> str:
        """
        Export visualization to HTML format.
        
        Args:
            content: Visualization content
            filename: Output filename
            data: Original data (not used for HTML)
        
        Returns:
            Path to exported HTML file
        """
        filepath = Path(f"{filename}.html")
        
        # Escape HTML and preserve formatting
        escaped_content = html.escape(content)
        
        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Visualization - {html.escape(filename)}</title>
    <style>
        body {{
            font-family: 'Courier New', monospace;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        .visualization {{
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 20px;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        h1 {{
            color: #333;
            font-family: Arial, sans-serif;
        }}
    </style>
</head>
<body>
    <h1>Data Visualization</h1>
    <div class="visualization">{escaped_content}</div>
</body>
</html>"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_template)
        
        return str(filepath)
    
    def _make_json_serializable(self, data: Any) -> Any:
        """
        Convert data to JSON-serializable format.
        
        Args:
            data: Data to convert
        
        Returns:
            JSON-serializable version of data
        """
        if isinstance(data, (str, int, float, bool, type(None))):
            return data
        elif isinstance(data, dict):
            return {str(k): self._make_json_serializable(v) for k, v in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self._make_json_serializable(item) for item in data]
        elif isinstance(data, set):
            return list(data)
        else:
            return str(data)
