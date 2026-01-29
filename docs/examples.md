# Examples

Practical examples demonstrating how to use Fishertools features.

## Example 1: Understanding Python Errors

### IndexError - List Index Out of Range

```python
from fishertools import explain_error

try:
    numbers = [1, 2, 3]
    print(numbers[10])  # This will cause an error
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
  Indexes in Python start at 0, and the maximum index equals the list length minus 1.

═══ How to Fix ═══
  Check the list length before accessing an element.
```

### NameError - Undefined Variable

```python
from fishertools import explain_error

try:
    print(result)  # Variable not defined
except Exception as e:
    explain_error(e)
```

### TypeError - Type Mismatch

```python
from fishertools import explain_error

try:
    age = 18
    message = "I am " + age + " years old"  # Can't add string and int
except Exception as e:
    explain_error(e)
```

### ZeroDivisionError - Division by Zero

```python
from fishertools import explain_error

try:
    result = 10 / 0
except Exception as e:
    explain_error(e)
```

## Example 2: Using Safe Utilities

### Safe Element Access

```python
from fishertools.safe import safe_get

# Safe list access
numbers = [1, 2, 3]
first = safe_get(numbers, 0, "not found")      # Returns 1
tenth = safe_get(numbers, 10, "not found")     # Returns "not found"

# Safe dictionary access
user = {"name": "Alice", "age": 30}
name = safe_get(user, "name", "unknown")       # Returns "Alice"
email = safe_get(user, "email", "no email")    # Returns "no email"
```

### Safe Division

```python
from fishertools.safe import safe_divide

# Normal division
result = safe_divide(10, 2, 0)  # Returns 5.0

# Division by zero
result = safe_divide(10, 0, 0)  # Returns 0 (default)
result = safe_divide(10, 0, -1) # Returns -1 (custom default)
```

### Safe File Reading

```python
from fishertools.safe import safe_read_file

# Read existing file
content = safe_read_file("data.txt", default="file not found")

# Read non-existent file
content = safe_read_file("missing.txt", default="file not found")
# Returns "file not found"
```

### Directory Creation

```python
from fishertools.safe import ensure_dir

# Create nested directories
path = ensure_dir("./data/users/profiles")
# Creates all intermediate directories if they don't exist
```

### File Hashing

```python
from fishertools.safe import get_file_hash

# Calculate SHA256 hash (default)
sha_hash = get_file_hash("document.pdf")

# Calculate MD5 hash
md5_hash = get_file_hash("document.pdf", algorithm='md5')

# Use for file integrity checking
original_hash = get_file_hash("backup.zip")
# ... later ...
current_hash = get_file_hash("backup.zip")
if original_hash == current_hash:
    print("File integrity verified")
```

### Reading Last Lines

```python
from fishertools.safe import read_last_lines

# Read last 10 lines of a log file
last_lines = read_last_lines("app.log", n=10)
for line in last_lines:
    print(line)

# Read last 5 lines
recent_errors = read_last_lines("error.log", n=5)
```

## Example 3: Learning Python Concepts

### Basic Concept Explanation

```python
from fishertools.learn import explain

# Learn about lists
list_info = explain("list")
print("Description:", list_info["description"])
print("When to use:", list_info["when_to_use"])
print("Example:")
print(list_info["example"])
```

### Learning Different Topics

```python
from fishertools.learn import explain

# Learn about different concepts
topics = ["int", "str", "list", "dict", "for", "if", "function"]

for topic in topics:
    info = explain(topic)
    print(f"\n=== {topic.upper()} ===")
    print(info["description"])
```

### Knowledge Engine - Detailed Topics

```python
from fishertools.learn import get_topic, list_topics, search_topics

# Get detailed information about a topic
topic = get_topic("Lists")
print("Topic:", topic["topic"])
print("Category:", topic["category"])
print("Description:", topic["description"])
print("Common mistakes:", topic["common_mistakes"])
print("Related topics:", topic["related_topics"])

# List all available topics
all_topics = list_topics()
print(f"Total topics available: {len(all_topics)}")

# Search for topics
loop_topics = search_topics("loop")
print(f"Topics about loops: {loop_topics}")
```

### Learning Path

```python
from fishertools.learn import get_learning_path

# Get recommended learning order
path = get_learning_path()
print("Recommended learning path:")
for i, topic in enumerate(path[:10], 1):
    print(f"{i}. {topic}")
```

