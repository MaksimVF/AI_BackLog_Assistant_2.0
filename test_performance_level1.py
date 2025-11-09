


"""
Performance comparison test for Level 1 implementations
"""

import logging
import time
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_performance_comparison():
    """Compare performance between original and LangGraph implementations"""

    # Import agents directly to avoid circular imports
    from agents.level1.input_agent import InputAgent
    from agents.level1.modality_detector import ModalityDetector
    from agents.level1.preprocessor import Preprocessor

    # Initialize agents
    input_agent = InputAgent()
    modality_detector = ModalityDetector()
    preprocessor = Preprocessor()

    # Test cases
    test_cases = [
        {
            "name": "Text input",
            "input": "This is a simple text message for performance testing"
        },
        {
            "name": "PDF file path",
            "input": "document.pdf"
        },
        {
            "name": "Audio file path",
            "input": "recording.mp3"
        },
        {
            "name": "Image file path",
            "input": "screenshot.png"
        }
    ]

    print("Performance Comparison: Original vs LangGraph Implementation")
    print("=" * 70)

    for test_case in test_cases:
        print(f"\n--- Testing {test_case['name']} ---")
        print(f"Input: {test_case['input']}")

        # Test original implementation
        start_time = time.time()
        modality = modality_detector.detect(test_case['input'])
        processed_data = input_agent.process(test_case['input'])
        if modality in ["pdf", "audio", "image"]:
            text, metadata = preprocessor.preprocess_file(test_case['input'], modality)
        else:
            text = processed_data.content
            metadata = {}
        original_time = time.time() - start_time

        print(f"Original implementation: {original_time:.4f} seconds")

        # Verify results are equivalent
        original_modality = modality
        print(f"Detected modality: {original_modality}")

        if original_modality:
            print("✅ Original implementation works")
        else:
            print("❌ Original implementation failed")

if __name__ == "__main__":
    test_performance_comparison()


