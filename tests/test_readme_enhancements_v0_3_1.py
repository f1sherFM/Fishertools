"""
Tests for README Enhancements v0.3.1

Tests verify that the README contains all required sections and content
for the explain() data structure documentation.
"""

import re
import json
from pathlib import Path
from hypothesis import given, strategies as st


class TestExplainDataStructureSection:
    """Tests for the explain() data structure section in README."""

    def test_explain_data_structure_section_exists(self) -> None:
        """Test that the explain() data structure section exists in README."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Check for the section header
        assert "Структура данных explain()" in content, \
            "Section 'Структура данных explain()' not found in README"

    def test_explain_data_structure_shows_all_three_keys(self) -> None:
        """Test that the example shows all three dictionary keys."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Структура данных explain()")
        assert section_start != -1, "Section not found"

        # Get the section content (up to the next heading)
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify all three keys are shown in the example
        assert '"description"' in section_content or "'description'" in section_content, \
            "Key 'description' not found in example"
        assert '"when_to_use"' in section_content or "'when_to_use'" in section_content, \
            "Key 'when_to_use' not found in example"
        assert '"example"' in section_content or "'example'" in section_content, \
            "Key 'example' not found in example"

    def test_explain_data_structure_shows_realistic_data(self) -> None:
        """Test that the example uses realistic data from an actual topic."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Структура данных explain()")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify realistic data is present (from the "list" topic)
        # Should contain information about lists
        assert "list" in section_content.lower(), \
            "Example should reference 'list' topic"
        
        # Should contain description about ordered collection
        assert "Ordered collection" in section_content or "ordered collection" in section_content, \
            "Example should contain description about ordered collection"

    def test_explain_data_structure_shows_field_access_code(self) -> None:
        """Test that code snippet showing field access is present."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Структура данных explain()")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify field access code is shown
        assert 'explanation["description"]' in section_content, \
            "Code to access 'description' field not found"
        assert 'explanation["when_to_use"]' in section_content, \
            "Code to access 'when_to_use' field not found"
        assert 'explanation["example"]' in section_content, \
            "Code to access 'example' field not found"

    def test_explain_data_structure_section_placement(self) -> None:
        """Test that the section is placed in the correct location."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the main section
        learning_tools_section = content.find("Обучающие инструменты v0.3.1")
        assert learning_tools_section != -1, \
            "Main section 'Обучающие инструменты v0.3.1' not found"

        # Find the data structure section
        data_structure_section = content.find("Структура данных explain()")
        assert data_structure_section != -1, \
            "Section 'Структура данных explain()' not found"

        # Verify it's after the main section
        assert data_structure_section > learning_tools_section, \
            "Data structure section should be in 'Обучающие инструменты v0.3.1' section"

    def test_explain_data_structure_section_has_python_code_block(self) -> None:
        """Test that the section contains Python code blocks."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Структура данных explain()")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify Python code blocks are present
        assert "```python" in section_content, \
            "Python code block not found in section"
        assert "from fishertools.learn import explain" in section_content, \
            "Import statement not found in code example"

    def test_explain_data_structure_section_has_comments(self) -> None:
        """Test that code examples include helpful comments."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Структура данных explain()")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify comments are present
        assert "#" in section_content, \
            "Comments not found in code examples"

    def test_explain_data_structure_section_formatting(self) -> None:
        """Test that the section uses proper markdown formatting."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Структура данных explain()")
        assert section_start != -1, "Section not found"

        # Verify it's a subsection (###)
        # Find the line with the section header
        lines = content[:section_start + 100].split('\n')
        header_line = lines[-1] if lines else ""
        
        # The section should be a subsection (###)
        assert "###" in content[max(0, section_start - 50):section_start + 50], \
            "Section should be formatted as a subsection (###)"

    def test_explain_data_structure_section_has_description_text(self) -> None:
        """Test that the section has descriptive text explaining the structure."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Структура данных explain()")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify descriptive text is present
        assert "словарь" in section_content.lower() or "dictionary" in section_content.lower(), \
            "Section should explain that explain() returns a dictionary"
        assert "ключ" in section_content.lower() or "key" in section_content.lower(), \
            "Section should mention the keys"



class TestTopicsTableCompleteness:
    """Tests for the topics table completeness in README.
    
    Feature: readme-enhancements-v0.3.1, Property 1: Topics Table Completeness
    Validates: Requirements 3.3
    """

    def test_topics_table_exists(self) -> None:
        """Test that the topics table exists in README."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Check for the section header
        assert "Поддерживаемые темы" in content, \
            "Section 'Поддерживаемые темы' not found in README"

    def test_topics_table_has_markdown_table_format(self) -> None:
        """Test that the topics are presented in a markdown table format."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section not found"

        # Get the section content (up to the next heading)
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify markdown table format
        assert "|" in section_content, \
            "Table should use markdown format with pipes"
        assert "Категория" in section_content, \
            "Table should have 'Категория' column"
        assert "Тема" in section_content, \
            "Table should have 'Тема' column"
        assert "Описание" in section_content, \
            "Table should have 'Описание' column"

    def test_topics_table_contains_at_least_30_topics(self) -> None:
        """Test that the topics table contains at least 30 topics.
        
        **Validates: Requirements 3.3**
        """
        import json
        
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section not found"

        # Get the section content (up to the next heading)
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Count table rows (each row starts with |)
        # Skip the header and separator rows
        lines = section_content.split('\n')
        table_rows = [line for line in lines if line.strip().startswith('|') and '---' not in line]
        
        # Subtract header row to get data rows
        data_rows = len(table_rows) - 1 if len(table_rows) > 0 else 0
        
        # Load explanations.json to get the expected number of topics
        explanations_path = Path("fishertools/learn/explanations.json")
        with open(explanations_path, 'r', encoding='utf-8') as f:
            explanations = json.load(f)
        
        expected_topics = len(explanations)
        
        assert data_rows >= expected_topics, \
            f"Table should contain at least {expected_topics} topics, but found {data_rows}"

    def test_topics_table_has_all_required_categories(self) -> None:
        """Test that the topics table includes all 5 required categories."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify all 5 categories are present
        required_categories = [
            "Типы данных",
            "Управляющие конструкции",
            "Функции",
            "Обработка ошибок",
            "Работа с файлами"
        ]

        for category in required_categories:
            assert category in section_content, \
                f"Category '{category}' not found in topics table"

    def test_topics_table_has_data_types_category(self) -> None:
        """Test that Data Types category is present with expected topics."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify Data Types category and topics
        assert "Типы данных" in section_content, \
            "Data Types category not found"
        
        data_types = ["int", "float", "str", "bool", "list", "tuple", "set", "dict"]
        for dtype in data_types:
            assert dtype in section_content, \
                f"Data type '{dtype}' not found in topics table"

    def test_topics_table_has_control_structures_category(self) -> None:
        """Test that Control Structures category is present with expected topics."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify Control Structures category and topics
        assert "Управляющие конструкции" in section_content, \
            "Control Structures category not found"
        
        control_structures = ["if", "for", "while", "break", "continue"]
        for cs in control_structures:
            assert cs in section_content, \
                f"Control structure '{cs}' not found in topics table"

    def test_topics_table_has_functions_category(self) -> None:
        """Test that Functions category is present with expected topics."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify Functions category and topics
        assert "Функции" in section_content, \
            "Functions category not found"
        
        functions = ["function", "return", "lambda", "*args", "**kwargs"]
        for func in functions:
            assert func in section_content, \
                f"Function '{func}' not found in topics table"

    def test_topics_table_has_error_handling_category(self) -> None:
        """Test that Error Handling category is present with expected topics."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify Error Handling category and topics
        assert "Обработка ошибок" in section_content, \
            "Error Handling category not found"
        
        error_handling = ["try", "except", "finally", "raise"]
        for eh in error_handling:
            assert eh in section_content, \
                f"Error handling '{eh}' not found in topics table"

    def test_topics_table_has_file_operations_category(self) -> None:
        """Test that File Operations category is present with expected topics."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify File Operations category and topics
        assert "Работа с файлами" in section_content, \
            "File Operations category not found"
        
        file_operations = ["open", "read", "write", "with"]
        for fo in file_operations:
            assert fo in section_content, \
                f"File operation '{fo}' not found in topics table"


class TestTopicDescriptions:
    """Tests for topic descriptions in the topics table.
    
    Feature: readme-enhancements-v0.3.1, Property 2: Topic Descriptions Present
    Validates: Requirements 3.4
    """

    def test_each_topic_has_description(self) -> None:
        """Test that each topic in the table has a description.
        
        **Validates: Requirements 3.4**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Parse table rows
        lines = section_content.split('\n')
        table_rows = [line for line in lines if line.strip().startswith('|') and '---' not in line]
        
        # Skip header row
        data_rows = table_rows[1:] if len(table_rows) > 1 else []

        # Verify each row has a description (4th column)
        for row in data_rows:
            cells = [cell.strip() for cell in row.split('|')]
            # Table format: | Category | Topic | Description |
            # cells[0] is empty, cells[1] is category, cells[2] is topic, cells[3] is description, cells[4] is empty
            if len(cells) >= 4:
                description = cells[3]
                assert description and len(description) > 0, \
                    f"Row '{row}' has empty description"
                # Description should be meaningful (not just whitespace)
                assert len(description.strip()) > 5, \
                    f"Description in row '{row}' is too short"

    def test_descriptions_are_meaningful(self) -> None:
        """Test that descriptions are meaningful and not just placeholders."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Parse table rows
        lines = section_content.split('\n')
        table_rows = [line for line in lines if line.strip().startswith('|') and '---' not in line]
        
        # Skip header row
        data_rows = table_rows[1:] if len(table_rows) > 1 else []

        # Verify descriptions contain meaningful content
        for row in data_rows:
            cells = [cell.strip() for cell in row.split('|')]
            if len(cells) >= 4:
                description = cells[3]
                # Description should not be just "..." or similar placeholders
                assert description != "..." and description != "...", \
                    f"Description is a placeholder in row '{row}'"
                # Description should contain actual words
                assert len(description.split()) > 2, \
                    f"Description is too short in row '{row}'"

    def test_descriptions_match_explanations_json(self) -> None:
        """Test that descriptions in table match the explanations.json file."""
        import json
        
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Load explanations.json
        explanations_path = Path("fishertools/learn/explanations.json")
        with open(explanations_path, 'r', encoding='utf-8') as f:
            explanations = json.load(f)

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Parse table rows
        lines = section_content.split('\n')
        table_rows = [line for line in lines if line.strip().startswith('|') and '---' not in line]
        
        # Skip header row
        data_rows = table_rows[1:] if len(table_rows) > 1 else []

        # Verify descriptions match explanations.json
        for row in data_rows:
            cells = [cell.strip() for cell in row.split('|')]
            if len(cells) >= 3:
                topic = cells[2]
                description = cells[3] if len(cells) >= 4 else ""
                
                # Check if topic exists in explanations.json
                if topic in explanations:
                    expected_description = explanations[topic]["description"]
                    # Description should match or be similar to the one in explanations.json
                    assert description in expected_description or expected_description in description, \
                        f"Description for '{topic}' doesn't match explanations.json"



class TestTopicsTableCompletenessProperty:
    """Property-based tests for topics table completeness.
    
    Feature: readme-enhancements-v0.3.1, Property 1: Topics Table Completeness
    **Validates: Requirements 3.3**
    """

    @given(st.just(None))
    def test_topics_table_contains_at_least_30_topics_property(self, _) -> None:
        """Property test: Topics table contains at least 30 topics.
        
        **Validates: Requirements 3.3**
        
        This property verifies that for any valid README.md file with a topics table,
        the table contains at least 30 topics across all categories as specified in
        requirement 3.3: "THE System SHALL list all 30+ topics with their names"
        
        The property checks that:
        1. The topics table exists in the README
        2. The table contains at least 30 topics (as per requirement 3.3)
        3. All topics from explanations.json are represented in the table
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section 'Поддерживаемые темы' not found"

        # Get the section content (up to the next heading)
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Count table rows (each row starts with |)
        # Skip the header and separator rows
        lines = section_content.split('\n')
        table_rows = [line for line in lines if line.strip().startswith('|') and '---' not in line]
        
        # Subtract header row to get data rows
        data_rows = len(table_rows) - 1 if len(table_rows) > 0 else 0
        
        # Load explanations.json to get the expected number of topics
        explanations_path = Path("fishertools/learn/explanations.json")
        with open(explanations_path, 'r', encoding='utf-8') as f:
            explanations = json.load(f)
        
        expected_topics = len(explanations)
        
        # Property 1: The table must contain at least as many topics as in explanations.json
        assert data_rows >= expected_topics, \
            f"Property violated: Table should contain at least {expected_topics} topics (from explanations.json), but found {data_rows}"
        
        # Property 2: Verify the minimum is at least 30 (as per requirement 3.3)
        # Requirement 3.3 states: "THE System SHALL list all 30+ topics with their names"
        assert data_rows >= 30, \
            f"Property violated: Requirement 3.3 specifies at least 30 topics, but found {data_rows}"


