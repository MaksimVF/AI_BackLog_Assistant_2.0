




"""
Level 1 Graph Agent

This module implements the Level 1 agents using LangGraph for enhanced
coordination and processing of input data.
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage

# Import existing agents for integration
from src.agents.level1.input_agent import InputAgent
from src.agents.level1.modality_detector import ModalityDetector
from src.agents.level1.preprocessor import Preprocessor

# Configure logging
logger = logging.getLogger(__name__)

class GraphState(BaseModel):
    """State for the Level 1 graph processing"""
    input_data: str
    metadata: Optional[Dict[str, Any]] = None
    modality_result: Optional[Dict[str, Any]] = None
    input_result: Optional[Dict[str, Any]] = None
    preprocessing_result: Optional[Dict[str, Any]] = None
    messages: List[Any] = []

class Level1GraphAgent:
    """Agent that uses LangGraph to coordinate Level 1 processing"""

    def __init__(self):
        """Initialize the Level 1 Graph Agent"""
        logger.info("Initializing Level 1 Graph Agent")

        # Initialize component agents
        self.input_agent = InputAgent()
        self.modality_detector = ModalityDetector()
        self.preprocessor = Preprocessor()

        # Create the graph
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        """Create the LangGraph for Level 1 processing"""
        graph = StateGraph(GraphState)

        # Add nodes for each processing step
        graph.add_node("detect_modality", self._run_modality_detection)
        graph.add_node("process_input", self._run_input_processing)
        graph.add_node("preprocess", self._run_preprocessing)

        # Define the execution flow
        graph.set_entry_point("detect_modality")
        graph.add_edge("detect_modality", "process_input")
        graph.add_edge("process_input", "preprocess")
        graph.set_finish_point("preprocess")  # Set final node

        return graph

    def _run_modality_detection(self, state: GraphState) -> GraphState:
        """Run modality detection"""
        if state.modality_result is None:
            modality = self.modality_detector.detect(state.input_data)
            result = {
                "modality": modality,
                "detection_method": "filename_extension"
            }
            state.modality_result = result
            state.messages.append(AIMessage(content=f"Modality detected: {modality}"))

        return state

    def _run_input_processing(self, state: GraphState) -> GraphState:
        """Run input processing"""
        if state.input_result is None:
            processed_data = self.input_agent.process(state.input_data, state.metadata)
            result = {
                "content": processed_data.content,
                "modality": processed_data.modality,
                "metadata": processed_data.metadata
            }
            state.input_result = result
            state.messages.append(AIMessage(content=f"Input processed as {processed_data.modality}"))

        return state

    def _run_preprocessing(self, state: GraphState) -> GraphState:
        """Run preprocessing for file-based inputs"""
        if state.preprocessing_result is None:
            modality = state.modality_result.get("modality", "text")
            if modality in ["pdf", "audio", "image"]:
                # For file-based inputs, use preprocessor
                file_path = state.input_result.get("content", "")
                text, metadata = self.preprocessor.preprocess_file(file_path, modality)
                result = {
                    "processed_text": text,
                    "metadata": metadata
                }
                state.preprocessing_result = result
                state.messages.append(AIMessage(content=f"Preprocessing completed for {modality}"))
            else:
                # For text inputs, no preprocessing needed
                result = {
                    "processed_text": state.input_result.get("content", ""),
                    "metadata": {"processing_status": "not_required"}
                }
                state.preprocessing_result = result
                state.messages.append(AIMessage(content="No preprocessing needed for text input"))

        return state

    def process_input(self, input_data: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process input using the LangGraph-based Level 1 pipeline

        Args:
            input_data: Raw input data
            metadata: Additional metadata

        Returns:
            Processed data with all agent outputs
        """
        # Initialize state
        initial_state = GraphState(
            input_data=input_data,
            metadata=metadata or {},
            messages=[HumanMessage(content=input_data)]
        )

        # Compile and run the graph
        compiled_graph = self.graph.compile()
        result = compiled_graph.invoke(initial_state)

        # Extract the values from the result
        return {
            "input_data": result.get("input_data", initial_state.input_data),
            "modality_detection": result.get("modality_detection"),
            "input_processing": result.get("input_processing"),
            "preprocessing": result.get("preprocessing_result"),
            "messages": [msg.model_dump() for msg in result.get("messages", [])]
        }

# Create a global instance for easy access
level1_graph_agent = Level1GraphAgent()




