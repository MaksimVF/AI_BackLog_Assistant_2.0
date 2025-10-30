

"""
Advanced Task Classifier Module

This module provides enhanced task classification using:
- Advanced keyword analysis
- Contextual understanding
- Machine learning integration (when available)
- Better confidence scoring
"""

import logging
import re
from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel

# Import other agents for context
from src.agents.level2.contextualiza_agent import contextualiza_agent

# Configure logging
logger = logging.getLogger(__name__)

class ClassificationResult(BaseModel):
    """Data model for classification results"""
    task_type: str  # idea, bug, feedback, question, request
    confidence: float  # confidence score 0-1
    sub_category: Optional[str] = None  # more specific classification
    metadata: Optional[Dict[str, Any]] = None

class AdvancedTaskClassifier:
    """Agent for advanced task classification"""

    def __init__(self):
        """Initialize the Advanced Task Classifier"""
        logger.info("Initializing Advanced Task Classifier")

        # Predefined patterns and keywords
        self.keyword_patterns = {
            "bug": {
                "primary": ["bug", "error", "issue", "problem", "defect", "failure", "crash", "malfunction"],
                "secondary": ["fix", "repair", "resolve", "debug", "troubleshoot"],
                "context": ["not working", "broken", "doesn't work", "failing", "incorrect"]
            },
            "idea": {
                "primary": ["idea", "feature", "proposal", "improvement", "enhancement"],
                "secondary": ["new", "add", "implement", "create", "develop", "build"],
                "context": ["should", "could", "would be nice", "might be good", "potential"]
            },
            "feedback": {
                "primary": ["feedback", "comment", "opinion", "review", "complaint", "praise", "criticism"],
                "secondary": ["like", "dislike", "love", "hate", "think", "believe", "feel", "appreciate", "enjoy"],
                "context": ["good job", "well done", "poor", "bad", "excellent", "terrible", "awesome", "fantastic"]
            },
            "question": {
                "primary": ["question", "query", "ask", "inquiry", "request information"],
                "secondary": ["how", "what", "when", "where", "why", "who"],
                "context": ["can you", "could you", "please explain", "need to know", "want to understand"]
            },
            "request": {
                "primary": ["request", "need", "require", "ask for", "demand"],
                "secondary": ["please", "could you", "can you", "would you"],
                "context": ["urgent", "important", "priority", "ASAP", "immediate"]
            }
        }

        # Domain-specific keywords
        self.domain_keywords = {
            "technical": ["code", "software", "system", "database", "API", "server", "network", "security"],
            "business": ["revenue", "profit", "market", "customer", "sales", "growth", "strategy"],
            "design": ["UI", "UX", "interface", "layout", "design", "aesthetic", "visual"],
            "content": ["text", "article", "post", "content", "writing", "editing", "copy"]
        }

    def _score_keywords(self, text: str, keyword_list: List[str], weight: float = 1.0) -> float:
        """Score text based on keyword matches"""
        score = 0.0
        text_lower = text.lower()

        for keyword in keyword_list:
            if keyword in text_lower:
                score += weight

        return score

    def _analyze_sentiment(self, text: str) -> Tuple[str, float]:
        """Simple sentiment analysis"""
        positive_words = ["good", "great", "excellent", "awesome", "fantastic", "perfect", "love"]
        negative_words = ["bad", "terrible", "awful", "poor", "hate", "worst", "broken"]

        pos_score = self._score_keywords(text, positive_words, 0.5)
        neg_score = self._score_keywords(text, negative_words, 0.5)

        if pos_score > neg_score:
            return "positive", pos_score - neg_score
        elif neg_score > pos_score:
            return "negative", neg_score - pos_score
        else:
            return "neutral", 0.0

    def _detect_domain(self, text: str) -> str:
        """Detect the domain of the task"""
        domain_scores = {domain: 0.0 for domain in self.domain_keywords}

        for domain, keywords in self.domain_keywords.items():
            domain_scores[domain] += self._score_keywords(text, keywords, 0.5)

        # Get domain with highest score
        best_domain = max(domain_scores.items(), key=lambda x: x[1])[0]
        best_score = domain_scores[best_domain]

        # Only return domain if score is significant
        return best_domain if best_score > 0.5 else "general"

    def _classify_with_keywords(self, text: str) -> Dict[str, float]:
        """Classify using advanced keyword analysis"""
        scores = {task_type: 0.0 for task_type in self.keyword_patterns}

        text_lower = text.lower()

        # Check for sentiment to boost feedback detection
        sentiment, sentiment_score = self._analyze_sentiment(text)

        for task_type, patterns in self.keyword_patterns.items():
            # Primary keywords (high weight)
            scores[task_type] += self._score_keywords(text_lower, patterns["primary"], 1.5)

            # Secondary keywords (medium weight)
            scores[task_type] += self._score_keywords(text_lower, patterns["secondary"], 1.0)

            # Context patterns (low weight)
            scores[task_type] += self._score_keywords(text_lower, patterns["context"], 0.5)

        # Boost feedback score if sentiment is detected
        if sentiment != "neutral":
            scores["feedback"] += abs(sentiment_score) * 1.0

        return scores

    def _calculate_confidence(self, scores: Dict[str, float]) -> float:
        """Calculate confidence based on score distribution"""
        sorted_scores = sorted(scores.values(), reverse=True)

        if len(sorted_scores) < 2:
            return 0.7  # default confidence

        # Calculate confidence based on the gap between top scores
        top_score = sorted_scores[0]
        second_score = sorted_scores[1]

        if top_score == 0:
            return 0.3  # low confidence if no matches

        score_difference = top_score - second_score

        # Map score difference to confidence (0-1)
        if score_difference > 3:
            return 0.95
        elif score_difference > 2:
            return 0.85
        elif score_difference > 1:
            return 0.75
        else:
            return 0.60

    def _determine_sub_category(self, text: str, main_category: str) -> str:
        """Determine more specific sub-category"""
        if main_category == "bug":
            if "security" in text.lower():
                return "security_bug"
            elif "performance" in text.lower():
                return "performance_bug"
            elif "UI" in text.lower() or "interface" in text.lower():
                return "ui_bug"
            else:
                return "functional_bug"

        elif main_category == "idea":
            if "feature" in text.lower():
                return "new_feature"
            elif "improvement" in text.lower() or "enhancement" in text.lower():
                return "improvement"
            elif "redesign" in text.lower() or "rework" in text.lower():
                return "redesign"
            else:
                return "general_idea"

        elif main_category == "feedback":
            sentiment, _ = self._analyze_sentiment(text)
            return f"{sentiment}_feedback"

        return "general"

    def classify_task(self, text: str) -> ClassificationResult:
        """
        Classify task using advanced analysis

        Args:
            text: Input text to classify

        Returns:
            Classification result with confidence and sub-category
        """
        # Get keyword-based scores
        scores = self._classify_with_keywords(text)

        # Determine best classification
        best_type = max(scores.items(), key=lambda x: x[1])[0]
        confidence = self._calculate_confidence(scores)

        # Get sub-category
        sub_category = self._determine_sub_category(text, best_type)

        # Get domain context
        domain = self._detect_domain(text)

        # Get sentiment for feedback
        if best_type == "feedback":
            sentiment, sentiment_score = self._analyze_sentiment(text)
        else:
            sentiment, sentiment_score = "neutral", 0.0

        return ClassificationResult(
            task_type=best_type,
            confidence=confidence,
            sub_category=sub_category,
            metadata={
                "scores": scores,
                "domain": domain,
                "sentiment": sentiment,
                "sentiment_score": sentiment_score,
                "classification_method": "advanced_keyword_analysis"
            }
        )

    def analyze_task(self, text: str) -> Dict[str, Any]:
        """
        Provide comprehensive task analysis

        Args:
            text: Input text to analyze

        Returns:
            Comprehensive analysis result
        """
        # Get classification
        classification = self.classify_task(text)

        # Get context analysis
        context = contextualiza_agent.analyze_context(text)

        return {
            "task_type": classification.task_type,
            "sub_category": classification.sub_category,
            "confidence": classification.confidence,
            "domain": context.domain,
            "entities": context.entities,
            "sentiment": classification.metadata["sentiment"],
            "metadata": {
                "classification": classification.metadata,
                "context": context.metadata
            }
        }

# Create a global instance for easy access
advanced_task_classifier = AdvancedTaskClassifier()

