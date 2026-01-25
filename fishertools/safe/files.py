"""
Safe file operations for beginners.

This module provides safe file handling utilities that prevent common
file-related errors and provide helpful error messages.
"""

import os
from pathlib import Path
from typing import Union, Optional, List


def safe_read_file(filepath: Union[str, Path], encoding: str = 'utf-8', default: str = '') -> str:
    """
    Safely read a file with comprehensive error handling.
    
    Предотвращает ошибки FileNotFoundError, PermissionError и UnicodeDecodeError,
    возвращая значение по умолчанию вместо исключения.
    
    Args:
        filepath: Путь к файлу (строка или Path объект)
        encoding: Кодировка файла (по умолчанию utf-8)
        default: Значение по умолчанию при ошибке чтения
        
    Returns:
        Содержимое файла или значение по умолчанию
        
    Raises:
        SafeUtilityError: If filepath is None or invalid type
        
    Examples:
        >>> safe_read_file("example.txt")
        'содержимое файла'
        >>> safe_read_file("несуществующий.txt", default="файл не найден")
        'файл не найден'
    """
    from ..errors.exceptions import SafeUtilityError
    
    if filepath is None:
        raise SafeUtilityError("Путь к файлу не может быть None", utility_name="safe_read_file")
    
    if not isinstance(filepath, (str, Path)):
        raise SafeUtilityError(f"Путь к файлу должен быть строкой или Path объектом, получен {type(filepath).__name__}", 
                             utility_name="safe_read_file")
    
    if not isinstance(encoding, str):
        raise SafeUtilityError(f"Кодировка должна быть строкой, получен {type(encoding).__name__}", 
                             utility_name="safe_read_file")
    
    try:
        with open(filepath, 'r', encoding=encoding) as file:
            return file.read()
    except FileNotFoundError:
        return default
    except PermissionError:
        return default
    except UnicodeDecodeError:
        return default
    except OSError:
        # Covers other OS-related errors
        return default


def safe_write_file(filepath: Union[str, Path], content: str, encoding: str = 'utf-8', 
                   create_dirs: bool = True) -> bool:
    """
    Safely write content to a file with error handling.
    
    Предотвращает ошибки при записи файла и может создавать директории.
    
    Args:
        filepath: Путь к файлу
        content: Содержимое для записи
        encoding: Кодировка файла
        create_dirs: Создавать ли директории если они не существуют
        
    Returns:
        True если запись успешна, False при ошибке
        
    Raises:
        SafeUtilityError: If arguments have invalid types
        
    Examples:
        >>> safe_write_file("output.txt", "Hello World")
        True
        >>> safe_write_file("/invalid/path/file.txt", "content", create_dirs=False)
        False
    """
    from ..errors.exceptions import SafeUtilityError
    
    if filepath is None:
        raise SafeUtilityError("Путь к файлу не может быть None", utility_name="safe_write_file")
    
    if not isinstance(filepath, (str, Path)):
        raise SafeUtilityError(f"Путь к файлу должен быть строкой или Path объектом, получен {type(filepath).__name__}", 
                             utility_name="safe_write_file")
    
    if not isinstance(content, str):
        raise SafeUtilityError(f"Содержимое должно быть строкой, получен {type(content).__name__}", 
                             utility_name="safe_write_file")
    
    if not isinstance(encoding, str):
        raise SafeUtilityError(f"Кодировка должна быть строкой, получен {type(encoding).__name__}", 
                             utility_name="safe_write_file")
    
    try:
        filepath = Path(filepath)
        
        # Create directories if requested
        if create_dirs and filepath.parent != filepath:
            filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding=encoding) as file:
            file.write(content)
        return True
    except (PermissionError, OSError, UnicodeEncodeError):
        return False


def safe_file_exists(filepath: Union[str, Path]) -> bool:
    """
    Safely check if a file exists.
    
    Предотвращает ошибки при проверке существования файла.
    
    Args:
        filepath: Путь к файлу
        
    Returns:
        True если файл существует, False иначе
        
    Raises:
        SafeUtilityError: If filepath is None or invalid type
        
    Examples:
        >>> safe_file_exists("example.txt")
        True
        >>> safe_file_exists("несуществующий.txt")
        False
    """
    from ..errors.exceptions import SafeUtilityError
    
    if filepath is None:
        raise SafeUtilityError("Путь к файлу не может быть None", utility_name="safe_file_exists")
    
    if not isinstance(filepath, (str, Path)):
        raise SafeUtilityError(f"Путь к файлу должен быть строкой или Path объектом, получен {type(filepath).__name__}", 
                             utility_name="safe_file_exists")
    
    try:
        return Path(filepath).exists() and Path(filepath).is_file()
    except (OSError, ValueError):
        return False


def safe_get_file_size(filepath: Union[str, Path], default: int = 0) -> int:
    """
    Safely get file size in bytes.
    
    Предотвращает ошибки при получении размера файла.
    
    Args:
        filepath: Путь к файлу
        default: Значение по умолчанию при ошибке
        
    Returns:
        Размер файла в байтах или значение по умолчанию
        
    Raises:
        SafeUtilityError: If filepath is None or invalid type
        
    Examples:
        >>> safe_get_file_size("example.txt")
        1024
        >>> safe_get_file_size("несуществующий.txt")
        0
    """
    from ..errors.exceptions import SafeUtilityError
    
    if filepath is None:
        raise SafeUtilityError("Путь к файлу не может быть None", utility_name="safe_get_file_size")
    
    if not isinstance(filepath, (str, Path)):
        raise SafeUtilityError(f"Путь к файлу должен быть строкой или Path объектом, получен {type(filepath).__name__}", 
                             utility_name="safe_get_file_size")
    
    try:
        return Path(filepath).stat().st_size
    except (OSError, FileNotFoundError):
        return default


def safe_list_files(directory: Union[str, Path], pattern: str = "*", default: Optional[List[str]] = None) -> List[str]:
    """
    Safely list files in a directory.
    
    Предотвращает ошибки при чтении содержимого директории.
    
    Args:
        directory: Путь к директории
        pattern: Паттерн для фильтрации файлов (например, "*.txt")
        default: Значение по умолчанию при ошибке
        
    Returns:
        Список имен файлов или значение по умолчанию
        
    Raises:
        SafeUtilityError: If directory is None or invalid type
        
    Examples:
        >>> safe_list_files(".")
        ['file1.txt', 'file2.py']
        >>> safe_list_files("несуществующая_папка")
        []
    """
    from ..errors.exceptions import SafeUtilityError
    
    if default is None:
        default = []
    
    if directory is None:
        raise SafeUtilityError("Путь к директории не может быть None", utility_name="safe_list_files")
    
    if not isinstance(directory, (str, Path)):
        raise SafeUtilityError(f"Путь к директории должен быть строкой или Path объектом, получен {type(directory).__name__}", 
                             utility_name="safe_list_files")
    
    if not isinstance(pattern, str):
        raise SafeUtilityError(f"Паттерн должен быть строкой, получен {type(pattern).__name__}", 
                             utility_name="safe_list_files")
    
    try:
        directory_path = Path(directory)
        if not directory_path.exists() or not directory_path.is_dir():
            return default
        
        files = [f.name for f in directory_path.glob(pattern) if f.is_file()]
        return sorted(files)
    except (OSError, ValueError):
        return default