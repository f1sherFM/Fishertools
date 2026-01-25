"""
Legacy support module for fishertools.

This module maintains backward compatibility for existing functions
while providing deprecation warnings for functions being removed.
"""

from .deprecated import *

# Import retained functions that align with the new mission
# These will be determined during the legacy support implementation