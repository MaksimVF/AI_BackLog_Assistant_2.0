
# AI Backlog Assistant: Technical Vision

## Technologies

The project uses a minimal, cost-effective tech stack to support the MVP, prioritizing simplicity, rapid development, and accessibility in Russia, per the KISS principle.

- **Language**: Python 3.11 — simple, widely supported, compatible with all required libraries.
- **Backend**: FastAPI — lightweight, fast, and async-friendly for API development.
- **LLM**:
  - Mistral (via API) for primary language model tasks, leveraging free token quotas and Russia accessibility.
- **Storage**:
  - PostgreSQL with SQLAlchemy (async) for metadata and logs — simple relational database.
  - Weaviate for vector search and task context storage — minimal configuration, no complex indexing.
  - S3 (Timeweb Object Storage) for raw files (audio, video, PDF) to support multimodality and future monetization.
- **Queue**: Redis — lightweight, reliable for async task triggering and batch processing.
- **TTS**: Yandex SpeechKit — cost-effective, Russia-friendly for audio output; no additional providers for MVP.
- **Multimodality**:
  - Text/PDF: pdfplumber — simple parser for documents.
  - Audio: Whisper (open-source, local) for Automatic Speech Recognition (ASR).
  - Images: Tesseract OCR — free, minimal setup for text extraction.
- **Integration**: Telegram (aiogram) — primary user interface for MVP; no Slack/Jira to keep it simple.
- **CI/CD**: GitHub Actions — minimal pipeline for automated testing and deployment.
- **Agent Framework**: LangGraph — for stateful workflows and agent coordination, replacing CrewAI to handle complex flows (e.g., parallel analysis in Level 3).

This stack ensures low-cost, rapid iteration, and easy deployment while supporting core functionality (multimodal input, prioritization, recommendations).

## Development Principles

The development process follows the KISS principle to ensure rapid iteration, minimal technical debt, and flexibility for future enhancements.

- **Simplicity and Iterativity**: Build in small, incremental steps, adding one key feature at a time (e.g., Input Agent, then Trigger Agent). Avoid overcomplicating frameworks like LangGraph for MVP.
- **Clean Code**:
  - Adhere to PEP 8 for readability.
  - Use flake8 for linting to enforce code consistency.
  - Write modular code: each agent/module in a separate file with a clear interface (e.g., `agents/level1/input_agent.py`).
- **Testing**: Write minimal unit tests (pytest) for each component as it is developed (e.g., agent → test, level → test). Target ~50% coverage for MVP to balance speed and reliability.
- **Versioning**: Use Git with `main` branch for stable code and `dev` for experiments. Use pull requests (PRs) for major changes, with lightweight review process.
- **Documentation**: Maintain a README with project structure, setup, and API details. Use docstrings for public functions/classes (e.g., `TriggerAgent.evaluate()`).
- **Error Handling**: Log errors to stderr and PostgreSQL for debugging; no complex monitoring tools (e.g., Sentry) for MVP.
- **MVP Focus**: Prioritize Level 1 (Input, Preprocessing) and Telegram bot for initial validation, with Levels 2–4 implemented as working components to support full workflow.

These principles ensure a lean development process, enabling quick validation of the project idea with minimal overhead.

## Project Structure

The project structure is modular, aligned with the 4-level architecture, ensuring clarity and scalability.

```plaintext
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
├── README.md                 # Project structure, setup, and API details
└── requirements.txt          # Dependencies
```

- **Naming**: Files follow the pattern `agent_name.py` (e.g., `input_agent.py`, `risk_assessment.py`) for clarity.
- **Level Separation**: Each level has dedicated agents, reflecting the 4-level workflow.
- **Extensibility**: Structure supports adding new agents or levels without refactoring.
- **Tests**: Stored in `tests/` for simplicity and CI/CD integration.
- **Logs**: Stored in `logs/` for local debugging and version comparison.
- **Documentation**: README covers setup, structure, and basic usage; docstrings for public methods.

This structure minimizes complexity, supports rapid development, and aligns with the KISS principle while enabling future expansion.

## Project Architecture

The architecture is a modular monolith, designed for simplicity in MVP while preparing for future microservices, adhering to KISS with minimal complexity.

