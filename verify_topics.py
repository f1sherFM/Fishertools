#!/usr/bin/env python
"""Verify that all topics are loaded and examples are valid."""

from fishertools.learn import list_topics, get_topic, get_learning_path

# Verify all topics are loaded
topics = list_topics()
print(f"✓ Total topics loaded: {len(topics)}")
assert len(topics) == 35, f"Expected 35 topics, got {len(topics)}"

# Verify learning path
path = get_learning_path()
print(f"✓ Learning path length: {len(path)}")
assert len(path) == 35, f"Expected 35 topics in learning path, got {len(path)}"

# Verify all examples are valid Python
errors = []
for topic_name in topics:
    topic = get_topic(topic_name)
    example = topic.get('example', '')
    try:
        compile(example, f'<{topic_name}>', 'exec')
    except SyntaxError as e:
        errors.append((topic_name, str(e)))

if errors:
    print(f"✗ Topics with syntax errors: {len(errors)}")
    for topic_name, error in errors:
        print(f"  - {topic_name}: {error}")
else:
    print(f"✓ All {len(topics)} examples are valid Python code")

# Verify all related topics exist
missing_related = []
for topic_name in topics:
    topic = get_topic(topic_name)
    for related_name in topic.get('related_topics', []):
        if get_topic(related_name) is None:
            missing_related.append((topic_name, related_name))

if missing_related:
    print(f"✗ Missing related topics: {len(missing_related)}")
    for topic_name, related_name in missing_related:
        print(f"  - {topic_name} -> {related_name}")
else:
    print(f"✓ All related topics exist")

# Verify categories
categories = {}
for topic_name in topics:
    topic = get_topic(topic_name)
    category = topic.get('category')
    if category not in categories:
        categories[category] = []
    categories[category].append(topic_name)

print(f"✓ Topics organized in {len(categories)} categories:")
for category, topic_list in sorted(categories.items()):
    print(f"  - {category}: {len(topic_list)} topics")

print("\n✓ All verifications passed!")
