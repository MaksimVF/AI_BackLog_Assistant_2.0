


"""
Simple test script for Level 1 LangGraph implementation
"""

import logging
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agents.level1.input_agent import InputAgent
from agents.level1.modality_detector import ModalityDetector
from agents.level1.preprocessor import Preprocessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_level1_agents():
    """Test the Level 1 agents directly"""

    # Initialize agents
    input_agent = InputAgent()
    modality_detector = ModalityDetector()
    preprocessor = Preprocessor()

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

        # Step 1: Detect modality
        modality = modality_detector.detect(test_case['input'])
        print(f"Detected modality: {modality}")
        print(f"Expected modality: {test_case['expected_modality']}")

        # Step 2: Process input
        processed_data = input_agent.process(test_case['input'])
        print(f"Processed content: {processed_data.content[:100]}...")

        # Step 3: Preprocess if needed
        if modality in ["pdf", "audio", "image"]:
            text, metadata = preprocessor.preprocess_file(test_case['input'], modality)
            print(f"Preprocessed text: {text[:100]}...")
            print(f"Metadata: {metadata}")

        # Verify the result
        if modality == test_case['expected_modality']:
            print("✅ Test passed")
        else:
            print("❌ Test failed")

if __name__ == "__main__":
    test_level1_agents()


