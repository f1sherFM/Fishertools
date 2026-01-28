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

### Примеры других ошибок

#### NameError: имя не определено

```python
from fishertools import explain_error

try:
    print(result)
except Exception as e:
    explain_error(e)
```
### Возможный вывод:
```
🚨 Ошибка Python: NameError

═══ Сообщение об ошибке ═══
  name 'result' is not defined

═══ Что это означает ═══
  В коде используется переменная или имя, которое ещё не было объявлено.
  Чаще всего это опечатка или переменная создана в другом месте.

═══ Как исправить ═══
  Проверьте, правильно ли написано имя переменной и объявлена ли она
  до использования.

═══ Пример ═══
┌─ Правильный код ─┐
    result = 42
    print(result)
```

TypeError: нельзя сложить число и строку
```python
from fishertools import explain_error

try:
    age = 18
    message = "Мне " + age + " лет"
except Exception as e:
    explain_error(e)
```
### Возможный вывод:
```
🚨 Ошибка Python: TypeError

═══ Сообщение об ошибке ═══
  can only concatenate str (not "int") to str

═══ Что это означает ═══
  Вы пытаетесь выполнить операцию над значениями разных типов
  (например, сложить строку и число).

═══ Как исправить ═══
  Приведите значение к нужному типу или используйте форматирование строки.

═══ Пример ═══
┌─ Правильный код ─┐
    age = 18
    message = f"Мне {age} лет"
    print(message)
└───────────────────┘
```


### 🛡️ Безопасные утилиты
Функции, которые предотвращают типичные ошибки новичков:

```python
from fishertools.safe import safe_get, safe_divide, safe_read_file, ensure_dir, get_file_hash, read_last_lines

# Безопасное получение элемента
numbers = [1, 2, 3]
result = safe_get(numbers, 10, "не найден")  # "не найден"

# Безопасное деление
result = safe_divide(10, 0, 0)  # 0 вместо ошибки

# Безопасное чтение файла
content = safe_read_file("file.txt", default="файл не найден")

# Рекурсивное создание директорий
path = ensure_dir("./data/nested/directory")  # Создаст все промежуточные папки

# Вычисление хэша файла
file_hash = get_file_hash("data.txt")  # SHA256 по умолчанию
md5_hash = get_file_hash("data.txt", algorithm='md5')

# Чтение последних строк файла
last_lines = read_last_lines("log.txt", n=10)  # Последние 10 строк
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

### Текущий статус версии

⚠️ **Важно:** Версия 0.3.1 ещё не опубликована на PyPI. Последняя версия на PyPI - это 0.2.1.

Для установки версии 0.3.1 используйте один из следующих способов:

### Установка из исходников

```bash
git clone https://github.com/f1sherFM/My_1st_library_python.git
cd My_1st_library_python
pip install -e .
```

### Установка последней версии с PyPI (v0.2.1)

```bash
pip install fishertools
```

### Установка для разработки

```bash
git clone https://github.com/f1sherFM/My_1st_library_python.git
cd My_1st_library_python
pip install -e ".[dev]"
```

**Примечание:** Версия 0.3.1 будет опубликована на PyPI после завершения тестирования и финализации документации.

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

### Структура данных explain()

Функция `explain()` возвращает словарь с тремя ключами, содержащими полную информацию о теме:

```python
from fishertools.learn import explain

explanation = explain("list")
print(explanation)
# {
#     "description": "Ordered collection of items that can be of different types. Lists are mutable, meaning you can add, remove, or modify items.",
#     "when_to_use": "Use lists when you need to store multiple items in order and may need to modify them later. Perfect for storing collections of data.",
#     "example": "fruits = [\"apple\", \"banana\", \"orange\"]\nfruits.append(\"grape\")\nprint(fruits[0])\nprint(len(fruits))\nfor fruit in fruits:\n    print(fruit)"
# }
```

**Доступ к полям:**

```python
from fishertools.learn import explain

explanation = explain("list")

# Получить описание
print(explanation["description"])
# Ordered collection of items that can be of different types...

# Получить информацию о применении
print(explanation["when_to_use"])
# Use lists when you need to store multiple items in order...

