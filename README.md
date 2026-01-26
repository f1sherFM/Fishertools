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