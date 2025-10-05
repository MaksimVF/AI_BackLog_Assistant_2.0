
"""
Test cases for Preprocessor
"""

import sys
import os
import tempfile
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.agents.input_processing.preprocessor import Preprocessor







def test_preprocessor_initialization():
    """Test that Preprocessor initializes correctly"""
    preprocessor = Preprocessor()
    assert preprocessor is not None







def test_text_file_processing():
    """Test processing of text files"""
    preprocessor = Preprocessor()

    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Sample text content")
        temp_path = f.name

    try:
        # Test text file processing
        text, metadata = preprocessor.preprocess_file(temp_path, "text")

        assert "Sample text content" in text
        assert metadata["file_path"] == temp_path
        assert metadata["modality"] == "text"
        assert metadata["processing_status"] == "success"

    finally:
        # Clean up
        os.unlink(temp_path)







def test_pdf_processing():
    """Test PDF processing (mocked)"""
    preprocessor = Preprocessor()

    # Create a temporary file with pdf extension
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        f.write(b"Sample PDF content")
        temp_path = f.name

    try:
        # Test PDF processing
        text, metadata = preprocessor.preprocess_file(temp_path, "pdf")

        assert "[Extracted text from PDF:" in text
        assert metadata["file_path"] == temp_path
        assert metadata["modality"] == "pdf"
        assert metadata["processing_status"] == "success"

    finally:
        # Clean up
        os.unlink(temp_path)







def test_audio_processing():
    """Test audio processing (mocked)"""
    preprocessor = Preprocessor()

    # Create a temporary file with audio extension
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
        f.write(b"Sample audio content")
        temp_path = f.name

    try:
        # Test audio processing
        text, metadata = preprocessor.preprocess_file(temp_path, "audio")

        assert "[Transcribed audio:" in text
        assert metadata["file_path"] == temp_path
        assert metadata["modality"] == "audio"
        assert metadata["processing_status"] == "success"

    finally:
        # Clean up
        os.unlink(temp_path)







def test_image_processing():
    """Test image processing (mocked)"""
    preprocessor = Preprocessor()

    # Create a temporary file with image extension
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
        f.write(b"Sample image content")
        temp_path = f.name

    try:
        # Test image processing
        text, metadata = preprocessor.preprocess_file(temp_path, "image")

        assert "[Extracted text from image:" in text
        assert metadata["file_path"] == temp_path
        assert metadata["modality"] == "image"
        assert metadata["processing_status"] == "success"

    finally:
        # Clean up
        os.unlink(temp_path)







def test_error_handling():
    """Test error handling in preprocessing"""
    preprocessor = Preprocessor()

    # Test with non-existent file
    text, metadata = preprocessor.preprocess_file("non_existent_file.txt", "text")

    assert text == ""
    assert metadata["processing_status"] == "error"
    assert "error_message" in metadata
