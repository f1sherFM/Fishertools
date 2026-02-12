.PHONY: install install-dev test clean build upload demo

# Установка пакета
install:
	pip install -e .

# Установка для разработки
install-dev:
	pip install -e ".[dev]"
	pip install build twine

# Запуск демонстрации
demo:
	python3 examples/refactored_safe_usage.py

# Форматирование кода
format:
	black fishertools/ examples/ tests/

# Проверка стиля
lint:
	ruff check fishertools/ examples/ tests/
	mypy fishertools/

# Проверка стиля (альтернативно через flake8)
lint-flake8:
	flake8 fishertools/
	mypy fishertools/

# Очистка временных файлов
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f test.json

# Сборка пакета
build: clean
	python3 -m build

# Загрузка на PyPI (тестовый)
upload-test: build
	twine upload --repository testpypi dist/*

# Загрузка на PyPI
upload: build
	twine upload dist/*
