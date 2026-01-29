# 📦 Публикация fishertools v0.3.4 на PyPI

Этот документ содержит пошаговые инструкции для публикации пакета на PyPI.

---

## 🔐 Подготовка учётных данных PyPI

### Вариант 1: Использование токена (рекомендуется)

1. Перейдите на https://pypi.org/account/
2. Войдите в свой аккаунт (или создайте новый)
3. Перейдите в "Account settings" → "API tokens"
4. Нажмите "Create token"
5. Выберите "Entire account" (или конкретный проект)
6. Скопируйте токен (он больше не будет показан!)

### Вариант 2: Использование пароля (менее безопасно)

1. Перейдите на https://pypi.org/account/
2. Войдите в свой аккаунт
3. Используйте ваше имя пользователя и пароль при загрузке

---

## 📋 Предварительные проверки

### 1. Проверка версии

```bash
# Убедитесь, что версия 0.3.4 везде
grep -r "0.3.4" setup.py fishertools/__init__.py

# Должно вывести:
# setup.py:    version="0.3.4",
# fishertools/__init__.py:__version__ = "0.3.4"
```

### 2. Проверка CHANGELOG

```bash
# Убедитесь, что CHANGELOG.md содержит запись о v0.3.4
head -50 CHANGELOG.md | grep -A 5 "0.3.4"
```

### 3. Запуск тестов

```bash
# Запустите все тесты
pytest tests/ -v

# Должно вывести: passed (все тесты должны пройти)
```

### 4. Проверка структуры пакета

```bash
# Убедитесь, что все необходимые файлы присутствуют
ls -la fishertools/learn/
# Должны быть:
# - knowledge_engine.py
# - topics.json
# - test_knowledge_engine.py
# - test_knowledge_engine_pbt.py
# - __init__.py
```

---

## 🔨 Сборка пакета

### 1. Установка инструментов

```bash
# Установите build и twine (если не установлены)
pip install build twine

# Проверьте версии
python -m build --version
twine --version
```

### 2. Очистка старых артефактов

```bash
# Удалите старые файлы сборки
rm -rf build dist *.egg-info

# Проверьте, что удалено
ls -la | grep -E "build|dist|egg-info"
# Не должно быть результатов
```

### 3. Сборка пакета

```bash
# Создайте distribution файлы
python -m build

# Проверьте результат
ls -la dist/
# Должны быть:
# - fishertools-0.3.4-py3-none-any.whl (wheel)
# - fishertools-0.3.4.tar.gz (source distribution)
```

### 4. Проверка пакета

```bash
# Проверьте метаданные пакета
twine check dist/*

# Должно вывести:
# Checking distribution dist/fishertools-0.3.4-py3-none-any.whl: Passed
# Checking distribution dist/fishertools-0.3.4.tar.gz: Passed
```

---

## 🚀 Загрузка на PyPI

### Вариант 1: С использованием токена (рекомендуется)

```bash
# Загрузите пакет на PyPI
twine upload dist/* --username __token__ --password pypi-YOUR_TOKEN_HERE

# Замените YOUR_TOKEN_HERE на ваш токен
# Например: pypi-AgEIcHlwaS5vcmc...
```

### Вариант 2: С использованием пароля

```bash
# Загрузите пакет на PyPI
twine upload dist/

# Введите:
# - Username: ваше имя пользователя PyPI
# - Password: ваш пароль PyPI
```

### Вариант 3: С использованием .pypirc (продвинутый)

