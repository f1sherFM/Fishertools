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
]
