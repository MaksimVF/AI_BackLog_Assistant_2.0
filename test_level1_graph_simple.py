


"""
Simple test for Level 1 LangGraph implementation
"""

import logging
import sys
import os
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.level1.input_agent import InputAgent
from agents.level1.modality_detector import ModalityDetector
from agents.level1.preprocessor import Preprocessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GraphState(BaseModel):
    """State for the Level 1 graph processing"""
    input_data: str
    metadata: Optional[Dict[str, Any]] = None
    modality_detection: Optional[Dict[str, Any]] = None
    input_processing: Optional[Dict[str, Any]] = None
    preprocessing_result: Optional[Dict[str, Any]] = None
    messages: List[Any] = []

class Level1GraphAgentSimple:
    """Simple Level 1 Graph Agent for testing"""

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
        graph.add_node("modality_detection", self._run_modality_detection)
        graph.add_node("input_processing", self._run_input_processing)
        graph.add_node("preprocessing", self._run_preprocessing)

        # Define the execution flow
        graph.set_entry_point("modality_detection")
        graph.add_edge("modality_detection", "input_processing")
        graph.add_edge("input_processing", "preprocessing")
        graph.set_finish_point("preprocessing")  # Set final node

        return graph

    def _run_modality_detection(self, state: GraphState) -> GraphState:
        """Run modality detection"""
        if state.modality_detection is None:
            modality = self.modality_detector.detect(state.input_data)
            result = {
                "modality": modality,
                "detection_method": "filename_extension"
            }
            state.modality_detection = result
            state.messages.append(AIMessage(content=f"Modality detected: {modality}"))

        return state

    def _run_input_processing(self, state: GraphState) -> GraphState:
        """Run input processing"""
        if state.input_processing is None:
            processed_data = self.input_agent.process(state.input_data, state.metadata)
            result = {
                "content": processed_data.content,
                "modality": processed_data.modality,
                "metadata": processed_data.metadata
            }
            state.input_processing = result
            state.messages.append(AIMessage(content=f"Input processed as {processed_data.modality}"))

        return state

    def _run_preprocessing(self, state: GraphState) -> GraphState:
        """Run preprocessing for file-based inputs"""
        if state.preprocessing_result is None:
            modality = state.modality_detection.get("modality", "text")
            if modality in ["pdf", "audio", "image"]:
                # For file-based inputs, use preprocessor
                file_path = state.input_processing.get("content", "")
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
                    "processed_text": state.input_processing.get("content", ""),
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

def test_level1_graph_agent():
    """Test the Level 1 Graph Agent"""

    # Create the agent
    agent = Level1GraphAgentSimple()

    # Test cases
    test_cases = [
        {
            "name": "Text input",
            "input": "This is a simple text message",
            "expected_modality": "text"
        },
        {
            "name": "PDF file path",
            "input": "document.pdf",
            "expected_modality": "pdf"
        },
        {
            "name": "Audio file path",
            "input": "recording.mp3",
            "expected_modality": "audio"
        },
        {
            "name": "Image file path",
            "input": "screenshot.png",
            "expected_modality": "image"
        }
    ]

    for test_case in test_cases:
        print(f"\n--- Testing {test_case['name']} ---")
        print(f"Input: {test_case['input']}")

        # Process the input
        result = agent.process_input(test_case['input'])

        detected_modality = result["modality_detection"].get("modality", "unknown")
        print(f"Detected modality: {detected_modality}")
        print(f"Expected modality: {test_case['expected_modality']}")
        print(f"Content: {result['input_processing'].get('content', '')[:100]}...")  # Show first 100 chars

        # Verify the result
        if detected_modality == test_case['expected_modality']:
            print("✅ Test passed")
        else:
            print("❌ Test failed")

        # Show metadata
        print(f"Metadata keys: {list(result.keys())}")

if __name__ == "__main__":
    test_level1_graph_agent()



