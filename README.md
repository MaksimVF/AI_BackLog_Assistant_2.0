


# AI Backlog Assistant

AI Backlog Assistant is a project for optimizing backlog management using AI. This project follows the KISS principle and is designed for rapid development and deployment.

## Project Structure

```
ai-backlog-assistant/
├── src/
│   ├── agents/               # All agents, grouped by levels
│   │   ├── level1/           # Input, Modality Detector, Preprocessing Agents
│   │   ├── level2/           # Reflection, Semantic Block Classifier, Contextualiza Agents
│   │   ├── level3/           # Risk Assessment, Resource Availability, Impact Potential, Confidence & Urgency Agents
│   │   ├── level4/           # Aggregator, Visualization, Summary Agents
│   │   └── superadmin/       # PromptSanitizer, monitoring (minimal for MVP)
│   ├── api/                  # FastAPI endpoints (tasks, triggers)
│   ├── utils/                # Shared utilities (pdfplumber, Whisper, Tesseract)
│   └── orchestrator/         # Orchestrator for coordinating agents (LangGraph-based)
├── tests/                    # Pytest tests for all components
├── logs/                     # Log files for local debugging
├── .github/workflows/        # GitHub Actions CI/CD workflows
├── README.md                 # Project structure, setup, and API details
├── requirements.txt           # Dependencies
├── docker-compose.yml         # Docker Compose for local development
├── .env.dev                   # Environment configuration (development)
└── src/config.py              # Configuration loader
```

## Setup

### Prerequisites

- Python 3.11
- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/MaksimVF/AI_BackLog_Assistant_2.0.git
   cd AI_BackLog_Assistant_2.0
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Copy `.env.dev` to `.env` and update the values as needed.

4. Start Docker services:
   ```bash
   docker-compose up -d
   ```

### Running the Application

```bash
# Run the main API (without webapp)
uvicorn src.api.main:app --reload

# OR run the combined API with webapp support
uvicorn src.api.main_with_webapp:app --reload
```

### Running Tests

```bash
pytest tests/
```

### Linting

```bash
flake8 src/ --max-line-length=88 --ignore=E501,W503
```

## Telegram Bot Setup

To use the Telegram bot functionality:

1. Create a new bot using BotFather in Telegram:
   - Open Telegram and search for "BotFather"
   - Use the command `/newbot` to create a new bot
   - Follow the instructions to set a name and username for your bot
   - After creation, BotFather will provide you with an API token

2. Get the API token from BotFather:
   - The token will look something like: `123456789:ABCDefGhIjKlMnOpQrStUvWxYz`
   - Keep this token secure and don't share it publicly

3. Set the token in your `.env` file:
   - Copy `.env.dev` to `.env` if it doesn't exist:
     ```bash
     cp .env.dev .env
     ```
   - Update the TELEGRAM_TOKEN value in your `.env` file:
     ```
     TELEGRAM_TOKEN=your_real_telegram_bot_token_here
     ```
   - Make sure the token is not "AIBLA" (which is a mock token)

4. Run the bot:
   ```bash
   python -m src.bot.telegram_bot
   ```

   Note: If you don't have a valid Telegram token, the bot will run in mock mode and won't connect to Telegram servers. If you're using the mock token "AIBLA", the bot will attempt to connect but will fail.

5. Test the bot:
   - After running the bot, open Telegram and search for your bot by username
   - Start a chat with your bot and try sending commands like `/start`, `/help`, etc.
   - If the bot doesn't respond, check the logs for any error messages

6. Troubleshooting:
   - If the bot doesn't respond, check the logs for messages about the token
   - Make sure you're using a real token, not "AIBLA" or "your_real_telegram_token_here"
   - Ensure your bot has the necessary permissions in Telegram
   - Check your network connection to Telegram servers

7. Common issues:
   - Using a mock token: The bot will try to connect but fail
   - No token set: The bot will run in mock mode and won't connect
   - Invalid token format: Make sure the token is in the format `123456789:ABCDefGhIjKlMnOpQrStUvWxYz`

8. Debugging tips:
   - Check the logs for any error messages
   - Look for warnings about the token being invalid or not set
   - Make sure you've followed all the steps to create a bot and get a token
   - If you're still having issues, try creating a new bot and getting a fresh token

9. Additional resources:
   - Telegram Bot API documentation: https://core.telegram.org/bots/api
   - BotFather commands: https://core.telegram.org/bots#botfather
   - Telegram Bot FAQ: https://core.telegram.org/bots/faq

10. Important notes:
    - The bot will not work with the mock token "AIBLA"
    - The bot will not work with the placeholder token "your_real_telegram_token_here"
    - You must use a real Telegram bot token to connect to Telegram servers
    - If you're having trouble, double-check your token and network connection

11. Example of a valid token:
    - A valid token looks like: `123456789:ABCDefGhIjKlMnOpQrStUvWxYz`
    - It should start with numbers, followed by a colon, and then a mix of letters and numbers
    - If your token doesn't look like this, it's probably invalid

12. Contact support:
    - If you're still having issues, contact the project maintainers
    - Provide details about your setup and any error messages you're seeing
    - Include information about your environment and configuration

13. Advanced configuration:
    - You can configure additional settings in the `.env` file
    - Check the `.env.dev` file for examples of other configuration options
    - Make sure to keep your `.env` file secure and don't share it publicly

14. Security considerations:
    - Never commit your `.env` file to version control
    - Add `.env` to your `.gitignore` file to prevent accidental commits
    - Use environment variables in production for better security

15. Deployment considerations:
    - For production deployments, use secure methods to store your Telegram token
    - Consider using secret management services for better security
    - Ensure your bot has proper rate limiting and error handling

16. Monitoring and maintenance:
    - Regularly check your bot's performance and logs
    - Update your bot's token if you need to regenerate it
    - Monitor Telegram API rate limits and adjust your bot's behavior accordingly

17. Performance optimization:
    - Consider implementing caching for frequent requests
    - Optimize your bot's response time for better user experience
    - Monitor resource usage and adjust as needed

18. Community and support:
    - Join our community forums for additional help
    - Check our GitHub issues page for common problems and solutions
    - Contribute to the project by reporting issues and suggesting improvements

19. Contributing:
    - We welcome contributions to improve the bot
    - Follow our contribution guidelines in CONTRIBUTING.md
    - Submit pull requests with your improvements

20. Feedback and suggestions:
    - Share your ideas for new features
    - Report bugs and issues you encounter
    - Help us improve the bot's functionality

21. Future development:
    - We're planning to add more features to the bot
    - Stay tuned for updates and new releases
    - Follow our roadmap for upcoming improvements

22. Documentation:
    - Check our wiki for more detailed documentation
    - Read our API reference for developers
    - Explore our examples and tutorials

## Development

Follow the conventions in [conventions.md](conventions.md) and the workflow in [workflow.md](workflow.md).

## Documentation

- [Vision](vision.md) - Technical vision and architecture
- [Conventions](conventions.md) - Coding conventions
- [Task List](tasklist.md) - Development plan and progress
- [Workflow](workflow.md) - Development workflow

## License

This project is licensed under the MIT License.


