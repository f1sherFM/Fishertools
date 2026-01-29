# Extended Documentation Style Guide

## Overview

This style guide defines formatting conventions, naming conventions, code example standards, and diagram standards for the Extended Documentation system.

## Formatting Conventions

### Headings
- Use markdown headings (# for H1, ## for H2, etc.)
- H1 reserved for page title
- Use H2 for major sections
- Use H3 for subsections
- Use H4 for sub-subsections

### Text Formatting
- Use **bold** for emphasis on important terms
- Use *italics* for variable names and file paths
- Use `code` for inline code references
- Use code blocks for multi-line code examples

### Lists
- Use bullet points for unordered lists
- Use numbered lists for sequential steps
- Indent nested lists with 2 spaces
- Keep list items concise and parallel in structure

### Code Blocks
- Use triple backticks with language identifier: ```python
- Include syntax highlighting for all code examples
- Limit code blocks to 20 lines when possible
- Add comments for complex logic

## Naming Conventions

### File Names
- Use kebab-case for file names: `example-name.md`
- Use descriptive names that indicate content type
- Format: `{type}-{module}.md` or `{type}-{topic}.md`
- Examples:
  - `example-errors.md` for error module examples
  - `guide-safe.md` for safe module guide
  - `faq-patterns.md` for patterns module FAQ

### IDs
- Use kebab-case for all IDs
- Format: `{type}-{number}` or `{type}-{descriptor}`
- Examples:
  - `ex-1`, `ex-2` for examples
  - `guide-errors-intro` for guide sections
  - `faq-1`, `faq-2` for FAQ entries

### Module Names
- Use lowercase module names
- Valid modules: errors, safe, learn, patterns, config, documentation
- Use full module name in references

## Code Example Standards

### Structure
Every code example should include:
1. **Title**: Clear, descriptive title
2. **Module**: Which module it demonstrates
3. **Difficulty**: beginner, intermediate, or advanced
4. **Code**: Complete, runnable Python code
5. **Expected Output**: What the code produces
6. **Explanation**: What the code does and why
7. **Variations**: Alternative approaches (optional)
8. **Tags**: Relevant keywords for searching

### Code Quality
- All code must be syntactically correct
- All code must be executable with current library version
- Use meaningful variable names
- Include comments for non-obvious logic
- Follow PEP 8 style guidelines
- Test all code before including

### Output Documentation
- Show actual output, not just description
- Include error messages if demonstrating error handling
- Show multiple examples if behavior varies
- Document any side effects

### Variations
- Include common variations of the example
- Show edge cases when relevant
- Document different use cases
- Explain when to use each variation

## Diagram Standards

### Types
- **Architecture**: System component relationships
- **Flow**: Process or data flow sequences
- **Concept**: Conceptual relationships and hierarchies

### Format
- Use Mermaid diagram syntax for consistency
- Include clear labels for all components
- Provide legend explaining notation
- Use consistent colors and shapes

### Content
- Keep diagrams simple and focused
- Avoid cluttering with too many elements
- Use descriptive labels
- Include title and description
- Reference all relevant modules

### Accessibility
- Provide alt text for all diagrams
- Use high contrast colors
- Ensure text is readable
- Provide text description of complex diagrams

## Content Organization

### Module Documentation Structure
Each module should have:
1. **Overview**: Purpose and key features
2. **Use Cases**: When and why to use
3. **API Reference**: Functions and classes
4. **Examples**: 3-5 runnable examples
5. **Best Practices**: Recommendations
6. **Troubleshooting**: Common issues and solutions
7. **Related Topics**: Links to related content

### Guide Structure
Each guide should include:
1. **Introduction**: What you'll learn
2. **Prerequisites**: Required knowledge
3. **Basic Section**: Fundamental concepts
4. **Intermediate Section**: Practical usage
5. **Advanced Section**: Complex scenarios
6. **Exercises**: Hands-on practice
7. **Checkpoints**: Understanding verification
8. **Summary**: Key takeaways

### FAQ Structure
Each FAQ entry should include:
1. **Question**: Clear, specific question
2. **Answer**: Detailed, beginner-friendly answer
3. **Code Example**: When applicable
4. **Related Questions**: Links to similar topics
5. **Tags**: Keywords for searching

## Language and Tone

### Writing Style
- Use clear, simple language
- Avoid jargon or define it clearly
- Use active voice
- Keep sentences short and focused
- Use second person ("you") when addressing readers

### Tone
- Be encouraging and supportive
- Avoid condescending language
- Be precise and accurate
- Use positive framing
- Acknowledge common challenges

### Technical Accuracy
- Verify all information before publishing
- Test all code examples
- Keep documentation current with library updates
- Document version-specific behavior
- Include deprecation notices when relevant

## Accessibility Standards

### Images and Diagrams
- Provide descriptive alt text
- Use high contrast colors
- Ensure text is readable at normal size
- Avoid color-only differentiation

### Code Examples
- Use syntax highlighting
- Ensure sufficient contrast
- Use semantic HTML structure
- Support keyboard navigation

### General
- Use proper heading hierarchy
- Provide text alternatives for visual content
- Ensure sufficient color contrast (WCAG AA)
- Support screen readers
- Enable keyboard navigation

## Consistency Checklist

Before publishing content, verify:
- [ ] File name follows naming conventions
- [ ] All IDs follow naming conventions
- [ ] Code examples are syntactically correct
- [ ] Code examples are executable
- [ ] Expected output is documented
- [ ] Explanations are clear and complete
- [ ] Diagrams have labels and legends
- [ ] All links are functional
- [ ] Accessibility requirements are met
- [ ] Content follows tone and style guidelines
- [ ] Module references are accurate
- [ ] Tags are relevant and consistent
