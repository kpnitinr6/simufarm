> HISTORICAL PAID-PATH DOCUMENT. Superseded by MASTER_PROMPT_FREE_TIER.md, current DECISIONS.md and FREE_TIER_REPORT.md. Do not provision from these instructions.

# SimuFarm — initial master prompt execution report

> Historical initial delivery. The operator's later decisions are implemented in DECISION_UPDATE_REPORT.md, ADRs 007/009 and STATUS.md; those supersede budget, approval and sequencing statements below.

Date: 27 October 2026, Asia/Kolkata. Requested organization/repository: **simufarm-team/simufarm**. Infrastructure budget ceiling: **US$200 per month**.

## Outcome
The master prompt's five initial actions have been executed as local deliverables. The result is a tested monorepo scaffold and an approval-ready device-name proposal. The full multi-month SimuFarm platform is **not complete**. P0 remains partial, and P1–P6 have not been executed. This stopping boundary follows §10: report the initial artifacts and await human approval before P2 spec extraction.

The source tree is this directory. A distributable source archive is supplied beside it as simufarm-source.zip. The original operative prompt is preserved in MASTER_PROMPT.md; the surrounding 'How to use' commentary was excluded.

## What was made

### 1. Monorepo and application foundations
Created apps/web, apps/api and apps/orchestrator, plus all requested package/data/infra/task directories.

The React/Vite/TypeScript frontend shows an honest empty device catalog. It fetches the approved-profile API and presents an actionable message when the API is unavailable. A generic reusable device-shell Web Component exists, using original CSS and no branded assets. It does not yet render a real device model or implement mock OS interactions.

FastAPI supplies GET /health/live, GET /api/profiles and GET /api/profiles/{profile_id}. The catalog currently reads versioned JSON, filters review status/confidence and returns 404 for unknown devices. No device records are installed. Liveness does not assert infrastructure readiness. PostgreSQL query projection, manifests API, auth, job submission, test-result queries and production hardening remain future work.

Celery has a serializable health task and Redis configuration. It intentionally cannot launch an emulator at this stage. The test-runner package is a placeholder, not an Appium implementation.

### 2. Frozen contracts
packages/device-schema contains the installable Python package, generated JSON Schemas and generated TypeScript declarations, all at version 0.1.0. One generator and a CI drift check keep wire fields aligned.

Validation covers source URL presence, dimensions/resources, review labels, confidence, timestamps, profile identity and the iOS functional-emulation prohibition. Manifest base images must be provided for functional Android instances. Cross-object/runtime validation remains Python-enforced; static TS types cannot prove numeric limits or source truth.

The brief's schema ambiguities are recorded in ADR 008: visual manifests may have null base_image_id; the omitted os_version field was not silently introduced; field evidence belongs in sidecars. Human review cannot be proven by a self-declared JSON field. P2 must implement evidence/approval verification before real profile promotion.

### 3. Infrastructure and CI definitions
Created PostgreSQL 16, Redis 7 and MinIO Compose definitions with persistent volumes and loopback-only exposed ports. Secrets are supplied through environment variables; the example file contains placeholders only. Added relational/JSONB SQL foundations and a Python 3.12 API Dockerfile. Kubernetes and Terraform directories explicitly document their pending status.

GitHub Actions definitions cover Python checks, contract generation drift, frontend compilation and browser smoke tests. A separate scheduled web smoke workflow runs at 02:00 IST daily. This is a definition only: no repository has been pushed and no workflow has run remotely. Nightly native APK matrices are not configured yet.

Docker is absent from this environment. Backing services were **not deployed**, the Dockerfile was **not built**, and Compose was **not runtime-validated**. YAML parsing is not a substitute for these checks. MinIO bucket initialization and application object-store integration remain unimplemented.

### 4. Decisions and team handoffs
DECISIONS.md contains ADRs 001–006 requested by the prompt, plus four clarifications:

| ADR | Decision |
|---|---|
| 001 | Python 3.12, FastAPI, Celery and Redis |
| 002 | React/Vite/TypeScript and Web Components |
| 003 | Canonical Pydantic contracts, versioned JSON, PostgreSQL JSONB |
| 004 | Shared Android base images on KVM; visual-only iOS |
| 005 | S3-compatible storage and local MinIO |
| 006 | GitHub CI, tests and task-file agent handoffs |
| 007 | Approval boundary and P1/P2 dependency conflict |
| 008 | Manifest and profile contract clarifications |
| 009 | US$200 budget and provisional KVM provider-selection policy |
| 010 | Host-versus-target runtime verification limits |

Created tasks/TEMPLATE.yaml and the three requested seed tasks: P1-generator.yaml, P2-gemini-extract.yaml and P4-emulator-spinup.yaml. An additional P0-bootstrap.yaml tracks the outstanding bootstrap acceptance requirements. Every task names an owner, branch, inputs, outputs, acceptance criteria and guardrails. No DeepSeek, Gemini or Ollama call was made; integrations are unavailable, so these are manual handoffs. Named agent branches are proposed contracts, not completed external-agent work.

### 5. Exactly 1,000 proposed targets
Created data/profiles/_targets.yaml with **1,000 unique brand/model-name candidates across 20 brands**, sourced from Google's supported-device CSV. The proposal includes source model/device identifiers, unique candidate IDs, source URLs and pending review status. No technical specifications were fetched.

