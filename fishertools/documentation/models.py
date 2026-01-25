"""
Data models for the Documentation Generation module.
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from enum import Enum


class DiagramType(Enum):
    """Types of diagrams that can be generated."""
    ARCHITECTURE = "architecture"
    DATA_FLOW = "data_flow"
    FLOWCHART = "flowchart"
    STRUCTURE = "structure"


class PublishStatus(Enum):
    """Status of documentation publishing."""
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"


@dataclass
class FunctionInfo:
    """Information about a function for documentation."""
    name: str
    docstring: Optional[str]
    parameters: Dict[str, str]  # param_name -> type_annotation
    return_type: Optional[str]
    module_path: str
    line_number: int
    examples: List[str] = None
    
    def __post_init__(self):
        if self.examples is None:
            self.examples = []


@dataclass
class APIInfo:
    """Complete API information for a module."""
    module_name: str
    functions: List[FunctionInfo]
    classes: List[Dict[str, Any]]
    constants: Dict[str, Any]
    imports: List[str]
    docstring: Optional[str] = None


@dataclass
class NavigationTree:
    """Navigation structure for documentation."""
    name: str
    path: str
    children: List['NavigationTree'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []


@dataclass
class ExampleCode:
    """Code example with explanation."""
    code: str
    description: str
    expected_output: Optional[str] = None
    language: str = "python"


@dataclass
class SphinxDocuments:
    """Generated Sphinx documentation."""
    source_files: Dict[str, str]  # filename -> content
    config: Dict[str, Any]
    navigation: NavigationTree
    build_path: str


@dataclass
class PublishResult:
    """Result of publishing documentation."""
    status: PublishStatus
    url: Optional[str] = None
    error_message: Optional[str] = None
    build_log: List[str] = None
    
    def __post_init__(self):
        if self.build_log is None:
            self.build_log = []


@dataclass
class MermaidDiagram:
    """Mermaid diagram representation."""
    diagram_type: DiagramType
    content: str
    title: Optional[str] = None


@dataclass
class FlowDiagram:
    """Data flow diagram."""
    nodes: List[Dict[str, str]]
    edges: List[Dict[str, str]]
    title: str


@dataclass
class Flowchart:
    """Algorithm flowchart."""
    steps: List[Dict[str, Any]]
    connections: List[Dict[str, str]]
    title: str


@dataclass
class StructureDiagram:
    """Data structure visualization."""
    structure_type: str
    data: Any
    visualization: str
    title: Optional[str] = None