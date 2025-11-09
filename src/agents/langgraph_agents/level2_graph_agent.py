

"""
Level 2 Graph Agent

This module implements the Level 2 agents using LangGraph for enhanced
coordination and processing.
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage

# Import existing agents for integration
from src.agents.level2.advanced_task_classifier import AdvancedTaskClassifier
from src.agents.level2.reflection_agent import ReflectionAgent
from src.agents.level2.semantic_block_classifier import SemanticBlockClassifier
from src.agents.level2.contextualiza_agent import ContextualizaAgent

# Configure logging
logger = logging.getLogger(__name__)

class GraphState(BaseModel):
    """State for the Level 2 graph processing"""
    input_text: str
    classification_result: Optional[Dict[str, Any]] = None
    reflection_result: Optional[Dict[str, Any]] = None
    semantic_blocks: Optional[Dict[str, Any]] = None
    context_analysis: Optional[Dict[str, Any]] = None
    messages: List[Any] = []

class Level2GraphAgent:
    """Agent that uses LangGraph to coordinate Level 2 processing"""

    def __init__(self):
        """Initialize the Level 2 Graph Agent"""
        logger.info("Initializing Level 2 Graph Agent")

        # Initialize component agents
        self.advanced_classifier = AdvancedTaskClassifier()
        self.reflection_agent = ReflectionAgent()
        self.semantic_classifier = SemanticBlockClassifier()
        self.context_agent = ContextualizaAgent()

        # Create the graph
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        """Create the LangGraph for Level 2 processing"""
        graph = StateGraph(GraphState)

        # Add nodes for each processing step
        graph.add_node("classify_task", self._run_advanced_classification)
        graph.add_node("reflection_analysis", self._run_reflection_analysis)
        graph.add_node("semantic_segmentation", self._run_semantic_segmentation)
        graph.add_node("context_extraction", self._run_context_extraction)

        # Define the execution flow without cycles
        graph.set_entry_point("classify_task")
        graph.add_edge("classify_task", "reflection_analysis")
        graph.add_edge("reflection_analysis", "semantic_segmentation")
        graph.add_edge("semantic_segmentation", "context_extraction")
        graph.set_finish_point("context_extraction")  # Set final node

        return graph

    def _run_advanced_classification(self, state: GraphState) -> GraphState:
        """Run advanced task classification"""
        if state.classification_result is None:
            result = self.advanced_classifier.classify_task(state.input_text)
            state.classification_result = result.model_dump()
            state.messages.append(AIMessage(content=f"Advanced classification: {result.task_type}"))

        return state

    def _run_reflection_analysis(self, state: GraphState) -> GraphState:
        """Run reflection analysis"""
        if state.reflection_result is None:
            result = self.reflection_agent.interpret_task(state.input_text)
            state.reflection_result = result
            state.messages.append(AIMessage(content=f"Reflection analysis: {result['task_type']}"))

        return state

    def _run_semantic_segmentation(self, state: GraphState) -> GraphState:
        """Run semantic segmentation"""
        if state.semantic_blocks is None:
            result = self.semantic_classifier.classify_blocks(state.input_text)
            state.semantic_blocks = result
            state.messages.append(AIMessage(content="Semantic segmentation completed"))

        return state

    def _run_context_extraction(self, state: GraphState) -> GraphState:
        """Run context extraction"""
        if state.context_analysis is None:
            result = self.context_agent.extract_entities(state.input_text)
            state.context_analysis = result
            state.messages.append(AIMessage(content="Context extraction completed"))

        return state

    def analyze_text(self, text: str, max_iterations: int = 3) -> Dict[str, Any]:
        """
        Analyze text using the LangGraph-based Level 2 pipeline

        Args:
            text: Input text to analyze
            max_iterations: Maximum number of graph iterations

        Returns:
            Analysis results with all agent outputs
        """
        # Initialize state
        initial_state = GraphState(
            input_text=text,
            messages=[HumanMessage(content=text)]
        )

        # Compile and run the graph
        compiled_graph = self.graph.compile()
        result = compiled_graph.invoke(initial_state)

        # The result is a dictionary, extract the values
        return {
            "input_text": result.get("input_text", initial_state.input_text),
            "advanced_classification": result.get("advanced_classification"),
            "reflection": result.get("reflection_result"),
            "semantic_blocks": result.get("semantic_blocks"),
            "context": result.get("context_analysis"),
            "messages": [msg.model_dump() for msg in result.get("messages", [])]
        }

# Create a global instance for easy access
level2_graph_agent = Level2GraphAgent()

