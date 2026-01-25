#!/usr/bin/env python3
"""
Примеры использования библиотеки FisherTools
"""

from fishertools import utils, decorators, helpers


def demo_utils():
    """Демонстрация утилит"""
    print("=== Демонстрация утилит ===")
    
    # Работа с JSON
    test_data = {"name": "Тест", "version": "1.0", "config": {"debug": True}}
    utils.write_json(test_data, "test.json")
    loaded_data = utils.read_json("test.json")
    print(f"Загруженные данные: {loaded_data}")
    
    # Плоский словарь
    flat = utils.flatten_dict(test_data)
    print(f"Плоский словарь: {flat}")
    
    # Временная метка
    print(f"Текущее время: {utils.timestamp()}")


def demo_decorators():
    """Демонстрация декораторов"""
    print("\n=== Демонстрация декораторов ===")
    
    @decorators.timer
    @decorators.debug
    def slow_function(n):
        """Медленная функция для демонстрации"""
        import time
        time.sleep(0.1)
        return n * 2
    
    result = slow_function(5)
    
    @decorators.cache_result
    def expensive_calculation(x, y):
        """Дорогая операция"""
        print(f"Выполняем вычисление для {x}, {y}")
        return x ** y
    
    # Первый вызов - вычисление
    print(expensive_calculation(2, 10))
    # Второй вызов - из кеша
    print(expensive_calculation(2, 10))
    
    @decorators.validate_types(name=str, age=int)
    def create_user(name, age):
        return f"Пользователь: {name}, возраст: {age}"
    
    try:
        print(create_user("Иван", 25))
        # Это вызовет ошибку типа
        # create_user("Иван", "25")
    except TypeError as e:
        print(f"Ошибка типа: {e}")


def demo_helpers():
    """Демонстрация помощников"""
    print("\n=== Демонстрация помощников ===")
    
    # Конфигурация
    config = helpers.QuickConfig({
        "database": {
            "host": "localhost",
            "port": 5432
        },
        "debug": True
    })
    
    print(f"DB Host: {config.get('database.host')}")
    print(f"Debug: {config.get('debug')}")
    config.set('database.name', 'myapp')
    print(f"Конфигурация: {config.to_dict()}")
    
    # Генерация пароля
    password = helpers.generate_password(16)
    print(f"Сгенерированный пароль: {password}")
    
    # Хеширование
    hash_value = helpers.hash_string("секретная строка")
    print(f"Хеш: {hash_value}")
    
    # Валидация email
    emails = ["test@example.com", "invalid-email", "user@domain.ru"]
    for email in emails:
        valid = helpers.validate_email(email)
        print(f"{email}: {'✓' if valid else '✗'}")
    
    # Разбивка списка
    big_list = list(range(20))
    chunks = helpers.chunk_list(big_list, 5)
    print(f"Разбитый список: {chunks}")
    
    # Логгер
    logger = helpers.SimpleLogger("Demo")
    logger.info("Это информационное сообщение")
    logger.warning("Это предупреждение")
    logger.error("Это ошибка")


if __name__ == "__main__":
    demo_utils()
    demo_decorators()
    demo_helpers()
    
    print("\n=== Демонстрация завершена ===")
    print("Теперь вы можете использовать библиотеку в своих проектах!")
    print("Установка: pip install fishertools")