Создайте файл `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Затем просто запустите:

```bash
twine upload dist/*
```

---

## ✅ Проверка после загрузки

### 1. Проверка на PyPI

```bash
# Перейдите на https://pypi.org/project/fishertools/
# Убедитесь, что версия 0.3.4 отображается
# Проверьте, что описание и примеры отображаются корректно
```

### 2. Установка из PyPI

```bash
# Создайте новое виртуальное окружение
python -m venv test_env
source test_env/bin/activate  # На Windows: test_env\Scripts\activate

# Установите пакет с PyPI
pip install fishertools

# Проверьте версию
python -c "import fishertools; print(fishertools.__version__)"
# Должно вывести: 0.3.4
```

### 3. Тестирование функциональности

```bash
# Протестируйте Knowledge Engine
python -c "
from fishertools.learn import get_topic, list_topics, search_topics

# Получить тему
topic = get_topic('Lists')
assert topic is not None
assert 'description' in topic
print('✅ get_topic работает')

# Список всех тем
topics = list_topics()
assert len(topics) == 35
print('✅ list_topics работает')

# Поиск
results = search_topics('loop')
assert len(results) > 0
print('✅ search_topics работает')

print('✅ Все функции работают корректно!')
"

# Выход из виртуального окружения
deactivate
```

### 4. Проверка документации

```bash
# Проверьте, что README отображается на PyPI
# Перейдите на https://pypi.org/project/fishertools/
# Убедитесь, что:
# - Описание отображается корректно
# - Примеры кода отображаются с форматированием
# - Таблицы отображаются корректно
# - Ссылки работают
```

---

## 🔄 Откат (если что-то пошло не так)

### Если пакет загружен с ошибками

К сожалению, PyPI не позволяет удалять или перезагружать версии. Вместо этого:

1. **Создайте новую версию** (например, 0.3.4.1)
2. **Обновите версию** в `setup.py` и `fishertools/__init__.py`
3. **Создайте новый тег** в Git
4. **Загрузите новую версию** на PyPI

```bash
# Обновите версию
sed -i 's/0.3.4/0.3.4.1/g' setup.py fishertools/__init__.py

# Создайте коммит
git add .
git commit -m "Fix: Release v0.3.4.1 with corrections"

# Создайте тег
git tag -a v0.3.4.1 -m "Release v0.3.4.1"

# Пуш на GitHub
git push origin main v0.3.4.1

# Пересоберите и загрузите
rm -rf build dist *.egg-info
python -m build
twine upload dist/*
```

---

## 📊 Статистика релиза

| Параметр | Значение |
|----------|----------|
| Версия | 0.3.4 |
| Тем | 35 |
| Тестов | 35 |
| Покрытие | 100% |
| Размер пакета | ~150 KB |
| Зависимости | requests, click |
| Python версии | 3.8+ |

---

## 🎯 Что дальше

После успешной публикации на PyPI:

1. **Создайте Release на GitHub**
   - Перейдите на https://github.com/f1sherFM/My_1st_library_python/releases
   - Нажмите "Draft a new release"
   - Выберите тег v0.3.4
   - Добавьте описание из CHANGELOG.md
   - Нажмите "Publish release"

2. **Обновите документацию**
   - Обновите README.md с информацией о новой версии
   - Добавьте примеры использования Knowledge Engine

3. **Создайте следующую версию**
   - Обновите версию на 0.3.5-dev
   - Создайте новую запись в CHANGELOG.md
   - Создайте GitHub Issue для отслеживания улучшений

4. **Поделитесь релизом**
   - Поделитесь в сообществах Python
   - Обновите профиль на GitHub
   - Добавьте информацию в социальные сети

---

## 🆘 Решение проблем

### Проблема: "Invalid distribution"

```
ERROR: File already exists. See https://pypi.org/help/#file-name-reuse for more information.
```

**Решение:** Версия уже загружена. Создайте новую версию (например, 0.3.4.1).

### Проблема: "Authentication failed"

```
ERROR: Invalid credentials. See https://pypi.org/help/#invalid-credentials for more information.
```

**Решение:** Проверьте токен или пароль. Убедитесь, что используете правильный формат.

### Проблема: "Invalid metadata"

```
ERROR: The metadata is invalid. See https://pypi.org/help/#invalid-metadata for more information.
```

**Решение:** Запустите `twine check dist/*` для проверки метаданных.

### Проблема: "Network error"

```
ERROR: Network error while uploading.
```

**Решение:** Проверьте интернет-соединение и повторите попытку.

---

## 📞 Контакты

- **GitHub Issues:** https://github.com/f1sherFM/My_1st_library_python/issues
- **PyPI Support:** https://pypi.org/help/
- **Email:** kirillka229top@gmail.com

---

**Готово к публикации! 🚀**

Следуйте этим инструкциям для успешной публикации fishertools v0.3.4 на PyPI.
