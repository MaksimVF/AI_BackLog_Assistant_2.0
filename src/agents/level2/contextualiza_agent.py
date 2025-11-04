
"""
Contextualiza Agent Module

This module is responsible for extracting entities and determining the domain
of the input text to provide contextual understanding.
"""

import logging
import re
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from src.utils.llm_client import llm_client
from src.utils.prompts import CONTEXTUALIZA_PROMPT

# Configure logging
logger = logging.getLogger(__name__)








class Entity(BaseModel):
    """Data model for an extracted entity"""
    entity_type: str  # person, organization, location, date, etc.
    text: str
    start_index: int
    end_index: int
    confidence: float








class ContextAnalysis(BaseModel):
    """Data model for context analysis results"""
    domain: str  # e.g., IT, marketing, finance, etc.
    entities: List[Entity]
    metadata: Optional[Dict[str, Any]] = None








class ContextualizaAgent:
    """Agent for extracting context and entities from text"""

    def __init__(self):
        """Initialize the Contextualiza Agent"""
        logger.info("Initializing Contextualiza Agent")

    def _simple_entity_extraction(self, text: str) -> List[Entity]:
        """Simple entity extraction using regex patterns"""
        entities = []

        # Email extraction
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        for match in re.finditer(email_pattern, text):
            entities.append(Entity(
                entity_type="email",
                text=match.group(),
                start_index=match.start(),
                end_index=match.end(),
                confidence=0.9
            ))

        # URL extraction
        url_pattern = r'https?://\S+|www\.\S+'
        for match in re.finditer(url_pattern, text):
            entities.append(Entity(
                entity_type="url",
                text=match.group(),
                start_index=match.start(),
                end_index=match.end(),
                confidence=0.9
            ))

        # Date extraction (simple pattern)
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b'
        for match in re.finditer(date_pattern, text):
            entities.append(Entity(
                entity_type="date",
                text=match.group(),
                start_index=match.start(),
                end_index=match.end(),
                confidence=0.8
            ))

        # Simple domain keywords detection
        domain_keywords = {
            "IT": ["software", "code", "programming", "database", "server", "API", "cloud"],
            "marketing": ["campaign", "brand", "advertising", "social media", "SEO", "CTR"],
            "finance": ["revenue", "profit", "budget", "investment", "ROI", "expenses"]
        }

        # Add domain entities
        for domain, keywords in domain_keywords.items():
            for keyword in keywords:
                keyword_pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
                for match in keyword_pattern.finditer(text):
                    entities.append(Entity(
                        entity_type=domain.lower(),
                        text=match.group(),
                        start_index=match.start(),
                        end_index=match.end(),
                        confidence=0.7
                    ))

        return entities

    def _determine_domain(self, text: str, entities: List[Entity]) -> str:
        """Determine the domain based on text content and entities"""
        # Simple keyword-based domain detection
        text_lower = text.lower()

        domain_scores = {
            "it": 0,
            "marketing": 0,
            "finance": 0,
            "general": 1  # default
        }

        # Check for domain keywords
        it_keywords = ["software", "code", "programming", "database", "server", "api", "cloud"]
        marketing_keywords = ["campaign", "brand", "advertising", "social media", "seo", "ctr"]
        finance_keywords = ["revenue", "profit", "budget", "investment", "roi", "expenses"]

        # Score based on keywords
        for keyword in it_keywords:
            if keyword in text_lower:
                domain_scores["it"] += 1

        for keyword in marketing_keywords:
            if keyword in text_lower:
                domain_scores["marketing"] += 1

        for keyword in finance_keywords:
            if keyword in text_lower:
                domain_scores["finance"] += 1

        # Score based on entities
        for entity in entities:
            if entity.entity_type in ["it", "email", "url"]:  # tech-related
                domain_scores["it"] += 0.5
            elif entity.entity_type == "marketing":
                domain_scores["marketing"] += 0.5
            elif entity.entity_type == "finance":
                domain_scores["finance"] += 0.5

        # Determine highest score
        best_domain = max(domain_scores.items(), key=lambda x: x[1])[0]
        return best_domain

    def analyze_context(self, text: str) -> ContextAnalysis:
        """
        Analyze the context of the text including domain detection and entity extraction

        Args:
            text: Input text to analyze

        Returns:
            Context analysis results
        """
        # Try to use LLM for context analysis if available
        try:
            # Use the LLM client for context analysis
            prompt = CONTEXTUALIZA_PROMPT.format(input_text=text)
            response = llm_client.generate_json(prompt)

            if response and "entities" in response and "domain" in response:
                # Parse LLM response
                entities = []
                for entity_data in response["entities"]:
                    entities.append(Entity(
                        entity_type=entity_data.get("type", "unknown"),
                        text=entity_data.get("text", ""),
                        start_index=entity_data.get("start_index", 0),
                        end_index=entity_data.get("end_index", 0),
                        confidence=entity_data.get("confidence", 0.7)
                    ))

                return ContextAnalysis(
                    domain=response["domain"],
                    entities=entities,
                    metadata={
                        "text_length": len(text),
                        "entity_count": len(entities),
                        "analysis_method": "llm"
                    }
                )

        except Exception as e:
            logger.warning(f"LLM context analysis failed, falling back to heuristic: {e}")
            # Fallback to simple heuristic
            entities = self._simple_entity_extraction(text)
            domain = self._determine_domain(text, entities)

            return ContextAnalysis(
                domain=domain,
                entities=entities,
                metadata={
                    "text_length": len(text),
                    "entity_count": len(entities),
                    "analysis_method": "keyword_based"
                }
            )

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Extract entities and provide context analysis

        Args:
            text: Input text to analyze

        Returns:
            Context analysis result as dictionary
        """
        try:
            if not text:
                logger.warning("Empty text provided for entity extraction")
                return {
                    "domain": "unknown",
                    "entities": [],
                    "metadata": {
                        "text_length": 0,
                        "entity_count": 0,
                        "analysis_method": "fallback"
                    }
                }

            analysis = self.analyze_context(text)

            # Check if analysis has the required attributes
            if not hasattr(analysis, 'domain') or not hasattr(analysis, 'entities'):
                logger.error("Analysis object is missing required attributes")
                return {
                    "domain": "unknown",
                    "entities": [],
                    "metadata": {
                        "text_length": len(text),
                        "entity_count": 0,
                        "analysis_method": "fallback"
                    }
                }

            return {
                "domain": analysis.domain,
                "entities": [entity.model_dump() for entity in analysis.entities],
                "metadata": analysis.metadata
            }
        except AttributeError as e:
            logger.error(f"Failed to extract entities due to missing attributes: {e}")
            # Return a safe fallback
            return {
                "domain": "unknown",
                "entities": [],
                "metadata": {
                    "text_length": len(text),
                    "entity_count": 0,
                    "analysis_method": "fallback"
                }
            }
        except Exception as e:
            logger.error(f"Unexpected error in entity extraction: {e}")
            return {
                "domain": "unknown",
                "entities": [],
                "metadata": {
                    "text_length": len(text),
                    "entity_count": 0,
                    "analysis_method": "fallback"
                }
            }


# Create a global instance for easy access

contextualiza_agent = ContextualizaAgent()
