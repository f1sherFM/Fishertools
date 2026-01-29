# API Reference

Complete documentation of all Fishertools functions and classes.

## Main Module: fishertools

### explain_error()

Explains Python errors in clear, understandable language.

**Signature:**
```python
explain_error(exception: Exception) -> None
```

**Parameters:**
- `exception` (Exception): The exception object to explain

**Returns:** None (prints explanation to console)

**Supported Error Types:**
- TypeError
- ValueError
- IndexError
- KeyError
- NameError
- AttributeError
- ImportError
- FileNotFoundError
- ZeroDivisionError
- SyntaxError (with limitations)

**Example:**
```python
from fishertools import explain_error

try:
    numbers = [1, 2, 3]
    print(numbers[10])
except Exception as e:
    explain_error(e)
```

**Output:**
```
🚨 Error Python: IndexError

═══ Error Message ═══
  list index out of range

═══ What This Means ═══
  You're trying to access a list element by an index that doesn't exist.

═══ How to Fix ═══
  Check the list length before accessing an element.

═══ Example ═══
┌─ Correct Code ─┐
    numbers = [1, 2, 3]
    if len(numbers) > 10:
        print(numbers[10])
└─────────────────┘
```

---

## Module: fishertools.safe

Safe functions that prevent common beginner mistakes.

### safe_get()

Safely access elements from lists or dictionaries.

**Signature:**
```python
safe_get(collection, index, default=None)
```

**Parameters:**
- `collection` (list or dict): The collection to access
- `index` (int or str): The index or key to access
- `default` (any): Value to return if index/key doesn't exist

**Returns:** Element at index/key or default value

**Example:**
```python
from fishertools.safe import safe_get

numbers = [1, 2, 3]
result = safe_get(numbers, 10, "not found")  # Returns "not found"

data = {"name": "Alice"}
age = safe_get(data, "age", 0)  # Returns 0
```

### safe_divide()

Divide numbers safely without ZeroDivisionError.

**Signature:**
```python
safe_divide(a, b, default=0)
```

**Parameters:**
- `a` (number): Dividend
- `b` (number): Divisor
- `default` (number): Value to return if b is 0

**Returns:** a / b or default if b is 0

**Example:**
```python
from fishertools.safe import safe_divide

result = safe_divide(10, 0, 0)  # Returns 0
result = safe_divide(10, 2, 0)  # Returns 5.0
```

### safe_max()

Find maximum value safely.

**Signature:**
```python
safe_max(collection, default=None)
```

**Parameters:**
- `collection` (list): Collection to find max from
- `default` (any): Value to return if collection is empty

**Returns:** Maximum value or default

**Example:**
```python
from fishertools.safe import safe_max

result = safe_max([1, 2, 3], 0)  # Returns 3
result = safe_max([], 0)  # Returns 0
```

### safe_min()

Find minimum value safely.

**Signature:**
```python
safe_min(collection, default=None)
```

**Parameters:**
- `collection` (list): Collection to find min from
- `default` (any): Value to return if collection is empty

**Returns:** Minimum value or default

**Example:**
```python
from fishertools.safe import safe_min

result = safe_min([1, 2, 3], 0)  # Returns 1
result = safe_min([], 0)  # Returns 0
```

### safe_sum()

Sum collection elements safely.

**Signature:**
```python
safe_sum(collection, default=0)
```

**Parameters:**
- `collection` (list): Collection to sum
- `default` (number): Value to return if collection is empty

**Returns:** Sum of elements or default

**Example:**
```python
from fishertools.safe import safe_sum

result = safe_sum([1, 2, 3], 0)  # Returns 6
result = safe_sum([], 0)  # Returns 0
```

### safe_read_file()

Read file contents safely.

**Signature:**
```python
safe_read_file(path, default="", encoding='utf-8')
```

**Parameters:**
- `path` (str): Path to file
- `default` (str): Value to return if file doesn't exist
- `encoding` (str): File encoding (default: 'utf-8')

**Returns:** File contents or default

**Example:**
```python
from fishertools.safe import safe_read_file

content = safe_read_file("file.txt", default="file not found")
```

### ensure_dir()

Create directories recursively.

**Signature:**
```python
ensure_dir(path)
```

**Parameters:**
- `path` (str): Directory path to create

**Returns:** Created path

**Example:**
```python
from fishertools.safe import ensure_dir

path = ensure_dir("./data/nested/directory")
```

### get_file_hash()

Calculate file hash.

**Signature:**
```python
get_file_hash(path, algorithm='sha256')
```

**Parameters:**
- `path` (str): Path to file
- `algorithm` (str): Hash algorithm ('sha256', 'md5', etc.)

**Returns:** Hash string

