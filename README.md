# Guardrails Gateway

A minimal GenAI guardrails gateway that analyzes an incoming prompt + optional retrieved context, returning a policy decision (allow/block/transform).

## Features
*   **PII Detection**: Redacts emails and phone numbers.
*   **Prompt Injection**: Blocks attempts to bypass system rules.
*   **RAG Injection**: Scans retrieved context documents for malicious triggers.
*   **Policy Engine**: Returns `allow`, `block`, or `transform` based on risk scores.

## Requirements
*   Docker & Docker Compose
*   Python 3.9+ (for local development)

## Quick Start (Docker)
The easiest way to run the entire system (API + UI):

```bash
docker compose up --build
```
*   **API**: [http://localhost:8000/docs](http://localhost:8000/docs)
*   **UI**: [http://localhost:8501](http://localhost:8501)

## Local Development
1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    pip install -r requirements.ui.txt
    ```
2.  **Start API**:
    ```bash
    uvicorn app.main:app --reload
    ```
3.  **Start UI** (in a new terminal):
    ```bash
    streamlit run ui/streamlit_app.py
    ```

## CLI Usage
To analyze a request from the command line:

1.  **Create a sample file** (e.g., `input.json`):
    ```json
    {
      "prompt": "Call me at 555-0199",
      "context_docs": []
    }
    ```

2.  **Run the CLI**:
    ```bash
    python cli.py --input input.json --output output.json
    ```

## Running Tests
To verify all 10 requirements are met:

```bash
# Local
python -m pytest tests/

# Docker
docker compose exec api pytest tests/
```

## Design Notes

### Assumptions
*   **Deterministic**: We used regex and static keywords instead of LLMs to ensure offline reproducibility and speed.
*   **Scope**: This is an MVP. It handles English text only.

### Tradeoffs
*   **Regex for PII**: Fast and exact, but brittle. It misses obfuscated emails (e.g., "bob at gmail"). In production, we would use a proper NER model (like Presidio).
*   **Keyword Injection**: Simple blocking of phrases like "Ignore previous instructions". In production, this would be replaced by a vector database lookup or an LLM classifier (e.g., Llama Guard).

### Security
*   **No Persistence**: We do not store logs or prompts to avoid PII leakage liability.
*   **Input Validation**: Strict Pydantic models prevent malformed data.
*   **Sanitization**: We return `[REDACTED]` tokens instead of masking characters to make it clear intervention occurred.

### Next Steps for Production
1.  **Authentication**: Add API Key middleware.
2.  **Rate Limiting**: Use Redis to prevent DoS attacks.
3.  **Observability**: Add Prometheus metrics for "Blocked Requests" count.
