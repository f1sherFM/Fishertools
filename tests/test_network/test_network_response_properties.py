"""
Property-based tests for NetworkResponse enhancements.

Feature: fishertools-v0.5.2
Tests the requests-compatible API additions to NetworkResponse.
"""

from __future__ import annotations

import json
import pytest
from hypothesis import given, strategies as st, settings

from fishertools.network.models import NetworkResponse


# Simpler strategy for generating various data types
simple_json_values = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-1000, max_value=1000),
    st.floats(allow_nan=False, allow_infinity=False, min_value=-1000.0, max_value=1000.0),
    st.text(max_size=100),
    st.lists(st.integers(), max_size=10),
    st.dictionaries(st.text(max_size=10), st.integers(), max_size=5)
)


class TestNetworkResponseProperties:
    """Property-based tests for NetworkResponse enhancements."""
    
    @given(data=simple_json_values)
    @settings(max_examples=100)
    def test_property_1_json_equivalence(self, data):
        """
        Property 1: NetworkResponse json() equivalence
        
        **Validates: Requirements 1.1, 1.2**
        
        For any successful NetworkResponse with data, calling .json() should
        return the same value as accessing .data directly.
        """
        response = NetworkResponse(success=True, data=data)
        
        # Property: json() returns same data as .data attribute
        assert response.json() == response.data
        assert response.json() == data
    
    @given(data=st.one_of(st.none(), st.text(max_size=100), st.binary(max_size=100), simple_json_values))
    @settings(max_examples=100)
    def test_property_2_content_returns_bytes(self, data):
        """
        Property 2: NetworkResponse content returns bytes
        
        **Validates: Requirements 1.3**
        
        For any NetworkResponse, the .content property should always return
        bytes, regardless of the data type stored.
        """
        response = NetworkResponse(success=True, data=data)
        
        # Property: content always returns bytes
        assert isinstance(response.content, bytes)
    
    @given(data=st.one_of(st.none(), st.text(max_size=100), st.binary(max_size=100), simple_json_values))
    @settings(max_examples=100)
    def test_property_3_text_returns_string(self, data):
        """
        Property 3: NetworkResponse text returns string
        
        **Validates: Requirements 1.4**
        
        For any NetworkResponse, the .text property should always return
        a string, regardless of the data type stored.
        """
        response = NetworkResponse(success=True, data=data)
        
        # Property: text always returns string
        assert isinstance(response.text, str)
    
    @given(data=simple_json_values)
    @settings(max_examples=100)
    def test_property_5_backward_compatibility(self, data):
        """
        Property 5: Backward compatibility for data attribute
        
        **Validates: Requirements 11.1**
        
        For any NetworkResponse, the .data attribute should continue to work
        as before, providing direct access to the response data.
        """
        response = NetworkResponse(success=True, data=data)
        
        # Property: .data attribute still works
        assert response.data == data
        
        # Property: .data is accessible without calling methods
        direct_access = response.data
        assert direct_access == data


