"""
Interactive session manager for learning activities.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from .models import (
    TutorialSession, InteractiveExercise, ValidationResult,
    DifficultyLevel, ExerciseStatus
)


class InteractiveSessionManager:
    """
    Manages interactive learning sessions with exercises and feedback.
    
    Handles user input, provides feedback, and manages session state
    for interactive learning experiences.
    """
    
    def __init__(self):
        """Initialize the session manager."""
        self._active_sessions: Dict[str, TutorialSession] = {}
    
    def create_session(self, user_id: str, topic: str, level: DifficultyLevel) -> TutorialSession:
        """
        Create a new interactive learning session.
        
        Args:
            user_id: Unique identifier for the user
            topic: Topic for the session
            level: Difficulty level for the session
            
        Returns:
            TutorialSession: New tutorial session
        """
        # Implementation will be added in task 5.2
        raise NotImplementedError("Will be implemented in task 5.2")
    
    def get_session(self, session_id: str) -> Optional[TutorialSession]:
        """
        Get an active session by ID.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Optional[TutorialSession]: Session or None if not found
        """
        # Implementation will be added in task 5.2
        raise NotImplementedError("Will be implemented in task 5.2")
    
    def submit_solution(self, session_id: str, solution: str) -> ValidationResult:
        """
        Submit a solution for the current exercise in the session.
        
        Args:
            session_id: Unique session identifier
            solution: User's code solution
            
        Returns:
            ValidationResult: Validation result with feedback
        """
        # Implementation will be added in task 5.2
        raise NotImplementedError("Will be implemented in task 5.2")
    
    def get_hint(self, session_id: str) -> Optional[str]:
        """
        Get a hint for the current exercise in the session.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Optional[str]: Hint text or None if no hints available
        """
        # Implementation will be added in task 5.2
        raise NotImplementedError("Will be implemented in task 5.2")
    
    def next_exercise(self, session_id: str) -> Optional[InteractiveExercise]:
        """
        Move to the next exercise in the session.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Optional[InteractiveExercise]: Next exercise or None if session complete
        """
        # Implementation will be added in task 5.2
        raise NotImplementedError("Will be implemented in task 5.2")
    
    def complete_session(self, session_id: str) -> Dict[str, Any]:
        """
        Complete the session and return summary statistics.
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Dict[str, Any]: Session completion summary
        """
        # Implementation will be added in task 5.2
        raise NotImplementedError("Will be implemented in task 5.2")
    
    def provide_additional_examples(self, session_id: str, topic: str) -> List[str]:
        """
        Provide additional examples when user is struggling.
        
        Args:
            session_id: Unique session identifier
            topic: Topic for which to provide examples
            
        Returns:
            List[str]: List of additional example descriptions
        """
        # Implementation will be added in task 5.2
        raise NotImplementedError("Will be implemented in task 5.2")