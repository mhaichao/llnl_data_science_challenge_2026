# API Contracts

FastAPI Pydantic schemas and the exported OpenAPI document will become the
contract source of truth in Phase 2.

## Contract policy

- Scientific units are explicit in field names.
- Unavailable values are nullable; missing data is not converted to zero.
- Large arrays never appear in normal JSON responses.
- Every mock response identifies demo mode.
- Contract changes require team discussion and regenerated TypeScript types.
- Phase 2 will create the generated-types location and command together; generated
  files will not be edited manually.

## Planned versioned resources

- system configuration and health
- datasets and upload metadata
- analysis summaries and jobs
- grounded chat requests/responses
- report retrieval

The detailed field inventory from the project brief will be implemented and
tested in Phase 2. Until then, `/health` is the only stable public endpoint.
