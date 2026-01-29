# 📝 Примеры кода для новых модулей fishertools

## 1️⃣ VISUALIZATION МОДУЛЬ

### Пример 1: Визуализация списка
```python
from fishertools.visualization import visualize

# Простой список
numbers = [10, 20, 30, 40, 50]
visualize(numbers)

# Вывод:
# 📊 List visualization:
# [0] → 10
# [1] → 20
# [2] → 30
# [3] → 40
# [4] → 50
```

### Пример 2: Визуализация словаря
```python
from fishertools.visualization import visualize

# Словарь
user = {
    "name": "Alice",
    "age": 25,
    "email": "alice@example.com",
    "active": True
}
visualize(user)

# Вывод:
# 📊 Dictionary visualization:
# {
#   "name" → "Alice"
#   "age" → 25
#   "email" → "alice@example.com"
#   "active" → True
# }
```

### Пример 3: Вложенные структуры
```python
from fishertools.visualization import visualize

# Вложенная структура
data = {
    "users": [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30}
    ],
    "total": 2
}
visualize(data, max_depth=3, colors=True)

# Вывод:
# 📊 Nested structure visualization:
# {
#   "users" → [
#     [0] → {
#       "name" → "Alice"
#       "age" → 25
#     }
#     [1] → {
#       "name" → "Bob"
#       "age" → 30
#     }
#   ]
#   "total" → 2
# }
```

### Пример 4: Визуализация с фильтром
```python
from fishertools.visualization import visualize

# Большой список - показать только первые 5 элементов
big_list = list(range(1000))
visualize(big_list, max_items=5)

# Вывод:
# 📊 List visualization (showing 5 of 1000):
# [0] → 0
# [1] → 1
# [2] → 2
# [3] → 3
# [4] → 4
# ... and 995 more items
```

---

## 2️⃣ VALIDATION МОДУЛЬ

### Пример 1: Проверка типов через декоратор
```python
from fishertools.validation import validate_types, ValidationError

@validate_types
def create_user(name: str, age: int, email: str) -> dict:
    """Создать пользователя с проверкой типов."""
    return {
        "name": name,
        "age": age,
        "email": email
    }

# ✅ Правильно
user = create_user("Alice", 25, "alice@example.com")
print(user)

# ❌ Ошибка типа
try:
    user = create_user("Bob", "thirty", "bob@example.com")
except ValidationError as e:
    print(f"❌ Ошибка: {e}")
    # Ошибка: age должен быть int, получен str
```

### Пример 2: Валидация email
```python
from fishertools.validation import validate_email, ValidationError

# ✅ Правильный email
try:
    validate_email("user@example.com")
    print("✅ Email валиден")
except ValidationError as e:
    print(f"❌ {e}")

# ❌ Неправильный email
try:
    validate_email("invalid-email")
    print("✅ Email валиден")
except ValidationError as e:
    print(f"❌ {e}")
    # Ошибка: Неправильный формат email
```

### Пример 3: Валидация числа
```python
from fishertools.validation import validate_number, ValidationError

# ✅ Число в диапазоне
try:
    validate_number(42, min_val=0, max_val=100)
    print("✅ Число валидно")
except ValidationError as e:
    print(f"❌ {e}")

# ❌ Число вне диапазона
try:
    validate_number(150, min_val=0, max_val=100)
    print("✅ Число валидно")
except ValidationError as e:
    print(f"❌ {e}")
    # Ошибка: Число должно быть между 0 и 100
```

### Пример 4: Валидация структуры данных
```python
from fishertools.validation import validate_structure, ValidationError

# Определить структуру
user_structure = {
    "name": str,
    "age": int,
    "email": str,
    "active": bool
}

# ✅ Правильная структура
user_data = {
    "name": "Alice",
    "age": 25,
    "email": "alice@example.com",
    "active": True
}

try:
    validate_structure(user_data, user_structure)
    print("✅ Структура валидна")
except ValidationError as e:
    print(f"❌ {e}")

# ❌ Неправильная структура
bad_data = {
    "name": "Bob",
    "age": "thirty",  # Должен быть int
    "email": "bob@example.com",
    "active": True
}

try:
    validate_structure(bad_data, user_structure)
    print("✅ Структура валидна")
except ValidationError as e:
    print(f"❌ {e}")
    # Ошибка: age должен быть int, получен str
```

