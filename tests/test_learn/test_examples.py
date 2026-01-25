"""
Unit tests for the examples module in fishertools.learn.

Tests the generate_example function and related utilities for
generating educational code examples.
"""

import pytest
from fishertools.learn.examples import (
    generate_example,
    list_available_concepts,
    get_concept_info,
    CODE_EXAMPLES
)


class TestGenerateExample:
    """Test the generate_example function."""
    
    def test_generate_example_valid_concept(self):
        """Test generating example for a valid concept."""
        result = generate_example("variables")
        
        # Should return a formatted string with content
        assert isinstance(result, str)
        assert len(result) > 0
        
        # Should contain expected sections
        assert "Переменные и типы данных" in result
        assert "Описание:" in result
        assert "Пример кода:" in result
        assert "Совет:" in result
        
        # Should contain actual code content
        assert "name = " in result
        assert "print(" in result
    
    def test_generate_example_invalid_concept(self):
        """Test generating example for an invalid concept."""
        result = generate_example("nonexistent_concept")
        
        # Should return error message
        assert "❌ Концепция 'nonexistent_concept' не найдена" in result
        assert "📚 Доступные концепции:" in result
    
    def test_generate_example_case_insensitive(self):
        """Test that concept matching is case insensitive."""
        result1 = generate_example("VARIABLES")
        result2 = generate_example("variables")
        result3 = generate_example("Variables")
        
        # All should produce the same result
        assert "Переменные и типы данных" in result1
        assert "Переменные и типы данных" in result2
        assert "Переменные и типы данных" in result3
    
    def test_generate_example_whitespace_handling(self):
        """Test that whitespace is handled correctly."""
        result = generate_example("  variables  ")
        
        # Should work despite extra whitespace
        assert "Переменные и типы данных" in result
    
    def test_all_concepts_generate_valid_examples(self):
        """Test that all available concepts generate valid examples."""
        concepts = list_available_concepts()
        
        for concept in concepts:
            result = generate_example(concept)
            
            # Each should return a valid formatted example
            assert isinstance(result, str)
            assert len(result) > 100  # Should be substantial content
            assert "Описание:" in result
            assert "Пример кода:" in result
            assert "Совет:" in result
            
            # Should not contain error messages (but may contain ❌ in educational content)
            assert "не найдена" not in result
            assert "Доступные концепции:" not in result


class TestListAvailableConcepts:
    """Test the list_available_concepts function."""
    
    def test_returns_list(self):
        """Test that function returns a list."""
        result = list_available_concepts()
        assert isinstance(result, list)
    
    def test_contains_expected_concepts(self):
        """Test that list contains expected concepts."""
        concepts = list_available_concepts()
        
        # Should contain core Python concepts
        expected_concepts = [
            "variables", "lists", "dictionaries", 
            "functions", "loops", "conditionals", "file_operations"
        ]
        
        for concept in expected_concepts:
            assert concept in concepts
    
    def test_all_concepts_have_data(self):
        """Test that all listed concepts have corresponding data."""
        concepts = list_available_concepts()
        
        for concept in concepts:
            assert concept in CODE_EXAMPLES
            assert "title" in CODE_EXAMPLES[concept]
            assert "description" in CODE_EXAMPLES[concept]
            assert "code" in CODE_EXAMPLES[concept]


class TestGetConceptInfo:
    """Test the get_concept_info function."""
    
    def test_valid_concept_returns_info(self):
        """Test getting info for a valid concept."""
        info = get_concept_info("variables")
        
        assert info is not None
        assert isinstance(info, dict)
        assert "title" in info
        assert "description" in info
        
        # Should contain expected content
        assert "Переменные и типы данных" in info["title"]
        assert "Основы работы с переменными" in info["description"]
    
    def test_invalid_concept_returns_none(self):
        """Test getting info for an invalid concept."""
        info = get_concept_info("nonexistent")
        assert info is None
    
    def test_case_insensitive_lookup(self):
        """Test that concept lookup is case insensitive."""
        info1 = get_concept_info("VARIABLES")
        info2 = get_concept_info("variables")
        
        assert info1 is not None
        assert info2 is not None
        assert info1["title"] == info2["title"]
    
    def test_whitespace_handling(self):
        """Test that whitespace is handled in concept lookup."""
        info = get_concept_info("  variables  ")
        
        assert info is not None
        assert "Переменные и типы данных" in info["title"]


class TestCodeExamplesData:
    """Test the CODE_EXAMPLES data structure."""
    
    def test_all_examples_have_required_fields(self):
        """Test that all code examples have required fields."""
        for concept, data in CODE_EXAMPLES.items():
            assert "title" in data
            assert "description" in data
            assert "code" in data
            
            # Fields should not be empty
            assert len(data["title"]) > 0
            assert len(data["description"]) > 0
            assert len(data["code"]) > 0
    
    def test_code_examples_contain_actual_code(self):
        """Test that code examples contain actual Python code."""
        for concept, data in CODE_EXAMPLES.items():
            code = data["code"]
            
            # Should contain Python-like syntax
            assert any(keyword in code for keyword in ["print(", "def ", "=", "if ", "for "])
    
    def test_examples_are_educational(self):
        """Test that examples contain educational content."""
        for concept, data in CODE_EXAMPLES.items():
            code = data["code"]
            
            # Should contain comments (educational explanations)
            assert "#" in code
            
            # Should contain Russian explanations
            assert any(char in code for char in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя")


class TestIntegration:
    """Integration tests for the examples module."""
    
    def test_complete_workflow(self):
        """Test complete workflow of discovering and generating examples."""
        # Get available concepts
        concepts = list_available_concepts()
        assert len(concepts) > 0
        
        # Get info for first concept
        first_concept = concepts[0]
        info = get_concept_info(first_concept)
        assert info is not None
        
        # Generate example for the concept
        example = generate_example(first_concept)
        assert "❌" not in example  # Should not be an error
        assert info["title"] in example  # Should contain the title
    
    def test_error_handling_consistency(self):
        """Test that error handling is consistent across functions."""
        invalid_concept = "definitely_not_a_concept"
        
        # generate_example should return error message
        example_result = generate_example(invalid_concept)
        assert "❌" in example_result
        
        # get_concept_info should return None
        info_result = get_concept_info(invalid_concept)
        assert info_result is None
        
        # list_available_concepts should not include invalid concept
        concepts = list_available_concepts()
        assert invalid_concept not in concepts