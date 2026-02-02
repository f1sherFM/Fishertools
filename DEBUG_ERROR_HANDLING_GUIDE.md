# Руководство по обработке ошибок в debug_step_by_step

## Обзор

Начиная с версии 0.4.6, декоратор `debug_step_by_step` поддерживает гибкую обработку ошибок через callback функцию `on_error`. Это позволяет:

- Перехватывать и обрабатывать ошибки без прерывания выполнения
- Логировать ошибки для анализа
- Выборочно обрабатывать определенные типы ошибок
- Восстанавливаться после ошибок в отладочном режиме

## Проблема (до v0.4.6)

**Старое поведение:**
```python
@debug_step_by_step
def divide(a, b):
    return a / b

divide(10, 0)  # ❌ Выбрасывает ZeroDivisionError
```

Декоратор логировал ошибку, но затем всё равно выбрасывал её дальше. Это не давало возможности:
- Продолжить выполнение после ошибки
- Обработать ошибку специальным образом
- Собрать статистику по ошибкам

## Решение (v0.4.6+)

**Новое поведение с `on_error`:**
```python
def handle_error(e):
    print(f"Обработана ошибка: {e}")
    return True  # Ошибка обработана

@debug_step_by_step(on_error=handle_error)
def divide(a, b):
    return a / b

result = divide(10, 0)  # ✅ Возвращает None, не выбрасывает ошибку
print(result)  # None
```

## Базовое использование

### 1. Обработка всех ошибок

```python
from fishertools.debug import debug_step_by_step

def handle_all_errors(e):
    """Обрабатывает все ошибки."""
    print(f"🔧 Обработана ошибка: {type(e).__name__}: {e}")
    return True  # True = ошибка обработана

@debug_step_by_step(on_error=handle_all_errors)
def risky_operation(x):
    if x < 0:
        raise ValueError("Отрицательное значение")
    return 100 / x

# Все ошибки будут обработаны
result1 = risky_operation(-5)  # ValueError обработана
result2 = risky_operation(0)   # ZeroDivisionError обработана
result3 = risky_operation(10)  # Успешно: 10.0

print(result1)  # None (ошибка обработана)
print(result2)  # None (ошибка обработана)
print(result3)  # 10.0 (успех)
```

### 2. Выборочная обработка ошибок

```python
def handle_only_value_errors(e):
    """Обрабатывает только ValueError, остальные пробрасывает."""
    if isinstance(e, ValueError):
        print(f"✅ ValueError обработана: {e}")
        return True  # Обработана
    return False  # Не обработана, будет выброшена

@debug_step_by_step(on_error=handle_only_value_errors)
def validate_and_process(value):
    if value < 0:
        raise ValueError("Значение должно быть положительным")
    if value == 0:
        raise ZeroDivisionError("Деление на ноль")
    return 100 / value

# ValueError будет обработана
result1 = validate_and_process(-5)
print(result1)  # None

# ZeroDivisionError будет выброшена
try:
    result2 = validate_and_process(0)
except ZeroDivisionError as e:
    print(f"❌ Не обработана: {e}")
```

### 3. Логирование ошибок

```python
error_log = []

def log_errors(e):
    """Логирует ошибки для последующего анализа."""
    error_log.append({
        'type': type(e).__name__,
        'message': str(e),
        'timestamp': datetime.now()
    })
    print(f"📝 Залогирована ошибка: {type(e).__name__}")
    return True  # Обработана

@debug_step_by_step(on_error=log_errors)
def process_batch(items):
    results = []
    for item in items:
        result = 100 / item  # Может вызвать ZeroDivisionError
        results.append(result)
    return results

# Обрабатываем batch с ошибками
items = [10, 5, 0, 2, 0, 1]
process_batch(items)

# Анализируем логи
print(f"Всего ошибок: {len(error_log)}")
for error in error_log:
    print(f"  - {error['type']}: {error['message']}")
```

## Продвинутое использование

