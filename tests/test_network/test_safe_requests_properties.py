"""
Property-based tests for safe network request operations.

Feature: fishertools-enhancements, Property 1: Safe request behavior
For any valid URL and timeout value, calling safe_request() should either return 
a successful NetworkResponse with data or a structured error response, never 
raising unhandled exceptions.

Feature: fishertools-enhancements, Property 2: Network error handling
For any network failure condition (timeout, connection error, invalid parameters), 
the Safe_Network_Module should return a structured NetworkResponse with success=False 
and descriptive error information.

**Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5, 1.6**
"""

import pytest
from hypothesis import given, strategies as st, assume, settings
from unittest.mock import Mock, patch, MagicMock
import requests
from requests.exceptions import (
    Timeout, ConnectionError, HTTPError, TooManyRedirects, InvalidURL, RequestException
)

from fishertools.network import SafeHTTPClient, NetworkResponse


# Custom strategies for network testing
@st.composite
def valid_urls(draw):
    """Generate valid HTTP/HTTPS URLs"""
    protocol = draw(st.sampled_from(['http://', 'https://']))
    domain = draw(st.text(
        alphabet=st.characters(whitelist_categories=('Ll', 'Nd'), min_codepoint=97, max_codepoint=122),
        min_size=3,
        max_size=20
    ))
    tld = draw(st.sampled_from(['.com', '.org', '.net', '.io']))
    path = draw(st.one_of(
        st.just(''),
        st.text(
            alphabet=st.characters(whitelist_categories=('Ll', 'Nd'), min_codepoint=97, max_codepoint=122),
            min_size=1,
            max_size=20
        ).map(lambda x: f'/{x}')
    ))
    return f"{protocol}{domain}{tld}{path}"


@st.composite
def invalid_urls(draw):
    """Generate invalid URLs"""
    return draw(st.one_of(
        st.just(''),
        st.just('not-a-url'),
        st.just('ftp://invalid.com'),
        st.text(max_size=10).filter(lambda x: not x.startswith(('http://', 'https://'))),
        st.none()
    ))


