# Network Module

Safe network operations module for fishertools.

## Overview

This module provides safe HTTP request and file download operations with comprehensive error handling, timeouts, and progress tracking.

## Components

### SafeHTTPClient
Safe HTTP client with structured error responses instead of exceptions.

### SafeFileDownloader
File downloader with progress tracking and automatic cleanup on failure.

## Data Models

- `NetworkRequest`: HTTP request parameters
- `NetworkResponse`: Structured response for network operations
- `DownloadProgress`: Download progress information
- `DownloadResponse`: Structured response for download operations

## Usage

```python
from fishertools.network import safe_request, safe_download

# Make a safe HTTP request
response = safe_request("https://api.example.com/data")
if response.success:
    print(response.data)
else:
    print(f"Error: {response.error}")

# Download a file safely
result = safe_download(
    "https://example.com/file.zip",
    "local_file.zip",
    overwrite=True
)
if result.success:
    print(f"Downloaded to: {result.file_path}")
```

## Implementation Status

- ✅ Module structure created
- ✅ Data models defined
- ⏳ HTTP client implementation (Task 2.1)
- ⏳ File downloader implementation (Task 2.4)
