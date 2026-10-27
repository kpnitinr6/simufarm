# SimuFarm — zero-spend development path

A software-only simulator platform scaffold. The active brief is MASTER_PROMPT_FREE_TIER.md and active decisions are DECISIONS.md. Recurring cloud spend and setup allowance are both **US$0**. Previous paid plans are historical and must not be provisioned.

**Current delivery:** tested API/catalog/schema foundations, task handoffs and source-backed feasibility research. **Not delivered:** a running Oracle VM, a booted emulator, noVNC, GADS, native APK tests, or generated device-specific pages. There are zero approved technical profiles and zero launched sessions.

## Free-path compatibility blockers

The requested unmodified budtmo/docker-android launcher requires /dev/kvm and installs an x86_64 Android image. A native Oracle ARM/no-KVM path is not established; SwiftShader only provides software graphics. Do not claim this image boots by passing -no-accel. GADS adopts running emulators and requires MongoDB; it does not launch them. See docs/EMULATOR_COMPATIBILITY.md.

Current primary-source checks show Oracle Free-only allowance equivalent to2 OCPU/12 GB and MobileAPI pricing/signup at50 requests/month, not the brief's4/24 and200. Account entitlements and remaining quota are unverified. See docs/FREE_TIER_FACT_CHECK.md. No API requests, trial signup, account upgrade or cloud resource creation has occurred.

The operator confirmed the Oracle account active and ZERO_SPEND_CONFIRMED=yes. The account email is stored only in ignored .env. The supplied repository https://github.com/kpnitinr6/simufarm is **private**. Automatic CI is disabled because the current token cannot read billing usage. Manual-only workflows must not run before free-minute/billing controls are checked. Repository visibility was not changed.

## Local setup

Intended runtime: Python 3.12 and Node 22. Current host verification uses Python 3.14/Node 26; remote target-runtime CI has not run.

```sh
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e ./packages/device-schema -e '.[dev]'
npm ci
uvicorn simufarm_api.main:app --host 127.0.0.1 --port 8000
# In another terminal:
npm run dev
```

Web http://127.0.0.1:5173; API documentation http://127.0.0.1:8000/docs. API liveness does not establish emulator or cloud readiness.

Optional local Docker development, after setting local MinIO credentials in .env:
```sh
docker compose --env-file .env -f infra/docker/compose.yaml up --build -d --wait
```
This defines API/MinIO/bucket-init only. No Oracle, emulator, GADS, MongoDB, PostgreSQL or Redis is deployed. Docker is unavailable in the current environment, so this configuration has not been runtime-validated.

```sh
pytest -q
ruff check .
python scripts/validate_data.py
npm run contracts:check
npm run build
npx playwright install chromium
npm run test:web
python scripts/zero_spend_check.py tasks/P1-static-generator.yaml
# External-resource tasks report blocked and exit2; they execute no action.
```

## Data and approval

Schema 0.2.0 requires source_type=api|scraper|manual. Scraped data retains confidence<0.9 and requires actual human review before promotion. API/manual profiles retain the>=0.9 review threshold. No JSON field proves the truth of a review; evidence maps and reviewer approvals are required.

The original1000-name list is approved for static generation only, explicitly not spec extraction. The500-name alternative is vendor-share-weighted, not a measured model-popularity ranking. Its separate proposed top100 awaits explicit approval. The visual iPhone list now contains55 iPhones only, per operator direction; no iPad padding. No device specifications or branded assets were collected.

## Runtime design and limits

The planned maximum is **one active Android session**, with a future durable SQLite queue and test-result store. The queue, lifecycle executor, GADS integration and Appium harness are not implemented. Emulator launch remains disabled until a supported, approved zero-cost architecture is established. Boot time is unmeasured;5–15 minutes is a brief assumption, not a platform guarantee. P6 scale-out is out of scope.

Visual mockups do not reproduce vendor firmware. Emulator results cannot establish OEM quirks, real sensors/radio, camera fidelity, DRM, thermals, battery behavior or physical performance. iPhone support is visual-only. No functional iOS emulation, per-brand full image clones, image binaries, trademarked wallpapers/logos, or cloud-paid fallback is included.

See FREE_TIER_REPORT.md, STATUS.md and data/usage/free-tier-usage.json for current evidence and remaining work.