- **Modular Monolith**:
  - Single FastAPI application with clear module separation (agents, api, utils, orchestrator).
  - Modules designed with clean interfaces (e.g., `InputAgent.process() → Dict`) for easy splitting into microservices later.
- **Data Flow**:
  - Input: Telegram (aiogram) → Level 1 (Input Agent → Modality Detector → Preprocessing) → Level 2 (Reflection → Semantic Block Classifier → Contextualiza) → Level 3 (Risk Assessment, Resource Availability, Impact Potential, Confidence & Urgency) → Level 4 (Aggregator → Visualization → Summary) → response (Telegram/TTS).
  - Levels 1–2 are synchronous for speed (<1s latency), Level 3 uses parallel LangGraph nodes, Level 4 generates output.
- **Agents (LangGraph)**:
  - **Level 1**:
    - **Input Agent**: Parses text, PDF (pdfplumber), audio (Whisper), images (Tesseract).
    - **Modality Detector**: Identifies input type (text/audio/image).
    - **Preprocessing**: Normalizes data (OCR, ASR).
  - **Level 2**:
    - **Reflection Agent**: Interprets task type (idea/bug/feedback).
    - **Semantic Block Classifier**: Segments text into blocks (headers, tables).
    - **Contextualiza Agent**: Extracts entities, determines domain (e.g., IT/marketing).
  - **Level 3**:
    - **Risk Assessment**: Evaluates risks (e.g., RICE/Kano).
    - **Resource Availability**: Assesses resource needs.
    - **Impact Potential**: Measures potential impact.
    - **Confidence & Urgency**: Scores confidence and urgency.
  - **Level 4**:
    - **Aggregator Agent**: Combines Level 3 outputs.
    - **Visualization Agent**: Generates charts (plotly).
    - **Summary Agent**: Provides recommendations (implement/delay).
  - **SuperAdmin Agent**: Logs errors to PostgreSQL and provides prompt sanitization.
- **Orchestrator**: LangGraph-based workflow managing 4-level chain with parallel execution in Level 3.
- **API**: Minimal FastAPI endpoints:
  - `/tasks` (POST: add task).
  - `/triggers` (GET: check triggers, for bot integration).
  - Accessible via Telegram, with API as a foundation for future integrations.
- **LLM**: Mistral API for classification, entity extraction, and assessment across levels.
- **Error Handling**: Log errors to stderr and PostgreSQL; single retry for Mistral API failures.
- **Diagram**:
  ```
  [Telegram] → [Level 1: Input → Modality → Preprocessing] → [Level 2: Reflection → Semantic → Contextualiza] → [Level 3: Risk, Resource, Impact, Confidence] → [Level 4: Aggregator → Visualization → Summary] → [Response to Telegram]
      ↓ (TTS)    ↓ (Mistral API)       ↓ (Mistral API)       ↓ (Parallel LangGraph)    ↓ (plotly/TTS)    ↓ (store/output)
  [Redis/Weaviate/PostgreSQL]
  ```

This architecture ensures rapid MVP development, supports parallel analysis in Level 3, and provides actionable outputs in Level 4, with extensibility for future microservices.

## Data Model

The data model supports all 4 levels, with extensibility for future enhancements, adhering to KISS while enabling monetization.

- **Storages**:
  - **PostgreSQL**: Relational database for task metadata and logs (SQLAlchemy async).
  - **Weaviate**: Vector database for task text and similarity search.
  - **S3**: Timeweb Object Storage for raw files (audio, video, PDF).