# Получить пример кода
print(explanation["example"])
# fruits = ["apple", "banana", "orange"]
# fruits.append("grape")
# print(fruits[0])
# ...
```

### Поддерживаемые темы

| Категория | Тема | Описание |
|-----------|------|---------|
| **Типы данных** | int | Integer data type for whole numbers without decimals. Integers can be positive, negative, or zero. |
| **Типы данных** | float | Floating-point data type for numbers with decimal places. Floats represent real numbers with fractional parts. |
| **Типы данных** | str | String data type for text. Strings are sequences of characters enclosed in quotes (single, double, or triple). |
| **Типы данных** | bool | Boolean data type with only two possible values: True or False. Used for logical operations and conditions. |
| **Типы данных** | list | Ordered collection of items that can be of different types. Lists are mutable, meaning you can add, remove, or modify items. |
| **Типы данных** | tuple | Ordered collection of items similar to lists, but immutable. Once created, tuples cannot be modified. |
| **Типы данных** | set | Unordered collection of unique items. Sets automatically remove duplicates and are useful for membership testing. |
| **Типы данных** | dict | Unordered collection of key-value pairs. Dictionaries allow you to store and retrieve data using meaningful keys instead of numeric indices. |
| **Управляющие конструкции** | if | Conditional statement that executes code only if a condition is true. Forms the basis of decision-making in programs. |
| **Управляющие конструкции** | for | Loop statement that iterates over a sequence (list, tuple, string, etc.) and executes code for each item. |
| **Управляющие конструкции** | while | Loop statement that repeatedly executes code as long as a condition is true. Useful when you don't know how many iterations you need. |
| **Управляющие конструкции** | break | Statement that immediately exits the current loop, skipping any remaining iterations. |
| **Управляющие конструкции** | continue | Statement that skips the current iteration of a loop and moves to the next iteration. |
| **Функции** | function | Reusable block of code that performs a specific task. Functions help organize code and avoid repetition. |
| **Функции** | return | Statement that sends a value back from a function to the caller. A function can return any type of data. |
| **Функции** | lambda | Anonymous function defined with a single expression. Lambdas are useful for short, simple functions. |
| **Функции** | *args | Special parameter that allows a function to accept any number of positional arguments as a tuple. |
| **Функции** | **kwargs | Special parameter that allows a function to accept any number of keyword arguments as a dictionary. |
| **Обработка ошибок** | try | Statement that begins a block of code where exceptions might occur. Used with except to handle errors gracefully. |
| **Обработка ошибок** | except | Statement that catches and handles specific exceptions that occur in a try block. |
| **Обработка ошибок** | finally | Statement that executes code after try and except blocks, regardless of whether an exception occurred. |
| **Обработка ошибок** | raise | Statement that manually raises an exception to signal an error condition in your code. |
| **Работа с файлами** | open | Function that opens a file and returns a file object. Used to read from or write to files. |
| **Работа с файлами** | read | Method that reads the entire contents of a file as a string, or reads a specific number of characters. |
| **Работа с файлами** | write | Method that writes data to a file. Creates the file if it doesn't exist, or overwrites it if it does. |
| **Работа с файлами** | with | Context manager statement that automatically handles resource management, ensuring files are properly closed. |
| **Типы данных** | slice | Technique to extract a portion of a sequence (list, tuple, string) using start:stop:step notation. |
| **Типы данных** | list_comprehension | Concise way to create a new list by applying an expression to each item in an existing sequence. |
| **Типы данных** | enumerate | Built-in function that returns both the index and value when iterating over a sequence. |
| **Управляющие конструкции** | import | Statement that loads a module or specific items from a module into your program. Modules contain reusable code. |

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

### Расширение и локализация

Все темы хранятся в JSON файле `fishertools/learn/explanations.json`, что делает их легко расширяемыми и локализуемыми:

**Для контрибьюторов:**
- Добавьте новую тему в JSON файл `fishertools/learn/explanations.json`
- Каждая тема должна содержать три поля: `description`, `when_to_use`, и `example`
- Функция `explain()` автоматически загружает все темы из этого файла

**Для локализации:**
- Переведите существующие темы на другой язык
- Создайте новый JSON файл с переводами
- Используйте параметр `language` при вызове `explain()` для выбора языка

**Для кастомизации:**
- Используйте свой JSON файл с дополнительными темами
- Передайте путь к файлу при инициализации модуля
- Это позволяет добавлять специфичные для вашего проекта темы

Благодаря JSON-хранилищу, расширение fishertools не требует изменения кода - просто добавьте новые записи в JSON файл!

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

Fishertools объясняет следующие типы ошибок Python. Это полный список поддерживаемых типов ошибок:

#### Ошибки типов и значений

- **TypeError** - возникает при попытке выполнить операцию над значениями несовместимых типов (например, сложить число и строку)
- **ValueError** - возникает когда функция получает аргумент правильного типа, но неправильного значения (например, int("abc"))

#### Ошибки доступа к данным

- **AttributeError** - возникает при попытке доступа к несуществующему атрибуту объекта
- **IndexError** - возникает при попытке доступа к элементу списка по индексу, который выходит за границы списка
- **KeyError** - возникает при попытке доступа к несуществующему ключу в словаре

#### Ошибки импорта и синтаксиса

- **ImportError** - возникает при проблемах с импортом модулей (модуль не найден или ошибка в модуле)
- **SyntaxError** - возникает при синтаксических ошибках в коде (неправильный синтаксис Python)

#### Ошибки имён и вычислений

- **NameError** - возникает при использовании переменной или имени, которое не было определено
- **ZeroDivisionError** - возникает при попытке деления на ноль

#### Ошибки файловой системы

- **FileNotFoundError** - возникает при попытке открыть файл, который не существует

**Примеры использования:**

```python
from fishertools import explain_error

