


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
uvicorn src.api.main:app --reload
```

### Running Tests

```bash
pytest tests/
```

### Linting

```bash
flake8 src/ --max-line-length=88 --ignore=E501,W503
```

## Development

Follow the conventions in [conventions.md](conventions.md) and the workflow in [workflow.md](workflow.md).

## Documentation

- [Vision](vision.md) - Technical vision and architecture
- [Conventions](conventions.md) - Coding conventions
- [Task List](tasklist.md) - Development plan and progress
- [Workflow](workflow.md) - Development workflow

## License

This project is licensed under the MIT License.


