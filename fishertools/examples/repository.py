"""
Repository for managing code examples and learning scenarios.
"""

from typing import List, Optional, Dict
from .models import (
    CodeExample, Scenario, ProjectTemplate, LineByLineExplanation,
    ExampleCategory, ProjectType
)


class ExampleRepository:
    """
    Manages collections of examples and scenarios for Python beginners.
    
    Provides categorized examples with step-by-step explanations
    and simple project templates.
    """
    
    def __init__(self, examples_dir: Optional[str] = None):
        """
        Initialize the example repository.
        
        Args:
            examples_dir: Optional directory containing example files
        """
        self.examples_dir = examples_dir
        self._examples: Dict[str, CodeExample] = {}
        self._scenarios: Dict[str, Scenario] = {}
        self._projects: Dict[str, ProjectTemplate] = {}
    
    def get_examples_by_topic(self, topic: str) -> List[CodeExample]:
        """
        Get all examples for a specific topic.
        
        Args:
            topic: Topic name (e.g., "lists", "dictionaries", "functions")
            
        Returns:
            List[CodeExample]: Examples matching the topic
        """
        # Implementation will be added in task 7.1
        raise NotImplementedError("Will be implemented in task 7.1")
    
    def get_examples_by_category(self, category: ExampleCategory) -> List[CodeExample]:
        """
        Get all examples in a specific category.
        
        Args:
            category: Example category
            
        Returns:
            List[CodeExample]: Examples in the category
        """
        # Implementation will be added in task 7.1
        raise NotImplementedError("Will be implemented in task 7.1")
    
    def get_beginner_scenarios(self) -> List[Scenario]:
        """
        Get all scenarios suitable for beginners.
        
        Returns:
            List[Scenario]: Beginner-friendly scenarios
        """
        # Implementation will be added in task 7.1
        raise NotImplementedError("Will be implemented in task 7.1")
    
    def create_simple_project(self, project_type: ProjectType) -> ProjectTemplate:
        """
        Create a simple project template with step-by-step instructions.
        
        Args:
            project_type: Type of project to create
            
        Returns:
            ProjectTemplate: Project template with instructions
        """
        # Implementation will be added in task 7.1
        raise NotImplementedError("Will be implemented in task 7.1")
    
    def explain_example_line_by_line(self, example: CodeExample) -> LineByLineExplanation:
        """
        Generate line-by-line explanation for a code example.
        
        Args:
            example: Code example to explain
            
        Returns:
            LineByLineExplanation: Detailed line-by-line explanation
        """
        # Implementation will be added in task 7.2
        raise NotImplementedError("Will be implemented in task 7.2")
    
    def add_example(self, example: CodeExample) -> None:
        """
        Add a new example to the repository.
        
        Args:
            example: Code example to add
        """
        # Implementation will be added in task 7.1
        raise NotImplementedError("Will be implemented in task 7.1")
    
    def search_examples(self, query: str, category: Optional[ExampleCategory] = None) -> List[CodeExample]:
        """
        Search for examples matching a query.
        
        Args:
            query: Search query
            category: Optional category filter
            
        Returns:
            List[CodeExample]: Matching examples
        """
        # Implementation will be added in task 7.1
        raise NotImplementedError("Will be implemented in task 7.1")