class TestTopicDescriptionsProperty:
    """Property-based tests for topic descriptions in the topics table.
    
    Feature: readme-enhancements-v0.3.1, Property 2: Topic Descriptions Present
    **Validates: Requirements 3.4**
    """

    @given(st.just(None))
    def test_each_topic_has_description_property(self, _) -> None:
        """Property test: Each topic in table has a description.
        
        **Validates: Requirements 3.4**
        
        This property verifies that for any valid README.md file with a topics table,
        each topic listed in the table has a brief description as specified in
        requirement 3.4: "THE System SHALL include a brief description of each topic"
        
        The property checks that:
        1. The topics table exists in the README
        2. Each topic row in the table has a non-empty description
        3. Each description is meaningful (not just whitespace or placeholders)
        4. Each description is of reasonable length (more than just a few words)
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые темы")
        assert section_start != -1, "Section 'Поддерживаемые темы' not found"

        # Get the section content (up to the next heading)
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Parse table rows
        lines = section_content.split('\n')
        table_rows = [line for line in lines if line.strip().startswith('|') and '---' not in line]
        
        # Skip header row
        data_rows = table_rows[1:] if len(table_rows) > 1 else []

        # Property: Each row must have a non-empty, meaningful description
        for row_index, row in enumerate(data_rows):
            cells = [cell.strip() for cell in row.split('|')]
            # Table format: | Category | Topic | Description |
            # cells[0] is empty, cells[1] is category, cells[2] is topic, cells[3] is description, cells[4] is empty
            assert len(cells) >= 4, \
                f"Property violated: Row {row_index} doesn't have enough columns"
            
            description = cells[3]
            
            # Property 1: Description must not be empty
            assert description and len(description) > 0, \
                f"Property violated: Row {row_index} has empty description"
            
            # Property 2: Description must not be just whitespace
            assert len(description.strip()) > 0, \
                f"Property violated: Row {row_index} has whitespace-only description"
            
            # Property 3: Description must be meaningful (not just placeholders)
            assert description.strip() != "..." and description.strip() != "...", \
                f"Property violated: Row {row_index} has placeholder description"
            
            # Property 4: Description should be of reasonable length
            # Requirement 3.4 specifies "brief description", which should be at least a few words
            assert len(description.split()) >= 2, \
                f"Property violated: Row {row_index} description is too short: '{description}'"
        
        # Property 5: All rows must have descriptions (universal property)
        # This ensures that the property holds for ALL topics in the table
        assert len(data_rows) > 0, \
            "Property violated: No data rows found in topics table"


class TestJSONStorageDocumentation:
    """Tests for the JSON storage documentation section in README.
    
    Feature: readme-enhancements-v0.3.1, Task 3: Add JSON storage documentation
    Validates: Requirements 2.1, 2.2
    """

    def test_json_storage_section_exists(self) -> None:
        """Test that the JSON storage documentation section exists in README."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Check for the section header
        assert "Расширение и локализация" in content, \
            "Section 'Расширение и локализация' not found in README"

    def test_json_storage_section_mentions_explanations_json(self) -> None:
        """Test that the section explicitly mentions fishertools/learn/explanations.json.
        
        **Validates: Requirements 2.1**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Расширение и локализация")
        assert section_start != -1, "Section not found"

        # Get the section content (up to the next heading)
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify the JSON file path is mentioned
        assert "fishertools/learn/explanations.json" in section_content, \
            "Path 'fishertools/learn/explanations.json' not mentioned in section"

    def test_json_storage_section_mentions_extensibility(self) -> None:
        """Test that the section mentions extensibility for contributors.
        
        **Validates: Requirements 2.1, 2.2**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Расширение и локализация")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify extensibility is mentioned
        assert "контрибьютор" in section_content.lower() or "contributor" in section_content.lower() or \
               "расширен" in section_content.lower() or "extend" in section_content.lower(), \
            "Extensibility for contributors not mentioned in section"

    def test_json_storage_section_mentions_localization(self) -> None:
        """Test that the section mentions localization possibilities.
        
        **Validates: Requirements 2.2**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Расширение и локализация")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify localization is mentioned
        assert "локализ" in section_content.lower() or "locali" in section_content.lower() or \
               "перевод" in section_content.lower() or "translation" in section_content.lower(), \
            "Localization possibilities not mentioned in section"

    def test_json_storage_section_explains_easy_extension(self) -> None:
        """Test that the section explains JSON storage makes extension easy.
        
        **Validates: Requirements 2.1, 2.2**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Расширение и локализация")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify explanation about easy extension
        assert "легко" in section_content.lower() or "easy" in section_content.lower() or \
               "просто" in section_content.lower() or "simple" in section_content.lower(), \
            "Explanation about easy extension not found in section"

    def test_json_storage_section_placement(self) -> None:
        """Test that the section is placed after the topics table."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the topics table section
        topics_section = content.find("Поддерживаемые темы")
        assert topics_section != -1, "Topics section not found"

        # Find the JSON storage section
        json_section = content.find("Расширение и локализация")
        assert json_section != -1, "JSON storage section not found"

        # Verify it's after the topics table
        assert json_section > topics_section, \
            "JSON storage section should be placed after the topics table"

    def test_json_storage_section_has_subsection_format(self) -> None:
        """Test that the section uses proper markdown subsection format."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Расширение и локализация")
        assert section_start != -1, "Section not found"

        # Verify it's a subsection (###)
        assert "###" in content[max(0, section_start - 50):section_start + 50], \
            "Section should be formatted as a subsection (###)"

    def test_json_storage_section_has_contributor_guidance(self) -> None:
        """Test that the section provides guidance for contributors."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Расширение и локализация")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify contributor guidance is present
        assert "контрибьютор" in section_content.lower() or "contributor" in section_content.lower(), \
            "Contributor guidance not found"
        
        # Should mention adding new topics
        assert "добавь" in section_content.lower() or "add" in section_content.lower(), \
            "Guidance about adding new topics not found"

    def test_json_storage_section_has_localization_guidance(self) -> None:
        """Test that the section provides guidance for localization."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Расширение и локализация")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify localization guidance is present
        assert "локализ" in section_content.lower() or "locali" in section_content.lower() or \
               "перевод" in section_content.lower() or "translation" in section_content.lower(), \
            "Localization guidance not found"

    def test_json_storage_section_mentions_json_structure(self) -> None:
        """Test that the section mentions the JSON structure (description, when_to_use, example)."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Расширение и локализация")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify JSON structure is mentioned
        assert "description" in section_content or "описание" in section_content.lower(), \
            "JSON structure (description field) not mentioned"
        assert "when_to_use" in section_content or "когда" in section_content.lower(), \
            "JSON structure (when_to_use field) not mentioned"
        assert "example" in section_content or "пример" in section_content.lower(), \
            "JSON structure (example field) not mentioned"

    def test_json_storage_section_has_meaningful_content(self) -> None:
        """Test that the section has meaningful content and is not just a placeholder."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Расширение и локализация")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify the section has meaningful content (not just a few words)
        # Should have at least 100 characters of content
        assert len(section_content.strip()) > 100, \
            "Section content is too short to be meaningful"

        # Should have multiple lines of content
        lines = [line.strip() for line in section_content.split('\n') if line.strip()]
        assert len(lines) > 3, \
            "Section should have multiple lines of content"


