# SimuFarm v3 decision register

Controlling brief: MASTER_PROMPT.md (v3). It supersedes every previous prompt, ADR and execution report. Pre-v3 documents are archived in docs/archive/pre-v3/. Interrupted pre-v3 uncommitted work was preserved in a named Git stash, not carried into Stage A.

Operator inputs were received: supplied repository, public visibility confirmed by GitHub, Oracle account confirmed active, ZERO_SPEND_CONFIRMED=yes and MOBILEAPI_KEY_STORED=yes. Keys/email are not published. No key/account API call is made. Work occurs on pivot/redroid-shell-first. Stage A was accepted and merged in PR #1. Stage B is authorized; Stage C requires separate acceptance.

## ADR 011 — Redroid ARM runtime (v3 supersession)
Redroid ARM64 replaces docker-android. No KVM, physical handsets, paid/trial hosts, per-model images or cloned /data volumes. Host plan2 OCPU / 12 GB Oracle Always Free, subject to later account-specific eligibility/capacity. Stage D owns provisioning, kernel validation, real boots and measurements. No VM or runtime container is needed or created during Stage A. Current runtime ceilings remain unvalidated; do not advertise capacity or identities as proven.

The requested redroid/redroid:12.0.0-arm64 tag must be verified in Stage D. A mutable tag, platform documentation, or old image metadata is not an instance boot. GApps/Magisk licensing and host compatibility remain future validation. Do not deploy or bake brand/model images now.

## ADR 012 — Shell-first copy-paste model
Three separate artifacts: handmade brand shells, sourced profile JSON and shared per-OS runtime images. Stage A builds one original Vivo-style Web Component and three manual India-variant profiles. A minimal deterministic static-page renderer reuses that one shell. Copying generated static assets is allowed; runtime image/data cloning is not. Stage C's CSV profile generator is deliberately not implemented before its gate.

Source profile layout: profiles/vivo/vivo-<model>.json. A draft static catalog is separate from the human-approved API/runtime admission path. Generated preview pages are clearly labeled as original artwork with pending human review. Physical PPI (some values derived) is not claimed as Android logical densityDpi or actual runtime identity.

## ADR 013 — Out-of-scope expansion
No 10,000-device expansion,1,000 concurrent emulators, physical-device farm, functional iOS runtime or paid infrastructure. Later stages must stay within the prompt's strict order, real capacity evidence and zero-spend limits. P6 from earlier briefs is retired.

## ADR 014 — Approved: honest unknowns for static-only drafts
Manufacturer specifications do not provide genuine ro.product.model, ro.product.device or ro.build.fingerprint values. Codex is not among the allowed verified_by values and no human has reviewed the facts yet. Do not fabricate firmware fingerprints, reuse example V100 values or claim a human reviewer.

**Approved by the operator with the Stage B addendum:** v0.3.0 retains all requested profile keys, with nullable build properties and nullable paired verified_by/verified_at for explicitly labeled static drafts. Runtime admission requires actual human approval and every build property non-null/nonblank. Strict profile promotion still rejects unreviewed drafts. Source-backed preview generation requires an explicit --allow-draft flag and labels its output. Stage B is authorized. Every runtime promotion additionally requires build.source_type (manufacturer_spec | lineageos_tree | xda_dump | firmware) and a nonempty build.sources URL list. All four properties must be literal, matching-device primary-source values. Firmware package names and inferred identifiers do not qualify. Static drafts retain null properties, null source_type and empty build.sources. Human technical review remains mandatory.

The requested dpi field is physical PPI for these static references: X100 452 is manufacturer-stated; Y100 413/V30 453 are calculated from manufacturer diagonal/resolution. Their derivation is recorded, not represented as OEM logical density. Notch classification is a visual inference with review pending. Artwork/bezel geometry is original/stylized, not dimensional hardware fidelity.

## Deferred contradictions — do not silently resolve
- Stage C allocation resolved: 20 brands × 50 rows = 1,000. At least three OS versions, two screen-size classes and two chipset families are required per brand. No Stage C extraction/generation is authorized yet.
- Shared per-OS images conflict with the per-brand Magisk baking sentence. Resolve before Stage E; no baking now.
- Fresh data does not prove every IMEI/GSF/advertising ID exists or differs on Redroid. Stage D must record actuals and fail missing/duplicate evidence instead of inventing values.
- binderfs supplies Binder IPC; it does not alone replace ashmem. Exact kernel/memfd choices require Stage D evidence.

