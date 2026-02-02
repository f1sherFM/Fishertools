"""
Robust explanation loader for fishertools learning module.

This module provides the ExplanationLoader class that handles loading
explanations.json using importlib.resources with fallbacks for different
Python versions and proper error handling.
"""

import json
import sys
from typing import Dict, Any, Optional

# Import handling for different Python versions
if sys.version_info >= (3, 9):
    from importlib import resources
else:
    try:
        import importlib_resources as resources
    except ImportError:
        # Fallback to pkg_resources for older Python versions
        import pkg_resources
        resources = None


class ExplanationLoader:
    """
    Handles loading and caching of explanation data from explanations.json.
    
    This class provides robust resource loading using importlib.resources
    with fallbacks for different Python versions and clear error handling
    for missing file scenarios.
    
    Attributes:
        explanations (Dict[str, Any]): Cached explanation data
        _loaded (bool): Whether explanations have been successfully loaded
    
    Example:
        >>> loader = ExplanationLoader()
        >>> explanation = loader.get_explanation("list")
        >>> print(explanation["description"])
    """
    
    def __init__(self):
        """
        Initialize the ExplanationLoader.
        
        The loader will attempt to load explanations during initialization
        but will not raise errors - use is_loaded() to check if loading succeeded.
        """
        self.explanations: Optional[Dict[str, Any]] = None
        self._loaded: bool = False
        self._load_explanations()
    
    def _load_explanations(self) -> None:
        """
        Load explanations from bundled JSON file using importlib.resources.
        
        This method tries multiple approaches for maximum compatibility:
        1. importlib.resources (Python 3.9+)
        2. importlib_resources backport
        3. pkg_resources fallback
        4. Direct file access as last resort
        
        Raises:
            FileNotFoundError: If explanations.json cannot be found
            json.JSONDecodeError: If the JSON file is corrupted
            Exception: For other unexpected errors during loading
        """
        try:
            # Try modern importlib.resources approach (Python 3.9+)
            if sys.version_info >= (3, 9) and resources:
                self._load_with_importlib_resources()
            # Try importlib_resources backport
            elif resources:
                self._load_with_importlib_resources()
            # Fallback to pkg_resources
            else:
                self._load_with_pkg_resources()
                
        except Exception as e:
            # Last resort: try direct file access for development
            try:
                self._load_with_direct_access()
            except Exception:
                # Re-raise the original error if all methods fail
                raise e
    
    def _load_with_importlib_resources(self) -> None:
        """Load explanations using importlib.resources."""
        try:
            # For Python 3.9+
            if hasattr(resources, 'files'):
                files = resources.files('fishertools.learn')
                explanations_file = files / 'explanations.json'
                content = explanations_file.read_text(encoding='utf-8')
            # For older versions with importlib_resources
            else:
                content = resources.read_text('fishertools.learn', 'explanations.json', encoding='utf-8')
            
            self.explanations = json.loads(content)
            self._loaded = True
            
        except (FileNotFoundError, ModuleNotFoundError) as e:
            raise FileNotFoundError(
                "explanations.json not found in fishertools.learn package. "
                "This may indicate a packaging issue. Please ensure the file is "
                "included in the package distribution."
            ) from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Failed to parse explanations.json: {e.msg}. "
                "The file may be corrupted or contain invalid JSON.",
                e.doc,
                e.pos
            ) from e
    
    def _load_with_pkg_resources(self) -> None:
        """Load explanations using pkg_resources fallback."""
        try:
            content = pkg_resources.resource_string(
                'fishertools.learn', 
                'explanations.json'
            ).decode('utf-8')
            
            self.explanations = json.loads(content)
            self._loaded = True
            
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "explanations.json not found in fishertools.learn package using pkg_resources. "
                "This may indicate a packaging issue. Please ensure the file is "
                "included in the package distribution."
            ) from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Failed to parse explanations.json using pkg_resources: {e.msg}. "
                "The file may be corrupted or contain invalid JSON.",
                e.doc,
                e.pos
            ) from e
    
    def _load_with_direct_access(self) -> None:
        """
        Load explanations using direct file access as last resort.
        
        This method is primarily for development environments where
        the package may not be properly installed.
        """
        import os
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        explanations_path = os.path.join(current_dir, 'explanations.json')
        
        if not os.path.exists(explanations_path):
            raise FileNotFoundError(
                f"explanations.json not found at {explanations_path}. "
                "Please ensure the file exists in the fishertools/learn/ directory. "
                "If you installed fishertools via pip, this may indicate a packaging issue."
            )
        
        try:
            with open(explanations_path, 'r', encoding='utf-8') as f:
                self.explanations = json.load(f)
            self._loaded = True
            
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Failed to parse explanations.json at {explanations_path}: {e.msg}. "
                "The file may be corrupted or contain invalid JSON.",
                e.doc,
                e.pos
            ) from e
    
    def is_loaded(self) -> bool:
        """
        Check if explanations have been successfully loaded.
        
        Returns:
            bool: True if explanations are loaded and available, False otherwise
        """
        return self._loaded and self.explanations is not None
    
    def get_explanation(self, topic: str) -> Dict[str, str]:
        """
        Retrieve explanation for a specific topic.
        
        Args:
            topic: The topic name to get explanation for (case-insensitive)
        
        Returns:
            Dictionary containing explanation data with keys:
            - 'description': Clear explanation of the topic
            - 'when_to_use': Practical guidance on usage
            - 'example': Code example demonstrating the topic
        
        Raises:
            RuntimeError: If explanations are not loaded
            ValueError: If the topic is not found
        
        Example:
            >>> loader = ExplanationLoader()
            >>> explanation = loader.get_explanation("list")
            >>> print(explanation["description"])
        """
        if not self.is_loaded():
            raise RuntimeError(
                "Explanations are not loaded. This may be due to a missing "
                "explanations.json file or a packaging issue. Please ensure "
                "fishertools is properly installed."
            )
        
        # Normalize topic name
        topic_normalized = topic.strip().lower()
        
        if topic_normalized not in self.explanations:
            available_topics = sorted(self.explanations.keys())
            topics_str = ", ".join(available_topics)
            raise ValueError(
                f"Topic '{topic}' not found. Available topics: {topics_str}"
            )
        
        # Return a copy to prevent modification of cached data
        import copy
        return copy.deepcopy(self.explanations[topic_normalized])
    
    def list_topics(self) -> list:
        """
        Get a list of all available topics.
        
        Returns:
            Sorted list of available topic names
        
        Raises:
            RuntimeError: If explanations are not loaded
        """
        if not self.is_loaded():
            raise RuntimeError(
                "Explanations are not loaded. Cannot list topics."
            )
        
        return sorted(self.explanations.keys())
    
    def reload(self) -> None:
        """
        Reload explanations from the source file.
        
        This method can be used to refresh explanations if the source
        file has been updated.
        
        Raises:
            Same exceptions as _load_explanations()
        """
        self.explanations = None
        self._loaded = False
        self._load_explanations()


