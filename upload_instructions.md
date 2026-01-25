# 📦 Инструкции по загрузке на PyPI

## Загрузка на Test PyPI

```bash
# Активируйте виртуальное окружение
source venv/bin/activate

# Загрузите на тестовый PyPI
twine upload --repository testpypi dist/*

# Когда появится запрос:
# Username: __token__
# Password: [вставьте ваш API токен]
```

## Тестирование установки

После успешной загрузки протестируйте установку:

```bash
# Создайте новое виртуальное окружение для теста
python3 -m venv test_env
source test_env/bin/activate

# Установите из тестового PyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ fishertools

# Протестируйте
python3 -c "from fishertools import utils; print('Работает!')"
```

## Загрузка на основной PyPI

Если всё работает на тестовом PyPI, загрузите на основной:

1. Получите токен на https://pypi.org/manage/account/token/
2. Загрузите:
```bash
twine upload dist/*
```

## Альтернативный способ с сохранением токена

Создайте файл `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-ваш-токен-для-основного-pypi

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-ваш-токен-для-тестового-pypi
```

Тогда можно загружать без ввода токена:
```bash
twine upload --repository testpypi dist/*
```