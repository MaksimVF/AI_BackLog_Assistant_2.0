


"""
Test for Level 2 Graph Orchestrator
"""

from src.agents.langgraph_agents import level2_graph_orchestrator

def main():
    """Test the Level 2 Graph Orchestrator"""
    # Test with a sample input
    text = """# New Feature Idea
We should add a new feature for user profiles that allows users to upload avatars.
This would improve user engagement.

Contact: support@company.com
Deadline: 2023-12-31
"""

    try:
        result = level2_graph_orchestrator.analyze_text(text)
        print("Test successful!")
        print(f"Result keys: {list(result.keys())}")
        print(f"Advanced classification: {result['advanced_classification']['task_type']}")
        print(f"Reflection: {result['reflection']['task_type']}")
        print(f"Semantic blocks: {len(result['blocks']['blocks'])}")
        print(f"Context domain: {result['context']['domain']}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


