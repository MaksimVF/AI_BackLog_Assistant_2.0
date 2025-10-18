
import os
from dotenv import load_dotenv

# Load environment variables
# First try to load .env, if it doesn't exist or is missing variables, load .env.dev
if os.path.exists('.env'):
    load_dotenv('.env')
    # Check if we have a valid Telegram token
    if not os.getenv('TELEGRAM_TOKEN') or os.getenv('TELEGRAM_TOKEN') == 'AIBLA' or os.getenv('TELEGRAM_TOKEN').startswith('your_'):
        # If token is invalid, try to load from .env.dev
        if os.path.exists('.env.dev'):
            load_dotenv('.env.dev')
else:
    # If .env doesn't exist, try to load from .env.dev
    if os.path.exists('.env.dev'):
        load_dotenv('.env.dev')

# Check if we have a valid Telegram token
telegram_token = os.getenv('TELEGRAM_TOKEN')
if not telegram_token:
    print("⚠️  WARNING: Telegram token is not set!")
    print("   Please set a valid Telegram token in your .env file")
    print("   You can get a token by creating a new bot with BotFather in Telegram")
elif telegram_token == 'AIBLA':
    print("⚠️  WARNING: Using mock Telegram token 'AIBLA'")
    print("   Please replace 'AIBLA' with your real Telegram bot token in .env file")
    print("   The bot will attempt to connect but will fail with this token")
elif telegram_token.startswith('your_'):
    print("⚠️  WARNING: Using placeholder Telegram token")
    print("   Please replace 'your_real_telegram_token_here' with your real Telegram bot token in .env file")
    print("   The bot will attempt to connect but will fail with this token")
else:
    print("✅ Telegram token is set correctly")








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
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', "AIBLA")  # Default to mock token if not set

    @property
    def telegram_api_key(self):
        return self.TELEGRAM_TOKEN

    # Mistral API
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY')
    MISTRAL_API_URL = os.getenv('MISTRAL_API_URL', 'https://api.mistral.ai/v1')

    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

    @property
    def POSTGRES_URL(self):
        # Use SQLite for testing if no PostgreSQL credentials are provided
        if self.POSTGRES_USER == 'devuser' and self.POSTGRES_PASSWORD == 'devpass':
            return "sqlite+aiosqlite:///test_ai_backlog.db"
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def WEAVIATE_URL(self):
        return f"http://{self.WEAVIATE_HOST}:{self.WEAVIATE_PORT}"