# Пример 1: TypeError
try:
    result = "5" + 10
except Exception as e:
    explain_error(e)

# Пример 2: ValueError
try:
    number = int("abc")
except Exception as e:
    explain_error(e)

# Пример 3: IndexError
try:
    items = [1, 2, 3]
    print(items[10])
except Exception as e:
    explain_error(e)

# Пример 4: KeyError
try:
    data = {"name": "Alice"}
    print(data["age"])
except Exception as e:
    explain_error(e)

# Пример 5: FileNotFoundError
try:
    with open("nonexistent.txt") as f:
        content = f.read()
except Exception as e:
    explain_error(e)
```

### Безопасные утилиты

- `safe_get(collection, index, default)` - безопасное получение элемента
- `safe_divide(a, b, default)` - деление без ошибки на ноль
- `safe_max(collection, default)` - максимум из коллекции
- `safe_min(collection, default)` - минимум из коллекции
- `safe_sum(collection, default)` - сумма элементов
- `safe_read_file(path, default)` - чтение файла без ошибок
- `ensure_dir(path)` - рекурсивное создание директорий
- `get_file_hash(path, algorithm='sha256')` - вычисление хэша файла
- `read_last_lines(path, n=10)` - чтение последних N строк файла

### Обучающие функции

- `show_best_practice(topic)` - показать лучшие практики
- `generate_example(concept)` - сгенерировать пример кода
- `list_available_concepts()` - список доступных концепций
- `list_available_topics()` - список доступных тем

## ⚠️ Ограничения

Текущая версия fishertools имеет следующие известные ограничения:

### explain_error() и SyntaxError

`explain_error()` не может объяснить `SyntaxError` до исполнения кода. Это связано с тем, что синтаксические ошибки обнаруживаются на этапе парсинга (анализа кода), который происходит **до** выполнения программы. Это означает, что вы не сможете поймать `SyntaxError` в блоке `try-except`, так как программа не будет запущена вообще.

**Пример:**
```python
# Это вызовет SyntaxError ДО выполнения программы
try:
    x = 5 +  # Синтаксическая ошибка - неполное выражение
except SyntaxError as e:
    explain_error(e)  # Этот код никогда не выполнится
```

Однако вы можете объяснить другие типы ошибок, которые возникают во время выполнения:
```python
# Это работает - ошибка возникает во время выполнения
try:
    result = 10 / 0  # ZeroDivisionError
except Exception as e:
    explain_error(e)  # Работает корректно
```

### explain() и объектно-ориентированное программирование

Функция `explain()` пока не поддерживает объяснение классов и концепций OOP (объектно-ориентированного программирования), таких как:
- Классы и объекты
- Наследование
- Полиморфизм
- Инкапсуляция
- Методы и свойства класса

Поддержка OOP планируется в будущих версиях fishertools. На данный момент `explain()` работает с базовыми типами данных и управляющими конструкциями.

**Текущие возможности explain():**
```python
from fishertools.learn import explain

# Это работает
explain("list")        # Типы данных
explain("for")         # Управляющие конструкции
explain("function")    # Функции
explain("try")         # Обработка ошибок

# Это пока не поддерживается
# explain("class")      # Классы
# explain("inheritance") # Наследование
# explain("polymorphism") # Полиморфизм
```

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
