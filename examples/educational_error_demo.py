"""
Demonstration of the Educational Error Wrapper.

This example shows how fishertools provides beginner-friendly
error explanations for common Python errors.
"""

from fishertools.errors import (
    EducationalErrorWrapper,
    explain_exception,
    with_educational_errors
)


def demo_import_error():
    """Demonstrate educational explanation for import errors."""
    print("=" * 70)
    print("DEMO 1: Import Error Explanation")
    print("=" * 70)
    
    wrapper = EducationalErrorWrapper()
    
    try:
        import nonexistent_module
    except ImportError as e:
        explanation = wrapper.enhance_import_error(e)
        print(explanation)


def demo_file_error():
    """Demonstrate educational explanation for file errors."""
    print("\n" + "=" * 70)
    print("DEMO 2: File Not Found Error Explanation")
    print("=" * 70)
    
    wrapper = EducationalErrorWrapper()
    
    try:
        with open("nonexistent_file.txt", "r") as f:
            data = f.read()
    except FileNotFoundError as e:
        explanation = wrapper.enhance_file_error(e)
        print(explanation)


def demo_wrap_error():
    """Demonstrate the general wrap_error method."""
    print("\n" + "=" * 70)
    print("DEMO 3: General Error Wrapping")
    print("=" * 70)
    
    wrapper = EducationalErrorWrapper()
    
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        explanation = wrapper.wrap_error(e, "dividing numbers")
        print(explanation)


def demo_convenience_function():
    """Demonstrate the convenience function."""
    print("\n" + "=" * 70)
    print("DEMO 4: Convenience Function")
    print("=" * 70)
    
    try:
        my_list = [1, 2, 3]
        value = my_list[10]
    except IndexError as e:
        explanation = explain_exception(e, "accessing list element")
        print(explanation)


@with_educational_errors("calculating average")
def calculate_average(numbers):
    """Calculate average with educational error handling."""
    return sum(numbers) / len(numbers)


def demo_decorator():
    """Demonstrate the decorator."""
    print("\n" + "=" * 70)
    print("DEMO 5: Decorator Usage")
    print("=" * 70)
    
    try:
        # This will cause a ZeroDivisionError
        result = calculate_average([])
    except ZeroDivisionError as e:
        print(f"Caught error: {e}")
        print("(Educational message was logged)")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "EDUCATIONAL ERROR WRAPPER DEMO" + " " * 23 + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    # Run all demos
    demo_import_error()
    demo_file_error()
    demo_wrap_error()
    demo_convenience_function()
    demo_decorator()
    
    print("\n" + "=" * 70)
    print("All demos completed!")
    print("=" * 70)
