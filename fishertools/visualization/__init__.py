"""Visualization module for fishertools.

Provides tools for visualizing data structures in a human-readable format,
with enhanced options for styling, colors, and algorithm visualization.
"""

from .visualizer import Visualizer, visualize
from .models import (
    VisualizationConfig,
    VisualizationResult,
    AlgorithmStep,
    SortingStep,
    SearchStep,
    AlgorithmVisualization,
)
from .enhanced_visualizer import EnhancedVisualizer
from .algorithm_visualizer import AlgorithmVisualizer

# Algorithm implementations
from .algorithms import (
    visualize_quick_sort,
    visualize_merge_sort,
    visualize_insertion_sort,
    visualize_selection_sort,
    visualize_linear_search,
    visualize_jump_search,
)

__all__ = [
    # Core visualization (existing)
    "Visualizer",
    "visualize",
    
    # Enhanced visualization (new)
    "EnhancedVisualizer",
    "AlgorithmVisualizer",
    
    # Data models (new)
    "VisualizationConfig",
    "VisualizationResult",
    "AlgorithmStep",
    "SortingStep",
    "SearchStep",
    "AlgorithmVisualization",
    
    # Algorithm implementations (v0.5.2)
    "visualize_quick_sort",
    "visualize_merge_sort",
    "visualize_insertion_sort",
    "visualize_selection_sort",
    "visualize_linear_search",
    "visualize_jump_search",
]