---

## 3️⃣ DEBUG МОДУЛЬ

### Пример 1: Пошаговое выполнение
```python
from fishertools.debug import debug_step_by_step

@debug_step_by_step
def calculate_average(numbers):
    """Вычислить среднее значение."""
    total = sum(numbers)
    average = total / len(numbers)
    return average

# Вызов функции
result = calculate_average([1, 2, 3, 4, 5])

# Вывод:
# 🔍 Debugging: calculate_average
# 
# Step 1: numbers = [1, 2, 3, 4, 5]
# Step 2: total = sum(numbers) = 15
# Step 3: len(numbers) = 5
# Step 4: average = 15 / 5 = 3.0
# Step 5: return 3.0
# 
# ✅ Result: 3.0
```

### Пример 2: Трассировка рекурсии
```python
from fishertools.debug import trace

@trace
def fibonacci(n):
    """Вычислить n-е число Фибоначчи."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Вызов функции
result = fibonacci(5)

# Вывод:
# 🔍 Tracing: fibonacci
# 
# → fibonacci(5)
#   → fibonacci(4)
#     → fibonacci(3)
#       → fibonacci(2)
#         → fibonacci(1) = 1
#         → fibonacci(0) = 0
#       ← fibonacci(2) = 1
#       → fibonacci(1) = 1
#     ← fibonacci(3) = 2
#     → fibonacci(2)
#       → fibonacci(1) = 1
#       → fibonacci(0) = 0
#     ← fibonacci(2) = 1
#   ← fibonacci(4) = 3
#   → fibonacci(3)
#     → fibonacci(2)
#       → fibonacci(1) = 1
#       → fibonacci(0) = 0
#     ← fibonacci(2) = 1
#     → fibonacci(1) = 1
#   ← fibonacci(3) = 2
# ← fibonacci(5) = 5
# 
# ✅ Result: 5
```

### Пример 3: Точки останова
```python
from fishertools.debug import set_breakpoint, debug_context

def complex_calculation():
    """Сложный расчет с точками останова."""
    x = 10
    y = 20
    
    print(f"x = {x}, y = {y}")
    
    set_breakpoint()  # Остановка здесь
    
    z = x + y
    print(f"z = {z}")
    
    set_breakpoint()  # Остановка здесь
    
    result = z * 2
    print(f"result = {result}")
    
    return result

# Вызов функции
result = complex_calculation()

# Вывод:
# x = 10, y = 20
# 🔴 Breakpoint 1: complex_calculation:6
# (Можно проверить переменные)
# z = 30
# 🔴 Breakpoint 2: complex_calculation:11
# (Можно проверить переменные)
# result = 60
```

### Пример 4: Отладка с контекстом
```python
from fishertools.debug import debug_context

def process_data(data):
    """Обработать данные с отладкой."""
    with debug_context("process_data"):
        result = []
        for i, item in enumerate(data):
            processed = item * 2
            result.append(processed)
        return result

# Вызов функции
result = process_data([1, 2, 3, 4, 5])

# Вывод:
# 🔍 Debug context: process_data
# 
# Iteration 1: item = 1, processed = 2
# Iteration 2: item = 2, processed = 4
# Iteration 3: item = 3, processed = 6
# Iteration 4: item = 4, processed = 8
# Iteration 5: item = 5, processed = 10
# 
# ✅ Result: [2, 4, 6, 8, 10]
```

---

## 4️⃣ PERFORMANCE МОДУЛЬ

