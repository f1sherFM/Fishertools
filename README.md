**Инструменты, которые делают Python удобнее и безопаснее для новичков**
```bash
pip install fishertools
```
| Задача | Что вызвать |
|--------|-------------|
| Объяснить ошибку | explain_error(e) |
| Красиво показать traceback | explain_error(e) |
| Безопасно читать файл | safe_read_file(path) |
## Для кого эта библиотека

- Ты только начал изучать Python
- Сообщения об ошибках кажутся страшными и непонятными
- Хочешь, чтобы ошибки объяснялись на нормальном русском с примерами
# Fishertools

**Инструменты, которые делают Python удобнее и безопаснее для новичков**

Fishertools - это Python библиотека, созданная специально для начинающих разработчиков. Она предоставляет понятные объяснения ошибок, безопасные утилиты и обучающие инструменты.

## 🎯 Основные возможности

### 🚨 Объяснение ошибок Python
Получайте понятные объяснения ошибок на русском языке с советами по исправлению:

```python
from fishertools import explain_error

try:
    numbers = [1, 2, 3]
    print(numbers[10])
except Exception as e:
    explain_error(e)
```

**Вывод:**
```
🚨 Ошибка Python: IndexError

═══ Сообщение об ошибке ═══
  list index out of range

═══ Что это означает ═══
  Вы пытаетесь получить элемент списка по индексу, которого не существует.
  Индексы в Python начинаются с 0, а максимальный индекс равен длине списка минус 1.

═══ Как исправить ═══
  Проверьте длину списка перед обращением к элементу или используйте
  безопасные методы получения элементов.

═══ Пример ═══
┌─ Правильный код ─┐
    numbers = [1, 2, 3]
    if len(numbers) > 10:
        print(numbers[10])
    else:
        print("Индекс слишком большой!")
└───────────────────┘
```

### 🛡️ Безопасные утилиты
Функции, которые предотвращают типичные ошибки новичков:

```python
from fishertools.safe import safe_get, safe_divide, safe_read_file

# Безопасное получение элемента
numbers = [1, 2, 3]
result = safe_get(numbers, 10, "не найден")  # "не найден"

# Безопасное деление
result = safe_divide(10, 0, 0)  # 0 вместо ошибки

# Безопасное чтение файла
content = safe_read_file("file.txt", default="файл не найден")
```

### 📚 Обучающие инструменты
Изучайте Python на примерах и лучших практиках:

```python
from fishertools.learn import show_best_practice, generate_example

# Показать лучшие практики
show_best_practice("variables")

# Сгенерировать пример кода
example = generate_example("functions")
print(example)
```

### 🎓 Объяснение Python концепций
Получайте структурированные объяснения Python тем с примерами:

```python
from fishertools.learn import explain

# Получить объяснение темы
explanation = explain("list")
print(explanation["description"])
print(explanation["when_to_use"])
print(explanation["example"])
```

### 🔧 Готовые паттерны
Используйте готовые шаблоны для типичных задач:

```python
from fishertools.patterns import simple_menu, JSONStorage, SimpleLogger, SimpleCLI

# Интерактивное меню
simple_menu({
    "Опция 1": lambda: print("Выбрана опция 1"),
    "Опция 2": lambda: print("Выбрана опция 2")
})

# Сохранение данных в JSON
storage = JSONStorage("data.json")
storage.save({"name": "Alice", "age": 30})

# Логирование
logger = SimpleLogger("app.log")
logger.info("Приложение запущено")

# CLI приложение
cli = SimpleCLI("myapp", "Мое приложение")
@cli.command("greet", "Поздравить пользователя")
def greet(name):
    print(f"Привет, {name}!")
cli.run()
```

### 🔄 Обратная совместимость
Все полезные функции из предыдущих версий сохранены:

```python
from fishertools.legacy import hash_string, generate_password, QuickConfig

# Старые функции работают как прежде
password = generate_password(12)
hash_value = hash_string("my_string")
config = QuickConfig({"debug": True})
```

