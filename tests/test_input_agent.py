
"""
Test cases for Input Agent
"""

import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
import pytest
from src.agents.input_processing.input_agent import InputAgent, InputData


def test_input_agent_initialization():
    """Test that InputAgent initializes correctly"""
    agent = InputAgent()
    assert agent is not None


def test_text_processing():
    """Test text processing functionality"""
    agent = InputAgent()
    result = agent.process_text("Sample text input")

    assert isinstance(result, InputData)
    assert result.modality == "text"
    assert result.content == "Sample text input"


def test_modality_detection():
    """Test modality detection for different file types"""
    agent = InputAgent()

    # Test audio files
    assert agent.detect_modality("test.mp3") == "audio"
    assert agent.detect_modality("test.wav") == "audio"

    # Test PDF files
    assert agent.detect_modality("document.pdf") == "pdf"

    # Test image files
    assert agent.detect_modality("image.jpg") == "image"
    assert agent.detect_modality("image.png") == "image"

    # Test text (default)
    assert agent.detect_modality("plain text") == "text"
    assert agent.detect_modality("document.txt") == "text"


def test_process_method():
    """Test the main process method with different modalities"""
    agent = InputAgent()

    # Test text processing
    text_result = agent.process("Sample text")
    assert text_result.modality == "text"
    assert text_result.content == "Sample text"

    # Test audio processing
    audio_result = agent.process("test.mp3")
    assert audio_result.modality == "audio"
    assert audio_result.content == "test.mp3"

    # Test PDF processing
    pdf_result = agent.process("document.pdf")
    assert pdf_result.modality == "pdf"
    assert pdf_result.content == "document.pdf"

    # Test image processing
    image_result = agent.process("image.jpg")
    assert image_result.modality == "image"
    assert image_result.content == "image.jpg"


def test_metadata_handling():
    """Test that metadata is properly handled"""
    agent = InputAgent()
    metadata = {"source": "telegram", "user_id": "12345"}

    result = agent.process_text("Test with metadata", metadata)

    assert result.metadata == metadata
    assert result.metadata["source"] == "telegram"
    assert result.metadata["user_id"] == "12345"