## Stage B / Stage D gates
MOBILEAPI_KEY_STORED=yes was confirmed by the operator; no MobileAPI call is needed for Stage B and none is made. Conservative cap remains 50/month until dashboard verification. Re-verify PUBLIC repository visibility immediately before Stage D touches Oracle, even though it was verified for Stage A. No provisioning during Stage B.

## Operator addendum — Stage B accepted; Stage C authorized
Stage B static/interactive scope accepted. Missing Vivo build blocks are deferred and no longer block Stage C. All 1,000 generated profiles must deterministically emit build: null and runtime_eligible: false. Runtime admission remains separate: complete human-reviewed identities, consistent variants and field-level sources only. Stage E operates only on that subset. Third-party-device-db and firmware-dump evidence classes are authorized for candidate research; schema extension and human review precede promotion. Do not merge China X100 V2309A identity candidates into the India V2308 fingerprint without resolving the mismatch. Y100 additional extraction requires human region resolution. Stage D prep switches to verified 64only image tags and an inspected/pinned oci-arm-free-retry task, with no execution until Stage C acceptance.

## Stage C implementation addendum
Per-brand quota/diversity failures use explicit measured exemptions in data/devices.csv.exemptions.yaml; global 3 OS versions, 2 screen-size classes and 2 chipset families remain mandatory. Nothing target11; no invented or cosmetic/RAM duplicates. Missing notch geometry is represented explicitly as unknown in static drafts and omitted from artwork, never asserted as a hardware absence. Known reference build fragments remain separate; generated profiles always null/false. Runtime source enum includes third_party_device_db and firmware_dump, with human-review/complete-identity admission unchanged. X100 regional choice is needs-human and Stage D remains prepared-not-authorized.

## ADR 015 — OCI provisioning guardrails (binding)

Status: Superseded by Local Hardware Pivot (31 October 2026)
Context: Stage D requires a free-tier Oracle Always Free ARM VM to run Redroid. Oracle's free tier is capped at 2 OCPU / 12 GB per tenancy, capacity in home regions is frequently exhausted, and any mistake in shape, region, or billing model can silently accrue charges.

Decision:
1. Codex may ONLY launch shape `VM.Standard.A1.Flex` with `--shape-config '{"ocpus":2,"memoryInGBs":12}'`. Any other shape is a P0 defect. Stop immediately and report.
2. Preflight (already completed).
3. Retry policy: Use `oci-arm-free-retry` (or your prepared script) pinned to a specific commit. Bounded: max 500 attempts OR 24 hours, whichever first. Backoff: 60 seconds. Log every attempt outcome. Stop immediately on any error other than "Out of host capacity" — especially LimitExceeded, NotAuthenticated, NotAuthorizedOrNotFound must be distinguished. Do not retry through auth or quota errors.
4. No fallback. If capacity is not available in the home region within the bounds above, report and stop. Codex MUST NOT: Create a second Oracle account; Provision in a non-home region; Upgrade to pay-as-you-go; Provision a different shape; Use a trial or promotional credit.
5. Post-launch tagging and evidence: Immediately after a successful launch, tag the instance `--freeform-tags '{"project":"simufarm","tier":"always-free","stage":"D"}'`. Record instance OCID, shape, AD, public IP, launch timestamp, and preflight A1 availability to `data/runtime/oci-instance.json` BEFORE any SSH.
6. Reporting: After execution, report preflight results, attempt count, time-to-capacity, region/AD, instance OCID. Do not claim success unless the instance is confirmed at 2 OCPU / 12 GB.
7. Cost safety: Any observation of non-free billing MUST halt execution.

## ADR 016 — Local hardware Stage D over Meshnet

Status: Accepted (31 October 2026)

Stage D targets a user-owned Ubuntu22.04 server over its Meshnet IPv4 address using SSH. Oracle provisioning/retries and automatic Oracle API calls are disabled. Oracle cleanup commands are supplied for the user to run; cleanup has not been executed or verified by Codex. No paid cloud resources or MobileAPI calls are authorized. Await the IP and SSH username before any connection. Detect CPU architecture before selecting an immutable Redroid image; do not assume Ampere/ARM. KVM is optional and is recorded, not required or forbidden. Keep ADB bound to remote loopback and use SSH tunnels if needed. Human runtime-profile promotion and StageE remain separate gates.