### 4. Счетчик ошибок с лимитом

```python
class ErrorCounter:
    def __init__(self, max_errors=3):
        self.count = 0
        self.max_errors = max_errors
    
    def handle(self, e):
        self.count += 1
        print(f"⚠️ Ошибка #{self.count}: {e}")
        
        if self.count >= self.max_errors:
            print(f"❌ Достигнут лимит ошибок ({self.max_errors})")
            return False  # Не обрабатывать, выбросить
        
        return True  # Обработать

counter = ErrorCounter(max_errors=3)

@debug_step_by_step(on_error=counter.handle)
def unreliable_operation(x):
    if x % 2 == 0:
        raise ValueError(f"Четное число: {x}")
    return x * 2

# Первые 3 ошибки обработаются
for i in range(10):
    try:
        result = unreliable_operation(i)
        print(f"✅ {i} -> {result}")
    except ValueError as e:
        print(f"❌ Выброшена: {e}")
        break
```

### 5. Retry механизм

```python
class RetryHandler:
    def __init__(self, max_retries=3):
        self.retries = {}
        self.max_retries = max_retries
    
    def handle(self, e):
        error_type = type(e).__name__
        self.retries[error_type] = self.retries.get(error_type, 0) + 1
        
        if self.retries[error_type] <= self.max_retries:
            print(f"🔄 Retry {self.retries[error_type]}/{self.max_retries} для {error_type}")
            return True  # Обработать и продолжить
        
        print(f"❌ Превышен лимит retry для {error_type}")
        return False  # Выбросить

retry_handler = RetryHandler(max_retries=2)

@debug_step_by_step(on_error=retry_handler.handle)
def flaky_api_call(endpoint):
    import random
    if random.random() < 0.7:  # 70% вероятность ошибки
        raise ConnectionError("API недоступен")
    return f"Данные из {endpoint}"
```

### 6. Контекстная обработка с fallback значениями

```python
def handle_with_fallback(e):
    """Возвращает fallback значения для разных типов ошибок."""
    fallbacks = {
        'ZeroDivisionError': 0,
        'ValueError': -1,
        'KeyError': None,
    }
    
    error_type = type(e).__name__
    if error_type in fallbacks:
        print(f"🔄 Используется fallback для {error_type}: {fallbacks[error_type]}")
        # Примечание: декоратор возвращает None, но можно логировать fallback
        return True
    
    return False  # Неизвестная ошибка - выбросить

@debug_step_by_step(on_error=handle_with_fallback)
def calculate(operation, a, b):
    if operation == 'divide':
        return a / b
    elif operation == 'subtract':
        if a < b:
            raise ValueError("Результат отрицательный")
        return a - b
    else:
        raise KeyError(f"Неизвестная операция: {operation}")
```

## Обратная совместимость

Старый код продолжает работать без изменений:

```python
# Старый способ (без on_error) - всё ещё работает
@debug_step_by_step
def old_function(x):
    return 10 / x

# Ошибки выбрасываются как раньше
try:
    old_function(0)
except ZeroDivisionError:
    print("Ошибка выброшена как обычно")
```

## Сигнатура callback функции

```python
def on_error(exception: Exception) -> bool:
    """
    Callback для обработки ошибок.
    
    Args:
        exception: Перехваченное исключение
    
    Returns:
        bool: True если ошибка обработана (не выбрасывать)
              False или None если ошибку нужно выбросить
    
    Примечание:
        Если callback сам выбрасывает исключение, оно логируется,
        но выбрасывается оригинальное исключение.
    """
    pass
```

## Возвращаемое значение

При обработке ошибки декоратор возвращает `None`:

```python
def handle_errors(e):
    return True

@debug_step_by_step(on_error=handle_errors)
def divide(a, b):
    return a / b

result = divide(10, 0)
print(result)  # None (ошибка обработана)

result = divide(10, 2)
print(result)  # 5.0 (успешное выполнение)
```

