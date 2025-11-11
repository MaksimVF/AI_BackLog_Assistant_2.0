



"""
Level 2 Duplicate Detector - Pure LangGraph Implementation

This module implements duplicate detection using pure LangGraph without depending on old agents.
"""

import logging
import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from src.db.connection import AsyncSessionLocal
from src.db.repository import TaskRepository
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)

class Level2DuplicateDetectorPure:
    """Detects duplicate messages using various similarity techniques in Level 2"""

    def __init__(self):
        """Initialize the Level 2 Duplicate Detector"""
        logger.info("Initializing Level 2 Duplicate Detector (Pure LangGraph)")

        # Initialize Weaviate client for semantic analysis
        try:
            from src.utils.weaviate_client import get_weaviate_client
            self.weaviate_client = get_weaviate_client()
            self.weaviate_available = True
        except Exception as e:
            logger.warning(f"Weaviate client not available: {e}")
            self.weaviate_client = None
            self.weaviate_available = False

    def preprocess_text(self, text: str) -> str:
        """Preprocess text for similarity comparison"""
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation and special characters
        text = re.sub(r'[^\w\s]', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def jaccard_similarity(self, str1: str, str2: str) -> float:
        """Calculate Jaccard similarity between two strings"""
        # Preprocess texts
        str1 = self.preprocess_text(str1)
        str2 = self.preprocess_text(str2)

        # Tokenize into words
        set1 = set(str1.split())
        set2 = set(str2.split())

        # Calculate Jaccard similarity
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))

        if union == 0:
            return 0.0

        return intersection / union

    def cosine_similarity_text(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two texts"""
        # Preprocess texts
        text1 = self.preprocess_text(text1)
        text2 = self.preprocess_text(text2)

        # Create vectorizer and transform texts
        vectorizer = CountVectorizer().fit_transform([text1, text2])
        vectors = vectorizer.toarray()

        # Calculate cosine similarity
        return cosine_similarity(vectors)[0, 1]

    def generate_mock_embedding(self, text: str) -> List[float]:
        """Generate a mock embedding for semantic analysis (placeholder for LLM integration)"""
        # This is a simple mock embedding - in production we would use an LLM API
        # to generate proper embeddings
        import hashlib

        # Create a simple hash-based embedding
        hash_obj = hashlib.md5(text.encode())
        hash_hex = hash_obj.hexdigest()

        # Convert hash to a simple vector representation
        # In a real implementation, this would be a proper LLM embedding
        vector = [ord(c) / 255.0 for c in hash_hex[:30]]  # Simple 30-dim vector

        # Extend to a reasonable size (e.g., 156 dim like some LLM embeddings)
        while len(vector) < 156:
            vector.extend([ord(c) / 255.0 for c in hash_hex[:30]])
        return vector[:156]

    def semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity using embeddings"""
        # Generate embeddings for both texts
        embedding1 = self.generate_mock_embedding(text1)
        embedding2 = self.generate_mock_embedding(text2)

        # Calculate cosine similarity between embeddings
        dot_product = np.dot(embedding1, embedding2)
        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def weaviate_similarity_search(self, text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search for similar tasks using Weaviate vector search"""
        if not self.weaviate_available:
            return []

        try:
            # Generate embedding for the input text
            vector = self.generate_mock_embedding(text)

            # Search for similar tasks in Weaviate
            # Use a simple mock search since we don't have a real Weaviate client
            # In a real implementation, this would use the Weaviate client
            return []

        except Exception as e:
            logger.error(f"Error in Weaviate similarity search: {e}")
            return []

    async def check_duplicate(self, message_text: str, user_id: str, time_window_minutes: int = 60,
                             similarity_threshold: float = 0.6) -> Dict[str, Any]:
        """
        Check if a message is a duplicate within a time window using various similarity techniques

        Args:
            message_text: The text message to check
            user_id: The user ID
            time_window_minutes: Time window to check for duplicates
            similarity_threshold: Threshold for considering messages as duplicates (0-1)

        Returns:
            Dict with duplicate status and analysis
        """
        result = {
            "is_duplicate": False,
            "duplicate_count": 0,
            "last_occurrence": None,
            "time_since_last": None,
            "analysis": "No duplicates found",
            "similarity_scores": [],
            "most_similar_task": None,
            "highest_similarity": 0.0
        }

        try:
            # Calculate time window
            time_threshold = datetime.utcnow() - timedelta(minutes=time_window_minutes)

            # Get recent tasks for this user
            async with AsyncSessionLocal() as db:
                try:
                    recent_tasks = await TaskRepository.get_recent_tasks_by_user(
                        db, user_id, time_threshold
                    )
                    logger.info(f"Found {len(recent_tasks)} recent tasks for user {user_id}")
                except Exception as e:
                    logger.error(f"Error getting recent tasks: {e}")
                    recent_tasks = []

                if not recent_tasks:
                    logger.info(f"No recent tasks found for user {user_id}")
                    return result

                # Check for exact duplicates and calculate similarities
                exact_duplicates = []
                similarity_scores = []

                for task in recent_tasks:
                    # Check for exact match first
                    if task.input_data == message_text:
                        exact_duplicates.append(task)
                        result["is_duplicate"] = True
                        result["original_task_id"] = task.task_id
                        result["analysis"] = f"Exact duplicate found: task_{task.task_id}"
                        result["most_similar_task"] = task.input_data
                        result["highest_similarity"] = 1.0
                        result["last_occurrence"] = task.created_at
                        result["time_since_last"] = (datetime.utcnow() - task.created_at).total_seconds() / 60
                        break  # Stop checking once we find an exact duplicate

                    # Calculate similarity scores
                    jaccard = self.jaccard_similarity(task.input_data, message_text)
                    cosine = self.cosine_similarity_text(task.input_data, message_text)
                    semantic = self.semantic_similarity(task.input_data, message_text)

                    # Calculate weighted average similarity
                    # Give more weight to semantic similarity
                    avg_similarity = (jaccard * 0.2 + cosine * 0.3 + semantic * 0.5)

                    similarity_scores.append({
                        "task_id": task.task_id,
                        "task_text": task.input_data,
                        "jaccard": jaccard,
                        "cosine": cosine,
                        "semantic": semantic,
                        "avg_similarity": avg_similarity,
                        "created_at": task.created_at
                    })

                # If we found exact duplicates, return immediately
                if exact_duplicates:
                    return result

                # Sort by average similarity (highest first)
                similarity_scores.sort(key=lambda x: x["avg_similarity"], reverse=True)

                # Check if we have any similar tasks above the threshold
                if similarity_scores and similarity_scores[0]["avg_similarity"] >= similarity_threshold:
                    most_similar = similarity_scores[0]
                    result["is_duplicate"] = True
                    result["most_similar_task"] = most_similar["task_text"]
                    result["highest_similarity"] = most_similar["avg_similarity"]
                    result["last_occurrence"] = most_similar["created_at"]
                    result["time_since_last"] = (datetime.utcnow() - most_similar["created_at"]).total_seconds() / 60  # in minutes

                    # Generate analysis
                    result["analysis"] = (f"Found similar task: '{most_similar['task_text']}' "
                                         f"(similarity: {most_similar['avg_similarity']:.2f})")

                    # Add similarity details
                    result["similarity_scores"] = similarity_scores[:3]  # Top 3 most similar

                    # Add pattern analysis based on time
                    if result["time_since_last"] and result["time_since_last"] < 10:
                        result["analysis"] += ". User is repeating similar tasks frequently."

                # Also check Weaviate for semantic similarities (if available)
                if self.weaviate_available:
                    weaviate_results = self.weaviate_similarity_search(message_text, top_k=3)
                    if weaviate_results:
                        # Convert Weaviate distance to similarity (lower distance = higher similarity)
                        for weaviate_result in weaviate_results:
                            # Distance ranges from 0 to 2 (0 = identical, 2 = completely different)
                            similarity = max(0, 1 - weaviate_result["similarity"] / 2)  # Convert to 0-1 range

                            if similarity >= similarity_threshold:
                                result["is_duplicate"] = True
                                result["weaviate_results"] = weaviate_results
                                result["analysis"] += f"\nWeaviate found similar task: '{weaviate_result['input_data']}' (similarity: {similarity:.2f})"
                                break

                # Handle exact duplicates
                if exact_duplicates:
                    result["is_duplicate"] = True
                    result["duplicate_count"] = len(exact_duplicates)

                    # Get most recent exact duplicate
                    most_recent = max(exact_duplicates, key=lambda x: x.created_at)
                    result["last_occurrence"] = most_recent.created_at
                    result["time_since_last"] = (datetime.utcnow() - most_recent.created_at).total_seconds() / 60  # in minutes

                    # Generate analysis for exact duplicates
                    if result["duplicate_count"] == 1:
                        result["analysis"] = "This message was sent once before (exact match)"
                    else:
                        result["analysis"] = f"This message has been sent {result['duplicate_count']} times before (exact matches)"

                    # Add pattern analysis for exact duplicates
                    if result["time_since_last"] and result["time_since_last"] < 10:
                        result["analysis"] += ". User is repeating the exact message frequently."

        except Exception as e:
            logger.error(f"Error checking for duplicates: {e}")
            result["error"] = str(e)

        return result

# Create a global instance for easy access
level2_duplicate_detector_pure = Level2DuplicateDetectorPure()

