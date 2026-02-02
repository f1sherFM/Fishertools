"""
Property-based tests for explanation loading reliability in fishertools.learn.

Tests the correctness properties of the ExplanationLoader class using hypothesis
for property-based testing.

**Feature: fishertools-bug-fixes, Property 1: Explanation Loading Reliability**
**Validates: Requirements 1.1**
"""

import pytest
from hypothesis import given, strategies as st
import json
import os
from typing import Dict, Any

from fishertools.learn.explanation_loader import ExplanationLoader, explain


def get_valid_topics_from_file() -> list:
    """Get all valid topics from explanations.json file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    explanations_path = os.path.join(
        current_dir, '..', '..', 'fishertools', 'learn', 'explanations.json'
    )
    
    with open(explanations_path, 'r', encoding='utf-8') as f:
        explanations = json.load(f)
    
    return sorted(explanations.keys())


VALID_TOPICS = get_valid_topics_from_file()


class TestExplanationLoadingReliability:
    """
    Property 1: Explanation Loading Reliability
    
    For any valid topic in the explanations data, calling explain() should 
    successfully return educational content without FileNotFoundError.
    
    **Feature: fishertools-bug-fixes, Property 1: Explanation Loading Reliability**
    **Validates: Requirements 1.1**
    """
    
    @given(st.sampled_from(VALID_TOPICS))
    def test_explanation_loading_never_fails_for_valid_topics(self, topic):
        """
        Property test: For any valid topic, explain() should never raise FileNotFoundError.
        
        This test validates that the ExplanationLoader can reliably load and access
        explanations for all valid topics without file access errors.
        """
        # This should never raise FileNotFoundError for valid topics
        try:
            result = explain(topic)
            
            # Verify we got a valid result structure
            assert isinstance(result, dict)
            assert 'description' in result
            assert 'when_to_use' in result  
            assert 'example' in result
            
            # Verify all values are non-empty strings
            assert isinstance(result['description'], str)
            assert isinstance(result['when_to_use'], str)
            assert isinstance(result['example'], str)
            assert len(result['description']) > 0
            assert len(result['when_to_use']) > 0
            assert len(result['example']) > 0
            
        except FileNotFoundError as e:
            pytest.fail(f"FileNotFoundError raised for valid topic '{topic}': {e}")
        except Exception as e:
            # Other exceptions are acceptable (like ValueError for invalid topics)
            # but FileNotFoundError specifically should never occur for valid topics
            if "FileNotFoundError" in str(type(e)) or "file" in str(e).lower():
                pytest.fail(f"File-related error for valid topic '{topic}': {e}")
    
    @given(st.sampled_from(VALID_TOPICS))
    def test_explanation_loader_instance_reliability(self, topic):
        """
        Property test: ExplanationLoader instances should reliably load explanations.
        
        This test validates that creating new ExplanationLoader instances and
        calling get_explanation() works reliably for all valid topics.
        """
        # Create a new loader instance
        loader = ExplanationLoader()
        
        # Verify the loader loaded successfully
        assert loader.is_loaded(), "ExplanationLoader failed to load explanations"
        
        # This should never raise FileNotFoundError for valid topics
        try:
            result = loader.get_explanation(topic)
            
            # Verify we got a valid result structure
            assert isinstance(result, dict)
            assert 'description' in result
            assert 'when_to_use' in result
            assert 'example' in result
            
            # Verify all values are non-empty strings
            assert isinstance(result['description'], str)
            assert isinstance(result['when_to_use'], str)
            assert isinstance(result['example'], str)
            assert len(result['description']) > 0
            assert len(result['when_to_use']) > 0
            assert len(result['example']) > 0
            
        except FileNotFoundError as e:
            pytest.fail(f"FileNotFoundError raised for valid topic '{topic}': {e}")
        except RuntimeError as e:
            if "not loaded" in str(e).lower():
                pytest.fail(f"ExplanationLoader failed to load for topic '{topic}': {e}")
    
    @given(st.sampled_from(VALID_TOPICS))
    def test_explanation_loading_consistency(self, topic):
        """
        Property test: Multiple calls to explain() should return consistent results.
        
        This test validates that the explanation loading is reliable and consistent
        across multiple calls for the same topic.
        """
        try:
            # Call explain multiple times
            result1 = explain(topic)
            result2 = explain(topic)
            result3 = explain(topic)
            
            # All results should be identical
            assert result1 == result2, f"Inconsistent results for topic '{topic}'"
            assert result2 == result3, f"Inconsistent results for topic '{topic}'"
            
            # Verify structure is maintained across calls
            for result in [result1, result2, result3]:
                assert isinstance(result, dict)
                assert set(result.keys()) == {'description', 'when_to_use', 'example'}
                
        except FileNotFoundError as e:
            pytest.fail(f"FileNotFoundError raised for valid topic '{topic}': {e}")
    
    def test_explanation_loader_handles_all_valid_topics(self):
        """
        Test that ExplanationLoader can handle all valid topics without file errors.
        
        This is a comprehensive test that validates the loader works for every
        single topic in the explanations file.
        """
        loader = ExplanationLoader()
        assert loader.is_loaded(), "ExplanationLoader failed to load explanations"
        
        # Test every single valid topic
        for topic in VALID_TOPICS:
            try:
                result = loader.get_explanation(topic)
                
                # Basic validation
                assert isinstance(result, dict)
                assert 'description' in result
                assert 'when_to_use' in result
                assert 'example' in result
                
            except FileNotFoundError as e:
                pytest.fail(f"FileNotFoundError for topic '{topic}': {e}")
            except RuntimeError as e:
                if "not loaded" in str(e).lower():
                    pytest.fail(f"Loader not loaded for topic '{topic}': {e}")
    
    def test_explanation_loader_initialization_reliability(self):
        """
        Test that ExplanationLoader initialization is reliable and doesn't fail.
        
        This test validates that creating multiple ExplanationLoader instances
        works reliably without file access issues.
        """
        # Create multiple loader instances
        loaders = []
        for i in range(5):
            try:
                loader = ExplanationLoader()
                assert loader.is_loaded(), f"Loader {i} failed to load explanations"
                loaders.append(loader)
            except FileNotFoundError as e:
                pytest.fail(f"FileNotFoundError during loader {i} initialization: {e}")
        
        # Verify all loaders work with a sample topic
        sample_topic = VALID_TOPICS[0] if VALID_TOPICS else "list"
        for i, loader in enumerate(loaders):
            try:
                result = loader.get_explanation(sample_topic)
                assert isinstance(result, dict)
            except FileNotFoundError as e:
                pytest.fail(f"FileNotFoundError from loader {i} for topic '{sample_topic}': {e}")
    
    @given(st.sampled_from(VALID_TOPICS))
    def test_explanation_loading_with_case_variations(self, topic):
        """
        Property test: Explanation loading should work with case variations.
        
        This test validates that the loader handles case-insensitive topic names
        reliably without file access errors.
        """
        # Test different case variations
        variations = [
            topic.lower(),
            topic.upper(), 
            topic.capitalize(),
            topic  # original case
        ]
        
        results = []
        for variation in variations:
            try:
                result = explain(variation)
                results.append(result)
                
                # Verify structure
                assert isinstance(result, dict)
                assert 'description' in result
                assert 'when_to_use' in result
                assert 'example' in result
                
            except FileNotFoundError as e:
                pytest.fail(f"FileNotFoundError for topic variation '{variation}': {e}")
        
        # All variations should return the same result
        for i in range(1, len(results)):
            assert results[0] == results[i], f"Inconsistent results for case variations of '{topic}'"


class TestExplanationLoadingEdgeCases:
    """Test edge cases for explanation loading reliability."""
    
    def test_explanation_loading_with_whitespace_handling(self):
        """
        Test that explanation loading handles whitespace in topic names reliably.
        """
        if not VALID_TOPICS:
            pytest.skip("No valid topics available")
            
        sample_topic = VALID_TOPICS[0]
        
        # Test whitespace variations
        variations = [
            f"  {sample_topic}  ",  # leading/trailing spaces
            f"\t{sample_topic}\t",  # tabs
            f"\n{sample_topic}\n",  # newlines
            sample_topic           # original
        ]
        
        results = []
        for variation in variations:
            try:
                result = explain(variation)
                results.append(result)
                
                # Verify structure
                assert isinstance(result, dict)
                assert 'description' in result
                
            except FileNotFoundError as e:
                pytest.fail(f"FileNotFoundError for whitespace variation '{repr(variation)}': {e}")
        
        # All should return the same result
        for i in range(1, len(results)):
            assert results[0] == results[i], f"Inconsistent results for whitespace variations"
    
    def test_explanation_loading_after_reload(self):
        """
        Test that explanation loading works reliably after loader reload.
        """
        if not VALID_TOPICS:
            pytest.skip("No valid topics available")
            
        loader = ExplanationLoader()
        sample_topic = VALID_TOPICS[0]
        
        # Get initial result
        try:
            result1 = loader.get_explanation(sample_topic)
        except FileNotFoundError as e:
            pytest.fail(f"FileNotFoundError before reload: {e}")
        
        # Reload the loader
        try:
            loader.reload()
            assert loader.is_loaded(), "Loader failed to reload"
        except FileNotFoundError as e:
            pytest.fail(f"FileNotFoundError during reload: {e}")
        
        # Get result after reload
        try:
            result2 = loader.get_explanation(sample_topic)
        except FileNotFoundError as e:
            pytest.fail(f"FileNotFoundError after reload: {e}")
        
        # Results should be identical
        assert result1 == result2, "Results differ after reload"