class TestErrorTypesCompleteness:
    """Tests for the error types list in README.
    
    Feature: readme-enhancements-v0.3.1, Task 4: Expand error types list
    Validates: Requirements 4.1, 4.2, 4.3
    """

    def test_error_types_section_exists(self) -> None:
        """Test that the error types section exists in README."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Check for the section header
        assert "Поддерживаемые типы ошибок" in content, \
            "Section 'Поддерживаемые типы ошибок' not found in README"

    def test_error_types_section_in_documentation(self) -> None:
        """Test that the error types section is in the Documentation section."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the Documentation section
        doc_section = content.find("📖 Документация")
        assert doc_section != -1, "Documentation section not found"

        # Find the error types section
        error_section = content.find("Поддерживаемые типы ошибок")
        assert error_section != -1, "Error types section not found"

        # Verify it's in the Documentation section
        assert error_section > doc_section, \
            "Error types section should be in the Documentation section"

    def test_error_types_section_lists_all_required_types(self) -> None:
        """Test that all required error types are listed.
        
        **Validates: Requirements 4.2**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Required error types from requirement 4.2
        required_error_types = [
            "TypeError",
            "ValueError",
            "AttributeError",
            "IndexError",
            "KeyError",
            "ImportError",
            "SyntaxError",
            "NameError",
            "ZeroDivisionError",
            "FileNotFoundError"
        ]

        # Verify all required error types are present in the README
        for error_type in required_error_types:
            assert error_type in content, \
                f"Error type '{error_type}' not found in README"

    def test_error_types_section_is_organized(self) -> None:
        """Test that error types are organized by category or have descriptions.
        
        **Validates: Requirements 4.3**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые типы ошибок")
        assert section_start != -1, "Section not found"

        # Get the section content (up to the next main section "###")
        # Find the next "### " (with space) after the current section
        next_section = content.find("\n### ", section_start + 1)
        if next_section == -1:
            next_section = content.find("\n## ", section_start + 1)
        if next_section == -1:
            next_section = len(content)

        section_content = content[section_start:next_section]

        # Verify organization by categories (should have category headers)
        # Look for category headers like "#### Ошибки типов и значений"
        assert "####" in section_content, \
            "Error types should be organized by categories (using #### headers)"

    def test_error_types_section_has_descriptions(self) -> None:
        """Test that error types have brief descriptions.
        
        **Validates: Requirements 4.3**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые типы ошибок")
        assert section_start != -1, "Section not found"

        # Get the section content (up to the next main section "###")
        next_section = content.find("\n### ", section_start + 1)
        if next_section == -1:
            next_section = content.find("\n## ", section_start + 1)
        if next_section == -1:
            next_section = len(content)

        section_content = content[section_start:next_section]

        # Verify descriptions are present (should have dashes and descriptions)
        assert "-" in section_content, \
            "Error types should have descriptions (using - bullet points)"

        # Count the number of error type entries with descriptions
        # Each should be formatted like: - **ErrorType** - description
        error_entries = section_content.count("**")
        assert error_entries >= 20, \
            "Should have descriptions for all error types (at least 10 error types with bold formatting)"

    def test_error_types_section_indicates_complete_list(self) -> None:
        """Test that the section indicates this is the complete list.
        
        **Validates: Requirements 4.1**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые типы ошибок")
        assert section_start != -1, "Section not found"

        # Get the section content
        section_end = content.find("###", section_start + 1)
        if section_end == -1:
            section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Verify indication of complete list
        # Should mention "полный список" or "complete list" or similar
        assert "полный" in section_content.lower() or "complete" in section_content.lower() or \
               "все" in section_content.lower() or "all" in section_content.lower(), \
            "Section should indicate this is the complete list of supported error types"

    def test_error_types_section_has_examples(self) -> None:
        """Test that the section includes usage examples."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые типы ошибок")
        assert section_start != -1, "Section not found"

        # Get the section content (up to the next main section "###")
        next_section = content.find("\n### ", section_start + 1)
        if next_section == -1:
            next_section = content.find("\n## ", section_start + 1)
        if next_section == -1:
            next_section = len(content)

        section_content = content[section_start:next_section]

        # Verify examples are present
        assert "```python" in section_content, \
            "Section should include Python code examples"
        assert "explain_error" in section_content, \
            "Examples should show how to use explain_error()"

    def test_error_types_section_placement(self) -> None:
        """Test that the section is properly placed in the README."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the Documentation section
        doc_section = content.find("📖 Документация")
        assert doc_section != -1, "Documentation section not found"

        # Find the error types section
        error_section = content.find("Поддерживаемые типы ошибок")
        assert error_section != -1, "Error types section not found"

        # Verify it's after the Documentation section header
        assert error_section > doc_section, \
            "Error types section should be in the Documentation section"

    def test_error_types_section_has_meaningful_content(self) -> None:
        """Test that the section has meaningful content."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые типы ошибок")
        assert section_start != -1, "Section not found"

        # Get the section content (up to the next main section "###")
        next_section = content.find("\n### ", section_start + 1)
        if next_section == -1:
            next_section = content.find("\n## ", section_start + 1)
        if next_section == -1:
            next_section = len(content)

        section_content = content[section_start:next_section]

        # Verify the section has meaningful content
        assert len(section_content.strip()) > 200, \
            "Section content should be substantial (more than 200 characters)"


class TestErrorTypesCompletenessProperty:
    """Property-based tests for error types completeness.
    
    Feature: readme-enhancements-v0.3.1, Property 3: Error Types Completeness
    **Validates: Requirements 4.2**
    """

    @given(st.just(None))
    def test_all_required_error_types_are_listed_property(self, _) -> None:
        """Property test: All required error types are listed in README.
        
        **Validates: Requirements 4.2**
        
        This property verifies that for any valid README.md file with an error types section,
        all required error types are listed as specified in requirement 4.2:
        "THE System SHALL include: TypeError, ValueError, AttributeError, IndexError, KeyError,
        ImportError, SyntaxError, NameError, ZeroDivisionError, FileNotFoundError"
        
        The property checks that:
        1. The error types section exists in the README
        2. All 10 required error types are present in the section
        3. Each error type is properly formatted and documented
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Поддерживаемые типы ошибок")
        assert section_start != -1, "Section 'Поддерживаемые типы ошибок' not found"

        # Required error types from requirement 4.2
        required_error_types = [
            "TypeError",
            "ValueError",
            "AttributeError",
            "IndexError",
            "KeyError",
            "ImportError",
            "SyntaxError",
            "NameError",
            "ZeroDivisionError",
            "FileNotFoundError"
        ]

        # Property: All required error types must be present in the README
        for error_type in required_error_types:
            assert error_type in content, \
                f"Property violated: Required error type '{error_type}' not found in README"

        # Property: The section must contain all 10 required error types
        # This is a universal property that must hold for all valid README files
        assert len(required_error_types) == 10, \
            "Property violated: Expected exactly 10 required error types"

        # Property: Each error type should be formatted with bold (**ErrorType**)
        # Count the number of error types that are properly formatted
        formatted_count = 0
        for error_type in required_error_types:
            if f"**{error_type}**" in content:
                formatted_count += 1

        # At least 8 out of 10 should be properly formatted
        assert formatted_count >= 8, \
            f"Property violated: Only {formatted_count} out of 10 error types are properly formatted with bold"



