
# Conventions for Code Development (@conventions.md)

This document outlines the core coding conventions for the "AI Backlog Assistant" project, aligning with the development principles defined in [@vision.md](#). These rules are designed to ensure consistency, readability, and maintainability, adhering to the KISS principle.

## General Guidelines
- Follow the simplicity and iterativity principle from [@vision.md](#) by writing clean, modular code with minimal complexity.
- Adhere to PEP 8 style guidelines for Python, as specified in [@vision.md](#), ensuring readability.
- Use flake8 for linting to enforce code consistency, as outlined in [@vision.md](#).

## Code Structure
- Organize code into modular files (e.g., `agents/level1/input_agent.py`) as per the project structure in [@vision.md](#).
- Maintain clear interfaces for all agents and modules, avoiding unnecessary abstractions (see [@vision.md](#) for details).
- Include docstrings for public functions/classes, following the documentation approach in [@vision.md](#).

## Testing
- Write minimal unit tests using `pytest` for each component, targeting ~50% coverage, as described in [@vision.md](#).
- Use mocks for external services (e.g., Mistral API, S3) to ensure stability, per the testing approach in [@vision.md](#).
- Integrate tests with CI/CD via GitHub Actions, as specified in [@vision.md](#).

## Error Handling
- Implement basic error logging to stderr and PostgreSQL, following the logging approach in [@vision.md](#).
- Handle errors with single retries where applicable, as outlined in [@vision.md](#).

## Version Control
- Use Git with `main` and `dev` branches, submitting changes via pull requests, per the versioning guidelines in [@vision.md](#).

## Collaboration
- These conventions are intended for code assistants (e.g., GitHub Copilot) to generate compliant code. Refer to [@vision.md](#) for full context and principles.

---

### Примечания
- Правила лаконичны, фокусируются на ключевых аспектах (стиль, структура, тестирование, ошибки, версия), избегая дублирования деталей из `@vision.md`.
- Ссылки на `@vision.md` обеспечивают доступ к полным описаниям без переписывания.
- Подходит для передачи ассистенту, обеспечивая ясные рамки для генерации кода.