| Brand | Candidates |
|---|---:|
| Samsung | 53 |
| Xiaomi | 52 |
| OPPO | 52 |
| vivo | 52 |
| motorola | 52 |
| HUAWEI | 52 |
| HONOR | 52 |
| realme | 52 |
| OnePlus | 52 |
| Google | 52 |
| Sony | 52 |
| Nokia | 52 |
| ASUS | 52 |
| Lenovo | 52 |
| LGE | 52 |
| TECNO | 52 |
| Infinix | 52 |
| Nothing | 11 |
| ZTE | 52 |
| TCL | 52 |

Selection uses brand-balanced round-robin sampling and alphabetical order within each brand. This is **not a validated popularity ranking or a claim to include the latest top models**. The Google inventory contains legacy devices and variants; human review must resolve tablets, regional naming, duplicates in meaning and desired coverage. The first proposal contains Android names only. iOS visual target coverage remains to be proposed after scope review. The phrase 'top 200 brands' in P2's DoD is unresolved against this 20-brand initial proposal.

Provenance is recorded in data/sources/google-device-names.provenance.json, including a checksum of the retrieved source. scripts/propose_targets.py rebuilds the proposal from an operator-supplied copy of the public CSV. The raw complete dataset and trademarked images are not bundled. Google identifies this inventory on its official help page: https://support.google.com/googleplay/answer/1727131 .

## Verification performed

| Check | Actual result |
|---|---|
| Python unit/integration tests | 19 passed |
| Playwright browser test | 1 passed |
| Ruff | Passed |
| Pydantic → JSON Schema → TS drift check | Passed |
| TypeScript and Vite production build | Passed |
| Target proposal integrity | 1,000 unique candidates; source URLs present |
| Approved profile validation | Passed with zero approved profiles; no data coverage implied |
| Task/service YAML parsing | Six documents parsed |
| npm audit during installation | Zero known vulnerabilities reported at installation time |
| Docker services/build | Not run: Docker unavailable |
| Python 3.12 / Node 22 remote CI | Not run: host has Python 3.14.6 / Node 26.4.0 |
| Remote PR, CI, publication | Not performed |
| Emulator, APK and capacity benchmarks | Not performed |

One dependency deprecation warning remains for FastAPI/Starlette TestClient's httpx adapter. Tests passed; pinning/migration should be checked under the intended runtime. package-lock.json records JavaScript resolution. requirements.lock.txt records the locally tested Python environment and is not yet a validated cross-platform Python 3.12 lock.

## Remaining work, by milestone

| Milestone | Remaining |
|---|---|
| P0 | Run Docker backing services, build/test container, test Python 3.12/Node 22, push/review in approved repository, run remote CI and publish schemas to an approved registry |
| P1 | Implement profile-to-shell/page generator; generate 1,000 approved static pages; serve dev URLs; review 50 visual regression samples |
| P2 | Approve target list, configure/manual-route extractors and normalizer, collect field-level sources, build executable evidence validation and review queue, obtain actual human sign-offs |
| P3 | Implement OS chrome, keyboard, rotation, dark mode and navigation; generate interactive pages; run coverage and measure <2s TTI on 10 samples |
| P4 | Select licensed shared images, confirm KVM host, implement fair scheduling/limits/idle teardown/snapshots, evaluate Redroid, demonstrate 200 on-demand profiles and required latency bounds |
| P5 | Implement Appium and web harnesses, sample APK, object-store reports/result API and UI, 50-profile nightly native runs |
| P6 | Expand to 10,000 approved manifests/pages, schedule 1,000 emulator profiles, audit <2TB storage, implement autoscaling/cost dashboard and document measured simulator-hour cost |

No milestone is accepted under the global DoD until required tests, docs, remote review/CI and human approvals are satisfied. The 16–28-week roadmap is not compressed into a claim of completion here.

## Budget and hosting decision
No paid infrastructure has been provisioned or committed: **US$0 new cloud spend**. This excludes any AI subscription/session charges, which were not measured.

ADR 009 provisionally selects Hetzner's dedicated Server Auction as the first low-cost KVM-host candidate. It does not claim a verified cheapest available SKU. The official auction describes dynamic offers and root access but did not expose a stable purchasable quote in this session: https://www.hetzner.com/sb/ . Hetzner's published AX42-1 reference is $117.10/month plus $59 setup, excluding VAT and IPv4: https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/ . That reference is not an approved all-in quote or confirmed stock.

Planning allocation: host at most $120, backup $15, tax/network reserve $35, contingency $30. Setup charges must fit the first month too unless separately approved. Final pricing, checkout tax, bandwidth, location, host suitability and actual /dev/kvm availability remain unverified. A lower-cost VPS is unsuitable unless nested KVM is explicitly available and tested. No actual cloud configuration is enabled.

The budget supports a small measured development deployment, not a promise of hundreds of concurrent emulators. Start with one active instance; increase only after resource measurements and cost review. The prompt's >50-concurrent gate still applies.

## Next operator decisions
1. Approve or revise the concrete _targets.yaml list, including phones/tablets/regions and desired iOS visual targets.
2. Resolve the P1-before-P2 dependency and 'top 200 brands' wording, then authorize P2 extraction. No extraction begins merely because this report was delivered.
3. Provide approved GitHub/registry access and a Docker-capable environment to finish P0.
4. Approve a verified all-in KVM-host quote only when P4 is ready; licensing approvals are required for future branded assets.

The project is ready for source review and target-list review. It is not ready for production, native app testing, or scale claims.
