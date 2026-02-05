# Internationalization Module

Multilingual support for fishertools error explanations.

## Overview

This module provides multilingual error explanations with automatic language detection and fallback behavior.

## Components

### ErrorTranslator
Translates error messages and explanations to different languages.

### LanguageDetector
Detects system language settings for automatic localization.

## Data Models

- `ErrorExplanation`: Structured error explanation with suggestions

## Supported Languages

- Russian (ru) - Default
- English (en) - Fallback

## Usage

```python
from fishertools.i18n import translate_error, detect_language

# Translate an error to English
try:
    result = 10 / 0
except Exception as e:
    explanation = translate_error(e, lang='en')
    print(explanation)

# Auto-detect system language
system_lang = detect_language()
print(f"System language: {system_lang}")
```

## Implementation Status

- ✅ Module structure created
- ✅ Data models defined
- ⏳ Language detection implementation (Task 7.1)
- ⏳ Error translation implementation (Task 7.2)
