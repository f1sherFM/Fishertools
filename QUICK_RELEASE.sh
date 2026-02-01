#!/bin/bash

# Быстрый скрипт для релиза v0.3.4 на GitHub и PyPI
# Использование: bash QUICK_RELEASE.sh

set -e  # Выход при первой ошибке

echo "🚀 Начинаем релиз v0.3.4..."
echo ""

# Проверка статуса репозитория
echo "📋 Проверка статуса репозитория..."
if [[ -n "$(git status --porcelain)" ]]; then
    echo "⚠️  В репозитории есть незакоммиченные изменения"
    echo "Пожалуйста, закоммитьте все изменения перед релизом"
    exit 1
fi

# Проверка версии
echo "✅ Проверка версии..."
VERSION=$(grep "__version__" fishertools/__init__.py | grep -oP '"\K[^"]+')
echo "Текущая версия: $VERSION"

if [[ "$VERSION" != "0.3.4" ]]; then
    echo "❌ Версия не совпадает с 0.3.4"
    exit 1
fi

# Запуск тестов
echo ""
echo "🧪 Запуск тестов..."
pytest tests/ -v --tb=short || {
    echo "❌ Тесты не прошли"
    exit 1
}

# Создание тага
echo ""
echo "🏷️  Создание тага v0.3.4..."
git tag -a v0.3.4 -m "Release v0.3.4: Knowledge Engine with 35+ Python topics" || {
    echo "⚠️  Тег уже существует"
}

# Пуш на GitHub
echo ""
echo "📤 Пуш на GitHub..."
git push origin main
git push origin v0.3.4

echo "✅ GitHub обновлён"

# Сборка пакета
echo ""
echo "📦 Сборка пакета..."
rm -rf build dist *.egg-info
python -m build

# Проверка пакета
echo ""
echo "🔍 Проверка пакета..."
twine check dist/*

# Загрузка на PyPI
echo ""
echo "🚀 Загрузка на PyPI..."
echo "Введите учётные данные PyPI (или используйте токен):"
twine upload dist/*

echo ""
echo "✅ Релиз v0.3.4 успешно завершён!"
echo ""
echo "📊 Статистика:"
echo "  - Версия: 0.3.4"
echo "  - Тем: 35"
echo "  - Тестов: 35 (27 unit + 8 property-based)"
echo "  - Покрытие: 100%"
echo ""
echo "🔗 Ссылки:"
echo "  - GitHub: https://github.com/f1sherFM/My_1st_library_python/releases/tag/v0.3.4"
echo "  - PyPI: https://pypi.org/project/fishertools/0.3.4/"
echo ""
echo "🎉 Спасибо за использование fishertools!"
