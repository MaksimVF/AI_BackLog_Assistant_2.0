
"""
Semantic Block Classifier Module

This module is responsible for segmenting text into semantic blocks
(headers, paragraphs, tables, etc.) for better analysis.
"""

import logging
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)



class SemanticBlock(BaseModel):
    """Data model for a semantic block"""
    block_type: str  # header, paragraph, table, list, etc.
    content: str
    start_index: int
    end_index: int
    metadata: Optional[Dict[str, Any]] = None



class SemanticBlockClassifier:
    """Agent for classifying text into semantic blocks"""

    def __init__(self):
        """Initialize the Semantic Block Classifier"""
        logger.info("Initializing Semantic Block Classifier")

    def _is_header(self, line: str) -> bool:
        """Check if a line is a header (simple heuristic)"""
        # Headers are typically short, end with colon, or are in ALL CAPS
        stripped = line.strip()
        if not stripped:
            return False

        if len(stripped) < 80 and (stripped.endswith(':') or stripped.isupper()):
            return True

        # Check for Markdown headers
        if re.match(r'^[#]{1,6}\s+', stripped):
            return True

        return False

    def _is_list_item(self, line: str) -> bool:
        """Check if a line is a list item"""
        stripped = line.strip()
        return bool(re.match(r'^[-\*•]\s+|^\d+\.\s+', stripped))

    def _is_table_row(self, line: str) -> bool:
        """Check if a line looks like a table row"""
        # Simple check for pipe-separated values
        return '|' in line and not line.strip().startswith('|')

    def segment_text(self, text: str) -> List[SemanticBlock]:
        """
        Segment text into semantic blocks

        Args:
            text: Input text to segment

        Returns:
            List of semantic blocks
        """
        blocks = []
        lines = text.split('\n')
        current_block = None
        current_content = []

        for i, line in enumerate(lines):
            if self._is_header(line):
                # Save previous block if exists
                if current_block:
                    blocks.append(current_block)
                # Start new header block
                current_block = SemanticBlock(
                    block_type="header",
                    content=line,
                    start_index=i,
                    end_index=i,
                    metadata={"level": "h1" if line.startswith('# ') else "h2"}
                )
                current_content = [line]
            elif self._is_list_item(line):
                # Save previous block if exists and it's not a list
                if current_block and current_block.block_type != "list":
                    blocks.append(current_block)
                    current_block = None

                # Start or continue list block
                if not current_block:
                    current_block = SemanticBlock(
                        block_type="list",
                        content=line,
                        start_index=i,
                        end_index=i,
                        metadata={"list_type": "bullet" if line.strip().startswith(('-', '•', '*')) else "numbered"}
                    )
                    current_content = [line]
                else:
                    # Continue current list
                    current_content.append(line)
                    current_block.end_index = i
                    current_block.content = '\n'.join(current_content)
            elif self._is_table_row(line):
                # Save previous block if exists and it's not a table
                if current_block and current_block.block_type != "table":
                    blocks.append(current_block)
                    current_block = None

                # Start or continue table block
                if not current_block:
                    current_block = SemanticBlock(
                        block_type="table",
                        content=line,
                        start_index=i,
                        end_index=i,
                        metadata={"row_count": 1}
                    )
                    current_content = [line]
                else:
                    # Continue current table
                    current_content.append(line)
                    current_block.end_index = i
                    current_block.content = '\n'.join(current_content)
                    current_block.metadata["row_count"] = len(current_content)
            else:
                # Regular paragraph text
                if not current_block:
                    current_block = SemanticBlock(
                        block_type="paragraph",
                        content=line,
                        start_index=i,
                        end_index=i,
                        metadata={}
                    )
                    current_content = [line]
                elif current_block.block_type == "paragraph":
                    # Continue current paragraph
                    current_content.append(line)
                    current_block.end_index = i
                    current_block.content = '\n'.join(current_content)
                else:
                    # Save previous block and start new paragraph
                    blocks.append(current_block)
                    current_block = SemanticBlock(
                        block_type="paragraph",
                        content=line,
                        start_index=i,
                        end_index=i,
                        metadata={}
                    )
                    current_content = [line]

        # Add the last block if it exists
        if current_block:
            blocks.append(current_block)

        return blocks

    def classify_blocks(self, text: str) -> Dict[str, Any]:
        """
        Classify text into semantic blocks and return analysis

        Args:
            text: Input text to classify

        Returns:
            Analysis result with blocks and statistics
        """
        blocks = self.segment_text(text)

        # Generate statistics
        block_types = [block.block_type for block in blocks]
        stats = {
            "total_blocks": len(blocks),
            "block_types": {block_type: block_types.count(block_type) for block_type in set(block_types)},
            "text_length": len(text)
        }

        return {
            "blocks": [block.model_dump() for block in blocks],
            "statistics": stats
        }

# Create a global instance for easy access
semantic_block_classifier = SemanticBlockClassifier()
