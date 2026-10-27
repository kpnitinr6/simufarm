# SimuFarm
A software-only mobile simulator platform scaffold for simufarm-team/simufarm.

This delivery executes the master prompt's initial bootstrap and planning actions. It is not a deployed emulator farm. There are **1,000 proposed device names, zero approved profiles, zero generated simulator URLs, and zero running emulators**.

## What is implemented
- FastAPI health and approved-profile read API; Pydantic profile/manifest contracts.
- Generated JSON Schema and TypeScript packages with drift checks.
- React/Vite catalog shell and a generic Web Component primitive.
- Celery worker health task; no emulator launch implementation.
- PostgreSQL/Redis/MinIO Compose definitions, SQL schema and API Dockerfile.
- Unit/integration checks, Playwright bootstrap smoke, CI and nightly web workflow.
- Task handoffs, ADRs, target proposal, provenance, status and execution report.

## Local setup
Python 3.12, Node 22, npm, and Docker Compose v2 are the intended toolchain.

```sh
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ./packages/device-schema -e '.[dev]'
npm ci
cp .env.example .env
# Replace local password placeholders in .env before starting services.
docker compose --env-file .env -f infra/compose.yaml up -d
uvicorn simufarm_api.main:app --host 127.0.0.1 --port 8000
# In another terminal:
npm run dev
```
Web: http://127.0.0.1:5173; API docs: http://127.0.0.1:8000/docs.
API liveness is not a database/object-store readiness check. Compose currently starts backing services only; API and worker are started separately. MinIO bucket creation, database projection sync and application storage integration remain to implement.

```sh
celery -A simufarm_orchestrator.worker:app worker --loglevel=info
pytest -q
ruff check .
python scripts/validate_data.py
npm run contracts:check
npm run build
npx playwright install chromium
npm run test:web
```

## Profile approval and provenance
Review data/profiles/_targets.yaml before spec extraction. Names come from Google's public device inventory, not invented technical specifications. It is a balanced candidate pool, not a market-share ranking. Models, regional aliases, tablet inclusion and device class require human review. Current proposal covers Android; iOS visual targets can be added after approval.
See docs/PROFILE_EVIDENCE.md for evidence and human review requirements. No real profile may be committed based only on a model's confidence or self-declared reviewer label. The P2 promotion workflow must validate those records. Synthetic data exists only in tests, clearly marked, with example.org references.

## Fidelity limits and prohibited uses
A visual shell is not a real OEM operating system. Android emulator results cannot establish OEM firmware compatibility, actual radio/cellular behavior, physical sensor behavior, thermal/battery performance, camera fidelity, DRM behavior, or real-hardware performance. Google Play services and images depend on image selection and licensing. Real handset testing may still be needed outside this platform. iOS is supported only through static/interactive web visuals; no functional iOS emulator is supplied or planned.
No logos, branded wallpapers or redistributable device imagery are bundled. Generic frames only until licenses receive human approval. No per-brand full image clones, committed secrets, or image binaries.

## Scope, costs and handoffs
Budget ceiling US$200/month; provider selection is provisional in ADR 009. No cloud resources have been purchased. A 1,000-device catalog does not imply 1,000 simultaneous emulators. Functional scaling must fit measured host capacity and budget. More than 50 concurrent emulator instances always requires explicit approval; any new paid resources also require approval under the master prompt.
External agent task files are ready for manual routing; the named external agents have not run. No GitHub repository, PR, remote CI run, registry publication or production deployment is claimed.

Read STATUS.md, DECISIONS.md and EXECUTION_REPORT.md for exact completion evidence and remaining work.
