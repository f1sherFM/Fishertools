"""
Fishertools - инструменты, которые делают Python удобнее и безопаснее для новичков
"""

__version__ = "0.2.0"
__author__ = "f1sherFM"

# Main API exports - the primary interface for users
from .errors import explain_error

# Legacy imports for backward compatibility
from . import utils
from . import decorators  
from . import helpers

# Module imports for advanced users
from . import errors
from . import safe
from . import learn
from . import legacy

__all__ = [
    # Primary API
    "explain_error",
    # Legacy modules
    "utils", "decorators", "helpers",
    # New modules
    "errors", "safe", "learn", "legacy"
]