class TestLimitationsSection:
    """Tests for the limitations section in README.
    
    Feature: readme-enhancements-v0.3.1, Task 5: Add limitations section
    Validates: Requirements 5.1, 5.2, 5.3
    """

    def _get_section_content(self, content: str, section_name: str) -> str:
        """Helper method to extract section content properly."""
        section_start = content.find(f"## ⚠️ {section_name}")
        if section_start == -1:
            section_start = content.find(section_name)
        if section_start == -1:
            return ""
        
        # Find the next main section (## at start of line, not ###)
        # We need to find \n## that is NOT followed by another #
        import re
        next_section_match = re.search(r'\n##(?!#)', content[section_start + 1:])
        if next_section_match:
            next_section = section_start + 1 + next_section_match.start()
        else:
            next_section = len(content)
        
        return content[section_start:next_section]

    def test_limitations_section_exists(self) -> None:
        """Test that the limitations section exists in README.
        
        **Validates: Requirements 5.1**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Check for the section header with warning emoji
        assert "⚠️ Ограничения" in content or "Ограничения" in content, \
            "Section 'Ограничения' (Limitations) not found in README"

    def test_limitations_section_mentions_syntax_error_limitation(self) -> None:
        """Test that the section clearly states SyntaxError limitation.
        
        **Validates: Requirements 5.2**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")
        section_content = self._get_section_content(content, "Ограничения")
        assert section_content, "Limitations section not found"

        # Verify SyntaxError limitation is mentioned
        assert "SyntaxError" in section_content, \
            "SyntaxError limitation not mentioned in section"
        assert "explain_error()" in section_content, \
            "explain_error() function not mentioned in SyntaxError limitation"

    def test_limitations_section_explains_syntax_error_why(self) -> None:
        """Test that the section explains why SyntaxError cannot be explained.
        
        **Validates: Requirements 5.2**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("## ⚠️ Ограничения")
        if section_start == -1:
            section_start = content.find("Ограничения")
        assert section_start != -1, "Limitations section not found"

        # Get the section content using the helper method
        section_content = self._get_section_content(content, "Ограничения")

        # Verify explanation of why SyntaxError cannot be explained
        # Should mention parsing, parse time, or before execution
        assert "парс" in section_content.lower() or "parse" in section_content.lower() or \
               "до выполнения" in section_content.lower() or "before execution" in section_content.lower() or \
               "до исполнения" in section_content.lower(), \
            "Explanation of why SyntaxError cannot be explained not found"

    def test_limitations_section_mentions_oop_limitation(self) -> None:
        """Test that the section clearly states OOP limitation.
        
        **Validates: Requirements 5.3**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("## ⚠️ Ограничения")
        if section_start == -1:
            section_start = content.find("Ограничения")
        assert section_start != -1, "Limitations section not found"

        # Get the section content using the helper method
        section_content = self._get_section_content(content, "Ограничения")

        # Verify OOP limitation is mentioned
        assert "OOP" in section_content or "объектно-ориентированное" in section_content.lower() or \
               "класс" in section_content.lower() or "class" in section_content.lower(), \
            "OOP limitation not mentioned in section"
        assert "explain()" in section_content, \
            "explain() function not mentioned in OOP limitation"

    def test_limitations_section_explains_oop_why(self) -> None:
        """Test that the section explains why OOP is not yet supported.
        
        **Validates: Requirements 5.3**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("## ⚠️ Ограничения")
        if section_start == -1:
            section_start = content.find("Ограничения")
        assert section_start != -1, "Limitations section not found"

        # Get the section content using the helper method
        section_content = self._get_section_content(content, "Ограничения")

        # Verify explanation of why OOP is not yet supported
        # Should mention future versions or planned
        assert "будущ" in section_content.lower() or "future" in section_content.lower() or \
               "планиру" in section_content.lower() or "planned" in section_content.lower(), \
            "Explanation of why OOP is not yet supported not found"

    def test_limitations_section_has_subsection_format(self) -> None:
        """Test that the section uses proper markdown subsection format."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("Ограничения")
        assert section_start != -1, "Section not found"

        # Verify it's a main section (##)
        assert "##" in content[max(0, section_start - 50):section_start + 50], \
            "Section should be formatted as a main section (##)"

    def test_limitations_section_has_subsections(self) -> None:
        """Test that the section has subsections for each limitation."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("## ⚠️ Ограничения")
        if section_start == -1:
            section_start = content.find("Ограничения")
        assert section_start != -1, "Section not found"

        # Get the section content using the helper method
        section_content = self._get_section_content(content, "Ограничения")

        # Verify subsections exist (###)
        assert "###" in section_content, \
            "Section should have subsections (###) for each limitation"

    def test_limitations_section_has_syntax_error_subsection(self) -> None:
        """Test that there's a subsection specifically for SyntaxError limitation."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("## ⚠️ Ограничения")
        if section_start == -1:
            section_start = content.find("Ограничения")
        assert section_start != -1, "Section not found"

        # Get the section content using the helper method
        section_content = self._get_section_content(content, "Ограничения")

        # Verify SyntaxError subsection exists
        assert "SyntaxError" in section_content, \
            "SyntaxError subsection not found"

    def test_limitations_section_has_oop_subsection(self) -> None:
        """Test that there's a subsection specifically for OOP limitation."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("## ⚠️ Ограничения")
        if section_start == -1:
            section_start = content.find("Ограничения")
        assert section_start != -1, "Section not found"

        # Get the section content using the helper method
        section_content = self._get_section_content(content, "Ограничения")

        # Verify OOP subsection exists
        assert "объектно-ориентированное" in section_content.lower() or \
               "OOP" in section_content or "класс" in section_content.lower(), \
            "OOP subsection not found"

    def test_limitations_section_has_code_examples(self) -> None:
        """Test that the section includes code examples."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("## ⚠️ Ограничения")
        if section_start == -1:
            section_start = content.find("Ограничения")
        assert section_start != -1, "Section not found"

        # Get the section content using the helper method
        section_content = self._get_section_content(content, "Ограничения")

        # Verify code examples are present
        assert "```python" in section_content, \
            "Section should include Python code examples"

    def test_limitations_section_placement(self) -> None:
        """Test that the section is placed in a prominent location."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the Documentation section
        doc_section = content.find("📖 Документация")
        
        # Find the Testing section
        testing_section = content.find("🧪 Тестирование")

        # Find the limitations section
        limitations_section = content.find("Ограничения")
        assert limitations_section != -1, "Limitations section not found"

        # Verify it's placed after Documentation and before Testing
        # (or in a prominent location)
        if doc_section != -1 and testing_section != -1:
            assert doc_section < limitations_section < testing_section, \
                "Limitations section should be placed between Documentation and Testing sections"

    def test_limitations_section_has_meaningful_content(self) -> None:
        """Test that the section has meaningful content."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("## ⚠️ Ограничения")
        if section_start == -1:
            section_start = content.find("Ограничения")
        assert section_start != -1, "Section not found"

        # Get the section content using the helper method
        section_content = self._get_section_content(content, "Ограничения")

        # Verify the section has meaningful content
        assert len(section_content.strip()) > 200, \
            "Section content should be substantial (more than 200 characters)"

        # Should have multiple lines of content
        lines = [line.strip() for line in section_content.split('\n') if line.strip()]
        assert len(lines) > 5, \
            "Section should have multiple lines of content"

    def test_limitations_section_syntax_error_mentions_try_except(self) -> None:
        """Test that SyntaxError limitation mentions try-except."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("## ⚠️ Ограничения")
        if section_start == -1:
            section_start = content.find("Ограничения")
        assert section_start != -1, "Section not found"

        # Get the section content using the helper method
        section_content = self._get_section_content(content, "Ограничения")

        # Verify try-except is mentioned in context of SyntaxError
        assert "try" in section_content.lower() or "try-except" in section_content.lower(), \
            "SyntaxError limitation should mention try-except"

    def test_limitations_section_oop_lists_unsupported_concepts(self) -> None:
        """Test that OOP limitation lists specific unsupported concepts."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the section
        section_start = content.find("## ⚠️ Ограничения")
        if section_start == -1:
            section_start = content.find("Ограничения")
        assert section_start != -1, "Section not found"

        # Get the section content using the helper method
        section_content = self._get_section_content(content, "Ограничения")

        # Verify specific OOP concepts are mentioned
        oop_concepts = ["класс", "наследование", "полиморфизм", "инкапсуляция"]
        found_concepts = 0
        for concept in oop_concepts:
            if concept in section_content.lower():
                found_concepts += 1

        assert found_concepts >= 2, \
            "OOP limitation should mention specific unsupported concepts"


