
"""
Test cases for Modality Detector
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.agents.level1.modality_detector import ModalityDetector










def test_modality_detector_initialization():
    """Test that ModalityDetector initializes correctly"""
    detector = ModalityDetector()
    assert detector is not None










def test_filename_detection():
    """Test modality detection from filenames"""
    detector = ModalityDetector()

    # Test audio files
    assert detector.detect_from_filename("test.mp3") == "audio"
    assert detector.detect_from_filename("audio.wav") == "audio"
    assert detector.detect_from_filename("sound.m4a") == "audio"

    # Test PDF files
    assert detector.detect_from_filename("document.pdf") == "pdf"

    # Test image files
    assert detector.detect_from_filename("image.jpg") == "image"
    assert detector.detect_from_filename("photo.png") == "image"
    assert detector.detect_from_filename("scan.gif") == "image"

    # Test text files
    assert detector.detect_from_filename("notes.txt") == "text"
    assert detector.detect_from_filename("document.docx") == "text"

    # Test unknown files
    assert detector.detect_from_filename("unknown.exe") == "unknown"
    assert detector.detect_from_filename("") == "unknown"










def test_mimetype_detection():
    """Test modality detection from MIME types"""
    detector = ModalityDetector()

    # Test audio MIME types
    assert detector.detect_from_mimetype("audio/mpeg") == "audio"
    assert detector.detect_from_mimetype("audio/wav") == "audio"

    # Test PDF MIME type
    assert detector.detect_from_mimetype("application/pdf") == "pdf"

    # Test image MIME types
    assert detector.detect_from_mimetype("image/jpeg") == "image"
    assert detector.detect_from_mimetype("image/png") == "image"

    # Test text MIME types
    assert detector.detect_from_mimetype("text/plain") == "text"
    assert detector.detect_from_mimetype("text/html") == "text"

    # Test unknown MIME type
    assert detector.detect_from_mimetype("application/octet-stream") == "unknown"
    assert detector.detect_from_mimetype("") == "unknown"










def test_content_detection():
    """Test modality detection from content"""
    detector = ModalityDetector()

    # Test text content
    assert detector.detect_from_content("This is some text content") == "text"
    assert detector.detect_from_content("Hello world!") == "text"

    # Test with special characters
    assert detector.detect_from_content("Text with symbols: !@#$%^&*()") == "text"

    # Test empty content
    assert detector.detect_from_content("") == "unknown"










def test_main_detection_method():
    """Test the main detection method with different inputs"""
    detector = ModalityDetector()

    # Test with MIME type hint
    assert detector.detect("document.pdf", "application/pdf") == "pdf"
    assert detector.detect("audio.mp3", "audio/mpeg") == "audio"

    # Test with filename only
    assert detector.detect("image.jpg") == "image"
    assert detector.detect("notes.txt") == "text"

    # Test with unknown input (should default to text for unknown file extensions)
    assert detector.detect("unknown.bin") == "text"
