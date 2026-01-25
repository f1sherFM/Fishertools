"""
Tutorial Engine for generating step-by-step explanations and interactive lessons.
"""

from typing import List, Optional
from .models import (
    StepExplanation, InteractiveExercise, ValidationResult, 
    CodeContext, DifficultyLevel
)


class TutorialEngine:
    """
    Generates step-by-step explanations and creates interactive exercises.
    
    Provides detailed code explanations with examples and creates
    interactive learning experiences for beginners.
    """
    
    def __init__(self):
        """Initialize the tutorial engine."""
        pass
    
    def generate_step_explanation(self, code_line: str, context: CodeContext) -> StepExplanation:
        """
        Generate detailed explanation for a single line of code.
        
        Args:
            code_line: Single line of Python code to explain
            context: Context information about the code
            
        Returns:
            StepExplanation: Detailed explanation with examples
        """
        # Implementation will be added in task 5.1
        raise NotImplementedError("Will be implemented in task 5.1")
    
    def create_interactive_exercise(self, topic: str, difficulty: DifficultyLevel = DifficultyLevel.BEGINNER) -> InteractiveExercise:
        """
        Create an interactive coding exercise for the given topic.
        
        Args:
            topic: Topic for the exercise (e.g., "lists", "functions")
            difficulty: Difficulty level for the exercise
            
        Returns:
            InteractiveExercise: A new interactive exercise
        """
        # Implementation will be added in task 5.1
        raise NotImplementedError("Will be implemented in task 5.1")
    
    def validate_solution(self, exercise: InteractiveExercise, solution: str) -> ValidationResult:
        """
        Validate a user's solution to an interactive exercise.
        
        Args:
            exercise: The exercise being solved
            solution: User's code solution
            
        Returns:
            ValidationResult: Validation result with feedback
        """
        # Implementation will be added in task 5.1
        raise NotImplementedError("Will be implemented in task 5.1")
    
    def provide_hint(self, exercise: InteractiveExercise, attempt: str) -> str:
        """
        Provide a helpful hint based on the user's attempt.
        
        Args:
            exercise: The exercise being solved
            attempt: User's current attempt
            
        Returns:
            str: Helpful hint for the user
        """
        # Implementation will be added in task 5.1
        raise NotImplementedError("Will be implemented in task 5.1")
    
    def explain_solution(self, exercise: InteractiveExercise) -> List[StepExplanation]:
        """
        Provide detailed explanation of the exercise solution.
        
        Args:
            exercise: The completed exercise
            
        Returns:
            List[StepExplanation]: Step-by-step solution explanation
        """
        # Implementation will be added in task 5.1
        raise NotImplementedError("Will be implemented in task 5.1")