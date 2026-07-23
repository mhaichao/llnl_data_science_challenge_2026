# Analysis API

FastAPI orchestration service for the Multi-Agent Lattice CT Inspection
Dashboard.

Phase 1 provides application configuration, CORS, and a health endpoint only.
Pydantic analysis contracts, mock services, versioned routes, storage adapters,
and report/chat endpoints are Phase 2 work.

## Local development

From the repository root:

```bash
.venv/bin/python -m pip install -r services/analysis-api/requirements-dev.txt
cd services/analysis-api
../../.venv/bin/python -m uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000/health` or `http://localhost:8000/docs`.

Do not add scientific calculations to API route modules. Future implementations
must sit behind service interfaces and return validated Pydantic schemas.
