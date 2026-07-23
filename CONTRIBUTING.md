# Contributing

## Branches and commits

Use focused branches such as:

- `frontend/<feature>`
- `backend/<feature>`
- `science/<feature>`
- `infra/<feature>`
- `docs/<topic>`

Keep commits reviewable and avoid formatting unrelated files. Commit messages
should describe the result, for example `backend: add demo analysis contract`.

## Pull requests

Every pull request should include:

- concise summary and feature owner;
- screenshots for visual changes;
- files or directories changed;
- explicit API contract changes;
- commands and tests run;
- integration notes and known limitations.

Keep contract changes separate when practical. Obtain review from each affected
workstream before merging shared schema changes.

## Phase 1 checks

```bash
npm run lint:web
npm run typecheck:web
npm run test:web
npm run build:web
cd services/analysis-api && python -m pytest -q
```

Later phases will add formatting, generated-type parity, integration, and Docker
checks.

## Generated files

FastAPI OpenAPI will be the source of truth once generated frontend types are
introduced. Regenerate types after an approved Pydantic contract change and
commit the schema and generated diff together. Do not create or hand-edit a
generated-types folder before the contract generation workflow exists.

## Merge-conflict avoidance

- keep route files small;
- add behavior inside a feature-owned directory;
- avoid editing root layout and API router for local feature work;
- preserve root `src/` paths;
- do not rename shared models silently;
- do not commit `.env`, credentials, real CT outputs, or caches.

## Formatting and typing

TypeScript uses strict mode and ESLint. Python code requires type hints on
public functions. The final formatting tools will be selected in Phase 7 to
avoid introducing overlapping toolchains.