- **PostgreSQL Schema**:
  - **Table `tasks`**:
    ```sql
    CREATE TABLE tasks (
        task_id SERIAL PRIMARY KEY,
        user_id VARCHAR(50), -- Telegram ID
        input_text TEXT, -- Parsed text
        input_type VARCHAR(20), -- idea/bug/feedback
        ice_score FLOAT, -- Initial priority
        risk_score FLOAT, -- From Level 3
        resource_needs JSONB, -- From Level 3
        impact_score FLOAT, -- From Level 3
        confidence_score FLOAT, -- From Level 3
        urgency_score FLOAT, -- From Level 3
        recommendation TEXT, -- From Level 4
        file_path VARCHAR(255), -- S3 path
        metadata JSONB, -- Flexible extensions
        created_at TIMESTAMP DEFAULT NOW(),
        status VARCHAR(20) DEFAULT 'pending' -- pending/processed
    );
    ```
  - **Table `logs`**:
    ```sql
    CREATE TABLE logs (
        log_id SERIAL PRIMARY KEY,
        task_id INT REFERENCES tasks(task_id),
        agent VARCHAR(50), -- e.g., risk_assessment
        message TEXT, -- Error or event
        created_at TIMESTAMP DEFAULT NOW()
    );
    ```
  - **Table `triggers`**:
    ```sql
    CREATE TABLE triggers (
        trigger_id SERIAL PRIMARY KEY,
        task_id INT REFERENCES tasks(task_id),
        reason VARCHAR(50), -- e.g., high_urgency
        created_at TIMESTAMP DEFAULT NOW()
    );
    ```
- **Weaviate Schema**:
  - Collection `Tasks`:
    ```json
    {
      "class": "Task",
      "properties": {
        "task_id": "int",
        "input_text": "string",
        "input_type": "string",
        "metadata": "object",
        "vector": "float[]"
      }
    }
    ```
  - Used for: Similarity search, context storage.
- **S3 Storage**:
  - Path format: `s3://bucket/user_id/task_id/filename`.
- **Data Flow**:
  - **Level 1**: Saves `input_text`, `file_path`, `user_id`, `metadata`.
  - **Level 2**: Updates `input_type`, adds entity data to `metadata`.
  - **Level 3**: Adds `risk_score`, `resource_needs`, `impact_score`, `confidence_score`, `urgency_score`.
  - **Level 4**: Updates `recommendation`.
- **Extensibility**: `metadata` and new fields support Levels 2–4 data.

This model ensures comprehensive storage for all levels, supporting multimodality and monetization.

## LLM Integration

LLM integration supports all 4 levels with tailored prompts and error handling.

- **LLM Usage**: Mistral API for classification, entity extraction, and assessment.
- **Tasks**:
  - **Level 1**: Basic parsing (no LLM).
  - **Level 2**:
    - Reflection: `Classify as "idea", "bug", or "feedback": {input_text} → {type}`.
    - Contextualiza: `Extract entities and domain from: {input_text} → {entities, domain}`.
  - **Level 3**:
    - Risk: `Assess risk (0-10) for: {input_text} → {score}`.
    - Resource: `Estimate resources for: {input_text} → {needs}`.
    - Impact: `Measure impact (0-10) for: {input_text} → {score}`.
    - Confidence/Urgency: `Score confidence and urgency (0-10) for: {input_text} → {confidence, urgency}`.
  - **Level 4**:
    - Summary: `Recommend action (implement/delay) based on: {analyzed_data} → {recommendation}`.
- **Prompts**: Stored in `src/utils/prompts.py`, short and specific.
- **Fallback Mechanism**: Default values (e.g., `risk_score=5`) on Mistral failure.
- **Caching**: No caching for MVP; Redis for future optimization.
- **Error Handling**: Single retry (5s timeout), log to PostgreSQL.
- **Extensibility**: Prompts updatable for complex tasks.

This ensures cost-effective LLM usage across all levels.

## LLM Monitoring

Minimal monitoring supports debugging and reliability.

- **SuperAdmin Agent**: Monitors LLM (Mistral API), sanitizes prompts.
- **Monitoring**:
  - **Errors**: Log failures (rate limit, timeout).
  - **Metrics**: Call count, latency, status.
  - **Quality**: Validate outputs (e.g., scores 0–10).
- **Prompt Sanitization**: Regex check for injections.
- **Logging**: To PostgreSQL `logs` table.
- **Extensibility**: Supports future analytics.

## Usage Scenarios

Scenarios cover all 4 levels via Telegram and API.

- **Primary Scenarios (Telegram Bot)**:
  1. **Add Task**: User sends input → Level 1–4 process → "Task #{task_id} classified as {input_type}, recommended: {recommendation}" (text/TTS).
  2. **Check Task Status**: `/status {task_id}` → status + scores.
  3. **List Tasks**: `/list` → last 5 tasks with recommendations.
  4. **Access Archive**: `/archive {task_id}` → S3 link or text.
