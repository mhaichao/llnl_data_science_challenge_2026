# Team Integration Guide

## Repository layout

| Path | Owner / responsibility |
| --- | --- |
| `apps/web/` | Next.js presentation and client interaction |
| `services/analysis-api/` | FastAPI validation and orchestration |
| `src/` | existing challenge scientific/MCP code |
| `docs/` | architecture and operational guidance |

## Local setup

Frontend:

```bash
nvm install
nvm use
npm install
cp apps/web/.env.example apps/web/.env.local
npm run dev:web
```

Backend, in a second terminal:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r services/analysis-api/requirements-dev.txt
cp services/analysis-api/.env.example services/analysis-api/.env
npm run dev:api
```

The frontend runs at `http://localhost:3000`; the API runs at
`http://localhost:8000`.

## Suggested ownership

1. frontend shell, theme, navigation, shared primitives, responsive layout;
2. CT loading, slice visualization, segmentation controls, histograms;
3. skeletonization, thickness, density, defects, spatial analysis;
4. FastAPI orchestration, grounded assistant, reports, agents, cloud jobs.

Shared Pydantic contracts require team discussion before modification.

## Adding features in later phases

- Add pages as small route files under `apps/web/app/`.
- Put domain components and local state under `apps/web/features/<feature>/`.
- Put reusable, domain-neutral UI under `apps/web/components/`.
- Add API endpoints through an `APIRouter` module and include it in
  `app/api/router.py`.
- Put scientific behavior behind a protocol in the feature folder created by its
  owner; route modules perform no scientific calculations.
- Replace mock services through dependency injection, not route rewrites.

## API type regeneration

Phase 2 will create the generated-types folder and exact export/generation
commands together. Generated TypeScript files are reviewed but never
hand-edited.

## Merge-conflict avoidance

- Work in the feature-owned directory whenever possible.
- Do not rename or move root `src/`.
- Avoid routine edits to root layout, API router, and shared schemas.
- Separate contract changes from UI changes.
- Do not commit local environment files, generated CT outputs, or large data.
- Run the relevant local checks before requesting review.

## Scientific integration testing

A scientific adapter test should use a bounded synthetic fixture, validate its
typed result, and exercise the service through dependency injection. Tests must
not require the tracked CT files, GCP credentials, an LLM key, a GPU, or a
browser.
