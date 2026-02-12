# Fishertools

РќР°Р±РѕСЂ РїСЂР°РєС‚РёС‡РЅС‹С… РёРЅСЃС‚СЂСѓРјРµРЅС‚РѕРІ РґР»СЏ Р±РµР·РѕРїР°СЃРЅРѕРіРѕ Рё РїРѕРЅСЏС‚РЅРѕРіРѕ Python-РєРѕРґР°.

`Fishertools` РїРѕРјРѕРіР°РµС‚ РїРёСЃР°С‚СЊ СѓСЃС‚РѕР№С‡РёРІС‹Рµ СЃРєСЂРёРїС‚С‹ Рё Р±С‹СЃС‚СЂРµРµ СЂР°Р·Р±РёСЂР°С‚СЊСЃСЏ СЃ РѕС€РёР±РєР°РјРё: Р±РµР·РѕРїР°СЃРЅС‹Рµ РѕРїРµСЂР°С†РёРё СЃ РєРѕР»Р»РµРєС†РёСЏРјРё/С„Р°Р№Р»Р°РјРё, РґСЂСѓР¶РµР»СЋР±РЅС‹Рµ РѕР±СЉСЏСЃРЅРµРЅРёСЏ РёСЃРєР»СЋС‡РµРЅРёР№, СѓС‚РёР»РёС‚С‹ РІР°Р»РёРґР°С†РёРё, РІРёР·СѓР°Р»РёР·Р°С†РёСЏ Рё РѕР±СѓС‡Р°СЋС‰РёРµ РёРЅСЃС‚СЂСѓРјРµРЅС‚С‹.

## Р’РµСЂСЃРёСЏ

**РўРµРєСѓС‰Р°СЏ РІРµСЂСЃРёСЏ: `0.4.0`**

## Documentation

- [Getting Started](docs/getting-started.md)
- [Features](docs/features.md)
- [Installation](docs/installation.md)
- [API Reference](docs/api-reference.md)
- [Examples](docs/examples.md)
- [Limitations](docs/limitations.md)
- [Contributing](docs/contributing.md)

## РЈСЃС‚Р°РЅРѕРІРєР°

```bash
pip install fishertools==0.4.0
```

Р”Р»СЏ СЂР°Р·СЂР°Р±РѕС‚РєРё РёР· СЂРµРїРѕР·РёС‚РѕСЂРёСЏ:

```bash
git clone <YOUR_REPO_URL>
cd My_1st_library_python
pip install -e .
```

## Р‘С‹СЃС‚СЂС‹Р№ СЃС‚Р°СЂС‚

```python
from fishertools import explain_error, safe_get, safe_divide

# Р‘РµР·РѕРїР°СЃРЅС‹Р№ РґРѕСЃС‚СѓРї Рє РєРѕР»Р»РµРєС†РёСЏРј
value = safe_get([10, 20, 30], 10, default=0)
print(value)  # 0

# Р‘РµР·РѕРїР°СЃРЅРѕРµ РґРµР»РµРЅРёРµ
result = safe_divide(10, 0, default=None)
print(result)  # None

# РџРѕРЅСЏС‚РЅРѕРµ РѕР±СЉСЏСЃРЅРµРЅРёРµ РѕС€РёР±РєРё
try:
    int("abc")
except Exception as e:
    explain_error(e, language="ru")
```

## РљР»СЋС‡РµРІС‹Рµ РІРѕР·РјРѕР¶РЅРѕСЃС‚Рё

### 1. РћР±СЉСЏСЃРЅРµРЅРёРµ РѕС€РёР±РѕРє
- `explain_error(e, language='ru' | 'en' | 'auto')`
- `explain_last_error()` РІРЅСѓС‚СЂРё `except`
- `get_explanation(e, format_type='console' | 'plain' | 'json')`

### 2. Р‘РµР·РѕРїР°СЃРЅС‹Рµ СѓС‚РёР»РёС‚С‹ (`safe`)
- РєРѕР»Р»РµРєС†РёРё: `safe_get`, `safe_pop`, `safe_slice`
- РјР°С‚РµРјР°С‚РёРєР°: `safe_divide`, `safe_average`
- СЃС‚СЂРѕРєРё: `safe_format`, `safe_split`, `safe_join`
- С„Р°Р№Р»С‹: `safe_read_file`, `safe_write_file`, `safe_read_json`, `safe_write_json`

