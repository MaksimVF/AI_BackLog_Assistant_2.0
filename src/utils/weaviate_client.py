




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
        from weaviate.connect.base import ConnectionParams, ProtocolParams

        # Parse URL to extract host and port
        from urllib.parse import urlparse
        parsed_url = urlparse(config.WEAVIATE_URL)

        # Create connection parameters
        connection_params = ConnectionParams(
            http=ProtocolParams(
                host=parsed_url.hostname,
                port=parsed_url.port or (443 if parsed_url.scheme == 'https' else 80),
                secure=parsed_url.scheme == 'https'
            ),
            grpc=ProtocolParams(
                host=parsed_url.hostname,
                port=50051,  # Default gRPC port for Weaviate
                secure=False
            )
        )

        self.client = weaviate.WeaviateClient(
            connection_params=connection_params,
            additional_headers={
                "X-OpenAI-Api-Key": config.MISTRAL_API_KEY  # Using Mistral API key for Weaviate
            }
        )

    def create_schema(self):
        """Create Weaviate schema for task embeddings"""
        schema_config = {
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

        self.client.schema.create_class(schema_config)
        return True

    def add_task_embedding(self, task_id: str, input_data: str, classification: str, recommendation: str, vector: list):
        """Add a task embedding to Weaviate"""
        data_object = {
            "task_id": task_id,
            "input_data": input_data,
            "classification": classification,
            "recommendation": recommendation
        }

        self.client.data.insert(
            class_name="Task",
            properties=data_object,
            vector=vector
        )
        return True

    def search_similar_tasks(self, query_vector: list, limit: int = 5):
        """Search for similar tasks using vector search"""
        result = self.client.graphql_query(
            """
            {
              Get {
                Task(
                  nearVector: {
                    vector: %s
                  },
                  limit: %s
                ) {
                  task_id
                  input_data
                  classification
                  recommendation
                }
              }
            }
            """ % (query_vector, limit)
        )

        return result["data"]["Get"]["Task"]

    def get_task_by_id(self, task_id: str):
        """Get a task by ID from Weaviate"""
        result = self.client.graphql_query(
            """
            {
              Get {
                Task(
                  where: {
                    path: ["task_id"]
                    operator: Equal
                    valueString: "%s"
                  }
                ) {
                  task_id
                  input_data
                  classification
                  recommendation
                }
              }
            }
            """ % task_id
        )

        if result["data"]["Get"]["Task"]:
            return result["data"]["Get"]["Task"][0]
        return None

# Create a global Weaviate client instance (lazy initialization)
weaviate_client = None

def get_weaviate_client():
    """Get the Weaviate client instance with lazy initialization"""
    global weaviate_client
    if weaviate_client is None:
        weaviate_client = WeaviateClient()
    return weaviate_client