### Пример 1: Анализ производительности
```python
from fishertools.performance import analyze_performance

@analyze_performance
def find_element(lst, target):
    """Найти элемент в списке."""
    for i in range(len(lst)):
        if lst[i] == target:
            return i
    return -1

# Вызов функции
result = find_element(list(range(1000)), 500)

# Вывод:
# 📊 Performance Analysis: find_element
# 
# ⏱️ Время выполнения: 0.0001 сек
# 💾 Память: 2.5 MB
# 📈 Сложность: O(n)
# 
# 💡 Рекомендации:
# - Используйте set для O(1) поиска
# - Для 1000 элементов: 1000 операций vs 1 операция
# - Ускорение: 1000x
```

### Пример 2: Измерение времени
```python
from fishertools.performance import measure_time

# Измерение времени операции
with measure_time("list creation"):
    my_list = list(range(1000000))

# Вывод:
# ⏱️ list creation: 0.0234 сек
```

### Пример 3: Измерение памяти
```python
from fishertools.performance import measure_memory

# Измерение использования памяти
with measure_memory("data processing"):
    data = [i * 2 for i in range(1000000)]

# Вывод:
# 💾 data processing: 8.5 MB
```

### Пример 4: Профилирование функции
```python
from fishertools.performance import profile_function

def slow_function(n):
    """Медленная функция."""
    result = 0
    for i in range(n):
        for j in range(n):
            result += i * j
    return result

# Профилирование
profile_function(slow_function, args=(100,))

# Вывод:
# 📊 Function Profile: slow_function
# 
# ⏱️ Время выполнения: 0.1234 сек
# 💾 Память: 5.2 MB
# 📈 Вызовов: 10000
# 
# 💡 Рекомендации:
# - Функция выполняется медленно
# - Рассмотрите использование numpy для векторизации
# - Возможное ускорение: 100x
```

---

## 5️⃣ ALGORITHMS МОДУЛЬ

### Пример 1: Анализ сложности
```python
from fishertools.algorithms import analyze_complexity

@analyze_complexity
def bubble_sort(arr):
    """Сортировка пузырьком."""
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Вызов функции
result = bubble_sort([3, 1, 4, 1, 5, 9, 2, 6])

# Вывод:
# 📊 Algorithm Complexity Analysis: bubble_sort
# 
# ⏱️ Временная сложность: O(n²)
# 💾 Пространственная сложность: O(1)
# 
# ⚠️ Худший случай:
# - 1000 элементов = 1,000,000 операций
# - 10000 элементов = 100,000,000 операций
# 
# 💡 Альтернативы:
# 1. sorted() - O(n log n) - 100x быстрее
# 2. quicksort - O(n log n) - 100x быстрее
# 3. mergesort - O(n log n) - 100x быстрее
# 
# 🏆 Рекомендация: Используйте встроенную sorted()
```

### Пример 2: Рекомендации по оптимизации
```python
from fishertools.algorithms import suggest_optimization

def linear_search(lst, target):
    """Линейный поиск."""
    for item in lst:
        if item == target:
            return True
    return False

# Получить рекомендации
suggest_optimization(linear_search)

# Вывод:
# 💡 Optimization Suggestions: linear_search
# 
# Текущая сложность: O(n)
# 
# Рекомендация 1: Используйте set
# - Новая сложность: O(1)
# - Ускорение: 1000x для 1000 элементов
# 
# Рекомендация 2: Используйте бинарный поиск
# - Требует: отсортированный список
# - Новая сложность: O(log n)
# - Ускорение: 100x для 1000 элементов
# 
# Рекомендация 3: Используйте встроенный оператор in
# - Новая сложность: O(n) но быстрее на практике
# - Ускорение: 10x за счет оптимизаций C
```

---

## 6️⃣ COMPARISON МОДУЛЬ

