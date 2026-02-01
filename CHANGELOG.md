# Changelog

Все важные изменения в проекте Fishertools будут документированы в этом файле.

## [0.4.3.3] - 2026-02-01

### 🔧 Code Quality Improvements

**Масштабная оптимизация кода - устранены дублирующиеся литералы и снижена когнитивная сложность**

#### 📝 Константы вместо дублирующихся литералов:
- **fishertools/documentation/generator.py** - константы для имен файлов (INDEX_RST, CONF_PY, etc.)
- **fishertools/documentation/visual.py** - константы для HTML тегов (DIV_CLOSE, DIV_OPEN)
- **fishertools/examples/logger_example.py** - константы для имен лог-файлов
- **fishertools/examples/repository.py** - полный набор констант для концепций и паттернов кода
- **fishertools/learn/repl/command_handler.py** - константы для сообщений пользователю
- **fishertools/learn/repl/command_parser.py** - константы для сообщений об ошибках

#### 🧠 Рефакторинг сложных функций:
- **fishertools/examples/repository.py** - разбита анонимная функция с когнитивной сложностью 46 на множество специализированных методов
- **fishertools/learn/repl/engine.py** - функция `_handle_command` (сложность 65→15) разбита на 15 специализированных методов

#### 🐛 Исправлены синтаксические ошибки:
- **fishertools/documentation/api.py** - исправлена индентация и удален дублирующийся код
- **fishertools/readme_transformer.py** - исправлена индентация в блоке try-except
- **fishertools/visualization/formatters.py** - удален дублирующийся код функции

Код стал значительно более читаемым, поддерживаемым и менее подверженным ошибкам.

## [0.4.3.2] - 2026-02-01

### 🐛 Bug Fixes

**Исправлена ошибка индентации в readme_transformer.py**

#### Исправленные файлы:
- `fishertools/readme_transformer.py` - исправлена индентация в методе write_transformed_readme

Это исправление устраняет IndentationError в блоке try-except, который препятствовал корректной работе трансформера README.

## [0.4.3.1] - 2026-02-01

### 🐛 Bug Fixes

**Исправлены синтаксические ошибки в модуле documentation**

#### Исправленные файлы:
- `fishertools/documentation/code_validator.py` - удален дублирующийся код метода
- `fishertools/documentation/examples_manager.py` - добавлен отсутствующий блок except
- `fishertools/documentation/generator.py` - исправлена индентация в методе _generate_readthedocs_config

Эти исправления устраняют ошибки IndentationError и SyntaxError, которые препятствовали корректной работе модуля документации.

## [Unreleased] - 2026-01-30

### 🔧 Code Quality Refactoring (v0.4.3)

**Исправлен "spaghetti code" - библиотека стала более человечной!**

#### ✅ Реализован safe_string_operations
- **Было:** Stub-метод с `pass` (ничего не делал)
- **Стало:** Полноценный модуль с 6 функциями:
  - `safe_strip()` - безопасный strip с обработкой None
  - `safe_split()` - безопасный split с обработкой None
  - `safe_join()` - безопасный join с пропуском None
  - `safe_format()` - безопасное форматирование строк
  - `safe_lower()` / `safe_upper()` - безопасное изменение регистра

#### 🔢 Исправлена математика в safe_divide
- **Было:** `safe_divide(10, 0) = 0` (математически НЕПРАВИЛЬНО!)
- **Стало:** `safe_divide(10, 0) = None` (честно: результат неопределен)
- Можно явно указать default: `safe_divide(10, 0, default=0)`

#### 🐍 Упрощена обработка ошибок (Pythonic подход)
- Убраны избыточные проверки типов (было 50+ строк, стало 10)
- Используется EAFP (Easier to Ask Forgiveness than Permission)
- Проверяются только явно неправильные типы (None, bool, complex)
- Код стал проще и понятнее

#### 📦 Упрощены функции коллекций
- `safe_max()`, `safe_min()`, `safe_sum()` - с 30+ строк до 5 строк
- `safe_get()` - универсальный getter для любых коллекций
- Меньше кода, больше читаемости

#### 📊 Результаты
- ✅ Все 82 теста проходят
- 📉 -150 строк избыточного кода
- 📈 +6 новых полезных функций
- 🎯 100% математическая корректность

#### 📝 Документация
- Добавлен `REFACTORING_SUMMARY.md` с подробным описанием изменений
- Добавлен `examples/refactored_safe_usage.py` с примерами использования
- Обновлены docstrings с честными примерами

## [0.4.1] - 2026-01-29

### 🎨 Phase 1: Core Modules (Visualization, Validation, Debug)

**Три новых мощных модуля для разработки и обучения:**

#### 📊 Visualization Module
- `visualize()` - визуализация структур данных в понятном формате
- Поддержка списков, словарей, вложенных структур
- Ограничение глубины и количества элементов
- Форматирование с индексами и ключами

#### ✅ Validation Module
- `@validate_types` - проверка типов через type hints
- `validate_email()`, `validate_url()` - валидация данных
- `validate_number()`, `validate_string()` - проверка значений
- `validate_structure()` - валидация структуры данных
- `ValidationError` - исключение для ошибок валидации

#### 🔍 Debug Module
- `@debug_step_by_step` - пошаговое выполнение функций
- `@trace` - трассировка вызовов функций
- `set_breakpoint()` - точки останова для отладки
- Визуализация стека вызовов и значений переменных

#### 📈 Тестирование
- 65+ новых тестов для всех модулей
- 90%+ покрытие кода
- Property-based тесты с Hypothesis

---

## [0.4.0] - 2026-01-29

### 🎓 Knowledge Engine Interactive REPL

**Полнофункциональный интерактивный REPL для обучения Python:**

#### 🎯 Основные компоненты
- **REPLEngine** - главный интерактивный цикл с управлением состоянием
- **CommandParser** - парсинг пользовательского ввода с поддержкой команд и тем
- **CodeSandbox** - безопасное выполнение кода с ограничениями и таймаутом
- **SessionManager** - отслеживание прогресса и сохранение состояния сессии
- **CommandHandler** - обработка всех команд REPL
- **TopicDisplay** - форматирование и отображение тем

#### 📚 Функциональность
- **Просмотр тем:** /list, /search, /random, /categories, /category, /path
- **Навигация:** /next, /prev, /goto, /related
- **Выполнение кода:** /run, /modify, /exit_edit
- **Отслеживание прогресса:** /progress, /stats, /reset_progress
- **Управление сессией:** /history, /clear_history, /session
- **Справка:** /help, /commands, /about, /hint, /tip, /tips

#### 🔒 Безопасность
- Ограничение доступа к опасным операциям (file I/O, imports)
- Таймаут выполнения кода (5 секунд по умолчанию)
- Валидация кода перед выполнением
