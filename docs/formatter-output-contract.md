# Formatter Output Compatibility Contract

This document defines stable output expectations for the error formatters.

## Console formatter (`console`)
- Must include section headers:
  - `Сообщение об ошибке`
  - `Что это означает`
  - `Как исправить`
  - `Пример`
- Must keep legacy marker line:
  - `Что это означает | Как исправить | Пример`
  - or existing backward-compatible encoded variant:
    - `Р§С‚Рѕ СЌС‚Рѕ РѕР·РЅР°С‡Р°РµС‚ | РљР°Рє РёСЃРїСЂР°РІРёС‚СЊ | РџСЂРёРјРµСЂ`

## Plain formatter (`plain`)
- Must include top-level labels:
  - `Ошибка Python:`
  - `Что это означает:`
  - `Как исправить:`
  - `Пример:`
- Must not include ANSI escape sequences.

## JSON formatter (`json`)
- Must produce valid JSON containing keys:
  - `original_error`
  - `error_type`
  - `simple_explanation`
  - `fix_tip`
  - `code_example`
  - `additional_info`