## 📦 Установка

```bash
pip install fishertools
```

Или из исходников:
```bash
git clone https://github.com/f1sherFM/My_1st_library_python.git
cd My_1st_library_python
pip install -e .
```

## 🚀 Быстрый старт

```python
from fishertools import explain_error

# Основная функция - объяснение ошибок
try:
    result = 10 / 0
except Exception as e:
    explain_error(e)

# Безопасные утилиты
from fishertools.safe import safe_get, safe_divide
safe_result = safe_get([1, 2, 3], 5, "default")

# Обучающие инструменты  
from fishertools.learn import show_best_practice
show_best_practice("functions")
```

## 📚 Обучающие инструменты v0.3.1

### Объяснение Python концепций с помощью explain()

Функция `explain()` предоставляет структурированные объяснения для 30+ Python тем с примерами кода:

```python
from fishertools.learn import explain

# Получить объяснение темы
explanation = explain("list")
print(explanation["description"])    # Что это такое
print(explanation["when_to_use"])    # Когда использовать
print(explanation["example"])        # Пример кода
```

**Поддерживаемые темы:**

- **Типы данных**: int, float, str, bool, list, tuple, set, dict
- **Управляющие конструкции**: if, for, while, break, continue
- **Функции**: function, return, lambda, *args, **kwargs
- **Обработка ошибок**: try, except, finally, raise
- **Работа с файлами**: open, read, write, with

**Пример использования:**

```python
from fishertools.learn import explain

# Объяснение списков
list_info = explain("list")
print(list_info)
# {
#     "description": "Упорядоченная коллекция элементов",
#     "when_to_use": "Используйте, когда нужно хранить несколько элементов в порядке",
#     "example": "items = [1, 2, 3]\nitems.append(4)\nprint(items[0])"
# }

# Объяснение цикла for
for_info = explain("for")
print(for_info["example"])
```

### Готовые паттерны для типичных задач

Модуль `fishertools.patterns` предоставляет готовые шаблоны для типичных программных задач.

#### 1. simple_menu() - Интерактивное меню

Создавайте интерактивные консольные меню без лишнего кода:

```python
from fishertools.patterns import simple_menu

def show_greeting():
    print("Привет! 👋")

def show_goodbye():
    print("До свидания! 👋")

def show_help():
    print("Это справка по приложению")

simple_menu({
    "Поздравить": show_greeting,
    "Попрощаться": show_goodbye,
    "Справка": show_help
})
```

**Особенности:**
- Автоматическая нумерация опций
- Обработка некорректного ввода
- Команды "quit" и "exit" для выхода
- Повторный запрос при ошибке

#### 2. JSONStorage - Сохранение данных

Сохраняйте и загружайте данные в JSON без обработки ошибок:

```python
from fishertools.patterns import JSONStorage

# Создание хранилища
storage = JSONStorage("users.json")

# Сохранение данных
users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
]
storage.save(users)

# Загрузка данных
loaded_users = storage.load()
print(loaded_users)

# Проверка существования файла
if storage.exists():
    print("Файл существует")
```

**Особенности:**
- Автоматическое создание директорий
- Автоматическое создание файла при сохранении
- Обработка ошибок файловых операций
- Простой API для сохранения/загрузки

#### 3. SimpleLogger - Логирование

Добавляйте логирование в приложение с временными метками:

```python
from fishertools.patterns import SimpleLogger

# Создание логгера
logger = SimpleLogger("app.log")

# Логирование сообщений
logger.info("Приложение запущено")
logger.warning("Низкий уровень памяти")
logger.error("Ошибка подключения")
```

**Формат логов:**
```
[2024-01-15 10:30:45] [INFO] Приложение запущено
[2024-01-15 10:30:46] [WARNING] Низкий уровень памяти
[2024-01-15 10:30:47] [ERROR] Ошибка подключения
```

