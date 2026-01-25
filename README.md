# MyDevTools

Библиотека для быстрой и удобной разработки на Python.

## 🚀 Возможности

**🛠️ Utils** - базовые утилиты:
- Чтение/запись JSON файлов
- Создание директорий и работа с файлами
- Временные метки
- Преобразование вложенных словарей

**🎯 Decorators** - полезные декораторы:
- `@timer` - измерение времени выполнения
- `@debug` - отладка функций
- `@retry` - повторные попытки при ошибках
- `@cache_result` - кеширование результатов
- `@validate_types` - проверка типов аргументов

**🚀 Helpers** - помощники для частых задач:
- Удобная работа с конфигурацией
- Генерация безопасных паролей
- Валидация email адресов
- Простое логирование

## 📦 Установка

```bash
# Из исходников
git clone https://github.com/f1sherFM/My_1st_library_python.git
cd My_1st_library_python
pip install -e .
```

## 💡 Использование

```python
from mydevtools import utils, decorators, helpers

# Работа с JSON
data = {"name": "test", "config": {"debug": True}}
utils.write_json(data, "config.json")
loaded = utils.read_json("config.json")

# Декораторы
@decorators.timer
@decorators.debug
def my_function(x):
    return x * 2

# Помощники
config = helpers.QuickConfig({"db": {"host": "localhost"}})
print(config.get("db.host"))  # localhost

password = helpers.generate_password(16)
logger = helpers.SimpleLogger("MyApp")
logger.info("Приложение запущено")
```

## 🧪 Демонстрация

Запустите файл с примерами:

```bash
python3 examples.py
```

## 🛠️ Разработка

```bash
# Установка для разработки
make install-dev

# Форматирование кода
make format

# Проверка стиля
make lint

# Демонстрация
make demo
```

## 📋 Требования

- Python 3.8+
- requests
- click

## 📄 Лицензия

MIT License