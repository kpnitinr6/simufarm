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

## ADR 007 — Option A, scoped target approval and staged delivery (accepted 27 October 2026)
User decisions supersede the previous sequencing proposal. Adopt Option A: identify and explicitly approve the top 100 devices, extract and human-verify their specs, run P1 generation against those 100, and expand only after that pilot passes. This resolves the P1/P2 data dependency with a narrowly scoped extraction pilot; it does not waive P0 acceptance or profile-evidence requirements.

The existing 1,000-name list is **approved for P1 static mockup generation only**. The same decision explicitly prohibits spec extraction from that list. It is not approval for interactive or functional emulation, nor evidence that the device specifications are known. No invented dimensions may be used to turn names into device-specific frames. Thus approval of names alone cannot produce accurate static models under the existing profile contract.

Prepare in parallel (a) a 500–1,000-device alternative using public market-share/reach evidence, and (b) a 100-device Apple visual proposal. Public vendor share is only a vendor-level prioritization proxy; absent model-level reach data, do not represent a model order as measured popularity. The top-100 extraction pilot must be a separate approved artifact; new proposals inherit no approval. Pending operator clarification, prepare a top-100 candidate subset but do not extract specs. An iPhone+iPad/iPadOS list must flag the broader scope; approval is requested before treating it as the intended iOS set.

P0 stays **incomplete** until Docker Compose starts successfully, the API image builds, MinIO bucket initialization and storage roundtrip succeed, and remote CI is green on Python 3.12 / Node 22. Capture commit-bound evidence; local Python 3.14 checks do not replace this gate. The global review/publication requirements remain tracked. The top-200-brands wording still needs scope clarification before accepting P2 at full scale.

## ADR 008 — Wire-contract clarifications (accepted)
The detailed §5 manifest omits os_version although §4 mentions it. Preserve the frozen §5 field set: encode Android version in the shared base-image record and simulator identity; add an explicit os_version field only through a later versioned contract change. base_image_id is required as a key but nullable for visual simulators, required non-null for emulators. Notch enum values are limited initially and need versioned expansion if sourced devices require other shapes. Per-field evidence lives in sidecars to preserve the profile field set. Schema validation alone cannot establish the truth of a human review claim; signed/referenced evidence checks are a P2 prerequisite.

## ADR 009 — Revised budget and hard provisioning gate (accepted 27 October 2026)
Recurring ceiling: **US$200/month**, including recurring tax, IPv4, storage, bandwidth and other recurring charges. A separate **US$100 one-time setup allowance applies in month 1 only**. Maximum planned first-month commitment is US$300, split as <=$200 recurring plus <=$100 eligible one-time setup; the extra $100 cannot support a higher recurring run rate.

**Do not provision** until P0 is fully green AND a confirmed all-in Hetzner quote is attached, including VAT/tax treatment, primary IPv4, exact SKU/configuration, region, stock, currency, recurring total, setup total and validity/confirmation timestamp. The quote and vendor confirmation of KVM suitability must refer to the selected configuration. Actual host KVM and emulator boot checks follow only after a separately authorized provisioning action, before accepting emulator capacity. A marketing page, estimated conversion, public price table, or alternative-provider comparison does not satisfy this gate. The user explicitly requires a Hetzner quote; switching providers requires a new operator decision.

Prepare a comparison of Hetzner AX-line, OVH, Scaleway bare-metal and AWS m7i.metal. Record published tax/IPv4 components, tax assumptions, KVM documentation and unverified availability separately. Hardware virtualization documentation is not proof that a purchased host has exposed /dev/kvm; acceptance includes a real KVM/emulator boot check when a host is authorized. No host is authorized now. Billing jurisdiction/tax status and acceptable hosting region have been requested; do not infer them from the chat timezone.

Re-estimate (published references, not confirmed quote): Hetzner AX42-1 $117.10/month plus $1.90 primary IPv4 = **$119/month pre-tax**, with **$59 setup pre-tax**. At an illustrative 20% tax, host+IPv4 is $142.80 recurring and setup is $70.80; at an illustrative 18%, $140.42 and $69.62. Neither tax rate is asserted to apply to the user. With an internal $15 backup allocation and $10 other-recurring allocation, remaining recurring capacity is $32.20 (20% example) or $34.58 (18% example). These allocations are planning limits, not vendor service quotes. Setup must independently stay <=$100; recurring independently <=$200. Actual provider currency/tax at checkout takes precedence.

Sources: https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/ and https://docs.hetzner.com/general/infrastructure-and-availability/ipv4-pricing/ . Read docs/HOSTING_COMPARISON.md and data/sources/hosting-comparison.json for complete dated evidence and alternative-provider calculations. No purchase or cloud provisioning has occurred. Start at one emulator when eventually authorized; >50 concurrent instances still requires explicit approval.

## ADR 010 — Local verification runtime (accepted for bootstrap verification only)
Host Python is 3.14 and Node is 26. Docker is absent. Production/API image and GitHub CI target Python 3.12; CI targets Node 22. Host checks supplement, and do not replace, the required target-runtime CI and Docker checks. P0 remains partial until those checks and publication/deployment requirements pass.
