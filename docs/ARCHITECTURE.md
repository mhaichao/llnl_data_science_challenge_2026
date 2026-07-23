# Architecture

## Project overview

The Multi-Agent Lattice CT Inspection Dashboard separates presentation,
orchestration, and deterministic scientific analysis so four contributors can
work independently.

```text
Browser
  ├── Next.js frontend on Cloud Run
  ├── compact API requests to FastAPI on Cloud Run
  └── future direct uploads to Cloud Storage
                                  │
FastAPI orchestration ── typed service interfaces
                                  │
Scientific Python / future jobs ── compact results and asset URIs
```

## Frontend architecture

`apps/web` is a strict TypeScript Next.js App Router application. Phase 1
contains only the base layout and architectural landing page. Later phases will
organize routes under `app/`, domain UI under `features/`, shared primitives
under `components/`, and API/configuration code under `lib/`.

Route files compose feature components. They do not calculate scientific
results. Browser-visible environment values use the `NEXT_PUBLIC_` prefix and
must never contain credentials.

## Backend architecture

`services/analysis-api` is an independently runnable FastAPI service.

- `api/` owns HTTP routing and validation boundaries.
- `schemas/` owns Pydantic request/response contracts.
- `core/` owns settings, logging, errors, and security policy.

Only `/health` exists in Phase 1. Versioned domain endpoints begin in Phase 2.

## Scientific-layer boundary

The existing root `src/` directory remains the challenge scientific/MCP layer.
It is not renamed or moved. The API will eventually use adapters to call
deterministic functions. It will not expose arbitrary local file paths or put
large arrays into JSON.

## API and data flow

Phase 2 will establish FastAPI OpenAPI as the single contract source and create
the generated TypeScript type location at the same time as the generation
workflow.

The intended compact flow is:

1. frontend selects a demo dataset or requests a signed upload;
2. browser uploads large data directly to Cloud Storage;
3. API creates or reads an analysis job;
4. scientific services write result assets to storage;
5. API returns metadata, statistics, defect records, statuses, and URIs;
6. frontend renders the validated response;
7. assistant receives only the compact analysis summary.

## State-management approach

Later frontend phases will use:

- URL state for shareable defect filters;
- component state for inspector controls and row selection;
- server-state caching for API responses;
- a small shared store only for dataset ID, analysis ID, demo mode, API status,
  and pipeline status.

No single global object will own every interaction.

## Data contracts

Pydantic schemas will be implemented in Phase 2. Missing scientific values will
be nullable rather than represented by misleading zeros. Units remain explicit
in field names.

## Mock-data strategy

One deterministic backend `AnalysisSummary` will feed every page. The frontend
will not duplicate scientific numbers in individual components. Mock services
will use a fixed seed and mark every response as demo data.

## Cloud Run and Cloud Storage

The frontend and API deploy as separate containers. Cloud Storage is optional in
demo mode. Production uploads bypass Next.js and normal JSON requests by using a
short-lived signed URL created by the API.

## Future job processing

The initial API will expose placeholder job resources without adding queues.
Cloud Run Jobs, Cloud Tasks, Pub/Sub, Compute Engine, or GPU execution will be
evaluated only after workload measurements.

## Security boundaries

- CORS origins come from backend environment variables.
- production origins must be explicit; wildcard credentials are not allowed.
- user filenames and types are validated before signed-upload creation.
- no endpoint accepts shell commands or arbitrary filesystem paths.
- secrets stay server-side and are not logged.
- authentication belongs at the Cloud Run/API boundary in a later phase.

## Known Phase 1 limitations

- no analysis contracts or mock domain endpoints;
- no dashboard feature routes;
- no Cloud Storage adapter or signed uploads;
- no generated TypeScript API declarations;
- no production Dockerfiles or Cloud Build configuration;
- no authentication, database, queue, agent, or LLM connection;
- no real scientific computation through the API.
