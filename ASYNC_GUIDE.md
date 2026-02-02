# Руководство по асинхронным возможностям fishertools

## Введение

Начиная с версии 0.4.6, fishertools поддерживает асинхронное программирование (async/await). Это позволяет создавать высокопроизводительные приложения, которые не блокируют event loop.

## Когда использовать async версии?

### ✅ Используйте async версии когда:
- Пишете веб-приложения (FastAPI, aiohttp, Sanic)
- Работаете с множеством файлов одновременно
- Нужна высокая производительность I/O операций
- Уже используете asyncio в проекте

### ❌ Используйте обычные версии когда:
- Пишете простые скрипты
- Работаете с одним файлом за раз
- Не знакомы с async/await
- Проект не использует asyncio

## AsyncSimpleLogger

### Базовое использование

```python
import asyncio
from fishertools.async_logger import AsyncSimpleLogger

async def main():
    logger = AsyncSimpleLogger("app.log")
    
    await logger.info("Приложение запущено")
    await logger.warning("Низкая память")
    await logger.error("Ошибка подключения")

asyncio.run(main())
```

### Использование в FastAPI

```python
from fastapi import FastAPI
from fishertools.async_logger import AsyncSimpleLogger

app = FastAPI()
logger = AsyncSimpleLogger("api.log")

@app.get("/")
async def root():
    await logger.info("Получен запрос на /")
    return {"message": "Hello World"}

@app.post("/data")
async def create_data(data: dict):
    await logger.info(f"Создание данных: {data}")
    # ... обработка данных
    await logger.info("Данные успешно созданы")
    return {"status": "success"}
```

### Логирование в нескольких задачах

```python
import asyncio
from fishertools.async_logger import AsyncSimpleLogger

async def process_user(user_id: int, logger: AsyncSimpleLogger):
    await logger.info(f"Обработка пользователя {user_id}")
    await asyncio.sleep(1)  # Имитация работы
    await logger.info(f"Пользователь {user_id} обработан")

async def main():
    logger = AsyncSimpleLogger("users.log")
    
    # Обработка 10 пользователей параллельно
    tasks = [process_user(i, logger) for i in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

## Async Safe Utilities

### Чтение файлов

```python
import asyncio
from fishertools.async_safe import async_safe_read_file

async def read_config():
    # С значением по умолчанию
    config = await async_safe_read_file("config.json", default="{}")
    print(f"Конфигурация: {config}")
    
    # Без значения по умолчанию
    data = await async_safe_read_file("data.txt")
    if data is None:
        print("Файл не найден")
    else:
        print(f"Данные: {data}")

asyncio.run(read_config())
```

### Запись файлов

```python
import asyncio
from fishertools.async_safe import async_safe_write_file

async def save_report():
    report = "Отчет за день\n" + "=" * 20 + "\n"
    report += "Всего операций: 100\n"
    
    success = await async_safe_write_file("report.txt", report)
    
    if success:
        print("Отчет сохранен")
    else:
        print("Ошибка сохранения отчета")

asyncio.run(save_report())
```

### Работа со списком файлов

```python
import asyncio
from fishertools.async_safe import (
    async_safe_list_files,
    async_safe_read_file,
    async_safe_get_file_size
)

async def process_all_logs():
    # Получить все .log файлы
    log_files = await async_safe_list_files("logs", pattern="*.log")
    
    print(f"Найдено {len(log_files)} файлов логов")
    
    # Обработать все файлы параллельно
    tasks = []
    for log_file in log_files:
        tasks.append(process_log_file(log_file))
    
    results = await asyncio.gather(*tasks)
    return results

async def process_log_file(file_path: str):
    # Получить размер
    size = await async_safe_get_file_size(file_path)
    
    # Прочитать содержимое
    content = await async_safe_read_file(file_path)
    
    if content:
        lines = content.count('\n')
        return {
            "file": file_path,
            "size": size,
            "lines": lines
        }
    return None

asyncio.run(process_all_logs())
```

### Проверка существования файлов

```python
import asyncio
from fishertools.async_safe import (
    async_safe_file_exists,
    async_safe_read_file,
    async_safe_write_file
)

async def ensure_config():
    # Проверить существование
    if not await async_safe_file_exists("config.json"):
        # Создать конфигурацию по умолчанию
        default_config = '{"debug": false, "port": 8000}'
        await async_safe_write_file("config.json", default_config)
        print("Создана конфигурация по умолчанию")
    
    # Прочитать конфигурацию
    config = await async_safe_read_file("config.json")
    return config

asyncio.run(ensure_config())
```

## Параллельная обработка файлов

### Чтение множества файлов

```python
import asyncio
from fishertools.async_safe import async_safe_read_file

async def read_all_configs():
    config_files = [
        "config/database.json",
        "config/api.json",
        "config/cache.json",
        "config/logging.json"
    ]
    
    # Читаем все файлы параллельно
    tasks = [async_safe_read_file(f, default="{}") for f in config_files]
    configs = await asyncio.gather(*tasks)
    
    # Обработка результатов
    for file, content in zip(config_files, configs):
        print(f"{file}: {len(content)} байт")
    
    return configs

asyncio.run(read_all_configs())
```

### Запись множества файлов

```python
import asyncio
from fishertools.async_safe import async_safe_write_file

