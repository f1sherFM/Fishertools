# Interactive Example Template

This template shows the required structure for interactive code examples in the Fishertools documentation.

## Template Structure

```markdown
# Example: [Brief Title]

**Module**: [errors|safe|learn|patterns|config|documentation]
**Difficulty**: [beginner|intermediate|advanced]
**Tags**: [comma-separated tags]

## Code

\`\`\`python
# Your Python code here
# Make sure it's syntactically correct and executable
\`\`\`

## Expected Output

\`\`\`
output from running the code
\`\`\`

## Explanation

Explain what the code does and why it's useful. This should be beginner-friendly and clear.

## Variations

- **Variation 1**: Description of how to modify the code
- **Variation 2**: Another way to use this feature

## Related Examples

- [Link to related example](./other-example.md)
```

## Required Fields

- **Title**: Brief, descriptive title for the example
- **Module**: One of: errors, safe, learn, patterns, config, documentation
- **Difficulty**: One of: beginner, intermediate, advanced
- **Code**: Valid, executable Python code
- **Expected Output**: The output when the code is run
- **Explanation**: Clear explanation of what the code does
- **Tags**: Comma-separated keywords for searching

## Optional Fields

- **Variations**: Alternative ways to use the feature
- **Related Examples**: Links to similar examples

## Best Practices

### Code Quality

1. **Keep it simple**: Examples should be easy to understand
2. **Make it runnable**: Code must execute without errors
3. **Show output**: Include expected output so users can verify
4. **Add comments**: Use comments to explain complex parts

### Explanation Quality

1. **Use simple language**: Avoid jargon or explain technical terms
2. **Explain the "why"**: Not just what the code does, but why it's useful
3. **Start with basics**: Begin with simple concepts before advanced ones
4. **Include context**: Explain when and where to use this pattern

### Organization

1. **One concept per example**: Focus on a single feature or pattern
2. **Progressive difficulty**: Order examples from simple to complex
3. **Use consistent formatting**: Follow the template structure
4. **Tag appropriately**: Use tags that help users find related examples

## Example: Safe Division

**Module**: safe
**Difficulty**: beginner
**Tags**: division, error-handling, safe-operations

## Code

```python
from fishertools.safe import safe_divide

# Safe division with default value
result = safe_divide(10, 2)
print(f"10 / 2 = {result}")

# Division by zero returns default
result = safe_divide(10, 0, default=0)
print(f"10 / 0 = {result}")

# Custom default value
result = safe_divide(10, 0, default=-1)
print(f"10 / 0 with default -1 = {result}")
```

## Expected Output

```
10 / 2 = 5.0
10 / 0 = 0
10 / 0 with default -1 = -1
```

## Explanation

The `safe_divide()` function performs division safely by catching division by zero errors. Instead of raising an exception, it returns a default value. This is useful when you want to handle division by zero gracefully without using try-except blocks.

## Variations

- **Using with floats**: Works with any numeric types
- **Custom error handling**: Combine with error explanation for debugging
- **Chaining operations**: Use in data processing pipelines

## Related Examples

- [Error Explanation](./error-explanation.md)
- [Safe Operations Overview](./safe-overview.md)

## File Naming Convention

Save examples with the following naming pattern:

```
docs/interactive-examples/{module}/{example-name}.md
```

Examples:
- `docs/interactive-examples/errors/error-explanation.md`
- `docs/interactive-examples/safe/safe-division.md`
- `docs/interactive-examples/learn/learning-patterns.md`

## Validation

All examples are validated for:

1. **Syntax**: Code must be valid Python
2. **Execution**: Code must run without errors
3. **Output**: Actual output must match expected output
4. **Completeness**: All required fields must be present
5. **Accessibility**: Examples must be understandable to beginners

## Adding Examples

1. Create a new markdown file in the appropriate module directory
2. Follow the template structure
3. Ensure code is syntactically correct
4. Test the code locally to verify output
5. Add appropriate tags and difficulty level
6. Submit for review

## Questions?

If you have questions about creating examples, refer to the [Best Practices Guide](../best-practices/examples.md) or ask in the community.