**Особенности:**
- Автоматические временные метки
- Три уровня логирования: INFO, WARNING, ERROR
- Автоматическое создание файла логов
- Добавление к существующему файлу

#### 4. SimpleCLI - Командная строка

Создавайте CLI приложения с минимальным кодом:

```python
from fishertools.patterns import SimpleCLI

# Создание CLI приложения
cli = SimpleCLI("myapp", "Мое приложение")

# Регистрация команд через декоратор
@cli.command("greet", "Поздравить пользователя")
def greet(name):
    print(f"Привет, {name}!")

@cli.command("add", "Сложить два числа")
def add(a, b):
    result = int(a) + int(b)
    print(f"Результат: {result}")

# Запуск приложения
if __name__ == "__main__":
    cli.run()
```

**Использование:**
```bash
python myapp.py greet Alice
# Привет, Alice!

python myapp.py add 5 3
# Результат: 8

python myapp.py --help
# Показать все доступные команды
```

**Особенности:**
- Регистрация команд через декоратор
- Автоматический парсинг аргументов
- Встроенная справка (--help)
- Обработка неправильных команд

### Примеры использования

Полные примеры использования всех компонентов находятся в директории `fishertools/examples/`:

- `learn_example.py` - Примеры использования explain()
- `menu_example.py` - Примеры simple_menu()
- `storage_example.py` - Примеры JSONStorage
- `logger_example.py` - Примеры SimpleLogger
- `cli_example.py` - Примеры SimpleCLI

Вы можете запустить любой пример:
```bash
python -m fishertools.examples.learn_example
python -m fishertools.examples.menu_example
python -m fishertools.examples.storage_example
python -m fishertools.examples.logger_example
python -m fishertools.examples.cli_example
```

## 📖 Документация

### Поддерживаемые типы ошибок

Fishertools объясняет следующие типы ошибок Python:

- **TypeError** - ошибки типов данных
- **ValueError** - неправильные значения
- **AttributeError** - отсутствующие атрибуты
- **IndexError** - выход за границы списка
- **KeyError** - отсутствующие ключи словаря
- **ImportError** - проблемы с импортом модулей
- **SyntaxError** - синтаксические ошибки

### Безопасные утилиты

- `safe_get(collection, index, default)` - безопасное получение элемента
- `safe_divide(a, b, default)` - деление без ошибки на ноль
- `safe_max(collection, default)` - максимум из коллекции
- `safe_min(collection, default)` - минимум из коллекции
- `safe_sum(collection, default)` - сумма элементов
- `safe_read_file(path, default)` - чтение файла без ошибок

### Обучающие функции

- `show_best_practice(topic)` - показать лучшие практики
- `generate_example(concept)` - сгенерировать пример кода
- `list_available_concepts()` - список доступных концепций
- `list_available_topics()` - список доступных тем

## 🧪 Тестирование

Библиотека покрыта comprehensive тестами:

```bash
# Запуск всех тестов
pytest

# Запуск property-based тестов
pytest -k "property"

# Запуск с покрытием
pytest --cov=fishertools
```

## 🛠️ Разработка

```bash
# Установка для разработки
pip install -e ".[dev]"

# Форматирование кода
black fishertools tests

# Проверка типов
mypy fishertools

# Линтинг
ruff check fishertools
```

## 📋 Требования

- Python 3.8+
- requests >= 2.25.0
- click >= 8.0.0

Для разработки:
- pytest >= 8.0.0
- hypothesis >= 6.0.0 (для property-based тестов)
- black >= 24.0.0
- ruff >= 0.1.0
- mypy >= 1.8.0

## 🤝 Вклад в проект

Мы приветствуем вклад в развитие проекта! Пожалуйста:

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Добавьте тесты для новой функциональности
4. Убедитесь, что все тесты проходят
5. Создайте Pull Request

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 🙏 Благодарности

Спасибо всем, кто помогает делать Python более доступным для новичков!

---

**Fishertools** - потому что каждый заслуживает понятные инструменты для изучения программирования! 🐍✨