## Example 4: Interactive Menu

```python
from fishertools.patterns import simple_menu

def show_greeting():
    print("Hello! 👋")

def show_goodbye():
    print("Goodbye! 👋")

def show_help():
    print("This is a help menu")

simple_menu({
    "Greet": show_greeting,
    "Say goodbye": show_goodbye,
    "Help": show_help
})
```

**Output:**
```
1. Greet
2. Say goodbye
3. Help
4. quit
5. exit

Choose an option (1-5): 1
Hello! 👋

Choose an option (1-5): 4
Goodbye!
```

## Example 5: JSON Data Storage

```python
from fishertools.patterns import JSONStorage

# Create storage
storage = JSONStorage("users.json")

# Save data
users = [
    {"name": "Alice", "age": 30, "email": "alice@example.com"},
    {"name": "Bob", "age": 25, "email": "bob@example.com"}
]
storage.save(users)

# Load data
loaded_users = storage.load()
print(f"Loaded {len(loaded_users)} users")

# Check if file exists
if storage.exists():
    print("User data file exists")
```

## Example 6: Application Logging

```python
from fishertools.patterns import SimpleLogger

# Create logger
logger = SimpleLogger("app.log")

# Log different types of messages
logger.info("Application started")
logger.info("User logged in: alice@example.com")
logger.warning("High memory usage detected")
logger.error("Failed to connect to database")
logger.info("Application stopped")
```

**Log file output:**
```
[2024-01-15 10:30:45] [INFO] Application started
[2024-01-15 10:30:46] [INFO] User logged in: alice@example.com
[2024-01-15 10:30:47] [WARNING] High memory usage detected
[2024-01-15 10:30:48] [ERROR] Failed to connect to database
[2024-01-15 10:30:49] [INFO] Application stopped
```

## Example 7: Command Line Application

```python
from fishertools.patterns import SimpleCLI

# Create CLI application
cli = SimpleCLI("calculator", "Simple Calculator")

# Register commands
@cli.command("add", "Add two numbers")
def add(a, b):
    result = float(a) + float(b)
    print(f"{a} + {b} = {result}")

@cli.command("subtract", "Subtract two numbers")
def subtract(a, b):
    result = float(a) - float(b)
    print(f"{a} - {b} = {result}")

@cli.command("multiply", "Multiply two numbers")
def multiply(a, b):
    result = float(a) * float(b)
    print(f"{a} * {b} = {result}")

# Run the application
if __name__ == "__main__":
    cli.run()
```

**Usage:**
```bash
python calculator.py add 5 3
# 5 + 3 = 8.0

python calculator.py multiply 4 7
# 4 * 7 = 28.0

python calculator.py --help
# Shows all available commands
```

## Example 8: Complete Application

```python
from fishertools import explain_error
from fishertools.safe import safe_get, safe_divide, safe_read_file
from fishertools.patterns import JSONStorage, SimpleLogger, simple_menu

# Initialize components
storage = JSONStorage("scores.json")
logger = SimpleLogger("game.log")

def load_scores():
    """Load scores from file"""
    scores = storage.load() if storage.exists() else []
    logger.info(f"Loaded {len(scores)} scores")
    return scores

def save_scores(scores):
    """Save scores to file"""
    storage.save(scores)
    logger.info(f"Saved {len(scores)} scores")

def add_score():
    """Add a new score"""
    try:
        name = input("Enter player name: ")
        score = int(input("Enter score: "))
        scores = load_scores()
        scores.append({"name": name, "score": score})
        save_scores(scores)
        logger.info(f"Added score for {name}: {score}")
        print("Score added!")
    except Exception as e:
        explain_error(e)

def show_scores():
    """Display all scores"""
    scores = load_scores()
    if not scores:
        print("No scores yet")
        return
    
    print("\n=== High Scores ===")
    for i, entry in enumerate(scores, 1):
        print(f"{i}. {entry['name']}: {entry['score']}")

def calculate_average():
    """Calculate average score"""
    scores = load_scores()
    if not scores:
        print("No scores to calculate")
        return
    
    total = sum(s["score"] for s in scores)
    average = safe_divide(total, len(scores), 0)
    print(f"Average score: {average:.2f}")

# Main menu
simple_menu({
    "Add Score": add_score,
    "Show Scores": show_scores,
    "Calculate Average": calculate_average
})
```

---

Return to [Documentation Index](index.md)
