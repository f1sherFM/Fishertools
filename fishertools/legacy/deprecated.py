"""
Deprecated functions from original fishertools library

These functions are retained for backward compatibility and align with the new
mission of making Python more convenient and safer for beginners. All functions
maintain identical behavior to the original implementation.
"""

import time
import hashlib
import functools
from typing import Any, Dict, List, Callable

from .. import helpers as _helpers
from .. import utils as _utils

# File and directory utilities - helpful for beginners
read_json = _utils.read_json
write_json = _utils.write_json
ensure_dir = _utils.ensure_dir
get_file_size = _utils.get_file_size
list_files = _utils.list_files
timestamp = _utils.timestamp
flatten_dict = _utils.flatten_dict


# String utilities - common beginner needs
def validate_email(email: str) -> bool:
    """Проверяет корректность email адреса"""
    return bool(_helpers._EMAIL_PATTERN.match(email))


def clean_string(text: str) -> str:
    """Очищает строку от лишних пробелов и символов"""
    # Убираем лишние пробелы
    text = _helpers._WHITESPACE_PATTERN.sub(' ', text.strip())
    # Убираем специальные символы (оставляем только буквы, цифры, пробелы и основную пунктуацию)
    text = _helpers._SPECIAL_CHARS_PATTERN.sub('', text)
    return text


# Data utilities - safe operations for beginners
def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Разбивает список на части заданного размера"""
    if chunk_size > 0:
        return _helpers.chunk_list(lst, chunk_size)
    # Сохраняем legacy-поведение:
    # chunk_size == 0 -> ValueError от range()
    # chunk_size < 0 -> []
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Объединяет несколько словарей в один"""
    return _helpers.merge_dicts(*dicts)


# Security utilities - helpful for beginners
def generate_password(length: int = 12, include_symbols: bool = True) -> str:
    """Генерирует случайный пароль"""
    # Legacy: length <= 0 возвращает пустую строку вместо ValueError
    if length <= 0:
        return ""
    return _helpers.generate_password(length, include_symbols)


def hash_string(text: str, algorithm: str = 'sha256') -> str:
    """Хеширует строку указанным алгоритмом"""
    try:
        return _helpers.hash_string(text, algorithm)
    except ValueError:
        # Сохраняем legacy-тип исключения и сообщение от hashlib.new(...)
        hashlib.new(algorithm)
        raise


# Helper classes - simplified for beginners
QuickConfig = _helpers.QuickConfig
SimpleLogger = _helpers.SimpleLogger


# Educational decorators - help beginners understand code behavior
def timer(func: Callable) -> Callable:
    """Декоратор для измерения времени выполнения функции"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} выполнилась за {end_time - start_time:.4f} секунд")
        return result
    return wrapper


def debug(func: Callable) -> Callable:
    """Декоратор для отладки - выводит аргументы и результат функции"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Вызов {func.__name__} с аргументами: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} вернула: {result}")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Декоратор для повторных попыток выполнения функции при ошибке"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Попытка {attempt + 1} не удалась: {e}. Повтор через {delay} сек...")
                    time.sleep(delay)
        return wrapper
    return decorator


def cache_result(func: Callable) -> Callable:
    """Простой декоратор для кеширования результатов функции"""
    cache = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Создаем ключ из аргументов
        key = str(args) + str(sorted(kwargs.items()))
        
        if key in cache:
            print(f"Результат {func.__name__} взят из кеша")
            return cache[key]
        
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    
    return wrapper


def validate_types(**expected_types):
    """Декоратор для проверки типов аргументов функции"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Получаем имена параметров функции
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Проверяем типы
            for param_name, expected_type in expected_types.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"Параметр '{param_name}' должен быть типа {expected_type.__name__}, "
                            f"получен {type(value).__name__}"
                        )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
