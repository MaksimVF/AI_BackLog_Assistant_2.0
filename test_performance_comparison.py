



"""
Performance comparison between original and LangGraph-based Level 2 orchestrators
"""

import time
from src.orchestrator.level2_orchestrator import level2_orchestrator
from src.agents.langgraph_agents import level2_graph_orchestrator

def main():
    """Compare performance between original and LangGraph orchestrators"""
    # Test with a sample input
    text = """# New Feature Idea
We should add a new feature for user profiles that allows users to upload avatars.
This would improve user engagement.

Contact: support@company.com
Deadline: 2023-12-31
"""

    # Test original orchestrator
    print("Testing original Level 2 orchestrator...")
    start_time = time.time()
    try:
        original_result = level2_orchestrator.analyze_text(text)
        original_time = time.time() - start_time
        print(f"Original orchestrator time: {original_time:.3f} seconds")
        print(f"Result keys: {list(original_result.keys())}")
    except Exception as e:
        print(f"Original orchestrator error: {e}")
        original_time = None

    # Test LangGraph orchestrator
    print("\nTesting LangGraph Level 2 orchestrator...")
    start_time = time.time()
    try:
        graph_result = level2_graph_orchestrator.analyze_text(text)
        graph_time = time.time() - start_time
        print(f"LangGraph orchestrator time: {graph_time:.3f} seconds")
        print(f"Result keys: {list(graph_result.keys())}")
    except Exception as e:
        print(f"LangGraph orchestrator error: {e}")
        graph_time = None

    # Compare results
    if original_time is not None and graph_time is not None:
        print(f"\nPerformance comparison:")
        print(f"Original: {original_time:.3f}s")
        print(f"LangGraph: {graph_time:.3f}s")
        print(f"Difference: {graph_time - original_time:.3f}s")

        if original_result and graph_result:
            # Check if results are similar
            original_class = original_result["advanced_classification"]["task_type"]
            graph_class = graph_result["advanced_classification"]["task_type"]

            print(f"\nClassification comparison:")
            print(f"Original: {original_class}")
            print(f"LangGraph: {graph_class}")
            print(f"Match: {original_class == graph_class}")

if __name__ == "__main__":
    main()



