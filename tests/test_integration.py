
"""
Integration tests for Input Processing components
"""

import sys
import os
import tempfile
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.agents.input_processing.input_agent import InputAgent, input_agent
from src.agents.input_processing.modality_detector import ModalityDetector, modality_detector
from src.agents.input_processing.preprocessor import Preprocessor, preprocessor





def test_full_input_processing_pipeline():
    """Test the complete input processing pipeline"""
    # Create test files
    text_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    text_file.write("Sample text content for integration test")
    text_file_path = text_file.name

    pdf_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    pdf_file.write(b"Sample PDF content")
    pdf_file_path = pdf_file.name

    audio_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
    audio_file.write(b"Sample audio content")
    audio_file_path = audio_file.name

    image_file = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    image_file.write(b"Sample image content")
    image_file_path = image_file.name

    try:
        # Test text processing pipeline
        text_result = input_agent.process(text_file_path)
        assert text_result.modality == "text"
        assert text_result.content == text_file_path

        # Test PDF processing pipeline
        pdf_result = input_agent.process(pdf_file_path)
        assert pdf_result.modality == "pdf"
        assert pdf_result.content == pdf_file_path

        # Test audio processing pipeline
        audio_result = input_agent.process(audio_file_path)
        assert audio_result.modality == "audio"
        assert audio_result.content == audio_file_path

        # Test image processing pipeline
        image_result = input_agent.process(image_file_path)
        assert image_result.modality == "image"
        assert image_result.content == image_file_path

        # Test modality detection
        assert modality_detector.detect(text_file_path) == "text"
        assert modality_detector.detect(pdf_file_path) == "pdf"
        assert modality_detector.detect(audio_file_path) == "audio"
        assert modality_detector.detect(image_file_path) == "image"

        # Test preprocessing
        text_content, text_meta = preprocessor.preprocess_file(text_file_path, "text")
        # Read the file directly to verify content
        with open(text_file_path, 'r', encoding='utf-8') as f:
            expected_content = f.read()
        assert expected_content in text_content
        assert text_meta["modality"] == "text"
        assert text_meta["processing_status"] == "success"

        pdf_content, pdf_meta = preprocessor.preprocess_file(pdf_file_path, "pdf")
        assert "[Extracted text from PDF:" in pdf_content
        assert pdf_meta["modality"] == "pdf"
        assert pdf_meta["processing_status"] == "success"

        audio_content, audio_meta = preprocessor.preprocess_file(audio_file_path, "audio")
        assert "[Transcribed audio:" in audio_content
        assert audio_meta["modality"] == "audio"
        assert audio_meta["processing_status"] == "success"

        image_content, image_meta = preprocessor.preprocess_file(image_file_path, "image")
        assert "[Extracted text from image:" in image_content
        assert image_meta["modality"] == "image"
        assert image_meta["processing_status"] == "success"

    finally:
        # Clean up
        os.unlink(text_file_path)
        os.unlink(pdf_file_path)
        os.unlink(audio_file_path)
        os.unlink(image_file_path)





def test_integration_with_metadata():
    """Test integration with metadata handling"""
    # Create a test file
    test_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    test_file.write("Integration test with metadata")
    test_file_path = test_file.name

    try:
        # Define metadata
        metadata = {
            "source": "telegram",
            "user_id": "test_user_123",
            "timestamp": "2025-10-05T12:00:00Z"
        }

        # Process through input agent
        result = input_agent.process(test_file_path, metadata)

        # Verify metadata is preserved
        assert result.metadata == metadata
        assert result.metadata["source"] == "telegram"
        assert result.metadata["user_id"] == "test_user_123"

        # Process through preprocessor
        content, meta = preprocessor.preprocess_file(test_file_path, "text")

        # Read the file directly to verify content
        with open(test_file_path, 'r', encoding='utf-8') as f:
            expected_content = f.read()

        # Verify content is processed correctly
        assert expected_content in content
        assert meta["modality"] == "text"
        assert meta["processing_status"] == "success"

    finally:
        # Clean up
        os.unlink(test_file_path)





def test_error_handling_integration():
    """Test error handling in the integrated pipeline"""
    # Test with non-existent file
    result = input_agent.process("non_existent_file.txt")
    assert result.modality == "text"
    assert result.content == "non_existent_file.txt"

    # Test preprocessing of non-existent file
    content, meta = preprocessor.preprocess_file("non_existent_file.txt", "text")
    assert content == ""
    assert meta["processing_status"] == "error"
    assert "error_message" in meta
