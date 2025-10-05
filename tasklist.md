

# Task List (@tasklist.md)

## Progress Report
| Iteration | Task Description         | Status   | Notes                     | Icon    |
|-----------|--------------------------|----------|---------------------------|---------|
| 1         | Setup Infrastructure     | ✅ Done   | Basic setup completed     |        |
| 2         | Level 1: Input Processing|   In Progress | Testing Input Agent       |        |
| 3         | Level 2: Semantic Analysis | ☐ Not Started | -                        |        |
| 4         | Level 3: Analysis        | ☐ Not Started | -                        |        |
| 5         | Level 4: Recommendations | ☐ Not Started | -                        |        |

*Last Updated: 02:31 AM CDT, Sunday, October 05, 2025*

---

## Development Plan

### Iteration 1: Setup Infrastructure (Weeks 1–2)
- [x] Set up project structure and `requirements.txt` per [@vision.md](#).
- [x] Configure `.env.dev` and `src/config.py` for environment loading.
- [x] Initialize Docker Compose with PostgreSQL, Redis, Weaviate (local testing).
- [x] Setup CI/CD with GitHub Actions (flake8, pytest).
- **Test**: Verify Docker setup and CI/CD pipeline run successfully.

### Iteration 2: Level 1: Input Processing (Weeks 3–4)
- [ ] Implement `Input Agent` for text parsing.
- [ ] Add `Modality Detector` to identify input types (text/audio/PDF/image).
- [ ] Implement `Preprocessing` with pdfplumber, Whisper, Tesseract.
- [ ] Integrate with S3 for file storage.
- [ ] Test Telegram bot with `/add` command.
- **Test**: Validate input parsing and S3 upload with 5 sample inputs.

### Iteration 3: Level 2: Semantic Analysis (Weeks 5–6)
- [ ] Implement `Reflection Agent` for task classification (idea/bug/feedback).
- [ ] Add `Semantic Block Classifier` for text segmentation.
- [ ] Implement `Contextualiza Agent` for entity extraction and domain detection.
- [ ] Update LangGraph orchestrator for Level 1–2 chain.
- **Test**: Verify classification and entity extraction with 10 tasks.

### Iteration 4: Level 3: Analysis & Evaluation (Weeks 7–8)
- [ ] Implement `Risk Assessment` agent for risk scoring.
- [ ] Add `Resource Availability` and `Impact Potential` agents.
- [ ] Implement `Confidence & Urgency` agent for scoring.
- [ ] Configure LangGraph for parallel execution of Level 3 agents.
- **Test**: Validate parallel analysis with 5 complex tasks.

### Iteration 5: Level 4: Recommendations & Visualization (Weeks 9–10)
- [ ] Implement `Aggregator Agent` to combine Level 3 outputs.
- [ ] Add `Visualization Agent` with plotly for charts.
- [ ] Implement `Summary Agent` for recommendations.
- [ ] Deploy to Timeweb Cloud with API endpoints.
- **Test**: Verify recommendations and visualizations with 5 tasks.

---

### Примечания
- **Прогресс-отчет**: Таблица с иконками ( ,  , ☐) и статусами для наглядности, обновляется после каждой итерации.
- **Итерации**: 5 шагов, каждый добавляет функционал и включает тестирование для проверки ассистента.
- **KISS**: План лаконичен, фокусируется на ключевых задачах и тестах, избегает лишних деталей.
- **Ссылки**: Указана связь с `@vision.md` для контекста.
- **Дата**: Учтена текущая дата (02:31 AM CDT, October 05, 2025) для отчета.

После каждой итерации обновляй статусы и заметки в таблице прогресса. Если нужны уточнения, дай знать!

