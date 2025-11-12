

"""
Simple test for LangGraph implementation
"""

from src.agents.langgraph_agents.level2_graph_agent import Level2GraphAgent

def main():
    """Test the LangGraph agent"""
    agent = Level2GraphAgent()

    # Test with a simple input
    text = "This is a test input for the LangGraph agent."

    try:
        result = agent.analyze_text(text)
        print("Test successful!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