### 3. Р’Р°Р»РёРґР°С†РёСЏ Рё РѕС‚Р»Р°РґРєР°
- РґРµРєРѕСЂР°С‚РѕСЂС‹ Рё С…РµР»РїРµСЂС‹ РїСЂРѕРІРµСЂРєРё С‚РёРїРѕРІ
- РёРЅСЃС‚СЂСѓРјРµРЅС‚С‹ РїРѕС€Р°РіРѕРІРѕРіРѕ РґРµР±Р°РіР°
- СѓС‚РёР»РёС‚С‹ С‚СЂР°СЃСЃРёСЂРѕРІРєРё

### 4. Р’РёР·СѓР°Р»РёР·Р°С†РёСЏ
- РІРёР·СѓР°Р»РёР·Р°С†РёСЏ СЃС‚СЂСѓРєС‚СѓСЂ РґР°РЅРЅС‹С…
- РІРёР·СѓР°Р»РёР·Р°С†РёСЏ Р°Р»РіРѕСЂРёС‚РјРѕРІ СЃРѕСЂС‚РёСЂРѕРІРєРё Рё РїРѕРёСЃРєР°

### 5. РћР±СѓС‡Р°СЋС‰РёРµ РјРѕРґСѓР»Рё
- СѓС‚РёР»РёС‚С‹ РґР»СЏ РёРЅС‚РµСЂР°РєС‚РёРІРЅРѕРіРѕ РѕР±СѓС‡РµРЅРёСЏ
- РѕР±СЉСЏСЃРЅРµРЅРёРµ Р±Р°Р·РѕРІС‹С… РєРѕРЅС†РµРїС†РёР№ Python

## Р§Р°СЃС‚С‹Рµ СЃС†РµРЅР°СЂРёРё

### JSON-Р»РѕРіРёСЂРѕРІР°РЅРёРµ РѕС€РёР±РєРё

```python
from fishertools.errors import get_explanation

try:
    data = {"a": 1}
    print(data["b"])
except Exception as e:
    payload = get_explanation(e, format_type="json")
    print(payload)
```

### РљРѕРЅС‚РµРєСЃС‚РЅРѕРµ РѕР±СЉСЏСЃРЅРµРЅРёРµ

```python
from fishertools.errors import explain_error

try:
    arr = [1, 2, 3]
    arr[10]
except Exception as e:
    explain_error(
        e,
        context={
            "operation": "list_access",
            "variable_name": "arr",
            "index": 10,
        },
    )
```

## РЎРѕРІРјРµСЃС‚РёРјРѕСЃС‚СЊ

- Python `>=3.8`
- РџР»Р°С‚С„РѕСЂРјС‹: Linux / macOS / Windows

## РљР°С‡РµСЃС‚РІРѕ

- С€РёСЂРѕРєРѕРµ РїРѕРєСЂС‹С‚РёРµ Р°РІС‚РѕС‚РµСЃС‚Р°РјРё
- property-based С‚РµСЃС‚С‹
- backward compatibility С‚РµСЃС‚С‹

## РЎС‚СЂСѓРєС‚СѓСЂР° РїСЂРѕРµРєС‚Р°

- `fishertools/` вЂ” Р±РёР±Р»РёРѕС‚РµРєР°
- `tests/` вЂ” Р°РІС‚РѕС‚РµСЃС‚С‹
- `docs/` вЂ” РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ

## Р Р°Р·СЂР°Р±РѕС‚РєР°

Р—Р°РїСѓСЃРє С‚РµСЃС‚РѕРІ:

```bash
pytest -q -p no:cacheprovider
```

Р›РёРЅС‚РёРЅРі:

```bash
ruff check .
```

## Р РµР»РёР· `0.4.0`

Р’ СЌС‚РѕРј СЂРµР»РёР·Рµ:
- Р·Р°С„РёРєСЃРёСЂРѕРІР°РЅР° РІРµСЂСЃРёСЏ РїР°РєРµС‚Р° `0.4.0`
- РѕР±РЅРѕРІР»РµРЅР° РґРѕРєСѓРјРµРЅС‚Р°С†РёСЏ Рё README
- СЃРёРЅС…СЂРѕРЅРёР·РёСЂРѕРІР°РЅС‹ РІРµСЂСЃРёРѕРЅРЅС‹Рµ СѓРїРѕРјРёРЅР°РЅРёСЏ РїРѕ РїСЂРѕРµРєС‚Сѓ

## Р›РёС†РµРЅР·РёСЏ

MIT