async def generate_reports():
    reports = {
        "daily.txt": "Дневной отчет",
        "weekly.txt": "Недельный отчет",
        "monthly.txt": "Месячный отчет"
    }
    
    # Записываем все файлы параллельно
    tasks = [
        async_safe_write_file(f"reports/{name}", content)
        for name, content in reports.items()
    ]
    
    results = await asyncio.gather(*tasks)
    
    success_count = sum(results)
    print(f"Создано {success_count} из {len(reports)} отчетов")

asyncio.run(generate_reports())
```

## Комбинирование с другими async библиотеками

### С aiohttp (HTTP клиент)

```python
import asyncio
import aiohttp
from fishertools.async_logger import AsyncSimpleLogger
from fishertools.async_safe import async_safe_write_file

async def download_and_log(url: str, filename: str):
    logger = AsyncSimpleLogger("downloads.log")
    
    await logger.info(f"Начало загрузки: {url}")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            
            # Сохранить файл
            success = await async_safe_write_file(filename, content)
            
            if success:
                await logger.info(f"Загружено: {filename}")
            else:
                await logger.error(f"Ошибка сохранения: {filename}")

asyncio.run(download_and_log("https://example.com", "page.html"))
```

### С asyncpg (PostgreSQL)

```python
import asyncio
import asyncpg
from fishertools.async_logger import AsyncSimpleLogger

async def process_database():
    logger = AsyncSimpleLogger("database.log")
    
    await logger.info("Подключение к базе данных")
    
    conn = await asyncpg.connect(
        user='user', password='password',
        database='mydb', host='localhost'
    )
    
    await logger.info("Выполнение запроса")
    rows = await conn.fetch('SELECT * FROM users')
    
    await logger.info(f"Получено {len(rows)} записей")
    
    await conn.close()
    await logger.info("Соединение закрыто")

asyncio.run(process_database())
```

## Производительность

### Сравнение: синхронный vs асинхронный

```python
import asyncio
import time
from fishertools.safe import safe_read_file
from fishertools.async_safe import async_safe_read_file

# Синхронная версия
def sync_read_files(files):
    start = time.time()
    results = [safe_read_file(f) for f in files]
    return time.time() - start

# Асинхронная версия
async def async_read_files(files):
    start = time.time()
    tasks = [async_safe_read_file(f) for f in files]
    results = await asyncio.gather(*tasks)
    return time.time() - start

# Тест
files = [f"data/file{i}.txt" for i in range(100)]

sync_time = sync_read_files(files)
async_time = asyncio.run(async_read_files(files))

print(f"Синхронно: {sync_time:.2f}s")
print(f"Асинхронно: {async_time:.2f}s")
print(f"Ускорение: {sync_time/async_time:.1f}x")
```

## Лучшие практики

### 1. Используйте context managers для ресурсов

```python
import asyncio
from contextlib import asynccontextmanager
from fishertools.async_logger import AsyncSimpleLogger

@asynccontextmanager
async def get_logger(filename):
    logger = AsyncSimpleLogger(filename)
    await logger.info("Логгер инициализирован")
    try:
        yield logger
    finally:
        await logger.info("Логгер закрыт")

async def main():
    async with get_logger("app.log") as logger:
        await logger.info("Работа приложения")

asyncio.run(main())
```

### 2. Обрабатывайте ошибки правильно

```python
import asyncio
from fishertools.async_safe import async_safe_read_file
from fishertools.async_logger import AsyncSimpleLogger

async def safe_process_file(filename: str, logger: AsyncSimpleLogger):
    try:
        content = await async_safe_read_file(filename)
        if content is None:
            await logger.warning(f"Файл не найден: {filename}")
            return None
        
        # Обработка содержимого
        await logger.info(f"Обработан файл: {filename}")
        return content
        
    except Exception as e:
        await logger.error(f"Ошибка обработки {filename}: {e}")
        return None
```

### 3. Используйте семафоры для ограничения параллелизма

```python
import asyncio
from fishertools.async_safe import async_safe_read_file

async def process_with_limit(files, max_concurrent=5):
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def process_one(file):
        async with semaphore:
            return await async_safe_read_file(file)
    
    tasks = [process_one(f) for f in files]
    return await asyncio.gather(*tasks)

# Обработка 100 файлов, но не более 5 одновременно
files = [f"data/file{i}.txt" for i in range(100)]
results = asyncio.run(process_with_limit(files))
```

## Миграция с синхронного кода

### До (синхронный):
```python
from fishertools.patterns import SimpleLogger
from fishertools.safe import safe_read_file

logger = SimpleLogger("app.log")
logger.info("Начало работы")

content = safe_read_file("data.txt")
logger.info(f"Прочитано {len(content)} байт")
```

### После (асинхронный):
```python
import asyncio
from fishertools.async_logger import AsyncSimpleLogger
from fishertools.async_safe import async_safe_read_file

async def main():
    logger = AsyncSimpleLogger("app.log")
    await logger.info("Начало работы")
    
    content = await async_safe_read_file("data.txt")
    await logger.info(f"Прочитано {len(content)} байт")

asyncio.run(main())
```

## Заключение

Асинхронные версии fishertools позволяют:
- ✅ Не блокировать event loop
- ✅ Обрабатывать множество операций параллельно
- ✅ Интегрироваться с async фреймворками
- ✅ Повысить производительность I/O операций

Используйте их в современных async приложениях для максимальной производительности! 🚀
