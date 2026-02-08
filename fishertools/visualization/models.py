"""
Data models for visualization operations.

This module defines the core data structures used for enhanced visualization
including configuration, results, and algorithm visualization steps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple


@dataclass
class VisualizationConfig:
    """
    Configuration for visualization operations.
    
    Attributes:
        style: Visualization style ('default', 'tree', 'compact')
        colors: Whether to use color highlighting
        max_depth: Maximum depth to visualize (None for unlimited)
        export_format: Export format ('json', 'html', or None)
        color_scheme: Color scheme to use ('default', 'dark', 'light')
    """
    style: str = 'default'
    colors: bool = False
    max_depth: Optional[int] = None
    export_format: Optional[str] = None
    color_scheme: str = 'default'


@dataclass
class VisualizationResult:
    """
    Result of a visualization operation.
    
    Attributes:
        content: The visualization content as a string
        exported_file: Path to exported file (if export was requested)
    """
    content: str
    exported_file: Optional[str] = None
    
    def __str__(self) -> str:
        """Return the visualization content."""
        return self.content


@dataclass
class AlgorithmStep:
    """
    Base class for algorithm visualization steps.
    
    Attributes:
        step_number: Sequential step number
        description: Human-readable description of this step
        array_state: Current state of the array
        highlighted_indices: Indices to highlight in visualization
        comparison_indices: Indices being compared (if applicable)
        swap_occurred: Whether a swap occurred in this step
    """
    step_number: int
    description: str
    array_state: List[Any]
    highlighted_indices: List[int] = field(default_factory=list)
    comparison_indices: Optional[Tuple[int, int]] = None
    swap_occurred: bool = False


@dataclass
class SortingStep(AlgorithmStep):
    """
    Specialized step for sorting algorithm visualization.
    
    Attributes:
        comparisons_count: Total number of comparisons so far
        swaps_count: Total number of swaps so far
        partition_index: Pivot/partition index for quick_sort (optional)
        merge_range: Range being merged for merge_sort as (start, end) tuple (optional)
    """
    comparisons_count: int = 0
    swaps_count: int = 0
    partition_index: Optional[int] = None
    merge_range: Optional[Tuple[int, int]] = None


@dataclass
class SearchStep(AlgorithmStep):
    """
    Specialized step for search algorithm visualization.
    
    Attributes:
        search_range: Current search range (start, end)
        middle_index: Current middle index being examined
        found: Whether the target was found (None if still searching)
        jump_size: Jump size for jump_search algorithm (optional)
        block_start: Block start index for jump_search algorithm (optional)
    """
    search_range: Tuple[int, int] = (0, 0)
    middle_index: int = 0
    found: Optional[bool] = None
    jump_size: Optional[int] = None
    block_start: Optional[int] = None


@dataclass
class AlgorithmVisualization:
    """
    Complete visualization of an algorithm execution.
    
    Attributes:
        steps: List of algorithm steps
        statistics: Dictionary of algorithm statistics (comparisons, swaps, etc.)
        algorithm_name: Name of the algorithm
        input_data: Original input data
        final_array: Final result array (computed from last step)
    """
    steps: List[AlgorithmStep]
    statistics: dict = field(default_factory=dict)
    algorithm_name: str = ""
    input_data: List[Any] = field(default_factory=list)
    final_array: List[Any] = field(init=False)
    
    def __post_init__(self) -> None:
        """Compute final_array from the last step."""
        if self.steps:
            last_step = self.steps[-1]
            if hasattr(last_step, 'array_state'):
                self.final_array = list(last_step.array_state)
            else:
                self.final_array = list(self.input_data)
        else:
            self.final_array = list(self.input_data)
    
    def __len__(self) -> int:
        """Return the number of steps."""
        return len(self.steps)
