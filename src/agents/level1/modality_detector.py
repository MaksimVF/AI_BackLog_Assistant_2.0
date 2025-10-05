
"""
Modality Detector Module

This module is responsible for detecting the type of input (text, audio, PDF, image)
and routing it to the appropriate processing pipeline.
"""

import logging
from typing import Optional

# Configure logging
logger = logging.getLogger(__name__)







class ModalityDetector:
    """Detects the modality of input data"""

    def __init__(self):
        """Initialize the Modality Detector"""
        logger.info("Initializing Modality Detector")

    def detect_from_filename(self, filename: str) -> str:
        """
        Detect modality based on file extension

        Args:
            filename: Name of the file to analyze

        Returns:
            Detected modality type
        """
        if not filename:
            return "unknown"

        # Get file extension
        ext = filename.lower().split('.')[-1] if '.' in filename else ""

        # Map extensions to modalities
        audio_extensions = {'mp3', 'wav', 'm4a', 'flac', 'aac', 'ogg'}
        pdf_extensions = {'pdf'}
        image_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'}

        if ext in audio_extensions:
            return "audio"
        elif ext in pdf_extensions:
            return "pdf"
        elif ext in image_extensions:
            return "image"
        elif ext in {'txt', 'md', 'doc', 'docx'}:
            return "text"
        else:
            return "unknown"

    def detect_from_mimetype(self, mimetype: str) -> str:
        """
        Detect modality based on MIME type

        Args:
            mimetype: MIME type of the content

        Returns:
            Detected modality type
        """
        if not mimetype:
            return "unknown"

        if mimetype.startswith('audio/'):
            return "audio"
        elif mimetype.startswith('application/pdf'):
            return "pdf"
        elif mimetype.startswith('image/'):
            return "image"
        elif mimetype.startswith('text/'):
            return "text"
        else:
            return "unknown"

    def detect_from_content(self, content: str, max_length: int = 1000) -> str:
        """
        Detect modality based on content analysis (basic heuristic)

        Args:
            content: Content to analyze
            max_length: Maximum length of content to analyze

        Returns:
            Detected modality type
        """
        # Truncate content if too long
        truncated = content[:max_length]

        # Simple heuristics - this would be more sophisticated in production
        if len(truncated) > 0:
            # Check if content contains only valid text characters
            if all(c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.;:!?()[]{}-_+=/@#$%^&*\"'\\|<>" for c in truncated):
                return "text"
            else:
                return "unknown"
        else:
            return "unknown"

    def detect(self, input_data: str, mimetype: Optional[str] = None) -> str:
        """
        Main detection method that uses multiple strategies

        Args:
            input_data: Input data to analyze
            mimetype: Optional MIME type hint

        Returns:
            Detected modality type
        """
        if mimetype:
            detected = self.detect_from_mimetype(mimetype)
            if detected != "unknown":
                return detected

        # Try filename detection
        detected = self.detect_from_filename(input_data)
        if detected != "unknown":
            return detected

        # Try content detection
        return self.detect_from_content(input_data)

# Create a global instance for easy access
modality_detector = ModalityDetector()