**Example:**
```python
from fishertools.safe import get_file_hash

sha_hash = get_file_hash("data.txt")
md5_hash = get_file_hash("data.txt", algorithm='md5')
```

### read_last_lines()

Read last N lines from file.

**Signature:**
```python
read_last_lines(path, n=10, encoding='utf-8')
```

**Parameters:**
- `path` (str): Path to file
- `n` (int): Number of lines to read
- `encoding` (str): File encoding

**Returns:** List of last N lines

**Example:**
```python
from fishertools.safe import read_last_lines

last_lines = read_last_lines("log.txt", n=10)
```

---

## Module: fishertools.learn

Learning and educational tools.

### explain()

Get structured explanation of Python concepts.

**Signature:**
```python
explain(topic: str) -> dict
```

**Parameters:**
- `topic` (str): Topic name (e.g., "list", "for", "function")

**Returns:** Dictionary with keys: "description", "when_to_use", "example"

**Example:**
```python
from fishertools.learn import explain

explanation = explain("list")
print(explanation["description"])
print(explanation["when_to_use"])
print(explanation["example"])
```

### get_topic()

Get detailed information about a Python topic.

**Signature:**
```python
get_topic(topic_name: str) -> dict
```

**Parameters:**
- `topic_name` (str): Topic name

**Returns:** Dictionary with topic information

**Example:**
```python
from fishertools.learn import get_topic

topic = get_topic("Lists")
print(topic["description"])
print(topic["common_mistakes"])
```

### list_topics()

Get list of all available topics.

**Signature:**
```python
list_topics() -> list
```

**Returns:** List of topic names

**Example:**
```python
from fishertools.learn import list_topics

topics = list_topics()
print(f"Total topics: {len(topics)}")
```

### search_topics()

Search for topics by keyword.

**Signature:**
```python
search_topics(keyword: str) -> list
```

**Parameters:**
- `keyword` (str): Search keyword

**Returns:** List of matching topics

**Example:**
```python
from fishertools.learn import search_topics

results = search_topics("loop")
print(f"Found {len(results)} topics about loops")
```

### get_learning_path()

Get recommended learning path.

**Signature:**
```python
get_learning_path() -> list
```

**Returns:** List of topics in recommended order

**Example:**
```python
from fishertools.learn import get_learning_path

path = get_learning_path()
for i, topic in enumerate(path[:5], 1):
    print(f"{i}. {topic}")
```

---

## Module: fishertools.patterns

Ready-made patterns for common tasks.

### simple_menu()

Create interactive console menu.

**Signature:**
```python
simple_menu(options: dict) -> None
```

**Parameters:**
- `options` (dict): Dictionary of option names to functions

**Example:**
```python
from fishertools.patterns import simple_menu

simple_menu({
    "Option 1": lambda: print("Selected 1"),
    "Option 2": lambda: print("Selected 2")
})
```

### JSONStorage

Class for saving and loading JSON data.

**Methods:**

#### save()
```python
save(data: any) -> None
```
Save data to JSON file.

#### load()
```python
load() -> any
```
Load data from JSON file.

#### exists()
```python
exists() -> bool
```
Check if file exists.

**Example:**
```python
from fishertools.patterns import JSONStorage

storage = JSONStorage("data.json")
storage.save({"name": "Alice"})
data = storage.load()
```

### SimpleLogger

Class for logging messages.

**Methods:**

#### info()
```python
info(message: str) -> None
```
Log info message.

#### warning()
```python
warning(message: str) -> None
```
Log warning message.

#### error()
```python
error(message: str) -> None
```
Log error message.

**Example:**
```python
from fishertools.patterns import SimpleLogger

logger = SimpleLogger("app.log")
logger.info("Application started")
logger.warning("Low memory")
logger.error("Connection failed")
```

### SimpleCLI

Class for creating CLI applications.

**Methods:**

#### command()
```python
@cli.command(name: str, help: str)
def command_function(*args):
    pass
```
Register a command.

#### run()
```python
run() -> None
```
Run the CLI application.

**Example:**
```python
from fishertools.patterns import SimpleCLI

cli = SimpleCLI("myapp", "My Application")

@cli.command("greet", "Greet a user")
def greet(name):
    print(f"Hello, {name}!")

cli.run()
```

---

## Module: fishertools.legacy

Legacy functions from previous versions.

### hash_string()

Hash a string using SHA256.

**Signature:**
```python
hash_string(text: str) -> str
```

### generate_password()

Generate a random password.

**Signature:**
```python
generate_password(length: int) -> str
```

### QuickConfig

Configuration management class.

**Example:**
```python
from fishertools.legacy import QuickConfig

config = QuickConfig({"debug": True})
```

---

Return to [Documentation Index](index.md)
