# Fishertools Updates

## v0.4.7 (5 февраля 2026) - РЕАЛИЗОВАНО ✅

### 🌐 Безопасные сетевые операции
```python
from fishertools import safe_request, safe_download

# Безопасные HTTP запросы с таймаутами и обработкой ошибок
response = safe_request("https://api.example.com/data", timeout=10)
if response.success:
    print(response.data)
else:
    print(f"Ошибка: {response.error}")

# Загрузка файлов с отслеживанием прогресса
def progress_callback(progress):
    print(f"Загружено: {progress.percentage:.1f}%")

response = safe_download(
    "https://example.com/file.zip",
    "downloads/file.zip",
    progress_callback=progress_callback
)
```

### 🎨 Улучшенная визуализация
```python
from fishertools import EnhancedVisualizer, AlgorithmVisualizer

# Расширенная визуализация с новыми опциями
viz = EnhancedVisualizer()
result = viz.visualize(
    data, 
    style="tree",      # древовидная структура
    colors=True,       # цветная подсветка типов
    max_depth=3,       # ограничение глубины
    export="json"      # экспорт в файл
)

# Визуализация алгоритмов сортировки и поиска
algo_viz = AlgorithmVisualizer()
result = algo_viz.visualize_sorting([3,1,4,1,5,9], algorithm="bubble_sort")
print(f"Сравнений: {result.statistics['comparisons']}")

result = algo_viz.visualize_search([1,2,3,4,5], target=3, algorithm="binary_search")
```

### 🌍 Многоязычная поддержка
```python
from fishertools import explain_error, translate_error, detect_language

# Определение языка системы
lang = detect_language()  # 'ru' или 'en'

try:
    result = 10 / 0
except ZeroDivisionError as e:
    # Объяснение на русском (по умолчанию)
    explain_error(e, language='ru')
    
    # Объяснение на английском
    explain_error(e, language='en')
    
    # Автоопределение языка
    explain_error(e, language='auto')
    
    # Структурированное объяснение
    explanation = translate_error(e, lang='en')
    print(explanation.explanation)
```

### ⚙️ Управление конфигурацией
```python
from fishertools.config import NetworkConfig, VisualizationConfig, I18nConfig

# Настройка сетевых операций
net_config = NetworkConfig(default_timeout=15.0, max_retries=5)

# Настройка визуализации
viz_config = VisualizationConfig(default_style='tree', default_colors=True)

# Настройка языков
i18n_config = I18nConfig(default_language='en', auto_detect=True)
```

### 📊 Информация о версии
```python
from fishertools import get_version_info

info = get_version_info()
print(f"Версия: {info['version']}")
print(f"Возможности: {', '.join(info['features'])}")
```

---

## Предыдущие обновления

**4. Безопасная работа с сетью** - РЕАЛИЗОВАНО в v0.4.7 ✅
from fishertools.safe_network import safe_request, safe_download

# Безопасные HTTP запросы с таймаутами и обработкой ошибок
response = safe_request("https://api.example.com", timeout=5)
safe_download("https://example.com/file.zip", "local_file.zip")

**5. Улучшенная визуализация**

# Больше опций для visualize()
visualize(data, 
    style="tree",      # древовидная структура
    colors=True,       # цветная подсветка типов
    max_depth=3,       # ограничение глубины
    export="json"      # экспорт в файл
)

# Визуализация алгоритмов
visualize_sorting([3,1,4,1,5], algorithm="bubble")
visualize_search([1,2,3,4,5], target=3, algorithm="binary")

**Расширение языковой поддержки**

# Текущее состояние
explain_error(e)  # только на русском

# Предложение
explain_error(e, lang='ru')  # русский
explain_error(e, lang='en')  # английский
explain_error(e, lang='auto')  # автоопределение по системе