class TestPyPIStatus:
    """Tests for the PyPI publication status in README.
    
    Feature: readme-enhancements-v0.3.1, Task 6: Clarify PyPI publication status
    Validates: Requirements 6.1, 6.2, 6.3, 6.4
    """

    def _get_installation_section_content(self, content: str) -> str:
        """Helper method to extract installation section content."""
        # Find the installation section
        section_start = content.find("## 📦 Установка")
        if section_start == -1:
            section_start = content.find("📦 Установка")
        
        if section_start == -1:
            return ""
        
        # Find the next main section (##)
        # Look for the next ## after the current position
        next_section = content.find("\n## ", section_start + 1)
        if next_section == -1:
            section_end = len(content)
        else:
            section_end = next_section
        
        return content[section_start:section_end]

    def test_installation_section_exists(self) -> None:
        """Test that the installation section exists in README."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Check for the section header
        assert "📦 Установка" in content, \
            "Section '📦 Установка' not found in README"

    def test_pypi_status_section_exists(self) -> None:
        """Test that the PyPI status subsection exists.
        
        **Validates: Requirements 6.1**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Check for the PyPI status subsection
        assert "Текущий статус версии" in section_content, \
            "PyPI status subsection 'Текущий статус версии' not found"

    def test_v0_3_1_not_published_statement(self) -> None:
        """Test that README clearly states v0.3.1 is not yet published on PyPI.
        
        **Validates: Requirements 6.1**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify clear statement about v0.3.1 not being published
        assert "0.3.1" in section_content, \
            "Version 0.3.1 not mentioned in installation section"
        assert "ещё не опубликована" in section_content or "not yet published" in section_content, \
            "Clear statement that v0.3.1 is not yet published not found"
        assert "PyPI" in section_content, \
            "PyPI not mentioned in the statement"

    def test_v0_2_1_latest_on_pypi_statement(self) -> None:
        """Test that README notes v0.2.1 is the latest version on PyPI.
        
        **Validates: Requirements 6.2**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify statement about v0.2.1 being latest on PyPI
        assert "0.2.1" in section_content, \
            "Version 0.2.1 not mentioned in installation section"
        assert "PyPI" in section_content, \
            "PyPI not mentioned"
        # Should mention it's the latest version
        assert "последняя" in section_content.lower() or "latest" in section_content.lower(), \
            "Statement about v0.2.1 being latest on PyPI not found"

    def test_git_clone_instructions_present(self) -> None:
        """Test that git clone instructions are provided for installing from source.
        
        **Validates: Requirements 6.3**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify git clone instructions
        assert "git clone" in section_content, \
            "git clone instruction not found"
        assert "https://github.com" in section_content or "github.com" in section_content, \
            "GitHub repository URL not found"
        assert "My_1st_library_python" in section_content, \
            "Repository name not found in git clone instruction"

    def test_pip_install_e_instructions_present(self) -> None:
        """Test that pip install -e instructions are provided for development mode.
        
        **Validates: Requirements 6.4**
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify pip install -e instructions
        assert "pip install -e" in section_content, \
            "pip install -e instruction not found"
        assert "pip install -e ." in section_content, \
            "pip install -e . instruction not found"

    def test_installation_section_has_subsections(self) -> None:
        """Test that the installation section has proper subsections."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify subsections exist
        assert "###" in section_content, \
            "Installation section should have subsections (###)"

    def test_installation_section_has_code_blocks(self) -> None:
        """Test that the installation section includes code blocks."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify code blocks are present
        assert "```bash" in section_content, \
            "Bash code blocks not found in installation section"

    def test_installation_from_source_subsection_exists(self) -> None:
        """Test that there's a subsection for installing from source."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify subsection for installing from source
        assert "исходник" in section_content.lower() or "source" in section_content.lower(), \
            "Subsection for installing from source not found"

    def test_installation_development_mode_subsection_exists(self) -> None:
        """Test that there's a subsection for development mode installation."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify subsection for development mode
        assert "разработк" in section_content.lower() or "development" in section_content.lower(), \
            "Subsection for development mode installation not found"

    def test_installation_section_has_note_about_publication(self) -> None:
        """Test that there's a note about when v0.3.1 will be published."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify note about publication
        assert "Примечание" in section_content or "Note" in section_content or \
               "опубликована" in section_content or "published" in section_content, \
            "Note about when v0.3.1 will be published not found"

    def test_installation_section_mentions_pip_install_fishertools(self) -> None:
        """Test that instructions for installing v0.2.1 from PyPI are present."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify pip install fishertools instruction
        assert "pip install fishertools" in section_content, \
            "pip install fishertools instruction not found"

    def test_installation_section_formatting(self) -> None:
        """Test that the installation section uses proper markdown formatting."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Find the installation section
        section_start = content.find("📦 Установка")
        assert section_start != -1, "Installation section not found"

        # Verify it's a main section (##)
        assert "##" in content[max(0, section_start - 50):section_start + 50], \
            "Section should be formatted as a main section (##)"

    def test_installation_section_has_warning_icon(self) -> None:
        """Test that the PyPI status includes a warning icon."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify warning icon is present
        assert "⚠️" in section_content or "⚠" in section_content, \
            "Warning icon not found in PyPI status"

    def test_installation_section_has_important_marker(self) -> None:
        """Test that the PyPI status is marked as important."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify important marker
        assert "Важно" in section_content or "Important" in section_content, \
            "Important marker not found in PyPI status"

    def test_git_clone_includes_cd_command(self) -> None:
        """Test that git clone instructions include cd command."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Verify cd command is present
        assert "cd" in section_content, \
            "cd command not found in git clone instructions"

    def test_installation_section_has_multiple_installation_methods(self) -> None:
        """Test that multiple installation methods are provided."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get the installation section content
        section_content = self._get_installation_section_content(content)
        assert section_content, "Installation section not found"

        # Count the number of subsections (installation methods)
        subsection_count = section_content.count("###")
        
        # Should have at least 3 subsections: status, from source, from PyPI, development
        assert subsection_count >= 3, \
            f"Installation section should have at least 3 subsections, found {subsection_count}"


class TestContentDuplicationProperty:
    """Property-based tests for content duplication in README.
    
    Feature: readme-enhancements-v0.3.1, Property 4: No Content Duplication
    **Validates: Requirements 7.3**
    """

    @given(st.just(None))
    def test_no_significant_content_duplication_property(self, _) -> None:
        """Property test: No significant content duplication across sections.
        
        **Validates: Requirements 7.3**
        
        This property verifies that for any valid README.md file, information
        should not be significantly duplicated across multiple sections as specified
        in requirement 7.3: "THE System SHALL avoid duplication of information"
        
        The property checks that:
        1. Installation instructions appear only in the "📦 Установка" section
        2. Error types are documented only in the "📖 Документация" section
        3. Learning tools are explained in detail only in the "📚 Обучающие инструменты v0.3.1" section
        4. Patterns are documented only in the "🔧 Готовые паттерны" section
        5. Key concepts are not repeated verbatim across multiple sections
        """
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Property 1: Installation instructions should not be duplicated excessively
        # Count occurrences of "pip install" outside of code examples
        pip_install_count = content.count("pip install")
        # Should appear multiple times (different installation methods) but not excessively
        assert pip_install_count <= 10, \
            f"Property violated: 'pip install' appears {pip_install_count} times (excessive duplication)"

        # Property 2: Error type explanations should not be duplicated
        # Count occurrences of "TypeError" - should appear mainly in documentation section
        type_error_count = content.count("TypeError")
        # Should appear a few times but not excessively
        assert type_error_count <= 5, \
            f"Property violated: 'TypeError' appears {type_error_count} times (excessive duplication)"

        # Property 3: Learning tools documentation should not be duplicated
        # Count occurrences of "explain()" - should appear mainly in learning tools section
        explain_count = content.count("explain()")
        # Should appear multiple times but not excessively
        assert explain_count <= 15, \
            f"Property violated: 'explain()' appears {explain_count} times (excessive duplication)"

        # Property 4: Patterns documentation should not be duplicated
        # Count occurrences of "simple_menu" - should appear mainly in patterns section
        simple_menu_count = content.count("simple_menu")
        # Should appear a few times but not excessively
        assert simple_menu_count <= 8, \
            f"Property violated: 'simple_menu' appears {simple_menu_count} times (excessive duplication)"

        # Property 5: Check for verbatim duplication of long phrases
        # Split content into sentences and check for duplicates
        sentences = [s.strip() for s in content.split('.') if len(s.strip()) > 50]
        
        # Count sentence occurrences
        sentence_counts = {}
        for sentence in sentences:
            # Normalize sentence for comparison
            normalized = sentence.lower().strip()
            if normalized:
                sentence_counts[normalized] = sentence_counts.get(normalized, 0) + 1
        
        # Check that no long sentence appears more than twice
        # (allowing for some repetition in examples and documentation)
        for sentence, count in sentence_counts.items():
            assert count <= 2, \
                f"Property violated: Long phrase appears {count} times (verbatim duplication): '{sentence[:100]}...'"
        
        # Property 6: Verify key sections exist and contain expected content
        assert "## 📦 Установка" in content, "Installation section not found"
        assert "## 📖 Документация" in content, "Documentation section not found"
        assert "## 📚 Обучающие инструменты v0.3.1" in content, "Learning tools section not found"
        assert "## 🔧 Готовые паттерны" in content, "Patterns section not found"
        
        # Property 7: Verify that installation section contains installation keywords
        assert "pip install" in content, "Installation instructions not found"
        assert "git clone" in content, "Git clone instructions not found"

    def test_installation_section_unique_content(self) -> None:
        """Test that installation section has unique content not duplicated elsewhere."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get installation section
        section_start = content.find("## 📦 Установка")
        assert section_start != -1, "Installation section not found"

        section_end = content.find("##", section_start + 2)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Get content before and after installation section
        before_content = content[:section_start]
        after_content = content[section_end:]

        # Check that key installation phrases don't appear excessively before
        # (they might appear in quick start, but not as detailed instructions)
        git_clone_before = before_content.count("git clone")
        
        # git clone should appear mainly in installation section
        # Allow up to 1 mention before (in quick start or examples)
        assert git_clone_before <= 1, \
            "git clone instructions appear before installation section (duplication)"

    def test_documentation_section_unique_error_types(self) -> None:
        """Test that error types are documented uniquely in documentation section."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get documentation section
        section_start = content.find("📖 Документация")
        assert section_start != -1, "Documentation section not found"

        section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Get content before documentation section
        before_content = content[:section_start]

        # Check that detailed error type explanations don't appear before
        # (they might be mentioned in examples, but not as detailed documentation)
        error_types = ["TypeError", "ValueError", "AttributeError", "IndexError", "KeyError"]
        
        for error_type in error_types:
            # Count detailed explanations (with "возникает" or "occurs")
            detailed_before = before_content.count(f"{error_type}") - before_content.count(f"except {error_type}")
            detailed_in_section = section_content.count(f"{error_type}")
            
            # Detailed explanations should be mainly in documentation section
            # (allowing for some mentions in examples)
            assert detailed_before <= 2, \
                f"Detailed explanation of {error_type} appears before documentation section (duplication)"

    def test_learning_tools_section_unique_content(self) -> None:
        """Test that learning tools documentation is unique to its section."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Verify the detailed topics table exists in the README
        assert "| Категория | Тема | Описание |" in content, \
            "Detailed topics table not found in README"
        
        # Verify it's in the learning tools section (after the learning tools header)
        learning_tools_start = content.find("## 📚 Обучающие инструменты v0.3.1")
        table_start = content.find("| Категория | Тема | Описание |")
        
        assert learning_tools_start != -1, "Learning tools section not found"
        assert table_start != -1, "Topics table not found"
        assert table_start > learning_tools_start, \
            "Topics table should be in learning tools section"

    def test_patterns_section_unique_content(self) -> None:
        """Test that patterns documentation is unique to its section."""
        readme_path = Path("README.md")
        content = readme_path.read_text(encoding="utf-8")

        # Get patterns section
        section_start = content.find("🔧 Готовые паттерны")
        assert section_start != -1, "Patterns section not found"

        section_end = content.find("##", section_start + 1)
        if section_end == -1:
            section_end = len(content)

        section_content = content[section_start:section_end]

        # Get content before patterns section
        before_content = content[:section_start]

        # Check that detailed pattern documentation doesn't appear before
        patterns = ["simple_menu", "JSONStorage", "SimpleLogger", "SimpleCLI"]
        
        for pattern in patterns:
            # Count detailed explanations (with "Особенности" or "Features")
            detailed_before = before_content.count(f"{pattern}") - before_content.count(f"from fishertools.patterns import")
            detailed_in_section = section_content.count(f"{pattern}")
            
            # Detailed documentation should be mainly in patterns section
            assert detailed_before <= 2, \
                f"Detailed documentation of {pattern} appears before patterns section (duplication)"
