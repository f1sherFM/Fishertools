#!/usr/bin/env python3
"""
Demonstration of fishertools integration capabilities.

This script shows how all the enhancement components work together
to provide a comprehensive learning experience.
"""

from fishertools.integration import get_integration, start_learning, explain_code


def main():
    """Demonstrate the integrated fishertools system."""
    print("🚀 Fishertools Integration Demo")
    print("=" * 50)
    
    # Get the integration instance
    integration = get_integration(project_name="demo")
    
    # Show system status
    print("\n📊 System Status:")
    status = integration.get_system_status()
    for component, state in status.items():
        if component not in ['current_config', 'total_examples']:
            print(f"  {component}: {state}")
    
    print(f"\n📚 Total examples available: {status.get('total_examples', 0)}")
    
    # Demonstrate learning session
    print("\n🎓 Starting Learning Session:")
    session = start_learning("variables", "beginner", "demo_user")
    print(f"  Topic: {session.topic}")
    print(f"  Level: {session.level.value}")
    print(f"  Exercises: {len(session.exercises)}")
    
    # Demonstrate code explanation
    print("\n🔍 Code Explanation Demo:")
    code_examples = [
        "name = 'Alice'",
        "numbers = [1, 2, 3, 4, 5]",
        "def greet(name): return f'Hello, {name}!'"
    ]
    
    for code in code_examples:
        print(f"\n  Code: {code}")
        result = explain_code(code, include_visuals=False)
        
        if result['step_explanations']:
            explanation = result['step_explanations'][0]
            print(f"  Explanation: {explanation.description}")
            print(f"  Concepts: {', '.join(explanation.related_concepts)}")
        
        if result['related_examples']:
            print(f"  Related examples: {len(result['related_examples'])} found")
    
    # Demonstrate learning recommendations
    print("\n💡 Learning Recommendations:")
    recommendations = integration.get_learning_recommendations("demo_user", "variables")
    
    if recommendations['next_topics']:
        print(f"  Next topics: {', '.join(recommendations['next_topics'])}")
    
    if recommendations['recommended_examples']:
        print(f"  Recommended examples: {len(recommendations['recommended_examples'])}")
    
    # Show error recovery capabilities
    print("\n🛡️ Error Recovery System:")
    recovery_stats = integration.recovery_manager.get_error_statistics()
    print(f"  Total errors handled: {recovery_stats['total_errors']}")
    print(f"  Recovery strategies: {recovery_stats['recovery_strategies']}")
    print(f"  Registered fallbacks: {recovery_stats['registered_fallbacks']}")
    
    print("\n✅ Integration demo completed successfully!")
    print("\nThe fishertools enhancement system provides:")
    print("  • Integrated learning experiences")
    print("  • Step-by-step code explanations")
    print("  • Personalized recommendations")
    print("  • Comprehensive error recovery")
    print("  • Automatic documentation generation")
    print("  • Visual learning aids")


if __name__ == "__main__":
    main()