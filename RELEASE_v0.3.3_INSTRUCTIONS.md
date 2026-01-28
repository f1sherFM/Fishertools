# Инструкции по выпуску v0.3.3 на GitHub и PyPI

## 📋 Предварительная проверка

Убедитесь, что все тесты проходят:

```bash
# Запустить все тесты
pytest tests/ -v

# Или с покрытием
pytest tests/ --cov=fishertools --cov-report=html
```

Ожидаемый результат: **56 тестов пройдено**

## 🔧 Шаг 1: Подготовка локального репозитория

```bash
# Убедитесь, что вы на ветке main
git branch

# Обновите локальный репозиторий
git pull origin main

# Проверьте статус
git status
```

## 📝 Шаг 2: Коммит изменений

```bash
# Добавьте все изменения
git add .

# Создайте коммит с описанием
git commit -m "Release v0.3.3: Add file utilities (ensure_dir, get_file_hash, read_last_lines)

- Implement ensure_dir() for recursive directory creation
- Implement get_file_hash() with streaming and multiple algorithms
- Implement read_last_lines() with efficient buffer algorithm
- Add 11 property-based tests validating all correctness properties
- Add 9 unit tests for error handling and edge cases
- Update README with usage examples
- All 56 tests passing (100% success rate)"
```

## 🏷️ Шаг 3: Создание тага

```bash
# Создайте аннотированный тег
git tag -a v0.3.3 -m "Release v0.3.3: File utilities with property-based testing

New Features:
- ensure_dir(): Recursive directory creation with idempotency
- get_file_hash(): Streaming file hashing (md5, sha1, sha256, sha512, blake2b)
- read_last_lines(): Efficient reading of last N lines

Testing:
- 56 tests passing (100% success rate)
- 11 property-based tests validating correctness properties
- Full edge case coverage

Documentation:
- Complete type hints and PEP 257 docstrings
- Examples in README.md
- Updated CHANGELOG.md"
```

## 🚀 Шаг 4: Отправка на GitHub

```bash
# Отправьте коммиты на main ветку
git push origin main

# Отправьте тег на GitHub
git push origin v0.3.3

# Проверьте, что всё отправилось
git log --oneline -5
git tag -l | grep v0.3.3
```

## 📦 Шаг 5: Подготовка пакета для PyPI

### 5.1 Установите необходимые инструменты (если не установлены)

```bash
pip install build twine
```

### 5.2 Очистите старые артефакты

```bash
# Windows
rmdir /s /q dist build *.egg-info

# Linux/macOS
rm -rf dist/ build/ *.egg-info
```

### 5.3 Соберите пакет

```bash
python -m build
```

Ожидаемый результат:
```
Successfully built fishertools-0.3.3.tar.gz and fishertools-0.3.3-py3-none-any.whl
```

### 5.4 Проверьте пакет перед загрузкой

```bash
twine check dist/*
```

Ожидаемый результат:
```
Checking distribution dist/fishertools-0.3.3.tar.gz: Passed
Checking distribution dist/fishertools-0.3.3-py3-none-any.whl: Passed
```

## 🌐 Шаг 6: Загрузка на PyPI

### 6.1 Загрузите на PyPI

```bash
twine upload dist/*
```

Вам будет предложено ввести учётные данные PyPI:
- Username: `__token__`
- Password: `pypi-...` (ваш PyPI токен)

### 6.2 Проверьте загрузку

```bash
# Проверьте на PyPI
# https://pypi.org/project/fishertools/0.3.3/

# Или установите из PyPI
pip install --upgrade fishertools==0.3.3
```

## ✅ Шаг 7: Финальная проверка

### 7.1 Проверьте, что пакет установился

```bash
python -c "from fishertools.safe import ensure_dir, get_file_hash, read_last_lines; print('✅ All functions imported successfully')"
```

### 7.2 Проверьте версию

```bash
python -c "import fishertools; print(f'fishertools version: {fishertools.__version__ if hasattr(fishertools, \"__version__\") else \"unknown\"}')"
```

### 7.3 Проверьте на PyPI

Откройте в браузере:
```
https://pypi.org/project/fishertools/0.3.3/
```

