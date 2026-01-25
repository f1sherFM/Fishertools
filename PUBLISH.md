# 📦 Публикация FisherTools на PyPI

## Подготовка

1. **Создайте аккаунт на PyPI:**
   - Основной: https://pypi.org/account/register/
   - Тестовый: https://test.pypi.org/account/register/

2. **Установите необходимые инструменты:**
   ```bash
   pip install build twine
   ```

## 🚀 Публикация

### Шаг 1: Сборка пакета
```bash
# Очистка старых файлов
make clean

# Сборка пакета
python3 setup.py sdist
# или с wheel (если установлен)
python3 -m build
```

### Шаг 2: Проверка пакета
```bash
# Проверка содержимого
twine check dist/*
```

### Шаг 3: Тестовая публикация
```bash
# Загрузка на тестовый PyPI
twine upload --repository testpypi dist/*
```

### Шаг 4: Тестирование установки
```bash
# Установка с тестового PyPI
pip install --index-url https://test.pypi.org/simple/ fishertools

# Проверка работы
python3 -c "from fishertools import utils; print('Работает!')"
```

### Шаг 5: Публикация на основном PyPI
```bash
# Загрузка на основной PyPI
twine upload dist/*
```

## ✅ После публикации

Теперь любой может установить вашу библиотеку:
```bash
pip install fishertools
```

И использовать:
```python
from fishertools import utils, decorators, helpers
```

## 🔄 Обновление версии

1. Измените версию в `setup.py` и `pyproject.toml`
2. Обновите `CHANGELOG.md` (если есть)
3. Создайте новый пакет и опубликуйте

## 📋 Checklist перед публикацией

- [ ] Версия обновлена
- [ ] README.md актуален
- [ ] Примеры работают
- [ ] Код отформатирован
- [ ] Нет ошибок линтера
- [ ] Тесты пройдены (если есть)

## 🔐 Безопасность

- Используйте API токены вместо паролей
- Настройте 2FA на PyPI
- Не коммитьте токены в git