### Пример 1: Сравнение подходов
```python
from fishertools.comparison import compare_approaches

# Способ 1: Цикл
def find_max_loop(lst):
    max_val = lst[0]
    for item in lst:
        if item > max_val:
            max_val = item
    return max_val

# Способ 2: Встроенная функция
def find_max_builtin(lst):
    return max(lst)

# Способ 3: Сортировка
def find_max_sorted(lst):
    return sorted(lst)[-1]

# Сравнение
compare_approaches([find_max_loop, find_max_builtin, find_max_sorted])

# Вывод:
# 📊 Comparison of Approaches
# 
# Способ 1 (find_max_loop):
#   ⏱️ Время: 0.0005 сек
#   📝 Строк кода: 5
#   💾 Память: 1.2 MB
#   📖 Читаемость: 3/5
#   🔧 Сложность: O(n)
#
# Способ 2 (find_max_builtin):
#   ⏱️ Время: 0.0001 сек (5x быстрее!)
#   📝 Строк кода: 1
#   💾 Память: 0.8 MB
#   📖 Читаемость: 5/5
#   🔧 Сложность: O(n)
#
# Способ 3 (find_max_sorted):
#   ⏱️ Время: 0.0010 сек (медленнее!)
#   📝 Строк кода: 1
#   💾 Память: 2.5 MB
#   📖 Читаемость: 4/5
#   🔧 Сложность: O(n log n)
#
# 🏆 Лучший вариант: Способ 2 (find_max_builtin)
# 💡 Вывод: Используйте встроенные функции
```

### Пример 2: Сравнение с метриками
```python
from fishertools.comparison import compare_with_metrics

# Способ 1: List comprehension
def process_list_comp(data):
    return [x * 2 for x in data]

# Способ 2: Map
def process_map(data):
    return list(map(lambda x: x * 2, data))

# Способ 3: Цикл
def process_loop(data):
    result = []
    for x in data:
        result.append(x * 2)
    return result

# Сравнение с метриками
compare_with_metrics(
    [process_list_comp, process_map, process_loop],
    metrics=['time', 'memory', 'readability', 'complexity']
)

# Вывод:
# 📊 Detailed Comparison with Metrics
# 
# ⏱️ Performance:
#   1. process_list_comp: 0.0001 сек ⭐⭐⭐⭐⭐
#   2. process_loop: 0.0002 сек ⭐⭐⭐⭐
#   3. process_map: 0.0003 сек ⭐⭐⭐
#
# 📖 Readability:
#   1. process_list_comp: 5/5 ⭐⭐⭐⭐⭐
#   2. process_loop: 4/5 ⭐⭐⭐⭐
#   3. process_map: 3/5 ⭐⭐⭐
#
# 🏆 Overall Winner: process_list_comp
```

---

## 🔗 Интеграция между модулями

### Пример: Полный workflow
```python
from fishertools.visualization import visualize
from fishertools.validation import validate_types
from fishertools.debug import debug_step_by_step
from fishertools.performance import analyze_performance
from fishertools.algorithms import analyze_complexity

# 1. Валидация входных данных
@validate_types
def process_numbers(numbers: list) -> dict:
    """Обработать список чисел."""
    
    # 2. Визуализация данных
    print("Входные данные:")
    visualize(numbers)
    
    # 3. Отладка с пошаговым выполнением
    @debug_step_by_step
    def calculate():
        total = sum(numbers)
        average = total / len(numbers)
        return average
    
    # 4. Анализ производительности
    @analyze_performance
    def find_max():
        return max(numbers)
    
    # 5. Анализ сложности
    @analyze_complexity
    def sort_numbers():
        return sorted(numbers)
    
    average = calculate()
    max_val = find_max()
    sorted_nums = sort_numbers()
    
    return {
        "average": average,
        "max": max_val,
        "sorted": sorted_nums
    }

# Использование
result = process_numbers([1, 2, 3, 4, 5])
print(result)
```

---

## 📚 Заключение

Эти примеры показывают, как новые модули могут быть использованы для:
- **Обучения** - визуализация и отладка
- **Разработки** - валидация и анализ производительности
- **Оптимизации** - анализ сложности и сравнение подходов
- **Качества** - интеграция всех инструментов

Вместе они создают мощную экосистему для Python разработки! 🚀