# Global loader instance for convenience
_loader: Optional[ExplanationLoader] = None


def get_loader() -> ExplanationLoader:
    """
    Get the global ExplanationLoader instance.
    
    Returns:
        The global ExplanationLoader instance
    
    Example:
        >>> loader = get_loader()
        >>> explanation = loader.get_explanation("list")
    """
    global _loader
    if _loader is None:
        _loader = ExplanationLoader()
    return _loader


def explain(topic: str) -> Dict[str, str]:
    """
    Get a structured explanation for a Python topic using the global loader.
    
    This function provides a convenient interface to the ExplanationLoader
    for getting topic explanations.
    
    Args:
        topic: The name of the Python topic to explain (case-insensitive)
    
    Returns:
        Dictionary containing explanation data with keys:
        - 'description': Clear explanation of the topic
        - 'when_to_use': Practical guidance on usage  
        - 'example': Code example demonstrating the topic
    
    Raises:
        RuntimeError: If explanations cannot be loaded
        ValueError: If the topic is not found
        FileNotFoundError: If explanations.json is missing
        json.JSONDecodeError: If explanations.json is corrupted
    
    Example:
        >>> explanation = explain('list')
        >>> print(explanation['description'])
        >>> print(explanation['example'])
    """
    return get_loader().get_explanation(topic)