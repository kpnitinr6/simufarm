# Architecture decisions — SimuFarm
Recorded 27 October 2026. Owner: Codex. Organization: simufarm-team. Repository: simufarm.

## ADR 001 — Python API and worker stack (accepted)
Python 3.12, FastAPI, Celery, Redis. One API plus independent queue workers. This scaffold exposes health and approved-profile read endpoints only. No emulator lifecycle is claimed.

## ADR 002 — Web and reusable simulator shells (accepted)
React, Vite, TypeScript with Web Components for reusable shells. The initial generic CSS shell contains no branded assets. P1/P3 remain gated; it is not a device-fidelity implementation.

## ADR 003 — Versioned profile contracts and PostgreSQL JSONB (accepted)
Versioned JSON is the profile source of truth; PostgreSQL JSONB becomes the query projection. Pydantic is the canonical wire schema; JSON Schema and TypeScript declarations are generated and drift-checked. Python/JSON runtime validation enforces numeric ranges and cross-object rules that TS types cannot encode. The bootstrap API reads approved JSON; database sync is pending P2. Contracts are version 0.1.0; future wire changes require versioning and migration notes.

## ADR 004 — Shared Android base images and KVM containers (accepted)
Use 5–8 shared base system images with device profiles. Never create full per-brand clones. Linux KVM hosts are required for functional Android emulation. iOS is static/interactive visual only. Redroid must be evaluated and benchmarked during P4 before adoption. The image manifest is empty by design until licensed images are selected.

## ADR 005 — S3-compatible artifact storage (accepted)
MinIO for local development; provider-compatible object storage for production. Store manifests, shell outputs, screenshots, and test artifacts separately from shared image binaries. No image binaries enter git. Local Compose defines persistent volumes but has not been deployed here.

## ADR 006 — CI, testing, and controlled agent handoffs (accepted)
GitHub Actions runs lint, contract drift, backend unit/integration, frontend build and Playwright smoke checks. A nightly web workflow is included; native nightly runs wait for P5 and an approved KVM runner. YAML task files define ownership and branches. DeepSeek, Gemini, and Ollama integrations are unavailable: tasks are prepared for manual dispatch, not represented as executed. Packages remain local; registry publication and remote CI require repository access.

## ADR 007 — Milestone order and explicit approval boundary (accepted)
Execute the prompt's five first actions now. Fetch device names only to propose the target list; do not extract specifications. P1 depends on verified profiles while the brief orders P1 before P2: record that dependency, and request an explicit P2-before-P1 dependency resolution after target approval. Do not pretend P1's 1,000 URLs exist or silently skip DoD. No later milestone has started. Human review remains required for every promoted profile. The 'top 200 brands' criterion conflicts with a 20-brand initial proposal and needs scope clarification during target review.

## ADR 008 — Wire-contract clarifications (accepted)
The detailed §5 manifest omits os_version although §4 mentions it. Preserve the frozen §5 field set: encode Android version in the shared base-image record and simulator identity; add an explicit os_version field only through a later versioned contract change. base_image_id is required as a key but nullable for visual simulators, required non-null for emulators. Notch enum values are limited initially and need versioned expansion if sourced devices require other shapes. Per-field evidence lives in sidecars to preserve the profile field set. Schema validation alone cannot establish the truth of a human review claim; signed/referenced evidence checks are a P2 prerequisite.

## ADR 009 — Budget and provisional KVM provider selection (proposed; no purchase)
User ceiling: US$200/month. Provisional provider: Hetzner dedicated Server Auction, selecting the cheapest currently available x86_64 machine that passes KVM, storage, memory and all-in-price checks. This is a selection policy, not a verified cheapest SKU or a global lowest-price claim. Dynamic inventory did not expose a reliably purchasable price in this session. Final provider/SKU selection therefore remains open; do not provision.

Primary-source review, 27 October 2026:
- https://www.hetzner.com/sb/ documents refurbished dedicated servers, root access, dynamic inventory and no setup fees. Recheck at checkout.
- https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/ lists AX42-1 at $117.10/month plus $59 setup, excluding VAT and IPv4. This is a published reference, not an availability quote; first month exceeds $176.10 before additions.
- https://www.netcup.com/en/helpcenter/documentation/server warns about nested virtualization. Being hosted on KVM does not prove a guest can run KVM emulators; exclude unverified nested-virtualization VPS plans.
- OVHcloud Eco/RISE remains a comparison candidate; no verified comparable all-in offer was obtained.

Planning allocations, not vendor quotes: host <= $120, object backup <= $15, tax/network reserve <= $35, contingency >= $30 = $200. Setup fees must fit the first month's $200 total unless separately approved. These allocations may prove infeasible. Start with one emulator at a time; thousands of catalog entries are metadata, not thousands of concurrent instances. Require measured /dev/kvm availability, CPU virtualization flags, a successful emulator boot, and checkout total before purchase. No automated provisioning configuration is supplied.

## ADR 010 — Local verification runtime (accepted for bootstrap verification only)
Host Python is 3.14 and Node is 26. Docker is absent. Production/API image and GitHub CI target Python 3.12; CI targets Node 22. Host checks supplement, and do not replace, the required target-runtime CI and Docker checks. P0 remains partial until those checks and publication/deployment requirements pass.
