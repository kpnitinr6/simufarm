> HISTORICAL PAID-PATH DOCUMENT. Superseded by MASTER_PROMPT_FREE_TIER.md, current DECISIONS.md and FREE_TIER_REPORT.md. Do not provision from these instructions.

# P0 runtime acceptance — NOT VALIDATED

Observed 27 October 2026: no Docker CLI, Docker Desktop/OrbStack installation or Docker socket was found. Python 3.12 is unavailable locally. GitHub CLI authentication reports the current token invalid, and no Git remote is configured. No remote environment credentials were provided. Do not interpret prepared workflows, YAML parsing or mocked unit tests as Docker evidence.

## Prepared changes
- Compose now builds/runs the Python 3.12 API image.
- MinIO initialization runs as an idempotent one-shot service using the API image and waits for local MinIO accessibility. It refuses non-local endpoints.
- API startup depends on healthy PostgreSQL/Redis and successful bucket initialization.
- A container-side verification script checks API liveness, PostgreSQL connection and schema, Redis ping, S3 bucket access and write/read/delete roundtrip.
- CI now includes a real Docker smoke job with evidence artifacts, plus the existing Python 3.12/Node 22 code checks. These jobs have not run remotely.

## Execute on the supplied Docker-capable environment
From the repository root, create .env with local credentials (use URL-safe alphanumeric/hex passwords for DATABASE_URL interpolation). Never attach .env or resolved Compose configuration containing secrets to a report.

```sh
cp .env.example .env
# Replace password placeholders before startup.
docker version
docker compose version
docker compose --env-file .env -f infra/compose.yaml config --quiet
docker compose --env-file .env -f infra/compose.yaml up --build -d --wait --wait-timeout 180
docker compose --env-file .env -f infra/compose.yaml exec -T api python scripts/verify_stack.py
docker compose --env-file .env -f infra/compose.yaml logs --no-color minio-init
docker compose --env-file .env -f infra/compose.yaml ps --all
# Repeat initializer to demonstrate idempotency:
docker compose --env-file .env -f infra/compose.yaml run --rm minio-init
```

Record commit SHA, Docker/Compose versions, image build output, Compose service state, successful initializer output, successful object roundtrip and remote CI run URL/SHA. CI must have both code-check and docker-smoke jobs green on the same reviewed commit. Local evidence does not replace the remote Python 3.12/Node 22 run.

After collecting real evidence, update data/validation/p0-state.json with evidence references and review results. Leave p0_complete=false until every required gate passes. Global package publication/review requirements remain tracked separately and are not silently waived. A confirmed all-in Hetzner quote is an additional provisioning gate even after P0 passes.

## Current gate table
| Requirement | State |
|---|---|
| docker compose up succeeds | Not run; Docker unavailable |
| Python 3.12 API image builds | Not run |
| MinIO bucket initializes and repeated init succeeds | Prepared; not runtime-tested |
| API/Postgres/Redis/S3 object roundtrip | Prepared; not runtime-tested |
| Remote CI Python 3.12 / Node 22 green | Not run; auth invalid, no remote |
| P0 complete | **No** |
| Provisioning allowed | **No** |