## Примеры из реальной жизни

### Пример 1: Парсинг данных с ошибками

```python
def skip_invalid_data(e):
    """Пропускает невалидные данные при парсинге."""
    if isinstance(e, (ValueError, KeyError)):
        print(f"⚠️ Пропущена невалидная запись: {e}")
        return True
    return False

@debug_step_by_step(on_error=skip_invalid_data)
def parse_record(record):
    # Парсинг может вызвать ValueError или KeyError
    age = int(record['age'])
    name = record['name']
    if age < 0:
        raise ValueError("Отрицательный возраст")
    return {'name': name, 'age': age}

records = [
    {'name': 'Alice', 'age': '30'},
    {'name': 'Bob', 'age': 'invalid'},  # ValueError
    {'age': '25'},  # KeyError (нет name)
    {'name': 'Charlie', 'age': '35'},
]

valid_records = []
for record in records:
    result = parse_record(record)
    if result is not None:
        valid_records.append(result)

print(f"Обработано {len(valid_records)} из {len(records)} записей")
```

### Пример 2: Тестирование с мягкими ошибками

```python
test_results = {'passed': 0, 'failed': 0}

def record_test_failure(e):
    """Записывает провалы тестов без остановки."""
    test_results['failed'] += 1
    print(f"❌ Тест провален: {e}")
    return True  # Продолжить тестирование

@debug_step_by_step(on_error=record_test_failure)
def run_test(test_name, test_func):
    print(f"\n🧪 Запуск теста: {test_name}")
    test_func()
    test_results['passed'] += 1
    print(f"✅ Тест пройден: {test_name}")

# Запуск тестов
def test_addition():
    assert 2 + 2 == 4

def test_division():
    assert 10 / 0 == 0  # Провалится

def test_string():
    assert "hello".upper() == "HELLO"

run_test("Addition", test_addition)
run_test("Division", test_division)
run_test("String", test_string)

print(f"\n📊 Результаты: {test_results['passed']} пройдено, {test_results['failed']} провалено")
```

## Лучшие практики

### ✅ DO: Используйте для отладки и разработки

```python
# Хорошо: для отладки в development
@debug_step_by_step(on_error=log_and_continue)
def experimental_feature(data):
    # Новый код, который может содержать ошибки
    pass
```

### ✅ DO: Логируйте обработанные ошибки

```python
def handle_with_logging(e):
    logger.error(f"Обработана ошибка: {e}", exc_info=True)
    return True
```

### ✅ DO: Будьте избирательны в обработке

```python
def handle_expected_errors(e):
    # Обрабатывайте только ожидаемые ошибки
    if isinstance(e, (ValueError, KeyError)):
        return True
    return False  # Неожиданные ошибки выбрасываются
```

### ❌ DON'T: Не скрывайте критические ошибки

```python
# Плохо: скрывает все ошибки
def hide_all_errors(e):
    return True  # Опасно!

# Хорошо: обрабатывайте только некритичные
def handle_safe_errors(e):
    if isinstance(e, (ValueError, KeyError)):
        return True
    return False  # Критичные ошибки выбрасываются
```

### ❌ DON'T: Не используйте в production коде

```python
# Плохо: debug_step_by_step в production
@debug_step_by_step(on_error=handle_errors)
def production_api_endpoint(request):
    pass

# Хорошо: используйте только для отладки
if DEBUG:
    @debug_step_by_step(on_error=handle_errors)
    def api_endpoint(request):
        pass
else:
    def api_endpoint(request):
        pass
```

## Заключение

Новая возможность обработки ошибок в `debug_step_by_step` делает отладку более гибкой:

- ✅ Перехват и обработка ошибок без прерывания
- ✅ Выборочная обработка по типу ошибки
- ✅ Логирование для анализа
- ✅ 100% обратная совместимость
- ✅ Простой и понятный API

Используйте эту возможность для улучшения процесса отладки и разработки! 🚀
