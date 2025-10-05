
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env.dev')








class Config:
    # Database
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'devuser')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'devpass')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'ai_backlog')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

    # Redis
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')

    # Weaviate
    WEAVIATE_HOST = os.getenv('WEAVIATE_HOST', 'localhost')
    WEAVIATE_PORT = os.getenv('WEAVIATE_PORT', '8080')

    # S3
    S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
    S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
    S3_BUCKET = os.getenv('S3_BUCKET', 'ai-backlog-files')
    S3_ENDPOINT = os.getenv('S3_ENDPOINT', 'https://s3.timeweb.cloud')

    # Telegram
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

    # Mistral API
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
    MISTRAL_API_URL = os.getenv('MISTRAL_API_URL', 'https://api.mistral.ai/v1')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def WEAVIATE_URL(self):
        return f"http://{self.WEAVIATE_HOST}:{self.WEAVIATE_PORT}"
