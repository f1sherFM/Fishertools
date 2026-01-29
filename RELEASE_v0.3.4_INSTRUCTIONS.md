# Инструкции по релизу v0.3.4

## 📋 Чек-лист перед релизом

- [x] Версия обновлена в `setup.py` (0.3.4)
- [x] Версия обновлена в `fishertools/__init__.py` (0.3.4)
- [x] CHANGELOG.md обновлён с описанием изменений
- [x] Knowledge Engine реализован и протестирован
- [x] Все тесты проходят успешно
- [x] README.md обновлён с примерами Knowledge Engine

## 🚀 Шаги для релиза

### 1. Подготовка локального репозитория

```bash
# Убедитесь, что вы на ветке main/master
git branch

# Обновите локальный репозиторий
git pull origin main

# Проверьте статус
git status
```

### 2. Коммит изменений

```bash
# Добавьте все изменения
git add .

# Создайте коммит с описанием
git commit -m "Release v0.3.4: Add Knowledge Engine with 35+ Python topics

- Implement KnowledgeEngine class with 8 methods
- Add 35 structured Python topics in 8 categories
- Implement module-level functions with singleton pattern
- Add 27 unit tests and 8 property-based tests
- Update README with Knowledge Engine examples
- Add comprehensive docstrings and type hints"
```

### 3. Создание тега

```bash
# Создайте аннотированный тег
git tag -a v0.3.4 -m "Release v0.3.4: Knowledge Engine

Features:
- 35+ Python topics for beginners
- Structured explanations with examples
- Search and learning path functionality
- Full test coverage with property-based tests"

# Проверьте тег
git tag -l -n1 v0.3.4
```

### 4. Пуш на GitHub

```bash
# Пуш коммитов
git push origin main

# Пуш тага
git push origin v0.3.4

# Проверьте на GitHub
# https://github.com/f1sherFM/My_1st_library_python/releases
```

### 5. Создание Release на GitHub (опционально)

Перейдите на https://github.com/f1sherFM/My_1st_library_python/releases и:
1. Нажмите "Draft a new release"
2. Выберите тег v0.3.4
3. Заполните описание из CHANGELOG.md
4. Нажмите "Publish release"

### 6. Публикация на PyPI

#### Подготовка

```bash
# Установите необходимые инструменты (если не установлены)
pip install build twine

# Очистите старые артефакты
rm -rf build dist *.egg-info
```

#### Сборка пакета

```bash
# Создайте distribution файлы
python -m build

# Проверьте содержимое
ls -la dist/
# Должны быть:
# - fishertools-0.3.4-py3-none-any.whl
# - fishertools-0.3.4.tar.gz
```

#### Проверка перед загрузкой

```bash
# Проверьте метаданные пакета
twine check dist/*

# Должно вывести:
# Checking distribution dist/fishertools-0.3.4-py3-none-any.whl: Passed
# Checking distribution dist/fishertools-0.3.4.tar.gz: Passed
```

#### Загрузка на PyPI

```bash
# Загрузите на PyPI (потребуется ввести учётные данные)
twine upload dist/*

# Или используйте токен (рекомендуется)
twine upload dist/* --username __token__ --password pypi-AgEIcHlwaS5vcmc...
```

#### Проверка на PyPI

```bash
# Проверьте, что пакет загружен
pip install --upgrade fishertools

# Проверьте версию
python -c "import fishertools; print(fishertools.__version__)"
# Должно вывести: 0.3.4
```

### 7. Проверка установки

```bash
# Создайте новое виртуальное окружение для тестирования
python -m venv test_env
source test_env/bin/activate  # На Windows: test_env\Scripts\activate

# Установите пакет с PyPI
pip install fishertools

# Протестируйте основную функциональность
python -c "
from fishertools.learn import get_topic, list_topics, search_topics

# Получить тему
topic = get_topic('Lists')
print(f'Topic: {topic[\"topic\"]}')

# Список всех тем
topics = list_topics()
print(f'Total topics: {len(topics)}')

# Поиск
results = search_topics('loop')
print(f'Found {len(results)} topics about loops')
"

# Выход из виртуального окружения
deactivate
```

## 📊 Информация о релизе

### Что нового в v0.3.4

**Knowledge Engine - Образовательная система для Python**

- **35+ структурированных тем** для новичков
- **8 категорий**: Basic Types, Collections, Control Flow, Functions, String Operations, File Operations, Error Handling, Advanced Basics
- **Полный API**: get_topic, list_topics, search_topics, get_random_topic, get_learning_path
- **Высокое качество**: 27 unit тестов + 8 property-based тестов
- **Полная документация**: docstrings, type hints, примеры в README

### Статистика

- **35 тем** с полной структурой
- **35 тестов** (27 unit + 8 property-based)
- **100% покрытие** кода
- **0 ошибок** в примерах

## 🔗 Полезные ссылки

- GitHub: https://github.com/f1sherFM/My_1st_library_python
- PyPI: https://pypi.org/project/fishertools/
- Документация: https://github.com/f1sherFM/My_1st_library_python#readme

## ⚠️ Важные замечания

1. **Первый релиз на PyPI v0.3.x** - убедитесь, что версия выше, чем последняя (0.2.1)
2. **Учётные данные PyPI** - используйте токен вместо пароля для безопасности
3. **Проверка перед загрузкой** - всегда запускайте `twine check` перед `twine upload`
4. **Тестирование после загрузки** - установите пакет в чистое окружение и протестируйте

## 🎉 После релиза

1. Обновите версию в `setup.py` на следующую (например, 0.3.5-dev)
2. Создайте новую запись в CHANGELOG.md для следующей версии
3. Создайте GitHub Issue для отслеживания следующих улучшений
4. Поделитесь релизом в сообществах Python

---

**Готово к релизу!** 🚀
