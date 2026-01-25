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
	python3 examples.py

# Форматирование кода
format:
	black mydevtools/ examples.py

# Проверка стиля
lint:
	ruff check mydevtools/ examples.py
	mypy mydevtools/

# Проверка стиля (альтернативно через flake8)
lint-flake8:
	flake8 mydevtools/
	mypy mydevtools/

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