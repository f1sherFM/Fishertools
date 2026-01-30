"""
Примеры использования отрефакторенных safe утилит.

Демонстрирует улучшения после рефакторинга "spaghetti code".
"""

from fishertools.safe import (
    safe_get, safe_divide, safe_max, safe_min, safe_sum,
    safe_strip, safe_split, safe_join, safe_format
)


def demo_safe_divide():
    """Демонстрация исправленной математики в safe_divide"""
    print("=== safe_divide: Честная математика ===\n")
    
    # Нормальное деление
    result = safe_divide(10, 2)
    print(f"10 / 2 = {result}")  # 5.0
    
    # Деление на ноль - честно возвращает None
    result = safe_divide(10, 0)
    print(f"10 / 0 = {result}")  # None (математически корректно!)
    
    # Можно явно указать default
    result = safe_divide(10, 0, default=0)
    print(f"10 / 0 (с default=0) = {result}")  # 0 (явно указано)
    
    result = safe_divide(10, 0, default=float('inf'))
    print(f"10 / 0 (с default=inf) = {result}")  # inf
    
    print()


def demo_safe_get():
    """Демонстрация упрощенного safe_get"""
    print("=== safe_get: Простой и универсальный ===\n")
    
    # Работает со списками
    numbers = [1, 2, 3, 4, 5]
    print(f"numbers[2] = {safe_get(numbers, 2)}")  # 3
    print(f"numbers[10] = {safe_get(numbers, 10, 'не найдено')}")  # не найдено
    
    # Работает со словарями
    user = {"name": "Иван", "age": 25}
    print(f"user['name'] = {safe_get(user, 'name')}")  # Иван
    print(f"user['email'] = {safe_get(user, 'email', 'нет email')}")  # нет email
    
    # Работает со строками
    text = "Hello"
    print(f"text[0] = {safe_get(text, 0)}")  # H
    print(f"text[10] = {safe_get(text, 10, '?')}")  # ?
    
    print()


def demo_safe_collections():
    """Демонстрация упрощенных функций коллекций"""
    print("=== safe_max/min/sum: Простые и надежные ===\n")
    
    numbers = [1, 5, 3, 9, 2]
    print(f"Максимум: {safe_max(numbers)}")  # 9
    print(f"Минимум: {safe_min(numbers)}")  # 1
    print(f"Сумма: {safe_sum(numbers)}")  # 20
    
    # Пустые коллекции
    empty = []
    print(f"Максимум пустого списка: {safe_max(empty)}")  # None
    print(f"Минимум пустого списка: {safe_min(empty, default=-1)}")  # -1
    print(f"Сумма пустого списка: {safe_sum(empty, default=0)}")  # 0
    
    print()


def demo_safe_strings():
    """Демонстрация новых строковых функций"""
    print("=== Новые строковые функции ===\n")
    
    # safe_strip - обработка None
    text = "  hello  "
    print(f"safe_strip('{text}') = '{safe_strip(text)}'")  # 'hello'
    print(f"safe_strip(None) = '{safe_strip(None)}'")  # ''
    print(f"safe_strip(None, default='N/A') = '{safe_strip(None, default='N/A')}'")  # 'N/A'
    
    # safe_split - обработка None
    text = "a,b,c"
    print(f"safe_split('{text}', ',') = {safe_split(text, ',')}")  # ['a', 'b', 'c']
    print(f"safe_split(None) = {safe_split(None)}")  # []
    
    # safe_join - пропуск None
    items = ["a", None, "b", "c"]
    print(f"safe_join(', ', {items}) = '{safe_join(', ', items)}'")  # 'a, b, c'
    print(f"safe_join(', ', {items}, skip_none=False) = '{safe_join(', ', items, skip_none=False)}'")  # 'a, None, b, c'
    
    # safe_format - обработка ошибок
    template = "Hello, {name}!"
    print(f"safe_format('{template}', name='World') = '{safe_format(template, name='World')}'")  # 'Hello, World!'
    print(f"safe_format('{template}') = '{safe_format(template)}'")  # 'Hello, {name}!' (не падает)
    
    print()


def demo_real_world_usage():
    """Реальный пример использования"""
    print("=== Реальный пример: обработка данных пользователя ===\n")
    
    # Данные могут быть неполными или некорректными
    users = [
        {"name": "Иван", "age": 25, "scores": [85, 90, 88]},
        {"name": "Мария", "scores": [92, 95]},  # нет возраста
        {"name": "Петр", "age": 30},  # нет оценок
    ]
    
    print("Обработка пользователей:")
    for i, user in enumerate(users):
        # Безопасное получение данных
        name = safe_get(user, "name", "Неизвестно")
        age = safe_get(user, "age", "N/A")
        scores = safe_get(user, "scores", [])
        
        # Безопасные вычисления
        avg_score = safe_divide(safe_sum(scores), len(scores) if scores else 0, default=0)
        max_score = safe_max(scores, default=0)
        
        # Безопасное форматирование
        info = safe_format(
            "{name} ({age} лет): средний балл {avg:.1f}, максимум {max}",
            name=name,
            age=age,
            avg=avg_score,
            max=max_score
        )
        
        print(f"  {i+1}. {info}")
    
    print("\n  💡 Все данные обработаны безопасно, даже с пропущенными полями!")
    print()


if __name__ == "__main__":
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  Демонстрация отрефакторенных safe утилит fishertools    ║")
    print("║  Больше никакого 'spaghetti code'!                        ║")
    print("╚═══════════════════════════════════════════════════════════╝\n")
    
    demo_safe_divide()
    demo_safe_get()
    demo_safe_collections()
    demo_safe_strings()
    demo_real_world_usage()
    
    print("✅ Все примеры выполнены успешно!")
    print("📝 Код стал проще, понятнее и математически корректнее!")