class TestSafeRequestBehavior:
    """
    Property 1: Safe request behavior
    
    For any valid URL and timeout value, calling safe_request() should either 
    return a successful NetworkResponse with data or a structured error response, 
    never raising unhandled exceptions.
    
    **Validates: Requirements 1.1, 1.2, 1.5**
    """
    
    @given(
        url=valid_urls(),
        timeout=st.one_of(st.none(), st.floats(min_value=0.1, max_value=60.0))
    )
    @settings(max_examples=20)
    def test_safe_request_always_returns_network_response(self, url, timeout):
        """Property: safe_request always returns NetworkResponse, never raises exceptions."""
        client = SafeHTTPClient()
        
        # Mock the session to avoid actual network calls
        with patch.object(client.session, 'request') as mock_request:
            # Simulate successful response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = "Success"
            mock_response.json.return_value = {"status": "ok"}
            mock_response.headers = {"content-type": "application/json"}
            mock_request.return_value = mock_response
            
            # Property: Should return NetworkResponse
            result = client.safe_request(url, timeout=timeout)
            assert isinstance(result, NetworkResponse)
            
            # Property: Response should have success attribute
            assert hasattr(result, 'success')
            assert isinstance(result.success, bool)
            
            # Property: If successful, should have data
            if result.success:
                assert result.data is not None
                assert result.error is None
            else:
                # Property: If not successful, should have error
                assert result.error is not None
                assert isinstance(result.error, str)
    
    @given(
        url=valid_urls(),
        method=st.sampled_from(['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
    )
    @settings(max_examples=20)
    def test_safe_request_handles_all_http_methods(self, url, method):
        """Property: safe_request handles all standard HTTP methods."""
        client = SafeHTTPClient()
        
        with patch.object(client.session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = "Success"
            mock_response.json.side_effect = ValueError()  # No JSON
            mock_response.headers = {}
            mock_request.return_value = mock_response
            
            # Property: Should handle any valid HTTP method
            result = client.safe_request(url, method=method)
            assert isinstance(result, NetworkResponse)
            
            # Property: Should call request with correct method
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[0][0] == method.upper()
    
    @given(
        url=valid_urls(),
        status_code=st.integers(min_value=200, max_value=299)
    )
    @settings(max_examples=20)
    def test_safe_request_success_for_2xx_status_codes(self, url, status_code):
        """Property: safe_request returns success=True for 2xx status codes."""
        client = SafeHTTPClient()
        
        with patch.object(client.session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = status_code
            mock_response.text = "Success"
            mock_response.json.side_effect = ValueError()
            mock_response.headers = {}
            mock_response.raise_for_status = Mock()  # Don't raise for 2xx
            mock_request.return_value = mock_response
            
            result = client.safe_request(url)
            
            # Property: Should be successful for 2xx codes
            assert result.success is True
            assert result.status_code == status_code
            assert result.error is None
    
    @given(
        default_timeout=st.floats(min_value=0.1, max_value=60.0)
    )
    @settings(max_examples=10)
    def test_safe_request_uses_default_timeout_when_not_specified(self, default_timeout):
        """Property: safe_request uses default timeout when not specified."""
        client = SafeHTTPClient(default_timeout=default_timeout)
        
        with patch.object(client.session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = "Success"
            mock_response.json.side_effect = ValueError()
            mock_response.headers = {}
            mock_request.return_value = mock_response
            
            client.safe_request('https://example.com')
            
            # Property: Should use default timeout
            call_kwargs = mock_request.call_args[1]
            assert call_kwargs['timeout'] == default_timeout
    
    @given(
        url=valid_urls(),
        custom_timeout=st.floats(min_value=0.1, max_value=60.0)
    )
    @settings(max_examples=10)
    def test_safe_request_uses_custom_timeout_when_specified(self, url, custom_timeout):
        """Property: safe_request uses custom timeout when specified."""
        client = SafeHTTPClient()
        
        with patch.object(client.session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = "Success"
            mock_response.json.side_effect = ValueError()
            mock_response.headers = {}
            mock_request.return_value = mock_response
            
            client.safe_request(url, timeout=custom_timeout)
            
            # Property: Should use custom timeout
            call_kwargs = mock_request.call_args[1]
            assert call_kwargs['timeout'] == custom_timeout


class TestNetworkErrorHandling:
    """
    Property 2: Network error handling
    
    For any network failure condition (timeout, connection error, invalid parameters), 
    the Safe_Network_Module should return a structured NetworkResponse with success=False 
    and descriptive error information.
    
    **Validates: Requirements 1.3, 1.4, 1.6**
    """
    
    @given(url=valid_urls())
    @settings(max_examples=15)
    def test_timeout_errors_return_structured_response(self, url):
        """Property: Timeout errors return NetworkResponse with success=False."""
        client = SafeHTTPClient()
        
        with patch.object(client.session, 'request') as mock_request:
            mock_request.side_effect = Timeout("Request timed out")
            
            result = client.safe_request(url)
            
            # Property: Should return NetworkResponse
            assert isinstance(result, NetworkResponse)
            
            # Property: Should indicate failure
            assert result.success is False
            
            # Property: Should have descriptive error message
            assert result.error is not None
            assert isinstance(result.error, str)
            assert len(result.error) > 0
            assert 'timeout' in result.error.lower() or 'timed out' in result.error.lower()
    
    @given(url=valid_urls())
    @settings(max_examples=15)
    def test_connection_errors_return_structured_response(self, url):
        """Property: Connection errors return NetworkResponse with success=False."""
        client = SafeHTTPClient()
        
        with patch.object(client.session, 'request') as mock_request:
            mock_request.side_effect = ConnectionError("Failed to connect")
            
            result = client.safe_request(url)
            
            # Property: Should return NetworkResponse
            assert isinstance(result, NetworkResponse)
            
            # Property: Should indicate failure
            assert result.success is False
            
            # Property: Should have descriptive error message
            assert result.error is not None
            assert 'connection' in result.error.lower() or 'connect' in result.error.lower()
    
    @given(
        url=valid_urls(),
        status_code=st.sampled_from([400, 401, 403, 404, 500, 502, 503])
    )
    @settings(max_examples=20)
    def test_http_errors_return_structured_response(self, url, status_code):
        """Property: HTTP errors return NetworkResponse with status code and error."""
        client = SafeHTTPClient()
        
        with patch.object(client.session, 'request') as mock_request:
            mock_response = Mock()
            mock_response.status_code = status_code
            http_error = HTTPError()
            http_error.response = mock_response
            mock_request.side_effect = http_error
            
            result = client.safe_request(url)
            
            # Property: Should return NetworkResponse
            assert isinstance(result, NetworkResponse)
            
            # Property: Should indicate failure
            assert result.success is False
            
            # Property: Should include status code
            assert result.status_code == status_code
            
            # Property: Should have descriptive error message
            assert result.error is not None
            assert isinstance(result.error, str)
    
    @given(url=invalid_urls())
    @settings(max_examples=15)
    def test_invalid_url_returns_structured_response(self, url):
        """Property: Invalid URLs return NetworkResponse with success=False."""
        client = SafeHTTPClient()
        
        # Handle None case
        if url is None:
            url = None
        
        result = client.safe_request(url)
        
        # Property: Should return NetworkResponse
        assert isinstance(result, NetworkResponse)
        
        # Property: Should indicate failure
        assert result.success is False
        
        # Property: Should have descriptive error message
        assert result.error is not None
        # Error message should be descriptive (not empty) and indicate a problem
        assert len(result.error) > 0
        assert isinstance(result.error, str)
    
    @given(
        url=st.just('https://example.com'),
        timeout=st.floats(max_value=0.0)
    )
    @settings(max_examples=15)
    def test_invalid_timeout_returns_structured_response(self, url, timeout):
        """Property: Invalid timeout values return NetworkResponse with success=False."""
        client = SafeHTTPClient()
        
        result = client.safe_request(url, timeout=timeout)
        
        # Property: Should return NetworkResponse
        assert isinstance(result, NetworkResponse)
        
        # Property: Should indicate failure
        assert result.success is False
        
        # Property: Should have descriptive error message
        assert result.error is not None
        assert 'timeout' in result.error.lower() or 'invalid' in result.error.lower()
    
    @given(url=valid_urls())
    @settings(max_examples=15)
    def test_too_many_redirects_returns_structured_response(self, url):
        """Property: Too many redirects return NetworkResponse with success=False."""
        client = SafeHTTPClient()
        
        with patch.object(client.session, 'request') as mock_request:
            mock_request.side_effect = TooManyRedirects("Too many redirects")
            
            result = client.safe_request(url)
            
            # Property: Should return NetworkResponse
            assert isinstance(result, NetworkResponse)
            
            # Property: Should indicate failure
            assert result.success is False
            
            # Property: Should have descriptive error message
            assert result.error is not None
            assert 'redirect' in result.error.lower()
    
    @given(url=valid_urls())
    @settings(max_examples=15)
    def test_generic_request_exception_returns_structured_response(self, url):
        """Property: Generic request exceptions return NetworkResponse with success=False."""
        client = SafeHTTPClient()
        
        with patch.object(client.session, 'request') as mock_request:
            mock_request.side_effect = RequestException("Generic error")
            
            result = client.safe_request(url)
            
            # Property: Should return NetworkResponse
            assert isinstance(result, NetworkResponse)
            
            # Property: Should indicate failure
            assert result.success is False
            
            # Property: Should have descriptive error message
            assert result.error is not None
            assert isinstance(result.error, str)
            assert len(result.error) > 0
    
    @given(url=valid_urls())
    @settings(max_examples=15)
    def test_unexpected_exceptions_return_structured_response(self, url):
        """Property: Unexpected exceptions return NetworkResponse with success=False."""
        client = SafeHTTPClient()
        
        with patch.object(client.session, 'request') as mock_request:
            mock_request.side_effect = RuntimeError("Unexpected error")
            
            result = client.safe_request(url)
            
            # Property: Should return NetworkResponse
            assert isinstance(result, NetworkResponse)
            
            # Property: Should indicate failure
            assert result.success is False
            
            # Property: Should have descriptive error message
            assert result.error is not None
            assert 'error' in result.error.lower()
    
    @given(
        url=valid_urls(),
        exception_type=st.sampled_from([
            Timeout, ConnectionError, HTTPError, TooManyRedirects, RequestException
        ])
    )
    @settings(max_examples=20)
    def test_all_network_exceptions_never_propagate(self, url, exception_type):
        """Property: No network exceptions propagate to caller."""
        client = SafeHTTPClient()
        
        with patch.object(client.session, 'request') as mock_request:
            if exception_type == HTTPError:
                mock_response = Mock()
                mock_response.status_code = 500
                error = exception_type()
                error.response = mock_response
                mock_request.side_effect = error
            else:
                mock_request.side_effect = exception_type("Error")
            
            # Property: Should not raise any exception
            try:
                result = client.safe_request(url)
                # Property: Should return NetworkResponse
                assert isinstance(result, NetworkResponse)
                assert result.success is False
            except Exception as e:
                pytest.fail(f"Exception should not propagate: {type(e).__name__}: {e}")
