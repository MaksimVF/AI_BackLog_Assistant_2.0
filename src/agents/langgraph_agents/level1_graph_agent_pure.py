

"""
Level 1 Graph Agent - Pure LangGraph Implementation

This module implements the Level 1 agents using LangGraph without depending on old agents.
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage

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

class Level1GraphAgentPure:
    """Agent that uses LangGraph to coordinate Level 1 processing without old agents"""

    def __init__(self):
        """Initialize the Level 1 Graph Agent"""
        logger.info("Initializing Level 1 Graph Agent (Pure LangGraph)")

        # Create the graph
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        """Create the LangGraph for Level 1 processing"""
        graph = StateGraph(GraphState)

        # Add nodes for each processing step
        graph.add_node("modality_detection", self._run_modality_detection)
        graph.add_node("input_processing", self._run_input_processing)
        graph.add_node("preprocessing", self._run_preprocessing)

        # Define the execution flow without cycles
        graph.set_entry_point("modality_detection")
        graph.add_edge("modality_detection", "input_processing")
        graph.add_edge("input_processing", "preprocessing")
        graph.set_finish_point("preprocessing")  # Set final node

        return graph

    def _run_modality_detection(self, state: GraphState) -> GraphState:
        """Run modality detection"""
        if state.modality_result is None:
            # Implement modality detection logic directly
            result = self._detect_modality(state.input_data, state.metadata)
            state.modality_result = result
            state.messages.append(AIMessage(content="Modality detection completed"))

        return state

    def _run_input_processing(self, state: GraphState) -> GraphState:
        """Run input processing"""
        if state.input_result is None and state.modality_result:
            # Implement input processing logic directly
            result = self._process_input(state.input_data, state.modality_result)
            state.input_result = result
            state.messages.append(AIMessage(content="Input processing completed"))

        return state

    def _run_preprocessing(self, state: GraphState) -> GraphState:
        """Run preprocessing"""
        if state.preprocessing_result is None and state.input_result:
            # Implement preprocessing logic directly
            result = self._preprocess_input(state.input_result)
            state.preprocessing_result = result
            state.messages.append(AIMessage(content="Preprocessing completed"))

        return state

    def _detect_modality(self, input_data: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Detect the modality of input data"""
        # Implement modality detection logic directly
        modality = "text"  # Default to text

        # Check if metadata provides modality information
        if metadata and "modality" in metadata:
            modality = metadata["modality"]
        elif metadata and "filename" in metadata:
            # Detect from filename
            filename = metadata["filename"]
            ext = filename.lower().split('.')[-1] if '.' in filename else ""

            # Map extensions to modalities
            audio_extensions = {'mp3', 'wav', 'm4a', 'flac', 'aac', 'ogg'}
            pdf_extensions = {'pdf'}
            image_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'}

            if ext in audio_extensions:
                modality = "audio"
            elif ext in pdf_extensions:
                modality = "pdf"
            elif ext in image_extensions:
                modality = "image"

        return {
            "modality": modality,
            "confidence": 0.95,
            "method": "filename_extension" if metadata and "filename" in metadata else "default"
        }

    def _process_input(self, input_data: str, modality_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process input based on detected modality"""
        modality = modality_result.get("modality", "text")

        # For text, just return the input as is
        if modality == "text":
            return {
                "content": input_data,
                "modality": "text",
                "processing_method": "direct_text"
            }

        # For other modalities, we would implement specific processing
        # For now, return a placeholder
        return {
            "content": input_data,
            "modality": modality,
            "processing_method": f"{modality}_processing"
        }

    def _preprocess_input(self, input_result: Dict[str, Any]) -> Dict[str, Any]:
        """Preprocess input data"""
        content = input_result.get("content", "")
        modality = input_result.get("modality", "text")

        # Basic text preprocessing
        if modality == "text":
            # Simple text cleaning
            cleaned_text = content.strip()
            return {
                "content": cleaned_text,
                "modality": "text",
                "preprocessing_method": "text_cleaning",
                "token_count": len(cleaned_text.split()),
                "character_count": len(cleaned_text)
            }

        # For other modalities, we would implement specific preprocessing
        # For now, return a placeholder
        return {
            "content": content,
            "modality": modality,
            "preprocessing_method": f"{modality}_preprocessing"
        }

    def process_input(self, input_data: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process Level 1 input using pure LangGraph

        Args:
            input_data: Raw input data
            metadata: Additional metadata

        Returns:
            Processed input data
        """
        # Initialize state
        initial_state = GraphState(
            input_data=input_data,
            metadata=metadata,
            messages=[HumanMessage(content="Processing Level 1 input")]
        )

        # Compile and run the graph
        compiled_graph = self.graph.compile()
        result = compiled_graph.invoke(initial_state)

        # The result is a dictionary, extract the values
        logger.info(f"Level 1 result: {result}")
        return {
            "modality": result.get("modality_result"),
            "input": result.get("input_result"),
            "preprocessing": result.get("preprocessing_result"),
            "messages": [msg.model_dump() for msg in result.get("messages", [])]
        }

# Create a global instance for easy access
level1_graph_agent_pure = Level1GraphAgentPure()

