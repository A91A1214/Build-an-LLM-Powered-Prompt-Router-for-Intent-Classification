# LLM-Powered Prompt Router

An intelligent service that routes user requests to specialized AI personas using intent classification.

## Features
- **Intent-Based Routing**: Classes user intent (Code, Data, Writing, Career) before responding.
- **Specialized Personas**: Expert prompts for specific domains to ensure high-quality responses.
- **Robust Classification**: Uses JSON-formatted LLM responses with confidence scoring.
- **Observability**: Logs all routing decisions and responses to `route_log.jsonl`.
- **Dockerized**: Easy setup and execution using Docker and Docker Compose.

## Architecture
1. **Classify**: A lightweight LLM call determines the user's intent from the message.
2. **Route**: The system maps the intent to a specific expert system prompt.
3. **Respond**: A second, detailed LLM call is made using the specialized persona.
4. **Log**: Every interaction is logged in JSONL format for audit and debugging.

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed.
- OpenAI API Key.

### Configuration
1. Clone the repository.
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Add your `OPENAI_API_KEY` to the `.env` file.

### Running the Application

#### Using Docker (Recommended)
Build and run the evaluation test suite:
```bash
docker-compose up --build
```
This will run the 15 predefined test cases and exit. You can check `route_log.jsonl` for the results.

#### Running Locally
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the interactive CLI:
   ```bash
   python main.py
   ```
3. To run the automated test suite locally:
   ```bash
   python main.py --test
   ```

## Design Decisions
- **Two-Step Orchestration**: Separating classification from generation allows for more accurate and context-aware responses compared to a single monolithic prompt.
- **JSON Output**: Forcing the classifier to return JSON ensures structured data for easier routing logic.
- **Confidence Threshold**: Any classification with confidence below 0.7 (configurable) is treated as 'unclear' to avoid misleading the user with inaccurate 'expert' responses.
- **Personas**: Each persona is designed to be "opinionated" and focused, following the provided constraints (e.g., Code Expert provides only code and brief technical explanations).
