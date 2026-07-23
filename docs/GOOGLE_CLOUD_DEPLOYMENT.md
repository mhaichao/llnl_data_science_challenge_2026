# Google Cloud Deployment

Production deployment is scheduled for Phase 6. No cloud resources or
credentials are required in Phase 1.

## Planned prerequisites

- a Google Cloud project with billing and least-privilege administration;
- Artifact Registry, Cloud Build, Cloud Run, and optionally Cloud Storage APIs;
- separate deploy/runtime service accounts;
- reviewed frontend URL, backend URL, and CORS origins.

## Planned services

- Next.js frontend Cloud Run service;
- FastAPI backend Cloud Run service;
- optional regional Cloud Storage bucket for inputs and generated assets.

## Environment variables

Frontend public configuration:

- `NEXT_PUBLIC_ANALYSIS_API_URL`
- `NEXT_PUBLIC_DEMO_MODE`
- `NEXT_PUBLIC_APP_VERSION`

Backend server configuration:

- `APP_ENV`
- `CORS_ALLOWED_ORIGINS`
- `GCP_PROJECT_ID`
- `GCS_BUCKET_NAME`
- `DEMO_MODE`
- `LOG_LEVEL`

No secret may use a `NEXT_PUBLIC_` variable.

## Direct-upload design

The browser will request validated, short-lived signed URLs from FastAPI and
upload CT data directly to Cloud Storage. Next.js server actions, API routes,
chat prompts, and normal JSON requests will never proxy full CT volumes.

## Phase 6 additions

This document will gain exact commands for service enablement, Artifact
Registry, service accounts, bucket creation, builds, Cloud Run deployment,
CORS, health testing, logs, updates, common errors, and cost controls after the
production Dockerfiles exist.