Должны увидеть:
- ✅ Версия 0.3.3
- ✅ Описание с файловыми утилитами
- ✅ Ссылка на GitHub
- ✅ Информация об авторе

## 🎉 Шаг 8: Создание GitHub Release (опционально)

1. Откройте https://github.com/f1sherFM/My_1st_library_python/releases
2. Нажмите "Draft a new release"
3. Выберите тег `v0.3.3`
4. Заполните описание:

```markdown
# Release v0.3.3 - File Utilities

## 🎯 What's New

### New Functions
- **ensure_dir()** - Recursive directory creation with idempotency
- **get_file_hash()** - Streaming file hashing (md5, sha1, sha256, sha512, blake2b)
- **read_last_lines()** - Efficient reading of last N lines

### Testing
- ✅ 56 tests passing (100% success rate)
- ✅ 11 property-based tests validating correctness properties
- ✅ Full edge case coverage

### Documentation
- Complete type hints and PEP 257 docstrings
- Examples in README.md
- Updated CHANGELOG.md

## 📦 Installation

```bash
pip install fishertools==0.3.3
```

## 📖 Usage

```python
from fishertools.safe import ensure_dir, get_file_hash, read_last_lines

# Create directories recursively
path = ensure_dir("./data/nested/directory")

# Calculate file hash
hash_sha256 = get_file_hash("data.txt")
hash_md5 = get_file_hash("data.txt", algorithm='md5')

# Read last lines efficiently
lines = read_last_lines("log.txt", n=10)
```

## 🔗 Links
- [PyPI Package](https://pypi.org/project/fishertools/0.3.3/)
- [GitHub Repository](https://github.com/f1sherFM/My_1st_library_python)
- [CHANGELOG](https://github.com/f1sherFM/My_1st_library_python/blob/main/CHANGELOG.md)
```

5. Нажмите "Publish release"

## 🐛 Troubleshooting

### Проблема: "twine: command not found"

```bash
pip install twine
```

### Проблема: "Invalid distribution"

```bash
# Проверьте, что setup.py и pyproject.toml согласованы
# Убедитесь, что версия одинакова везде
grep -r "0.3.3" setup.py pyproject.toml
```

### Проблема: "Authentication failed"

```bash
# Убедитесь, что используете правильный токен
# Токен должен начинаться с "pypi-"
# Проверьте на https://pypi.org/manage/account/tokens/
```

### Проблема: "File already exists"

```bash
# Нельзя переиздать ту же версию
# Нужно создать новую версию (например, 0.3.4)
# Или удалить версию на PyPI (требует прав администратора)
```

## 📊 Проверочный список

- [ ] Все тесты проходят (56/56)
- [ ] Версия обновлена в setup.py
- [ ] Версия обновлена в pyproject.toml
- [ ] CHANGELOG.md обновлён
- [ ] README.md обновлён с примерами
- [ ] Коммит создан с описанием
- [ ] Тег создан
- [ ] Коммит отправлен на GitHub
- [ ] Тег отправлен на GitHub
- [ ] Пакет собран (dist/)
- [ ] Пакет проверен (twine check)
- [ ] Пакет загружен на PyPI
- [ ] Пакет установлен из PyPI
- [ ] Функции работают после установки
- [ ] GitHub Release создан (опционально)

## 🎯 Итоговые команды (быстрый способ)

```bash
# 1. Коммит и тег
git add .
git commit -m "Release v0.3.3: Add file utilities"
git tag -a v0.3.3 -m "Release v0.3.3: File utilities with property-based testing"

# 2. Отправка на GitHub
git push origin main
git push origin v0.3.3

# 3. Подготовка пакета
rm -rf dist/ build/ *.egg-info
python -m build

# 4. Проверка
twine check dist/*

# 5. Загрузка на PyPI
twine upload dist/*

# 6. Финальная проверка
pip install --upgrade fishertools==0.3.3
python -c "from fishertools.safe import ensure_dir, get_file_hash, read_last_lines; print('✅ Success')"
```

---

**Дата:** 28 января 2026  
**Версия:** 0.3.3  
**Статус:** Готово к выпуску
