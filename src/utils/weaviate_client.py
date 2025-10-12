




"""
Weaviate Client for AI Backlog Assistant

This module provides Weaviate vector database client functionality.
"""

import weaviate
from src.config import Config

config = Config()

class WeaviateClient:
    """Weaviate client for vector storage operations"""

    def __init__(self):
        """Initialize the Weaviate client"""
        self.client = weaviate.Client(
            url=config.WEAVIATE_URL,
            additional_headers={
                "X-OpenAI-Api-Key": config.MISTRAL_API_KEY  # Using Mistral API key for Weaviate
            }
        )

    def create_schema(self):
        """Create Weaviate schema for task embeddings"""
        schema = {
            "classes": [
                {
                    "class": "Task",
                    "description": "AI Backlog Task",
                    "properties": [
                        {
                            "name": "task_id",
                            "dataType": ["string"],
                            "description": "Unique task ID"
                        },
                        {
                            "name": "input_data",
                            "dataType": ["text"],
                            "description": "Task input data"
                        },
                        {
                            "name": "classification",
                            "dataType": ["string"],
                            "description": "Task classification (idea/bug/feedback)"
                        },
                        {
                            "name": "recommendation",
                            "dataType": ["text"],
                            "description": "AI recommendation"
                        }
                    ]
                }
            ]
        }

        self.client.schema.create(schema)
        return True

    def add_task_embedding(self, task_id: str, input_data: str, classification: str, recommendation: str, vector: list):
        """Add a task embedding to Weaviate"""
        data_object = {
            "task_id": task_id,
            "input_data": input_data,
            "classification": classification,
            "recommendation": recommendation
        }

        self.client.data_object.create(
            data_object=data_object,
            class_name="Task",
            vector=vector
        )
        return True

    def search_similar_tasks(self, query_vector: list, limit: int = 5):
        """Search for similar tasks using vector search"""
        result = self.client.query.get(
            "Task",
            ["task_id", "input_data", "classification", "recommendation"]
        ).with_near_vector({
            "vector": query_vector
        }).with_limit(limit).do()

        return result["data"]["Get"]["Task"]

    def get_task_by_id(self, task_id: str):
        """Get a task by ID from Weaviate"""
        result = self.client.query.get(
            "Task",
            ["task_id", "input_data", "classification", "recommendation"]
        ).with_where({
            "path": ["task_id"],
            "operator": "Equal",
            "valueString": task_id
        }).do()

        if result["data"]["Get"]["Task"]:
            return result["data"]["Get"]["Task"][0]
        return None

# Create a global Weaviate client instance
weaviate_client = WeaviateClient()