- **API Scenarios**:
  - **Add Task**: `POST /tasks` → `task_id`.
  - **Check Triggers**: `GET /triggers` → tasks with recommendations.
- **Monetization**: Freemium (50 tasks), Premium (S3 access).
- **Extensibility**: Supports advanced visualizations.

## Deployment

Simple deployment using Timeweb Cloud and Docker.

- **Platform**: Timeweb Cloud with Docker, managed PostgreSQL/Redis, S3.
- **Deployment**: Single FastAPI Docker container, Weaviate/Whisper/Tesseract in separate containers.
- **CI/CD**: GitHub Actions for linting, testing, and deployment.
- **Extensibility**: Prepared for microservices.

## Configuration Approach

Uses `.env` files with `python-dotenv` for dev/prod environments.

- **Parameters**: `TELEGRAM_TOKEN`, `MISTRAL_API_KEY`, etc.
- **Loading**: Via `src/config.py`.
- **Security**: Excluded from Git, stored in Secrets Manager.
- **Extensibility**: Supports future parameters.

## Logging Approach

Minimal error logging to PostgreSQL, stderr, and `logs/app.log`.

- **Events**: Errors from all agents and services.
- **Implementation**: Python `logging` with async PostgreSQL logging.
- **Extensibility**: Supports analytics.

## Testing Approach

Minimal unit tests with ~50% coverage using `pytest`.

- **Components**: All agents, API, orchestrator.
- **Mocks**: For external services.
- **CI/CD**: Integrated with GitHub Actions.
- **Extensibility**: Supports Levels 2–4 tests.

## Development Roadmap

MVP in 6–8 weeks, accelerated to 4–6 weeks.

- **Iterations**:
  1. **Weeks 1–2**: Infrastructure, Level 1 (Input, Modality, Preprocessing).
  2. **Weeks 3–4**: Level 2 (Reflection, Semantic, Contextualiza), Telegram bot.
  3. **Weeks 5–6**: Level 3 (Risk, Resource, Impact, Confidence), LangGraph orchestration.
  4. **Weeks 7–8**: Level 4 (Aggregator, Visualization, Summary), API, deployment.
- **Post-MVP**: Monetization, Ollama, scaling.
- **Resources**: One developer, minimal budget.
- **Extensibility**: Adjustable based on validation.

This roadmap ensures rapid MVP delivery with full 4-level functionality.

---

### Примечания к Изменениям
1. **Адаптация к 4 Уровням**:
   - Architecture, Data Model, and Usage Scenarios now reflect 4 levels as per your diagram.
   - Agents renamed to match (e.g., Input Agent → Level 1, Risk Assessment → Level 3).
2. **Переход на LangGraph**:
   - Replaced CrewAI with LangGraph in Technologies and Architecture for stateful, parallel workflows (e.g., Level 3).
   - Orchestrator updated to use LangGraph chains/nodes.
3. **Levels 3–4 как Рабочие Варианты**:
   - Level 3 agents (Risk, Resource, etc.) implemented with parallel LangGraph nodes.
   - Level 4 (Aggregator, Visualization, Summary) included with basic functionality (text/TTS for MVP, plotly for visualization).
   - Data Model extended with Level 3–4 fields (e.g., `risk_score`, `recommendation`).
   - Roadmap adjusted to include Levels 3–4 development within 6–8 weeks.
4. **Ускорение**:
   - Focused on parallel development of Levels 1–2 (4 weeks), with Levels 3–4 in subsequent iterations to manage complexity.

### Дополнительные Рекомендации
- **LangGraph Реализация**: Используй `langgraph.graph` для Level 3 параллелизма. Пример:
  ```python
  from langgraph.graph import Graph
  graph = Graph()
  graph.add_node("risk_assessment", RiskAssessment().run)
  graph.add_node("resource_availability", ResourceAvailability().run)
  graph.add_edge("risk_assessment", "aggregator")
  graph.add_edge("resource_availability", "aggregator")
  ```
- **Тестирование Levels 3–4**: Добавь интеграционные тесты для параллельных агентов и визуализации.
- **Ресурсы**: Учитывая полный охват Levels 3–4, рассмотри временное увеличение бюджета для Mistral API (или локальный Ollama для тестов).

Если нужны детали (e.g., код для LangGraph или тесты), дай знать!
